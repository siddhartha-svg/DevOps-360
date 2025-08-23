import paramiko
import smtplib
from email.mime.text import MIMEText

# Kafka boxes
hosts = [
    "tpaldey2va026.ebiz.verizon.com",
    "tpaldey2va027.ebiz.verizon.com",
    "tpaldey2va028.ebiz.verizon.com",
]

username = "yadane2"
password = "from@1234"

# Email details
sender = "netula.siddhartha.yadav@verizon.com"
recipients = ["netula.siddhartha.yadav@verizon.com"]

def check_services(host):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password, timeout=15)

        # Elevate to wasadmin and check both services
        commands = [
            "pbrun wasadmin systemctl is-active kafka.service",
            "pbrun wasadmin systemctl is-active zookeeper.service",
            "pbrun wasadmin netstat -tulnp | grep 5102"
        ]

        results = {}
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            results[cmd] = output if output else error if error else "No Output"

        ssh.close()
        return results

    except Exception as e:
        return {f"ERROR connecting to {host}": str(e)}

def send_email(message):
    msg = MIMEText(message)
    msg["Subject"] = "Kafka & Zookeeper Cluster Monitoring"
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    # Assuming local mail relay is configured
    with smtplib.SMTP("localhost") as server:
        server.sendmail(sender, recipients, msg.as_string())

# Main
report_lines = []
for host in hosts:
    service_results = check_services(host)
    report_lines.append(f"\n🔹 Host: {host}")
    for cmd, result in service_results.items():
        report_lines.append(f"  {cmd} → {result}")

final_report = "\n".join(report_lines)

print(final_report)
send_email(final_report)
