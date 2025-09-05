Based on your description, this is a detailed process for performing a Kafka/Ignite cluster maintenance cycle. I've broken it down into a clear, step-by-step procedure.

### 🔹 Step 1: Stop and Clean Up on Each Kafka Box

You need to perform these commands on each of your Kafka servers.

1.  **Kill the Kafka/Ignite processes:** Stop any running processes related to your old configuration.
    ```bash
    # Kill any processes related to the old RATE/FID services
    pkill -f RATE
    pkill -f FID

    # Check for any lingering Ignite processes and kill them
    jps # to list Java processes
    ps -ef | grep $ORACLE_SID # to check for Oracle-related processes
    pkill -f ignite
    pkill -f 461
    ```
2.  **Navigate and set up the environment:** Go to the correct directory and load the environment variables.
    ```bash
    # Move to the Kafka home directory
    cd /opt/app/KAFKA/kafka_2.12-3.1.1/bin

    # Kill any Kafka processes running
    pkill -f kafka_2.12-3.1.1
    ```
3.  **Source the environment file:**
    ```bash
    source envst1b2b.sh
    ```

-----

### 🔹 Step 2: Start the Ignite Server on Each Kafka Box

After cleaning up the old processes, you will start the Ignite server.

1.  **Start the Ignite service:** Go to the Ignite home directory and run the `ignite.sh` script to start the server. The `nohup` command ensures the process continues to run after you log out.
    ```bash
    cd $IGNITE_HOME/bin
    nohup ./ignite.sh ../xmls/imdg-cache-config.xml &
    ```
2.  **Verify the status:** Use `tail` to check the `nohup.out` log file to see if the nodes are active. You should see a log message indicating that all nodes are up.
    ```bash
    tail -100f nohup.out
    ```

-----

### 🔹 Step 3: Start the Cache Loader (on the RATE Box)

Once the Ignite servers are running, you can start the cache loader. This is done on your designated "RATE Box."

1.  **Start the B2B cache loaders:** Navigate to the cache loader's binary directory and run the `run-cache-loader.ksh` script with the appropriate arguments.
    ```bash
    cd /jitr/rbm/infinys/NRMUDM/bin

    # Run the cache loaders for B2B
    ./run-cache-loader.ksh 3
    ./run-cache-loader.ksh 4
    ```
2.  **Verify the cache loader logs:** Use `tail` to check the logs and ensure the loader is running correctly. The log filename will vary based on the server and timestamp.
    ```bash
    tail -100f /jitr/rbm/infinys/NRMUDM/logs/udm_cache_loader_out_3_2025-09-01-11-30-39.log
    ```

-----

### 🔹 Step 4: Start the Ignite Proxy (on the RATE Box)

After the cache loader is running, you'll start the Ignite proxy, which allows other applications to connect to the Ignite cluster.

1.  **Start the Ignite proxy:**
    ```bash
    cd /jitr/rbm/infinys/NRMUDM/bin
    ./start-ignite-proxy.sh ignite.proxy.instance.1
    ```
2.  **Verify the proxy logs:** Use `tail` to check the log file for the Ignite proxy. Look for a message indicating that it has connected to all the active nodes in the cluster.
    ```bash
    tail -100f /jitr/rbm/infinys/NRMUDM/logs/ignite.proxy.instance.1_2025-09-01-11-50-45.log
    ```
3.  **Confirm the cluster topology:** The logs should contain a section similar to the one you provided, showing the list of active nodes.
    ```
    current cluster topology :: List of Active Nodes
    node : 1 -- server : tpaldey2va031.ebiz.verizon.com
    node : 2 -- server : tpaldey2va032.ebiz.verizon.com
    node : 3 -- server : tpaldey2va033.ebiz.verizon.com
    ```
