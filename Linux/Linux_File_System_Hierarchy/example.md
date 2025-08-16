-----

### 📂 Real-World Linux File System Examples

This guide uses command-line examples to show you what you might find inside common Linux directories on a server named **`app-server-01`**. The user in this scenario is **`siddhu`**.

### `/` (Root Directory)

The root directory is the foundation of the file system. Listing its contents shows you the top-level structure.

```bash
siddhu@app-server-01:/$ ls
bin   dev  home  lib64       mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr
```

### `/home` (User Home Directories)

The `/home` directory holds personal directories for all non-root users. Here, we see home directories for `siddhu` and other users on the system.

```bash
siddhu@app-server-01:/home $ ls -lrt
total 8
drwxr-xr-x  2 siddhu     siddhu     4096 Apr 16 2025 siddhu
drwxr-xr-x  2 bob       bob        4096 Apr 16 2025 bob
drwxr-xr-x  3 appuser  appuser    4096 May 7  2025 appuser
drwxr-xr-x  2 sysadmin sysadmin   4096 Jun 4  2025 sysadmin
```

This output shows the directory permissions, owner, group, size, and last modification date. For example, `siddhu` owns his own directory and can read, write, and execute files within it. Other users cannot access his files.

### `/etc` (Configuration Files)

The `/etc` directory is for system-wide configuration. It's the central place for controlling how the system and its services behave.

```bash
siddhu@app-server-01:/etc $ ls
apache2/      bash.bashrc  cron.d/     fstab       hosts    nginx/    os-release
```

You can view the contents of a configuration file like `/etc/os-release` to get system information:

```bash
siddhu@app-server-01:/etc $ cat /etc/os-release
NAME="Ubuntu"
VERSION="22.04.4 LTS (Jammy Jellyfish)"
ID=ubuntu
VERSION_ID="22.04"
VERSION_CODENAME=jammy
UBUNTU_CODENAME=jammy
```

### `/var` (Variable Data)

The `/var` directory stores data that changes frequently, with logs being one of the most common types.

```bash
siddhu@app-server-01:/var $ ls -l /var/log/
total 165380
-rw-r--r-- 1 root root  1147047 Aug 15 10:45 auth.log
-rw-r--r-- 1 root root  2048995 Jul 28 11:21 boot.log
-rw-r--r-- 1 root root  3845667 Aug 16 10:45 dmesg
...
```

This shows the log files for system authentication, boot processes, and kernel messages, which are essential for troubleshooting.

### `/bin` and `/sbin` (Essential Binaries)

These directories contain the core executables required to operate the system.

```bash
siddhu@app-server-01:/$ ls /bin/
arch    bunzip2  cp    dash  echo   false   ln   mkdir  mv   ps   rm   sync   uncompress
...
```

These are the fundamental commands all users need. Binaries in `/sbin`, such as `reboot` or `fdisk`, are for administrative tasks and typically require root privileges to run.

### `/proc` (Virtual File System)

The `/proc` directory is a **virtual file system** that provides a real-time view of running processes and kernel data. It doesn't contain physical files on a disk.

```bash
siddhu@app-server-01:/$ ls /proc/ | head -n 15
1
10
11
12
13
14
15
16
17
18
19
2
20
21
22
```

The numbered directories correspond to the **Process IDs (PIDs)** of currently running processes. You can inspect files within these directories to get details about each process.
