"""
Game Design - Generate game concepts and mechanics
"""

import random
from typing import Dict, List, Optional

class GameDesigner:
    """
    Generates game design concepts and mechanics
    """
    
    def __init__(self):
        self.genres = [
            'RPG', 'FPS', 'Platformer', 'Puzzle', 'Strategy', 
            'Simulation', 'Adventure', 'Roguelike', 'Battle Royale',
            'MOBA', 'Racing', 'Fighting', 'Stealth', 'Survival',
            'Horror', 'Sandbox', 'MMO', 'Card Game', 'Rhythm'
        ]
        
        self.themes = [
            'fantasy', 'sci-fi', 'post-apocalyptic', 'cyberpunk', 'steampunk',
            'medieval', 'ancient', 'modern', 'horror', 'mythology',
            'space opera', 'dystopian', 'superhero', 'western', 'pirate'
        ]
        
        self.mechanics = [
            'turn-based combat', 'real-time combat', 'crafting', 'building',
            'exploration', 'puzzle solving', 'stealth', 'parkour',
            'resource management', 'base building', 'skill trees', 'perks',
            'multiplayer', 'co-op', 'PvP', 'trading', 'faction system'
        ]
        
        self.art_styles = [
            'pixel art', 'low-poly 3D', 'realistic 3D', 'hand-drawn 2D',
            'cel-shaded', 'voxel', 'vector art', 'minimalist', 'cartoon'
        ]
        
        self.platforms = [
            'PC', 'PlayStation', 'Xbox', 'Nintendo Switch', 'Mobile',
            'VR', 'Web Browser', 'Cross-platform'
        ]
    
    def generate_game_concept(self) -> Dict:
        """
        Generate a complete game concept
        """
        concept = {
            'title': self._generate_title(),
            'tagline': self._generate_tagline(),
            'genre': random.choice(self.genres),
            'theme': random.choice(self.themes),
            'core_mechanics': self._generate_mechanics(3),
            'art_style': random.choice(self.art_styles),
            'platforms': random.sample(self.platforms, random.randint(1, 3)),
            'target_audience': self._generate_audience(),
            'unique_selling_point': self._generate_usp(),
            'estimated_development_time': random.choice(['6 months', '1 year', '2 years', '3+ years']),
            'team_size': random.randint(1, 50)
        }
        return concept
    
    def _generate_title(self) -> str:
        """Generate a game title"""
        prefixes = ['The', 'Chronicles of', 'Legends of', 'Rise of', 'Fall of',
                   'Echoes of', 'Realm of', 'Age of', 'Quest for', 'Tales of']
        nouns = ['Darkness', 'Light', 'Dragons', 'Empire', 'Souls', 'Stars',
                'Destiny', 'Fate', 'Legends', 'Heroes', 'Void', 'Infinity']
        suffixes = ['Warrior', 'Mage', 'Knight', 'Chronicles', 'Saga', 'Odyssey']
        
        if random.random() > 0.5:
            return f"{random.choice(prefixes)} {random.choice(nouns)}"
        else:
            return f"{random.choice(nouns)} {random.choice(suffixes)}"
    
    def _generate_tagline(self) -> str:
        """Generate a tagline"""
        taglines = [
            "Survive the darkness",
            "Forge your destiny",
            "The end is just the beginning",
            "Your choices matter",
            "Unleash your power",
            "Explore infinite worlds",
            "The ultimate adventure awaits",
            "Face your fears",
            "Build your legacy"
        ]
        return random.choice(taglines)
    
    def _generate_mechanics(self, count: int) -> List[str]:
        """Generate core mechanics"""
        return random.sample(self.mechanics, min(count, len(self.mechanics)))
    
    def _generate_audience(self) -> str:
        """Generate target audience"""
        audiences = ['Casual gamers', 'Hardcore gamers', 'All ages', 'Teens and adults',
                    'Strategy enthusiasts', 'RPG fans', 'Competitive players',
                    'Story-driven players', 'Co-op fans']
        return random.choice(audiences)
    
    def _generate_usp(self) -> str:
        """Generate unique selling point"""
        usps = [
            f"Revolutionary {random.choice(self.mechanics)} system",
            f"Procedurally generated {random.choice(self.themes)} world",
            f"Deep {random.choice(self.mechanics)} mechanics",
            f"Branching narrative with {random.randint(3, 10)} endings",
            f"Cross-platform multiplayer",
            f"Unique {random.choice(self.art_styles)} art style",
            f"Modular character creation",
            f"Dynamic {random.choice(self.themes)} ecosystem"
        ]
        return random.choice(usps)
    
    def generate_character_class(self) -> Dict:
        """Generate an RPG character class"""
        classes = [
            {
                'name': 'Warrior',
                'primary_stat': 'Strength',
                'abilities': ['Power Strike', 'Shield Block', 'Whirlwind'],
                'role': 'Tank/Damage'
            },
            {
                'name': 'Mage',
                'primary_stat': 'Intelligence',
                'abilities': ['Fireball', 'Frost Nova', 'Teleport'],
                'role': 'Ranged Damage'
            },
            {
                'name': 'Rogue',
                'primary_stat': 'Dexterity',
                'abilities': ['Backstab', 'Stealth', 'Poison'],
                'role': 'Assassin'
            },
            {
                'name': 'Cleric',
                'primary_stat': 'Wisdom',
                'abilities': ['Heal', 'Bless', 'Smite'],
                'role': 'Support/Healer'
            }
        ]
        return random.choice(classes)
    
    def generate_quest(self) -> Dict:
        """Generate a quest"""
        quest_types = ['Main Story', 'Side Quest', 'Faction Quest', 'Random Encounter',
                       'Boss Battle', 'Escort Mission', 'Delivery', 'Investigation']
        
        objectives = ['defeat', 'collect', 'escort', 'find', 'deliver', 'protect',
                     'investigate', 'rescue', 'activate', 'destroy']
        
        targets = ['boss', 'artifact', 'NPC', 'location', 'item', 'enemy camp',
                  'dungeon', 'ancient ruins', 'forgotten temple']
        
        return {
            'title': f"{random.choice(objectives).title()} the {random.choice(targets)}",
            'type': random.choice(quest_types),
            'objective': f"{random.choice(objectives)} {random.choice(targets)}",
            'reward': f"{random.randint(100, 1000)} gold",
            'location': self._generate_location()
        }
    
    def _generate_location(self) -> str:
        """Generate a location name"""
        prefixes = ['Dark', 'Misty', 'Forgotten', 'Ancient', 'Cursed', 'Sacred',
                   'Sunken', 'Floating', 'Hidden', 'Lost']
        suffixes = ['Forest', 'Mountains', 'Swamp', 'Desert', 'Ruins', 'Temple',
                   'Castle', 'Cave', 'City', 'Island', 'Valley']
        
        return f"{random.choice(prefixes)} {random.choice(suffixes)}"
    
    def generate_enemy(self) -> Dict:
        """Generate an enemy type"""
        enemy_types = ['Goblin', 'Orc', 'Dragon', 'Skeleton', 'Zombie', 'Vampire',
                      'Werewolf', 'Demon', 'Elemental', 'Giant', 'Troll', 'Golem']
        
        return {
            'name': random.choice(enemy_types),
            'health': random.randint(50, 500),
            'damage': random.randint(5, 50),
            'difficulty': random.choice(['Easy', 'Medium', 'Hard', 'Boss']),
            'loot': ['gold', 'potion', 'weapon', 'armor', 'artifact']
        }