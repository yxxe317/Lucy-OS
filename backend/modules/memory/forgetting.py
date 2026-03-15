"""
Forgetting curve simulation - Ebbinghaus forgetting curve
"""

import math
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class ForgettingCurve:
    """
    Simulates forgetting using Ebbinghaus curve
    """
    
    def __init__(self):
        # Ebbinghaus parameters
        self.initial_retention = 1.0
        self.decay_factor = 0.5  # How fast forgetting occurs
        self.repetition_boost = 1.5  # Boost from repetition
        
        # Memory strengths
        self.memories = {}  # memory_id -> strength
        
    def calculate_retention(self, hours_ago: float, repetitions: int = 1) -> float:
        """
        Calculate retention after given hours
        Based on Ebbinghaus forgetting curve: R = e^(-t/S)
        """
        # Base retention
        retention = math.exp(-hours_ago / (24 * self.decay_factor))
        
        # Boost from repetitions
        retention *= (1 + (repetitions - 1) * 0.3)
        
        return min(1.0, retention)
    
    def record_memory(self, memory_id: str, initial_strength: float = 1.0):
        """
        Record a new memory
        """
        self.memories[memory_id] = {
            'strength': initial_strength,
            'repetitions': 1,
            'created': datetime.now(),
            'last_recall': datetime.now()
        }
    
    def recall_memory(self, memory_id: str) -> float:
        """
        Recall a memory, updating its strength
        """
        if memory_id not in self.memories:
            return 0.0
        
        mem = self.memories[memory_id]
        now = datetime.now()
        
        # Calculate hours since last recall
        hours_since = (now - mem['last_recall']).total_seconds() / 3600
        
        # Current strength based on forgetting curve
        current_strength = mem['strength'] * math.exp(-hours_since / (24 * self.decay_factor))
        
        # Boost from this recall
        mem['repetitions'] += 1
        mem['strength'] = current_strength * self.repetition_boost
        mem['last_recall'] = now
        
        return mem['strength']
    
    def get_forgetting_curve(self, days: int = 30) -> List[float]:
        """
        Generate forgetting curve for visualization
        """
        hours = np.linspace(0, days * 24, 100)
        curve = [self.calculate_retention(h) for h in hours]
        return curve
    
    def should_forget(self, memory_id: str, threshold: float = 0.1) -> bool:
        """
        Determine if memory should be forgotten
        """
        if memory_id not in self.memories:
            return True
        
        mem = self.memories[memory_id]
        hours_since = (datetime.now() - mem['last_recall']).total_seconds() / 3600
        current = mem['strength'] * math.exp(-hours_since / (24 * self.decay_factor))
        
        return current < threshold
    
    def reinforce_memory(self, memory_id: str, importance: float = 1.0):
        """
        Artificially reinforce a memory (important ones)
        """
        if memory_id in self.memories:
            self.memories[memory_id]['strength'] *= (1.5 * importance)
            self.memories[memory_id]['last_recall'] = datetime.now()
    
    def get_memory_health(self, memory_id: str) -> Dict:
        """
        Get detailed memory health metrics
        """
        if memory_id not in self.memories:
            return {'exists': False}
        
        mem = self.memories[memory_id]
        hours_since = (datetime.now() - mem['last_recall']).total_seconds() / 3600
        current = mem['strength'] * math.exp(-hours_since / (24 * self.decay_factor))
        
        return {
            'exists': True,
            'strength': current,
            'original_strength': mem['strength'],
            'repetitions': mem['repetitions'],
            'age_hours': (datetime.now() - mem['created']).total_seconds() / 3600,
            'hours_since_recall': hours_since,
            'forgetting_risk': 1 - current
        }
    
    def cleanup_forgotten(self, threshold: float = 0.05) -> int:
        """
        Remove forgotten memories
        """
        to_remove = []
        for mem_id in self.memories:
            if self.should_forget(mem_id, threshold):
                to_remove.append(mem_id)
        
        for mem_id in to_remove:
            del self.memories[mem_id]
        
        return len(to_remove)