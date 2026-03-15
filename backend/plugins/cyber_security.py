import logging
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger("LucyCyber")

class CyberSecurityFramework:
    def __init__(self):
        self.workspace = Path(__file__).parent.parent / "workspace" / "cyber"
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.threat_database = self._load_threat_definitions()
        logger.info("🛡️ Cybersecurity Framework Initialized (Defensive Mode)")
    
    def _load_threat_definitions(self) -> Dict:
        """Load common threat patterns (MITRE ATT&CK inspired)"""
        return {
            "brute_force": {"pattern": r"failed.*login|authentication.*fail", "severity": "high"},
            "sql_injection": {"pattern": r"union.*select|drop.*table|'--", "severity": "critical"},
            "xss_attempt": {"pattern": r"<script>|javascript:|onerror=", "severity": "high"},
            "path_traversal": {"pattern": r"\.\./|\.\.\\", "severity": "medium"},
            "suspicious_ip": {"pattern": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "severity": "low"}
        }
    
    def analyze_logs(self, log_content: str, log_type: str = "generic") -> Dict:
        """Analyze log files for suspicious patterns (DEFENSIVE)"""
        try:
            findings = []
            lines = log_content.split('\n')
            
            for i, line in enumerate(lines, 1):
                for threat_name, threat_info in self.threat_database.items():
                    if re.search(threat_info["pattern"], line, re.IGNORECASE):
                        findings.append({
                            "line": i,
                            "threat": threat_name,
                            "severity": threat_info["severity"],
                            "content": line[:100],
                            "recommendation": self._get_recommendation(threat_name)
                        })
            
            risk_score = self._calculate_risk_score(findings)
            
            return {
                "success": True,
                "lines_analyzed": len(lines),
                "findings_count": len(findings),
                "risk_score": risk_score,
                "findings": findings,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_recommendation(self, threat: str) -> str:
        """Get defensive recommendation for threat"""
        recommendations = {
            "brute_force": "Implement rate limiting, account lockout policies, and MFA.",
            "sql_injection": "Use parameterized queries, input validation, and WAF.",
            "xss_attempt": "Implement Content Security Policy, sanitize outputs, encode inputs.",
            "path_traversal": "Validate file paths, use chroot jails, restrict file access.",
            "suspicious_ip": "Review firewall logs, consider IP reputation filtering."
        }
        return recommendations.get(threat, "Review security logs and consult security team.")
    
    def _calculate_risk_score(self, findings: List) -> int:
        """Calculate overall risk score (0-100)"""
        if not findings:
            return 0
        
        severity_weights = {"low": 1, "medium": 5, "high": 10, "critical": 20}
        total_weight = sum(severity_weights.get(f["severity"], 1) for f in findings)
        
        # Normalize to 0-100
        score = min(100, total_weight * 2)
        return score
    
    def assess_password_strength(self, password: str) -> Dict:
        """Evaluate password strength (DEFENSIVE)"""
        score = 0
        feedback = []
        
        if len(password) >= 12:
            score += 30
        else:
            feedback.append("Password should be at least 12 characters")
        
        if re.search(r"[A-Z]", password):
            score += 20
        else:
            feedback.append("Add uppercase letters")
        
        if re.search(r"[a-z]", password):
            score += 20
        else:
            feedback.append("Add lowercase letters")
        
        if re.search(r"\d", password):
            score += 15
        else:
            feedback.append("Add numbers")
        
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 15
        else:
            feedback.append("Add special characters")
        
        strength = "Weak" if score < 50 else "Medium" if score < 80 else "Strong"
        
        return {
            "success": True,
            "strength": strength,
            "score": score,
            "feedback": feedback
        }
    
    def generate_incident_playbook(self, incident_type: str) -> Dict:
        """Generate incident response playbook (DEFENSIVE)"""
        playbooks = {
            "malware_detection": {
                "steps": [
                    "1. Isolate affected system from network",
                    "2. Document all observations and timestamps",
                    "3. Capture memory dump for forensics",
                    "4. Identify malware type and IOCs",
                    "5. Eradicate malware using approved tools",
                    "6. Restore from clean backup",
                    "7. Patch vulnerability that allowed infection",
                    "8. Conduct post-incident review"
                ],
                "tools": ["Wireshark", "Volatility", "YARA", "SIEM"]
            },
            "phishing_attack": {
                "steps": [
                    "1. Do not click links or download attachments",
                    "2. Report to security team immediately",
                    "3. Block sender domain in email gateway",
                    "4. Scan affected systems for compromise",
                    "5. Reset credentials if information was entered",
                    "6. Send awareness notification to users",
                    "7. Update email filtering rules"
                ],
                "tools": ["Email Gateway", "Sandbox", "Awareness Platform"]
            },
            "data_breach": {
                "steps": [
                    "1. Confirm breach scope and data types",
                    "2. Contain breach (revoke access, close ports)",
                    "3. Notify legal and compliance teams",
                    "4. Prepare customer notification if required",
                    "5. Engage forensic investigators",
                    "6. Implement additional monitoring",
                    "7. Review and update security controls"
                ],
                "tools": ["DLP", "SIEM", "Forensics Suite", "Legal Counsel"]
            }
        }
        
        return {
            "success": True,
            "incident_type": incident_type,
            "playbook": playbooks.get(incident_type, {"steps": ["Consult security team"], "tools": []})
        }
    
    def threat_modeling_assistant(self, application_description: str) -> Dict:
        """Help model threats for an application (DEFENSIVE)"""
        # Simple STRIDE-based analysis
        threats = []
        
        if "login" in application_description.lower():
            threats.append({
                "category": "Spoofing",
                "risk": "Authentication bypass",
                "mitigation": "Implement MFA, rate limiting, secure session management"
            })
        
        if "database" in application_description.lower():
            threats.append({
                "category": "Tampering",
                "risk": "SQL injection or data manipulation",
                "mitigation": "Use ORM, parameterized queries, input validation"
            })
        
        if "api" in application_description.lower():
            threats.append({
                "category": "Information Disclosure",
                "risk": "Sensitive data exposure via API",
                "mitigation": "Implement authentication, rate limiting, encrypt responses"
            })
        
        return {
            "success": True,
            "application": application_description[:100],
            "identified_threats": threats,
            "framework": "STRIDE"
        }

cyber_security = CyberSecurityFramework()