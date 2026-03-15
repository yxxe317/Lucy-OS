"""
Brain-Computer Interface - Neural signal processing and thought interpretation
"""

import random
import numpy as np
from typing import Dict, List, Optional

class BrainComputerInterface:
    """
    Simulates brain-computer interface for neural signal processing
    """
    
    def __init__(self):
        self.brain_regions = {
            'prefrontal': {'active': False, 'function': 'decision making'},
            'motor': {'active': False, 'function': 'movement'},
            'visual': {'active': False, 'function': 'vision'},
            'auditory': {'active': False, 'function': 'hearing'},
            'hippocampus': {'active': False, 'function': 'memory'},
            'amygdala': {'active': False, 'function': 'emotion'},
            'cerebellum': {'active': False, 'function': 'coordination'}
        }
        
        self.neural_patterns = {}
        self.thought_history = []
        
    def read_neural_signals(self, duration: float = 1.0) -> Dict:
        """
        Simulate reading neural signals
        """
        signals = {}
        for region in self.brain_regions:
            # Generate random neural activity
            activity = random.uniform(0, 100)
            frequency = random.uniform(1, 40)  # Hz
            amplitude = random.uniform(0.1, 1.0)
            
            signals[region] = {
                'activity': activity,
                'frequency': frequency,
                'amplitude': amplitude,
                'dominant': activity > 70
            }
            
            self.brain_regions[region]['active'] = activity > 50
        
        return signals
    
    def interpret_thought(self, neural_data: Dict) -> str:
        """
        Interpret thoughts from neural patterns
        """
        thoughts = []
        
        if neural_data.get('prefrontal', {}).get('dominant'):
            thoughts.append("decision making")
        if neural_data.get('visual', {}).get('dominant'):
            thoughts.append("visual processing")
        if neural_data.get('auditory', {}).get('dominant'):
            thoughts.append("listening")
        if neural_data.get('hippocampus', {}).get('dominant'):
            thoughts.append("memory recall")
        if neural_data.get('amygdala', {}).get('dominant'):
            thoughts.append("emotional processing")
        
        if not thoughts:
            return "resting state"
        
        return f"processing: {', '.join(thoughts)}"
    
    def encode_thought(self, thought: str) -> np.ndarray:
        """
        Encode a thought into neural patterns
        """
        # Create unique neural signature for thought
        thought_hash = hash(thought) % 1000
        pattern = np.array([
            (thought_hash >> i) & 1 for i in range(10)
        ], dtype=float)
        
        self.neural_patterns[thought] = pattern
        return pattern
    
    def decode_thought(self, pattern: np.ndarray) -> Optional[str]:
        """
        Decode neural pattern into thought
        """
        for thought, stored_pattern in self.neural_patterns.items():
            if np.array_equal(pattern, stored_pattern):
                return thought
        return None
    
    def simulate_brainwave_entrainment(self, frequency: float, duration: float) -> str:
        """
        Simulate brainwave entrainment to specific frequency
        """
        states = {
            (0.5, 4): "deep sleep",
            (4, 8): "meditation",
            (8, 13): "relaxed focus",
            (13, 30): "active thinking",
            (30, 100): "hyperfocus"
        }
        
        for (low, high), state in states.items():
            if low <= frequency < high:
                return f"Entraining to {state} state at {frequency}Hz"
        
        return f"Unknown brainwave state at {frequency}Hz"