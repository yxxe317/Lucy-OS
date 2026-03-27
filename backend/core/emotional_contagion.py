"""
Emotional Contagion Model - Emotional spread tracking and empathy simulation
"""
import asyncio
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import json

class EmotionalContagion:
    def __init__(self):
        self.emotion_path = Path("data/emotional_contagion")
        self.emotion_path.mkdir(exist_ok=True)
        self.emotion_network: Dict[str, List[str]] = {}
        self.emotional_states: Dict[str, float] = {}
        self.contagion_threshold = 0.5
        self.empathy_levels: Dict[str, float] = {}
    
    def initialize_network(self, nodes: List[str], edges: List[tuple]) -> dict:
        """Initialize emotional network"""
        for node in nodes:
            self.emotion_network[node] = []
        
        for edge in edges:
            if edge[0] in self.emotion_network and edge[1] in self.emotion_network:
                self.emotion_network[edge[0]].append(edge[1])
                self.emotion_network[edge[1]].append(edge[0])
        
        return {
            "nodes": len(nodes),
            "edges": len(edges),
            "network_density": self._calculate_density(nodes, edges)
        }
    
    def set_emotional_state(self, entity: str, emotion: str, intensity: float) -> dict:
        """Set emotional state for an entity"""
        self.emotional_states[entity] = {
            "emotion": emotion,
            "intensity": min(1.0, max(0.0, intensity)),
            "timestamp": datetime.now().isoformat()
        }
        self.empathy_levels[entity] = random.uniform(0.3, 0.9)
        return {"entity": entity, "emotion": emotion, "intensity": intensity}
    
    def propagate_emotion(self, source: str, emotion: str, intensity: float = 0.8) -> dict:
        """Propagate emotion through network"""
        propagation = {
            "source": source,
            "emotion": emotion,
            "intensity": intensity,
            "affected": [],
            "iterations": 0
        }
        
        queue = [(source, intensity, 0)]
        visited = {source}
        
        while queue:
            current, current_intensity, depth = queue.pop(0)
            propagation["iterations"] = depth
            
            if depth > 5:
                break
            
            for neighbor in self.emotion_network.get(current, []):
                if neighbor in visited:
                    continue
                
                # Calculate transmission probability
                empathy = self.empathy_levels.get(neighbor, 0.5)
                transmission_prob = current_intensity * empathy * 0.7
                
                if transmission_prob > self.contagion_threshold:
                    new_intensity = current_intensity * 0.6
                    visited.add(neighbor)
                    propagation["affected"].append(neighbor)
                    
                    # Queue neighbor for further propagation
                    queue.append((neighbor, new_intensity, depth + 1))
        
        return propagation
    
    def calculate_empathy_score(self, entity: str) -> float:
        """Calculate empathy score for entity"""
        if entity not in self.empathy_levels:
            return 0.5
        
        base_score = self.empathy_levels[entity]
        emotional_diversity = len(set(
            state["emotion"] for state in self.emotional_states.values()
            if state["entity"] == entity
        ))
        
        return min(1.0, base_score + (emotional_diversity * 0.1))
    
    def detect_emotional_resonance(self) -> List[dict]:
        """Detect emotional resonance patterns"""
        resonance_patterns = []
        
        for entity, state in self.emotional_states.items():
            similar_count = sum(1 for other_state in self.emotional_states.values()
                             if other_state["emotion"] == state["emotion"]
                             and abs(other_state["intensity"] - state["intensity"]) < 0.2)
            
            if similar_count > 2:
                resonance_patterns.append({
                    "emotion": state["emotion"],
                    "intensity": state["intensity"],
                    "resonance_count": similar_count,
                    "entities": [e for e, s in self.emotional_states.items()
                              if s["emotion"] == state["emotion"]
                              and abs(s["intensity"] - state["intensity"]) < 0.2]
                })
        
        return resonance_patterns
    
    def simulate_empathy_chain(self, chain_length: int = 5) -> dict:
        """Simulate empathy chain reaction"""
        if not self.emotion_network:
            return {"error": "Network not initialized"}
        
        start_node = random.choice(list(self.emotion_network.keys()))
        chain = [start_node]
        current = start_node
        
        for _ in range(chain_length - 1):
            neighbors = self.emotion_network.get(current, [])
            if not neighbors:
                break
            current = random.choice(neighbors)
            if current in chain:
                break
            chain.append(current)
        
        return {
            "chain": chain,
            "length": len(chain),
            "empathy_flow": self._calculate_empathy_flow(chain)
        }
    
    def _calculate_density(self, nodes: List[str], edges: List[tuple]) -> float:
        """Calculate network density"""
        if len(nodes) < 2:
            return 0.0
        max_edges = len(nodes) * (len(nodes) - 1) / 2
        return min(1.0, len(edges) / max_edges) if max_edges > 0 else 0.0
    
    def _calculate_empathy_flow(self, chain: List[str]) -> float:
        """Calculate empathy flow through chain"""
        if len(chain) < 2:
            return 0.0
        
        flow = 1.0
        for i in range(len(chain) - 1):
            empathy = self.empathy_levels.get(chain[i], 0.5)
            flow *= empathy * 0.8
        
        return max(0.0, min(1.0, flow))
    
    def export_contagion_data(self) -> str:
        """Export contagion data to JSON"""
        data = {
            "network": self.emotion_network,
            "states": self.emotional_states,
            "empathy_levels": self.empathy_levels,
            "timestamp": datetime.now().isoformat()
        }
        with open(self.emotion_path / "contagion_data.json", 'w') as f:
            json.dump(data, f, indent=2)
        return f"Exported data for {len(self.emotion_network)} nodes"

# Global instance
emotional_contagion = EmotionalContagion()