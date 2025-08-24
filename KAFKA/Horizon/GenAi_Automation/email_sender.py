#!/usr/bin/env python3
"""
email_sender.py
Email notification system using Verizon SMTP
Sends detailed failure alerts and recovery notifications
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime

class EmailSender:
    def __init__(self, config):
        self.config = config
        self.email_config = config['email']
        self.logger = logging.getLogger(__name__)
        
    def send_email(self, subject, body_html, body_text=None):
        """Send email notification with HTML and text versions"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = self.email_config['from_email']
            msg['To'] = ', '.join(self.email_config['to_emails'])
            
            # Add text version if provided
            if body_text:
                text_part = MIMEText(body_text, 'plain', 'utf-8')
                msg.attach(text_part)
            
            # Add HTML version
            html_part = MIMEText(body_html, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'], timeout=30) as server:
                server.send_message(msg)
            
            self.logger.info(f"Email sent successfully: {subject}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email '{subject}': {e}")
            return False
    
    def send_failure_alert(self, server_host, service_name, log_content, ai_analysis, restart_attempted, restart_attempts):
        """Send detailed service failure alert"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        subject = f"🚨 ALERT: {service_name.upper()} Service Down on {server_host} - {timestamp}"
        
        # Create HTML email body
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .status-value {{ font-size: 18px; font-weight: bold; margin: 5px 0; }}
                .status-down {{ color: #d32f2f; }}
                .status-attempted {{ color: #ff9800; }}
                .status-failed {{ color: #d32f2f; }}
                .ai-analysis {{ background: linear-gradient(135deg, #e8f5e8, #f1f8e9); border-left: 4px solid #4CAF50; padding: 15px; margin: 15px 0; border-radius: 6px; }}
                .logs-section {{ background: #f5f5f5; border: 1px solid #ddd; border-radius: 6px; margin: 15px 0; }}
                .logs-header {{ background: #333; color: white; padding: 10px 15px; font-family: monospace; font-size: 14px; }}
                .logs-content {{ padding: 15px; max-height: 400px; overflow-y: auto; font-family: monospace; font-size: 12px; line-height: 1.4; white-space: pre-wrap; }}
                .action-list {{ background: #fff3e0; padding: 15px; border-radius: 6px; border-left: 4px solid #ff9800; }}
                .action-list ol {{ margin: 0; padding-left: 20px; }}
                .action-list li {{ margin-bottom: 8px; }}
                .footer {{ background: #f8f9fa; padding: 15px; text-align: center; color: #666; font-size: 12px; }}
                .timestamp {{ color: #666; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="alert-icon">⚠️</div>
                    <h1>Service Failure Alert</h1>
                    <div class="timestamp">Alert generated at {timestamp}</div>
                </div>
                
                <div class="content">
                    <div class="status-grid">
                        <div class="status-card">
                            <div>Service</div>
                            <div class="status-value status-down">{service_name.upper()}</div>
                        </div>
                        <div class="status-card">
                            <div>Server</div>
                            <div class="status-value">{server_host}</div>
                        </div>
                        <div class="status-card">
                            <div>Status</div>
                            <div class="status-value status-down">DOWN ❌</div>
                        </div>
                        <div class="status-card">
                            <div>Auto Restart</div>
                            <div class="status-value {'status-attempted' if restart_attempted else 'status-failed'}">
                                {'ATTEMPTED' if restart_attempted else 'FAILED'}
                            </div>
                        </div>
                        <div class="status-card">
                            <div>Restart Attempts</div>
                            <div class="status-value">{restart_attempts}</div>
                        </div>
                    </div>
                    
                    <div class="ai-analysis">
                        <h3>🤖 AI Analysis & Recommendations</h3>
                        <pre style="white-space: pre-wrap; font-family: Arial, sans-serif; margin: 0;">{ai_analysis}</pre>
                    </div>
                    
                    <div class="section">
                        <h3>📋 Actions Taken</h3>
                        <ul>
                            <li>✅ Service health check performed</li>
                            <li>{'✅' if restart_attempted else '❌'} Automatic restart {'attempted' if restart_attempted else 'skipped'}</li>
                            <li>✅ Log analysis completed</li>
                            <li>✅ Team notification sent</li>
                        </ul>
                    </div>
                    
                    <div class="action-list">
                        <h3>🔧 Immediate Next Steps</h3>
                        <ol>
                            <li>SSH to <strong>{server_host}</strong> and check system resources</li>
                            <li>Manual service restart: <code>sudo systemctl restart {service_name}</code></li>
                            <li>Review full logs: <code>journalctl -u {service_name} -f</code></li>
                            <li>Check dependencies (Zookeeper for Kafka)</li>
                            <li>Verify configuration files</li>
                        </ol>
                    </div>
                    
                    <div class="logs-section">
                        <div class="logs-header">
                            📄 Recent Service Logs (Last 500 lines)
                        </div>
                        <div class="logs-content">{self._escape_html(log_content[:4000])}{'...\n[LOG TRUNCATED - CHECK SERVER FOR FULL LOGS]' if len(log_content) > 4000 else ''}</div>
                    </div>
                </div>
                
                <div class="footer">
                    <p>This alert was automatically generated by the Kafka Monitor System</p>
                    <p>Server: {server_host} | Monitor Version: 1.0</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create text version for email clients that don't support HTML
        text_body = f"""
KAFKA/ZOOKEEPER SERVICE FAILURE ALERT
=====================================

Service: {service_name.upper()}
Server: {server_host}
Status: DOWN
Timestamp: {timestamp}
Auto Restart: {'ATTEMPTED' if restart_attempted else 'FAILED'}
Restart Attempts: {restart_attempts}

AI ANALYSIS:
{ai_analysis}

RECENT LOGS:
{log_content[:2000]}{'...[TRUNCATED]' if len(log_content) > 2000 else ''}

IMMEDIATE ACTIONS:
1. SSH to {server_host} and check system resources
2. Manual restart: sudo systemctl restart {service_name}
3. Check logs: journalctl -u {service_name} -f
4. Verify dependencies and configuration

This alert was automatically generated by the Kafka Monitor System.
        """
        
        return self.send_email(subject, html_body, text_body)
    
    def send_recovery_notification(self, server_host, service_name, recovery_time):
        """Send service recovery notification"""
        timestamp = recovery_time.strftime("%Y-%m-%d %H:%M:%S")
        subject = f"✅ RECOVERY: {service_name.upper()} Service Restored on {server_host}"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #4CAF50, #66BB6A); color: white; padding: 20px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 24px; }}
                .success-icon {{ font-size: 48px; margin-bottom: 10px; }}
                .content {{ padding: 20px; }}
                .status-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px; }}
                .status-card {{ background: #e8f5e8; padding: 15px; border-radius: 6px; text-align: center; }}
                .status-value {{ font-size: 18px; font-weight: bold; margin: 5px 0; color: #2e7d32; }}
                .info-section {{ background: #f1f8e9; padding: 15px; border-radius: 6px; border-left: 4px solid #4CAF50; }}
                .footer {{ background: #f8f9fa; padding: 15px; text-align: center; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="success-icon">✅</div>
                    <h1>Service Recovery Notification</h1>
                    <div style="color: #e8f5e8; font-size: 14px;">Recovery confirmed at {timestamp}</div>
                </div>
                
                <div class="content">
                    <div class="status-grid">
                        <div class="status-card">
                            <div>Service</div>
                            <div class="status-value">{service_name.upper()}</div>
                        </div>
                        <div class="status-card">
                            <div>Server</div>
                            <div class="status-value">{server_host}</div>
                        </div>
                        <div class="status-card">
                            <div>Status</div>
                            <div class="status-value">RESTORED ✅</div>
                        </div>
                    </div>
                    
                    <div class="info-section">
                        <h3>Recovery Summary</h3>
                        <ul>
                            <li>✅ Service successfully restarted</li>
                            <li>✅ Port connectivity confirmed</li>
                            <li>✅ Service health verified</li>
                            <li>✅ Monitoring resumed</li>
                        </ul>
                    </div>
                    
                    <div style="margin-top: 20px; padding: 15px; background: #fff3e0; border-radius: 6px;">
                        <h3>Recommended Follow-up Actions</h3>
                        <ol>
                            <li>Monitor service stability over the next hour</li>
                            <li>Review logs for any warning messages</li>
                            <li>Check system resources to prevent recurrence</li>
                            <li>Update runbooks if new patterns identified</li>
                        </ol>
                    </div>
                </div>
                
                <div class="footer">
                    <p>Service recovery automatically detected by Kafka Monitor System</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
SERVICE RECOVERY NOTIFICATION
============================

Service: {service_name.upper()}
Server: {server_host}
Status: RESTORED
Recovery Time: {timestamp}

RECOVERY ACTIONS COMPLETED:
- Service successfully restarted
- Port connectivity confirmed
- Service health verified
- Monitoring resumed

FOLLOW-UP RECOMMENDED:
1. Monitor service stability
2. Review logs for warnings
3. Check system resources
4. Update documentation

This notification was automatically generated by the Kafka Monitor System.
        """
        
        return self.send_email(subject, html_body, text_body)
    
    def send_daily_report(self, service_status, health_recommendations):
        """Send daily cluster health report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        total_services = len(service_status)
        healthy_services = sum(1 for status in service_status.values() if status)
        failed_services = total_services - healthy_services
        
        health_color = "#4CAF50" if failed_services == 0 else "#ff9800" if failed_services < 3 else "#d32f2f"
        health_status = "HEALTHY" if failed_services == 0 else "DEGRADED" if failed_services < 3 else "CRITICAL"
        
        subject = f"📊 Daily Kafka/Zookeeper Cluster Report - {datetime.now().strftime('%Y-%m-%d')}"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background-color: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, {health_color}, {health_color}cc); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 25px; }}
                .metric-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }}
                .metric-value {{ font-size: 32px; font-weight: bold; margin: 10px 0; }}
                .metric-label {{ color: #666; font-size: 14px; }}
                .services-list {{ background: #f8f9fa; border-radius: 8px; padding: 15px; margin: 15px 0; }}
                .service-item {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; }}
                .service-status {{ font-weight: bold; }}
                .status-up {{ color: #4CAF50; }}
                .status-down {{ color: #d32f2f; }}
                .recommendations {{ background: #e3f2fd; border-left: 4px solid #2196F3; padding: 15px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Cluster Health Report</h1>
                    <h2>Overall Status: {health_status}</h2>
                    <div>Report generated: {timestamp}</div>
                </div>
                
                <div class="content">
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-value" style="color: {health_color};">{total_services}</div>
                            <div class="metric-label">Total Services</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value" style="color: #4CAF50;">{healthy_services}</div>
                            <div class="metric-label">Healthy Services</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value" style="color: #d32f2f;">{failed_services}</div>
                            <div class="metric-label">Failed Services</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value" style="color: #2196F3;">{int((healthy_services/total_services)*100)}%</div>
                            <div class="metric-label">Availability</div>
                        </div>
                    </div>
                    
                    <h3>Service Status Details</h3>
                    <div class="services-list">
        """
        
        for service_key, status in service_status.items():
            status_class = "status-up" if status else "status-down"
            status_text = "UP ✅" if status else "DOWN ❌"
            html_body += f"""
                        <div class="service-item">
                            <span>{service_key}</span>
                            <span class="service-status {status_class}">{status_text}</span>
                        </div>
            """
        
        html_body += f"""
                    </div>
                    
                    <div class="recommendations">
                        <h3>🤖 AI Health Recommendations</h3>
                        <pre style="white-space: pre-wrap; font-family: Arial, sans-serif;">{health_recommendations}</pre>
                    </div>
                    
                    <div style="margin-top: 25px; padding: 15px; background: #fff3e0; border-radius: 8px;">
                        <h3>📈 Monitoring Actions</h3>
                        <ul>
                            <li>Review system resource utilization</li>
                            <li>Check disk space on all servers</li>
                            <li>Verify backup completion status</li>
                            <li>Update capacity planning metrics</li>
                        </ul>
                    </div>
                </div>
                
                <div style="background: #f8f9fa; padding: 15px; text-align: center; color: #666; font-size: 12px;">
                    <p>Daily report automatically generated by Kafka Monitor System</p>
                    <p>Next report scheduled for tomorrow at the same time</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(subject, html_body)
    
    def _escape_html(self, text):
        """Escape HTML characters in text"""
        if not text:
            return ""
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#x27;'))container {{ max-width: 800px; margin: 0 auto; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #d32f2f, #f44336); color: white; padding: 20px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 24px; }}
                .alert-icon {{ font-size: 48px; margin-bottom: 10px; }}
                .content {{ padding: 20px; }}
                .section {{ margin-bottom: 25px; border-left: 4px solid #2196F3; padding-left: 15px; }}
                .section h3 {{ color: #1976D2; margin-top: 0; }}
                .status-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }}
                .status-card {{ background: #f8f9fa; padding: 15px; border-radius: 6px; text-align: center; }}
             
