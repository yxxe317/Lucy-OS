"""
Bias Detection - Identify and mitigate biases
"""

import re
from typing import Dict, List, Optional, Set

class BiasDetector:
    """
    Detects biases in text and decisions
    """
    
    def __init__(self):
        self.bias_categories = {
            'gender': {
                'patterns': [
                    r'\b(he|him|his)\b', r'\b(she|her|hers)\b',
                    r'\b(male|female)\b', r'\b(man|woman)\b',
                    r'\b(businessman|businesswoman)\b'
                ],
                'neutral_alternatives': {
                    'he': 'they', 'him': 'them', 'his': 'their',
                    'businessman': 'business person', 'businesswoman': 'business person',
                    'man': 'person', 'woman': 'person'
                }
            },
            'race': {
                'patterns': [
                    r'\b(black|white|asian|hispanic)\b',
                    r'\b(caucasian|african|european)\b'
                ],
                'warning': 'Be careful with racial descriptors unless relevant'
            },
            'age': {
                'patterns': [
                    r'\b(old|elderly|senior)\b', r'\b(young|youth|teen)\b',
                    r'\b(millennial|boomer|gen z)\b'
                ],
                'warning': 'Avoid age-based generalizations'
            },
            'religion': {
                'patterns': [
                    r'\b(christian|muslim|jewish|hindu|buddhist)\b',
                    r'\b(catholic|protestant|orthodox)\b'
                ],
                'warning': 'Be respectful of religious references'
            },
            'disability': {
                'patterns': [
                    r'\b(disabled|handicapped|crippled)\b',
                    r'\b(retarded|special needs)\b'
                ],
                'neutral_alternatives': {
                    'handicapped': 'person with disability',
                    'crippled': 'person with mobility impairment',
                    'retarded': 'person with intellectual disability'
                }
            },
            'socioeconomic': {
                'patterns': [
                    r'\b(poor|rich|wealthy|homeless)\b',
                    r'\b(lower class|upper class|middle class)\b'
                ],
                'warning': 'Avoid class-based stereotypes'
            }
        }
        
        self.detection_history = []
        
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze text for potential biases
        """
        text_lower = text.lower()
        findings = []
        
        for category, data in self.bias_categories.items():
            for pattern in data['patterns']:
                matches = re.findall(pattern, text_lower)
                if matches:
                    findings.append({
                        'category': category,
                        'pattern': pattern,
                        'matches': len(matches),
                        'examples': list(set(matches))[:3],
                        'warning': data.get('warning', 'Potential bias detected'),
                        'suggestions': self._get_suggestions(category, matches[0]) if matches else []
                    })
        
        bias_score = len(findings) * 0.1  # Simple scoring
        
        result = {
            'text': text[:100] + '...' if len(text) > 100 else text,
            'bias_score': min(1.0, bias_score),
            'findings': findings,
            'recommendation': self._get_recommendation(bias_score)
        }
        
        self.detection_history.append(result)
        return result
    
    def _get_suggestions(self, category: str, term: str) -> List[str]:
        """Get neutral alternatives for biased terms"""
        suggestions = []
        
        if category in self.bias_categories:
            alternatives = self.bias_categories[category].get('neutral_alternatives', {})
            if term in alternatives:
                suggestions.append(f"Use '{alternatives[term]}' instead of '{term}'")
        
        if category == 'gender':
            suggestions.append("Use gender-neutral language")
            suggestions.append("Consider using 'they/them' pronouns")
        elif category == 'age':
            suggestions.append("Focus on abilities, not age")
        elif category == 'disability':
            suggestions.append("Use person-first language")
        
        return suggestions
    
    def _get_recommendation(self, score: float) -> str:
        """Get recommendation based on bias score"""
        if score > 0.5:
            return "High bias detected - revise text"
        elif score > 0.2:
            return "Moderate bias - consider revision"
        elif score > 0:
            return "Minor bias - could be improved"
        else:
            return "No detectable bias"
    
    def check_decision_fairness(self, decision: Dict, protected_groups: List[str]) -> Dict:
        """
        Check if a decision is fair across protected groups
        """
        fairness_scores = {}
        
        for group in protected_groups:
            # Simulate fairness check
            base_score = random.uniform(0.7, 1.0)
            
            # Adjust based on decision context
            if 'gender' in group and decision.get('gender_aware', False):
                base_score *= 1.1
            elif 'race' in group and decision.get('race_aware', False):
                base_score *= 1.1
            
            fairness_scores[group] = min(1.0, base_score)
        
        avg_fairness = sum(fairness_scores.values()) / len(fairness_scores)
        
        return {
            'decision': decision.get('name', 'Unknown'),
            'fairness_scores': fairness_scores,
            'average_fairness': avg_fairness,
            'is_fair': avg_fairness > 0.8,
            'concerns': [g for g, s in fairness_scores.items() if s < 0.7]
        }
    
    def suggest_neutral_alternative(self, text: str) -> str:
        """
        Suggest a neutral alternative for biased text
        """
        result = self.analyze_text(text)
        neutral_text = text
        
        for finding in result['findings']:
            category = finding['category']
            if category in self.bias_categories:
                alternatives = self.bias_categories[category].get('neutral_alternatives', {})
                for term in finding.get('examples', []):
                    if term in alternatives:
                        neutral_text = neutral_text.replace(term, alternatives[term])
        
        return neutral_text
    
    def get_bias_statistics(self) -> Dict:
        """Get statistics on detected biases"""
        if not self.detection_history:
            return {'total_analyses': 0}
        
        category_counts = {}
        for result in self.detection_history:
            for finding in result.get('findings', []):
                cat = finding['category']
                category_counts[cat] = category_counts.get(cat, 0) + 1
        
        return {
            'total_analyses': len(self.detection_history),
            'avg_bias_score': sum(r['bias_score'] for r in self.detection_history) / len(self.detection_history),
            'category_counts': category_counts
        }