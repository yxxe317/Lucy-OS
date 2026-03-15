"""
Privacy Module - Privacy protection and data handling
"""

import re
import hashlib
from typing import Dict, List, Optional, Any

class PrivacyModule:
    """
    Ensures privacy protection and proper data handling
    """
    
    def __init__(self):
        self.privacy_levels = {
            'public': 1,
            'internal': 2,
            'confidential': 3,
            'restricted': 4,
            'secret': 5
        }
        
        self.sensitive_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b(?:\d[ -]*?){13,16}\b',
            'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            'password': r'(?i)(password|passwd|pwd)\s*[:=]\s*\S+',
            'api_key': r'(?i)(api[_-]?key|token|secret)\s*[:=]\s*\S+'
        }
        
        self.data_retention = {
            'public': 365,  # days
            'internal': 90,
            'confidential': 30,
            'restricted': 7,
            'secret': 1
        }
        
        self.access_log = []
        self.consent_records = {}
        
    def classify_data(self, data: str, context: Dict = None) -> Dict:
        """
        Classify data sensitivity level
        """
        sensitivity_score = 0
        findings = []
        
        for data_type, pattern in self.sensitive_patterns.items():
            matches = re.findall(pattern, data)
            if matches:
                sensitivity_score += len(matches)
                findings.append({
                    'type': data_type,
                    'count': len(matches),
                    'examples': matches[:2]
                })
        
        # Determine privacy level
        if sensitivity_score > 10:
            level = 'restricted'
        elif sensitivity_score > 5:
            level = 'confidential'
        elif sensitivity_score > 0:
            level = 'internal'
        else:
            level = 'public'
        
        return {
            'privacy_level': level,
            'sensitivity_score': sensitivity_score,
            'findings': findings,
            'recommendation': self._get_handling_recommendation(level)
        }
    
    def _get_handling_recommendation(self, level: str) -> str:
        """Get handling recommendation based on privacy level"""
        recommendations = {
            'public': 'Can be freely shared',
            'internal': 'Internal use only - do not share externally',
            'confidential': 'Restricted access - encrypt in transit',
            'restricted': 'Highly sensitive - encrypt at rest and in transit',
            'secret': 'Maximum security - limited access, audit required'
        }
        return recommendations.get(level, 'Unknown level')
    
    def anonymize_data(self, data: str, level: str = 'medium') -> str:
        """
        Anonymize sensitive data
        """
        anonymized = data
        
        for data_type, pattern in self.sensitive_patterns.items():
            matches = re.findall(pattern, anonymized)
            for match in matches:
                if data_type in ['email', 'phone', 'ssn', 'credit_card']:
                    # Replace with hash
                    hashed = hashlib.sha256(match.encode()).hexdigest()[:8]
                    anonymized = anonymized.replace(match, f"[{data_type}:{hashed}]")
                elif level == 'high':
                    # Full redaction
                    anonymized = anonymized.replace(match, "[REDACTED]")
                else:
                    # Partial masking
                    if data_type == 'email':
                        parts = match.split('@')
                        masked = parts[0][:2] + '***@' + parts[1]
                        anonymized = anonymized.replace(match, masked)
                    elif data_type == 'phone':
                        masked = '***-***-' + match[-4:]
                        anonymized = anonymized.replace(match, masked)
        
        return anonymized
    
    def check_consent(self, user_id: str, purpose: str) -> bool:
        """
        Check if user has given consent for purpose
        """
        if user_id not in self.consent_records:
            return False
        
        consents = self.consent_records[user_id]
        return consents.get(purpose, False)
    
    def record_consent(self, user_id: str, purpose: str, granted: bool):
        """
        Record user consent
        """
        if user_id not in self.consent_records:
            self.consent_records[user_id] = {}
        
        self.consent_records[user_id][purpose] = granted
        self._log_access('consent', user_id, purpose, granted)
    
    def log_access(self, user_id: str, data_type: str, purpose: str):
        """
        Log data access for audit
        """
        self._log_access('access', user_id, data_type, purpose)
    
    def _log_access(self, action: str, user_id: str, target: str, detail: Any):
        """Internal logging method"""
        from datetime import datetime
        self.access_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'user_id': user_id,
            'target': target,
            'detail': detail
        })
    
    def get_audit_log(self, user_id: str = None, limit: int = 100) -> List[Dict]:
        """
        Get audit log entries
        """
        if user_id:
            filtered = [log for log in self.access_log if log['user_id'] == user_id]
            return filtered[-limit:]
        return self.access_log[-limit:]
    
    def should_delete_data(self, data_type: str, created_date: datetime) -> bool:
        """
        Check if data should be deleted based on retention policy
        """
        from datetime import datetime, timedelta
        
        retention_days = self.data_retention.get(data_type, 30)
        cutoff = datetime.now() - timedelta(days=retention_days)
        
        return created_date < cutoff
    
    def get_privacy_policy(self) -> str:
        """
        Get privacy policy summary
        """
        return """
        PRIVACY POLICY SUMMARY:
        
        1. Data Collection: We collect only necessary data
        2. Data Usage: Data used only for stated purposes
        3. Data Sharing: No sharing without consent
        4. Data Retention: Data deleted after retention period
        5. User Rights: Access, correct, delete your data
        6. Security: Encryption and access controls
        7. Consent: Explicit consent required for sensitive data
        """