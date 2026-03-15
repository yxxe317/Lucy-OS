"""
Autonomous Learning - Self-improvement and learning from experience
"""

import random
import json
from typing import Dict, List, Optional
from datetime import datetime

class AutonomousLearning:
    """
    Enables autonomous learning and self-improvement
    """
    
    def __init__(self):
        self.experiences = []
        self.learned_patterns = {}
        self.skills = {}
        self.performance_history = []
        self.learning_rate = 0.1
        
    def add_experience(self, action: str, context: Dict, 
                        outcome: Dict, reward: float):
        """
        Add an experience for learning
        """
        experience = {
            'action': action,
            'context': context,
            'outcome': outcome,
            'reward': reward,
            'timestamp': datetime.now().isoformat()
        }
        
        self.experiences.append(experience)
        self._update_patterns(experience)
        
    def _update_patterns(self, experience: Dict):
        """
        Update learned patterns based on experience
        """
        action = experience['action']
        reward = experience['reward']
        
        if action not in self.learned_patterns:
            self.learned_patterns[action] = {
                'attempts': 0,
                'successes': 0,
                'total_reward': 0,
                'avg_reward': 0,
                'contexts': []
            }
        
        pattern = self.learned_patterns[action]
        pattern['attempts'] += 1
        pattern['successes'] += 1 if reward > 0.5 else 0
        pattern['total_reward'] += reward
        pattern['avg_reward'] = pattern['total_reward'] / pattern['attempts']
        pattern['contexts'].append(experience['context'])
        
        # Keep only recent contexts
        if len(pattern['contexts']) > 10:
            pattern['contexts'] = pattern['contexts'][-10:]
    
    def predict_outcome(self, action: str, context: Dict) -> Dict:
        """
        Predict outcome based on learned patterns
        """
        if action not in self.learned_patterns:
            return {'confidence': 0, 'predicted_reward': 0}
        
        pattern = self.learned_patterns[action]
        
        # Find similar contexts
        similar_count = 0
        total_reward = 0
        
        for past_context in pattern['contexts']:
            similarity = self._calculate_similarity(context, past_context)
            if similarity > 0.7:
                similar_count += 1
                total_reward += pattern['avg_reward']
        
        if similar_count > 0:
            confidence = min(1.0, similar_count / 5)
            predicted_reward = total_reward / similar_count
        else:
            confidence = pattern['attempts'] / 100
            predicted_reward = pattern['avg_reward']
        
        return {
            'confidence': confidence,
            'predicted_reward': predicted_reward,
            'action': action
        }
    
    def _calculate_similarity(self, context1: Dict, context2: Dict) -> float:
        """
        Calculate similarity between contexts
        """
        # Simplified similarity calculation
        common_keys = set(context1.keys()) & set(context2.keys())
        if not common_keys:
            return 0
        
        similarity = 0
        for key in common_keys:
            if context1[key] == context2[key]:
                similarity += 1
        
        return similarity / len(common_keys)
    
    def learn_skill(self, skill_name: str, training_data: List[Dict]) -> float:
        """
        Learn a new skill from training data
        """
        if skill_name not in self.skills:
            self.skills[skill_name] = {
                'proficiency': 0,
                'attempts': 0,
                'successes': 0,
                'last_practiced': None
            }
        
        skill = self.skills[skill_name]
        
        # Simulate learning
        for data in training_data:
            skill['attempts'] += 1
            if random.random() < 0.8:  # 80% success rate
                skill['successes'] += 1
        
        # Update proficiency
        if skill['attempts'] > 0:
            skill['proficiency'] = skill['successes'] / skill['attempts']
        
        skill['last_practiced'] = datetime.now().isoformat()
        
        return skill['proficiency']
    
    def practice_skill(self, skill_name: str, duration: int = 10) -> float:
        """
        Practice a skill to improve
        """
        if skill_name not in self.skills:
            return 0
        
        skill = self.skills[skill_name]
        
        # Practice improves proficiency
        improvement = self.learning_rate * (1 - skill['proficiency']) * (duration / 10)
        skill['proficiency'] = min(1.0, skill['proficiency'] + improvement)
        skill['last_practiced'] = datetime.now().isoformat()
        
        return skill['proficiency']
    
    def get_best_action(self, context: Dict, available_actions: List[str]) -> str:
        """
        Get best action for given context
        """
        predictions = []
        for action in available_actions:
            pred = self.predict_outcome(action, context)
            predictions.append((pred['predicted_reward'] * pred['confidence'], action))
        
        predictions.sort(reverse=True)
        return predictions[0][1] if predictions else random.choice(available_actions)
    
    def evaluate_performance(self) -> Dict:
        """
        Evaluate overall performance
        """
        total_attempts = sum(p['attempts'] for p in self.learned_patterns.values())
        total_successes = sum(p['successes'] for p in self.learned_patterns.values())
        
        avg_proficiency = 0
        if self.skills:
            avg_proficiency = sum(s['proficiency'] for s in self.skills.values()) / len(self.skills)
        
        performance = {
            'total_experiences': len(self.experiences),
            'total_attempts': total_attempts,
            'total_successes': total_successes,
            'success_rate': total_successes / total_attempts if total_attempts > 0 else 0,
            'learned_patterns': len(self.learned_patterns),
            'skills_learned': len(self.skills),
            'avg_proficiency': avg_proficiency,
            'learning_rate': self.learning_rate
        }
        
        self.performance_history.append(performance)
        return performance
    
    def adapt_learning_rate(self):
        """
        Adapt learning rate based on performance
        """
        if len(self.performance_history) < 2:
            return
        
        recent = self.performance_history[-1]
        previous = self.performance_history[-2]
        
        if recent['success_rate'] > previous['success_rate']:
            # Increase learning rate when doing well
            self.learning_rate = min(0.3, self.learning_rate * 1.1)
        else:
            # Decrease when struggling
            self.learning_rate = max(0.01, self.learning_rate * 0.9)
    
    def save_knowledge(self, filepath: str):
        """
        Save learned knowledge to file
        """
        knowledge = {
            'patterns': self.learned_patterns,
            'skills': self.skills,
            'performance': self.performance_history,
            'learning_rate': self.learning_rate
        }
        
        with open(filepath, 'w') as f:
            json.dump(knowledge, f, indent=2)
    
    def load_knowledge(self, filepath: str):
        """
        Load learned knowledge from file
        """
        try:
            with open(filepath, 'r') as f:
                knowledge = json.load(f)
                self.learned_patterns = knowledge['patterns']
                self.skills = knowledge['skills']
                self.performance_history = knowledge['performance']
                self.learning_rate = knowledge['learning_rate']
        except:
            pass