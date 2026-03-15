"""
Reasoning Engine - Logical inference and deduction
"""

import re
from typing import Dict, List, Optional, Any, Set, Tuple

class ReasoningEngine:
    """
    Performs logical reasoning and inference
    """
    
    def __init__(self, knowledge_graph=None):
        self.kg = knowledge_graph
        self.rules = []
        self.facts = set()
        self.inference_cache = {}
        
        # Initialize with basic logic rules
        self._init_rules()
    
    def _init_rules(self):
        """Initialize basic inference rules"""
        self.add_rule("transitive", 
                      ["A relates_to B", "B relates_to C"],
                      "A relates_to C")
        
        self.add_rule("symmetric",
                      ["A is_related_to B"],
                      "B is_related_to A")
        
        self.add_rule("inheritance",
                      ["A is_a B", "B has_property C"],
                      "A has_property C")
        
        self.add_rule("contrapositive",
                      ["if A then B", "not B"],
                      "not A")
    
    def add_rule(self, name: str, premises: List[str], conclusion: str):
        """
        Add an inference rule
        """
        self.rules.append({
            'name': name,
            'premises': premises,
            'conclusion': conclusion
        })
    
    def add_fact(self, fact: str):
        """Add a fact to knowledge base"""
        self.facts.add(fact)
    
    def add_facts(self, facts: List[str]):
        """Add multiple facts"""
        for fact in facts:
            self.facts.add(fact)
    
    def deduce(self, target: str, max_depth: int = 5) -> List[Dict]:
        """
        Try to deduce if target is true
        """
        if target in self.facts:
            return [{'conclusion': target, 'method': 'direct', 'confidence': 1.0}]
        
        # Check cache
        if target in self.inference_cache:
            return self.inference_cache[target]
        
        results = []
        
        # Try each rule
        for rule in self.rules:
            deductions = self._apply_rule(rule, target, max_depth)
            results.extend(deductions)
        
        # Cache results
        self.inference_cache[target] = results
        return results
    
    def _apply_rule(self, rule: Dict, target: str, depth: int) -> List[Dict]:
        """
        Apply a specific rule to deduce target
        """
        if depth <= 0:
            return []
        
        results = []
        conclusion = rule['conclusion']
        
        # Check if conclusion matches target pattern
        if not self._matches_pattern(conclusion, target):
            return []
        
        # Try to find premises that lead to this conclusion
        premises = rule['premises']
        premise_combinations = self._find_premise_combinations(premises, depth - 1)
        
        for combo in premise_combinations:
            confidence = sum(p.get('confidence', 1.0) for p in combo) / len(combo)
            results.append({
                'conclusion': target,
                'method': rule['name'],
                'premises': combo,
                'confidence': confidence
            })
        
        return results
    
    def _matches_pattern(self, pattern: str, target: str) -> bool:
        """
        Check if target matches pattern
        """
        # Simple pattern matching (can be enhanced)
        pattern_parts = pattern.split()
        target_parts = target.split()
        
        if len(pattern_parts) != len(target_parts):
            return False
        
        for p, t in zip(pattern_parts, target_parts):
            if p.startswith('?') or p.startswith('X') or p.startswith('Y') or p.startswith('Z'):
                continue  # Variable matches anything
            if p != t:
                return False
        
        return True
    
    def _find_premise_combinations(self, premises: List[str], depth: int) -> List[List[Dict]]:
        """
        Find combinations of facts that satisfy premises
        """
        if not premises:
            return [[]]
        
        first_premise = premises[0]
        remaining = premises[1:]
        
        combinations = []
        
        # Find facts matching first premise
        matching_facts = self._find_matching_facts(first_premise)
        
        for fact in matching_facts:
            fact_result = {'fact': fact, 'confidence': 1.0}
            for rest_combo in self._find_premise_combinations(remaining, depth):
                combinations.append([fact_result] + rest_combo)
        
        # If no direct facts, try to deduce premises
        if not matching_facts and depth > 0:
            deduced = self.deduce(first_premise, depth - 1)
            for ded in deduced:
                for rest_combo in self._find_premise_combinations(remaining, depth - 1):
                    combinations.append([ded] + rest_combo)
        
        return combinations
    
    def _find_matching_facts(self, pattern: str) -> List[str]:
        """
        Find facts matching pattern
        """
        matches = []
        pattern_parts = pattern.split()
        
        for fact in self.facts:
            fact_parts = fact.split()
            
            if len(fact_parts) != len(pattern_parts):
                continue
            
            match = True
            variables = {}
            
            for p, f in zip(pattern_parts, fact_parts):
                if p.startswith('?') or p.startswith('X') or p.startswith('Y') or p.startswith('Z'):
                    var_name = p
                    if var_name in variables:
                        if variables[var_name] != f:
                            match = False
                            break
                    else:
                        variables[var_name] = f
                elif p != f:
                    match = False
                    break
            
            if match:
                matches.append(fact)
        
        return matches
    
    def syllogism(self, premise1: str, premise2: str) -> Optional[str]:
        """
        Apply syllogistic reasoning
        """
        # Example: All A are B, All B are C -> All A are C
        patterns = [
            (r'all (\w+) are (\w+)', r'all (\w+) are (\w+)', 
             lambda m1, m2: f"all {m1.group(1)} are {m2.group(2)}" if m1.group(2) == m2.group(1) else None),
            
            (r'(\w+) is a (\w+)', r'all (\w+) are (\w+)',
             lambda m1, m2: f"{m1.group(1)} is {m2.group(2)}" if m1.group(2) == m2.group(1) else None),
            
            (r'(\w+) is (\w+)', r'(\w+) is not (\w+)',
             lambda m1, m2: None)  # Contradiction
        ]
        
        for p1_pattern, p2_pattern, resolver in patterns:
            import re
            m1 = re.match(p1_pattern, premise1)
            m2 = re.match(p2_pattern, premise2)
            
            if m1 and m2:
                conclusion = resolver(m1, m2)
                if conclusion:
                    return conclusion
        
        return None
    
    def contradiction(self, fact1: str, fact2: str) -> bool:
        """
        Check if two facts contradict each other
        """
        # Simple contradiction detection
        opposites = [
            ('is', 'is not'),
            ('are', 'are not'),
            ('has', 'does not have'),
            ('can', 'cannot'),
            ('will', 'will not')
        ]
        
        for pos, neg in opposites:
            if pos in fact1 and neg in fact2:
                # Check if subjects match
                subj1 = fact1.split()[0]
                subj2 = fact2.split()[0]
                if subj1 == subj2:
                    return True
        
        return False
    
    def get_explanation(self, target: str) -> str:
        """
        Get explanation for how a conclusion was reached
        """
        deductions = self.deduce(target)
        
        if not deductions:
            return f"I cannot determine if '{target}' is true."
        
        best = max(deductions, key=lambda x: x['confidence'])
        
        if best['method'] == 'direct':
            return f"I know that {target} is true."
        
        explanation = f"I concluded that {target} because:\n"
        for i, premise in enumerate(best.get('premises', []), 1):
            if 'fact' in premise:
                explanation += f"  {i}. I know that {premise['fact']}\n"
            else:
                explanation += f"  {i}. I deduced that {premise['conclusion']}\n"
        
        explanation += f"This uses the rule of {best['method']} reasoning."
        return explanation