"""
Creative Writing - Poetry, stories, and creative text generation
"""

import random
import re
from typing import List, Dict, Optional

class CreativeWriter:
    """
    Generates creative text: poetry, stories, etc.
    """
    
    def __init__(self):
        self.poetry_patterns = {
            'haiku': (5, 7, 5),
            'sonnet': 14,
            'limerick': 5
        }
        
        self.rhyme_patterns = {
            'couplet': 'aa',
            'alternating': 'abab',
            'enclosed': 'abba',
            'sonnet': 'ababcdcdefefgg'
        }
        
        self.topics = [
            'love', 'nature', 'time', 'dreams', 'stars',
            'ocean', 'forest', 'mountains', 'city', 'solitude',
            'friendship', 'hope', 'fear', 'joy', 'sorrow'
        ]
        
        self.adjectives = [
            'beautiful', 'dark', 'bright', 'silent', 'endless',
            'gentle', 'wild', 'ancient', 'mysterious', 'golden'
        ]
        
        self.nouns = [
            'sky', 'heart', 'soul', 'night', 'day',
            'wind', 'fire', 'water', 'earth', 'light'
        ]
        
        self.verbs = [
            'whispers', 'dances', 'shines', 'fades', 'dreams',
            'flows', 'burns', 'flies', 'sings', 'cries'
        ]
    
    def generate_haiku(self, topic: str = None) -> str:
        """
        Generate a haiku (5-7-5 syllables)
        """
        if not topic:
            topic = random.choice(self.topics)
        
        lines = [
            self._generate_line(5, topic),
            self._generate_line(7, topic),
            self._generate_line(5, topic)
        ]
        
        return "\n".join(lines)
    
    def _generate_line(self, syllables: int, topic: str) -> str:
        """Generate a line with specific syllable count"""
        words = []
        current_syllables = 0
        
        # Start with topic-related word
        if topic and random.random() > 0.5:
            topic_word = topic
            topic_syllables = self._count_syllables(topic)
            if topic_syllables <= syllables:
                words.append(topic_word)
                current_syllables = topic_syllables
        
        # Fill remaining syllables
        word_pools = [self.adjectives, self.nouns, self.verbs]
        while current_syllables < syllables:
            pool = random.choice(word_pools)
            word = random.choice(pool)
            word_syllables = self._count_syllables(word)
            
            if current_syllables + word_syllables <= syllables:
                words.append(word)
                current_syllables += word_syllables
        
        return ' '.join(words)
    
    def _count_syllables(self, word: str) -> int:
        """Simple syllable counter"""
        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        
        if word and word[0] in vowels:
            count += 1
        
        for i in range(1, len(word)):
            if word[i] in vowels and word[i-1] not in vowels:
                count += 1
        
        if word.endswith('e'):
            count -= 1
        if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
            count += 1
        if count == 0:
            count = 1
        
        return count
    
    def generate_poem(self, lines: int = 4, rhyme_scheme: str = 'couplet') -> str:
        """
        Generate a rhyming poem
        """
        pattern = self.rhyme_patterns.get(rhyme_scheme, 'aa')
        poem_lines = []
        
        # Extend pattern to match number of lines
        while len(pattern) < lines:
            pattern += pattern
        
        pattern = pattern[:lines]
        
        # Generate rhyming words
        rhymes = self._generate_rhymes(set(pattern))
        
        for i in range(lines):
            rhyme_char = pattern[i]
            rhyme_word = rhymes.get(rhyme_char, 'light')
            
            line = self._generate_line(random.randint(6, 8), random.choice(self.topics))
            if random.random() > 0.7:  # Sometimes end with rhyme word
                line = line.rsplit(' ', 1)[0] + ' ' + rhyme_word
            
            poem_lines.append(line)
        
        return '\n'.join(poem_lines)
    
    def _generate_rhymes(self, rhyme_chars: set) -> Dict[str, str]:
        """Generate rhyming words for each character"""
        rhymes = {}
        rhyming_groups = [
            ['light', 'night', 'bright', 'sight'],
            ['day', 'way', 'say', 'play'],
            ['heart', 'part', 'start', 'smart'],
            ['soul', 'whole', 'goal', 'roll'],
            ['sky', 'fly', 'high', 'why'],
            ['sea', 'free', 'be', 'me'],
            ['dream', 'seem', 'stream', 'beam']
        ]
        
        for i, char in enumerate(rhyme_chars):
            group = random.choice(rhyming_groups)
            rhymes[char] = random.choice(group)
        
        return rhymes
    
    def generate_story(self, prompt: str = None, length: str = 'short') -> str:
        """
        Generate a short story
        """
        if not prompt:
            prompt = random.choice(self.topics)
        
        templates = {
            'short': [
                f"Once upon a time, there was a {random.choice(self.adjectives)} "
                f"{random.choice(self.nouns)}. It lived in a {random.choice(self.adjectives)} "
                f"land where {random.choice(self.verbs)} the {random.choice(self.nouns)}. "
                f"One day, everything changed when {prompt} appeared. "
                f"The {random.choice(self.nouns)} knew it had to {random.choice(self.verbs)}. "
                f"And so, the adventure began."
            ],
            'medium': [
                f"In the heart of the {random.choice(self.adjectives)} forest, "
                f"a {random.choice(self.nouns)} dreamed of {prompt}. "
                f"For years, it had {random.choice(self.verbs)} alone, "
                f"watching the {random.choice(self.nouns)} dance in the {random.choice(self.adjectives)} light. "
                f"But destiny had other plans. A {random.choice(self.adjectives)} visitor arrived, "
                f"bringing news of {prompt}. The journey would be {random.choice(self.adjectives)}. "
                f"The challenges {random.choice(self.adjectives)}. Yet something called to it. "
                f"With {random.choice(self.adjectives)} courage, it stepped forward into the unknown."
            ]
        }
        
        template = random.choice(templates.get(length, templates['short']))
        return template
    
    def generate_story_prompt(self) -> str:
        """Generate a writing prompt"""
        prompts = [
            f"Write about a {random.choice(self.adjectives)} {random.choice(self.nouns)} "
            f"that {random.choice(self.verbs)} at midnight",
            
            f"A story about {random.choice(self.topics)} set in a "
            f"{random.choice(self.adjectives)} world",
            
            f"The last {random.choice(self.nouns)} on Earth discovers "
            f"something {random.choice(self.adjectives)}",
            
            f"Describe a meeting between {random.choice(self.adjectives)} "
            f"{random.choice(self.nouns)} and {random.choice(self.adjectives)} "
            f"{random.choice(self.nouns)}",
            
            f"What happens when {random.choice(self.verbs)} becomes "
            f"the only way to survive?"
        ]
        
        return random.choice(prompts)