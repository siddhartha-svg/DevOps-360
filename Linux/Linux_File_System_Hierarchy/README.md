# 📂 Linux File System Hierarchy (FHS) Guide

The Linux File System Hierarchy Standard (FHS) is a fundamental concept for anyone working with Linux. It provides a consistent and logical structure for storing system files, binaries, libraries, and user data. This guide serves as a quick reference for the most important directories.

---
Based on the image you uploaded, here is the Linux file system hierarchy presented in a text-based graph format using Markdown. This is ideal for a GitHub `README.md` file.

```markdown
🌳 Linux File System Hierarchy

```
```
/
├── boot/ (Boot Loader Files)
│
├── etc/ (Configuration Files)
│
├── home/ (User Home Directories)
│
├── root/ (Root Home Directory)
│
├── opt/ (Third-Party Applications)
│
├── dev/ (Device Files)
│
├── var/ (Variable Files)
│
├── bin/ (User Binaries)
│
├── sbin/ (System Binaries)
│
├── usr/ (User Applications)
│
├── proc/ (Process Information)
│
├── mnt/ (Mount Directory)
│
├── sys/ (Virtual File System)
│
├── media/ (Removable Devices)
│
├── run/ (Temporary File System)
│
├── tmp/ (Temporary Files)
│
├── lost+found/ (Recover Broken Files)
│
├── lib/ (System Libraries)
│
└── srv/ (Service Data Directory)
```

### Explanation of Directories

* **`/` (Root):** The top-level directory from which all other directories and files branch.
* **`/boot`:** Contains files needed to boot the system, such as the kernel and bootloader.
* **`/etc`:** Stores system-wide configuration files.
* **`/home`:** Houses individual user directories.
* **`/root`:** The home directory for the `root` (superuser) user.
* **`/opt`:** Contains optional, third-party software packages.
* **`/dev`:** Holds special files representing hardware devices.
* **`/var`:** Stores variable data that changes during system operation, such as log files and caches.
* **`/bin`:** Contains essential user command binaries (e.g., `ls`, `cp`).
* **`/sbin`:** Holds essential system binaries for administration (e.g., `reboot`, `fdisk`).
* **`/usr`:** The largest directory, containing user-level applications and libraries.
* **`/proc`:** A virtual file system providing real-time information about running processes.
* **`/mnt`:** A temporary mount point for external file systems.
* **`/sys`:** A virtual file system for interacting with hardware and kernel data.
* **`/media`:** Used for the automatic mounting of removable devices.
* **`/run`:** Stores runtime data for processes since the last boot.
* **`/tmp`:** A directory for temporary files that are automatically deleted on reboot.
* **`/lost+found`:** Holds recovered files from a file system check.
* **`/lib`:** Stores essential shared libraries used by programs in `/bin` and `/sbin`.
* **`/srv`:** Contains data for services offered by the system (e.g., web server data).
```

```
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
```
