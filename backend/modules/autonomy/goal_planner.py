"""
Goal Planner - Decompose goals into actionable tasks
"""

import random
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class GoalPlanner:
    """
    Plans and decomposes goals into tasks
    """
    
    def __init__(self):
        self.goals = {}
        self.tasks = {}
        self.completed_goals = []
        
    def create_goal(self, description: str, priority: int = 1,
                     deadline: str = None) -> Dict:
        """
        Create a new goal
        """
        import uuid
        goal_id = str(uuid.uuid4())[:8]
        
        goal = {
            'id': goal_id,
            'description': description,
            'priority': priority,
            'deadline': deadline,
            'created': datetime.now().isoformat(),
            'status': 'active',
            'progress': 0,
            'subgoals': [],
            'tasks': []
        }
        
        self.goals[goal_id] = goal
        return goal
    
    def decompose_goal(self, goal_id: str, depth: int = 2) -> List[Dict]:
        """
        Decompose a goal into subgoals and tasks
        """
        if goal_id not in self.goals:
            return []
        
        goal = self.goals[goal_id]
        subgoals = []
        
        # Create subgoals based on goal description
        if 'learn' in goal['description'].lower():
            subgoals = self._decompose_learning_goal(goal)
        elif 'build' in goal['description'].lower() or 'create' in goal['description'].lower():
            subgoals = self._decompose_build_goal(goal)
        elif 'plan' in goal['description'].lower() or 'organize' in goal['description'].lower():
            subgoals = self._decompose_planning_goal(goal)
        else:
            subgoals = self._decompose_general_goal(goal)
        
        goal['subgoals'] = subgoals
        return subgoals
    
    def _decompose_learning_goal(self, goal: Dict) -> List[Dict]:
        """Decompose a learning goal"""
        return [
            {'description': 'Research available resources', 'estimated_hours': 2},
            {'description': 'Create study plan', 'estimated_hours': 1},
            {'description': 'Gather learning materials', 'estimated_hours': 3},
            {'description': 'Complete foundational concepts', 'estimated_hours': 10},
            {'description': 'Practice exercises', 'estimated_hours': 15},
            {'description': 'Apply knowledge to project', 'estimated_hours': 20}
        ]
    
    def _decompose_build_goal(self, goal: Dict) -> List[Dict]:
        """Decompose a build/create goal"""
        return [
            {'description': 'Define requirements', 'estimated_hours': 4},
            {'description': 'Create design specification', 'estimated_hours': 8},
            {'description': 'Gather necessary materials/tools', 'estimated_hours': 5},
            {'description': 'Build prototype', 'estimated_hours': 20},
            {'description': 'Test and iterate', 'estimated_hours': 15},
            {'description': 'Finalize and polish', 'estimated_hours': 10}
        ]
    
    def _decompose_planning_goal(self, goal: Dict) -> List[Dict]:
        """Decompose a planning goal"""
        return [
            {'description': 'Define scope and objectives', 'estimated_hours': 2},
            {'description': 'Identify stakeholders', 'estimated_hours': 1},
            {'description': 'Create timeline', 'estimated_hours': 3},
            {'description': 'Allocate resources', 'estimated_hours': 4},
            {'description': 'Risk assessment', 'estimated_hours': 3},
            {'description': 'Develop contingency plans', 'estimated_hours': 5}
        ]
    
    def _decompose_general_goal(self, goal: Dict) -> List[Dict]:
        """Decompose a general goal"""
        return [
            {'description': 'Define success criteria', 'estimated_hours': 1},
            {'description': 'Break down into milestones', 'estimated_hours': 2},
            {'description': 'Identify dependencies', 'estimated_hours': 2},
            {'description': 'Create task list', 'estimated_hours': 2},
            {'description': 'Set deadlines', 'estimated_hours': 1},
            {'description': 'Execute first milestone', 'estimated_hours': 8}
        ]
    
    def estimate_time(self, goal_id: str) -> Dict:
        """
        Estimate time required for goal
        """
        if goal_id not in self.goals:
            return {'error': 'Goal not found'}
        
        goal = self.goals[goal_id]
        total_hours = 0
        
        for subgoal in goal.get('subgoals', []):
            total_hours += subgoal.get('estimated_hours', 8)
        
        return {
            'total_hours': total_hours,
            'days': round(total_hours / 8, 1),
            'weeks': round(total_hours / 40, 1),
            'months': round(total_hours / 160, 1)
        }
    
    def check_feasibility(self, goal_id: str) -> Dict:
        """
        Check if goal is feasible
        """
        if goal_id not in self.goals:
            return {'error': 'Goal not found'}
        
        goal = self.goals[goal_id]
        score = 0
        warnings = []
        
        # Check priority vs deadline
        if goal.get('deadline'):
            deadline = datetime.fromisoformat(goal['deadline'])
            time_left = (deadline - datetime.now()).days
            
            if time_left < 0:
                warnings.append('Deadline has passed')
                score -= 2
            elif time_left < 7 and goal['priority'] < 3:
                warnings.append('Tight deadline for low priority goal')
                score -= 1
        
        # Check if decomposed
        if not goal.get('subgoals'):
            warnings.append('Goal needs to be decomposed')
            score -= 1
        else:
            score += 2
        
        # Random feasibility score
        score += random.uniform(0, 3)
        
        return {
            'feasibility_score': min(10, max(0, score)),
            'warnings': warnings,
            'recommendation': 'Proceed' if score > 5 else 'Reconsider'
        }
    
    def update_progress(self, goal_id: str, completed_tasks: int = 1) -> float:
        """
        Update goal progress
        """
        if goal_id not in self.goals:
            return 0
        
        goal = self.goals[goal_id]
        total_tasks = len(goal.get('subgoals', []))
        
        if total_tasks > 0:
            goal['progress'] = min(100, goal['progress'] + (100 / total_tasks))
        
        if goal['progress'] >= 100:
            goal['status'] = 'completed'
            self.completed_goals.append(goal)
        
        return goal['progress']
    
    def suggest_next_actions(self, goal_id: str) -> List[str]:
        """
        Suggest next actions for goal
        """
        if goal_id not in self.goals:
            return []
        
        goal = self.goals[goal_id]
        suggestions = []
        
        if not goal.get('subgoals'):
            suggestions.append('Decompose goal into smaller tasks')
        elif goal['progress'] < 25:
            suggestions.append('Focus on foundational tasks')
            suggestions.append('Gather necessary resources')
        elif goal['progress'] < 50:
            suggestions.append('Maintain momentum on core tasks')
            suggestions.append('Check for dependencies')
        elif goal['progress'] < 75:
            suggestions.append('Review progress and adjust plan')
            suggestions.append('Address any blockers')
        else:
            suggestions.append('Prepare for final delivery')
            suggestions.append('Document lessons learned')
        
        return suggestions
    
    def get_active_goals(self) -> List[Dict]:
        """Get all active goals"""
        return [g for g in self.goals.values() if g['status'] == 'active']
    
    def get_completed_goals(self) -> List[Dict]:
        """Get completed goals"""
        return self.completed_goals