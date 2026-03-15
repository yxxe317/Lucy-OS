"""
Quantum Memory - Store and retrieve quantum states
"""

import numpy as np
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime

class QuantumMemory:
    """
    Stores quantum states and entanglement patterns
    """
    
    def __init__(self):
        self.quantum_states = {}  # id -> quantum state
        self.superpositions = {}  # id -> superposition of possibilities
        self.entanglement_network = {}  # id -> entangled ids
        self.coherence_times = {}  # id -> coherence time
        
    def store_state(self, state_vector: np.ndarray, 
                     coherence_time: float = 1.0) -> str:
        """
        Store a quantum state
        """
        state_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        
        self.quantum_states[state_id] = {
            'vector': state_vector,
            'created': datetime.now(),
            'coherence': coherence_time,
            'measurements': 0
        }
        
        self.coherence_times[state_id] = coherence_time
        return state_id
    
    def store_superposition(self, possibilities: List[Any], 
                              probabilities: List[float]) -> str:
        """
        Store a superposition of possibilities
        """
        state_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        
        # Normalize probabilities
        prob_sum = sum(probabilities)
        probs = [p/prob_sum for p in probabilities]
        
        self.superpositions[state_id] = {
            'possibilities': possibilities,
            'probabilities': probs,
            'created': datetime.now(),
            'collapsed': False,
            'collapsed_value': None
        }
        
        return state_id
    
    def entangle(self, id1: str, id2: str, strength: float = 1.0):
        """
        Entangle two quantum memories
        """
        if id1 not in self.entanglement_network:
            self.entanglement_network[id1] = {}
        
        if id2 not in self.entanglement_network:
            self.entanglement_network[id2] = {}
        
        self.entanglement_network[id1][id2] = strength
        self.entanglement_network[id2][id1] = strength
    
    def collapse(self, state_id: str) -> Any:
        """
        Collapse a superposition to a single value
        """
        if state_id not in self.superpositions:
            return None
        
        sup = self.superpositions[state_id]
        
        if sup['collapsed']:
            return sup['collapsed_value']
        
        # Choose based on probabilities
        import random
        idx = random.choices(
            range(len(sup['possibilities'])),
            weights=sup['probabilities']
        )[0]
        
        value = sup['possibilities'][idx]
        
        sup['collapsed'] = True
        sup['collapsed_value'] = value
        
        # Update coherence
        if state_id in self.coherence_times:
            self.coherence_times[state_id] *= 0.9  # Decoherence
        
        return value
    
    def get_entangled_states(self, state_id: str) -> List[str]:
        """
        Get all states entangled with given state
        """
        if state_id in self.entanglement_network:
            return list(self.entanglement_network[state_id].keys())
        return []
    
    def measure_coherence(self, state_id: str) -> float:
        """
        Measure quantum coherence (0 = decohered, 1 = perfect coherence)
        """
        if state_id in self.coherence_times:
            age = (datetime.now() - self.quantum_states[state_id]['created']).total_seconds()
            coherence = max(0, 1 - age / self.coherence_times[state_id])
            return coherence
        return 0.0
    
    def apply_quantum_fourier_transform(self, state_id: str):
        """
        Apply quantum Fourier transform to stored state
        """
        if state_id not in self.quantum_states:
            return
        
        state = self.quantum_states[state_id]
        vector = state['vector']
        
        # Simplified QFT simulation
        n = len(vector)
        transformed = np.zeros(n, dtype=complex)
        
        for k in range(n):
            for j in range(n):
                transformed[k] += vector[j] * np.exp(2j * np.pi * j * k / n)
            transformed[k] /= np.sqrt(n)
        
        state['vector'] = transformed
        state['qft_applied'] = True
    
    def quantum_search(self, target_func, n_items: int = 16) -> int:
        """
        Simulate Grover's search algorithm
        """
        # Store superposition of all items
        possibilities = list(range(n_items))
        probabilities = [1/n_items] * n_items
        
        state_id = self.store_superposition(possibilities, probabilities)
        
        # Grover iterations (simplified)
        n_iterations = int(np.pi/4 * np.sqrt(n_items))
        
        for _ in range(n_iterations):
            # Oracle marks target
            sup = self.superpositions[state_id]
            new_probs = []
            for i, p in enumerate(sup['probabilities']):
                if target_func(sup['possibilities'][i]):
                    new_probs.append(p * 2)  # Amplify
                else:
                    new_probs.append(p * 0.5)  # Suppress
            
            # Normalize
            total = sum(new_probs)
            sup['probabilities'] = [p/total for p in new_probs]
        
        # Collapse to result
        return self.collapse(state_id)
    
    def get_quantum_entropy(self) -> float:
        """
        Calculate total quantum entropy in memory
        """
        entropy = 0
        
        # Entropy from superpositions
        for sup in self.superpositions.values():
            if not sup['collapsed']:
                # Shannon entropy of probability distribution
                probs = sup['probabilities']
                entropy -= sum(p * np.log2(p) for p in probs if p > 0)
        
        # Entropy from entanglement
        entropy += len(self.entanglement_network) * 0.1
        
        return entropy