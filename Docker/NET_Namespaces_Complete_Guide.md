# NET Namespaces — Complete End-to-End Guide
### Linux Container Networking, Docker Internals & Real-World Examples

---

## 🧠 Simple Mental Model (Start Here)

Imagine your **house has one main phone line** (host network).  
You build **separate rooms** (containers), and each room gets its **own private phone extension** with its own number.

The rooms can call each other through an **internal switchboard** (docker0 bridge).  
To call the outside world, every call gets **routed through the main line** — the outside world only ever sees the house number, never the room extension.

> **That's NET namespace. Each container gets a completely isolated network stack — its own phone system.**

---

## Part 1 — What a Network Stack Actually Is

Before understanding isolation, you need to know what's being isolated.

A **network stack** is everything needed to send/receive data:

```
┌─────────────────────────────────────────┐
│           FULL NETWORK STACK            │
├─────────────────────────────────────────┤
│  Network Interfaces  → eth0, lo, wlan0  │
│  IP Addresses        → 192.168.1.10     │
│  Routing Table       → where to send    │
│  iptables Rules      → firewall/NAT     │
│  Socket Table        → open connections │
│  Ports               → 80, 443, 3000    │
└─────────────────────────────────────────┘
```

Without NET namespaces, every process shares all of this.  
If Container A listens on port 80, Container B **cannot also listen on port 80** — port conflict.  
NET namespaces give each container its **own copy of the entire stack**.

---

## Part 2 — What a Brand New NET Namespace Starts With

When Docker creates a container, the new NET namespace starts completely empty:

```
NEW NET NAMESPACE (just born):
─────────────────────────────
Interfaces:    lo only (loopback, not even active yet)
IP Addresses:  none
Routing Table: empty
iptables:      empty
Sockets:       none
Ports in use:  none (completely fresh)
```

Compare to the **host NET namespace** at the same time:

```
HOST NET NAMESPACE:
──────────────────────────────────────────────
eth0       → 192.168.1.10    (physical NIC to router)
docker0    → 172.17.0.1      (Docker's virtual switch)
veth3a2f   → no IP           (cable end to container 1)
veth7b1c   → no IP           (cable end to container 2)
lo         → 127.0.0.1       (loopback)

Routing Table:
  default via 192.168.1.1 dev eth0    (internet → router)
  172.17.0.0/16 dev docker0           (docker traffic → bridge)

iptables:
  MASQUERADE rule (NAT for outbound container traffic)
  DNAT rules for each port mapping (-p 8080:80 etc.)
```

---

## Part 3 — The veth Pair (The Virtual Ethernet Cable)

This is the most important mechanism to understand.  
Docker connects the host and container using a **veth pair** — a virtual cable with two ends.

Think of it like **two tin cans connected by a string**.  
Whatever you put in one end comes out the other — instantly, in kernel memory.

```
┌──────────────────────────────────────────────────┐
│              HOST NET NAMESPACE                  │
│                                                  │
│   docker0 bridge (172.17.0.1) ← virtual switch  │
│         │                                        │
│    veth3a2f ← (host end of cable, no IP)         │
└─────────────│────────────────────────────────────┘
              │  ← virtual cable through kernel memory
┌─────────────│────────────────────────────────────┐
│        eth0 (172.17.0.2) ← container end         │
│        lo   (127.0.0.1)                          │
│         CONTAINER NET NAMESPACE                  │
└──────────────────────────────────────────────────┘
```

### How Docker creates this (under the hood):

```bash
# Step 1: Create veth pair
ip link add veth3a2f type veth peer name eth0

# Step 2: Move one end into the container namespace
ip link set eth0 netns <container_namespace>

# Step 3: Attach host end to docker bridge
ip link set veth3a2f master docker0

# Step 4: Assign IP inside container
ip -n <container_namespace> addr add 172.17.0.2/16 dev eth0

# Step 5: Bring interfaces up
ip link set veth3a2f up
ip -n <container_namespace> link set eth0 up
ip -n <container_namespace> link set lo up
```

### See it yourself:

```bash
# See all veth pairs on host
ip link show type veth

# Output:
# 6: veth3a2f@if5: <BROADCAST,MULTICAST,UP>
#     link/ether 3a:2f:...
#     master docker0          ← attached to docker bridge
# Each running container adds one veth to the host
```

---

## Part 4 — Full Packet Journey (Container → Internet)

Let's trace a real HTTP request from a Node.js app inside a container to `api.github.com`.

```javascript
// Your Node.js app inside the container:
fetch('https://api.github.com/users')
```

### Step-by-Step Packet Journey:

```
STEP 1 — App opens a socket
────────────────────────────
Node.js calls: connect(socket, api.github.com:443)
Kernel resolves DNS → 140.82.121.5
Container socket table: { src: 172.17.0.2:54321, dst: 140.82.121.5:443 }


STEP 2 — Container's routing table decision
────────────────────────────────────────────
Container routing table:
  default via 172.17.0.1 dev eth0   ← "anything not local → send to gateway"

Packet headers:  src=172.17.0.2   dst=140.82.121.5
→ matches default route
→ send to gateway 172.17.0.1 via eth0


STEP 3 — Packet crosses the veth pair
───────────────────────────────────────
Container's eth0 (172.17.0.2)
    ↓  [veth cable — kernel memory transfer]
Host's veth3a2f
    ↓
docker0 bridge receives it (172.17.0.1)


STEP 4 — Host's iptables NAT (MASQUERADE)
──────────────────────────────────────────
iptables rule on host:
  -t nat -A POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE

Translation:
  Packet in:   src=172.17.0.2:54321   dst=140.82.121.5:443
  Packet out:  src=192.168.1.10:54321 dst=140.82.121.5:443
                   ↑
         container IP replaced with HOST IP
         GitHub never sees 172.17.0.2 — ever


STEP 5 — Packet leaves host
────────────────────────────
→ out through host's eth0 (192.168.1.10)
→ to router (192.168.1.1)
→ to internet
→ reaches GitHub's servers (140.82.121.5)


STEP 6 — Reply comes back
───────────────────────────
GitHub responds to: 192.168.1.10:54321

iptables connection tracking (remembers the NAT mapping):
  192.168.1.10:54321 ↔ 172.17.0.2:54321

Reverse NAT:
  Packet in:   src=140.82.121.5:443  dst=192.168.1.10:54321
  Packet out:  src=140.82.121.5:443  dst=172.17.0.2:54321

→ Packet crosses veth back into container namespace
→ Container's eth0 receives it
→ Node.js gets its response ✅
```

> **GitHub only ever saw `192.168.1.10` — never knew a container existed.**

---

## Part 5 — Port Mapping Deep Dive (`-p 8080:80`)

When you run:

```bash
docker run -p 8080:80 nginx
```

Docker creates an **iptables DNAT rule** on the host:

```bash
# What Docker actually creates:
iptables -t nat -A DOCKER \
  -p tcp \
  --dport 8080 \
  -j DNAT \
  --to-destination 172.17.0.2:80

# In plain English:
# "Any TCP packet arriving on host port 8080
#  → rewrite destination to 172.17.0.2:80
#  → forward into the container"
```

### Full journey of an incoming request:

```
curl http://your-server:8080

Request arrives at host on port 8080
        ↓
Host iptables PREROUTING chain:
  "dport 8080? → DNAT to 172.17.0.2:80"
        ↓
Kernel forwards to docker0 bridge
        ↓
veth pair carries packet into container
        ↓
Container's eth0 receives: dst=172.17.0.2:80
        ↓
nginx inside container gets the request ✅
nginx thinks: "someone hit me on port 80"
(has no idea port 8080 was involved at all)
```

### Verify it yourself:

```bash
# Start nginx with port mapping
docker run -d -p 8080:80 nginx

# See the iptables DNAT rule Docker created
iptables -t nat -L DOCKER -n --line-numbers

# Output:
# Chain DOCKER
# num  target  prot  source     destination
#  1   DNAT    tcp   0.0.0.0/0  0.0.0.0/0   tcp dpt:8080 to:172.17.0.2:80
```

---

## Part 6 — Container-to-Container Communication

### Same Docker Network — Direct Communication ✅

```
Container A (172.17.0.2)
        ↓ via eth0
    veth (host end)
        ↓
   docker0 bridge (172.17.0.1) ← acts like a switch
        ↓
    veth (host end)
        ↓ via eth0
Container B (172.17.0.3)
```

No NAT needed — same subnet, bridge forwards directly.

```bash
# Test container-to-container communication:
docker run -d --name containerB nginx
docker run -it --name containerA ubuntu bash

# Inside containerA:
curl http://172.17.0.3:80        # by IP ✅
curl http://containerB:80        # Docker DNS resolves name ✅
```

---

### Different Docker Networks — Blocked by Default ❌

```bash
# Create two isolated networks
docker network create network_A    # 172.18.0.0/16
docker network create network_B    # 172.19.0.0/16

docker run -d --network network_A --name appA nginx
docker run -d --network network_B --name appB nginx

# appA CANNOT reach appB
# Different bridges, no route between them
# Like two separate VLANs — intentional isolation
```

---

### Host Network Mode — Zero Isolation

```bash
docker run --network host nginx
# nginx binds directly to HOST's eth0
# port 80 on container = port 80 on host
# No veth, no bridge, no NAT
# Fastest performance, but zero network isolation
```

```
Normal mode:                Host Network mode:
──────────────────          ──────────────────────────
Container eth0              Container shares HOST eth0
  172.17.0.2                192.168.1.10 (same as host!)
     ↓ veth                 No veth pair
  docker0 bridge            No docker0 bridge
  172.17.0.1                No NAT translation
     ↓                      Direct kernel network stack
  host eth0
  192.168.1.10
```

---

## Part 7 — Real World: 3-Tier Microservices App

```bash
# Create an isolated app network
docker network create appnet

# Deploy services
docker run -d --network appnet --name postgres postgres:14
docker run -d --network appnet --name api node:18 node server.js
docker run -d --network appnet -p 80:3000 --name nginx nginx
```

### What the network looks like:

```
INTERNET
    ↓
HOST eth0 (192.168.1.10)
    ↓  iptables: DNAT port 80 → 172.20.0.4:3000
docker bridge "appnet" (172.20.0.1)
    ├── postgres  172.20.0.2   port 5432 — NOT exposed to internet
    ├── api       172.20.0.3   port 3000 — NOT exposed to internet
    └── nginx     172.20.0.4   port 3000 → host port 80 ✅
```

### Traffic flow:

```
User hits http://your-server:80
  ↓
iptables DNAT → nginx container (172.20.0.4:3000)
  ↓
nginx proxies → api (172.20.0.3:3000)      ← internal, no NAT
  ↓
api queries → postgres (172.20.0.2:5432)   ← internal, no NAT
  ↓
postgres → api → nginx → user ✅
```

> **Postgres and API are completely invisible from the internet.**  
> They live in their own NET namespaces but share the appnet bridge.

---

## Part 8 — Hands-On Debugging Commands

```bash
# ── See container's network interfaces ────────────────────────
docker exec mycontainer ip addr
# 1: lo: <LOOPBACK,UP>
#     inet 127.0.0.1/8
# 5: eth0: <BROADCAST,MULTICAST,UP>
#     inet 172.17.0.2/16    ← container IP

# ── See container's routing table ─────────────────────────────
docker exec mycontainer ip route
# default via 172.17.0.1 dev eth0   ← gateway = docker bridge
# 172.17.0.0/16 dev eth0            ← local subnet

# ── Enter container's network namespace from host ──────────────
docker inspect mycontainer | grep '"Pid"'
# "Pid": 15234
nsenter -t 15234 -n ip addr    # see container's net from host

# ── See docker bridge on host ──────────────────────────────────
ip addr show docker0
# inet 172.17.0.1/16    ← docker bridge IP

# ── See all veth pairs ─────────────────────────────────────────
ip link show type veth
# 6: veth3a2f@if5: master docker0   ← one per running container

# ── See all iptables rules Docker created ─────────────────────
iptables -t nat -L -n -v
# Shows DNAT rules for port mappings
# Shows MASQUERADE rule for outbound NAT

# ── Watch live traffic on the bridge ──────────────────────────
tcpdump -i docker0 -n
# Shows all packets crossing the docker bridge live

# ── Match veth on host to interface inside container ──────────
cat /sys/class/net/veth3a2f/ifindex  # e.g., 6 (on host)
# Inside container:
cat /sys/class/net/eth0/iflink       # e.g., 6 — they match! ✅
```

---

## Part 9 — Kubernetes Networking (NET Namespaces at Scale)

In Kubernetes, every **Pod** gets its own NET namespace.  
But all containers **inside a Pod share** the same NET namespace.

```
NODE (host)
├── Pod A NET namespace (10.244.0.5)
│    ├── nginx container      ← shares eth0 @ 10.244.0.5
│    ├── app container        ← shares eth0 @ 10.244.0.5
│    └── pause container      ← holds the namespace open (infra container)
│
├── Pod B NET namespace (10.244.0.6)
│    ├── api container        ← 10.244.0.6
│    └── sidecar container    ← 10.244.0.6 (same IP!)
│
└── CNI plugin (Flannel/Calico) bridges pods across nodes
```

### Containers in the same Pod communicate via localhost:

```bash
# nginx (port 80) and app sidecar in same Pod:
# nginx calls:  curl http://localhost:3000   → hits app container ✅
# app calls:    curl http://localhost:80     → hits nginx ✅
# They share the same NET namespace — it's like one machine
```

### Pods on different nodes communicate via CNI:

```
Node 1 Pod (10.244.0.5)
    ↓ CNI overlay (VXLAN/BGP)
Node 2 Pod (10.244.1.8)
```

The CNI plugin (Flannel, Calico, Cilium) creates a virtual network that spans all nodes — each Pod gets a routable IP across the entire cluster.

---

## Summary Cheat Sheet

| Concept | Simple Explanation |
|---|---|
| **NET Namespace** | Each container gets its own complete network stack — interfaces, IPs, ports, firewall |
| **veth pair** | Virtual cable with two ends — connects container's eth0 to host's bridge |
| **docker0 bridge** | Virtual switch on host — connects all containers on the default network |
| **MASQUERADE / NAT** | Hides container's private IP — replaces with host IP for outbound traffic |
| **DNAT (port mapping)** | `-p 8080:80` — iptables rewrites incoming port 8080 → container port 80 |
| **Host network mode** | `--network host` — container shares host NET namespace directly, no isolation |
| **Same network** | Containers communicate directly via bridge, no NAT needed |
| **Different networks** | Blocked by default — like separate VLANs |
| **Kubernetes Pod** | All containers in a Pod share ONE NET namespace — talk via localhost |
| **CNI plugin** | Kubernetes networking layer — gives every Pod a routable IP cluster-wide |

---

## The Bottom Line

```
Without NET namespaces:
→ All containers share one network
→ Port conflicts everywhere
→ Any container can sniff any other container's traffic
→ No isolation at all ❌

With NET namespaces:
→ Each container has its own eth0, its own IP, its own ports
→ Container A can run :80, Container B can run :80 — no conflict ✅
→ Containers can't see each other's traffic unless on same network ✅
→ Outside world only sees the host IP — containers are invisible ✅
```

> **NET namespace is what makes port mapping, container networking, and service isolation possible.**  
> Every `-p` flag you've ever used, every microservice that "just works" — it's all NET namespaces and iptables under the hood.

---

## Comparison: PID vs NET Namespace

| | PID Namespace | NET Namespace |
|---|---|---|
| **Isolates** | Process IDs | Network stack |
| **Key mechanism** | Kernel mapping table | veth pairs + bridge |
| **Host can see container** | Yes (real PIDs) | Yes (via veth/iptables) |
| **Container can see host** | No (blind upward) | No (separate stack) |
| **Most common problem** | Zombie processes, PID 1 signals | Port conflicts, routing issues |
| **Debug tool** | `ps`, `/proc/<pid>/ns/pid` | `ip`, `iptables`, `tcpdump` |

---

*Next topics to go deeper: Mount Namespaces → UTS Namespaces → cgroups → seccomp*
