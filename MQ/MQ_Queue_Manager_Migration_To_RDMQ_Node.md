step-by-step guide for migrating an MQ Queue Manager to an RDQM Node, formatted in Markdown for a GitHub README. It's organized into logical phases, from preparing the source queue manager to validating the new one.

### **MQ Queue Manager Migration to RDQM Node** ⚙️

This guide provides a comprehensive, step-by-step procedure for migrating an MQ Queue Manager from a traditional setup to a Replicated Data Queue Manager (RDQM) node. The process is broken down into four main phases: **Backup**, **Pre-Migration Cleanup**, **Migration**, and **Post-Migration Validation**.

-----

### **Phase 1: Backup on the Source MQ Server** 💾

Before any changes are made, it is critical to back up all queue manager objects, messages, and configurations. All commands in this phase should be executed by the `mqm` user.

1.  **Create a Backup Directory:**

    ```bash
    cd /tmp
    mkdir <queue_manager_name>
    ```

2.  **Back Up Queue Manager Definitions:**

      * **Full Backup:** Back up all queue manager objects, including default values.
        ```bash
        dmpmqcfg -m <qmgr> -a > /tmp/<qmgr>/<qmgrname>_full.mqsc
        ```
      * **Objects Only (Excluding System):** Back up only user-defined objects, with each definition on a single line. This is useful for clean restoration.
        ```bash
        dmpmqcfg -m <qmgr> -a all -o 1line | grep -v "SYSTEM" > /tmp/<qmgr>/<qmgrname>_objects.mqsc
        ```
      * **Queue Manager-specific Backup:** Back up the queue manager's own attributes.
        ```bash
        dmpmqcfg -m <qmgr> -n qmgr -t qmgr > /tmp/<qmgr>/<qmgrname>_qmgr.mqsc
        ```

3.  **Back Up Messages on Queues:**

      * List queues with messages to identify what needs to be backed up.
        ```bash
        echo " dis ql(*) where(CURDEPTH GT 0) " | runmqsc <qmgr name>
        ```
      * Dump messages from each queue to a file.
        ```bash
        dmpmqmsg -i <queue name> -f /tmp/<qmgr>/<queue_name>
        ```

4.  **Back Up the SSL Folder:**

      * Find the `SSLKEYR` path of the queue manager.
        ```bash
        echo " dis qmgr SSLKEYR " | runmqsc <qmgr name>
        ```
      * Copy the SSL directory to your backup folder.
        ```bash
        cp -r <SSLKEYR_PATH> /tmp/<qmgr>/SSL
        ```

5.  **Check Current Cluster and Channel Status:**
    Run these commands and save the output for later validation.

      * `DISPLAY CLUSQMGR(*)`
      * `DISPLAY CHANNEL(*) CHLTYPE(CLUSSDR)`
      * `DISPLAY CHSTATUS(*)`

-----

### **Phase 2: Pre-Migration Cleanup** 🧹

Before moving the queue manager, it must be gracefully removed from any clusters it belongs to.

1.  **Stop Monitoring:**

      * Stop the New Relic process to prevent monitoring during migration.
        ```bash
        ps -ef | grep newrelic
        kill -9 <pid>
        systemctl stop newrelic-infra.service
        ```

2.  **Remove the Queue Manager from Cluster:**

      * Suspend the queue manager from the cluster to prevent it from participating in cluster activities.
        ```bash
        SUSPEND QMGR CLUSTER('<CLUSTER NAME>')
        ```
      * Check the status to ensure the suspension is complete.
        ```bash
        DISPLAY CLUSQMGR('<qmgr>') CLUSTER SUSPEND
        ```
      * Alter the cluster sender and receiver channels to disassociate them from the cluster.
        ```bash
        ALTER CHANNEL('<channel name>') CHLTYPE(CLUSSDR) CLUSTER('') CLUSNL('')
        ALTER CHANNEL('<channel name>') CHLTYPE(CLUSRCVR) CLUSTER('') CLUSNL('')
        ```

-----

### **Phase 3: Migration to the RDQM Node** 🚚

1.  **Copy Backup Files to the RDQM Node:**
    Use `scp` to securely transfer your backup folder to the new RDQM host.

    ```bash
    scp -r /tmp/<qmgr_name> userid@<hostname>:/tmp
    ```

2.  **Create the RDQM Queue Manager (On the RDQM Node):**

      * Create a replicated data queue manager with the specified file system size.
          * For a **secondary node**: `crtmqm -sxs -fs <size in gb> <qmgr name>`
          * For a **primary node**: `crtmqm -sx -fs <size in gb> <qmgr name>`

3.  **Restore MQ Objects:**

      * Switch to the `mqm` user and change the ownership of the new queue manager directory.
      * Restore the object definitions using `runmqsc` and the backup files.
        ```bash
        runmqsc <qmgr> < /tmp/<qmgr>/<qmgr>_objects.mqsc > /tmp/<qmgr>/<qmgr>_objects.mqsc.out
        runmqsc <qmgr> < /tmp/<qmgr>/<qmgr>_qmgr.mqsc > /tmp/<qmgr>/<qmgr>_qmgr.mqsc.out
        ```

4.  **Copy SSL and `qm.ini` Files:**

      * Copy the backed-up SSL folder to the new queue manager's data directory.
        ```bash
        cp -r /tmp/<qmgr>/SSL /var/mqm/vols/<$qmgr>/qmgr/$<qmgr>/
        ```
      * Manually update the `qm.ini` file on the new RDQM node by comparing it with the old `qm.ini` backup and adding any necessary stanzas.

5.  **Configure SSL:**

      * Set the `SSLKEYR` value to the correct path of the copied SSL folder.
        ```bash
        runmqsc <qmgr>
        ALTER QMGR SSLKEYR('<SSL Path>')
        REFRESH SECURITY TYPE(SSL)
        ```

-----

### **Phase 4: Post-Migration Validation** ✅

1.  **Update Network Load Balancer (NLB):**

      * Log into the AWS console.
      * Add the new RDQM node's Elastic Network Interface (ENI) IP to the NLB's target group.

2.  **Stop and Alter Listener on Old Node:**

      * Stop the listener on the old MQ server to prevent new connections.
        ```bash
        STOP LISTENER(<listener_name>)
        ```
      * Alter the listener to `MANUAL` control.
        ```bash
        ALTER LISTENER(<name>) TRPTYPE(TCP) CONTROL(MANUAL)
        ```

3.  **Start Listener on New RDQM Node:**

      * Start the listener on the new RDQM host.
        ```bash
        START LISTENER(<name>)
        ```

4.  **Validate Cluster Participation and Messages:**

      * Check that the queue manager has successfully joined the cluster.
      * Restore messages to the queues from the backup files.
        ```bash
        dmpmqmsg -o <queue name> -f /tmp/<qmgr>/<filename>
        ```

5.  **Final Health Checks:**

      * Verify the status of the queue manager, listeners, and channels.
      * Check for the presence of the new queue manager metrics in the monitoring dashboard.
