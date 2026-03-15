"""
Quantum Decision Making - Quantum algorithms for decisions
"""

import random
import numpy as np
from typing import List, Dict, Any, Optional, Tuple

class QuantumDecision:
    """
    Uses quantum principles for decision making
    """
    
    def __init__(self):
        self.decision_history = []
        self.quantum_superpositions = {}
        self.entangled_decisions = {}
    
    def superposition_choice(self, options: List[Any], 
                               probabilities: List[float] = None) -> Any:
        """
        Make choice from superposition of options
        """
        if not options:
            return None
        
        if probabilities is None:
            probabilities = [1.0/len(options)] * len(options)
        
        # Normalize probabilities
        total = sum(probabilities)
        probs = [p/total for p in probabilities]
        
        # Store superposition
        sup_id = len(self.quantum_superpositions)
        self.quantum_superpositions[sup_id] = {
            'options': options,
            'probabilities': probs,
            'collapsed': False
        }
        
        # Collapse to single choice
        choice_idx = np.random.choice(len(options), p=probs)
        choice = options[choice_idx]
        
        self.quantum_superpositions[sup_id]['collapsed'] = True
        self.quantum_superpositions[sup_id]['choice'] = choice
        
        self.decision_history.append({
            'type': 'superposition',
            'options': options,
            'choice': choice,
            'probabilities': probs
        })
        
        return choice
    
    def quantum_walk(self, graph: Dict[Any, List[Any]], 
                      steps: int = 10) -> List[Any]:
        """
        Quantum walk on a graph
        """
        if not graph:
            return []
        
        # Start at random node
        current = random.choice(list(graph.keys()))
        path = [current]
        
        for _ in range(steps):
            neighbors = graph.get(current, [])
            if not neighbors:
                break
            
            # Quantum superposition of neighbors
            neighbor_probs = [1.0/len(neighbors)] * len(neighbors)
            
            # Add quantum interference effects
            for i in range(len(neighbors)):
                # Simulate constructive/destructive interference
                phase = random.random() * 2 * np.pi
                neighbor_probs[i] *= (1 + 0.3 * np.cos(phase))
            
            # Normalize
            total = sum(neighbor_probs)
            neighbor_probs = [p/total for p in neighbor_probs]
            
            # Choose next step
            next_idx = np.random.choice(len(neighbors), p=neighbor_probs)
            current = neighbors[next_idx]
            path.append(current)
        
        self.decision_history.append({
            'type': 'quantum_walk',
            'path': path
        })
        
        return path
    
    def amplitude_amplification(self, good_options: List[Any], 
                                  all_options: List[Any]) -> Any:
        """
        Amplify probability of good options (Grover-like)
        """
        n = len(all_options)
        k = len(good_options)
        
        # Initial uniform superposition
        probs = [1.0/n] * n
        
        # Mark good options
        marked_indices = [all_options.index(opt) for opt in good_options 
                         if opt in all_options]
        
        # Grover iterations (simplified)
        iterations = int(np.pi/4 * np.sqrt(n/k))
        
        for _ in range(iterations):
            # Oracle flips amplitude of marked
            for i in marked_indices:
                probs[i] *= 2
            
            # Diffusion operator (inverts about average)
            avg = sum(probs) / n
            for i in range(n):
                probs[i] = avg - (probs[i] - avg)
            
            # Normalize
            total = sum(probs)
            probs = [p/total for p in probs]
        
        # Make choice
        choice_idx = np.random.choice(n, p=probs)
        choice = all_options[choice_idx]
        
        self.decision_history.append({
            'type': 'amplitude_amplification',
            'good_options': good_options,
            'choice': choice,
            'probability': probs[choice_idx]
        })
        
        return choice
    
    def entangled_decision(self, decision_id: str, options: List[Any],
                             partner_id: str = None) -> Any:
        """
        Make decision entangled with another decision
        """
        if partner_id and partner_id in self.entangled_decisions:
            # Correlated decision
            partner_choice = self.entangled_decisions[partner_id]
            
            # Find matching option
            matching = [opt for opt in options if opt == partner_choice]
            if matching:
                choice = matching[0]
            else:
                # Anti-correlated
                choice = random.choice([opt for opt in options 
                                       if opt != partner_choice])
        else:
            # Independent decision
            choice = random.choice(options)
        
        # Store entanglement
        self.entangled_decisions[decision_id] = choice
        if partner_id:
            self.entangled_decisions[partner_id] = choice
        
        self.decision_history.append({
            'type': 'entangled',
            'decision_id': decision_id,
            'partner_id': partner_id,
            'choice': choice
        })
        
        return choice
    
    def parallel_universe_choice(self, options: List[Any]) -> Dict[Any, Any]:
        """
        Explore all options in parallel universes
        """
        outcomes = {}
        
        for opt in options:
            # Simulate outcome in parallel universe
            outcomes[opt] = {
                'choice': opt,
                'universe_id': random.randint(1000, 9999),
                'probability': 1.0/len(options),
                'outcome': self._simulate_outcome(opt)
            }
        
        self.decision_history.append({
            'type': 'parallel_universes',
            'universes': len(options),
            'outcomes': outcomes
        })
        
        return outcomes
    
    def _simulate_outcome(self, option: Any) -> Dict:
        """Simulate outcome of a choice"""
        return {
            'success_probability': random.random(),
            'expected_value': random.uniform(0, 100),
            'risk_level': random.choice(['low', 'medium', 'high']),
            'timeframe': random.choice(['immediate', 'short-term', 'long-term'])
        }
    
    def quantum_tunnel_choice(self, options: List[Any], 
                                barriers: List[float]) -> Any:
        """
        Quantum tunnel through barriers to reach options
        """
        if len(options) != len(barriers):
            return random.choice(options)
        
        # Calculate tunneling probabilities
        probs = []
        for barrier in barriers:
            # Higher barrier = lower probability
            tunnel_prob = np.exp(-barrier)
            probs.append(tunnel_prob)
        
        # Normalize
        total = sum(probs)
        probs = [p/total for p in probs]
        
        # Choose option
        choice_idx = np.random.choice(len(options), p=probs)
        choice = options[choice_idx]
        
        self.decision_history.append({
            'type': 'quantum_tunnel',
            'options': options,
            'barriers': barriers,
            'choice': choice,
            'tunnel_probability': probs[choice_idx]
        })
        
        return choice
    
    def get_decision_entropy(self) -> float:
        """
        Calculate entropy of decision history
        """
        if not self.decision_history:
            return 0.0
        
        # Count decision types
        types = {}
        for d in self.decision_history:
            t = d['type']
            types[t] = types.get(t, 0) + 1
        
        # Shannon entropy
        total = len(self.decision_history)
        entropy = 0
        for count in types.values():
            p = count / total
            entropy -= p * np.log2(p)
        
        return entropy