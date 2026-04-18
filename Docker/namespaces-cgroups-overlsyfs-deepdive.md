# Namespaces, cgroups & OverlayFS — Complete Deep Dive

> End-to-end reference covering all 7 Linux namespaces, cgroups v1/v2 with all controllers, and OverlayFS with every file operation — including how all three interconnect when Docker starts a container.

---

## Table of Contents

1. [Namespaces — Full Isolation System](#1-namespaces--full-isolation-system)
2. [cgroups — Full Resource Control System](#2-cgroups--full-resource-control-system)
3. [OverlayFS — Full Layered Filesystem System](#3-overlayfs--full-layered-filesystem-system)
4. [How All Three Work Together](#4-how-all-three-work-together)

---

# 1. Namespaces — Full Isolation System

---

## What Is a Namespace?

A namespace is a **kernel feature that wraps a global system resource inside an abstraction layer**, so that processes inside that namespace believe they have their own isolated instance of that resource — while the kernel manages the actual global resource underneath.

Every process on a Linux system **always belongs to exactly one namespace of each type**. When Linux boots, it creates a single **"initial namespace"** for each type. All processes start there. When Docker creates a container, it creates **new namespaces** and launches the container's processes inside them.

```
Linux Boot
│
├── Initial PID namespace      (all host processes live here)
├── Initial NET namespace      (host network lives here)
├── Initial MNT namespace      (host filesystem lives here)
├── Initial UTS namespace      (host hostname lives here)
├── Initial IPC namespace      (host IPC lives here)
├── Initial USER namespace     (host users live here)
└── Initial TIME namespace     (host clock lives here)

Docker creates a container:
├── New PID namespace          (container processes live here)
├── New NET namespace          (container network lives here)
├── New MNT namespace          (container filesystem lives here)
├── New UTS namespace          (container hostname lives here)
├── New IPC namespace          (container IPC lives here)
├── New USER namespace         (optional — rootless containers)
└── New TIME namespace         (optional — clock offset)
```

The kernel syscalls used to work with namespaces are:

| Syscall | Purpose |
|---------|---------|
| `clone()` | Create a new process in new namespaces |
| `unshare()` | Move current process into new namespaces |
| `setns()` | Join an existing namespace |

Docker uses `clone()` with flags like `CLONE_NEWPID`, `CLONE_NEWNET`, `CLONE_NEWNS`, etc.

---

## Namespace 1: PID Namespace

### What It Isolates
The **process ID number tree**. Every running process on Linux has a unique PID. The PID namespace creates a completely separate numbering system.

### How It Works in Depth

The Linux kernel maintains a **process tree** — a hierarchy rooted at PID 1 (init/systemd). Every process has a parent. When PID 1 dies, the kernel panics (on host) or kills the container (in Docker).

When Docker creates a PID namespace:

```
HOST KERNEL VIEW:
PID 1    → systemd          (host init)
PID 2    → kthreadd         (kernel thread)
PID 889  → dockerd          (Docker daemon)
PID 901  → containerd       (container runtime)
PID 1043 → node server.js   ← this IS the container's app
PID 1044 → node worker      ← this IS the container's worker

CONTAINER'S VIEW (inside the PID namespace):
PID 1    → node server.js   ← thinks it's the init process!
PID 2    → node worker
```

**The kernel maintains a mapping table:**
```
PID Namespace Table:
Container PID 1  ↔  Host PID 1043
Container PID 2  ↔  Host PID 1044
```

### Why PID 1 Matters Inside a Container
In Linux, PID 1 has special responsibilities:
- It must **reap zombie processes** (call `wait()` on dead children)
- If PID 1 exits → all other processes in that namespace are killed immediately
- Signals like `SIGTERM` go to PID 1

This is why Docker recommends using an **init system** (like `tini`) as PID 1 in containers — because your app (like `node`) may not handle zombie reaping correctly.

### Nested PID Namespaces
PID namespaces can be **nested**:

```
Root namespace (host)
└── Container namespace (level 1)
      └── Nested container namespace (level 2)
```

A process in level 2 has THREE PIDs:
- PID inside level 2 namespace (e.g., PID 1)
- PID inside level 1 namespace (e.g., PID 47)
- PID in root namespace (e.g., PID 2341)

The kernel tracks all mappings. A process in a **parent namespace can see all child PIDs**. A process in a **child namespace cannot see parent PIDs** — total blindness upward.

### Process Signals Across Namespaces
A host process can send signals to container processes using the **host PID**:
```bash
kill -9 1043    # kills container's PID 1 (node) from host
```
But the container cannot signal host processes at all — it doesn't even know their PIDs exist.

---

## Namespace 2: NET Namespace

### What It Isolates
The **entire network stack** — interfaces, routing tables, firewall rules (iptables), sockets, ports.

### How It Works in Depth

When a new NET namespace is created, it starts with:
- Only a **loopback interface** (`lo`) — not even brought up yet
- **Empty routing table**
- **Empty iptables rules**
- **Its own socket table** — no inherited connections

```
HOST NET namespace:
eth0       → 192.168.1.10    (physical NIC)
docker0    → 172.17.0.1      (Docker bridge — virtual switch)
veth3a2f   → (one end of a veth pair, connects to container)
lo         → 127.0.0.1

CONTAINER NET namespace:
eth0       → 172.17.0.2      (the other end of the veth pair)
lo         → 127.0.0.1
```

### The veth Pair — Virtual Ethernet Cable
Docker creates a **virtual ethernet pair (veth)** — a virtual network cable with two ends:

```
┌─────────────────────────────────────────────────┐
│  HOST NET namespace                             │
│  docker0 bridge (172.17.0.1)                    │
│       │                                         │
│   veth3a2f (host end)                           │
└────────┼────────────────────────────────────────┘
         │  ← virtual cable through kernel
┌────────┼────────────────────────────────────────┐
│   eth0 (container end)                          │
│   172.17.0.2                                    │
│  CONTAINER NET namespace                        │
└─────────────────────────────────────────────────┘
```

**Packet flow when container sends data to internet:**

```
Container app writes to socket
→ kernel routes via container's eth0 (172.17.0.2)
→ veth pair carries packet to host
→ host's docker0 bridge receives it
→ iptables NAT rule: rewrite source IP from 172.17.0.2 → 192.168.1.10
→ packet leaves via host's eth0 to internet
→ reply comes back, NAT rewrites destination back
→ packet delivered to container
```

### Port Mapping
When you run `docker run -p 8080:80`, Docker creates an **iptables DNAT rule** on the host:

```
iptables rule:
Incoming packet on host port 8080
→ rewrite destination to 172.17.0.2:80 (container)
→ forward into container's NET namespace
```

### Network Isolation Reality
Two containers in **different NET namespaces** cannot communicate directly. They must go through:
- Docker bridge network (default)
- Docker overlay network (Swarm/Kubernetes)
- Host network mode (share host's NET namespace — no isolation)

---

## Namespace 3: MNT (Mount) Namespace

### What It Isolates
The **filesystem mount table** — what is mounted where. Each process has a view of the filesystem tree, and the MNT namespace controls what that view contains.

### How It Works in Depth

In Linux, everything is a file. The **VFS (Virtual File System)** layer in the kernel presents a unified tree starting at `/`. Every filesystem is **mounted** at some point in this tree.

```
HOST mount table:
/           → ext4 on /dev/sda1
/proc       → procfs (kernel process info)
/sys        → sysfs (kernel device info)
/home       → ext4 on /dev/sda2
/var/lib/docker → overlay filesystem

CONTAINER mount table (completely separate):
/           → overlayfs (Docker image layers)
/proc       → new procfs (shows only container's processes)
/sys        → sysfs (read-only or restricted)
/dev        → tmpfs (virtual device files for container)
/etc/hosts  → bind mount (Docker injects host entries)
/etc/resolv.conf → bind mount (Docker injects DNS config)
```

### Bind Mounts

```bash
docker run -v /host/data:/container/data myimage
```

The kernel takes `/host/data` from the host's MNT namespace and makes it appear at `/container/data` in the container's MNT namespace. The **same inode** (actual data) is accessible from both sides.

### `/proc` Filesystem Inside Containers
Inside a container, `/proc` is a **new procfs** mounted in the container's MNT namespace. It shows:
- Only PIDs visible in the container's PID namespace
- Memory info scoped to the container
- The container's own network stats

Without this, running `ps aux` inside a container would show ALL host processes — a major security leak.

### Mount Propagation

| Mode | Behavior |
|------|---------|
| `private` | No propagation (default for containers) |
| `shared` | Mounts propagate in both directions |
| `slave` | Host mounts propagate in, but not out |
| `unbindable` | Cannot be bind-mounted |

Docker containers default to **private** propagation — a mount inside a container doesn't appear on the host, and new host mounts don't appear inside the container.

---

## Namespace 4: UTS Namespace

### What It Isolates
**UNIX Timesharing System** information — specifically the **hostname** and **NIS domain name** of the system.

### How It Works in Depth

When Docker creates a container, it calls `unshare(CLONE_NEWUTS)` and then `sethostname()` inside the new namespace.

```
HOST:
$ hostname
→ production-server-01

CONTAINER:
$ hostname
→ a3f2b1c9d4e5    ← Docker-assigned container ID (or custom name)
```

### Why It Matters
- Apps that use `gethostname()` to identify themselves get the **container's name**, not the host's name
- Logging systems see the right hostname per container
- Kubernetes sets the pod name as the hostname

```
Node.js app:
os.hostname() → "a3f2b1c9d4e5"   ← container's hostname
                                     NOT the host machine's name
```

---

## Namespace 5: IPC Namespace

### What It Isolates
**Inter-Process Communication** resources:
- **POSIX message queues** (`mq_open`, `mq_send`, `mq_receive`)
- **System V IPC**: shared memory segments (`shmget`), semaphore arrays (`semget`), message queues (`msgget`)

### How It Works in Depth

```
Without IPC namespace:
Container A creates shared memory: shmget(key=1234, size=1MB)
Container B can attach to it:     shmat(shmid from key 1234)
→ Direct memory access between containers! ← DANGEROUS

With IPC namespace:
Container A creates shared memory: shmget(key=1234) → shmid=3 (in Container A's IPC namespace)
Container B tries: shmget(key=1234) → gets ITS OWN object (in Container B's IPC namespace)
→ Completely isolated, no cross-container access
```

### Shared IPC Between Containers
Docker allows sharing an IPC namespace between containers:

```bash
docker run --ipc=container:container_A container_B
```

Used for **high-performance inter-container communication** — sharing a memory-mapped file without going through the network stack.

---

## Namespace 6: USER Namespace

### What It Isolates
**User IDs (UIDs) and Group IDs (GIDs)** — maps UIDs inside the container to different UIDs on the host.

### How It Works in Depth

Without USER namespaces, UID 0 (root) inside a container IS root on the host — a container escape gives full host root.

With USER namespaces:

```
INSIDE CONTAINER:      HOST KERNEL SEES:
UID 0 (root)      ↔    UID 100000 (unprivileged user)
UID 1 (daemon)    ↔    UID 100001
UID 1000 (app)    ↔    UID 101000
```

The mapping is stored in `/proc/[pid]/uid_map`:
```
0  100000  65536
```
This means: "Container UIDs 0–65535 map to host UIDs 100000–165535."

### Rootless Containers

```
TRADITIONAL (risky):
dockerd runs as root
container root → host root (if escaped)

ROOTLESS:
dockerd runs as UID 1000 (your user)
container root → host UID 100000 (still unprivileged)
container escape → attacker gets UID 100000, NOT root
```

### Linux Capabilities
Linux splits root power into individual **capability flags**:

| Capability | What it allows |
|-----------|---------------|
| `CAP_NET_BIND_SERVICE` | Bind to ports below 1024 |
| `CAP_SYS_PTRACE` | Debug other processes |
| `CAP_SYS_ADMIN` | Many administrative operations |
| `CAP_KILL` | Send signals to any process |

Docker **drops most capabilities** from containers by default, even if the container runs as root inside.

---

## Namespace 7: TIME Namespace (Linux 5.6+)

### What It Isolates
The **system clock offset** — specifically `CLOCK_MONOTONIC` and `CLOCK_BOOTTIME`.

### How It Works in Depth

```
HOST:
clock_gettime(CLOCK_BOOTTIME) → 86400 seconds (24 hours since boot)

CONTAINER with TIME namespace:
clock_gettime(CLOCK_BOOTTIME) → 120 seconds  ← container sees its own "uptime"
```

### Use Cases
- **Testing time-sensitive code** — make a container think only 5 minutes have passed
- **Checkpoint/restore (CRIU)** — when restoring a container from a snapshot, reset its clock
- **Live container migration** — move a container between hosts without time jumps breaking apps

---

# 2. cgroups — Full Resource Control System

---

## What Are cgroups?

**Control Groups (cgroups)** is a Linux kernel feature that **organizes processes into hierarchical groups** and applies **resource limits, accounting, and control** to each group.

While namespaces answer *"what can a process see?"*, cgroups answer *"how much can a process use?"*

There are two versions:
- **cgroups v1** — original, multiple hierarchies (Linux 2.6.24, 2008)
- **cgroups v2** — unified hierarchy, more consistent (Linux 4.5, 2016; default in modern systems)

---

## cgroups Architecture

cgroups are controlled through a **virtual filesystem** — you read and write files to control them:

```
/sys/fs/cgroup/               ← cgroup filesystem root (cgroups v2)
│
├── system.slice/             ← systemd's system services group
├── user.slice/               ← user session groups
└── docker/                   ← Docker's cgroup subtree
      │
      ├── <container_id_1>/   ← one cgroup per container
      │     ├── cgroup.procs          ← PIDs in this group
      │     ├── cpu.max               ← CPU limit
      │     ├── memory.max            ← RAM limit
      │     ├── memory.swap.max       ← swap limit
      │     ├── blkio.weight          ← disk I/O weight
      │     ├── pids.max              ← max processes
      │     └── ...
      │
      └── <container_id_2>/
```

To add a process to a cgroup, write its PID to `cgroup.procs`:
```bash
echo 1043 > /sys/fs/cgroup/docker/<container_id>/cgroup.procs
```
The kernel now enforces all limits in that cgroup on PID 1043 and all its children.

---

## cgroup Controller 1: CPU

### CPU Quota (Hard Limit)
```
cpu.max:  50000 100000
```
In every 100ms window (100000 microseconds), this cgroup can only use 50ms (50000 microseconds) of CPU time.

```
Timeline (ms):  0    50   100  150  200
                |████|    |████|    |████
                  run  stop  run  stop
                (50ms running) (50ms throttled)
```

If the container's processes use their 50ms quota, the kernel **throttles** them — they sleep until the next window.

### CPU Shares / Weight (Soft Limit)
```
cpu.weight: 100   ← default
cpu.weight: 200   ← gets 2x CPU time relative to weight-100 groups
```
Only matters when the system is **under contention**. If CPU is idle, a container can use 100% regardless.

### CPU Pinning (cpuset)
```
cpuset.cpus: 0-3        ← only use CPU cores 0, 1, 2, 3
cpuset.mems: 0          ← only use NUMA memory node 0
```
Used in **high-performance computing** to pin containers to specific cores, preventing cache thrashing.

### CPU Accounting
```
cpu.stat:
usage_usec      450000    ← 450ms total CPU time used
user_usec       380000    ← 380ms in user space
system_usec      70000    ← 70ms in kernel (syscalls)
throttled_usec  120000    ← 120ms throttled (hit quota)
```

---

## cgroup Controller 2: Memory

### Hard Memory Limit
```
memory.max: 536870912    ← 512MB hard limit
```

When a container's memory usage hits this limit, the kernel's **OOM (Out of Memory) Killer** is triggered **inside the cgroup only**:

```
Container uses 512MB → tries to allocate 1 more byte
→ kernel checks cgroup memory.max → LIMIT HIT
→ OOM killer selects a process inside the cgroup to kill
→ host is completely unaffected
→ container may restart (depends on Docker restart policy)
```

### Memory + Swap Limit
```
memory.max:       536870912    ← 512MB RAM
memory.swap.max:  0            ← no swap (common for containers)
```
Setting swap to 0 forces the container to only use RAM — OOM triggers immediately instead of slowing into swap.

### Memory High (Soft Limit / Throttling)
```
memory.high: 471859200    ← 450MB soft limit
memory.max:  536870912    ← 512MB hard limit
```
When usage exceeds `memory.high`, the kernel starts **reclaiming memory aggressively** — a warning signal before OOM.

### Memory Accounting

| Memory Type | Counted in cgroup? |
|------------|-------------------|
| Anonymous memory (heap, stack) | Yes |
| File-backed memory (mmap'd files) | Yes (can be reclaimed) |
| Page cache (filesystem reads) | Yes |
| Kernel memory for this cgroup | Yes (in v2) |
| Shared memory (tmpfs) | Yes |

### Memory Pressure Stall Information (PSI) — cgroups v2
```
memory.pressure:
some avg10=12.50 avg60=8.20 avg300=3.40 total=4523411
full avg10=0.00 avg60=0.00 avg300=0.00 total=0
```
PSI tells you the percentage of time tasks were **stalled waiting for memory** — enables proactive remediation before OOM crash.

---

## cgroup Controller 3: Block I/O (blkio / io)

### I/O Weight
```
io.weight: 100    ← default weight
```
Relative priority when multiple containers compete for disk I/O.

### I/O Rate Limiting (Throttle)
```
io.max: 8:0 rbps=10485760 wbps=5242880 riops=1000 wiops=500
```

This means for device `8:0` (e.g., `/dev/sda`):
- Max read: 10MB/s
- Max write: 5MB/s
- Max read IOPS: 1000
- Max write IOPS: 500

The kernel's block layer enforces this — requests are **queued/throttled** at the kernel level.

### I/O Accounting
```
io.stat: 8:0 rbytes=1073741824 wbytes=536870912 rios=4096 wios=2048
```
Exact byte-level read/write accounting per block device per container.

---

## cgroup Controller 4: PIDs

### How Process Count Limiting Works
```
pids.max: 100
```
The kernel refuses **any new `fork()` or `clone()` call** once the cgroup hits 100 processes.

```
Fork bomb without pids.max:
:(){ :|:& };:   ← bash fork bomb
→ exponential process creation
→ host runs out of PIDs → entire system freezes

With pids.max = 100:
→ after 100 processes, all further fork() calls return EAGAIN
→ damage contained to the container
→ host unaffected
```

---

## cgroup Controller 5: Network (net_cls / net_prio)

### Traffic Classification
```
net_cls.classid: 0x100010
```
Assigns a **traffic class ID** to all packets from this cgroup. The kernel's `tc` (traffic control) can then apply **QoS rules**:

```
Host tc rules:
class 0x10:  max 100Mbit/s  ← high priority containers
class 0x20:  max 10Mbit/s   ← low priority containers

Container A classid=0x10 → gets 100Mbit/s
Container B classid=0x20 → gets 10Mbit/s
```

---

## cgroup Controller 6: Devices

### Whitelisting Hardware Access
```
devices.allow: c 1:3 rwm    ← allow /dev/null (char device 1:3)
devices.allow: b 8:0 r      ← allow read from /dev/sda
devices.deny:  a             ← deny all other devices
```

By default Docker:
- **Denies** all raw device access
- **Allows** a safe whitelist: `/dev/null`, `/dev/zero`, `/dev/random`, `/dev/urandom`, `/dev/tty`
- **Denies** `/dev/sda` (raw disk), `/dev/mem` (physical memory), GPU devices (unless explicitly granted)

---

## cgroups v1 vs v2

| Feature | cgroups v1 | cgroups v2 |
|---------|-----------|---------
