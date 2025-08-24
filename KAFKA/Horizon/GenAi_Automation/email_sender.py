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
                .container {{ max-width: 800px; margin: 0 auto; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #d32f2f, #f44336); color: white; padding: 20px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 24px; }}
                .alert-icon {{ font-size: 48px; margin-bottom: 10px; }}
                .content {{ padding: 20px; }}
                .section {{ margin-bottom: 25px; border-left: 4px solid #2196F3; padding-left: 15px; }}
                .section h3 {{ color: #1976D2; margin-top: 0; }}
                .status-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }}
                .status-card {{ background: #f8f9fa; padding: 15px; border-radius: 6px; text-align: center; }}
                .
