"""
Humor Module - Jokes, puns, and comedic timing
"""

import random
import re
from typing import Dict, List, Optional

class Humor:
    """
    Generates jokes, puns, and handles comedic timing
    """
    
    def __init__(self):
        # Joke database
        self.jokes = {
            'dad': [
                "Why don't scientists trust atoms? Because they make up everything!",
                "What do you call a fake noodle? An impasta!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "How does a penguin build its house? Igloos it together!",
                "Why don't skeletons fight each other? They don't have the guts!",
                "What do you call a bear with no teeth? A gummy bear!",
                "Why can't you give Elsa a balloon? Because she will let it go!",
                "How do you make holy water? You boil the hell out of it!",
                "What do you call a fish wearing a bowtie? Sofishticated!",
                "Why did the bicycle fall over? Because it was two tired!"
            ],
            'pun': [
                "I'm reading a book on anti-gravity. It's impossible to put down!",
                "I used to be a baker, but I couldn't make enough dough.",
                "I'm terrified of elevators. I'm going to start taking steps to avoid them.",
                "I don't trust stairs. They're always up to something.",
                "I told my wife she should embrace her mistakes. She gave me a hug.",
                "I'm friends with all 26 letters. We go way back.",
                "I can't believe I got fired from the calendar factory. All I did was take a day off!",
                "I'm reading a book about mazes. I got lost in it.",
                "I used to play piano by ear, but now I use my hands.",
                "I don't play soccer because I enjoy the sport. I just do it for kicks!"
            ],
            'nerd': [
                "There are 10 types of people in the world: those who understand binary, and those who don't.",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "A SQL query goes into a bar, walks up to two tables and asks, 'Can I join you?'",
                "I would tell you a UDP joke, but you might not get it.",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
                "I'm not arguing, I'm just explaining why I'm right. There's a difference.",
                "Artificial intelligence is no match for natural stupidity.",
                "The best thing about a Boolean is even if you're wrong, you're only off by a bit.",
                "I'd tell you a joke about AI, but I'm still training it.",
                "There's no place like 127.0.0.1"
            ],
            'knock_knock': [
                "Knock knock. Who's there? Lettuce. Lettuce who? Lettuce in, it's cold out here!",
                "Knock knock. Who's there? Tank. Tank who? You're welcome!",
                "Knock knock. Who's there? Cow says. Cow says who? No, cow says moooo!",
                "Knock knock. Who's there? Interrupting cow. Interrupting cow wh- MOO!",
                "Knock knock. Who's there? Hawaii. Hawaii who? I'm fine, Hawaii you?"
            ],
            'dark': [
                "I have a joke about trickle-down economics, but 99% of it never reaches you.",
                "My therapist said time heals all wounds. So I stabbed him. Now we wait.",
                "I told my computer I needed a break, and now it won't stop sending me vacation ads.",
                "I'm not saying I'm Batman, but have you ever seen me and Batman in the same room?",
                "I asked God for a bike, but I know God doesn't work that way. So I stole a bike and asked for forgiveness."
            ]
        }
        
        # Pun word patterns
        self.pun_patterns = [
            (r'\bcomputer\b', 'comput-her'),
            (r'\bprogramming\b', 'program-ming'),
            (r'\bpython\b', 'pie-thon'),
            (r'\bjava\b', 'ja-va-va-voom'),
            (r'\bartificial\b', 'arti-fish-al'),
            (r'\bintelligence\b', 'in-tea-ligence'),
            (r'\bdata\b', 'day-ta or dah-ta?'),
            (r'\bcloud\b', 'clod'),
            (r'\bnetwork\b', 'net-work-out'),
            (r'\bdebug\b', 'de-bug')
        ]
        
        # Comedic timing modifiers
        self.timing_modifiers = [
            " *pauses for effect* ",
            " ... ",
            " Wait for it... ",
            " *drumroll* ",
            " *ba-dum-tss* ",
            " ... get it? ",
            " *rimshot* "
        ]
    
    def tell_joke(self, category: str = None) -> str:
        """
        Tell a random joke
        """
        if category and category in self.jokes:
            return random.choice(self.jokes[category])
        else:
            all_jokes = []
            for cat in self.jokes:
                all_jokes.extend(self.jokes[cat])
            return random.choice(all_jokes)
    
    def make_pun(self, text: str) -> str:
        """
        Create a pun based on input
        """
        text_lower = text.lower()
        
        for pattern, pun in self.pun_patterns:
            if re.search(pattern, text_lower):
                # Replace with pun
                return re.sub(pattern, pun, text, flags=re.IGNORECASE)
        
        # Default puns if no match
        puns = [
            f"That's what {random.choice(['she', 'he', 'they'])} said!",
            f"I'm {random.choice(['board', 'tired', 'hungry'])} of that joke.",
            f"That's a-{random.choice(['mazing', 'wesome', 'dorable'])}!",
            f"I {random.choice(['sea', 'see', 'c'])} what you did there."
        ]
        return random.choice(puns)
    
    def add_comedic_timing(self, text: str, intensity: float = 0.3) -> str:
        """
        Add comedic timing to text
        """
        if random.random() < intensity:
            # Add pause somewhere
            words = text.split()
            if len(words) > 3:
                pos = random.randint(1, len(words) - 2)
                words.insert(pos, random.choice(self.timing_modifiers))
                return ' '.join(words)
        return text
    
    def rate_joke(self, joke: str) -> int:
        """
        Rate how funny a joke is (1-10)
        """
        score = 5  # Base score
        
        # Length factor
        if len(joke) < 30:
            score += 1  # Short jokes are often funnier
        elif len(joke) > 100:
            score -= 1  # Too long
        
        # Punctuation factor
        if '!' in joke:
            score += 1
        if '?' in joke:
            score += 1
        
        # Wordplay factor
        wordplay_indicators = ['like', 'because', 'so', 'but', 'get it']
        if any(ind in joke.lower() for ind in wordplay_indicators):
            score += 1
        
        return max(1, min(10, score))
    
    def get_joke_categories(self) -> List[str]:
        """
        Get available joke categories
        """
        return list(self.jokes.keys())
    
    def joke_feedback(self, joke: str, liked: bool):
        """
        Learn from user feedback
        """
        # This would adjust joke weights in a more advanced implementation
        if liked:
            print("😊 User liked that joke!")
        else:
            print("😐 User didn't like that joke...")