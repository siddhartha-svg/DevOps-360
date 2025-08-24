#!/bin/bash

# Kafka Monitor Installation Script
# For Verizon environment - Runs as wasadmin user

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if running as wasadmin
if [[ "$USER" != "wasadmin" ]]; then
    print_error "This script should be run as wasadmin user"
    exit 1
fi

print_info "Starting Kafka Monitor installation for Verizon environment..."

# Create monitor directory
MONITOR_DIR="/opt/kafka-monitor"
print_step "Creating monitor directory structure..."

sudo mkdir -p $MONITOR_DIR
sudo mkdir -p $MONITOR_DIR/logs
sudo mkdir -p $MONITOR_DIR/templates

# Set ownership to wasadmin
sudo chown -R wasadmin:wasadmin $MONITOR_DIR
cd $MONITOR_DIR

print_info "Monitor directory created: $MONITOR_DIR"

# Install system packages (requires sudo)
print_step "Installing system dependencies..."
sudo yum update -y
sudo yum install -y python3 python3-pip curl wget

# Install Python packages
print_step "Installing Python dependencies..."
pip3 install --user pyyaml requests psutil

# Install Ollama for local AI
print_step "Installing Ollama for local AI analysis..."
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.ai/install.sh | sh
    
    # Start and enable Ollama service
    sudo systemctl enable ollama
    sudo systemctl start ollama
    
    print_info "Ollama installed and started"
else
    print_info "Ollama already installed"
fi

# Wait for Ollama to be ready and pull model
print_step "Setting up AI model..."
sleep 5

# Pull the Llama model
print_info "Pulling Llama3 8B model (this may take several minutes)..."
ollama pull llama3:8b

print_info "AI model setup complete"

# Create systemd service for the monitor
print_step "Creating systemd service..."

sudo tee /etc/systemd/system/kafka-monitor.service > /dev/null << EOF
[Unit]
Description=Kafka/Zookeeper Monitor Service
After=network.target kafka.service zookeeper.service ollama.service
Wants=kafka.service zookeeper.service ollama.service

[Service]
Type=simple
User=wasadmin
Group=wasadmin
WorkingDirectory=$MONITOR_DIR
Environment="PATH=/home/wasadmin/.local/bin:\$PATH"
Environment="PYTHONPATH=$MONITOR_DIR"
ExecStart=/usr/bin/python3 $MONITOR_DIR/monitor.py
Restart=always
RestartSec=30
StandardOutput=journal
StandardError=journal
SyslogIdentifier=kafka-monitor

[Install]
WantedBy=multi-user.target
EOF

# Create cron job for daily reports
print_step "Setting up daily reporting..."

# Add cron job for daily report at 9 AM
(crontab -l 2>/dev/null || true; echo "0 9 * * * /usr/bin/python3 $MONITOR_DIR/monitor.py --report") | crontab -

print_info "Daily report scheduled for 9:00 AM"

# Create log rotation
print_step "Setting up log rotation..."

sudo tee /etc/logrotate.d/kafka-monitor > /dev/null << EOF
$MONITOR_DIR/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    copytruncate
    su wasadmin wasadmin
}
EOF

# Set up SSH key authentication for passwordless SSH (if needed)
print_step "Setting up SSH key authentication..."

if [[ ! -f ~/.ssh/id_rsa ]]; then
    print_info "Generating SSH key for inter-server communication..."
    ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa -N ""
    
    print_warning "SSH key generated. You need to copy the public key to other servers:"
    print_warning "Run the following on each target server:"
    echo "ssh-copy-id wasadmin@tpaldey2va029.ebiz.verizon.com"
    echo "ssh-copy-id wasladmin@tpaldey2va030.ebiz.verizon.com"
else
    print_info "SSH key already exists"
fi

# Create email templates
print_step "Creating email templates..."

# Create failure alert template
cat > $MONITOR_DIR/templates/failure_alert.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Service Failure Alert</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .alert { background: #ffebee; border: 1px solid #f44336; padding: 15px; border-radius: 5px; }
        .info { background: #e3f2fd; border: 1px solid #2196F3; padding: 15px; border-radius: 5px; margin-top: 15px; }
        .logs { background: #f5f5f5; padding: 10px; font-family: monospace; font-size: 12px; max-height: 300px; overflow-y: auto; }
    </style>
</head>
<body>
    <div class="alert">
        <h2>🚨 Service Alert: {{service_name}} on {{server_host}}</h2>
        <p><strong>Time:</strong> {{timestamp}}</p>
        <p><strong>Status:</strong> Service Down</p>
        <p><strong>Restart Attempted:</strong> {{restart_status}}</p>
    </div>
    
    <div class="info">
        <h3>AI Analysis</h3>
        <pre>{{ai_analysis}}</pre>
    </div>
    
    <div class="info">
        <h3>Recent Logs</h3>
        <div class="logs">{{log_content}}</div>
    </div>
</body>
</html>
EOF

# Create recovery notification template
cat > $MONITOR_DIR/templates/recovery_notification.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Service Recovery</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .success { background: #e8f5e8; border: 1px solid #4CAF50; padding: 15px; border-radius: 5px; }
        .info { background: #e3f2fd; border: 1px solid #2196F3; padding: 15px; border-radius: 5px; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="success">
        <h2>✅ Service Recovered: {{service_name}} on {{server_host}}</h2>
        <p><strong>Recovery Time:</strong> {{timestamp}}</p>
        <p><strong>Status:</strong> Service Restored</p>
    </div>
    
    <div class="info">
        <h3>Recovery Details</h3>
        <ul>
            <li>Service successfully restarted</li>
            <li>Port connectivity confirmed</li>
            <li>Monitoring resumed</li>
        </ul>
    </div>
</body>
</html>
EOF

# Create daily report template
cat > $MONITOR_DIR/templates/daily_report.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Daily Cluster Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #2196F3; color: white; padding: 15px; border-radius: 5px; }
        .metrics { display: flex; justify-content: space-around; margin: 20px 0; }
        .metric { text-align: center; padding: 15px; background: #f5f5f5; border-radius: 5px; }
        .services { margin: 20px 0; }
        .service { padding: 10px; border-bottom: 1px solid #eee; }
        .up { color: #4CAF50; }
        .down { color: #f44336; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Daily Kafka/Zookeeper Report</h1>
        <p>Generated: {{timestamp}}</p>
    </div>
    
    <div class="metrics">
        <div class="metric">
            <h3>{{total_services}}</h3>
            <p>Total Services</p>
        </div>
        <div class="metric">
            <h3>{{healthy_services}}</h3>
            <p>Healthy</p>
        </div>
        <div class="metric">
            <h3>{{failed_services}}</h3>
            <p>Failed</p>
        </div>
    </div>
    
    <div class="services">
        <h3>Service Status</h3>
        {{service_list}}
    </div>
    
    <div>
        <h3>🤖 AI Recommendations</h3>
        <pre>{{recommendations}}</pre>
    </div>
</body>
</html>
EOF

print_info "Email templates created"

# Set proper permissions
print_step "Setting file permissions..."
chmod +x $MONITOR_DIR/monitor.py
chmod +x $MONITOR_DIR/log_analyzer.py
chmod +x $MONITOR_DIR/email_sender.py
chmod 600 $MONITOR_DIR/config.yml

# Reload systemd and enable service
print_step "Enabling monitor service..."
sudo systemctl daemon-reload
sudo systemctl enable kafka-monitor

print_info "Service enabled (not started yet)"

# Create helper scripts
print_step "Creating helper scripts..."

# Start script
cat > $MONITOR_DIR/start_monitor.sh << 'EOF'
#!/bin/bash
echo "Starting Kafka Monitor..."
sudo systemctl start kafka-monitor
sudo systemctl status kafka-monitor
EOF

# Stop script
cat > $MONITOR_DIR/stop_monitor.sh << 'EOF'
#!/bin/bash
echo "Stopping Kafka Monitor..."
sudo systemctl stop kafka-monitor
sudo systemctl status kafka-monitor
EOF

# Status script
cat > $MONITOR_DIR/check_status.sh << 'EOF'
#!/bin/bash
echo "=== Kafka Monitor Status ==="
sudo systemctl status kafka-monitor

echo ""
echo "=== Recent Monitor Logs ==="
sudo journalctl -u kafka-monitor -n 20 --no-pager

echo ""
echo "=== Ollama Status ==="
sudo systemctl status ollama

echo ""
echo "=== Monitor Log Files ==="
ls -la /opt/kafka-monitor/logs/
EOF

# Test script
cat > $MONITOR_DIR/test_monitor.sh << 'EOF'
#!/bin/bash
echo "Testing Kafka Monitor..."
cd /opt/kafka-monitor
python3 monitor.py --once
EOF

# Make scripts executable
chmod +x $MONITOR_DIR/*.sh

# Create configuration validation script
cat > $MONITOR_DIR/validate_config.py << 'EOF'
#!/usr/bin/env python3
import yaml
import socket
import sys

def validate_config():
    try:
        with open('/opt/kafka-monitor/config.yml', 'r') as f:
            config = yaml.safe_load(f)
        
        print("✅ Config file loaded successfully")
        
        # Test server connectivity
        print("\n🔍 Testing server connectivity...")
        for server in config['servers']:
            host = server['host']
            for service in server['services']:
                port = service['port']
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    result = sock.connect_ex((host, port))
                    sock.close()
                    
                    if result == 0:
                        print(f"✅ {host}:{port} ({service['name']}) - Connected")
                    else:
                        print(f"❌ {host}:{port} ({service['name']}) - Connection failed")
                except Exception as e:
                    print(f"❌ {host}:{port} ({service['name']}) - Error: {e}")
        
        # Test email config
        print(f"\n📧 Email Configuration:")
        print(f"   SMTP Server: {config['email']['smtp_server']}:{config['email']['smtp_port']}")
        print(f"   From: {config['email']['from_email']}")
        print(f"   To: {', '.join(config['email']['to_emails'])}")
        
        # Test Ollama
        print(f"\n🤖 AI Configuration:")
        print(f"   Ollama URL: {config['ai']['ollama_url']}")
        print(f"   Model: {config['ai']['model']}")
        
        try:
            import requests
            response = requests.get(f"{config['ai']['ollama_url']}/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Ollama service is running")
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                if config['ai']['model'] in model_names:
                    print(f"✅ Model {config['ai']['model']} is available")
                else:
                    print(f"❌ Model {config['ai']['model']} not found. Available: {model_names}")
            else:
                print("❌ Ollama service not responding")
        except Exception as e:
            print(f"❌ Ollama test failed: {e}")
        
        print("\n✅ Configuration validation complete")
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

if __name__ == "__main__":
    if not validate_config():
        sys.exit(1)
EOF

chmod +x $MONITOR_DIR/validate_config.py

print_info "Helper scripts created"

# Final setup summary
print_step "Installation Summary"
cat << EOF

🎉 Kafka Monitor installation completed successfully!

📁 Installation Directory: $MONITOR_DIR

📋 What was installed:
   ✅ Python dependencies (pyyaml, requests, psutil)
   ✅ Ollama AI service with Llama3 8B model
   ✅ Systemd service (kafka-monitor.service)
   ✅ Log rotation configuration
   ✅ Daily report cron job (9:00 AM)
   ✅ Email templates
   ✅ Helper scripts

🔧 Next Steps:

1. Validate configuration:
   cd $MONITOR_DIR && python3 validate_config.py

2. Test the monitor (single run):
   cd $MONITOR_DIR && ./test_monitor.sh

3. Start the monitor service:
   ./start_monitor.sh

4. Check monitor status:
   ./check_status.sh

5. View logs:
   tail -f $MONITOR_DIR/logs/monitor.log
   journalctl -u kafka-monitor -f

⚠️  Important Notes:
   - SSH keys may need to be set up for remote server access
   - Ensure wasladmin has sudo privileges for systemctl commands
   - Email notifications use vzsmtp.verizon.com (no authentication)
   - Monitor runs continuously and checks services every 60 seconds
   - AI analysis requires Ollama service to be running

📧 Email Configuration:
   From: netula.siddhartha.yadav@verizon.com
   To: netula.siddhartha.yadav@verizon.com
   SMTP: vzsmtp.verizon.com:25

🤖 AI Features:
   - Local Ollama with Llama3 8B model
   - No external API keys required
   - Automatic log analysis on service failures
   - Health recommendations and root cause analysis

EOF

print_info "Installation complete! 🚀"
