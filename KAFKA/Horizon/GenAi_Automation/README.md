# Kafka/Zookeeper AI Monitor System

A comprehensive monitoring solution for Apache Kafka and Zookeeper clusters with AI-powered log analysis and automated recovery.

## 🚀 Quick Start

### 1. Installation

Run the installation script as `wasadmin` user:

```bash
# Download and run setup
curl -O https://raw.githubusercontent.com/your-repo/kafka-monitor/main/setup.sh
chmod +x setup.sh
./setup.sh
```

Or manually copy files to `/opt/kafka-monitor/` and run:

```bash
cd /opt/kafka-monitor
chmod +x setup.sh
./setup.sh
```

### 2. Configuration

The system is pre-configured for your Verizon environment:

**Servers Monitored:**
- `tpaldey2va028.ebiz.verizon.com` (Kafka + Zookeeper)
- `tpaldey2va029.ebiz.verizon.com` (Kafka + Zookeeper)  
- `tpaldey2va030.ebiz.verizon.com` (Kafka + Zookeeper)

**Services Monitored:**
- Zookeeper: Port 2181
- Kafka: Port 9092

### 3. Start Monitoring

```bash
cd /opt/kafka-monitor
./start_monitor.sh
```

## 📋 Features

### ✅ Service Monitoring
- **Port-based health checks** every 60 seconds
- **Automatic service restart** on failure
- **Multi-server cluster monitoring**
- **Dependency management** (Kafka depends on Zookeeper)

### 🤖 AI-Powered Analysis
- **Local Ollama** with Llama3 8B model (no external APIs)
- **Root cause analysis** of service failures
- **Intelligent recommendations** for problem resolution
- **Log pattern recognition** and error categorization

### 📧 Smart Notifications
- **Rich HTML email alerts** with detailed analysis
- **Recovery notifications** when services are restored
- **Daily cluster health reports** at 9:00 AM
- **Verizon SMTP integration** (vzsmtp.verizon.com)

### 🔄 Automated Recovery
- **Intelligent restart logic** with attempt limits
- **Cooldown periods** to prevent restart loops  
- **Cluster-aware operations** (respects service dependencies)
- **SSH-based remote management**

## 🛠️ Commands

### Monitor Control
```bash
# Start monitoring
./start_monitor.sh

# Stop monitoring  
./stop_monitor.sh

# Check status
./check_status.sh

# Test configuration
python3 validate_config.py

# Run single check
python3 monitor.py --once

# Generate daily report
python3 monitor.py --report
```

### View Logs
```bash
# Monitor application logs
tail -f logs/monitor.log

# System service logs
journalctl -u kafka-monitor -f

# Check specific service
systemctl status kafka-monitor
```

## 📁 Directory Structure

```
/opt/kafka-monitor/
├── monitor.py              # Main monitoring script
├── log_analyzer.py         # AI-powered log analysis
├── email_sender.py         # Email notification system
├── config.yml              # Configuration file
├── setup.sh               # Installation script
├── validate_config.py     # Configuration validator
├── logs/                  # Monitor logs
│   └── monitor.log
├── templates/             # Email templates
│   ├── failure_alert.html
│   ├── recovery_notification.html
│   └── daily_report.html
└── *.sh                   # Helper scripts
```

## ⚙️ Configuration

### Main Configuration (`config.yml`)

```yaml
# Monitoring settings
monitoring:
  check_interval_seconds: 60
  max_restart_attempts: 3
  restart_wait_time: 15

# Email settings  
email:
  smtp_server: "vzsmtp.verizon.com"
  smtp_port: 25
  from_email: "netula.siddhartha.yadav@verizon.com"
  to_emails:
    - "netula.siddhartha.yadav@verizon.com"

# AI settings
ai:
  ollama_url: "http://localhost:11434"
  model: "llama3:8b"
```

### Service Configuration

Each server and service is defined with:
- **Host**: Server hostname
- **Port**: Service port for health checks
- **Systemd name**: Service name for restart commands
- **Log file**: Path to service logs for analysis

## 🔧 Troubleshooting

### Common Issues

**1. Ollama Service Not Running**
```bash
sudo systemctl start ollama
ollama pull llama3:8b
```

**2. SSH Permission Errors**
```bash
# Set up SSH keys
ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa -N ""
ssh-copy-id wasadmin@target-server
```

**3. Service Restart Failures**
```bash
# Check sudo permissions
sudo systemctl restart kafka
sudo systemctl restart zookeeper
```

**4. Email Not Sending**
```bash
# Test SMTP connectivity
telnet vzsmtp.verizon.com 25
```

### Debug Mode

Enable debug logging:
```yaml
# In config.yml
logging:
  level: "DEBUG"
```

### Manual Testing

Test individual components:
```bash
# Test port connectivity
python3 -c "import socket; print(socket.create_connection(('server', 9092), 5))"

# Test AI analysis
python3 -c "from log_analyzer import LogAnalyzer; import yaml; config=yaml.safe_load(open('config.yml')); analyzer=LogAnalyzer(config); print('AI Ready')"

# Test email
python3 -c "from email_sender import EmailSender; import yaml; config=yaml.safe_load(open('config.yml')); sender=EmailSender(config); sender.send_email('Test', 'Test email', 'Test')"
```

## 📊 Monitoring Dashboard

The system provides several types of notifications:

### 🚨 Failure Alerts
- **Service down detection**
- **AI-powered root cause analysis** 
- **Recommended actions**
- **Recent log excerpts**
- **Restart attempt status**

### ✅ Recovery Notifications
- **Service restoration confirmation**
- **Recovery timeline**
- **Health check results**

### 📈 Daily Reports
- **Cluster health summary**
- **Service availability metrics**
- **AI recommendations**
- **Trend analysis**

## 🔐 Security

- **No external API keys** required (uses local Ollama)
- **SSH key authentication** for remote management
- **Service runs as wasadmin** user
- **Log rotation** and cleanup
- **Secure email templates** (no credential exposure)

## 🤖 AI Features

### Root Cause Analysis
The AI analyzer examines log files and provides:
- **Problem summary** in plain language
- **Technical root cause** explanation  
- **Severity assessment** (Critical/High/Medium/Low)
- **Step-by-step solutions**
- **Prevention recommendations**

### Smart Pattern Recognition
- **Error pattern detection** using regex and AI
- **Service dependency mapping**
- **Historical failure analysis**
- **Predictive recommendations**

## 📞 Support

### Log Files to Check
1. **Monitor logs**: `/opt/kafka-monitor/logs/monitor.log`
2. **System logs**: `journalctl -u kafka-monitor`
3. **Kafka logs**: `/opt/app/KAFKA/kafka_2.12-3.1.1/logs/server.log`
4. **Zookeeper logs**: `/opt/app/KAFKA/kafka_2.12-3.1.1/logs/zookeeper.out`

### Contact Information
- **Primary Contact**: netula.siddhartha.yadav@verizon.com
- **System**: Verizon Kafka/Zookeeper Cluster
- **Environment**: Production

## 🔄 Maintenance

### Regular Tasks
- **Weekly**: Review monitor logs and adjust thresholds
- **Monthly**: Update AI model if newer versions available
- **Quarterly**: Review and update email templates
- **As needed**: Adjust monitoring intervals based on workload

### Updates
```bash
# Update configuration
vi /opt/kafka-monitor/config.yml
sudo systemctl restart kafka-monitor

# Update AI model
ollama pull llama3:8b
sudo systemctl restart kafka-monitor

# Check for system updates
sudo yum update
```

---

**Monitor Version**: 1.0  
**Last Updated**: 2025  
**Environment**: Verizon Production Kafka Cluster
