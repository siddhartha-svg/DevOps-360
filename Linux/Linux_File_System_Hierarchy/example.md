### **`/` (Root Directory)**
The root directory is the top-level directory in the Linux file system hierarchy. Everything else branches out from here.

-   `/bin`: Essential user command binaries.
-   `/sbin`: Essential system binaries.
-   `/etc`: System-wide configuration files.
-   `/usr`: User utilities and applications.
-   `/var`: Variable data files.
-   `/tmp`: Temporary files.
-   `/dev`: Device files.
-   `/proc`: Virtual file system for process information.
-   `/sys`: Virtual file system for kernel and device information.
-   `/home`: User home directories.
-   `/root`: Home directory for the root user.
-   `/boot`: Boot loader files.
-   `/lib`: Essential shared libraries.
-   `/lib64`: Shared libraries for 64-bit systems.
-   `/mnt`: Temporary mount points for external file systems.
-   `/media`: Mount points for removable media.
-   `/srv`: Service data.
-   `/opt`: Optional third-party software packages.
-   `/run`: Runtime data.
-   `/lost+found`: Recovered files after a file system check.

***

### **`/bin` (User Binaries)**
This directory holds essential command-line binaries available to all users. These are fundamental for basic system operation.

-   `ls`: Lists directory contents.
-   `cp`: Copies files and directories.
-   `mv`: Moves or renames files and directories.
-   `rm`: Removes files or directories.
-   `cat`: Concatenates and displays file contents.
-   `grep`: Searches for patterns in files.
-   `echo`: Displays a line of text.
-   `date`: Prints or sets the system date and time.
-   `mkdir`: Creates new directories.
-   `pwd`: Prints the current working directory.
-   `chmod`: Changes file permissions.
-   `chown`: Changes file ownership.
-   `df`: Reports file system disk space usage.
-   `mount`: Mounts a file system.
-   `umount`: Unmounts a file system.
-   `tar`: Archives and extracts files.
-   `gzip`: Compresses files.
-   `ping`: Tests network connectivity.
-   `su`: Switches user identity.
-   `sleep`: Delays for a specified amount of time.

***

### **`/etc` (Configuration Files)**
This directory contains **system-wide configuration files**. These are typically static and control how the system and services behave.

-   `/etc/passwd`: Stores user account information.
-   `/etc/group`: Stores group information.
-   `/etc/shadow`: Stores encrypted user passwords.
-   `/etc/fstab`: Defines file systems to be mounted at boot.
-   `/etc/hosts`: Maps hostnames to IP addresses.
-   `/etc/hostname`: Sets the system's hostname.
-   `/etc/crontab`: Schedules cron jobs.
-   `/etc/resolv.conf`: Configures DNS resolvers.
-   `/etc/ssh/sshd_config`: SSH daemon configuration file.
-   `/etc/sudoers`: Defines which users can execute commands as root.
-   `/etc/apt/sources.list`: APT package manager repository list.
-   `/etc/nginx/nginx.conf`: Nginx web server configuration.
-   `/etc/httpd/httpd.conf`: Apache web server configuration.
-   `/etc/my.cnf`: MySQL database configuration.
-   `/etc/systemd/system`: Systemd unit files for services.
-   `/etc/network/interfaces`: Network interface configuration.
-   `/etc/profile`: System-wide startup script for all users.
-   `/etc/bash.bashrc`: System-wide Bash configuration.
-   `/etc/issue`: Pre-login text message.
-   `/etc/rc.local`: Script executed at the end of the boot process.

***

### **`/usr` (User Utilities and Applications)**
This is a large directory containing user-level applications, libraries, and documentation. This is where most installed software resides.

-   `/usr/bin`: General user-level executables.
-   `/usr/sbin`: Non-essential system administration binaries.
-   `/usr/lib`: Libraries for programs in `/usr/bin` and `/usr/sbin`.
-   `/usr/local`: Hierarchical directory for local installations.
-   `/usr/share`: Architecture-independent data (e.g., documentation, fonts).
-   `/usr/include`: Header files for C/C++ development.
-   `/usr/src`: Source code for the Linux kernel and other packages.
-   `/usr/man`: Manual pages (documentation).
-   `/usr/games`: Games and educational software.
-   `/usr/etc`: Configuration files for programs in `/usr`.
-   `/usr/bin/git`: Git version control executable.
-   `/usr/bin/python3`: Python 3 interpreter.
-   `/usr/sbin/apachectl`: Apache web server control utility.
-   `/usr/lib/python3/dist-packages`: Python libraries.
-   `/usr/share/doc`: Documentation for installed packages.
-   `/usr/share/man/man1/ls.1.gz`: Compressed manual page for `ls`.
-   `/usr/local/bin`: Locally installed user binaries.
-   `/usr/local/lib`: Locally installed libraries.
-   `/usr/src/linux-headers-5.15.0-78`: Linux kernel headers.
-   `/usr/share/applications`: Desktop application launcher files.

***

### **`/var` (Variable Data)**
This directory holds **data that is expected to change frequently**, such as logs, caches, and temporary files.

-   `/var/log`: System and application log files.
-   `/var/www`: Web server data directory.
-   `/var/tmp`: Temporary files that are preserved between reboots.
-   `/var/cache`: Application caches.
-   `/var/lib`: State information for programs (e.g., databases, package manager data).
-   `/var/spool`: Queued jobs (e.g., print jobs, mail).
-   `/var/lock`: Lock files that prevent multiple processes from using the same resource.
-   `/var/run`: Obsolete, now a symbolic link to `/run`.
-   `/var/log/syslog`: General system log.
-   `/var/log/nginx/access.log`: Nginx web server access log.
-   `/var/www/html`: Default web root directory.
-   `/var/cache/apt`: APT package manager cache.
-   `/var/lib/apt/lists`: APT package lists.
-   `/var/lib/docker`: Docker's storage location for images and containers.
-   `/var/spool/mail`: User mailboxes.
-   `/var/lock/subsys`: Obsolete, lock files for old SysVinit scripts.
-   `/var/tmp/mysql.sock`: MySQL server socket file.
-   `/var/mail`: Mail spool directory (often a symlink to `/var/spool/mail`).
-   `/var/lib/mysql`: MySQL database files.
-   `/var/lib/dpkg`: DPKG package manager state information.

***

### **`/tmp` (Temporary Files)**
This directory is for **temporary files** created by users and applications. Its contents are often deleted on system reboot.

-   `/tmp/systemd-private-e8674d8122...`: A temporary directory used by a system service.
-   `/tmp/vmware-root/`: A temporary directory for VMWare.
-   `/tmp/app.lock`: A lock file created by an application to prevent multiple instances from running.
-   `/tmp/user-files-12345/`: A temporary directory created by a script.
-   `/tmp/session-1234.tmp`: A session file.
-   `/tmp/.X11-unix/`: Sockets for the X Window System.
-   `/tmp/mysql.sock`: A socket file for a local MySQL connection.
-   `/tmp/tempfile.txt`: A temporary text file.
-   `/tmp/log.txt`: A temporary log file.
-   `/tmp/cache/`: A temporary cache directory.
-   `/tmp/.font-unix/`: Font-related socket files.
-   `/tmp/systemd-private-a38b...`: Another systemd private temporary directory.
-   `/tmp/.ICE-unix/`: ICE protocol socket files.
-   `/tmp/gdm-wayland-sessions/`: GDM session files for Wayland.
-   `/tmp/ssh-agent.socket`: SSH agent socket.
-   `/tmp/.s.PGSQL.5432`: PostgreSQL socket.
-   `/tmp/user_sessions`: A directory for user session data.
-   `/tmp/app_data/`: A temporary directory for application data.
-   `/tmp/dbeaver-1234.lock`: A lock file for a database client.
-   `/tmp/vscode-socket-5678`: VS Code remote session socket.

***

### **`/dev` (Device Files)**
This directory contains special files that **represent hardware devices**. These are not normal files; they are interfaces to devices. 

-   `/dev/null`: A "null device" that discards all data written to it.
-   `/dev/zero`: A source of an infinite stream of zero-valued bytes.
-   `/dev/random`: A source of random data.
-   `/dev/urandom`: A source of "pseudo-random" data.
-   `/dev/sda`: The first hard disk in the system.
-   `/dev/sdb`: The second hard disk.
-   `/dev/sda1`: The first partition on the first hard disk.
-   `/dev/sr0`: The first CD-ROM or DVD-ROM drive.
-   `/dev/tty`: The controlling terminal for the current process.
-   `/dev/console`: The system console.
-   `/dev/pts/0`: The first pseudo-terminal.
-   `/dev/loop0`: The first loop device.
-   `/dev/mapper/centos-root`: LVM logical volume for the root file system.
-   `/dev/mem`: A character device that provides access to physical memory.
-   `/dev/cpu/0/cpuid`: A character device for accessing CPU registers.
-   `/dev/kmsg`: A character device for reading kernel messages.
-   `/dev/fuse`: A device for the FUSE file system.
-   `/dev/hda`: Obsolete, IDE hard disk.
-   `/dev/eth0`: Obsolete, a network interface.
-   `/dev/net/tun`: A device for network tunneling.
-   `/dev/usbmon0`: A device for monitoring USB traffic.

***

### **`/proc` (Process Information)**
This is a **virtual file system** that provides real-time information about running processes and the kernel. Files here are generated on the fly.

-   `/proc/1`: Directory for the init process (PID 1).
-   `/proc/self`: Symbolic link to the directory of the current process.
-   `/proc/cpuinfo`: Information about the CPU.
-   `/proc/meminfo`: Information about system memory.
-   `/proc/version`: The Linux kernel version.
-   `/proc/uptime`: System uptime.
-   `/proc/mounts`: Currently mounted file systems.
-   `/proc/filesystems`: Supported file systems.
-   `/proc/loadavg`: System load average.
-   `/proc/net/dev`: Network device statistics.
-   `/proc/sys/kernel/hostname`: System hostname.
-   `/proc/sys/vm/swappiness`: Swappiness setting.
-   `/proc/cmdline`: Kernel boot command line.
-   `/proc/modules`: Loaded kernel modules.
-   `/proc/partitions`: Disk partitions.
-   `/proc/cgroups`: Cgroup information.
-   `/proc/sched_debug`: Scheduler information.
-   `/proc/diskstats`: Disk statistics.
-   `/proc/buddyinfo`: Memory allocator information.
-   `/proc/pci`: PCI device information.

***

### **`/sys` (Kernel and Device Information)**
This is another **virtual file system** that provides a structured view of the hardware devices and the kernel's view of the system.

-   `/sys/class/net/eth0`: Directory for the `eth0` network interface.
-   `/sys/block/sda`: Directory for the first SATA disk.
-   `/sys/devices/pci0000:00/0000:00:01.0`: A PCI device.
-   `/sys/kernel/mm/hugepages`: HugePages memory information.
-   `/sys/bus`: Information about kernel buses.
-   `/sys/firmware`: Firmware-related information.
-   `/sys/fs`: File systems mounted with `sysfs`.
-   `/sys/module`: Information about loaded kernel modules.
-   `/sys/power/state`: Power state of the system.
-   `/sys/firmware/acpi`: ACPI-related information.
-   `/sys/class/power_supply/BAT0`: Battery information.
-   `/sys/class/net/eth0/address`: MAC address of `eth0`.
-   `/sys/class/net/eth0/operstate`: Operational state of `eth0`.
-   `/sys/class/net/eth0/speed`: Network link speed.
-   `/sys/devices/system/cpu/cpu0`: Information about the first CPU core.
-   `/sys/devices/system/cpu/cpu0/online`: Online status of the first CPU core.
-   `/sys/devices/system/cpu/cpufreq`: CPU frequency scaling.
-   `/sys/devices/pci.../00:02.0/drm/card0/device/power_state`: Graphics card power state.
-   `/sys/class/block/sda/size`: Size of the hard disk.
-   `/sys/class/backlight`: Backlight control.

***

### **`/home` (User Home Directories)**
This is the default location for individual user files, settings, and documents. Each user has their own directory.

-   `/home/john`: Home directory for user `john`.
-   `/home/mary`: Home directory for user `mary`.
-   `/home/siddhu`: Home directory for user `siddhu`.
-   `/home/john/Documents`: A directory for documents.
-   `/home/mary/Downloads`: A directory for downloads.
-   `/home/siddhu/projects`: A directory for project files.
-   `/home/john/.bashrc`: A hidden file for user-specific Bash configurations.
-   `/home/mary/.ssh`: A hidden directory for SSH keys.
-   `/home/siddhu/Pictures`: A directory for pictures.
-   `/home/john/.profile`: A hidden file for user-specific environment variables.
-   `/home/mary/.config/`: A hidden directory for application configurations.
-   `/home/siddhu/Public`: A directory for publicly shared files.
-   `/home/john/.local/share`: A hidden directory for local user data.
-   `/home/mary/Templates`: A directory for document templates.
-   `/home/siddhu/.mozilla/firefox`: Firefox profile directory.
-   `/home/john/.gnupg`: GnuPG key directory.
-   `/home/mary/Videos`: A directory for video files.
-   `/home/siddhu/.gitconfig`: Git configuration file.
-   `/home/john/.local/bin`: A directory for user-specific binaries.

***

### **`/root` (Root Home Directory)**
This is the home directory of the **root user**. It is separate from `/home` for security reasons and contains the root user's unique configuration files.

-   `/root/.bashrc`: Root user's Bash configuration.
-   `/root/.profile`: Root user's environment variables.
-   `/root/.ssh`: Root user's SSH keys.
-   `/root/.gnupg`: Root user's GnuPG key directory.
-   `/root/.vimrc`: Root user's Vim editor configuration.
-   `/root/.vim/`: Root user's Vim configuration directory.
-   `/root/.local/share`: Root user's local data directory.
-   `/root/.local/bin`: Root user's local binary directory.
-   `/root/.config`: Root user's application configuration directory.
-   `/root/.bash_history`: Root user's command history.
-   `/root/Documents`: A directory for documents (if created by root).
-   `/root/scripts`: A directory for root's scripts.
-   `/root/log`: A directory for root's personal logs.
-   `/root/.cache`: Root user's cache directory.
-   `/root/.bash_aliases`: Root user's Bash aliases.
-   `/root/bin`: Root user's private binary directory.
-   `/root/.gitconfig`: Root user's Git configuration.
-   `/root/.gnome/`: Root user's GNOME settings.
-   `/root/backups`: A directory for backups.
-   `/root/tmp`: A temporary directory for root.

***

### **`/boot` (Boot Loader Files)**
Contains essential files for the system to boot, including the Linux kernel and the GRUB bootloader configuration.

-   `vmlinuz-5.15.0-78-generic`: The Linux kernel image.
-   `initrd.img-5.15.0-78-generic`: The initial RAM disk image.
-   `grub/grub.cfg`: The main GRUB configuration file.
-   `grub/grubenv`: The GRUB environment block.
-   `System.map-5.15.0-78-generic`: Kernel symbol table.
-   `config-5.15.0-78-generic`: Kernel configuration file.
-   `grub/fonts/`: Fonts for the GRUB menu.
-   `grub/themes/`: Themes for the GRUB menu.
-   `grub/locale/`: Localization files for GRUB.
-   `grub/efi/`: EFI-related files.
-   `grub/i386-pc/`: GRUB modules for BIOS-based systems.
-   `grub/x86_64-efi/`: GRUB modules for UEFI-based systems.
-   `lost+found/`: Directory for file system recovery.
-   `efi/EFI/ubuntu/grubx64.efi`: EFI bootloader for Ubuntu.
-   `efi/EFI/boot/bootx64.efi`: Generic EFI bootloader.
-   `boot/grub/grub-mkconfig_lib`: GRUB library.
-   `boot.log`: Log file of the boot process.
-   `loader/`: Systemd-boot configuration directory.
-   `bootmgr`: A Windows boot manager file (in dual-boot systems).
-   `BOOT-INFO/`: A directory for boot information.

***

### **`/lib` (System Libraries)**
Stores essential shared libraries needed by the binaries in `/bin` and `/sbin`. These are critical for the basic functioning of the system.

-   `/lib/x86_64-linux-gnu/`: Main library directory for 64-bit systems.
-   `/lib/systemd/`: Systemd-related files.
-   `/lib/udev/`: Udev-related files.
-   `/lib/modules/5.15.0-78-generic/`: Kernel modules.
-   `/lib/firmware/`: Device firmware files.
-   `/lib/terminfo/`: Terminal information database.
-   `/lib/ld-linux-x86-64.so.2`: Dynamic linker/loader.
-   `/lib/libcrypt.so.1`: Cryptography library.
-   `/lib/libssl.so.1.1`: SSL library.
-   `/lib/libz.so.1`: Zlib compression library.
-   `/lib/libpthread.so.0`: POSIX threads library.
-   `/lib/libdl.so.2`: Dynamic linking library.
-   `/lib/librt.so.1`: Real-time extensions library.
-   `/lib/libm.so.6`: Math library.
-   `/lib/libresolv.so.2`: DNS resolver library.
-   `/lib/libncurses.so.5`: Curses library.
-   `/lib/libexpat.so.1`: XML parser library.
-   `/lib/libc.so.6`: GNU C Library.
-   `/lib/libstdc++.so.6`: C++ standard library.
-   `/lib/libgcc_s.so.1`: GCC shared library.

***

### **`/lib64` (64-bit Libraries)**
This directory is often a symbolic link to `/lib` or contains shared libraries for 64-bit binaries. It's a key part of the FHS for supporting 64-bit architectures.

-   `/lib64/ld-linux-x86-64.so.2`: 64-bit dynamic linker/loader.
-   `/lib64/libc.so.6`: 64-bit GNU C Library.
-   `/lib64/libm.so.6`: 64-bit math library.
-   `/lib64/libpthread.so.0`: 64-bit POSIX threads library.
-   `/lib64/libdl.so.2`: 64-bit dynamic linking library.
-   `/lib64/librt.so.1`: 64-bit real-time extensions library.
-   `/lib64/libz.so.1`: 64-bit Zlib compression library.
-   `/lib64/libssl.so.1.1`: 64-bit SSL library.
-   `/lib64/libcrypto.so.1.1`: 64-bit crypto library.
-   `/lib64/libstdc++.so.6`: 64-bit C++ standard library.
-   `/lib64/libgcc_s.so.1`: 64-bit GCC shared library.
-   `/lib64/libresolv.so.2`: 64-bit DNS resolver library.
-   `/lib64/libncurses.so.5`: 64-bit Curses library.
-   `/lib64/libexpat.so.1`: 64-bit XML parser library.
-   `/lib64/libcrypt.so.1`: 64-bit cryptography library.
-   `/lib64/libtinfo.so.5`: 64-bit Terminfo library.
-   `/lib64/libnsl.so.1`: 64-bit NIS library.
-   `/lib64/libutil.so.1`: 64-bit utility library.
-   `/lib64/libuuid.so.1`: 64-bit UUID library.
-   `/lib64/liblber-2.4.so.2`: 64-bit LDAP library.

***

### **`/mnt` (Mount Directory)**
This is a temporary location where administrators can **manually mount** external storage devices (e.g., hard drives, network shares).

-   `/mnt/backup`: Mount point for a backup drive.
-   `/mnt/data`: Mount point for a data partition.
-   `/mnt/nas`: Mount point for a network-attached storage device.
-   `/mnt/usb`: Mount point for a USB drive.
-   `/mnt/cdrom`: Mount point for a CD-ROM.
-   `/mnt/dvd`: Mount point for a DVD.
-   `/mnt/cifs_share`: Mount point for a CIFS/SMB share.
-   `/mnt/nfs_share`: Mount point for an NFS share.
-   `/mnt/ssd`: Mount point for an SSD drive.
-   `/mnt/temp_volume`: Mount point for a temporary volume.
-   `/mnt/iscsi`: Mount point for an iSCSI target.
-   `/mnt/raid`: Mount point for a RAID array.
-   `/mnt/cloud_storage`: Mount point for cloud storage.
-   `/mnt/samba`: Mount point for a Samba share.
-   `/mnt/ext4_drive`: Mount point for an ext4 formatted drive.
-   `/mnt/ntfs_drive`: Mount point for an NTFS formatted drive.
-   `/mnt/dev_volume`: Mount point for a developer volume.
-   `/mnt/archive`: Mount point for an archive drive.
-   `/mnt/media`: Mount point for a media drive.
-   `/mnt/remote_fs`: Mount point for a remote file system.

***

### **`/media` (Removable Devices)**
This directory is for the **automatic mounting** of removable storage media, such as USB drives, CDs, or DVDs.

-   `/media/usb_drive`: A USB drive automatically mounted here.
-   `/media/CDROM`: A CD-ROM automatically mounted.
-   `/media/dvd`: A DVD automatically mounted.
-   `/media/john/usbdisk`: A USB disk mounted for user `john`.
-   `/media/mary/music_cd`: A music CD mounted for user `mary`.
-   `/media/external_hdd`: An external hard disk drive.
-   `/media/sdd_card`: An SD card.
-   `/media/camera`: A digital camera mounted as a storage device.
-   `/media/phone`: A mobile phone mounted for file transfer.
-   `/media/floppy`: A floppy disk (if you still have one).
-   `/media/portable_drive`: A portable hard drive.
-   `/media/video_dvd`: A video DVD.
-   `/media/encrypted_drive`: An encrypted drive.
-   `/media/public_share`: A public share on removable media.
-   `/media/flash_drive`: A flash drive.
-   `/media/backup_disk`: A backup disk.
-   `/media/temp_storage`: Temporary storage.
-   `/media/music`: A directory for music files.
-   `/media/photos`: A directory for photos.
-   `/media/documents`: A directory for documents.

***

### **`/srv` (Service Data Directory)**
Contains data for **services offered by the system**. This is a well-defined location for service-specific data.

-   `/srv/www`: Web server data.
-   `/srv/ftp`: FTP server data.
-   `/srv/git`: Git repository data.
-   `/srv/samba`: Samba server data.
-   `/srv/nfs`: NFS server data.
-   `/srv/tftp`: TFTP server data.
-   `/srv/svn`: SVN repository data.
-   `/srv/dns`: DNS server data.
-   `/srv/ldap`: LDAP server data.
-   `/srv/proxy`: Proxy server data.
-   `/srv/minecraft`: Minecraft server data.
-   `/srv/wiki`: Wiki server data.
-   `/srv/mail`: Mail service data.
-   `/srv/postgresql`: PostgreSQL service data.
-   `/srv/mysql`: MySQL service data.
-   `/srv/mongodb`: MongoDB service data.
-   `/srv/jenkins`: Jenkins service data.
-   `/srv/monitoring`: Monitoring service data.
-   `/srv/backup`: Backup service data.
-   `/srv/storage`: General storage service data.

***

### **`/opt` (Third-Party Applications)**
This directory is for **optional or add-on software packages** that are not part of the default system.

-   `/opt/google/chrome`: The Google Chrome installation directory.
-   `/opt/splunk`: The Splunk software installation.
-   `/opt/jdk17`: The Java Development Kit installation.
-   `/opt/mongodb`: The MongoDB installation.
-   `/opt/firefox`: The Firefox installation (if installed this way).
-   `/opt/brave`: The Brave browser installation.
-   `/opt/docker-compose`: Docker Compose installation.
-   `/opt/nginx`: Nginx installation.
-   `/opt/node_exporter`: Prometheus node exporter.
-   `/opt/apache`: Apache web server installation.
-   `/opt/ibm/WebSphere`: IBM WebSphere installation.
-   `/opt/oracle/`: Oracle database installation.
-   `/opt/SAP/`: SAP software installation.
-   `/opt/Atlassian/Jira`: Jira software installation.
-   `/opt/VMware/`: VMware tools installation.
-   `/opt/Microsoft/Edge`: Microsoft Edge browser.
-   `/opt/Anaconda`: Anaconda Python distribution.
-   `/opt/Postman`: Postman API client.
-   `/opt/Visual Studio Code`: VS Code installation.
-   `/opt/Slack`: Slack desktop client.

***

### **`/run` (Runtime Data)**
This directory stores **runtime data** for system processes since the last boot. It's a temporary file system that is cleared on reboot.

-   `/run/systemd/`: Systemd runtime data.
-   `/run/lock/`: Lock files for processes.
-   `/run/shm/`: Shared memory.
-   `/run/user/1000/`: User-specific runtime data for user ID 1000.
-   `/run/shutter.pid`: A PID file for a screenshot application.
-   `/run/sshd.pid`: The PID file for the SSH daemon.
-   `/run/docker.sock`: The Docker daemon socket.
-   `/run/udev/`: Udev runtime data.
-   `/run/d-bus/`: D-Bus sockets.
-   `/run/sddm/`: SDDM display manager runtime data.
-   `/run/dbus/system_bus_socket`: D-Bus system bus socket.
-   `/run/postgresql/.s.PGSQL.5432`: PostgreSQL socket.
-   `/run/nginx.pid`: Nginx PID file.
-   `/run/apache2/apache2.pid`: Apache PID file.
-   `/run/cups/cups.sock`: CUPS printing service socket.
-   `/run/mysql/mysqld.sock`: MySQL socket.
-   `/run/rpcbind.sock`: RPC bind socket.
-   `/run/lightdm/`: LightDM display manager data.
-   `/run/wpa_supplicant/`: WPA supplicant sockets.
-   `/run/systemd/journal/socket`: Systemd journal socket.

***

### **`/lost+found` (Recovered Files)**
This directory is created during the recovery process after a system crash or improper shutdown. It contains **recovered files** that were part of the file system but became corrupted or lost.

-   `#123456`: An inode number of a recovered file.
-   `#123457`: Another recovered file.
-   `#123458`: Another recovered file.
-   `#123459`: Another recovered file.
-   `#123460`: Another recovered file.
-   `#123461`: Another recovered file.
-   `#123462`: Another recovered file.
-   `#123463`: Another recovered file.
-   `#123464`: Another recovered file.
-   `#123465`: Another recovered file.
-   `#123466`: Another recovered file.
-   `#123467`: Another recovered file.
-   `#123468`: Another recovered file.
-   `#123469`: Another recovered file.
-   `#123470`: Another recovered file.
-   `#123471`: Another recovered file.
-   `#123472`: Another recovered file.
-   `#123473`: Another recovered file.
-   `#123474`: Another recovered file.
-   `#123475`: Another recovered file.
