"""
Poetry Generation - Create poems in various styles
"""

import random
import re
from typing import Dict, List, Optional

class PoetryGenerator:
    """
    Generates poetry in various forms and styles
    """
    
    def __init__(self):
        self.poetic_forms = {
            'sonnet': {'lines': 14, 'rhyme': 'ababcdcdefefgg'},
            'haiku': {'lines': 3, 'syllables': [5, 7, 5]},
            'limerick': {'lines': 5, 'rhyme': 'aabba'},
            'villanelle': {'lines': 19, 'rhyme': 'aba aba aba aba aba abaa'},
            'acrostic': {'lines': 'variable', 'first_letter': True},
            'free_verse': {'lines': 'variable', 'rhyme': None}
        }
        
        self.themes = [
            'love', 'nature', 'time', 'death', 'beauty', 'sorrow',
            'joy', 'dreams', 'stars', 'ocean', 'forest', 'solitude',
            'friendship', 'memory', 'hope', 'despair', 'dawn', 'dusk'
        ]
        
        self.adjectives = [
            'gentle', 'wild', 'silent', 'golden', 'crimson', 'azure',
            'mystic', 'ancient', 'eternal', 'fleeting', 'tender', 'fierce',
            'luminous', 'shadowy', 'whispering', 'thundering', 'peaceful'
        ]
        
        self.nouns = [
            'heart', 'soul', 'dream', 'star', 'moon', 'sun', 'wind',
            'fire', 'water', 'earth', 'light', 'shadow', 'time', 'love',
            'hope', 'fear', 'memory', 'silence', 'whisper', 'echo'
        ]
        
        self.verbs = [
            'whispers', 'dances', 'shines', 'fades', 'dreams', 'flows',
            'burns', 'flies', 'sings', 'cries', 'laughs', 'weeps',
            'soars', 'drifts', 'wanders', 'returns', 'remembers'
        ]
        
    def generate_poem(self, form: str = None, theme: str = None) -> Dict:
        """
        Generate a poem in specified form
        """
        if form is None:
            form = random.choice(list(self.poetic_forms.keys()))
        
        if theme is None:
            theme = random.choice(self.themes)
        
        poem = {
            'form': form,
            'theme': theme,
            'title': self._generate_title(theme),
            'lines': [],
            'structure': self.poetic_forms[form]
        }
        
        if form == 'haiku':
            poem['lines'] = self._generate_haiku(theme)
        elif form == 'sonnet':
            poem['lines'] = self._generate_sonnet(theme)
        elif form == 'limerick':
            poem['lines'] = self._generate_limerick(theme)
        elif form == 'acrostic':
            poem['lines'] = self._generate_acrostic(theme)
        else:
            poem['lines'] = self._generate_free_verse(theme)
        
        return poem
    
    def _generate_title(self, theme: str) -> str:
        """Generate a poem title"""
        patterns = [
            f"Ode to {theme.title()}",
            f"The {random.choice(self.adjectives).title()} {theme.title()}",
            f"{theme.title()}'s {random.choice(self.nouns).title()}",
            f"Upon {random.choice(self.adjectives).title()} {theme.title()}",
            f"{random.choice(self.nouns).title()} of {theme.title()}"
        ]
        return random.choice(patterns)
    
    def _generate_line(self, theme: str, syllable_count: int = None) -> str:
        """Generate a poetic line"""
        patterns = [
            f"The {random.choice(self.adjectives)} {random.choice(self.nouns)} {random.choice(self.verbs)}",
            f"{random.choice(self.verbs).title()} through the {random.choice(self.adjectives)} {random.choice(self.nouns)}",
            f"{random.choice(self.nouns).title()} of {random.choice(self.adjectives)} {random.choice(self.nouns)}",
            f"{random.choice(self.adjectives).title()} {random.choice(self.nouns)} of {theme}",
            f"When {random.choice(self.nouns)} {random.choice(self.verbs)} like {random.choice(self.nouns)}"
        ]
        
        line = random.choice(patterns)
        
        # Rough syllable approximation
        if syllable_count:
            # Pad or trim to approximate syllable count (simplified)
            words = line.split()
            while len(words) < syllable_count // 2:
                words.append(random.choice(self.adjectives))
            line = ' '.join(words)
        
        return line
    
    def _generate_haiku(self, theme: str) -> List[str]:
        """Generate a haiku (5-7-5 syllables)"""
        lines = [
            self._generate_haiku_line(5, theme),
            self._generate_haiku_line(7, theme),
            self._generate_haiku_line(5, theme)
        ]
        return lines
    
    def _generate_haiku_line(self, syllables: int, theme: str) -> str:
        """Generate a haiku line with approximate syllables"""
        words = []
        current_syllables = 0
        
        # Start with theme word
        if theme in self.themes:
            words.append(theme)
            current_syllables += 2  # Approximate
        
        # Add words until we reach syllable count
        word_pools = [self.adjectives, self.nouns, self.verbs]
        while current_syllables < syllables:
            pool = random.choice(word_pools)
            word = random.choice(pool)
            words.append(word)
            current_syllables += 2  # Approximate
        
        return ' '.join(words[:syllables//2])
    
    def _generate_sonnet(self, theme: str) -> List[str]:
        """Generate a Shakespearean sonnet (14 lines)"""
        lines = []
        for i in range(14):
            line = self._generate_line(theme)
            # Add rhyme scheme (simplified)
            if i % 2 == 0:
                line = line.replace('.', ',')
            lines.append(line)
        return lines
    
    def _generate_limerick(self, theme: str) -> List[str]:
        """Generate a limerick"""
        lines = [
            f"There once was a {random.choice(self.adjectives)} {random.choice(self.nouns)} from {theme}",
            f"Whose {random.choice(self.nouns)} was terribly {random.choice(self.adjectives)}",
            f"They {random.choice(self.verbs)} all day",
            f"In a {random.choice(self.adjectives)} way",
            f"And {random.choice(self.verbs)} till the {random.choice(self.nouns)} was {random.choice(self.adjectives)}"
        ]
        return lines
    
    def _generate_acrostic(self, theme: str) -> List[str]:
        """Generate an acrostic poem"""
        word = theme.upper()
        lines = []
        
        for letter in word:
            lines.append(f"{letter} - {self._generate_acrostic_line(letter, theme)}")
        
        return lines
    
    def _generate_acrostic_line(self, letter: str, theme: str) -> str:
        """Generate a line starting with given letter"""
        words = [w for w in self.adjectives + self.nouns + self.verbs 
                if w[0].upper() == letter]
        
        if words:
            start_word = random.choice(words)
        else:
            start_word = letter
        
        return f"{start_word} {random.choice(self.nouns)} of {theme}"
    
    def _generate_free_verse(self, theme: str) -> List[str]:
        """Generate free verse poetry"""
        line_count = random.randint(4, 12)
        lines = []
        
        for _ in range(line_count):
            lines.append(self._generate_line(theme))
        
        return lines
    
    def analyze_poem(self, poem: Dict) -> Dict:
        """
        Analyze a poem's structure and style
        """
        lines = poem['lines']
        
        analysis = {
            'line_count': len(lines),
            'word_count': sum(len(line.split()) for line in lines),
            'avg_line_length': sum(len(line) for line in lines) / len(lines),
            'form': poem['form'],
            'theme': poem['theme']
        }
        
        # Rough rhyme detection (simplified)
        last_words = [line.split()[-1] if line.split() else '' for line in lines]
        analysis['unique_end_words'] = len(set(last_words))
        
        return analysis
    
    def get_poetic_forms(self) -> List[str]:
        """Get list of available poetic forms"""
        return list(self.poetic_forms.keys())