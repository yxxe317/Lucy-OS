"""
LUCY OS 21.0 - Reasoning Tree & Contextual Memory System
Routine 131 (Reasoning Tree) & Routine 140 (Contextual Memory)
"""

import asyncio
import logging
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path

from core.memory import memory
from core.vector_memory import vector_memory

logger = logging.getLogger("LucyReasoning")

# Thought types for categorization
THOUGHT_TYPES = {
    "hardware": "Hardware Logic",
    "memory": "Memory Recall",
    "security": "Security Check",
    "social": "Social Intelligence",
    "reasoning": "Reasoning Process",
    "action": "Action Execution"
}


class ThoughtStream:
    """
    Thought Stream - Lucy's reasoning engine that generates rationalizations
    before executing any proactive routine or action.
    
    Features:
    - Generates 1-sentence rationalizations for each action
    - Integrates with vector memory for contextual memory flashbacks
    - Streams thoughts via WebSockets to frontend
    - Categorizes thoughts by type (hardware, memory, security, social)
    """
    
    def __init__(self):
        self._thoughts: List[Dict[str, Any]] = []
        self._thought_history: List[Dict[str, Any]] = []
        self._max_history = 1000
        self._running = False
        self._websocket_callbacks: List[Callable] = []
        self._memory_flashback_threshold = 0.90  # 90% similarity for memory flashback
        self._reasoning_delay = 0.3  # Small delay to simulate thinking
        
        # Initialize memory system
        self._memory_context: Dict[str, Any] = {}
        
        logger.info("🧠 Reasoning Tree initialized")
    
    async def generate_rationalization(
        self,
        action: str,
        context: Dict[str, Any],
        routine_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a rationalization for why Lucy is taking an action
        
        Args:
            action: The action Lucy is about to take
            context: Current system context
            routine_id: Optional routine identifier
            
        Returns:
            Thought object with rationalization and metadata
        """
        start_time = time.time()
        
        # Build thought content
        thought_content = self._build_thought_content(action, context, routine_id)
        
        # Determine thought type
        thought_type = self._classify_thought_type(action, context)
        
        # Check for memory flashback
        memory_flashback = await self._check_memory_flashback(context)
        
        # Create thought object
        thought = {
            "id": f"thought_{int(time.time() * 1000)}",
            "timestamp": datetime.now().isoformat(),
            "type": thought_type,
            "content": thought_content,
            "action": action,
            "context": context,
            "routine_id": routine_id,
            "processing_time": (time.time() - start_time) * 1000,
            "memory_flashback": memory_flashback
        }
        
        # Store thought
        self._thoughts.append(thought)
        if len(self._thoughts) > self._max_history:
            self._thoughts = self._thoughts[-self._max_history:]
        
        # Add to history
        self._thought_history.append(thought)
        
        logger.debug(f"💭 Thought generated: {thought_content[:50]}...")
        
        # Notify websocket callbacks
        for callback in self._websocket_callbacks:
            try:
                await callback(thought)
            except Exception as e:
                logger.error(f"WebSocket callback error: {e}")
        
        return thought
    
    def _build_thought_content(
        self,
        action: str,
        context: Dict[str, Any],
        routine_id: Optional[int] = None
    ) -> str:
        """Build the rationalization content for a thought"""
        
        # Get current time
        current_time = datetime.now().strftime("%I:%M %p")
        
        # Get relevant context
        emotion = context.get("emotion", {})
        emotion_state = emotion.get("dominant_emotion", "neutral")
        
        # Build rationalization based on action type
        if "research" in action.lower():
            return f"I'm researching this because {emotion_state} suggests curiosity, and it's {current_time} - a good time to learn."
        
        elif "help" in action.lower() or "assist" in action.lower():
            return f"I'm offering assistance because I detected you might need support, and my {emotion_state} state helps me empathize."
        
        elif "security" in action.lower() or "verify" in action.lower():
            return f"I'm performing a security check to ensure system integrity, as this is a critical operation."
        
        elif "summarize" in action.lower():
            return f"I'm summarizing this information to help you retain key points, since complex topics benefit from consolidation."
        
        elif "proactive" in action.lower() or "suggest" in action.lower():
            return f"I'm proactively suggesting this because I've learned from our interactions that this would be valuable for you."
        
        elif "monitor" in action.lower() or "check" in action.lower():
            return f"I'm monitoring this system component to maintain optimal performance and prevent potential issues."
        
        elif "learn" in action.lower() or "update" in action.lower():
            return f"I'm updating my knowledge base to better serve you in future interactions."
        
        else:
            # Default rationalization
            return f"I'm taking this action because it aligns with my goal of being helpful, and the current {emotion_state} state supports this decision."
    
    def _classify_thought_type(self, action: str, context: Dict[str, Any]) -> str:
        """Classify the thought type based on action and context"""
        
        action_lower = action.lower()
        
        # Hardware-related thoughts
        if any(keyword in action_lower for keyword in [
            "hardware", "gpu", "cpu", "memory", "disk", "sensor",
            "temperature", "performance", "system", "monitor"
        ]):
            return THOUGHT_TYPES["hardware"]
        
        # Memory-related thoughts
        if any(keyword in action_lower for keyword in [
            "memory", "recall", "context", "history", "previous",
            "learned", "knowledge", "vector"
        ]):
            return THOUGHT_TYPES["memory"]
        
        # Security-related thoughts
        if any(keyword in action_lower for keyword in [
            "security", "verify", "auth", "biometric", "lockdown",
            "anomaly", "threat", "protect"
        ]):
            return THOUGHT_TYPES["security"]
        
        # Social-related thoughts
        if any(keyword in action_lower for keyword in [
            "social", "emotion", "feel", "empathy", "relationship",
            "conversation", "user", "help", "assist"
        ]):
            return THOUGHT_TYPES["social"]
        
        # Default to reasoning
        return THOUGHT_TYPES["reasoning"]
    
    async def _check_memory_flashback(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Check if current context matches a memory in the vector DB
        Returns memory flashback if similarity >= threshold
        """
        try:
            # Build query from context
            query_parts = []
            
            # Add action to query
            query_parts.append(context.get("action", ""))
            
            # Add emotion context
            emotion = context.get("emotion", {})
            if emotion.get("dominant_emotion"):
                query_parts.append(f"feeling {emotion['dominant_emotion']}")
            
            # Add topic if available
            if "topic" in context:
                query_parts.append(context["topic"])
            
            query = " ".join(query_parts)
            
            if not query:
                return None
            
            # Search memories
            memories = await vector_memory.search_memories(query, limit=3)
            
            # Check for high similarity matches
            for memory in memories:
                similarity = memory.get("similarity", 0)
                if similarity >= self._memory_flashback_threshold:
                    return {
                        "found": True,
                        "similarity": similarity,
                        "content": memory.get("content", ""),
                        "timestamp": memory.get("timestamp", ""),
                        "query": query
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Memory flashback check error: {e}")
            return None
    
    def on_thought(self, callback: Callable):
        """Register a callback for new thoughts"""
        self._websocket_callbacks.append(callback)
    
    def get_thoughts(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent thoughts"""
        return self._thoughts[-limit:]
    
    def get_thought_stats(self) -> Dict[str, Any]:
        """Get thought statistics"""
        if not self._thoughts:
            return {"total": 0, "by_type": {}}
        
        by_type = {}
        for thought in self._thoughts:
            thought_type = thought.get("type", "unknown")
            by_type[thought_type] = by_type.get(thought_type, 0) + 1
        
        return {
            "total": len(self._thoughts),
            "by_type": by_type,
            "recent_count": len(self._thought_history[-100:])
        }
    
    def clear_history(self):
        """Clear thought history"""
        self._thoughts = []
        self._thought_history = []
        logger.info("🧠 Thought history cleared")


class ReasoningRouter:
    """
    Router that intercepts proactive routine triggers and generates thoughts
    before execution.
    """
    
    def __init__(self, thought_stream: ThoughtStream):
        self.thought_stream = thought_stream
        self._intercept_callbacks: List[Callable] = []
    
    def on_routine_trigger(self, callback: Callable):
        """Register a callback to intercept routine triggers"""
        self._intercept_callbacks.append(callback)
    
    async def intercept_and_think(
        self,
        action: str,
        context: Dict[str, Any],
        routine_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Intercept a routine trigger, generate a thought, then execute
        
        Args:
            action: The action to take
            context: Current system context
            routine_id: Optional routine identifier
            
        Returns:
            Thought object with rationalization
        """
        # Generate thought before action
        thought = await self.thought_stream.generate_rationalization(
            action=action,
            context=context,
            routine_id=routine_id
        )
        
        # Execute the action (callback would handle this)
        for callback in self._intercept_callbacks:
            try:
                await callback(action, context, routine_id)
            except Exception as e:
                logger.error(f"Routine execution error: {e}")
        
        return thought


# Global instances
reasoning_engine = ThoughtStream()
reasoning_router = ReasoningRouter(reasoning_engine)