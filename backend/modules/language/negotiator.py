"""
Negotiation Engine - Persuasion and negotiation strategies
"""

import random
from typing import Dict, List, Optional, Tuple

class Negotiator:
    """
    Negotiation and persuasion strategies
    """
    
    def __init__(self):
        self.strategies = {
            'reciprocity': {
                'name': 'Reciprocity',
                'phrases': [
                    "I've been very flexible with you, so I hope you can meet me halfway.",
                    "Given everything I've offered, wouldn't you agree this is fair?",
                    "I've made several concessions already. Can you match my flexibility?"
                ],
                'effectiveness': 0.7
            },
            'scarcity': {
                'name': 'Scarcity',
                'phrases': [
                    "This offer won't last forever.",
                    "There are only a few opportunities like this left.",
                    "If we don't decide now, we might lose this chance."
                ],
                'effectiveness': 0.6
            },
            'authority': {
                'name': 'Authority',
                'phrases': [
                    "Experts in this field recommend this approach.",
                    "This is the standard practice in the industry.",
                    "Studies have shown this is the most effective solution."
                ],
                'effectiveness': 0.65
            },
            'consistency': {
                'name': 'Consistency',
                'phrases': [
                    "You mentioned earlier that fairness was important to you.",
                    "This aligns with what you said you wanted.",
                    "Given your previous statements, this makes perfect sense."
                ],
                'effectiveness': 0.75
            },
            'liking': {
                'name': 'Liking',
                'phrases': [
                    "We've built a good relationship, haven't we?",
                    "I really appreciate working with someone who understands.",
                    "People like us should be able to reach an agreement."
                ],
                'effectiveness': 0.55
            },
            'consensus': {
                'name': 'Consensus',
                'phrases': [
                    "Most people in your situation choose this option.",
                    "This is what others have found works best.",
                    "The majority of our clients prefer this arrangement."
                ],
                'effectiveness': 0.6
            }
        }
        
        self.concession_patterns = [
            "I can offer {concession}, but I'll need {request} in return.",
            "If you agree to {request}, I'm willing to {concession}.",
            "How about this: I'll {concession} if you'll {request}.",
            "To show good faith, I'll {concession}. Would you consider {request}?"
        ]
        
        self.closing_phrases = [
            "Shall we shake on it?",
            "Do we have a deal?",
            "Can we agree on these terms?",
            "Is this acceptable to you?",
            "I think we've found common ground."
        ]
    
    def negotiate(self, issue: str, position: Dict, 
                   opponent_position: Dict) -> Dict:
        """
        Conduct negotiation simulation
        """
        negotiation = {
            'issue': issue,
            'initial_position': position,
            'counter_offers': [],
            'concessions_made': [],
            'final_agreement': None,
            'success': False
        }
        
        current_position = position.copy()
        rounds = 0
        
        while rounds < 5:  # Max 5 rounds
            rounds += 1
            
            # Choose strategy
            strategy = self._choose_strategy()
            response = self._generate_response(issue, current_position, strategy)
            
            negotiation['counter_offers'].append({
                'round': rounds,
                'strategy': strategy['name'],
                'response': response
            })
            
            # Simulate opponent response
            agreement_chance = self._calculate_agreement_chance(
                current_position, opponent_position, rounds
            )
            
            if random.random() < agreement_chance:
                negotiation['final_agreement'] = current_position
                negotiation['success'] = True
                break
            
            # Make concession
            if rounds < 5:
                concession = self._make_concession(current_position, rounds)
                if concession:
                    current_position = concession
                    negotiation['concessions_made'].append({
                        'round': rounds,
                        'concession': concession
                    })
        
        return negotiation
    
    def _choose_strategy(self) -> Dict:
        """Choose negotiation strategy"""
        strategies = list(self.strategies.values())
        weights = [s['effectiveness'] for s in strategies]
        return random.choices(strategies, weights=weights)[0]
    
    def _generate_response(self, issue: str, position: Dict, strategy: Dict) -> str:
        """Generate negotiation response"""
        phrase = random.choice(strategy['phrases'])
        
        # Customize with issue
        if '{issue}' in phrase:
            phrase = phrase.replace('{issue}', issue)
        
        return phrase
    
    def _calculate_agreement_chance(self, position: Dict, 
                                      opponent: Dict, rounds: int) -> float:
        """Calculate chance of agreement"""
        # Simple similarity measure
        common_keys = set(position.keys()) & set(opponent.keys())
        if not common_keys:
            return 0.1
        
        similarity = 0
        for key in common_keys:
            if position.get(key) == opponent.get(key):
                similarity += 1
        
        similarity_score = similarity / len(common_keys)
        
        # Increase chance with each round
        round_bonus = rounds * 0.05
        
        return min(0.9, similarity_score + round_bonus)
    
    def _make_concession(self, position: Dict, round_num: int) -> Optional[Dict]:
        """Make a concession"""
        if not position:
            return None
        
        new_position = position.copy()
        
        # Concede on one random item
        keys = list(new_position.keys())
        if keys:
            key = random.choice(keys)
            if isinstance(new_position[key], (int, float)):
                # Numerical concession
                new_position[key] *= (1 - 0.1 * round_num)
            else:
                # Non-numerical concession - just note it
                new_position[key] = f"adjusted_{new_position[key]}"
        
        return new_position
    
    def propose_compromise(self, position1: Dict, position2: Dict) -> Dict:
        """
        Propose a compromise between two positions
        """
        compromise = {}
        
        all_keys = set(position1.keys()) | set(position2.keys())
        
        for key in all_keys:
            val1 = position1.get(key)
            val2 = position2.get(key)
            
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                # Average numerical values
                compromise[key] = (val1 + val2) / 2
            elif val1 == val2:
                compromise[key] = val1
            elif val1 is not None:
                compromise[key] = val1
            else:
                compromise[key] = val2
        
        return compromise
    
    def get_closing_statement(self) -> str:
        """Get a closing phrase"""
        return random.choice(self.closing_phrases)