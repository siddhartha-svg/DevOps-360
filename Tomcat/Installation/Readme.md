The provided instructions for installing Apache Tomcat are a bit confusing, as they describe moving files to `/opt/app` after downloading to a local directory, rather than a direct installation. However, I can combine these ideas into a streamlined guide that goes directly to the `/opt/app` directory.

### Apache Tomcat Installation Guide

This guide details how to install and configure Apache Tomcat directly into the `/opt/app/` directory on a Linux server.

1.  **Download and Extract**
    Download the Tomcat `tar.gz` archive and extract its contents directly into the `/opt/app/` directory. You will likely need `sudo` privileges for this.

      * **Source:** `https://archive.apache.org/dist/tomcat/tomcat-10/v10.1.43/bin/apache-tomcat-10.1.43.tar.gz`
      * **Command:**
        ```bash
        sudo tar -xvzf apache-tomcat-10.1.43.tar.gz -C /opt/app/
        ```

    This command downloads the file and extracts it to the specified location.

2.  **Set Java Environment Variables**
    Tomcat requires the **JAVA\_HOME** environment variable to be set. This tells the server where to find the Java Development Kit (JDK).

    ```bash
    # Set JAVA_HOME and update the PATH
    export JAVA_HOME=/apps/k2view/apps/jdk-17.0.15
    export PATH=$JAVA_HOME/bin:$PATH
    ```

    For these changes to persist after a reboot, you should add these lines to your `~/.bashrc` or `/etc/profile` file.

3.  **Create a Symbolic Link (Optional)**
    Creating a symbolic link provides a stable path to your Tomcat installation. This is useful for updates, as you can simply point the link to a new version without changing your scripts.

    ```bash
    # Create the symbolic link
    sudo ln -s /opt/app/apache-tomcat-10.1.43 /opt/app/tomcat
    ```

    Now, `/opt/app/tomcat` is a symbolic link to the full versioned directory.

4.  **Start and Verify Tomcat**
    Finally, start the Tomcat server and check its version to ensure the installation was successful.

    ```bash
    # Change to the Tomcat bin directory using the symlink
    cd /opt/app/tomcat/bin

    # Start the Tomcat server
    ./startup.sh

    # Check the Tomcat version
    ./version.sh
    ```

    If Tomcat fails to start, verify that the **JAVA\_HOME** path is correct and that the user has execution permissions for the script.
