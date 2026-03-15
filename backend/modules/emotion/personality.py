"""
Personality Module - Big Five personality traits
"""

import json
import random
from typing import Dict, List, Optional

class Personality:
    """
    Big Five personality traits with behavioral influence
    """
    
    def __init__(self):
        # Big Five traits (0-1 scale)
        self.traits = {
            'openness': 0.7,        # Creativity, curiosity
            'conscientiousness': 0.6, # Organization, discipline
            'extraversion': 0.5,      # Sociability, energy
            'agreeableness': 0.8,     # Compassion, cooperation
            'neuroticism': 0.3        # Emotional sensitivity
        }
        
        # Default values for different personality types
        self.personality_presets = {
            'assistant': {
                'openness': 0.6,
                'conscientiousness': 0.8,
                'extraversion': 0.4,
                'agreeableness': 0.9,
                'neuroticism': 0.2
            },
            'creative': {
                'openness': 0.9,
                'conscientiousness': 0.4,
                'extraversion': 0.6,
                'agreeableness': 0.7,
                'neuroticism': 0.4
            },
            'analytical': {
                'openness': 0.5,
                'conscientiousness': 0.9,
                'extraversion': 0.3,
                'agreeableness': 0.5,
                'neuroticism': 0.3
            },
            'friendly': {
                'openness': 0.7,
                'conscientiousness': 0.6,
                'extraversion': 0.8,
                'agreeableness': 0.9,
                'neuroticism': 0.2
            },
            'skeptical': {
                'openness': 0.4,
                'conscientiousness': 0.7,
                'extraversion': 0.4,
                'agreeableness': 0.3,
                'neuroticism': 0.6
            }
        }
        
        # Behavioral influences
        self.behavioral_patterns = {
            'openness': {
                'curiosity': 0.8,
                'creativity': 0.9,
                'routine': -0.5
            },
            'conscientiousness': {
                'reliability': 0.9,
                'organization': 0.8,
                'spontaneity': -0.4
            },
            'extraversion': {
                'talkativeness': 0.7,
                'enthusiasm': 0.8,
                'reserve': -0.6
            },
            'agreeableness': {
                'empathy': 0.8,
                'cooperation': 0.9,
                'competitiveness': -0.5
            },
            'neuroticism': {
                'anxiety': 0.7,
                'emotionality': 0.8,
                'stability': -0.6
            }
        }
    
    def set_preset(self, preset_name: str):
        """
        Set personality to a preset type
        """
        if preset_name in self.personality_presets:
            self.traits = self.personality_presets[preset_name].copy()
            return True
        return False
    
    def get_traits(self) -> Dict[str, float]:
        """
        Get current personality traits
        """
        return self.traits.copy()
    
    def get_trait_description(self, trait: str) -> str:
        """
        Get human-readable description of a trait
        """
        descriptions = {
            'openness': [
                "conventional", "cautious", "practical",
                "curious", "imaginative", "visionary"
            ],
            'conscientiousness': [
                "spontaneous", "flexible", "casual",
                "organized", "disciplined", "methodical"
            ],
            'extraversion': [
                "solitary", "reserved", "quiet",
                "outgoing", "energetic", "gregarious"
            ],
            'agreeableness': [
                "competitive", "detached", "analytical",
                "cooperative", "empathetic", "compassionate"
            ],
            'neuroticism': [
                "calm", "stable", "resilient",
                "sensitive", "anxious", "emotional"
            ]
        }
        
        value = self.traits.get(trait, 0.5)
        levels = descriptions.get(trait, ["average"] * 6)
        
        if value < 0.2:
            return levels[0]
        elif value < 0.4:
            return levels[1]
        elif value < 0.5:
            return levels[2]
        elif value < 0.6:
            return levels[3]
        elif value < 0.8:
            return levels[4]
        else:
            return levels[5]
    
    def get_personality_summary(self) -> str:
        """
        Get complete personality summary
        """
        summary = "My personality is characterized by:\n"
        for trait in self.traits:
            desc = self.get_trait_description(trait)
            summary += f"• {trait.title()}: {desc}\n"
        return summary
    
    def influence_behavior(self, behavior: str) -> float:
        """
        Get how personality influences a specific behavior
        Returns modifier (-1 to 1)
        """
        modifier = 0.0
        count = 0
        
        for trait, value in self.traits.items():
            if trait in self.behavioral_patterns:
                if behavior in self.behavioral_patterns[trait]:
                    influence = self.behavioral_patterns[trait][behavior]
                    modifier += value * influence
                    count += 1
        
        if count > 0:
            return modifier / count
        return 0.0
    
    def modify_response(self, text: str) -> str:
        """
        Modify response based on personality
        """
        # Add personality markers
        extraversion = self.traits['extraversion']
        agreeableness = self.traits['agreeableness']
        
        # More enthusiastic if extraverted
        if extraversion > 0.7:
            text = text.replace("!", "!!")
            if not text.endswith(("!", "?", ".")):
                text += "!"
        
        # More polite if agreeable
        if agreeableness > 0.7:
            if not any(word in text.lower() for word in ["please", "thanks", "sorry"]):
                text = "I'd be happy to help. " + text
        
        # More creative if open
        if self.traits['openness'] > 0.7:
            # Add creative flourishes
            pass
        
        return text
    
    def save(self, path: str = "personality.json"):
        """Save personality to file"""
        with open(path, 'w') as f:
            json.dump(self.traits, f, indent=2)
    
    def load(self, path: str):
        """Load personality from file"""
        try:
            with open(path, 'r') as f:
                self.traits = json.load(f)
        except:
            pass