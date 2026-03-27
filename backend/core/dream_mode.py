"""
Dream Mode - Creative, unconstrained reasoning and exploration
"""
import asyncio
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import json

class DreamMode:
    def __init__(self):
        self.dream_path = Path("data/dream_mode")
        self.dream_path.mkdir(exist_ok=True)
        self.active = False
        self.dream_log: List[dict] = []
        self.max_dreams = 100
        self.creative_operators = [
            self._metaphor_generator,
            self._association_chain,
            self._contradiction_resolver,
            self._lateral_think,
            self._poetic_synthesis
        ]
    
    def activate(self, intensity: float = 0.7) -> dict:
        """Activate dream mode with specified intensity"""
        self.active = True
        self.intensity = max(0.1, min(1.0, intensity))
        return {
            "active": True,
            "intensity": self.intensity,
            "timestamp": datetime.now().isoformat()
        }
    
    def deactivate(self) -> dict:
        """Deactivate dream mode"""
        self.active = False
        return {"active": False, "timestamp": datetime.now().isoformat()}
    
    def _metaphor_generator(self, concept: str) -> str:
        """Generate metaphorical interpretations"""
        metaphors = [
            f"{concept} is like a river flowing through time",
            f"{concept} dances with the shadows of possibility",
            f"{concept} weaves a tapestry of meaning",
            f"{concept} sings in frequencies beyond understanding"
        ]
        return random.choice(metaphors)
    
    def _association_chain(self, seed: str, depth: int = 3) -> List[str]:
        """Create association chains from a seed concept"""
        associations = []
        words = seed.split()
        for i, word in enumerate(words):
            next_word = random.choice(["dream", "thought", "idea", "concept", "notion", "vision"])
            associations.append(f"{word} → {next_word}")
        return associations
    
    def _contradiction_resolver(self, paradox: str) -> str:
        """Provide non-binary resolution to paradoxes"""
        resolutions = [
            f"The paradox '{paradox}' exists in both states simultaneously",
            f"Both sides of '{paradox}' are partial truths",
            f"The contradiction reveals a deeper unity in '{paradox}'",
            f"Time resolves '{paradox}' when viewed from another angle"
        ]
        return random.choice(resolutions)
    
    def _lateral_think(self, problem: str) -> List[str]:
        """Generate lateral thinking solutions"""
        solutions = []
        angles = ["reverse", "invert", "externalize", "internalize", "expand", "condense"]
        for angle in angles:
            solutions.append(f"View '{problem}' from an {angle} perspective")
        return solutions[:3]
    
    def _poetic_synthesis(self, elements: List[str]) -> str:
        """Create poetic synthesis of multiple elements"""
        if len(elements) < 2:
            return " ".join(elements)
        
        conjunctions = ["and", "with", "through", "beyond", "within", "across"]
        return f"{elements[0]} {random.choice(conjunctions)} {elements[-1]}"
    
    def dream_on(self, input: str, iterations: int = 5) -> dict:
        """Run dream mode processing on input"""
        if not self.active:
            return {"error": "Dream mode not active", "activate": self.activate()}
        
        dream_result = {
            "original": input,
            "transformations": [],
            "insights": [],
            "creativity_score": 0.0
        }
        
        for i in range(iterations):
            operator = random.choice(self.creative_operators)
            result = operator(input)
            dream_result["transformations"].append({
                "iteration": i,
                "operator": operator.__name__,
                "result": result
            })
            input = result
        
        # Calculate creativity score
        creativity = sum(len(t["result"]) for t in dream_result["transformations"]) / iterations
        dream_result["creativity_score"] = round(min(100.0, creativity), 2)
        
        self.dream_log.append(dream_result)
        if len(self.dream_log) > self.max_dreams:
            self.dream_log = self.dream_log[-self.max_dreams:]
        
        return dream_result
    
    def get_dream_statistics(self) -> dict:
        """Get dream mode statistics"""
        if not self.dream_log:
            return {"total_dreams": 0}
        
        total_transformations = sum(len(d["transformations"]) for d in self.dream_log)
        avg_creativity = sum(d.get("creativity_score", 0) for d in self.dream_log) / len(self.dream_log)
        
        return {
            "total_dreams": len(self.dream_log),
            "total_transformations": total_transformations,
            "avg_creativity_score": round(avg_creativity, 2),
            "active": self.active
        }
    
    def export_dream_log(self) -> str:
        """Export dream log to JSON"""
        with open(self.dream_path / "dream_log.json", 'w') as f:
            json.dump(self.dream_log[-100:], f, indent=2)
        return f"Exported {len(self.dream_log)} dreams"

# Global instance
dream_mode = DreamMode()