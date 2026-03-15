"""
Scientific Reasoning - Scientific method and domain knowledge
"""

import re
import math
from typing import Dict, List, Optional, Any, Tuple

class ScientificReasoning:
    """
    Scientific reasoning and domain knowledge
    """
    
    def __init__(self):
        self.scientific_facts = {}
        self.formulas = {}
        self.experiments = []
        self.hypotheses = []
        
        # Initialize with basic scientific knowledge
        self._init_science()
    
    def _init_science(self):
        """Initialize basic scientific knowledge"""
        # Physics formulas
        self.add_formula("newton_second", "F = m * a", 
                         ["force", "mass", "acceleration"])
        self.add_formula("einstein_energy", "E = m * c^2",
                         ["energy", "mass", "speed_of_light"])
        self.add_formula("gravity", "F = G * m1 * m2 / r^2",
                         ["force", "mass1", "mass2", "distance"])
        
        # Chemistry facts
        self.add_scientific_fact("water", "H2O", "chemistry")
        self.add_scientific_fact("methane", "CH4", "chemistry")
        self.add_scientific_fact("ideal_gas_law", "PV = nRT", "chemistry")
        
        # Biology facts
        self.add_scientific_fact("photosynthesis", 
            "6CO2 + 6H2O + light -> C6H12O6 + 6O2", "biology")
        self.add_scientific_fact("cell_theory", 
            "All living things are composed of cells", "biology")
    
    def add_scientific_fact(self, name: str, fact: str, domain: str):
        """Add a scientific fact"""
        self.scientific_facts[name] = {
            'fact': fact,
            'domain': domain,
            'verified': True
        }
    
    def add_formula(self, name: str, formula: str, variables: List[str]):
        """Add a scientific formula"""
        self.formulas[name] = {
            'formula': formula,
            'variables': variables,
            'uses': 0
        }
    
    def calculate(self, formula_name: str, **kwargs) -> Optional[float]:
        """
        Calculate using a formula
        """
        if formula_name not in self.formulas:
            return None
        
        formula = self.formulas[formula_name]
        formula['uses'] += 1
        
        # Parse and calculate based on formula name
        if formula_name == "newton_second":
            if 'mass' in kwargs and 'acceleration' in kwargs:
                return kwargs['mass'] * kwargs['acceleration']
        
        elif formula_name == "gravity":
            if all(v in kwargs for v in ['mass1', 'mass2', 'distance']):
                G = 6.67430e-11  # gravitational constant
                return G * kwargs['mass1'] * kwargs['mass2'] / (kwargs['distance'] ** 2)
        
        elif formula_name == "ideal_gas_law":
            # PV = nRT
            if 'pressure' in kwargs and 'volume' in kwargs:
                R = 8.314  # gas constant
                if 'moles' in kwargs and 'temperature' in kwargs:
                    return kwargs['pressure'] * kwargs['volume'] - kwargs['moles'] * R * kwargs['temperature']
        
        return None
    
    def test_hypothesis(self, hypothesis: str, evidence: List[str]) -> Dict:
        """
        Test a scientific hypothesis against evidence
        """
        result = {
            'hypothesis': hypothesis,
            'evidence': evidence,
            'supported': 0,
            'contradicted': 0,
            'confidence': 0.0,
            'conclusion': 'inconclusive'
        }
        
        # Simple keyword-based testing
        hypothesis_words = set(hypothesis.lower().split())
        
        for ev in evidence:
            ev_words = set(ev.lower().split())
            overlap = hypothesis_words.intersection(ev_words)
            
            if len(overlap) > 2:
                result['supported'] += 1
            elif len(overlap) == 0:
                result['contradicted'] += 1
        
        total = result['supported'] + result['contradicted']
        if total > 0:
            result['confidence'] = result['supported'] / total
        
        if result['confidence'] > 0.7:
            result['conclusion'] = 'supported'
        elif result['confidence'] < 0.3:
            result['conclusion'] = 'contradicted'
        
        return result
    
    def design_experiment(self, hypothesis: str) -> Dict:
        """
        Design an experiment to test a hypothesis
        """
        experiment = {
            'hypothesis': hypothesis,
            'independent_variables': [],
            'dependent_variables': [],
            'controls': [],
            'procedure': [],
            'predicted_outcome': None
        }
        
        # Extract potential variables
        words = hypothesis.split()
        for word in words:
            if word[0].isupper() and len(word) > 1:  # Potential proper noun
                experiment['independent_variables'].append(word)
        
        # Generate procedure
        experiment['procedure'] = [
            f"1. Set up controlled environment for testing: {hypothesis}",
            f"2. Measure baseline conditions",
            f"3. Apply variable: {', '.join(experiment['independent_variables'])}",
            f"4. Record observations",
            f"5. Analyze results",
            f"6. Draw conclusions"
        ]
        
        experiment['controls'] = ['temperature', 'pressure', 'time']
        
        return experiment
    
    def peer_review(self, paper: Dict) -> Dict:
        """
        Simulate peer review process
        """
        review = {
            'title': paper.get('title', 'Untitled'),
            'strengths': [],
            'weaknesses': [],
            'questions': [],
            'score': 0,
            'recommendation': 'reject'
        }
        
        # Check methodology
        if 'methodology' in paper:
            review['strengths'].append("Methodology clearly described")
            review['score'] += 2
        else:
            review['weaknesses'].append("Methodology not described")
        
        # Check results
        if 'results' in paper:
            if len(paper['results']) > 0:
                review['strengths'].append("Results presented")
                review['score'] += 3
        else:
            review['weaknesses'].append("No results presented")
        
        # Check conclusions
        if 'conclusions' in paper:
            review['strengths'].append("Conclusions drawn")
            review['score'] += 1
        else:
            review['weaknesses'].append("No conclusions")
        
        # Generate questions
        review['questions'] = [
            "How were variables controlled?",
            "Was the sample size adequate?",
            "Were there any confounding factors?"
        ]
        
        # Final score and recommendation
        if review['score'] >= 5:
            review['recommendation'] = 'accept'
        elif review['score'] >= 3:
            review['recommendation'] = 'revise'
        
        return review
    
    def explain_scientific_concept(self, concept: str) -> str:
        """
        Explain a scientific concept
        """
        explanations = {
            'gravity': "Gravity is a fundamental force that attracts objects with mass. "
                      "It's described by Newton's law and Einstein's general relativity.",
            
            'photosynthesis': "Photosynthesis is how plants convert light energy into chemical energy. "
                            "They use CO2, water, and sunlight to produce glucose and oxygen.",
            
            'evolution': "Evolution is change in heritable characteristics over generations. "
                        "It's driven by natural selection, mutation, and genetic drift.",
            
            'relativity': "Einstein's theory of relativity describes how space and time are connected. "
                         "Special relativity deals with constant motion, general relativity with acceleration and gravity.",
            
            'quantum': "Quantum mechanics describes physics at the smallest scales. "
                      "Particles can exist in multiple states and be entangled across distances."
        }
        
        return explanations.get(concept.lower(), f"Scientific concept: {concept}")