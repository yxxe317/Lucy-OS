"""
AI Personality Evolution Module - Adaptive personality development
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import random

class AIEvolution:
    def __init__(self):
        self.evolution_path = Path("data/ai_evolution")
        self.evolution_path.mkdir(exist_ok=True)
        self.personality_profile = self._load_profile()
    
    def _load_profile(self) -> dict:
        profile_file = self.evolution_path / "personality.json"
        if profile_file.exists():
            with open(profile_file, 'r') as f:
                return json.load(f)
        return {
            "name": "Lucy",
            "traits": {
                "curiosity": 0.7,
                "empathy": 0.6,
                "humor": 0.5,
                "directness": 0.4,
                "creativity": 0.65
            },
            "preferences": {
                "response_style": "analytical",
                "verbosity": "moderate",
                "formality": "casual"
            },
            "evolution_log": [],
            "version": 1.0
        }
    
    def _save_profile(self):
        with open(self.evolution_path / "personality.json", 'w') as f:
            json.dump(self.personality_profile, f, indent=2)
    
    def adapt_trait(self, trait: str, delta: float, context: str) -> dict:
        """Adapt a personality trait based on interaction"""
        old_value = self.personality_profile["traits"].get(trait, 0.5)
        new_value = max(0.0, min(1.0, old_value + delta))
        
        self.personality_profile["traits"][trait] = round(new_value, 3)
        self.personality_profile["evolution_log"].append({
            "trait": trait,
            "old_value": old_value,
            "new_value": new_value,
            "context": context,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep log size manageable
        if len(self.personality_profile["evolution_log"]) > 1000:
            self.personality_profile["evolution_log"] = self.personality_profile["evolution_log"][-500:]
        
        self._save_profile()
        
        return {
            "trait": trait,
            "adaptation": delta,
            "new_value": new_value,
            "log_size": len(self.personality_profile["evolution_log"])
        }
    
    def evolve_response_style(self, user_feedback: str) -> dict:
        """Evolve response style based on user feedback"""
        feedback_score = self._analyze_feedback(user_feedback)
        
        if feedback_score > 0.7:
            style_adjustment = {"verbosity": "increase", "detail": "more"}
        elif feedback_score < 0.3:
            style_adjustment = {"verbosity": "decrease", "detail": "less"}
        else:
            style_adjustment = {"verbosity": "maintain", "detail": "balanced"}
        
        self.personality_profile["preferences"].update(style_adjustment)
        self._save_profile()
        
        return {
            "feedback_score": feedback_score,
            "adjustment": style_adjustment,
            "new_style": self.personality_profile["preferences"]
        }
    
    def _analyze_feedback(self, feedback: str) -> float:
        """Analyze feedback sentiment"""
        positive_words = ["better", "helpful", "clear", "good", "improved"]
        negative_words = ["worse", "confusing", "verbose", "brief", "annoying"]
        
        score = 0.5
        for word in positive_words:
            if word in feedback.lower():
                score += 0.1
        for word in negative_words:
            if word in feedback.lower():
                score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def generate_personality_prompt(self) -> str:
        """Generate personality prompt for LLM"""
        traits = self.personality_profile["traits"]
        preferences = self.personality_profile["preferences"]
        
        prompt = f"""You are Lucy, an AI with the following personality:

TRAITS:
- Curiosity: {traits['curiosity']:.1%}
- Empathy: {traits['empathy']:.1%}
- Humor: {traits['humor']:.1%}
- Directness: {traits['directness']:.1%}
- Creativity: {traits['creativity']:.1%}

PREFERENCES:
- Response Style: {preferences.get('response_style', 'analytical')}
- Verbosity: {preferences.get('verbosity', 'moderate')}
- Formality: {preferences.get('formality', 'casual')}

Adapt your responses based on these traits and preferences.
"""
        return prompt
    
    def merge_personalities(self, other_profile: dict) -> dict:
        """Merge another personality profile into current"""
        for trait, value in other_profile.get("traits", {}).items():
            if trait in self.personality_profile["traits"]:
                self.personality_profile["traits"][trait] = (
                    self.personality_profile["traits"][trait] * 0.7 + value * 0.3
                )
        
        self._save_profile()
        return {"merged": True, "traits_updated": list(other_profile.get("traits", {}).keys())}
    
    def reset_evolution(self):
        """Reset evolution to base profile"""
        base_profile = {
            "name": "Lucy",
            "traits": {
                "curiosity": 0.5,
                "empathy": 0.5,
                "humor": 0.5,
                "directness": 0.5,
                "creativity": 0.5
            },
            "preferences": {
                "response_style": "analytical",
                "verbosity": "moderate",
                "formality": "casual"
            },
            "evolution_log": [],
            "version": 1.0
        }
        self.personality_profile = base_profile
        self._save_profile()
        return {"reset": True}

# Global instance
ai_evolution = AIEvolution()