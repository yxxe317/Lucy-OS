"""
Cognitive Load Manager - Adaptive processing based on mental capacity
"""
import asyncio
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
import json

class CognitiveLoadManager:
    def __init__(self):
        self.load_path = Path("data/cognitive_load")
        self.load_path.mkdir(exist_ok=True)
        self.base_load = 100.0
        self.current_load = 0.0
        self.load_history: List[float] = []
        self.max_history = 1000
        self.throttle_config = {
            "high_load_threshold": 70.0,
            "critical_load_threshold": 90.0,
            "recovery_rate": 0.5,
            "throttle_factor": 0.7
        }
        self._load_config()
    
    def _load_config(self):
        config_file = self.load_path / "load_config.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.throttle_config.update(config.get("thresholds", {}))
    
    def _save_config(self):
        with open(self.load_path / "load_config.json", 'w') as f:
            json.dump({"thresholds": self.throttle_config}, f, indent=2)
    
    def record_operation(self, cost: float = 1.0, operation_type: str = "compute"):
        """Record an operation's cognitive cost"""
        self.current_load = min(100.0, self.current_load + cost)
        self._update_history(cost)
        self._apply_throttling()
        return self.current_load
    
    def _update_history(self, cost: float):
        self.load_history.append(cost)
        if len(self.load_history) > self.max_history:
            self.load_history = self.load_history[-self.max_history:]
    
    def _apply_throttling(self):
        if self.current_load > self.throttle_config["critical_load_threshold"]:
            # Critical: batch operations, reduce parallelism
            asyncio.create_task(self._notify_critical())
        elif self.current_load > self.throttle_config["high_load_threshold"]:
            # High: moderate throttling
            asyncio.create_task(self._notify_high())
    
    async def _notify_critical(self):
        print(f"[COGNITIVE LOAD] CRITICAL: {self.current_load:.1f}%")
    
    async def _notify_high(self):
        print(f"[COGNITIVE LOAD] HIGH: {self.current_load:.1f}%")
    
    def get_effective_cost(self, base_cost: float) -> float:
        """Calculate throttled operation cost"""
        if self.current_load > self.throttle_config["critical_load_threshold"]:
            return base_cost * self.throttle_config["throttle_factor"]
        elif self.current_load > self.throttle_config["high_load_threshold"]:
            return base_cost * 0.85
        return base_cost
    
    def predict_load(self, pending_operations: List[float]) -> float:
        """Predict future load after pending operations"""
        predicted = self.current_load + sum(pending_operations)
        return min(100.0, predicted)
    
    def recover(self, recovery_time: float = 1.0):
        """Simulate load recovery over time"""
        self.current_load = max(0.0, self.current_load * (1 - self.throttle_config["recovery_rate"] * 0.1))
        return self.current_load
    
    def get_load_profile(self) -> dict:
        """Get current load profile"""
        avg_cost = sum(self.load_history[-100:]) / len(self.load_history) if self.load_history else 0
        return {
            "current_load": round(self.current_load, 2),
            "base_load": self.base_load,
            "avg_operation_cost": round(avg_cost, 3),
            "history_size": len(self.load_history),
            "status": self._get_status()
        }
    
    def _get_status(self) -> str:
        if self.current_load > self.throttle_config["critical_load_threshold"]:
            return "CRITICAL"
        elif self.current_load > self.throttle_config["high_load_threshold"]:
            return "HIGH"
        elif self.current_load > 50:
            return "MODERATE"
        return "NORMAL"
    
    def reset(self):
        """Reset load to baseline"""
        self.current_load = self.base_load
        self.load_history.clear()
        return {"reset": True, "load": self.current_load}

# Global instance
cognitive_load = CognitiveLoadManager()