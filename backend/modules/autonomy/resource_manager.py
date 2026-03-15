"""
Resource Manager - Manage and allocate resources
"""

import random
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class ResourceManager:
    """
    Manages resources like time, energy, compute, etc.
    """
    
    def __init__(self):
        self.resources = {
            'time': {'total': 24 * 60, 'used': 0, 'unit': 'minutes'},
            'energy': {'total': 100, 'used': 0, 'unit': 'percent'},
            'compute': {'total': 1000, 'used': 0, 'unit': 'units'},
            'memory': {'total': 1024, 'used': 0, 'unit': 'MB'},
            'storage': {'total': 10240, 'used': 0, 'unit': 'MB'},
            'bandwidth': {'total': 100, 'used': 0, 'unit': 'MBps'}
        }
        
        self.allocations = []
        self.resource_history = []
        
    def allocate(self, resource: str, amount: float, task_id: str) -> bool:
        """
        Allocate resources to a task
        """
        if resource not in self.resources:
            return False
        
        res = self.resources[resource]
        if res['used'] + amount <= res['total']:
            res['used'] += amount
            
            allocation = {
                'resource': resource,
                'amount': amount,
                'task_id': task_id,
                'time': datetime.now().isoformat()
            }
            self.allocations.append(allocation)
            return True
        return False
    
    def release(self, resource: str, amount: float, task_id: str) -> bool:
        """
        Release allocated resources
        """
        if resource not in self.resources:
            return False
        
        res = self.resources[resource]
        if res['used'] - amount >= 0:
            res['used'] -= amount
            return True
        return False
    
    def get_available(self, resource: str) -> float:
        """
        Get available amount of resource
        """
        if resource not in self.resources:
            return 0
        res = self.resources[resource]
        return res['total'] - res['used']
    
    def get_usage_percent(self, resource: str) -> float:
        """
        Get usage percentage
        """
        if resource not in self.resources:
            return 0
        res = self.resources[resource]
        return (res['used'] / res['total']) * 100
    
    def get_all_resources(self) -> Dict:
        """
        Get all resource status
        """
        status = {}
        for name, res in self.resources.items():
            status[name] = {
                'total': res['total'],
                'used': res['used'],
                'available': res['total'] - res['used'],
                'percent': (res['used'] / res['total']) * 100,
                'unit': res['unit']
            }
        return status
    
    def optimize(self) -> List[str]:
        """
        Optimize resource allocation
        """
        suggestions = []
        
        for name, res in self.resources.items():
            usage = (res['used'] / res['total']) * 100
            
            if usage > 90:
                suggestions.append(f"{name} usage is critical ({usage:.1f}%). Consider reducing load.")
            elif usage > 70:
                suggestions.append(f"{name} usage is high ({usage:.1f}%). Monitor closely.")
            elif usage < 20:
                suggestions.append(f"{name} is underutilized ({usage:.1f}%). Consider reallocating.")
        
        return suggestions
    
    def add_resource(self, name: str, total: float, unit: str = 'units'):
        """
        Add a new resource type
        """
        self.resources[name] = {
            'total': total,
            'used': 0,
            'unit': unit
        }
    
    def simulate_usage(self, resource: str, duration_hours: int = 24) -> List[float]:
        """
        Simulate resource usage over time
        """
        usage_pattern = []
        for hour in range(duration_hours):
            # Generate realistic usage pattern
            base = 50  # Base usage
            time_factor = 20 * (1 if 9 <= hour % 24 <= 17 else 0.3)  # Work hours peak
            random_factor = random.uniform(-10, 10)
            usage = min(100, max(0, base + time_factor + random_factor))
            usage_pattern.append(usage)
        
        return usage_pattern
    
    def predict_needs(self, task_requirements: List[Dict]) -> Dict:
        """
        Predict resource needs for tasks
        """
        predictions = {}
        
        for resource in self.resources:
            total_needed = 0
            for task in task_requirements:
                total_needed += task.get(resource, 0)
            
            available = self.get_available(resource)
            
            predictions[resource] = {
                'needed': total_needed,
                'available': available,
                'sufficient': available >= total_needed,
                'shortfall': max(0, total_needed - available)
            }
        
        return predictions
    
    def reset_daily(self):
        """Reset daily resources (like time)"""
        self.resources['time']['used'] = 0
        self.resources['energy']['used'] = 0
        self.resources['bandwidth']['used'] = 0
        
        self.resource_history.append({
            'date': datetime.now().date().isoformat(),
            'allocations': self.allocations.copy()
        })
        
        self.allocations = []