"""
Memory consolidation - moves short-term to long-term during "sleep"
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np

class MemoryConsolidation:
    """
    Consolidates memories during idle/sleep periods
    """
    
    def __init__(self, long_term_memory, episodic_memory, working_memory):
        self.ltm = long_term_memory
        self.episodic = episodic_memory
        self.wm = working_memory
        self.is_consolidating = False
        self.consolidation_thread = None
    
    def start_sleep_cycle(self, duration_seconds: int = 300):
        """
        Start sleep/consolidation cycle
        """
        if self.is_consolidating:
            return
        
        self.is_consolidating = True
        self.consolidation_thread = threading.Thread(
            target=self._sleep_cycle,
            args=(duration_seconds,)
        )
        self.consolidation_thread.daemon = True
        self.consolidation_thread.start()
    
    def _sleep_cycle(self, duration: int):
        """
        Main consolidation cycle
        """
        print("😴 Lucy is sleeping... consolidating memories")
        
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=duration)
        
        cycles = 0
        while datetime.now() < end_time and self.is_consolidating:
            # Consolidation phases
            self._consolidate_working_memory()
            self._replay_episodic_memories()
            self._strengthen_important_memories()
            self._prune_weak_memories()
            
            cycles += 1
            time.sleep(min(30, duration / 10))
        
        print(f"😊 Lucy woke up! Consolidated {cycles} memory cycles")
        self.is_consolidating = False
    
    def _consolidate_working_memory(self):
        """
        Move important working memory to long-term
        """
        for item in self.wm.get_all():
            importance = item.get('importance', 0.5)
            
            if importance > 0.7:
                # Store in long-term
                self.ltm.store_conversation(
                    user_id=item.get('user', 'default'),
                    role=item.get('role', 'system'),
                    content=item.get('content', ''),
                    importance=importance
                )
    
    def _replay_episodic_memories(self):
        """
        Replay recent episodes to strengthen them
        """
        recent = self.episodic.get_recent_episodes('default', limit=5)
        
        for episode in recent:
            # Simulate replay
            messages = episode.get('messages', [])
            if messages:
                # Strengthen by "replaying"
                print(f"🔄 Replaying conversation from {episode['start_time']}")
    
    def _strengthen_important_memories(self):
        """
        Increase strength of important memories
        """
        important = self.ltm.get_important_memories('default', days=1)
        
        for mem in important:
            # Increase importance
            # This would update embedding strength in real implementation
            pass
    
    def _prune_weak_memories(self):
        """
        Remove or archive weak memories
        """
        # Forget old, unimportant memories
        self.ltm.forget_old(days=30)
    
    def wake_up(self):
        """Interrupt sleep cycle"""
        self.is_consolidating = False
        if self.consolidation_thread:
            self.consolidation_thread.join(timeout=1)
        print("👋 Lucy woke up!")