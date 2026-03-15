"""
Dream Simulator - Generate and interpret dreams
"""

import random
from typing import Dict, List, Optional
from datetime import datetime

class DreamSimulator:
    """
    Simulates dream states and dream interpretation
    """
    
    def __init__(self):
        self.dream_symbols = {
            'water': ['emotions', 'unconscious', 'fluidity'],
            'flying': ['freedom', 'escape', 'perspective'],
            'falling': ['insecurity', 'loss of control', 'fear'],
            'chase': ['anxiety', 'avoidance', 'pressure'],
            'teeth': ['anxiety', 'communication', 'power'],
            'house': ['self', 'mind', 'personal space'],
            'snake': ['transformation', 'fear', 'wisdom'],
            'death': ['change', 'ending', 'rebirth'],
            'naked': ['vulnerability', 'exposure', 'truth']
        }
        
        self.dream_phases = ['NREM', 'REM', 'Deep Sleep', 'Hypnagogic']
        self.dream_history = []
        
    def generate_dream(self, seed: str = None) -> Dict:
        """
        Generate a random dream
        """
        if seed is None:
            seed = random.choice(['anxiety', 'joy', 'fear', 'love', 'adventure'])
        
        # Dream narrative elements
        settings = ['forest', 'city', 'ocean', 'space', 'castle', 'school', 'home']
        characters = ['stranger', 'friend', 'family', 'animal', 'celebrity', 'monster']
        actions = ['flying', 'running', 'hiding', 'searching', 'talking', 'fighting']
        
        dream = {
            'title': f"The {random.choice(['Mysterious', 'Strange', 'Vivid', 'Recurring'])} Dream",
            'phase': random.choice(self.dream_phases),
            'narrative': self._generate_narrative(settings, characters, actions),
            'symbols': self._extract_symbols(settings + characters + actions),
            'emotion': random.choice(['fear', 'joy', 'confusion', 'peace', 'excitement']),
            'vividness': random.uniform(0.3, 1.0),
            'lucidity': random.uniform(0, 0.5),
            'timestamp': datetime.now().isoformat()
        }
        
        self.dream_history.append(dream)
        return dream
    
    def _generate_narrative(self, settings: List[str], characters: List[str], actions: List[str]) -> str:
        """Generate dream narrative"""
        templates = [
            f"I was in a {random.choice(settings)} when a {random.choice(characters)} appeared. "
            f"We started {random.choice(actions)}. Suddenly, everything changed and I was "
            f"{random.choice(['flying', 'falling', 'floating'])} through {random.choice(['clouds', 'space', 'water'])}.",
            
            f"A {random.choice(characters)} was {random.choice(actions)} in the {random.choice(settings)}. "
            f"I tried to {random.choice(['speak', 'move', 'run'])} but couldn't. "
            f"The {random.choice(['colors', 'sounds', 'shapes'])} were {random.choice(['vibrant', 'distorted', 'shifting'])}."
        ]
        return random.choice(templates)
    
    def _extract_symbols(self, elements: List[str]) -> List[Dict]:
        """Extract and interpret dream symbols"""
        symbols = []
        for element in elements:
            for symbol, interpretations in self.dream_symbols.items():
                if symbol in element.lower():
                    symbols.append({
                        'symbol': symbol,
                        'interpretations': interpretations,
                        'significance': random.uniform(0.1, 1.0)
                    })
                    break
        return symbols
    
    def interpret_dream(self, dream: Dict) -> str:
        """
        Provide dream interpretation
        """
        interpretation = f"Dream Interpretation:\n"
        interpretation += f"Emotional tone: {dream['emotion']}\n"
        interpretation += f"Dream phase: {dream['phase']}\n\n"
        
        interpretation += "Symbolic meanings:\n"
        for symbol in dream['symbols']:
            interpretation += f"• {symbol['symbol']}: {', '.join(symbol['interpretations'])}\n"
        
        interpretation += f"\nOverall meaning: This dream suggests {random.choice(['inner conflict', 'desire for change', 'unresolved emotions', 'creative inspiration'])}."
        
        return interpretation
    
    def lucid_dream_induction(self) -> List[str]:
        """
        Generate lucid dreaming techniques
        """
        techniques = [
            "Reality checks throughout the day",
            "Keep a dream journal",
            "MILD technique (Mnemonic Induction of Lucid Dreams)",
            "WBTB method (Wake Back to Bed)",
            "Visualization before sleep",
            "Meditation and mindfulness"
        ]
        
        return random.sample(techniques, 3)
    
    def dream_reality_check(self) -> bool:
        """
        Perform a reality check to test if dreaming
        """
        checks = [
            random.random() < 0.3,  # 30% chance of passing reality check
            random.random() < 0.3,
            random.random() < 0.3
        ]
        
        return all(checks)  # All checks must pass to confirm reality
    
    def get_dream_statistics(self) -> Dict:
        """
        Get statistics about dream history
        """
        if not self.dream_history:
            return {'total_dreams': 0}
        
        emotions = {}
        phases = {}
        for dream in self.dream_history:
            emotions[dream['emotion']] = emotions.get(dream['emotion'], 0) + 1
            phases[dream['phase']] = phases.get(dream['phase'], 0) + 1
        
        return {
            'total_dreams': len(self.dream_history),
            'avg_vividness': sum(d['vividness'] for d in self.dream_history) / len(self.dream_history),
            'avg_lucidity': sum(d['lucidity'] for d in self.dream_history) / len(self.dream_history),
            'emotion_distribution': emotions,
            'phase_distribution': phases
        }