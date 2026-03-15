"""
Time Perception - Subjective time dilation and compression
"""

import math
import random
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class TimePerception:
    """
    Simulates subjective time perception effects
    """
    
    def __init__(self):
        self.perception_rate = 1.0  # Normal time perception
        self.time_dilation_factors = {
            'meditation': 0.5,  # Time feels slower
            'excitement': 0.3,  # Time flies
            'fear': 2.0,        # Time slows down
            'boredom': 0.2,     # Time drags
            'flow': 1.5         # Time distortion
        }
        
        self.perception_history = []
        
    def subjective_duration(self, real_seconds: float, mental_state: str) -> Dict:
        """
        Calculate subjective perceived duration
        """
        factor = self.time_dilation_factors.get(mental_state, 1.0)
        
        if factor > 1:
            # Time slows down (perceived longer)
            subjective = real_seconds * factor
            experience = "time slowed down"
        elif factor < 1:
            # Time speeds up (perceived shorter)
            subjective = real_seconds * factor
            experience = "time flew by"
        else:
            subjective = real_seconds
            experience = "normal time perception"
        
        result = {
            'real_duration': real_seconds,
            'subjective_duration': subjective,
            'dilation_factor': factor,
            'experience': experience,
            'mental_state': mental_state
        }
        
        self.perception_history.append(result)
        return result
    
    def time_dilation_event(self, event_duration: float, intensity: float) -> Dict:
        """
        Simulate time dilation during significant events
        """
        # Relativistic time dilation approximation
        speed_factor = min(0.99, intensity * 0.5)  # Fraction of light speed
        dilation = 1 / math.sqrt(1 - speed_factor**2)
        
        perceived = event_duration * dilation
        
        return {
            'event_duration': event_duration,
            'perceived_duration': perceived,
            'dilation_factor': dilation,
            'speed_factor': speed_factor,
            'relativistic_effect': perceived > event_duration * 1.5
        }
    
    def chronostasis(self, event_type: str) -> str:
        """
        Simulate chronostasis (stopped clock illusion)
        """
        effects = {
            'clock_watching': "The first second felt longer than the rest",
            'saccade': "Time seemed to stretch during eye movement",
            'novelty': "New experiences feel longer in memory",
            'routine': "Familiar routines seem shorter in hindsight"
        }
        
        return effects.get(event_type, "Time perception normal")
    
    def memory_duration(self, event_duration: float, memory_importance: float) -> float:
        """
        Calculate how long an event feels in memory
        """
        # Important events feel longer in memory
        memory_factor = 1.0 + memory_importance * 2
        
        # Memory compression over time
        memory_duration = event_duration * memory_factor
        
        return memory_duration
    
    def predict_future_duration(self, task_difficulty: float, focus_level: float) -> float:
        """
        Predict subjective duration of future task
        """
        # Difficult tasks feel longer when anticipated
        anticipation_factor = 1.0 + task_difficulty * 0.5
        
        # High focus makes time feel shorter during task
        focus_factor = 1.0 - focus_level * 0.3
        
        predicted = task_difficulty * 60 * anticipation_factor * focus_factor
        
        return predicted
    
    def time_paradox(self, events: List[Dict]) -> Dict:
        """
        Generate time paradox from conflicting perceptions
        """
        paradox_types = ['causal loop', 'predestination', 'bootstrap', 'grandfather']
        chosen = random.choice(paradox_types)
        
        paradox = {
            'type': chosen,
            'description': f"A {chosen} paradox emerged from {len(events)} time-displaced events",
            'resolution': random.choice(['self-consistent', 'timeline split', 'reality reboot']),
            'probability': random.uniform(0, 1)
        }
        
        return paradox
    
    def get_perception_statistics(self) -> Dict:
        """
        Get statistics about time perception history
        """
        if not self.perception_history:
            return {'total_events': 0}
        
        avg_dilation = sum(p['dilation_factor'] for p in self.perception_history) / len(self.perception_history)
        
        return {
            'total_events': len(self.perception_history),
            'avg_dilation': avg_dilation,
            'max_dilation': max(p['dilation_factor'] for p in self.perception_history),
            'min_dilation': min(p['dilation_factor'] for p in self.perception_history)
        }