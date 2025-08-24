#!/usr/bin/env python3
"""
monitor.py
Main monitoring script for Kafka/Zookeeper cluster
- Checks service status via port connectivity
- Attempts service restart on failure
- Triggers AI log analysis if restart fails
- Sends email notifications
"""

import os
import sys
import socket
import subprocess
import time
import yaml
import logging
import threading
from datetime import datetime, timedelta
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from log_analyzer import LogAnalyzer
from email_sender import EmailSender

class KafkaMonitor:
    def __init__(self, config_path="/opt/kafka-monitor/config.yml"):
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.analyzer = LogAnalyzer(self.config)
        self.emailer = EmailSender(self.config)
        
        # Service state tracking
        self.service_states = {}
        self.last_failure_time = {}
        self.restart_attempts = {}
        
        # Initialize service states
        for server in self.config['servers']:
            for service in server['services']:
                key = f"{server['host']}:{service['name']}"
                self.service_states[key] = True
                self.last_failure_time[key] = None
                self.restart_attempts[key] = 0
        
    def load_config(self, config_path):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            sys.exit(1)
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path(self.config['logging']['directory'])
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / 'monitor.log'
        
        logging.basicConfig(
            level=getattr(logging, self.config['logging']['level']),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Monitor initialized")
    
    def check_port(self, host, port, timeout=5):
        """Check if a TCP port is open"""
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except Exception as e:
            self.logger.debug(f"Port check failed for {host}:{port} - {e}")
            return False
    
    def check_service_status(self, server, service):
        """Check if a service is running via port connectivity"""
        host = server['host']
        port = service['port']
        service_name = service['name']
        
        is_up = self.check_port(host, port)
        service_key = f"{host}:{service_name}"
        
        if is_up:
            if not self.service_states.get(service_key, True):
                # Service recovered
                self.logger.info(f"Service recovered: {service_key}")
                self.service_states[service_key] = True
                self.restart_attempts[service_key] = 0
                
                # Send recovery notification
                self.emailer.send_recovery_notification(
                    server_host=host,
                    service_name=service_name,
                    recovery_time=datetime.now()
                )
        else:
            if self.service_states.get(service_key, True):
                # Service just went down
                self.logger.warning(f"Service failure detected: {service_key}")
                self.service_states[service_key] = False
                self.last_failure_time[service_key] = datetime.now()
        
        return is_up
    
    def restart_service(self, server, service):
        """Attempt to restart a service via SSH"""
        host = server['host']
        service_name = service['name']
        service_key = f"{host}:{service_name}"
        
        # Check restart attempt limits
        max_attempts = self.config['monitoring']['max_restart_attempts']
        if self.restart_attempts[service_key] >= max_attempts:
            self.logger.error(f"Max restart attempts ({max_attempts}) reached for {service_key}")
            return False
        
        self.restart_attempts[service_key] += 1
        
        try:
            self.logger.info(f"Attempting to restart {service_key} (attempt {self.restart_attempts[service_key]})")
            
            # Use systemctl to restart the service
            # Since we're running as wasadmin, we need sudo privileges
            restart_command = f"sudo systemctl restart {service['systemd_name']}"
            
            if host == socket.gethostname() or host.startswith(socket.gethostname().split('.')[0]):
                # Local restart
                result = subprocess.run(
                    restart_command.split(),
                    capture_output=True,
                    text=True,
                    timeout=60
                )
            else:
                # Remote restart via SSH
                ssh_command = [
                    'ssh', f"wasadmin@{host}",
                    restart_command
                ]
                result = subprocess.run(
                    ssh_command,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
            
            if result.returncode == 0:
                self.logger.info(f"Restart command executed successfully for {service_key}")
                
                # Wait for service to start
                time.sleep(self.config['monitoring']['restart_wait_time'])
                
                # Check if service is now running
                if self.check_port(host, service['port']):
                    self.logger.info(f"Service {service_key} successfully restarted")
                    return True
                else:
                    self.logger.warning(f"Service {service_key} restart failed - port not accessible")
                    return False
            else:
                self.logger.error(f"Restart command failed for {service_key}: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"Restart command timed out for {service_key}")
            return False
        except Exception as e:
            self.logger.error(f"Error restarting {service_key}: {e}")
            return False
    
    def get_log_content(self, server, service):
        """Get recent log content from service log file"""
        host = server['host']
        log_file = service['log_file']
        lines = self.config['monitoring']['log_lines_to_analyze']
        
        try:
            if host == socket.gethostname() or host.startswith(socket.gethostname().split('.')[0]):
                # Local log reading
                result = subprocess.run(
                    ['tail', '-n', str(lines), log_file],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            else:
                # Remote log reading via SSH
                ssh_command = [
                    'ssh', f"wasadmin@{host}",
                    f'tail -n {lines} {log_file}'
                ]
                result = subprocess.run(
                    ssh_command,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            
            if result.returncode == 0:
                return result.stdout
            else:
                self.logger.error(f"Failed to read log from {host}:{log_file}")
                return f"Error reading log file: {result.stderr}"
                
        except Exception as e:
            self.logger.error(f"Error getting log content from {host}: {e}")
            return f"Error accessing log file: {str(e)}"
    
    def handle_service_failure(self, server, service):
        """Handle service failure - restart and analyze if needed"""
        host = server['host']
        service_name = service['name']
        service_key = f"{host}:{service_name}"
        
        self.logger.warning(f"Handling service failure: {service_key}")
        
        # Attempt restart
        restart_success = self.restart_service(server, service)
        
        if restart_success:
            self.logger.info(f"Service {service_key} successfully recovered via restart")
            return True
        
        # If restart failed, get logs and analyze
        self.logger.warning(f"Service {service_key} restart failed, analyzing logs")
        
        log_content = self.get_log_content(server, service)
        
        # Get AI analysis of the logs
        ai_analysis = self.analyzer.analyze_service_logs(
            service_name=service_name,
            log_content=log_content,
            server_host=host
        )
        
        # Send failure notification with analysis
        self.emailer.send_failure_alert(
            server_host=host,
            service_name=service_name,
            log_content=log_content,
            ai_analysis=ai_analysis,
            restart_attempted=True,
            restart_attempts=self.restart_attempts[service_key]
        )
        
        return False
    
    def monitor_cycle(self):
        """Single monitoring cycle - check all services"""
        self.logger.info("Starting monitoring cycle")
        
        all_services_up = True
        failed_services = []
        
        for server in self.config['servers']:
            for service in server['services']:
                service_key = f"{server['host']}:{service['name']}"
                
                is_up = self.check_service_status(server, service)
                
                if not is_up:
                    all_services_up = False
                    failed_services.append({
                        'server': server,
                        'service': service,
                        'key': service_key
                    })
                    
                    # Check if we should handle this failure
                    if self.should_handle_failure(service_key):
                        self.handle_service_failure(server, service)
        
        # Log cycle completion
        if all_services_up:
            self.logger.info("All services are running normally")
        else:
            self.logger.warning(f"Services down: {[fs['key'] for fs in failed_services]}")
        
        return all_services_up
    
    def should_handle_failure(self, service_key):
        """Determine if we should handle this service failure"""
        # Avoid handling the same failure too frequently
        min_interval = timedelta(minutes=self.config['monitoring']['min_failure_interval'])
        
        last_failure = self.last_failure_time.get(service_key)
        if last_failure and datetime.now() - last_failure < min_interval:
            return False
        
        # Check if we've exceeded max restart attempts
        max_attempts = self.config['monitoring']['max_restart_attempts']
        if self.restart_attempts.get(service_key, 0) >= max_attempts:
            # Reset attempts after cooldown period
            cooldown = timedelta(minutes=self.config['monitoring']['restart_cooldown_minutes'])
            if last_failure and datetime.now() - last_failure > cooldown:
                self.restart_attempts[service_key] = 0
                return True
            return False
        
        return True
    
    def run_continuous_monitoring(self):
        """Run continuous monitoring loop"""
        self.logger.info("Starting continuous monitoring")
        
        check_interval = self.config['monitoring']['check_interval_seconds']
        
        while True:
            try:
                self.monitor_cycle()
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                self.logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(30)  # Wait before retrying
    
    def send_daily_report(self):
        """Send daily health report"""
        self.logger.info("Generating daily health report")
        
        service_status = {}
        for server in self.config['servers']:
            for service in server['services']:
                service_key = f"{server['host']}:{service['name']}"
                service_status[service_key] = self.check_port(server['host'], service['port'])
        
        # Get AI recommendations for overall cluster health
        health_recommendations = self.analyzer.generate_health_recommendations(service_status)
        
        self.emailer.send_daily_report(service_status, health_recommendations)

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--once':
            # Run single monitoring cycle
            monitor = KafkaMonitor()
            monitor.monitor_cycle()
        elif sys.argv[1] == '--report':
            # Send daily report
            monitor = KafkaMonitor()
            monitor.send_daily_report()
        else:
            print("Usage: python3 monitor.py [--once|--report]")
    else:
        # Run continuous monitoring
        monitor = KafkaMonitor()
        monitor.run_continuous_monitoring()

if __name__ == "__main__":
    main()
