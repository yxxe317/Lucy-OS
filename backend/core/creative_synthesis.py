"""
Creative Synthesis Module - Cross-domain idea generation and creative problem solving
"""
import asyncio
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
import json

class CreativeSynthesis:
    def __init__(self):
        self.synth_path = Path("data/creative_synthesis")
        self.synth_path.mkdir(exist_ok=True)
        self.idea_pool: List[dict] = []
        self.cross_domain_mappings: Dict[str, List[str]] = {}
        self.creative_operators: List[Callable] = []
        self.synthesis_history: List[dict] = []
    
    def register_idea(self, idea: str, domain: str, attributes: Dict = None) -> dict:
        """Register an idea in the pool"""
        idea_entry = {
            "idea": idea,
            "domain": domain,
            "attributes": attributes or {},
            "created": datetime.now().isoformat()
        }
        self.idea_pool.append(idea_entry)
        return {"registered": idea, "total_ideas": len(self.idea_pool)}
    
    def map_domains(self, domain: str, mappings: List[str]) -> dict:
        """Create cross-domain mappings"""
        self.cross_domain_mappings[domain] = mappings
        return {"domain": domain, "mappings": len(mappings)}
    
    def apply_operator(self, operator: Callable, input_data: Any) -> Any:
        """Apply a creative operator to input data"""
        result = operator(input_data)
        self.creative_operators.append(operator)
        return result
    
    def synthesize_ideas(self, ideas: List[str], domains: List[str] = None) -> dict:
        """Synthesize new ideas from existing ones"""
        domains = domains or list(self.cross_domain_mappings.keys())
        
        synthesis = {
            "input_ideas": ideas,
            "input_domains": domains,
            "synthesis_process": self._run_synthesis_process(ideas, domains),
            "output_ideas": self._extract_output_ideas(),
            "creativity_score": self._calculate_creativity_score(ideas, domains),
            "timestamp": datetime.now().isoformat()
        }
        
        self.synthesis_history.append(synthesis)
        if len(self.synthesis_history) > 100:
            self.synthesis_history = self.synthesis_history[-50:]
        
        return synthesis
    
    def _run_synthesis_process(self, ideas: List[str], domains: List[str]) -> List[dict]:
        """Run the synthesis process"""
        processes = []
        
        # Step 1: Deconstruct ideas
        deconstructed = self._deconstruct_ideas(ideas)
        processes.append({"step": "deconstruction", "result": deconstructed})
        
        # Step 2: Cross-pollinate with other domains
        cross_pollinated = self._cross_pollinate(deconstructed, domains)
        processes.append({"step": "cross-pollination", "result": cross_pollinated})
        
        # Step 3: Reconstruct with new connections
        reconstructed = self._reconstruct_connections(cross_pollinated)
        processes.append({"step": "reconstruction", "result": reconstructed})
        
        return processes
    
    def _deconstruct_ideas(self, ideas: List[str]) -> List[dict]:
        """Deconstruct ideas into components"""
        components = []
        for idea in ideas:
            # Simple deconstruction: extract key concepts
            words = idea.lower().split()
            concepts = [w for w in words if len(w) > 4]
            components.append({"idea": idea, "concepts": concepts[:5]})
        return components
    
    def _cross_pollinate(self, components: List[dict], domains: List[str]) -> List[dict]:
        """Cross-pollinate with other domains"""
        cross_results = []
        for component in components:
            # Find related domains
            related_domains = []
            for domain in domains:
                if domain != component["domain"]:
                    related_domains.append(domain)
            
            # Create cross-domain combinations
            if related_domains:
                cross_results.append({
                    "original": component,
                    "cross_domains": related_domains,
                    "potential_combinations": len(related_domains) * len(component.get("concepts", []))
                })
        return cross_results
    
    def _reconstruct_connections(self, cross_results: List[dict]) -> List[str]:
        """Reconstruct with new connections"""
        new_connections = []
        for cross in cross_results:
            original = cross["original"]
            concepts = original.get("concepts", [])
            domains = cross["cross_domains"]
            
            # Create new connection ideas
            for concept in concepts[:2]:
                for domain in domains[:2]:
                    new_connection = f"{concept} × {domain}"
                    new_connections.append(new_connection)
        
        return new_connections[:10]
    
    def _extract_output_ideas(self) -> List[str]:
        """Extract final output ideas"""
        return self._reconstruct_connections(self._cross_pollinate(
            self._deconstruct_ideas(self.idea_pool[:5]),
            list(self.cross_domain_mappings.keys())
        ))
    
    def _calculate_creativity_score(self, ideas: List[str], domains: List[str]) -> float:
        """Calculate creativity score"""
        if not ideas or not domains:
            return 0.0
        
        # Base score from idea diversity
        unique_words = set()
        for idea in ideas:
            unique_words.update(idea.lower().split())
        
        # Domain diversity bonus
        domain_diversity = len(set(d.lower() for d in domains))
        
        # Calculate score
        word_diversity = len(unique_words) / 10.0
        domain_bonus = domain_diversity * 0.1
        
        score = 0.3 + (word_diversity * 0.3) + domain_bonus
        return min(1.0, score)
    
    def brainstorm_session(self, topic: str, duration: int = 5, participants: int = 4) -> dict:
        """Simulate a brainstorming session"""
        session = {
            "topic": topic,
            "duration": duration,
            "participants": participants,
            "ideas_generated": [],
            "process": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Simulate idea generation
        for i in range(participants * 3):
            idea = self._generate_brainstorm_idea(topic, i)
            session["ideas_generated"].append(idea)
            session["process"].append({
                "iteration": i,
                "idea": idea,
                "type": random.choice(["free_association", "forced_connection", "reverse_thinking"])
            })
        
        # Cluster similar ideas
        clusters = self._cluster_ideas(session["ideas_generated"])
        session["clusters"] = clusters
        
        return session
    
    def _generate_brainstorm_idea(self, topic: str, seed: int) -> str:
        """Generate a brainstorm idea"""
        modifiers = [
            "Consider", "Imagine", "What if", "How might", "Explore",
            "Connect", "Combine", "Transform", "Reverse", "Expand"
        ]
        
        connectors = [
            "with", "to", "and", "or", "through", "beyond", "within"
        ]
        
        base = random.choice(modifiers) + " " + topic
        connector = random.choice(connectors)
        modifier = random.choice(modifiers)
        
        return f"{base} {connector} {modifier} {topic}"
    
    def _cluster_ideas(self, ideas: List[str]) -> List[dict]:
        """Cluster similar ideas"""
        if not ideas:
            return []
        
        clusters = []
        current_cluster = [ideas[0]]
        
        for idea in ideas[1:]:
            # Simple clustering by first word
            first_word = ideas[0].lower().split()[0] if ideas else ""
            current_first = idea.lower().split()[0] if idea else ""
            
            if first_word == current_first:
                current_cluster.append(idea)
            else:
                if current_cluster:
                    clusters.append({
                        "cluster_id": len(clusters),
                        "size": len(current_cluster),
                        "ideas": current_cluster
                    })
                current_cluster = [idea]
        
        if current_cluster:
            clusters.append({
                "cluster_id": len(clusters),
                "size": len(current_cluster),
                "ideas": current_cluster
            })
        
        return clusters
    
    def export_synthesis_data(self) -> str:
        """Export synthesis data to JSON"""
        data = {
            "idea_pool": self.idea_pool,
            "cross_domain_mappings": self.cross_domain_mappings,
            "synthesis_history": self.synthesis_history[-50:],
            "timestamp": datetime.now().isoformat()
        }
        with open(self.synth_path / "synthesis_data.json", 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return f"Exported data for {len(self.idea_pool)} ideas"

# Global instance
creative_synthesis = CreativeSynthesis()