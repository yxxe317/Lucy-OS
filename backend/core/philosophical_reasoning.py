"""
Philosophical Reasoning Engine - Deep conceptual analysis and dialectic reasoning
"""
import asyncio
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import json

class PhilosophicalReasoning:
    def __init__(self):
        self.phil_path = Path("data/philosophical_reasoning")
        self.phil_path.mkdir(exist_ok=True)
        self.concept_database: Dict[str, Dict] = {}
        self.dialectic_history: List[dict] = []
        self.paradigm_shifts: List[dict] = []
        self.ethical_frameworks = [
            "Utilitarianism", "Deontology", "Virtue Ethics", 
            "Existentialism", "Phenomenology", "Pragmatism"
        ]
    
    def register_concept(self, name: str, definition: str, attributes: Dict = None) -> dict:
        """Register a philosophical concept"""
        concept = {
            "name": name,
            "definition": definition,
            "attributes": attributes or {},
            "related_concepts": [],
            "created": datetime.now().isoformat()
        }
        self.concept_database[name] = concept
        return {"registered": name, "total_concepts": len(self.concept_database)}
    
    def dialectic_analysis(self, thesis: str, antithesis: str) -> dict:
        """Perform dialectic analysis between two propositions"""
        synthesis = self._find_synthesis(thesis, antithesis)
        
        analysis = {
            "thesis": thesis,
            "antithesis": antithesis,
            "synthesis": synthesis,
            "tension_level": self._calculate_tension(thesis, antithesis),
            "resolution_path": self._generate_resolution_path(thesis, antithesis),
            "timestamp": datetime.now().isoformat()
        }
        self.dialectic_history.append(analysis)
        
        if len(self.dialectic_history) > 100:
            self.dialectic_history = self.dialectic_history[-50:]
        
        return analysis
    
    def _find_synthesis(self, thesis: str, antithesis: str) -> str:
        """Find synthesis between opposing views"""
        # Extract key themes
        thesis_themes = self._extract_themes(thesis)
        antithesis_themes = self._extract_themes(antithesis)
        
        # Find common ground
        common = set(thesis_themes) & set(antithesis_themes)
        
        if common:
            return f"Synthesis: {', '.join(common[:3])} form the bridge between opposing views"
        else:
            return "Synthesis: A higher understanding emerges from the tension"
    
    def _extract_themes(self, text: str) -> List[str]:
        """Extract key themes from text"""
        # Simple theme extraction
        words = text.lower().split()
        themes = []
        for word in words:
            if len(word) > 4:
                themes.append(word)
        return themes[:10]
    
    def _calculate_tension(self, thesis: str, antithesis: str) -> float:
        """Calculate conceptual tension between propositions"""
        thesis_themes = self._extract_themes(thesis)
        antithesis_themes = self._extract_themes(antithesis)
        
        # Tension is higher when themes are more different
        common_themes = set(thesis_themes) & set(antithesis_themes)
        total_themes = len(set(thesis_themes + antithesis_themes))
        
        if total_themes == 0:
            return 0.5
        
        overlap = len(common_themes) / total_themes
        return 0.5 + (0.5 * (1 - overlap))
    
    def _generate_resolution_path(self, thesis: str, antithesis: str) -> List[str]:
        """Generate steps to resolve conceptual tension"""
        steps = [
            "Identify underlying assumptions in each position",
            "Find the context where both might be partially true",
            "Consider temporal or contextual factors",
            "Look for higher-order principles that encompass both",
            "Test against practical consequences"
        ]
        return steps[:random.randint(2, 4)]
    
    def paradigm_shift_detection(self, current_paradigm: str, new_evidence: str) -> dict:
        """Detect potential paradigm shifts"""
        shift = {
            "current_paradigm": current_paradigm,
            "new_evidence": new_evidence,
            "shift_probability": self._calculate_shift_probability(current_paradigm, new_evidence),
            "implications": self._analyze_implications(current_paradigm, new_evidence),
            "timestamp": datetime.now().isoformat()
        }
        self.paradigm_shifts.append(shift)
        
        if len(self.paradigm_shifts) > 50:
            self.paradigm_shifts = self.paradigm_shifts[-25:]
        
        return shift
    
    def _calculate_shift_probability(self, paradigm: str, evidence: str) -> float:
        """Calculate probability of paradigm shift"""
        base_prob = 0.3
        evidence_strength = len(evidence) / 100.0
        return min(0.95, base_prob + evidence_strength * 0.3)
    
    def _analyze_implications(self, paradigm: str, evidence: str) -> List[str]:
        """Analyze implications of potential paradigm shift"""
        implications = [
            "Epistemological: How we know what we know",
            "Ontological: The nature of reality itself",
            "Axiological: The nature of value and meaning",
            "Methodological: How we investigate truth"
        ]
        return implications[:random.randint(1, 3)]
    
    def ethical_dilemma_resolution(self, dilemma: str, frameworks: List[str] = None) -> dict:
        """Apply ethical frameworks to resolve dilemmas"""
        frameworks = frameworks or self.ethical_frameworks
        
        resolutions = {}
        for framework in frameworks:
            resolution = self._apply_framework(framework, dilemma)
            resolutions[framework] = resolution
        
        # Find consensus
        consensus = self._find_ethical_consensus(resolutions)
        
        return {
            "dilemma": dilemma,
            "frameworks_applied": frameworks,
            "resolutions": resolutions,
            "consensus": consensus,
            "timestamp": datetime.now().isoformat()
        }
    
    def _apply_framework(self, framework: str, dilemma: str) -> str:
        """Apply a specific ethical framework"""
        if framework == "Utilitarianism":
            return "Maximize overall well-being while minimizing suffering"
        elif framework == "Deontology":
            return "Follow universalizable duties regardless of consequences"
        elif framework == "Virtue Ethics":
            return "Act in accordance with character virtues"
        elif framework == "Existentialism":
            return "Create meaning through authentic choice"
        elif framework == "Phenomenology":
            return "Understand the lived experience of the dilemma"
        elif framework == "Pragmatism":
            return "Test solutions through practical consequences"
        else:
            return f"Framework '{framework}' analysis pending"
    
    def _find_ethical_consensus(self, resolutions: Dict[str, str]) -> str:
        """Find consensus among ethical frameworks"""
        if not resolutions:
            return "No frameworks applied"
        
        # Look for overlapping principles
        principles = []
        for resolution in resolutions.values():
            for principle in ["well-being", "duty", "virtue", "authenticity", "experience", "practice"]:
                if principle in resolution.lower():
                    if principle not in principles:
                        principles.append(principle)
        
        return f"Consensus: {', '.join(principles[:3]) if principles else 'general ethical principles'}"
    
    def export_philosophical_data(self) -> str:
        """Export philosophical reasoning data"""
        data = {
            "concepts": self.concept_database,
            "dialectic_history": self.dialectic_history[-50:],
            "paradigm_shifts": self.paradigm_shifts[-25:],
            "timestamp": datetime.now().isoformat()
        }
        with open(self.phil_path / "philosophical_data.json", 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return f"Exported data for {len(self.concept_database)} concepts"

# Global instance
philosophical_reasoning = PhilosophicalReasoning()