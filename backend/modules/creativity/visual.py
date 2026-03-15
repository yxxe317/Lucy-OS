"""
Visual Arts - Generate visual art concepts and color schemes
"""

import random
from typing import Dict, List, Optional, Tuple

class VisualArtGenerator:
    """
    Generates visual art concepts, color palettes, and compositions
    """
    
    def __init__(self):
        self.art_movements = [
            'impressionism', 'cubism', 'surrealism', 'abstract expressionism',
            'pop art', 'minimalism', 'renaissance', 'baroque', 'rococo',
            'romanticism', 'realism', 'art nouveau', 'bauhaus', 'dadaism',
            'fauvism', 'pointillism', 'symbolism', 'futurism', 'constructivism'
        ]
        
        self.mediums = [
            'oil on canvas', 'watercolor', 'acrylic', 'charcoal', 'pastel',
            'digital', 'photography', 'mixed media', 'sculpture', 'collage',
            'fresco', 'tempera', 'gouache', 'ink', 'pencil', 'spray paint'
        ]
        
        self.subjects = [
            'landscape', 'portrait', 'still life', 'abstract', 'cityscape',
            'seascape', 'mythological', 'religious', 'historical', 'genre scene',
            'nude', 'animal', 'botanical', 'architectural', 'industrial'
        ]
        
        self.composition_types = [
            'rule of thirds', 'golden ratio', 'symmetrical', 'asymmetrical',
            'radial', 'triangular', 'diagonal', 'horizontal', 'vertical',
            'circular', 'grid-based', 'dynamic symmetry'
        ]
        
        self.color_schemes = [
            'monochromatic', 'complementary', 'analogous', 'triadic',
            'split-complementary', 'tetradic', 'square'
        ]
        
        self.color_scheme_descriptions = {
            'monochromatic': 'Single hue variations',
            'complementary': 'Opposite on color wheel',
            'analogous': 'Adjacent on color wheel',
            'triadic': 'Three evenly spaced colors',
            'split-complementary': 'Base plus two adjacent to complement',
            'tetradic': 'Two complementary pairs',
            'square': 'Four evenly spaced colors'
        }
        
        self.moods = [
            'serene', 'dramatic', 'melancholic', 'joyful', 'mysterious',
            'chaotic', 'peaceful', 'tense', 'dreamy', 'energetic', 'calm',
            'ominous', 'hopeful', 'nostalgic', 'romantic', 'powerful'
        ]
        
        # Color palettes (hex codes)
        self.palettes = {
            'sunset': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
            'ocean': ['#2C3E50', '#E74C3C', '#ECF0F1', '#3498DB', '#9B59B6'],
            'forest': ['#27AE60', '#2ECC71', '#F1C40F', '#E67E22', '#E74C3C'],
            'desert': ['#F39C12', '#D35400', '#C0392B', '#BDC3C7', '#27AE60'],
            'night': ['#1A1A2E', '#16213E', '#0F3460', '#E94560', '#533483'],
            'pastel': ['#FFD3B5', '#FFAAA5', '#FF8B94', '#A8E6CF', '#DCEDC1'],
            'vintage': ['#8B5A2B', '#C19A6B', '#E6B800', '#4A4A4A', '#8B4513'],
            'cyberpunk': ['#FF00FF', '#00FFFF', '#FFFF00', '#FF0000', '#00FF00'],
            'minimal': ['#FFFFFF', '#000000', '#CCCCCC', '#666666', '#333333']
        }
    
    def generate_art_concept(self) -> Dict:
        """
        Generate a complete art concept
        """
        movement = random.choice(self.art_movements)
        
        concept = {
            'title': self._generate_title(),
            'movement': movement,
            'medium': random.choice(self.mediums),
            'subject': random.choice(self.subjects),
            'composition': random.choice(self.composition_types),
            'color_scheme': random.choice(self.color_schemes),
            'mood': random.choice(self.moods),
            'palette': self.generate_palette(mood=random.choice(list(self.palettes.keys()))),
            'description': self._generate_description(),
            'technique': self._generate_technique(movement),
            'dimensions': self._generate_dimensions(),
            'year_created': random.randint(1900, 2025)
        }
        
        return concept
    
    def _generate_title(self) -> str:
        """Generate an art title"""
        templates = [
            f"{random.choice(['Study in', 'Variations on', 'Homage to', 'Echoes of'])} "
            f"{random.choice(['Red', 'Blue', 'Light', 'Darkness', 'Time', 'Space'])}",
            
            f"The {random.choice(['Last', 'First', 'Lost', 'Hidden', 'Eternal'])} "
            f"{random.choice(['Dream', 'Memory', 'Vision', 'Moment', 'Thought'])}",
            
            f"{random.choice(['Portrait of', 'Landscape with', 'Still Life with', 'Abstract'])} "
            f"{random.choice(['a Figure', 'Flowers', 'Mountains', 'Geometry', 'Light'])}"
        ]
        return random.choice(templates)
    
    def _generate_description(self) -> str:
        """Generate an art description"""
        templates = [
            f"A {random.choice(self.moods)} {random.choice(self.subjects)} "
            f"executed in {random.choice(self.mediums)}. The composition follows the "
            f"{random.choice(self.composition_types)} principle, creating a sense of "
            f"{random.choice(['balance', 'tension', 'harmony', 'movement'])}.",
            
            f"This work explores the intersection of {random.choice(self.art_movements)} "
            f"and {random.choice(self.color_schemes)} color theory. The artist uses "
            f"{random.choice(self.mediums)} to create a {random.choice(self.moods)} atmosphere.",
            
            f"Inspired by {random.choice(self.art_movements)}, this piece combines "
            f"{random.choice(self.composition_types)} composition with a "
            f"{random.choice(self.color_schemes)} palette to evoke {random.choice(self.moods)} emotions."
        ]
        return random.choice(templates)
    
    def _generate_technique(self, movement: str) -> str:
        """Generate technique description based on movement"""
        techniques = {
            'impressionism': 'visible brush strokes, open composition, light emphasis',
            'cubism': 'geometric forms, multiple perspectives, fragmented objects',
            'surrealism': 'dreamlike imagery, unexpected juxtapositions, precise detail',
            'abstract expressionism': 'gestural marks, spontaneous execution, emotional intensity',
            'pop art': 'bold colors, commercial imagery, hard edges',
            'minimalism': 'geometric abstraction, monochromatic, industrial materials',
            'renaissance': 'linear perspective, chiaroscuro, sfumato',
            'baroque': 'tenebrism, dramatic lighting, dynamic composition'
        }
        
        return techniques.get(movement, f'characteristic {movement} techniques')
    
    def _generate_dimensions(self) -> str:
        """Generate random dimensions"""
        sizes = [
            f"{random.randint(20, 200)} x {random.randint(20, 200)} cm",
            f"{random.randint(8, 80)} x {random.randint(8, 80)} in",
            f"{random.randint(100, 500)} x {random.randint(100, 500)} pixels (digital)"
        ]
        return random.choice(sizes)
    
    def generate_palette(self, mood: str = None, n_colors: int = 5) -> List[str]:
        """Generate a color palette"""
        if mood and mood in self.palettes:
            return self.palettes[mood]
        
        # Generate random palette
        palette = []
        for _ in range(n_colors):
            # Generate random hex color
            color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
            palette.append(color)
        
        return palette
    
    def generate_composition_sketch(self, width: int = 800, height: int = 600) -> Dict:
        """
        Generate a composition sketch (text description)
        """
        elements = []
        num_elements = random.randint(3, 8)
        
        for i in range(num_elements):
            element = {
                'id': i,
                'type': random.choice(['circle', 'rectangle', 'triangle', 'organic shape']),
                'position': {
                    'x': random.randint(0, width),
                    'y': random.randint(0, height)
                },
                'size': random.randint(20, 200),
                'color': self.generate_palette(n_colors=1)[0],
                'opacity': round(random.uniform(0.3, 1.0), 2)
            }
            elements.append(element)
        
        return {
            'width': width,
            'height': height,
            'composition_type': random.choice(self.composition_types),
            'elements': elements,
            'focal_point': random.randint(0, num_elements - 1) if elements else None
        }
    
    def generate_art_critique(self, concept: Dict) -> str:
        """
        Generate an art critique
        """
        critique_templates = [
            f"The use of {concept['color_scheme']} color scheme effectively "
            f"creates a {concept['mood']} atmosphere. The {concept['composition']} composition "
            f"leads the eye through the {concept['subject']}.",
            
            f"This {concept['movement']} piece demonstrates strong technical skill in "
            f"{concept['medium']}. The artist's handling of {concept['technique']} is particularly notable.",
            
            f"While the {concept['subject']} is traditional, the treatment feels fresh. "
            f"The {random.choice(['bold', 'subtle', 'vibrant', 'muted'])} color choices "
            f"evoke a powerful {random.choice(self.moods)} response."
        ]
        
        return random.choice(critique_templates)
    
    def suggest_artists(self, movement: str = None) -> List[str]:
        """Suggest artists from a movement"""
        artists = {
            'impressionism': ['Claude Monet', 'Pierre-Auguste Renoir', 'Edgar Degas'],
            'cubism': ['Pablo Picasso', 'Georges Braque', 'Juan Gris'],
            'surrealism': ['Salvador Dali', 'Rene Magritte', 'Max Ernst'],
            'pop art': ['Andy Warhol', 'Roy Lichtenstein', 'Claes Oldenburg'],
            'abstract expressionism': ['Jackson Pollock', 'Mark Rothko', 'Willem de Kooning'],
            'renaissance': ['Leonardo da Vinci', 'Michelangelo', 'Raphael'],
            'baroque': ['Caravaggio', 'Rembrandt', 'Peter Paul Rubens']
        }
        
        if movement and movement in artists:
            return artists[movement]
        else:
            all_artists = []
            for artist_list in artists.values():
                all_artists.extend(artist_list)
            return random.sample(all_artists, min(5, len(all_artists)))
    
    def color_theory_info(self, scheme: str = None) -> Dict:
        """Get information about color theory"""
        if scheme and scheme in self.color_scheme_descriptions:
            return {
                'scheme': scheme,
                'description': self.color_scheme_descriptions[scheme],
                'example': self.generate_palette(n_colors=random.randint(3, 5))
            }
        else:
            return self.color_scheme_descriptions