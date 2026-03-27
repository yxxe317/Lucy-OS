"""
Reality Simulation Engine - Context-aware world modeling and prediction
"""
import asyncio
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
import json

class RealitySimulation:
    def __init__(self):
        self.sim_path = Path("data/reality_simulation")
        self.sim_path.mkdir(exist_ok=True)
        self.world_model: Dict[str, Any] = {}
        self.prediction_queue: List[dict] = []
        self.simulation_active = False
        self.confidence_threshold = 0.7
    
    def initialize_world(self, context: str) -> dict:
        """Initialize world model from context"""
        self.world_model = {
            "context": context,
            "entities": [],
            "relationships": [],
            "events": [],
            "constraints": [],
            "timestamp": datetime.now().isoformat()
        }
        return {"initialized": True, "context": context}
    
    def add_entity(self, name: str, properties: dict, relationships: List[str] = None) -> dict:
        """Add entity to world model"""
        entity = {
            "name": name,
            "properties": properties,
            "relationships": relationships or [],
            "created": datetime.now().isoformat()
        }
        self.world_model["entities"].append(entity)
        return {"entity": name, "total_entities": len(self.world_model["entities"])}
    
    def predict_outcome(self, scenario: str, variables: Dict[str, Any]) -> dict:
        """Predict outcome based on world model"""
        prediction = {
            "scenario": scenario,
            "variables": variables,
            "outcome": self._simulate_scenario(scenario, variables),
            "confidence": self._calculate_confidence(scenario, variables),
            "timestamp": datetime.now().isoformat()
        }
        self.prediction_queue.append(prediction)
        
        if len(self.prediction_queue) > 100:
            self.prediction_queue = self.prediction_queue[-50:]
        
        return prediction
    
    def _simulate_scenario(self, scenario: str, variables: dict) -> str:
        """Simulate scenario using world model"""
        # Extract relevant entities and constraints
        relevant_entities = [
            e for e in self.world_model.get("entities", [])
            if any(var in e["name"].lower() for var in variables.keys())
        ]
        
        # Generate simulated outcome
        outcome_factors = []
        for entity in relevant_entities:
            outcome_factors.append(entity["properties"].get("influence", 0.5))
        
        if not outcome_factors:
            return "Neutral outcome predicted"
        
        # Weighted outcome
        total = sum(outcome_factors)
        if total > 0:
            outcome_score = sum(outcome_factors) / len(outcome_factors)
        else:
            outcome_score = 0.5
        
        return f"Outcome: {'favorable' if outcome_score > 0.6 else 'challenging'} with score {outcome_score:.2f}"
    
    def _calculate_confidence(self, scenario: str, variables: dict) -> float:
        """Calculate prediction confidence"""
        base_confidence = 0.6
        entity_count = len([
            e for e in self.world_model.get("entities", [])
            if any(var in e["name"].lower() for var in variables.keys())
        ])
        return min(0.95, base_confidence + (entity_count * 0.05))
    
    def update_constraint(self, constraint: str, weight: float = 1.0) -> dict:
        """Add/update constraint in world model"""
        existing = next(
            (c for c in self.world_model.get("constraints", []) if c["text"] == constraint),
            None
        )
        if existing:
            existing["weight"] = weight
            existing["updated"] = datetime.now().isoformat()
        else:
            self.world_model["constraints"].append({
                "text": constraint,
                "weight": weight,
                "created": datetime.now().isoformat()
            })
        return {"constraint": constraint, "total_constraints": len(self.world_model["constraints"])}
    
    def resolve_conflict(self, conflicts: List[dict]) -> dict:
        """Resolve conflicting predictions"""
        resolution = {
            "conflicts": conflicts,
            "resolution": self._find_common_ground(conflicts),
            "confidence": self._calculate_confidence("conflict", {"resolution": True})
        }
        return resolution
    
    def _find_common_ground(self, conflicts: List[dict]) -> str:
        """Find common ground among conflicting predictions"""
        if not conflicts:
            return "No conflicts to resolve"
        
        # Extract key themes
        themes = []
        for conflict in conflicts:
            theme = conflict.get("theme", "unknown")
            if theme not in themes:
                themes.append(theme)
        
        return f"Common ground: {', '.join(themes[:3]) if themes else 'general consensus'}"
    
    def export_world_model(self) -> str:
        """Export world model to JSON"""
        with open(self.sim_path / "world_model.json", 'w') as f:
            json.dump(self.world_model, f, indent=2, default=str)
        return f"Exported world model with {len(self.world_model.get('entities', []))} entities"
    
    def get_simulation_stats(self) -> dict:
        """Get simulation statistics"""
        return {
            "entities": len(self.world_model.get("entities", [])),
            "relationships": len(self.world_model.get("relationships", [])),
            "constraints": len(self.world_model.get("constraints", [])),
            "predictions": len(self.prediction_queue),
            "active": self.simulation_active
        }

# Global instance
reality_simulation = RealitySimulation()