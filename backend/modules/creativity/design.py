"""
Design Generator - Graphic design, UI/UX concepts, and branding
"""

import random
from typing import Dict, List, Optional

class DesignGenerator:
    """
    Generates design concepts, branding ideas, and UI layouts
    """
    
    def __init__(self):
        self.design_styles = [
            'minimalist', 'brutalist', 'neumorphism', 'glassmorphism',
            'flat design', 'material design', 'skeuomorphic', 'retro',
            'cyberpunk', 'vaporwave', 'corporate', 'playful', 'elegant',
            'industrial', 'organic', 'geometric', 'abstract'
        ]
        
        self.typography_styles = [
            'serif', 'sans-serif', 'monospace', 'handwritten', 'display',
            'geometric sans', 'humanist', 'transitional', 'modern', 'slab serif'
        ]
        
        self.fonts = {
            'serif': ['Times New Roman', 'Garamond', 'Georgia', 'Baskerville'],
            'sans-serif': ['Helvetica', 'Arial', 'Roboto', 'Open Sans', 'Inter'],
            'monospace': ['Courier New', 'Consolas', 'Monaco', 'Fira Code'],
            'handwritten': ['Comic Sans', 'Bradley Hand', 'Caveat', 'Pacifico'],
            'display': ['Impact', 'Oswald', 'Montserrat', 'Poppins']
        }
        
        self.brand_archetypes = [
            'the innocent', 'the everyman', 'the hero', 'the outlaw',
            'the explorer', 'the creator', 'the ruler', 'the magician',
            'the lover', 'the caregiver', 'the jester', 'the sage'
        ]
        
        self.logo_types = [
            'wordmark', 'letterform', 'symbol', 'abstract mark',
            'mascot', 'combination mark', 'emblem', 'dynamic'
        ]
        
        self.ui_patterns = [
            'hero section', 'card grid', 'sidebar navigation', 'tab bar',
            'modal dialog', 'dropdown menu', 'search bar', 'footer',
            'testimonial slider', 'pricing table', 'contact form'
        ]
        
        self.color_psychology = {
            'red': 'energy, passion, urgency',
            'blue': 'trust, stability, professionalism',
            'green': 'growth, health, nature',
            'yellow': 'optimism, clarity, warmth',
            'purple': 'luxury, creativity, wisdom',
            'orange': 'enthusiasm, fun, confidence',
            'black': 'power, sophistication, elegance',
            'white': 'purity, simplicity, cleanliness'
        }
    
    def generate_brand_identity(self, company_name: str = None) -> Dict:
        """
        Generate a complete brand identity
        """
        if company_name is None:
            company_name = self._generate_company_name()
        
        primary_color = random.choice(list(self.color_psychology.keys()))
        secondary_color = random.choice([c for c in self.color_psychology.keys() if c != primary_color])
        
        identity = {
            'company_name': company_name,
            'tagline': self._generate_tagline(),
            'archetype': random.choice(self.brand_archetypes),
            'logo_type': random.choice(self.logo_types),
            'primary_color': primary_color,
            'secondary_color': secondary_color,
            'color_psychology': {
                primary_color: self.color_psychology[primary_color],
                secondary_color: self.color_psychology[secondary_color]
            },
            'typography': self._generate_typography(),
            'design_style': random.choice(self.design_styles),
            'target_audience': self._generate_audience(),
            'brand_voice': self._generate_brand_voice(),
            'logo_description': self._generate_logo_description(),
            'color_palette': self._generate_palette(primary_color, secondary_color)
        }
        
        return identity
    
    def _generate_company_name(self) -> str:
        """Generate a company name"""
        prefixes = ['Nova', 'Apex', 'Vertex', 'Fusion', 'Quantum', 'Nexus',
                   'Orbit', 'Echo', 'Vivid', 'Pulse', 'Spark', 'Flux']
        suffixes = ['Tech', 'Labs', 'Studio', 'Works', 'Solutions', 'Group',
                   'Creative', 'Digital', 'Systems', 'Innovations']
        
        return f"{random.choice(prefixes)} {random.choice(suffixes)}"
    
    def _generate_tagline(self) -> str:
        """Generate a brand tagline"""
        templates = [
            f"Innovating the {random.choice(['future', 'world', 'tomorrow'])}",
            f"{random.choice(['Create', 'Build', 'Design', 'Shape'])} with purpose",
            f"{random.choice(['Transforming', 'Revolutionizing', 'Redefining'])} "
            f"{random.choice(['ideas', 'possibilities', 'expectations'])}",
            f"Where {random.choice(['creativity', 'technology', 'design'])} meets "
            f"{random.choice(['innovation', 'simplicity', 'excellence'])}"
        ]
        return random.choice(templates)
    
    def _generate_typography(self) -> Dict:
        """Generate typography choices"""
        style = random.choice(self.typography_styles)
        fonts = self.fonts.get(style, self.fonts['sans-serif'])
        
        return {
            'heading_font': random.choice(fonts),
            'body_font': random.choice(fonts),
            'accent_font': random.choice(self.fonts['display']),
            'style': style
        }
    
    def _generate_audience(self) -> str:
        """Generate target audience description"""
        audiences = [
            'tech-savvy professionals aged 25-40',
            'creative entrepreneurs and startups',
            'corporate decision-makers',
            'young adults seeking innovation',
            'design-conscious consumers',
            'enterprise clients and businesses'
        ]
        return random.choice(audiences)
    
    def _generate_brand_voice(self) -> str:
        """Generate brand voice description"""
        voices = [
            'professional yet approachable',
            'innovative and forward-thinking',
            'playful and energetic',
            'sophisticated and elegant',
            'clear and concise',
            'inspiring and motivational'
        ]
        return random.choice(voices)
    
    def _generate_logo_description(self) -> str:
        """Generate logo description"""
        templates = [
            f"A {random.choice(['minimal', 'bold', 'elegant', 'playful'])} "
            f"{random.choice(self.logo_types)} featuring a "
            f"{random.choice(['geometric', 'organic', 'abstract'])} symbol",
            
            f"Combines a {random.choice(['strong', 'delicate', 'dynamic'])} "
            f"icon with {random.choice(['clean', 'custom', 'distinctive'])} typography",
            
            f"Uses {random.choice(['negative space', 'geometric forms', 'fluid lines'])} "
            f"to create a memorable mark"
        ]
        return random.choice(templates)
    
    def _generate_palette(self, primary: str, secondary: str) -> List[str]:
        """Generate color palette from base colors"""
        # Convert color names to hex (simplified)
        color_hex = {
            'red': '#FF0000', 'blue': '#0000FF', 'green': '#00FF00',
            'yellow': '#FFFF00', 'purple': '#800080', 'orange': '#FFA500',
            'black': '#000000', 'white': '#FFFFFF'
        }
        
        palette = [
            color_hex.get(primary, '#000000'),
            color_hex.get(secondary, '#FFFFFF'),
            f"#{random.randint(0, 0xFFFFFF):06x}",
            f"#{random.randint(0, 0xFFFFFF):06x}"
        ]
        return palette
    
    def generate_ui_layout(self, page_type: str = 'website') -> Dict:
        """
        Generate a UI layout concept
        """
        layout = {
            'page_type': page_type,
            'patterns': random.sample(self.ui_patterns, random.randint(3, 6)),
            'color_scheme': self._generate_palette('blue', 'gray'),
            'typography': self._generate_typography(),
            'grid_system': random.choice(['12-column', '8-column', 'fluid', 'fixed']),
            'spacing': random.choice(['compact', 'comfortable', 'spacious']),
            'interactive_elements': self._generate_interactive_elements(),
            'responsive_breakpoints': ['mobile', 'tablet', 'desktop']
        }
        
        return layout
    
    def _generate_interactive_elements(self) -> List[str]:
        """Generate interactive UI elements"""
        elements = [
            'buttons with hover states',
            'animated transitions',
            'dropdown menus',
            'modal dialogs',
            'form inputs with validation',
            'loading animations',
            'scroll effects',
            'parallax scrolling'
        ]
        return random.sample(elements, random.randint(2, 4))
    
    def generate_poster_concept(self) -> Dict:
        """
        Generate a poster design concept
        """
        return {
            'title': self._generate_title(),
            'style': random.choice(self.design_styles),
            'composition': random.choice(['asymmetrical', 'symmetrical', 'radial', 'grid']),
            'typography': self._generate_typography(),
            'color_scheme': self.generate_palette(),
            'imagery': random.choice(['photography', 'illustration', 'abstract', 'typographic']),
            'size': f"{random.randint(18, 36)} x {random.randint(24, 48)} inches",
            'message': self._generate_tagline()
        }
    
    def generate_palette(self, n_colors: int = 5) -> List[str]:
        """Generate a random color palette"""
        palette = []
        for _ in range(n_colors):
            palette.append(f"#{random.randint(0, 0xFFFFFF):06x}")
        return palette
    
    def _generate_title(self) -> str:
        """Generate a title"""
        templates = [
            f"{random.choice(['The', 'A', 'Annual', 'International'])} "
            f"{random.choice(['Design', 'Art', 'Tech', 'Innovation'])} "
            f"{random.choice(['Conference', 'Exhibition', 'Summit', 'Festival'])}",
            
            f"{random.choice(['Future', 'Vision', 'Create', 'Evolve'])} "
            f"{random.randint(2025, 2030)}"
        ]
        return random.choice(templates)
    
    def generate_mood_board(self, theme: str = None) -> Dict:
        """
        Generate a mood board concept
        """
        if theme is None:
            theme = random.choice(['nature', 'urban', 'futuristic', 'vintage', 'minimal'])
        
        return {
            'theme': theme,
            'color_palette': self.generate_palette(),
            'textures': random.sample(['paper', 'metal', 'fabric', 'wood', 'glass'], 3),
            'typography': self._generate_typography(),
            'keywords': random.sample(['clean', 'bold', 'organic', 'geometric', 'dynamic'], 3),
            'mood': random.choice(['calm', 'energetic', 'mysterious', 'playful'])
        }