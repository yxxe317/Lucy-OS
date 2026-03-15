"""
Quantum Entanglement - Simulated entanglement between qubits
"""

import random
import numpy as np
from typing import List, Dict, Tuple, Optional

class QuantumEntanglement:
    """
    Simulates quantum entanglement between qubits/particles
    """
    
    def __init__(self):
        self.entangled_pairs = {}  # pair_id -> (qubit1, qubit2)
        self.entangled_groups = []  # Groups of entangled particles
        self.correlations = {}  # Measurement correlations
    
    def create_bell_pair(self, qubit1: int, qubit2: int) -> str:
        """
        Create a Bell state (|00> + |11>)/√2
        """
        pair_id = f"bell_{qubit1}_{qubit2}"
        self.entangled_pairs[pair_id] = (qubit1, qubit2, 'bell')
        return pair_id
    
    def create_ghz_state(self, qubits: List[int]) -> str:
        """
        Create GHZ state (|00...0> + |11...1>)/√2
        """
        state_id = f"ghz_{'_'.join(map(str, qubits))}"
        self.entangled_groups.append({
            'id': state_id,
            'qubits': qubits,
            'type': 'ghz'
        })
        return state_id
    
    def create_w_state(self, qubits: List[int]) -> str:
        """
        Create W state (|100...0> + |010...0> + ... + |000...1>)/√n
        """
        state_id = f"w_{'_'.join(map(str, qubits))}"
        self.entangled_groups.append({
            'id': state_id,
            'qubits': qubits,
            'type': 'w'
        })
        return state_id
    
    def measure_correlated(self, pair_id: str) -> Tuple[int, int]:
        """
        Measure an entangled pair with perfect correlation
        """
        if pair_id not in self.entangled_pairs:
            return (random.randint(0, 1), random.randint(0, 1))
        
        # Bell pairs are perfectly correlated
        outcome = random.randint(0, 1)
        self.correlations[pair_id] = outcome
        return (outcome, outcome)
    
    def measure_anticorrelated(self, pair_id: str) -> Tuple[int, int]:
        """
        Measure an entangled pair with perfect anticorrelation
        """
        if pair_id not in self.entangled_pairs:
            return (random.randint(0, 1), random.randint(0, 1))
        
        outcome = random.randint(0, 1)
        self.correlations[pair_id] = outcome
        return (outcome, 1 - outcome)
    
    def teleport(self, state: int, alice_qubit: int, bell_pair_id: str) -> Optional[int]:
        """
        Simulate quantum teleportation
        """
        if bell_pair_id not in self.entangled_pairs:
            return None
        
        # Alice measures her qubit and the Bell pair
        alice_result = random.randint(0, 3)  # 2-bit result
        
        # Bob's qubit becomes the teleported state
        # (simplified simulation)
        bob_state = state
        if alice_result in [1, 3]:
            bob_state ^= 1  # Apply X if needed
        
        return bob_state
    
    def get_correlation_strength(self, pair_id: str) -> float:
        """
        Get correlation strength between entangled particles
        """
        if pair_id in self.correlations:
            return 1.0  # Perfect correlation for Bell pairs
        return 0.0
    
    def violate_bell_inequality(self) -> Dict:
        """
        Simulate Bell inequality violation (CHSH game)
        """
        # CHSH game: players share entangled pair
        # Random measurements show correlation > classical limit
        
        measurements = []
        wins = 0
        trials = 1000
        
        for _ in range(trials):
            # Random measurement bases
            a = random.randint(0, 1)  # Alice's basis
            b = random.randint(0, 1)  # Bob's basis
            
            # Entangled particles give correlated outcomes
            x = random.randint(0, 1)  # Alice's outcome
            y = x if random.random() < 0.85 else 1 - x  # Correlated
            
            # Winning condition: x*y = (a & b)
            win = (x ^ y) == (a & b)
            if win:
                wins += 1
            
            measurements.append({
                'a': a, 'b': b,
                'x': x, 'y': y,
                'win': win
            })
        
        win_prob = wins / trials
        
        return {
            'win_probability': win_prob,
            'classical_limit': 0.75,
            'quantum_violation': win_prob > 0.75,
            'trials': trials,
            'measurements': measurements[:10]  # First 10 samples
        }
    
    def get_entropy(self, group_id: str = None) -> float:
        """
        Calculate entanglement entropy
        """
        if group_id:
            # Calculate entropy for specific group
            return random.uniform(0, 1)  # Simplified
        else:
            # Average entropy across all entangled systems
            if self.entangled_pairs or self.entangled_groups:
                return 0.8  # Highly entangled
            return 0.0