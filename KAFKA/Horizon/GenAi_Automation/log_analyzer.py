#!/usr/bin/env python3
"""
log_analyzer.py
AI-powered log analysis using local Ollama
No external API keys required
"""

import requests
import json
import logging
import re
import subprocess
import time
from datetime import datetime

class LogAnalyzer:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Ollama configuration
        self.ollama_url = config['ai']['ollama_url']
        self.model = config['ai']['model']
        
        # Test Ollama connection
        self.ensure_ollama_ready()
        
    def ensure_ollama_ready(self):
        """Ensure Ollama is running and model is available"""
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = [m['name'] for m in models]
                
                if self.model in available_models:
                    self.logger.info(f"Ollama ready with model: {self.model}")
                else:
                    self.logger.warning(f"Model {self.model} not found. Available: {available_models}")
                    self.pull_model()
            else:
                self.logger.error(f"Ollama not responding: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            self.logger.error("Cannot connect to Ollama. Attempting to start...")
            self.start_ollama()
        except Exception as e:
            self.logger.error(f"Error checking Ollama: {e}")
    
    def start_ollama(self):
        """Start Ollama service if not running"""
        try:
            self.logger.info("Starting Ollama service...")
            subprocess.run(['sudo', 'systemctl', 'start', 'ollama'], check=True)
            time.sleep(10)  # Wait for service to start
            
            # Verify it started
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=15)
            if response.status_code == 200:
                self.logger.info("Ollama service started successfully")
            else:
                self.logger.error("Ollama service failed to start properly")
                
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to start Ollama: {e}")
        except Exception as e:
            self.logger.error(f"Error starting Ollama: {e}")
    
    def pull_model(self):
        """Pull the required model if not available"""
        try:
            self.logger.info(f"Pulling model {self.model}...")
            
            response = requests.post(
                f"{self.ollama_url}/api/pull",
                json={"name": self.model},
                timeout=600  # 10 minutes for model download
            )
            
            if response.status_code == 200:
                self.logger.info(f"Successfully pulled model {self.model}")
            else:
                self.logger.error(f"Failed to pull model: {response.text}")
                
        except Exception as e:
            self.logger.error(f"Error pulling model: {e}")
    
    def call_ollama(self, prompt, max_retries=3):
        """Call Ollama API with retry logic"""
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.2,
                            "top_p": 0.9,
                            "num_predict": 1000
                        }
                    },
                    timeout=120
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get('response', 'No response generated')
                else:
                    self.logger.error(f"Ollama API error: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                self.logger.warning(f"Ollama timeout (attempt {attempt + 1}/{max_retries})")
            except requests.exceptions.ConnectionError:
                self.logger.error("Ollama connection failed")
                if attempt == 0:  # Try to restart on first failure
                    self.start_ollama()
            except Exception as e:
                self.logger.error(f"Error calling Ollama: {e}")
            
            if attempt < max_retries - 1:
                time.sleep(5)
        
        # Fallback to rule-based analysis
        return self.rule_based_analysis(prompt)
    
    def analyze_service_logs(self, service_name, log_content, server_host):
        """Analyze service logs using AI"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extract key error patterns first
        key_errors = self.extract_error_patterns(log_content)
        
        prompt = f"""You are an expert system administrator specializing in Apache Kafka and Zookeeper.

ANALYSIS REQUEST:
- Service: {service_name}
- Server: {server_host}
- Timestamp: {timestamp}
- Log lines analyzed: {len(log_content.splitlines())}

KEY ERROR PATTERNS FOUND:
{chr(10).join(key_errors[-20:])}

RECENT LOG CONTENT:
{log_content[-2000:]}

Please analyze this {service_name} failure and provide:

PROBLEM SUMMARY:
[Brief description of the main issue in 2-3 sentences]

ROOT CAUSE:
[Detailed technical explanation of what went wrong]

SEVERITY LEVEL:
[Critical/High/Medium/Low] - [Reason for this severity level]

IMMEDIATE ACTIONS:
1. [Most urgent action to take right now]
2. [Second priority action]
3. [Third priority action]

SOLUTION STEPS:
1. [Step-by-step solution to fix the issue]
2. [Continue with detailed steps]
3. [Include any configuration changes needed]

PREVENTION MEASURES:
- [How to prevent this issue in the future]
- [Monitoring improvements needed]
- [Configuration recommendations]

RELATED COMPONENTS:
[What other services/components might be affected]
"""

        analysis = self.call_ollama(prompt)
        self.logger.info(f"Generated AI analysis for {service_name} on {server_host}")
        return analysis
    
    def generate_health_recommendations(self, service_status):
        """Generate cluster health recommendations"""
        failed_services = [k for k, v in service_status.items() if not v]
        healthy_services = [k for k, v in service_status.items() if v]
        
        prompt = f"""You are a Kafka/Zookeeper cluster expert. Analyze this cluster status:

CLUSTER STATUS:
- Total services: {len(service_status)}
- Healthy services: {len(healthy_services)}
- Failed services: {len(failed_services)}

HEALTHY SERVICES:
{chr(10).join(healthy_services)}

FAILED SERVICES:
{chr(10).join(failed_services)}

Provide cluster health recommendations:

CLUSTER HEALTH ASSESSMENT:
[Overall assessment of cluster health]

PRIORITY ACTIONS:
1. [Most important action for cluster stability]
2. [Second priority action]
3. [Third priority action]

MONITORING RECOMMENDATIONS:
- [Key metrics to monitor]
- [Alert thresholds to set]
- [Dashboard improvements]

INFRASTRUCTURE RECOMMENDATIONS:
- [Resource allocation suggestions]
- [Network configuration improvements]
- [Backup and recovery enhancements]

OPERATIONAL IMPROVEMENTS:
- [Process improvements]
- [Automation opportunities]
- [Documentation updates needed]
"""

        recommendations = self.call_ollama(prompt)
        self.logger.info("Generated cluster health recommendations")
        return recommendations
    
    def extract_error_patterns(self, log_content):
        """Extract error patterns using regex"""
        error_patterns = [
            r'.*ERROR.*',
            r'.*FATAL.*',
            r'.*Exception.*',
            r'.*Failed to.*',
            r'.*Connection refused.*',
            r'.*OutOfMemoryError.*',
            r'.*BindException.*',
            r'.*TimeoutException.*',
            r'.*UnknownHostException.*',
            r'.*Unable to.*',
            r'.*Cannot.*',
            r'.*WARN.*',
            r'.*Shutdown.*',
            r'.*Retrying.*',
            r'.*Disconnected.*'
        ]
        
        found_errors = []
        lines = log_content.split('\n')
        
        for line in lines[-500:]:  # Check last 500 lines
            line = line.strip()
            if not line:
                continue
                
            for pattern in error_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    found_errors.append(line)
                    break
        
        return found_errors
    
    def rule_based_analysis(self, prompt):
        """Fallback rule-based analysis when AI is unavailable"""
        self.logger.warning("Using rule-based analysis - AI unavailable")
        
        analysis = "AI ANALYSIS UNAVAILABLE - USING RULE-BASED FALLBACK\n\n"
        
        if "kafka" in prompt.lower():
            analysis += self.kafka_rule_analysis(prompt)
        elif "zookeeper" in prompt.lower():
            analysis += self.zookeeper_rule_analysis(prompt)
        else:
            analysis += self.generic_rule_analysis(prompt)
        
        return analysis
    
    def kafka_rule_analysis(self, prompt):
        """Rule-based Kafka analysis"""
        issues = []
        solutions = []
        
        if "OutOfMemoryError" in prompt:
            issues.append("JVM heap memory exhaustion")
            solutions.append("Increase heap size in KAFKA_HEAP_OPTS")
            solutions.append("Check for memory leaks in producers/consumers")
        
        if "BindException" in prompt or "Address already in use" in prompt:
            issues.append("Port conflict or service already running")
            solutions.append("Check if another Kafka instance is running")
            solutions.append("Verify port configuration in server.properties")
        
        if "Connection refused" in prompt:
            issues.append("Network connectivity issues")
            solutions.append("Check if Zookeeper is running")
            solutions.append("Verify network configuration and firewall rules")
        
        if "zookeeper" in prompt.lower():
            issues.append("Zookeeper connectivity problems")
            solutions.append("Restart Zookeeper service")
            solutions.append("Check Zookeeper configuration")
        
        return f"""
PROBLEM SUMMARY:
Kafka service failure detected. Issues found: {', '.join(issues) if issues else 'Unknown issue'}

ROOT CAUSE:
Based on log patterns, this appears to be related to {issues[0] if issues else 'service startup failure'}

SEVERITY LEVEL:
High - Kafka service disruption affects message processing

IMMEDIATE ACTIONS:
1. Check system resources (memory, disk, CPU)
2. Verify Zookeeper connectivity
3. Review Kafka configuration files

SOLUTION STEPS:
{chr(10).join([f"{i+1}. {sol}" for i, sol in enumerate(solutions[:5])])}

PREVENTION MEASURES:
- Monitor JVM heap usage
- Set up resource monitoring alerts
- Regular log rotation and cleanup
- Network connectivity monitoring
"""
    
    def zookeeper_rule_analysis(self, prompt):
        """Rule-based Zookeeper analysis"""
        return """
PROBLEM SUMMARY:
Zookeeper service failure detected. This is critical as it affects the entire Kafka cluster.

ROOT CAUSE:
Zookeeper service failure - common causes include resource exhaustion, configuration issues, or network problems.

SEVERITY LEVEL:
Critical - Zookeeper failure impacts all Kafka brokers

IMMEDIATE ACTIONS:
1. Check Zookeeper process status
2. Verify available disk space in Zookeeper data directory
3. Check network connectivity between Zookeeper nodes

SOLUTION STEPS:
1. Restart Zookeeper service: sudo systemctl restart zookeeper
2. Check Zookeeper logs for specific error messages
3. Verify Zookeeper configuration in zookeeper.properties
4. Ensure proper file permissions on data directories
5. Check system resources (memory, disk space)

PREVENTION MEASURES:
- Monitor Zookeeper ensemble health
- Set up disk space monitoring
- Regular backup of Zookeeper data
- Network connectivity monitoring between nodes
"""
    
    def generic_rule_analysis(self, prompt):
        """Generic rule-based analysis"""
        return """
PROBLEM SUMMARY:
Service failure detected. Manual investigation required due to AI analysis unavailability.

ROOT CAUSE:
Unable to determine specific root cause without AI analysis. Manual log review needed.

SEVERITY LEVEL:
Medium - Service disruption requires attention

IMMEDIATE ACTIONS:
1. Check service status: systemctl status <service>
2. Review system resources
3. Check recent system changes

SOLUTION STEPS:
1. Attempt service restart
2. Check configuration files for errors
3. Review system logs for additional context
4. Verify dependencies are running
5. Contact system administrator if issue persists

PREVENTION MEASURES:
- Regular system health monitoring
- Proper log management
- System resource monitoring
- Regular maintenance windows
"""
