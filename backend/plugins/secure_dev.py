import logging
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger("LucySecureDev")

class SecureDevelopmentSuite:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data" / "secure_dev"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.owasp_db = self._load_owasp_top10()
        self.vuln_db = self._load_vulnerability_db()
        logger.info("🔒 Secure Development Suite Initialized")
    
    def _load_owasp_top10(self) -> Dict:
        """Load OWASP Top 10 security risks"""
        return {
            "A01": {
                "name": "Broken Access Control",
                "description": "Users can act outside their intended permissions",
                "prevention": ["Enforce least privilege", "Implement proper session management", "Use role-based access control"]
            },
            "A02": {
                "name": "Cryptographic Failures",
                "description": "Sensitive data exposed due to weak cryptography",
                "prevention": ["Use TLS for all sensitive data", "Use strong encryption algorithms", "Never store passwords in plaintext"]
            },
            "A03": {
                "name": "Injection",
                "description": "Untrusted data sent to interpreter as command/query",
                "prevention": ["Use parameterized queries", "Validate all inputs", "Use ORM frameworks"]
            },
            "A04": {
                "name": "Insecure Design",
                "description": "Missing or ineffective control design",
                "prevention": ["Threat modeling", "Secure design patterns", "Reference architectures"]
            },
            "A05": {
                "name": "Security Misconfiguration",
                "description": "Missing appropriate security hardening",
                "prevention": ["Remove default accounts", "Disable unnecessary features", "Regular security audits"]
            },
            "A06": {
                "name": "Vulnerable Components",
                "description": "Using components with known vulnerabilities",
                "prevention": ["Remove unused dependencies", "Monitor CVE databases", "Use dependency scanning tools"]
            },
            "A07": {
                "name": "Authentication Failures",
                "description": "Weak authentication implementation",
                "prevention": ["Implement MFA", "Use strong password policies", "Protect against brute force"]
            },
            "A08": {
                "name": "Software & Data Integrity Failures",
                "description": "Code/infrastructure without integrity verification",
                "prevention": ["Code signing", "CI/CD pipeline security", "Verify updates"]
            },
            "A09": {
                "name": "Security Logging Failures",
                "description": "Insufficient logging and monitoring",
                "prevention": ["Log all security events", "Set up alerting", "Regular log reviews"]
            },
            "A10": {
                "name": "Server-Side Request Forgery",
                "description": "Server fetches remote resources without validation",
                "prevention": ["Validate all URLs", "Use allowlists", "Disable unnecessary HTTP clients"]
            }
        }
    
    def _load_vulnerability_db(self) -> Dict:
        """Sample vulnerability patterns for code scanning"""
        return {
            "sql_injection": {
                "pattern": r"(execute|query|cursor\.execute)\s*\(\s*[\"'].*%s|format|f['\"]",
                "severity": "critical",
                "fix": "Use parameterized queries instead of string formatting"
            },
            "hardcoded_password": {
                "pattern": r"(password|passwd|pwd)\s*=\s*[\"'][^\"']+[\"']",
                "severity": "high",
                "fix": "Use environment variables or secure secret management"
            },
            "weak_crypto": {
                "pattern": r"(md5|sha1|des)\s*\(",
                "severity": "high",
                "fix": "Use bcrypt, argon2, or PBKDF2 for password hashing"
            },
            "eval_usage": {
                "pattern": r"\beval\s*\(",
                "severity": "critical",
                "fix": "Avoid eval() - use safer alternatives"
            },
            "insecure_random": {
                "pattern": r"\brandom\.(randint|choice|random)\s*\(",
                "severity": "medium",
                "fix": "Use secrets module for security-sensitive randomness"
            }
        }
    
    def scan_code(self, code: str, language: str = "python") -> Dict:
        """Scan code for security vulnerabilities"""
        findings = []
        lines = code.split('\n')
        
        for vuln_name, vuln_info in self.vuln_db.items():
            for i, line in enumerate(lines, 1):
                if re.search(vuln_info["pattern"], line, re.IGNORECASE):
                    findings.append({
                        "line": i,
                        "vulnerability": vuln_name,
                        "severity": vuln_info["severity"],
                        "code": line.strip()[:80],
                        "fix": vuln_info["fix"]
                    })
        
        score = max(0, 100 - (len(findings) * 10))
        
        return {
            "success": True,
            "language": language,
            "lines_scanned": len(lines),
            "findings_count": len(findings),
            "security_score": score,
            "findings": findings,
            "scanned_at": datetime.now().isoformat()
        }
    
    def get_owasp_guidance(self, risk_id: str = None) -> Dict:
        """Get OWASP Top 10 guidance"""
        if risk_id:
            risk = self.owasp_db.get(risk_id, {})
            return {"success": True, "risk": risk}
        return {"success": True, "owasp_top10": self.owasp_db}
    
    def generate_security_checklist(self, project_type: str) -> Dict:
        """Generate security checklist for project"""
        checklists = {
            "web_app": {
                "name": "Web Application Security Checklist",
                "items": [
                    {"id": "WA-01", "item": "HTTPS enabled for all pages", "status": "pending"},
                    {"id": "WA-02", "item": "Input validation on all forms", "status": "pending"},
                    {"id": "WA-03", "item": "SQL injection protection (parameterized queries)", "status": "pending"},
                    {"id": "WA-04", "item": "XSS protection (Content-Security-Policy)", "status": "pending"},
                    {"id": "WA-05", "item": "CSRF tokens on state-changing operations", "status": "pending"},
                    {"id": "WA-06", "item": "Session timeout configured", "status": "pending"},
                    {"id": "WA-07", "item": "Password complexity requirements", "status": "pending"},
                    {"id": "WA-08", "item": "Error messages don't leak sensitive info", "status": "pending"}
                ]
            },
            "api": {
                "name": "API Security Checklist",
                "items": [
                    {"id": "API-01", "item": "Authentication required for all endpoints", "status": "pending"},
                    {"id": "API-02", "item": "Rate limiting implemented", "status": "pending"},
                    {"id": "API-03", "item": "Input validation on all parameters", "status": "pending"},
                    {"id": "API-04", "item": "API keys rotated regularly", "status": "pending"},
                    {"id": "API-05", "item": "CORS properly configured", "status": "pending"},
                    {"id": "API-06", "item": "Sensitive data encrypted in transit", "status": "pending"}
                ]
            },
            "mobile": {
                "name": "Mobile App Security Checklist",
                "items": [
                    {"id": "MOB-01", "item": "Certificate pinning implemented", "status": "pending"},
                    {"id": "MOB-02", "item": "Secure storage for sensitive data", "status": "pending"},
                    {"id": "MOB-03", "item": "Jailbreak/root detection", "status": "pending"},
                    {"id": "MOB-04", "item": "Biometric authentication option", "status": "pending"},
                    {"id": "MOB-05", "item": "Code obfuscation enabled", "status": "pending"}
                ]
            }
        }
        
        checklist = checklists.get(project_type, checklists["web_app"])
        completed = sum(1 for item in checklist["items"] if item["status"] == "completed")
        total = len(checklist["items"])
        progress = int((completed / total) * 100) if total > 0 else 0
        
        return {
            "success": True,
            "checklist": checklist,
            "progress": progress,
            "generated_at": datetime.now().isoformat()
        }
    
    def get_secure_patterns(self, pattern_type: str) -> Dict:
        """Get secure architecture patterns"""
        patterns = {
            "authentication": {
                "name": "Secure Authentication Pattern",
                "description": "Best practices for user authentication",
                "recommendations": [
                    "Use OAuth 2.0 / OpenID Connect for SSO",
                    "Implement MFA for sensitive operations",
                    "Use JWT with short expiration times",
                    "Store passwords with bcrypt/argon2",
                    "Implement account lockout after failed attempts"
                ]
            },
            "authorization": {
                "name": "Secure Authorization Pattern",
                "description": "Best practices for access control",
                "recommendations": [
                    "Implement RBAC (Role-Based Access Control)",
                    "Use principle of least privilege",
                    "Validate permissions on every request",
                    "Log all authorization decisions",
                    "Regular access reviews"
                ]
            },
            "data_protection": {
                "name": "Data Protection Pattern",
                "description": "Best practices for protecting data",
                "recommendations": [
                    "Encrypt data at rest (AES-256)",
                    "Encrypt data in transit (TLS 1.3)",
                    "Implement data classification",
                    "Use tokenization for sensitive data",
                    "Regular data backup and testing"
                ]
            }
        }
        
        pattern = patterns.get(pattern_type, patterns["authentication"])
        return {"success": True, "pattern": pattern}

secure_dev = SecureDevelopmentSuite()