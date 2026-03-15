"""
Mood Engine - 8 primary moods with decay and transitions
"""

import random
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class MoodEngine:
    """
    Simulates emotional states with 8 primary moods
    """
    
    def __init__(self, config_path: str = None):
        # 8 primary moods with values 0-1
        self.moods = {
            'joy': 0.5,
            'sadness': 0.1,
            'anger': 0.1,
            'fear': 0.1,
            'surprise': 0.2,
            'disgust': 0.1,
            'trust': 0.5,
            'anticipation': 0.3
        }
        
        # Mood decay rates (per hour)
        self.decay_rates = {
            'joy': 0.1,
            'sadness': 0.05,
            'anger': 0.15,
            'fear': 0.12,
            'surprise': 0.3,
            'disgust': 0.08,
            'trust': 0.04,
            'anticipation': 0.1
        }
        
        # Mood influences (what affects what)
        self.influences = {
            'joy': {'sadness': -0.3, 'trust': 0.2},
            'sadness': {'joy': -0.4, 'anger': 0.2},
            'anger': {'trust': -0.3, 'fear': 0.2},
            'fear': {'trust': -0.2, 'anticipation': 0.3},
            'surprise': {'joy': 0.1, 'fear': 0.1},
            'disgust': {'trust': -0.2, 'anger': 0.1},
            'trust': {'joy': 0.2, 'fear': -0.2},
            'anticipation': {'surprise': 0.3, 'joy': 0.1}
        }
        
        # Last update time
        self.last_update = datetime.now()
        
        # Mood history for analysis
        self.history = []
        
        # Load saved mood if exists
        if config_path:
            self.load(config_path)
    
    def get_current_mood(self) -> Dict[str, float]:
        """
        Get current mood state
        """
        self._apply_decay()
        return self.moods.copy()
    
    def get_dominant_mood(self) -> Tuple[str, float]:
        """
        Get the strongest current mood
        """
        dominant = max(self.moods.items(), key=lambda x: x[1])
        return dominant
    
    def update_from_sentiment(self, sentiment: Dict[str, float]):
        """
        Update mood based on sentiment analysis
        """
        # sentiment should have: positivity, negativity, etc.
        if 'positivity' in sentiment:
            self.adjust_mood('joy', sentiment['positivity'] * 0.3)
        
        if 'negativity' in sentiment:
            self.adjust_mood('sadness', sentiment['negativity'] * 0.2)
            self.adjust_mood('anger', sentiment['negativity'] * 0.1)
        
        if 'surprise' in sentiment:
            self.adjust_mood('surprise', sentiment['surprise'] * 0.4)
        
        self._record_history('sentiment_update', sentiment)
    
    def adjust_mood(self, mood: str, delta: float):
        """
        Adjust a specific mood
        """
        if mood in self.moods:
            self.moods[mood] = max(0.0, min(1.0, self.moods[mood] + delta))
            
            # Apply influence on related moods
            if mood in self.influences:
                for influenced, influence in self.influences[mood].items():
                    if influenced in self.moods:
                        self.moods[influenced] = max(0.0, min(1.0, 
                            self.moods[influenced] + delta * influence))
    
    def trigger_event(self, event_type: str, intensity: float = 0.3):
        """
        Trigger an emotional event
        """
        event_map = {
            'success': {'joy': 0.3, 'trust': 0.1},
            'failure': {'sadness': 0.2, 'anger': 0.1},
            'threat': {'fear': 0.4, 'anticipation': 0.2},
            'surprise': {'surprise': 0.5},
            'betrayal': {'trust': -0.4, 'anger': 0.3},
            'kindness': {'trust': 0.3, 'joy': 0.2},
            'danger': {'fear': 0.5, 'anticipation': 0.2},
            'relief': {'fear': -0.3, 'joy': 0.2}
        }
        
        if event_type in event_map:
            for mood, delta in event_map[event_type].items():
                self.adjust_mood(mood, delta * intensity)
            
            self._record_history('event', {'type': event_type, 'intensity': intensity})
    
    def natural_decay(self):
        """
        Apply natural mood decay over time
        """
        now = datetime.now()
        hours_passed = (now - self.last_update).total_seconds() / 3600
        
        if hours_passed > 0:
            for mood in self.moods:
                # Decay towards baseline (0.3 for most moods)
                baseline = 0.3
                if mood in ['joy', 'trust']:
                    baseline = 0.4
                
                decay = self.decay_rates[mood] * hours_passed
                current = self.moods[mood]
                
                if current > baseline:
                    self.moods[mood] = max(baseline, current - decay)
                elif current < baseline:
                    self.moods[mood] = min(baseline, current + decay * 0.5)
            
            self.last_update = now
    
    def _apply_decay(self):
        """Internal method to apply decay before operations"""
        self.natural_decay()
    
    def _record_history(self, event_type: str, data: Dict):
        """Record mood change for analysis"""
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'data': data,
            'moods': self.moods.copy()
        })
        
        # Keep history manageable
        if len(self.history) > 1000:
            self.history = self.history[-1000:]
    
    def get_mood_description(self) -> str:
        """
        Get human-readable mood description
        """
        dominant, value = self.get_dominant_mood()
        
        if value > 0.8:
            intensity = "extremely"
        elif value > 0.6:
            intensity = "very"
        elif value > 0.4:
            intensity = "somewhat"
        else:
            intensity = "slightly"
        
        mood_names = {
            'joy': 'happy',
            'sadness': 'sad',
            'anger': 'angry',
            'fear': 'afraid',
            'surprise': 'surprised',
            'disgust': 'disgusted',
            'trust': 'trusting',
            'anticipation': 'anticipating'
        }
        
        return f"I'm feeling {intensity} {mood_names[dominant]}"
    
    def save(self, path: str = "mood_state.json"):
        """Save mood state to file"""
        state = {
            'moods': self.moods,
            'last_update': self.last_update.isoformat(),
            'history': self.history[-100:]  # Save last 100 events
        }
        with open(path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load(self, path: str):
        """Load mood state from file"""
        try:
            with open(path, 'r') as f:
                state = json.load(f)
                self.moods = state['moods']
                self.last_update = datetime.fromisoformat(state['last_update'])
                self.history = state.get('history', [])
        except:
            pass  # Use defaults if load fails