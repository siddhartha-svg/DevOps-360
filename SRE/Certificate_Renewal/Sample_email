#!/usr/bin/env python3
"""
simple_cluster_monitor.py
- Checks if Kafka/Zookeeper services are active on remote servers.
- Sends a simple email if service is DOWN or UP.
"""

import os
import subprocess
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# === Configuration ===
SERVERS = ["tpaldey2va028.ebiz.verizon.com",
           "tpaldey2va029.ebiz.verizon.com",
           "tpaldey2va030.ebiz.verizon.com"]

SERVICES = ["zookeeper", "kafka"]

SMTP_SERVER = "vzsmtp.verizon.com"
SMTP_PORT = 25
FROM_EMAIL = "kafka-monitor@yourcompany.com"
TO_EMAIL = "you@yourcompany.com"

CHECK_CMD_TEMPLATE = "ssh wasadmin@{host} 'systemctl is-active {service}'"


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


def check_service(host, service):
    """Return True if service is active, else False."""
    cmd = CHECK_CMD_TEMPLATE.format(host=host, service=service)
    result = subprocess.run(cmd, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True)
    return result.stdout.strip() == "active"


def monitor_cycle():
    """Check all servers and services, send email summary."""
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    status_report = [f"Timestamp (UTC): {ts}"]

    for host in SERVERS:
        for service in SERVICES:
            ok = check_service(host, service)
            status = "UP ✅" if ok else "DOWN ❌"
            status_report.append(f"{host} - {service}: {status}")

    report_text = "\n".join(status_report)
    subject = "[Cluster Status] Kafka/ZK Health Report"
    send_email(subject, report_text)


if __name__ == "__main__":
    monitor_cycle()
