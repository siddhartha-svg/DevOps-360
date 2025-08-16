# 📂 Linux File System Hierarchy (FHS) Guide

The Linux File System Hierarchy Standard (FHS) is a fundamental concept for anyone working with Linux. It provides a consistent and logical structure for storing system files, binaries, libraries, and user data. This guide serves as a quick reference for the most important directories.

---

### 🌳 Root and Core Directories

-   **`/`**: The **root directory**. The top of the file system tree. Everything on a Linux system resides under this directory.
-   **`/boot`**: Contains files required for the system to boot, including the **kernel** and **bootloader (GRUB)**.
-   **`/etc`**: Holds **system-wide configuration files**. This is where you'll find settings for services, network configuration, and user information (`/etc/passwd`).
-   **`/home`**: The location for **individual user home directories** (`/home/john`, `/home/jane`).
-   **`/root`**: The home directory for the **root user**. It is kept separate from `/home` for security reasons.

---

### ⚙️ Programs and Libraries

-   **`/bin`**: **Essential user binaries**. Commands like `ls`, `cp`, and `mv` are here. These are required for all users and are critical for basic system function.
-   **`/sbin`**: **Essential system binaries**. Commands used for system administration, such as `shutdown` and `reboot`, that typically require root privileges.
-   **`/lib`**: **Shared libraries** needed by the binaries in `/bin` and `/sbin`.
-   **`/usr`**: Contains **user applications and resources**. A large directory with subdirectories for binaries, libraries, documentation, and source code.
-   **`/opt`**: **Optional software packages** from third-party vendors.

---

### 💾 Data, Devices, and Temporary Files

-   **`/dev`**: **Device files**. Represents hardware devices like hard drives (`/dev/sda`) and terminals.
-   **`/var`**: **Variable data**. Stores files that change during system operation, such as **system logs (`/var/log`)**, caches, and mail queues.
-   **`/tmp`**: **Temporary files**. A directory for transient files that can be deleted on system reboot.
-   **`/mnt`**: A temporary mount point for **mounting external file systems** manually.
-   **`/media`**: The standard location for **automounted removable media** like USB drives.

---

### 💻 Virtual and Service-Specific Directories

-   **`/proc`**: A **virtual file system** that provides a real-time view of kernel and process information.
-   **`/sys`**: Another **virtual file system** exposing information about hardware devices and the kernel.
-   **`/srv`**: Contains data for **services** provided by the system, such as web server data.
-   **`/run`**: A temporary file system for **runtime data** that's cleared at boot. Contains PID files and sockets.
-   **`/lost+found`**: Contains **recovered file fragments** after a file system check. Found on each partition.
