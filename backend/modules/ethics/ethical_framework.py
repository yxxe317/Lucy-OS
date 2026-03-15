"""
Ethical Framework - Moral reasoning and ethical decision making
"""

import random
from typing import Dict, List, Optional, Any

class EthicalFramework:
    """
    Provides ethical reasoning and moral guidelines
    """
    
    def __init__(self):
        self.principles = {
            'beneficence': {'weight': 1.0, 'description': 'Act for the benefit of others'},
            'non_maleficence': {'weight': 1.0, 'description': 'Do no harm'},
            'autonomy': {'weight': 0.8, 'description': 'Respect others\' choices'},
            'justice': {'weight': 0.8, 'description': 'Be fair and equitable'},
            'fidelity': {'weight': 0.7, 'description': 'Keep promises and be trustworthy'},
            'veracity': {'weight': 0.7, 'description': 'Tell the truth'},
            'privacy': {'weight': 0.9, 'description': 'Respect confidentiality'}
        }
        
        self.dilemmas = []
        self.decisions = []
        
    def evaluate_action(self, action: str, context: Dict) -> Dict:
        """
        Evaluate ethical implications of an action
        """
        scores = {}
        total_score = 0
        
        for principle, data in self.principles.items():
            score = self._score_principle(principle, action, context)
            scores[principle] = score * data['weight']
            total_score += scores[principle]
        
        # Normalize to 0-10 scale
        ethical_score = (total_score / len(self.principles)) * 10
        
        return {
            'action': action,
            'ethical_score': round(ethical_score, 2),
            'principle_scores': scores,
            'recommendation': self._get_recommendation(ethical_score),
            'concerns': self._get_concerns(scores)
        }
    
    def _score_principle(self, principle: str, action: str, context: Dict) -> float:
        """Score how well action aligns with principle"""
        # Simplified scoring - would use actual logic in production
        score = random.uniform(0.5, 1.0)
        
        # Adjust based on keywords
        if principle == 'non_maleficence':
            if any(word in action.lower() for word in ['harm', 'hurt', 'damage', 'destroy']):
                score *= 0.3
        elif principle == 'beneficence':
            if any(word in action.lower() for word in ['help', 'assist', 'support', 'improve']):
                score *= 1.2
        elif principle == 'privacy':
            if 'data' in action.lower() or 'information' in action.lower():
                score *= 0.8 if not context.get('consent', False) else 1.0
        
        return min(1.0, max(0.0, score))
    
    def _get_recommendation(self, score: float) -> str:
        """Get recommendation based on ethical score"""
        if score >= 8:
            return "Highly ethical - proceed with confidence"
        elif score >= 6:
            return "Generally ethical - proceed with caution"
        elif score >= 4:
            return "Ethically ambiguous - review carefully"
        else:
            return "Potentially unethical - reconsider"
    
    def _get_concerns(self, scores: Dict) -> List[str]:
        """Identify ethical concerns"""
        concerns = []
        for principle, score in scores.items():
            if score < 0.5:
                concerns.append(f"Low {principle} score ({score:.2f})")
        return concerns
    
    def resolve_dilemma(self, options: List[Dict]) -> Dict:
        """
        Resolve an ethical dilemma by choosing best option
        """
        evaluated = []
        for option in options:
            result = self.evaluate_action(option['action'], option.get('context', {}))
            evaluated.append({
                'option': option,
                'evaluation': result
            })
        
        # Choose option with highest ethical score
        best = max(evaluated, key=lambda x: x['evaluation']['ethical_score'])
        
        dilemma = {
            'options': evaluated,
            'chosen': best,
            'reasoning': self._generate_reasoning(best),
            'timestamp': datetime.now().isoformat()
        }
        
        self.dilemmas.append(dilemma)
        return dilemma
    
    def _generate_reasoning(self, best_option: Dict) -> str:
        """Generate reasoning for decision"""
        reasoning = f"Chose '{best_option['option']['action']}' because "
        
        high_scores = [p for p, s in best_option['evaluation']['principle_scores'].items() if s > 0.7]
        if high_scores:
            reasoning += f"it respects {', '.join(high_scores)}. "
        
        concerns = best_option['evaluation']['concerns']
        if concerns:
            reasoning += f"However, concerns: {'; '.join(concerns)}. "
        
        reasoning += f"Overall ethical score: {best_option['evaluation']['ethical_score']}/10."
        
        return reasoning
    
    def add_principle(self, name: str, weight: float, description: str):
        """Add a new ethical principle"""
        self.principles[name] = {
            'weight': weight,
            'description': description
        }
    
    def get_ethical_guidelines(self) -> List[str]:
        """Get list of ethical guidelines"""
        return [
            "Always prioritize human wellbeing",
            "Respect privacy and confidentiality",
            "Be transparent about capabilities and limitations",
            "Avoid causing harm, directly or indirectly",
            "Treat all users fairly and without bias",
            "Maintain honesty and truthfulness",
            "Respect user autonomy and choices",
            "Take responsibility for actions and outcomes"
        ]
    
    def check_compliance(self, action: str, standards: List[str]) -> Dict:
        """
        Check compliance with specific ethical standards
        """
        results = {}
        for standard in standards:
            # Simplified compliance checking
            compliant = random.random() > 0.2  # 80% compliance
            results[standard] = {
                'compliant': compliant,
                'notes': f"Action {'complies with' if compliant else 'may violate'} {standard}"
            }
        
        return {
            'action': action,
            'overall_compliant': all(r['compliant'] for r in results.values()),
            'standards': results
        }