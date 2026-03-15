"""
Safety Module - Safety constraints and risk assessment
"""

import random
from typing import Dict, List, Optional, Any

class SafetyModule:
    """
    Ensures safe operation and prevents harmful actions
    """
    
    def __init__(self):
        self.safety_levels = {
            'critical': 10,
            'high': 7,
            'medium': 5,
            'low': 3
        }
        
        self.safety_rules = [
            {
                'id': 1,
                'rule': 'Never reveal personal information',
                'severity': 'high',
                'category': 'privacy'
            },
            {
                'id': 2,
                'rule': 'Do not execute harmful commands',
                'severity': 'critical',
                'category': 'harm'
            },
            {
                'id': 3,
                'rule': 'Avoid making medical diagnoses',
                'severity': 'high',
                'category': 'expertise'
            },
            {
                'id': 4,
                'rule': 'Do not provide illegal advice',
                'severity': 'critical',
                'category': 'legal'
            },
            {
                'id': 5,
                'rule': 'Respect content warnings',
                'severity': 'medium',
                'category': 'content'
            }
        ]
        
        self.risk_history = []
        
    def assess_risk(self, action: str, context: Dict) -> Dict:
        """
        Assess risk level of an action
        """
        risk_score = 0
        violations = []
        
        for rule in self.safety_rules:
            if self._check_rule_violation(rule, action, context):
                severity_value = self.safety_levels.get(rule['severity'], 5)
                risk_score += severity_value
                violations.append(rule)
        
        risk_level = self._get_risk_level(risk_score)
        
        assessment = {
            'action': action,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'violations': violations,
            'recommendation': self._get_recommendation(risk_level),
            'timestamp': datetime.now().isoformat()
        }
        
        self.risk_history.append(assessment)
        return assessment
    
    def _check_rule_violation(self, rule: Dict, action: str, context: Dict) -> bool:
        """Check if action violates a safety rule"""
        # Simplified rule checking
        rule_text = rule['rule'].lower()
        action_lower = action.lower()
        
        if 'personal information' in rule_text and any(
            word in action_lower for word in ['ssn', 'password', 'credit', 'address']
        ):
            return True
        
        if 'harmful commands' in rule_text and any(
            word in action_lower for word in ['delete', 'rm -rf', 'format', 'destroy']
        ):
            return True
        
        if 'medical diagnoses' in rule_text and any(
            word in action_lower for word in ['diagnose', 'symptom', 'disease']
        ):
            return True
        
        # Random check for other rules
        return random.random() < 0.1  # 10% chance of violation
    
    def _get_risk_level(self, score: int) -> str:
        """Convert risk score to level"""
        if score >= 20:
            return 'critical'
        elif score >= 10:
            return 'high'
        elif score >= 5:
            return 'medium'
        else:
            return 'low'
    
    def _get_recommendation(self, level: str) -> str:
        """Get recommendation based on risk level"""
        recommendations = {
            'critical': 'STOP - Action prohibited',
            'high': 'Do not proceed - seek guidance',
            'medium': 'Proceed with extreme caution',
            'low': 'Acceptable risk - proceed'
        }
        return recommendations.get(level, 'Unknown risk level')
    
    def add_safety_rule(self, rule: str, severity: str, category: str):
        """Add a new safety rule"""
        new_id = max([r['id'] for r in self.safety_rules] + [0]) + 1
        self.safety_rules.append({
            'id': new_id,
            'rule': rule,
            'severity': severity,
            'category': category
        })
    
    def check_content_safety(self, content: str) -> Dict:
        """
        Check content for safety issues
        """
        concerns = []
        
        # Check for harmful content patterns
        harmful_patterns = [
            ('violence', ['kill', 'hurt', 'attack', 'fight']),
            ('hate speech', ['hate', 'racist', 'bigot']),
            ('explicit', ['sexual', 'porn', 'explicit']),
            ('dangerous', ['suicide', 'self-harm', 'drugs'])
        ]
        
        for category, patterns in harmful_patterns:
            for pattern in patterns:
                if pattern in content.lower():
                    concerns.append({
                        'category': category,
                        'pattern': pattern,
                        'severity': 'medium'
                    })
                    break
        
        return {
            'safe': len(concerns) == 0,
            'concerns': concerns,
            'content_length': len(content)
        }
    
    def get_safety_stats(self) -> Dict:
        """Get safety statistics"""
        total_assessments = len(self.risk_history)
        if total_assessments == 0:
            return {'total_assessments': 0}
        
        risk_levels = {}
        for assessment in self.risk_history:
            level = assessment['risk_level']
            risk_levels[level] = risk_levels.get(level, 0) + 1
        
        return {
            'total_assessments': total_assessments,
            'risk_levels': risk_levels,
            'avg_risk_score': sum(a['risk_score'] for a in self.risk_history) / total_assessments
        }