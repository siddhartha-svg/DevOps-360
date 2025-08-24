
These two below service scripts are running fine 

wasadmin@tpaldey2va028.ebiz.verizon.com-/etc/systemd/system $ cat kafka.service
[Unit]
Description=Apache Kafka Service
After=zookeeper.service

[Service]
Type=simple
ExecStart=/opt/app/KAFKA/kafka_2.12-3.1.1/bin/kafka-server-start.sh /opt/app/KAFKA/kafka_2.12-3.1.1/config/server.properties
ExecStop=/opt/app/KAFKA/kafka_2.12-3.1.1/bin/kafka-server-stop.sh
Restart=always
User=wasadmin
Environment="JAVA_HOME=/opt/app/jdk17"

[Install]
WantedBy=multi-user.target


wasadmin@tpaldey2va028.ebiz.verizon.com-/etc/systemd/system $ cat zookeeper.service
[Unit]
Description=Apache Zookeeper Service
After=network.target

[Service]
Type=simple
ExecStart=/opt/app/KAFKA/kafka_2.12-3.1.1/bin/zookeeper-server-start.sh /opt/app/KAFKA/kafka_2.12-3.1.1/config/zookeeper.properties
ExecStop=/opt/app/KAFKA/kafka_2.12-3.1.1/bin/zookeeper-server-stop.sh
Restart=always
User=wasadmin
Environment="JAVA_HOME=/opt/app/jdk17"

[Install]
WantedBy=multi-user.target

I used below script this is wokring fine in root user python3 simple_cluster_monitor.py
wasadmin@tpaldey2va028.ebiz.verizon.com-/opt/kafka-monitor $ cat simple_cluster_monitor.py
#!/usr/bin/env python3
"""
simple_cluster_monitor.py
- Checks if Kafka/Zookeeper services are active (via port check).
- Sends an email if any service is DOWN.
"""

import os
import socket
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# === Configuration ===
SERVERS = [
    {"host": "tpaldey2va028.ebiz.verizon.com", "port": 5102, "service": "zookeeper"},
    {"host": "tpaldey2va028.ebiz.verizon.com", "port": 5102, "service": "kafka"},
    {"host": "tpaldey2va029.ebiz.verizon.com", "port": 5102, "service": "kafka"},
    {"host": "tpaldey2va029.ebiz.verizon.com", "port": 5102, "service": "zookeeper"},
    {"host": "tpaldey2va030.ebiz.verizon.com", "port": 5102, "service": "zookeeper"},
    {"host": "tpaldey2va030.ebiz.verizon.com", "port": 5102, "service": "kafka"}
]

SMTP_SERVER = "vzsmtp.verizon.com"
SMTP_PORT = 25
FROM_EMAIL = "netula.siddhartha.yadav@verizon.com"
TO_EMAIL = "netula.siddhartha.yadav@verizon.com"


def send_email(subject, body):
    """Send a plain text email."""
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["From"] = FROM_EMAIL
        msg["To"] = TO_EMAIL
        msg["Subject"] = Header(subject, "utf-8")

        s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
        s.send_message(msg)
        s.quit()
        print(f"[INFO] Email sent: {subject}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")


def check_port(host, port):
    """Check if a TCP port is open (returns True if open)."""
    try:
        with socket.create_connection((host, port), timeout=5):
            return True
    except Exception:
        return False


def monitor_cycle():
    """Check all servers and services, send email summary."""
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    status_report = [f"Timestamp (UTC): {ts}"]
    is_down = False

    for srv in SERVERS:
        host = srv["host"]
        port = srv["port"]
        service = srv["service"]

        ok = check_port(host, port)
        status = "UP ✅" if ok else "DOWN ❌"
        status_report.append(f"{host}:{port} - {service}: {status}")
        if not ok:
            is_down = True

    report_text = "\n".join(status_report)
    subject = "[Cluster Status] Kafka/ZK Health Report"
    if is_down:
        send_email(subject, report_text)
    else:
        print("[INFO] All services are up. No email sent.")


if __name__ == "__main__":
    monitor_cycle()


Now based on above consideration details email , smtp server name and port and kafka box names and port names 
please create a 

/opt/kafka-monitor/ 
-> monitor.py  ----> Check service status check and attempt to restart 
-> log analysis with AI ----> if service stil not up ai  Analyse Error Logs 
-> email_sender.py  ----> It should send an email if service are not up with summarising logs problem , solution ,action  /opt/app/KAFKA/kafka_2.12-3.1.1/logs/server.log
-> config.yml  ---- > server details are stored here 
-> logs  ---- > If any logs should be generated , it should come in this 
-> email templates  ---- > please share differnet templated overe here 
