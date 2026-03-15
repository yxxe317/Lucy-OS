"""
Story Generation - Create narratives and plots
"""

import random
from typing import Dict, List, Optional

class StoryGenerator:
    """
    Generates stories, plots, and narratives
    """
    
    def __init__(self):
        self.genres = [
            'fantasy', 'sci-fi', 'mystery', 'romance', 'thriller',
            'horror', 'adventure', 'drama', 'comedy', 'historical',
            'western', 'cyberpunk', 'steampunk', 'mythology', 'fairy tale'
        ]
        
        self.adjectives = [
            'brave', 'cunning', 'wise', 'foolish', 'kind', 'cruel',
            'mysterious', 'ancient', 'forgotten', 'sacred', 'cursed',
            'magical', 'dark', 'light', 'shadowy', 'golden', 'silver'
        ]
        
        self.nouns = [
            'kingdom', 'prophecy', 'secret', 'legend', 'quest',
            'sword', 'crown', 'throne', 'dragon', 'castle',
            'forest', 'mountain', 'ocean', 'star', 'shadow'
        ]
        
        self.protagonists = [
            'a young hero', 'an unlikely champion', 'a grizzled veteran',
            'a naive dreamer', 'a cynical detective', 'a brave warrior',
            'a clever thief', 'a wise mentor', 'a fallen star', 'an ordinary person'
        ]
        
        self.antagonists = [
            'a dark lord', 'a corrupt corporation', 'an ancient evil',
            'a rival', 'a natural disaster', 'the protagonist themselves',
            'a secret society', 'a vengeful ghost', 'an AI gone rogue'
        ]
        
        self.settings = [
            'a fantasy kingdom', 'a dystopian city', 'a space station',
            'a small town', 'an ancient temple', 'a parallel dimension',
            'the wild west', 'a magical academy', 'a post-apocalyptic wasteland',
            'a virtual reality world', 'an underwater city', 'a floating island'
        ]
        
        self.plot_twists = [
            'the mentor was the villain all along',
            'the hero discovers they are the chosen one',
            'it was all a dream',
            'the world is actually a simulation',
            'the protagonist is the reincarnation of a legendary hero',
            'the villain is the hero from the future',
            'the sidekick saves the day',
            'the prophecy was misinterpreted'
        ]
        
        self.themes = [
            'redemption', 'sacrifice', 'love conquers all', 'power corrupts',
            'coming of age', 'man vs nature', 'man vs self', 'man vs society',
            'the hero\'s journey', 'forbidden love', 'revenge', 'forgiveness'
        ]
        
    def generate_story(self, genre: str = None, length: str = 'medium') -> Dict:
        """
        Generate a complete story outline
        """
        if genre is None:
            genre = random.choice(self.genres)
        
        story = {
            'title': self._generate_title(genre),
            'genre': genre,
            'length': length,
            'protagonist': random.choice(self.protagonists),
            'antagonist': random.choice(self.antagonists),
            'setting': random.choice(self.settings),
            'theme': random.choice(self.themes),
            'plot_twist': random.choice(self.plot_twists),
            'logline': self._generate_logline(),
            'acts': self._generate_acts(length)
        }
        
        return story
    
    def _generate_title(self, genre: str) -> str:
        """Generate a story title"""
        templates = [
            f"The {random.choice(['Last', 'First', 'Secret', 'Lost', 'Dark'])} "
            f"{random.choice(['Kingdom', 'Prophecy', 'Secret', 'Legend', 'Quest'])}",
            
            f"{random.choice(['Chronicles', 'Tales', 'Legend', 'Saga'])} of "
            f"{random.choice(['the Ancients', 'Forgotten Times', 'a Hero', 'Magic'])}",
            
            f"{random.choice(self.adjectives).title()} {random.choice(self.nouns).title()}",
            
            f"The {random.choice(self.adjectives).title()} {random.choice(self.nouns).title()}"
        ]
        return random.choice(templates)
    
    def _generate_logline(self) -> str:
        """Generate a one-sentence story summary"""
        templates = [
            f"A {random.choice(self.protagonists)} must {random.choice(['defeat', 'find', 'protect'])} "
            f"{random.choice(['the', 'a'])} {random.choice(self.antagonists)} to save "
            f"{random.choice(['the world', 'their people', 'everything', 'their loved ones'])}.",
            
            f"In {random.choice(self.settings)}, a {random.choice(self.protagonists)} discovers "
            f"that {random.choice(self.plot_twists)}.",
            
            f"After {random.choice(['a tragedy', 'a discovery', 'a prophecy', 'an accident'])}, "
            f"a {random.choice(self.protagonists)} embarks on a journey of {random.choice(self.themes)}."
        ]
        return random.choice(templates)
    
    def _generate_acts(self, length: str) -> List[Dict]:
        """Generate story acts"""
        if length == 'short':
            acts = [
                {'act': 1, 'title': 'Setup', 'events': self._generate_events(2)},
                {'act': 2, 'title': 'Confrontation', 'events': self._generate_events(3)},
                {'act': 3, 'title': 'Resolution', 'events': self._generate_events(2)}
            ]
        elif length == 'medium':
            acts = [
                {'act': 1, 'title': 'Setup', 'events': self._generate_events(3)},
                {'act': 2, 'title': 'Rising Action', 'events': self._generate_events(4)},
                {'act': 3, 'title': 'Climax', 'events': self._generate_events(2)},
                {'act': 4, 'title': 'Falling Action', 'events': self._generate_events(2)},
                {'act': 5, 'title': 'Resolution', 'events': self._generate_events(2)}
            ]
        else:  # long
            acts = [
                {'act': 1, 'title': 'Setup', 'events': self._generate_events(4)},
                {'act': 2, 'title': 'Inciting Incident', 'events': self._generate_events(3)},
                {'act': 3, 'title': 'First Plot Point', 'events': self._generate_events(3)},
                {'act': 4, 'title': 'Midpoint', 'events': self._generate_events(4)},
                {'act': 5, 'title': 'Darkest Hour', 'events': self._generate_events(3)},
                {'act': 6, 'title': 'Climax', 'events': self._generate_events(2)},
                {'act': 7, 'title': 'Resolution', 'events': self._generate_events(2)}
            ]
        
        return acts
    
    def _generate_events(self, count: int) -> List[str]:
        """Generate story events"""
        events = []
        for _ in range(count):
            events.append(self._generate_event())
        return events
    
    def _generate_event(self) -> str:
        """Generate a single story event"""
        templates = [
            f"The protagonist discovers {random.choice(['a secret', 'a clue', 'the truth', 'an ally'])}.",
            f"A conflict arises with {random.choice(['the antagonist', 'a rival', 'an obstacle', 'nature itself'])}.",
            f"A {random.choice(['revelation', 'betrayal', 'twist', 'miracle'])} changes everything.",
            f"The protagonist {random.choice(['trains', 'gathers allies', 'prepares', 'doubts'])}.",
            f"An unexpected {random.choice(['ally', 'enemy', 'event', 'discovery'])} appears.",
            f"{random.choice(['Emotional', 'Physical', 'Mental', 'Spiritual'])} challenge tests the hero."
        ]
        return random.choice(templates)
    
    def generate_character(self) -> Dict:
        """Generate a character profile"""
        return {
            'name': self._generate_name(),
            'role': random.choice(['protagonist', 'antagonist', 'sidekick', 'mentor', 'love interest']),
            'personality': random.choice(['brave', 'cowardly', 'wise', 'foolish', 'kind', 'cruel']),
            'goal': random.choice(['survival', 'power', 'love', 'revenge', 'knowledge', 'peace']),
            'flaw': random.choice(['pride', 'greed', 'fear', 'anger', 'doubt', 'vanity']),
            'backstory': self._generate_backstory()
        }
    
    def _generate_name(self) -> str:
        """Generate a character name"""
        first_names = ['Aria', 'Eldrin', 'Lyra', 'Thorne', 'Zephyr', 'Morgan', 'Sylas',
                      'Rowan', 'Elara', 'Kael', 'Mira', 'Dorian', 'Seraphina', 'Cassius']
        last_names = ['Stormborn', 'Shadowmere', 'Brightwood', 'Darkholme', 'Ironheart',
                     'Silverstream', 'Blackwood', 'Firebrand', 'Winterfell']
        
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _generate_backstory(self) -> str:
        """Generate a character backstory"""
        origins = [
            f"Born in {random.choice(['a royal family', 'poverty', 'a magical realm', 'exile'])}",
            f"Survived {random.choice(['a tragedy', 'a war', 'a plague', 'an accident'])}",
            f"Found {random.choice(['by a mentor', 'in the wild', 'with a destiny', 'alone'])}",
            f"Chosen by {random.choice(['fate', 'prophecy', 'the gods', 'circumstance'])}"
        ]
        return random.choice(origins)
    
    def generate_dialogue(self, character1: str, character2: str, situation: str) -> List[str]:
        """Generate dialogue between characters"""
        lines = []
        
        templates = [
            f"{character1}: I can't believe we have to {situation}.",
            f"{character2}: Neither can I, but we don't have a choice.",
            f"{character1}: There's always a choice.",
            f"{character2}: Is there? {situation} isn't exactly optional.",
            f"{character1}: Fine. But when this is over, you owe me.",
            f"{character2}: Deal. Now let's focus."
        ]
        
        return random.sample(templates, random.randint(3, 6))