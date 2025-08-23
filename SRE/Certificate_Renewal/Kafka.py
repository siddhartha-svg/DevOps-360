Nice — I built a single, ready-to-run Python script that:

Runs 24/7 (looped) or via systemd timer,

Checks services on each remote host,

Fetches the last ~200 lines of the service logs,

Summarizes them with a local LLaMA model using llama-cpp-python (no OpenAI cloud),

Decides a safe action from the model’s output (e.g. restart, no-action, escalate) and executes restart when recommended,

Saves the logs locally, attaches them to the notification email, and includes the AI summary (<=100 lines) in the email, and

Falls back to a rule-based analyzer if the local model is missing.


Below is the script plus the recommended systemd unit & env file and the sudoers snippet. Copy/paste, adjust paths and model location, install packages, then enable the service.


---

1) Full script — cluster_monitor_ai.py

Save to /opt/kafka-ai/cluster_monitor_ai.py and chmod +x it.

#!/usr/bin/env python3
"""
cluster_monitor_ai.py
- Checks services on remote Kafka/ZK servers via SSH.
- Fetches last N lines of logs.
- Summarizes logs using a local LLaMA model via llama-cpp-python.
- Decides an action (restart/no-action/escalate) based on AI output.
- Performs safe auto-restart if recommended and configured.
- Sends email with AI summary and logs attached.

Requirements:
- python3, pip3
- pip3 install llama-cpp-python paramiko psutil
- SSH key-based access for wasadmin and sudo NOPASSWD for systemctl restarts on remote hosts.
- Local LLaMA ggml model binary available (set MODEL_PATH env var).
"""

import os
import subprocess
import time
import datetime
import traceback
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header

# Optional: use paramiko if you prefer; current script uses subprocess ssh
# import paramiko

# === Configuration (override via /etc/cluster_monitor_ai.env) ===
SERVERS = os.getenv("SERVERS", "tpaldey2va028.ebiz.verizon.com,tpaldey2va029.ebiz.verizon.com,tpaldey2va030.ebiz.verizon.com")
SERVERS = [s.strip() for s in SERVERS.split(",") if s.strip()]

SERVICES = os.getenv("SERVICES", "zookeeper,kafka").split(",")  # comma-separated

MODEL_PATH = os.getenv("MODEL_PATH", "/opt/kafka-ai/models/ggml-model-q4_0.bin")  # update to your model file
LLAMA_ENABLED = os.getenv("LLAMA_ENABLED", "true").lower() in ("1","true","yes")
LOG_LINES = int(os.getenv("LOG_LINES", "200"))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))  # seconds

# Email / SMTP
SMTP_SERVER = os.getenv("SMTP_SERVER", "vzsmtp.verizon.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "25"))
FROM_EMAIL = os.getenv("FROM_EMAIL", "kafka-monitor@yourcompany.com")
TO_EMAIL = os.getenv("TO_EMAIL", "you@yourcompany.com")

# Paths
BASE_DIR = os.getenv("BASE_DIR", "/opt/kafka-ai")
LOG_DIR = os.path.join(BASE_DIR, "collected_logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Safety: only allow automatic restarts if enabled
AUTO_RESTART_ENABLED = os.getenv("AUTO_RESTART_ENABLED", "true").lower() in ("1","true","yes")

# Health check command templates
CHECK_CMD_TEMPLATE = "ssh wasadmin@{host} 'systemctl is-active {service}'"
FETCH_LOG_CMD_TEMPLATE = "ssh wasadmin@{host} 'sudo journalctl -u {service} -n {lines} --no-pager --no-hostname --output=short-iso'"
RESTART_CMD_TEMPLATE = "ssh wasadmin@{host} 'sudo systemctl restart {service}'"

# === Optional: LLaMA integration using llama-cpp-python ===
llama = None
if LLAMA_ENABLED:
    try:
        # lazy import
        from llama_cpp import Llama
        if os.path.isfile(MODEL_PATH):
            llama = Llama(model_path=MODEL_PATH)
            print(f"[INFO] Local LLaMA model loaded from {MODEL_PATH}")
        else:
            print(f"[WARN] LLaMA model not found at {MODEL_PATH}. Falling back to rule-based analyzer.")
            llama = None
    except Exception as e:
        print(f"[WARN] Could not import llama-cpp-python or load model: {e}")
        llama = None

def send_email(subject, body, attachment_paths=None):
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = Header(subject, 'utf-8')
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    if attachment_paths:
        for path in attachment_paths:
            try:
                with open(path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(path))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'
                    msg.attach(part)
            except Exception as e:
                print(f"[WARN] Failed to attach {path}: {e}")

    try:
        s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
        s.send_message(msg)
        s.quit()
        print(f"[INFO] Email sent: {subject}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

def check_service(host, service):
    """Return True if systemctl is-active returns active."""
    try:
        cmd = CHECK_CMD_TEMPLATE.format(host=host, service=service)
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
        out = result.stdout.strip()
        # result.returncode == 0 and out == 'active' is typical, but check output
        active = out == "active"
        print(f"[DEBUG] check_service {host} {service} -> '{out}' (active={active})")
        return active
    except Exception as e:
        print(f"[ERROR] check_service exception for {host} {service}: {e}")
        return False

def fetch_logs(host, service, lines=LOG_LINES):
    """Fetch last 'lines' from journalctl on remote host for the service."""
    try:
        cmd = FETCH_LOG_CMD_TEMPLATE.format(host=host, service=service, lines=lines)
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
        if result.returncode != 0:
            print(f"[WARN] fetch_logs non-zero return for {host} {service}: {result.stderr.strip()}")
            # try a lighter fallback
            return result.stdout.strip() or f"[no log output, stderr={result.stderr.strip()}]"
        return result.stdout.strip()
    except Exception as e:
        print(f"[ERROR] fetch_logs exception: {e}")
        return f"[exception fetching logs: {e}]"

def save_logs(host, service, log_text):
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    fname = os.path.join(LOG_DIR, f"{host.replace('.', '_')}_{service}_{ts}.log")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(log_text)
    return fname

# === AI analyze function ===
def ai_analyze(log_text, host, service):
    """
    Return a dict:
    {
      "summary": "...",  # <=100 lines ideally
      "action": "restart" | "no-action" | "escalate" | "unknown",
      "confidence": float (0-1),
      "reasoning": "..."
    }
    """
    prompt = f"""
You are an on-call Kafka/Zookeeper troubleshooting assistant.
You will be given recent logs for a single service on a host.
1) Provide a concise, readable actionable summary (MAX 100 LINES), labelled "SUMMARY:".
2) Suggest a single ACTION from: restart, no-action, escalate. Label "ACTION:" and only output the single word.
3) Provide short REASONING labelled "REASON:" (1-3 lines).
4) Provide a confidence score between 0.0 and 1.0 labelled "CONFIDENCE:".

Logs begin below:
---LOGS-BEGIN---
{log_text}
---LOGS-END---
"""
    # If LLaMA is available, use it.
    if llama:
        try:
            # control token usage with max_tokens (adjust if needed)
            resp = llama.create(prompt=prompt, max_tokens=512, temperature=0.0)
            text = resp.get("choices", [{}])[0].get("text", "").strip()
            # parse output
            return parse_ai_output(text)
        except Exception as e:
            print(f"[WARN] LLaMA analysis failed: {e}\nFalling back to rules.")
            # fall through to rule-based
    # Fallback rule-based analyzer
    return rule_based_analyze(log_text)

def parse_ai_output(text):
    """Parse the model output for SUMMARY/ACTION/REASON/CONFIDENCE."""
    lines = text.strip().splitlines()
    out = {"summary": "", "action": "unknown", "confidence": 0.0, "reasoning": ""}
    summary_lines = []
    for line in lines:
        l = line.strip()
        if l.upper().startswith("ACTION:"):
            out["action"] = l.split(":",1)[1].strip().lower()
        elif l.upper().startswith("CONFIDENCE:"):
            try:
                out["confidence"] = float(l.split(":",1)[1].strip())
            except:
                pass
        elif l.upper().startswith("REASON:"):
            out["reasoning"] = l.split(":",1)[1].strip()
        elif l.upper().startswith("SUMMARY:"):
            # rest of lines belong to summary until next label
            idx = lines.index(line)
            # gather following lines until end or until we hit known labels
            for s in lines[idx+1:]:
                if any(s.strip().upper().startswith(x) for x in ["ACTION:", "REASON:", "CONFIDENCE:"]):
                    break
                summary_lines.append(s)
            break
        else:
            # if no explicit labels, accumulate as summary
            summary_lines.append(l)
    out["summary"] = "\n".join(summary_lines).strip()[:10000]
    # sanitize action
    if out["action"] not in ("restart","no-action","escalate"):
        # try to find keywords
        t = text.lower()
        if "restart" in t or "start" in t or "killed" in t or "Segmentation" in t:
            out["action"] = "restart"
        elif "permission" in t or "corrupt" in t or "disk full" in t or "oom" in t:
            out["action"] = "escalate"
        else:
            out["action"] = "no-action"
    if out["confidence"] == 0.0:
        out["confidence"] = 0.8  # default
    return out

def rule_based_analyze(log_text):
    """Simple heuristics if model is not available."""
    t = log_text.lower()
    if "bind exception" in t or "address already in use" in t or "failed to bind" in t:
        action = "restart"
        reason = "Port bind conflict - restart recommended."
        confidence = 0.9
    elif "outofmemory" in t or "oom" in t or "java.lang.outofmemoryerror" in t:
        action = "escalate"
        reason = "OOM detected - escalate to ops, restart may not fix underlying memory leak."
        confidence = 0.95
    elif "permission denied" in t or "no such file or directory" in t or "corrupt" in t:
        action = "escalate"
        reason = "File system or permission problem - escalate."
        confidence = 0.9
    elif "connection refused" in t or "zookeeper is not running" in t or "kafka.server.KafkaServer" in t and "starting" in t:
        action = "restart"
        reason = "Service not accepting connections - restart recommended."
        confidence = 0.85
    else:
        action = "no-action"
        reason = "No clear actionable error found in logs."
        confidence = 0.6
    summary = f"{reason}\n(Heuristic summary.)"
    return {"summary": summary, "action": action, "confidence": confidence, "reasoning": reason}

def attempt_restart(host, service):
    try:
        cmd = RESTART_CMD_TEMPLATE.format(host=host, service=service)
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
        success = result.returncode == 0
        print(f"[INFO] restart {host} {service} returned {result.returncode}. stdout={result.stdout.strip()} stderr={result.stderr.strip()}")
        return success, result.stdout.strip() + ("\n" + result.stderr.strip() if result.stderr else "")
    except Exception as e:
        print(f"[ERROR] attempt_restart exception: {e}")
        return False, str(e)

def monitor_cycle():
    for host in SERVERS:
        for service in SERVICES:
            try:
                print(f"[INFO] Checking {service} on {host} ...")
                healthy = check_service(host, service)
                if healthy:
                    print(f"[DEBUG] {service} on {host} is active.")
                    continue
                # service down: gather logs and analyze
                print(f"[WARN] {service} on {host} appears DOWN. Fetching logs...")
                logs = fetch_logs(host, service, LOG_LINES)
                logfile = save_logs(host, service, logs)
                ai_result = ai_analyze(logs, host, service)
                # Build email body
                subject_alert = f"[ALERT] {service} down on {host}"
                body = (f"Timestamp(UTC): {datetime.datetime.utcnow().isoformat()}Z\n"
                        f"Host: {host}\nService: {service}\n\n"
                        f"AI Summary:\n{ai_result['summary']}\n\n"
                        f"AI Reasoning: {ai_result.get('reasoning','')}\n"
                        f"AI Action Suggestion: {ai_result.get('action')}\n"
                        f"AI Confidence: {ai_result.get('confidence')}\n\n"
                        f"Full logs are attached ({logfile}).")
                send_email(subject_alert, body, [logfile])
                # take action based on AI suggestion
                action = ai_result.get("action", "no-action")
                if action == "restart" and AUTO_RESTART_ENABLED:
                    print(f"[INFO] AI suggested restart for {service} on {host}. Attempting restart...")
                    ok, restart_out = attempt_restart(host, service)
                    if ok:
                        rec_subject = f"[RECOVERED] {service} restarted on {host}"
                        rec_body = (f"{service} on {host} was restarted automatically at {datetime.datetime.utcnow().isoformat()}Z.\n\n"
                                    f"AI summary: {ai_result['summary']}\n\nRestart stdout/stderr:\n{restart_out}")
                        send_email(rec_subject, rec_body, [logfile])
                    else:
                        fail_subject = f"[FAILED] Restart failed for {service} on {host}"
                        fail_body = (f"Attempted automatic restart but it failed.\n\nAI summary: {ai_result['summary']}\n\n"
                                     f"Restart output:\n{restart_out}\n\nPlease investigate manually.")
                        send_email(fail_subject, fail_body, [logfile])
                elif action == "escalate":
                    esc_subject = f"[ESCALATE] {service} issue on {host}"
                    esc_body = (f"AI suggests escalation for {service} on {host}.\n\nAI summary:\n{ai_result['summary']}\n\n"
                                f"Please investigate manually. Logs attached.")
                    send_email(esc_subject, esc_body, [logfile])
                else:
                    # no-action
                    print(f"[INFO] AI suggested no-action for {service} on {host}. Email sent with analysis.")
                # end service handling
            except Exception as exc:
                trace = traceback.format_exc()
                print(f"[ERROR] Exception in monitor_cycle for {host} {service}: {exc}\n{trace}")
                send_email(f"[ERROR] monitor exception for {host}", f"Exception:\n{exc}\n\nTraceback:\n{trace}")
    return

if __name__ == "__main__":
    print("[START] cluster_monitor_ai starting...")
    while True:
        try:
            monitor_cycle()
        except Exception as e:
            print(f"[CRITICAL] Fatal loop exception: {e}")
            send_email("[CRITICAL] cluster_monitor_ai crashed", f"Exception: {e}\n\nTrace: {traceback.format_exc()}")
        time.sleep(CHECK_INTERVAL)


---

2) Explanation of how the script acts (step-by-step)

1. Loads config (servers, services, SMTP, model path) from environment variables (or defaults).


2. Every CHECK_INTERVAL seconds it loops through each host and each service.


3. For each service it runs systemctl is-active over SSH (wasadmin@host).


4. If the service is active → nothing to do.


5. If it’s not active → it fetches the last LOG_LINES from journalctl on the remote host (via SSH + sudo), saves those logs to /opt/kafka-ai/collected_logs/... and calls the AI analyzer.


6. The AI analyzer tries the local LLaMA model: it receives a clear prompt asking for SUMMARY:, ACTION:, REASON:, CONFIDENCE:.

If the LLaMA model is not installed or fails, it falls back to a rule-based heuristic analyzer.



7. The script sends an [ALERT] email immediately with the AI summary and the logs attached.


8. If AI suggests restart and AUTO_RESTART_ENABLED=true, the script performs sudo systemctl restart on the remote host (via SSH).

If restart succeeds → send [RECOVERED] email.

If restart fails → send [FAILED] email.



9. If AI suggests escalate, a special [ESCALATE] email is sent.


10. All actions are printed to stdout and can be followed through journalctl -u cluster_monitor.service when run under systemd.




---

3) Systemd unit (daemon) recommendation

Create /etc/systemd/system/cluster_monitor_ai.service:

[Unit]
Description=Kafka/ZK AI Cluster Monitor
After=network.target

[Service]
Type=simple
User=wasadmin
Group=wasadmin
WorkingDirectory=/opt/kafka-ai
ExecStart=/usr/bin/python3 -u /opt/kafka-ai/cluster_monitor_ai.py
Restart=always
RestartSec=15
EnvironmentFile=/etc/cluster_monitor_ai.env
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target

Reload & enable:

sudo systemctl daemon-reload
sudo systemctl enable --now cluster_monitor_ai.service
sudo journalctl -u cluster_monitor_ai.service -f


---

4) Environment file /etc/cluster_monitor_ai.env (example)

# /etc/cluster_monitor_ai.env
SERVERS=tpaldey2va028.ebiz.verizon.com,tpaldey2va029.ebiz.verizon.com,tpaldey2va030.ebiz.verizon.com
SERVICES=zookeeper,kafka
SMTP_SERVER=vzsmtp.verizon.com
SMTP_PORT=25
FROM_EMAIL=netula.siddhartha.yadav@verizon.com
TO_EMAIL=netula.siddhartha.yadav@verizon.com
MODEL_PATH=/opt/kafka-ai/models/ggml-model-q4_0.bin
LLAMA_ENABLED=true
LOG_LINES=200
CHECK_INTERVAL=300
AUTO_RESTART_ENABLED=true
BASE_DIR=/opt/kafka-ai

Save as root and set chmod 600.


---

5) Sudoers snippet for safe passwordless restart (on each Kafka host)

On each kafka host (tpaldey2va028/29/30), create /etc/sudoers.d/wasadmin_kafka:

wasadmin ALL=(ALL) NOPASSWD: /bin/systemctl restart kafka, /bin/systemctl restart zookeeper, /bin/systemctl status kafka, /bin/systemctl status zookeeper, /bin/journalctl

(Adjust full path of systemctl/journalctl if they are in /usr/bin.)

Validate with:

sudo visudo -c

Security note: This allows wasadmin to restart those services without a password — restrict carefully.


---

6) Install local LLaMA model & python deps

1. Install system packages (Ubuntu/Debian example):



sudo apt update
sudo apt install -y build-essential libomp-dev python3-pip git
pip3 install --upgrade pip
pip3 install llama-cpp-python paramiko psutil

2. Download a ggml model (you must obtain a compatible model file and place it at /opt/kafka-ai/models/ggml-model-q4_0.bin or update MODEL_PATH). I am not giving links here — follow your organisation's licensing & download instructions for a local LLaMA-type model.


3. Make sure the model file is readable by the wasadmin user.




---

7) Behavior & examples of emails you will receive

On detection: [ALERT] kafka down on tpaldey2va028.ebiz.verizon.com with body containing AI Summary, AI Reasoning, AI Action Suggestion, AI Confidence and the full logs attached.

If AI recommended restart and it succeeded: [RECOVERED] kafka restarted on tpaldey2va028... with restart stdout/stderr and AI summary.

If restart failed: [FAILED] Restart failed for kafka on tpaldey2va028... with logs.

If AI recommended escalation: [ESCALATE] kafka issue on ...


The AI summary is generated to be human readable and limited (prompt asks for MAX 100 LINES). The email will include the logs file as an attachment.


---

8) Fallback & safety

If LLaMA model is not present or fails to load, the script uses a rule-based analyzer to still attempt restarts for common cases (bind errors, connection refu



# Update system
sudo dnf update -y

# Install development tools and dependencies
sudo dnf groupinstall -y "Development Tools"
sudo dnf install -y python3-devel openssl-devel make cmake gcc-c++ git python3-pip libstdc++-devel

# Install OpenMP support
sudo dnf install -y libgomp

# Upgrade pip and install packages
sudo pip3 install --upgrade pip
pip3 install llama-cpp-python paramiko psutil
