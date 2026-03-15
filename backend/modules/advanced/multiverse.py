"""
Multiverse Explorer - Explore parallel universes and timelines
"""

import random
import hashlib
from typing import Dict, List, Optional
from datetime import datetime

class MultiverseExplorer:
    """
    Simulates exploration of parallel universes and alternate timelines
    """
    
    def __init__(self):
        self.universes = {}
        self.timelines = []
        self.current_universe = 'prime'
        self.quantum_branches = 0
        
        # Initialize prime universe
        self.universes['prime'] = {
            'id': 'prime',
            'created': datetime.now().isoformat(),
            'timeline_count': 1,
            'stability': 1.0,
            'entropy': 0.5
        }
    
    def create_branch_universe(self, divergence_point: str, probability: float) -> str:
        """
        Create a branched universe at divergence point
        """
        universe_id = hashlib.md5(f"{divergence_point}{random.random()}".encode()).hexdigest()[:8]
        
        universe = {
            'id': universe_id,
            'parent': self.current_universe,
            'divergence_point': divergence_point,
            'probability': probability,
            'created': datetime.now().isoformat(),
            'timeline_count': random.randint(1, 100),
            'stability': random.uniform(0.1, 1.0),
            'entropy': random.uniform(0, 1),
            'inhabitants': random.randint(10**9, 10**12)
        }
        
        self.universes[universe_id] = universe
        self.quantum_branches += 1
        
        return universe_id
    
    def explore_universe(self, universe_id: str) -> Dict:
        """
        Explore a specific universe
        """
        if universe_id not in self.universes:
            return {'error': 'Universe not found'}
        
        universe = self.universes[universe_id]
        
        # Generate universe details
        exploration = {
            'universe_id': universe_id,
            'physical_laws': self._generate_physical_laws(),
            'civilization_level': random.choice(['primitive', 'advanced', 'transcendent', 'unknown']),
            'technology': random.choice(['steam', 'digital', 'quantum', 'consciousness-based']),
            'dominant_species': random.choice(['humanoid', 'AI', 'energy-based', 'unknown']),
            'notable_features': random.sample([
                'binary stars', 'ring world', 'dyson sphere', 'space elevators',
                'planet-sized AI', 'time loops', 'reality bubbles'
            ], 3),
            'stability': universe['stability'],
            'entropy': universe['entropy']
        }
        
        return exploration
    
    def _generate_physical_laws(self) -> Dict:
        """Generate physical laws for a universe"""
        return {
            'speed_of_light': random.uniform(1e8, 1e9),
            'gravity_constant': random.uniform(1e-11, 1e-10),
            'planck_constant': random.uniform(1e-35, 1e-33),
            'dimensions': random.randint(3, 11),
            'time_direction': random.choice(['forward', 'backward', 'cyclic', 'static'])
        }
    
    def quantum_superposition(self, options: List[str]) -> List[Dict]:
        """
        Place options in quantum superposition across universes
        """
        superpositions = []
        
        for option in options:
            # Option exists in multiple universes with different probabilities
            for _ in range(random.randint(1, 5)):
                universe_id = self.create_branch_universe(f"option_{option}", random.random())
                superpositions.append({
                    'option': option,
                    'universe': universe_id,
                    'amplitude': complex(random.random(), random.random()),
                    'observed': False
                })
        
        return superpositions
    
    def collapse_superposition(self, superpositions: List[Dict], observed_option: str) -> Dict:
        """
        Collapse superposition by observation
        """
        # Find matching options
        matches = [s for s in superpositions if s['option'] == observed_option]
        
        if not matches:
            return {'error': 'Option not in superposition'}
        
        # Collapse to one universe
        chosen = random.choice(matches)
        chosen['observed'] = True
        
        # Other universes branch off
        collapsed = {
            'observed_universe': chosen['universe'],
            'observed_option': observed_option,
            'branched_universes': len([s for s in superpositions if s != chosen]),
            'wavefunction_collapsed': True
        }
        
        return collapsed
    
    def timeline_merge(self, timeline1: str, timeline2: str) -> Dict:
        """
        Merge two timelines
        """
        merge_id = hashlib.md5(f"{timeline1}{timeline2}".encode()).hexdigest()[:8]
        
        merge_result = {
            'id': merge_id,
            'source_timelines': [timeline1, timeline2],
            'stability': random.uniform(0, 1),
            'paradox_risk': random.uniform(0, 1),
            'merged_elements': random.randint(10, 1000),
            'timeline': 'merged'
        }
        
        return merge_result
    
    def get_multiverse_statistics(self) -> Dict:
        """
        Get statistics about multiverse
        """
        return {
            'total_universes': len(self.universes),
            'quantum_branches': self.quantum_branches,
            'avg_stability': sum(u['stability'] for u in self.universes.values()) / len(self.universes),
            'avg_entropy': sum(u['entropy'] for u in self.universes.values()) / len(self.universes),
            'total_inhabitants': sum(u.get('inhabitants', 0) for u in self.universes.values())
        }
    
    def find_alternate_self(self, traits: List[str]) -> Dict:
        """
        Find alternate version of self in multiverse
        """
        alternate_selves = []
        
        for _ in range(random.randint(1, 10)):
            universe_id = self.create_branch_universe(f"self_variant_{random.random()}", random.random())
            
            alternate = {
                'universe': universe_id,
                'similarity': random.uniform(0, 1),
                'different_traits': random.sample(traits, random.randint(1, len(traits))),
                'life_path': random.choice(['similar', 'completely different', 'opposite']),
                'success_level': random.uniform(0, 1)
            }
            alternate_selves.append(alternate)
        
        # Find most similar
        if alternate_selves:
            most_similar = max(alternate_selves, key=lambda x: x['similarity'])
            return most_similar
        
        return {'error': 'No alternate selves found'}