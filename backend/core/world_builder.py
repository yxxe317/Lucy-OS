# backend/core/world_builder.py
"""
AI World Builder & Narrative Simulator
Features 44 & 45
"""
import json
import asyncio
import random
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import logging

logger = logging.getLogger("WorldBuilder")

class WorldBuilder:
    """
    Creates entire fictional universes and simulates narratives
    """
    
    def __init__(self):
        self.worlds = {}
        self.narratives = {}
        
    async def create_world(self, prompt: str, complexity: str = "medium") -> Dict:
        """
        Feature 44: Generate entire fictional universe
        """
        world_id = hashlib.md5(f"{prompt}{datetime.now()}".encode()).hexdigest()[:12]
        
        # Generate world components
        world = {
            "id": world_id,
            "name": await self._generate_world_name(prompt),
            "created_at": datetime.now().isoformat(),
            "prompt": prompt,
            "physics": await self._generate_physics(complexity),
            "geography": await self._generate_geography(complexity),
            "civilizations": await self._generate_civilizations(complexity),
            "magic_system": await self._generate_magic_system() if "magic" in prompt.lower() else None,
            "technology_level": await self._generate_tech_level(prompt),
            "history": await self._generate_history(complexity),
            "key_characters": await self._generate_characters(5),
            "conflicts": await self._generate_conflicts(3),
            "rules": await self._generate_rules()
        }
        
        self.worlds[world_id] = world
        logger.info(f"🌍 Created world: {world['name']}")
        
        return world
    
    async def _generate_world_name(self, prompt: str) -> str:
        """Generate world name"""
        prefixes = ["Aethel", "Nyx", "Val", "Ara", "Mor", "Thal", "Xy", "Zyph"]
        suffixes = ["oria", "endor", "is", "an", "ar", "on", "ara", "ium"]
        return f"{random.choice(prefixes)}{random.choice(suffixes)}"
    
    async def _generate_physics(self, complexity: str) -> Dict:
        """Generate world physics"""
        return {
            "gravity": f"{random.uniform(0.5, 2.0):.1f}g",
            "time_flow": random.choice(["linear", "cyclical", "fragmented", "reversible"]),
            "elements": random.sample(["fire", "water", "earth", "air", "aether", "void", "light", "dark"], 4),
            "dimensionality": random.randint(3, 5),
            "special_rules": [
                f"Objects remember their {random.choice(['past', 'future', 'alternate'])} positions",
                f"Consciousness can exist in {random.choice(['multiple', 'any', 'all'])} places at once"
            ]
        }
    
    async def _generate_geography(self, complexity: str) -> Dict:
        """Generate world geography"""
        terrains = ["mountains", "forests", "deserts", "oceans", "jungles", "tundras", "volcanoes", "floating_islands"]
        return {
            "continents": random.randint(1, 5),
            "dominant_terrain": random.choice(terrains),
            "unique_locations": [
                f"The {random.choice(['Crystal', 'Floating', 'Sunken', 'Whispering'])} {random.choice(['Forest', 'City', 'Temple', 'Mountain'])}",
                f"The {random.choice(['Eternal', 'Shifting', 'Inverted'])} {random.choice(['Desert', 'Sea', 'Plains'])}"
            ],
            "climate_zones": random.sample(["tropical", "arctic", "temperate", "desert", "jungle"], 3),
            "map_style": random.choice(["archipelago", "supercontinent", "ringworld", "hollow"])
        }
    
    async def _generate_civilizations(self, complexity: str) -> List[Dict]:
        """Generate civilizations"""
        count = 3 if complexity == "low" else 5 if complexity == "medium" else 8
        civs = []
        
        for i in range(count):
            civ = {
                "name": f"Civ_{i}",
                "type": random.choice(["humanoid", "energy", "machine", "organic", "psychic"]),
                "tech_level": random.choice(["stone age", "medieval", "industrial", "space age", "post-singularity"]),
                "government": random.choice(["democracy", "empire", "hive mind", "anarchy", "theocracy"]),
                "population": random.randint(1000, 1000000) * 1000,
                "alignment": random.choice(["peaceful", "aggressive", "isolationist", "trading"])
            }
            civs.append(civ)
        
        return civs
    
    async def _generate_magic_system(self) -> Dict:
        """Generate magic system"""
        return {
            "source": random.choice(["internal", "external", "bloodline", "learned", "granted"]),
            "cost": random.choice(["energy", "memory", "life", "sanity", "time"]),
            "schools": random.sample(["elemental", "mind", "reality", "time", "space", "life", "death"], 4),
            "limitations": [
                f"Cannot affect {random.choice(['metal', 'water', 'truth'])}",
                f"Requires {random.choice(['sacrifice', 'concentration', 'belief'])}"
            ]
        }
    
    async def _generate_tech_level(self, prompt: str) -> str:
        """Determine technology level"""
        if "future" in prompt.lower() or "sci-fi" in prompt.lower():
            return random.choice(["faster-than-light", "post-singularity", "quantum", "nanotech"])
        elif "fantasy" in prompt.lower():
            return random.choice(["medieval", "renaissance", "steam", "magitech"])
        else:
            return random.choice(["industrial", "information age", "biopunk", "cyberpunk"])
    
    async def _generate_history(self, complexity: str) -> List[str]:
        """Generate world history"""
        events = []
        for i in range(random.randint(5, 10)):
            event = f"Year {i*1000}: {random.choice(['Great War', 'Discovery', 'Cataclysm', 'Golden Age', 'Invasion', 'Rebellion'])} of the {random.choice(['Dragons', 'Machines', 'Gods', 'Ancients'])}"
            events.append(event)
        return events
    
    async def _generate_characters(self, count: int) -> List[Dict]:
        """Generate key characters"""
        chars = []
        for i in range(count):
            char = {
                "name": f"Character_{i}",
                "role": random.choice(["protagonist", "antagonist", "mentor", "ally", "villain"]),
                "species": random.choice(["human", "elf", "dwarf", "alien", "AI", "ancient"]),
                "goal": f"Seeking {random.choice(['power', 'knowledge', 'revenge', 'peace', 'truth'])}",
                "fatal_flaw": random.choice(["pride", "greed", "fear", "doubt", "anger"])
            }
            chars.append(char)
        return chars
    
    async def _generate_conflicts(self, count: int) -> List[str]:
        """Generate world conflicts"""
        conflicts = []
        for i in range(count):
            conflict = f"{random.choice(['War', 'Struggle', 'Competition', 'Mystery'])} of the {random.choice(['Throne', 'Element', 'Dimension', 'Soul'])}"
            conflicts.append(conflict)
        return conflicts
    
    async def _generate_rules(self) -> List[str]:
        """Generate world rules"""
        return [
            f"All {random.choice(['magic', 'technology', 'consciousness'])} has a cost",
            f"{random.choice(['Time', 'Space', 'Memory'])} is {random.choice(['circular', 'fluid', 'malleable'])}",
            f"Every {random.randint(10, 100)} years, the {random.choice(['veil', 'barrier', 'reality'])} weakens"
        ]
    
    # ========== FEATURE 45: Narrative Simulator ==========
    
    async def simulate_narrative(self, premise: str, characters: List[Dict], length: str = "medium") -> Dict:
        """
        Simulate how a story would unfold
        """
        narrative_id = hashlib.md5(f"{premise}{datetime.now()}".encode()).hexdigest()[:12]
        
        # Generate plot points
        plot = await self._generate_plot(premise, characters, length)
        
        # Predict endings
        endings = await self._predict_endings(plot, characters)
        
        # Character arcs
        arcs = await self._generate_character_arcs(characters, plot)
        
        # Theme analysis
        themes = await self._analyze_themes(plot)
        
        narrative = {
            "id": narrative_id,
            "premise": premise,
            "plot": plot,
            "endings": endings,
            "character_arcs": arcs,
            "themes": themes,
            "probability_matrix": await self._generate_probability_matrix(plot)
        }
        
        self.narratives[narrative_id] = narrative
        logger.info(f"📖 Simulated narrative: {premise[:50]}...")
        
        return narrative
    
    async def _generate_plot(self, premise: str, characters: List[Dict], length: str) -> List[Dict]:
        """Generate plot points"""
        acts = 3 if length == "short" else 5 if length == "medium" else 7
        plot = []
        
        for act in range(acts):
            act_plot = {
                "act": act + 1,
                "name": f"Act {act + 1}: {random.choice(['Setup', 'Confrontation', 'Resolution', 'Twist', 'Climax'])}",
                "events": []
            }
            
            for event in range(random.randint(3, 5)):
                event_data = {
                    "scene": event + 1,
                    "location": random.choice(["forest", "city", "space", "temple", "void"]),
                    "event": f"Character {random.choice([c['name'] for c in characters])} discovers/encounters/faces {random.choice(['truth', 'enemy', 'ally', 'artifact', 'choice'])}",
                    "conflict": random.choice(["internal", "external", "philosophical", "physical"]),
                    "stakes": random.choice(["life", "world", "soul", "truth", "freedom"])
                }
                act_plot["events"].append(event_data)
            
            plot.append(act_plot)
        
        return plot
    
    async def _predict_endings(self, plot: List[Dict], characters: List[Dict]) -> List[Dict]:
        """Predict possible endings"""
        endings = []
        
        ending_types = [
            ("heroic", 0.3),
            ("tragic", 0.2),
            ("ambiguous", 0.2),
            ("twist", 0.15),
            ("philosophical", 0.15)
        ]
        
        for ending_type, probability in ending_types:
            ending = {
                "type": ending_type,
                "probability": probability,
                "description": f"In this ending, {random.choice([c['name'] for c in characters])} ultimately {random.choice(['succeeds', 'fails', 'transcends', 'sacrifices', 'understands'])}",
                "conditions": [
                    f"If character {random.randint(0, len(characters)-1)} chooses...",
                    f"If the {random.choice(['artifact', 'truth', 'power'])} is..."
                ]
            }
            endings.append(ending)
        
        return endings
    
    async def _generate_character_arcs(self, characters: List[Dict], plot: List[Dict]) -> List[Dict]:
        """Generate character development arcs"""
        arcs = []
        for char in characters:
            arc = {
                "character": char["name"],
                "starting_point": char.get("role", "unknown"),
                "change": random.choice(["positive", "negative", "complex"]),
                "key_moments": [
                    f"Act {random.randint(1, 3)}: Realization about {random.choice(['self', 'world', 'others'])}",
                    f"Act {random.randint(3, 5)}: Choice between {random.choice(['duty and desire', 'truth and comfort', 'power and morality'])}"
                ],
                "ending_state": random.choice(["transformed", "destroyed", "elevated", "enlightened"])
            }
            arcs.append(arc)
        return arcs
    
    async def _analyze_themes(self, plot: List[Dict]) -> List[str]:
        """Analyze story themes"""
        all_themes = [
            "redemption", "sacrifice", "love", "death", "identity",
            "power", "knowledge", "freedom", "justice", "revenge",
            "humanity", "consciousness", "reality", "time", "purpose"
        ]
        return random.sample(all_themes, 4)
    
    async def _generate_probability_matrix(self, plot: List[Dict]) -> Dict:
        """Generate probability matrix for different outcomes"""
        return {
            "survival_rate": random.uniform(0.3, 0.9),
            "success_probability": random.uniform(0.2, 0.8),
            "twist_probability": random.uniform(0.1, 0.4),
            "sequel_probability": random.uniform(0.3, 0.7)
        }

# Global instance
world_builder = WorldBuilder()