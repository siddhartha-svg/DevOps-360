Renewing a certificate on a Kafka server, with the correct commands and a clear breakdown of each action. The process involves generating a new keystore and then verifying the certificate.

-----

### **Certificate Expiry Renewal**

This guide outlines the steps to renew an SSL certificate for the Kafka server **`xJITRKAFKAST1ae.ebiz.horizon.com`**.

-----

### **1. Download and Convert the Certificate**

First, download the renewed certificate from the security application. Then, use **`openssl`** to convert the certificate and its private key into a single PKCS12 file.

  * **Convert to PKCS12 format**:
    ```bash
    openssl pkcs12 -export -out xjitrkafkast1ae.pkcs12 -inkey xJITRKAFKAST1ae.ebiz.horizon.com_private_key.pem -in ChainCerts_xJITRKAFKAST1ae.ebiz.horizon.com.pem
    ```
    This command combines the private key (`-inkey`) and the certificate chain (`-in`) into a single output file (`-out`) named `xjitrkafkast1ae.pkcs12`. This format is necessary for Java's `keytool`.

-----

### **2. Generate and Update the Keystore**

Next, use the **`keytool`** utility to create a new Java keystore and import the certificate. The new keystore will contain the server's identity and its validity period.

  * **Generate a new keystore**:
    ```bash
    keytool -keystore kafka.keystore.jks -alias localhost -validity 365 -genkey -keyalg RSA -storetype pkcs12 -ext SAN=DNS:xjitrkafkast1ae.ebiz.horizon.com,DNS:xjitrkafkast1be.ebiz.horizon.com,DNS:xjitrkafkast1ce.ebiz.horizon.com,DNS:tpaldey2va025.ebiz.horizon.com,DNS:tpaldey2va026.ebiz.horizon.com,DNS:tpaldey2va027.ebiz.horizon.com
    ```
    This command creates a new keystore file named **`kafka.keystore.jks`**. It generates a new key pair (`-genkey`) with a 365-day validity (`-validity`) and specifies the **`Subject Alternative Name (SAN)`** extension. This ensures the certificate is valid for multiple hostnames, which is crucial for a Kafka cluster.

-----

### **3. Verify the Certificate in the Keystore**

After the keystore is created, you should verify that the certificate was imported correctly.

  * **List certificate details**:
    ```bash
    keytool -list -keystore kafka.keystore.jks -storepass devkafka123!
    ```
    This command lists the contents of the keystore, allowing you to check the certificate's details, including its alias, type, and creation date.

-----

### **4. Test Kafka Connectivity**

Finally, test the new certificate by connecting to a Kafka broker using a Kafka utility command. This confirms that the server can accept secure connections with the new certificate.

  * **List Kafka topics**:
    ```bash
    ./kafka-topics.sh --bootstrap-server xjitrkafkast1ae.ebiz.horizon.com:5102 --list --command-config /opt/app/KAFKA/kafka_2.12-3.1.1/config/client.properties
    ```
    This command attempts to connect to the Kafka broker at port `5102` and list the available topics. The `--command-config` flag points to a client properties file that contains the SSL configuration, ensuring the connection is secure. If the command runs successfully, the certificate renewal is complete.
