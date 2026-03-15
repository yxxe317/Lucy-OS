"""
Art Generation - Create visual art descriptions and concepts
"""

import random
from typing import Dict, List, Optional

class ArtGenerator:
    """
    Generates art concepts and descriptions
    """
    
    def __init__(self):
        self.styles = [
            'impressionism', 'cubism', 'surrealism', 'abstract', 'renaissance',
            'baroque', 'pop art', 'minimalism', 'expressionism', 'art nouveau',
            'cyberpunk', 'steampunk', 'vaporwave', 'synthwave', 'glitch art'
        ]
        
        self.subjects = [
            'landscape', 'portrait', 'cityscape', 'still life', 'abstract composition',
            'mythological scene', 'historical event', 'dream sequence', 'space scene',
            'underwater world', 'fantasy realm', 'post-apocalyptic wasteland',
            'cybernetic future', 'alien planet', 'magical forest'
        ]
        
        self.colors = [
            'vibrant', 'muted', 'monochrome', 'pastel', 'neon', 'earth tones',
            'primary colors', 'complementary', 'analogous', 'triadic', 'warm', 'cool'
        ]
        
        self.moods = [
            'serene', 'chaotic', 'melancholic', 'joyful', 'mysterious', 'dramatic',
            'peaceful', 'tense', 'dreamy', 'energetic', 'calm', 'ominous'
        ]
        
        self.techniques = [
            'oil painting', 'watercolor', 'charcoal sketch', 'digital painting',
            'pixel art', 'vector graphics', 'collage', 'mixed media', 'photography',
            '3D rendering', 'generative art', 'AI-generated'
        ]
        
    def generate_art_concept(self) -> Dict:
        """
        Generate a random art concept
        """
        concept = {
            'title': self._generate_title(),
            'style': random.choice(self.styles),
            'subject': random.choice(self.subjects),
            'color_scheme': random.choice(self.colors),
            'mood': random.choice(self.moods),
            'technique': random.choice(self.techniques),
            'description': self._generate_description(),
            'composition': self._generate_composition()
        }
        return concept
    
    def _generate_title(self) -> str:
        """Generate a creative title"""
        prefixes = ['The', 'Dream of', 'Echoes of', 'Reflections on', 'Memories of',
                   'Visions of', 'Study in', 'Variations on', 'Homage to', 'After']
        nouns = ['Light', 'Shadow', 'Time', 'Space', 'Consciousness', 'Memory',
                'Infinity', 'Chaos', 'Order', 'Nature', 'Technology', 'Spirit']
        
        return f"{random.choice(prefixes)} {random.choice(nouns)}"
    
    def _generate_description(self) -> str:
        """Generate an art description"""
        templates = [
            f"A {random.choice(self.moods)} {random.choice(self.styles)} "
            f"{random.choice(self.subjects)} using {random.choice(self.colors)} colors.",
            
            f"This piece explores the intersection of {random.choice(self.subjects)} "
            f"and {random.choice(self.styles)} through {random.choice(self.techniques)}.",
            
            f"Drawing inspiration from {random.choice(self.styles)}, this work "
            f"evokes a sense of {random.choice(self.moods)} {random.choice(self.moods)}."
        ]
        return random.choice(templates)
    
    def _generate_composition(self) -> str:
        """Generate composition description"""
        compositions = [
            "asymmetrical balance with a focal point in the upper third",
            "symmetrical arrangement with strong vertical elements",
            "dynamic diagonal lines creating movement",
            "circular composition drawing the eye inward",
            "grid-based structure with repeating patterns",
            "radial composition emanating from the center",
            "rule of thirds with multiple focal points"
        ]
        return random.choice(compositions)
    
    def generate_art_critique(self, style: str = None) -> str:
        """Generate an art critique"""
        if style is None:
            style = random.choice(self.styles)
        
        praise = [
            f"masterful use of {random.choice(self.colors)} tones",
            f"exceptional handling of {random.choice(self.techniques)} technique",
            f"powerful emotional resonance through {random.choice(self.moods)} atmosphere",
            f"innovative approach to {random.choice(self.subjects)} composition"
        ]
        
        suggestions = [
            f"could explore more {random.choice(self.colors)} contrasts",
            f"might benefit from stronger {random.choice(self.composition)}",
            f"consider emphasizing the {random.choice(self.moods)} elements further",
            f"could push the {random.choice(self.styles)} aspects more"
        ]
        
        critique = f"This {style} piece demonstrates {random.choice(praise)}. "
        critique += f"The artist {random.choice(suggestions)}. "
        critique += f"Overall, it's a {random.choice(['compelling', 'thought-provoking', 'stunning', 'intriguing'])} work."
        
        return critique
    
    def generate_color_palette(self) -> List[str]:
        """Generate a color palette"""
        palettes = [
            ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
            ['#2C3E50', '#E74C3C', '#ECF0F1', '#3498DB', '#9B59B6'],
            ['#F39C12', '#D35400', '#C0392B', '#BDC3C7', '#27AE60'],
            ['#1ABC9C', '#2ECC71', '#3498DB', '#9B59B6', '#34495E'],
            ['#E67E22', '#E74C3C', '#ECF0F1', '#95A5A6', '#16A085']
        ]
        return random.choice(palettes)
    
    def get_art_movement_info(self, movement: str = None) -> Dict:
        """Get information about an art movement"""
        movements = {
            'impressionism': {
                'period': '1860s-1890s',
                'key_artists': ['Claude Monet', 'Pierre-Auguste Renoir', 'Edgar Degas'],
                'characteristics': ['visible brush strokes', 'open composition', 'light emphasis'],
                'masterpiece': 'Impression, Sunrise'
            },
            'cubism': {
                'period': '1907-1914',
                'key_artists': ['Pablo Picasso', 'Georges Braque', 'Juan Gris'],
                'characteristics': ['geometric shapes', 'multiple perspectives', 'fragmented forms'],
                'masterpiece': 'Les Demoiselles d\'Avignon'
            },
            'surrealism': {
                'period': '1920s-1950s',
                'key_artists': ['Salvador Dali', 'Rene Magritte', 'Max Ernst'],
                'characteristics': ['dreamlike scenes', 'unexpected juxtapositions', 'symbolism'],
                'masterpiece': 'The Persistence of Memory'
            }
        }
        
        if movement and movement in movements:
            return movements[movement]
        return random.choice(list(movements.values()))