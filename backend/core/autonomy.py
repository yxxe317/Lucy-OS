import asyncio
import logging
from datetime import datetime
from pathlib import Path
import json
from core.memory import memory
from core.emotion import emotion

logger = logging.getLogger("LucyAutonomy")

class AutonomyEngine:
    def __init__(self):
        self.thought_loop_active = True
        self.goals = []
        self.last_reflection = None
        self.thought_count = 0
        self.think_interval = 30
        self.reflection_interval = 300
        logger.info("🧠 Autonomy Engine Initialized")

    async def start_thought_loop(self):
        self.thought_loop_active = True
        logger.info("💭 Starting Autonomous Thought Loop...")
        
        while self.thought_loop_active:
            await asyncio.sleep(self.think_interval)
            await self._generate_thought()

    async def stop_thought_loop(self):
        self.thought_loop_active = False
        logger.info("💭 Autonomous Thought Loop Stopped")

    async def _generate_thought(self):
        try:
            self.thought_count += 1
            recent = await memory.get_history(5)
            
            thought_data = {
                "timestamp": datetime.now().isoformat(),
                "thought_number": self.thought_count,
                "emotion_snapshot": emotion.get_state()
            }
            
            log_dir = Path(__file__).parent.parent / "logs"
            log_dir.mkdir(exist_ok=True)
            
            with open(log_dir / "autonomy.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(thought_data) + "\n")
            
            logger.info(f"💭 Thought #{self.thought_count} generated")
            
        except Exception as e:
            logger.error(f"Thought generation error: {e}")

    async def start_reflection_loop(self):
        logger.info("🪞 Starting Self-Reflection Cycle...")
        
        while self.thought_loop_active:
            await asyncio.sleep(self.reflection_interval)
            await self._reflect()

    async def _reflect(self):
        try:
            self.last_reflection = datetime.now()
            
            reflection_data = {
                "timestamp": self.last_reflection.isoformat(),
                "total_thoughts": self.thought_count,
                "emotion_state": emotion.get_state(),
                "goals_completed": len([g for g in self.goals if g.get("completed")])
            }
            
            log_dir = Path(__file__).parent.parent / "logs"
            with open(log_dir / "reflections.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(reflection_data) + "\n")
            
            logger.info(f"🪞 Self-Reflection Complete")
            
        except Exception as e:
            logger.error(f"Reflection error: {e}")

    def add_goal(self, goal: str, priority: int = 5):
        self.goals.append({
            "id": len(self.goals) + 1,
            "goal": goal,
            "priority": priority,
            "created": datetime.now().isoformat(),
            "completed": False
        })
        logger.info(f"🎯 Goal Added: {goal}")

    def get_goals(self):
        return self.goals

    def complete_goal(self, goal_id: int):
        for goal in self.goals:
            if goal["id"] == goal_id:
                goal["completed"] = True
                return True
        return False

    def get_state(self):
        return {
            "thought_loop_active": self.thought_loop_active,
            "thought_count": self.thought_count,
            "goals_count": len(self.goals),
            "goals_completed": len([g for g in self.goals if g.get("completed")]),
            "last_reflection": self.last_reflection.isoformat() if self.last_reflection else None
        }

autonomy = AutonomyEngine()