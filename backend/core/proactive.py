import logging
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger("ProactiveIntelligence")

# ═══════════════════════════════════════════════════════════════
# PATTERN MATCHER - Learns user routines from history
# ═══════════════════════════════════════════════════════════════
class PatternMatcher:
    """
    Detects behavioral patterns from user interaction history
    """
    
    def __init__(self, pattern_db_path: str = "backend/data/patterns.json"):
        self.db_path = Path(pattern_db_path)
        self.patterns: Dict[str, Dict[str, Any]] = {}
        self._load()
    
    def _load(self):
        """Load learned patterns"""
        try:
            if self.db_path.exists():
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.patterns = data.get("patterns", {})
                    logger.info(f"✅ Loaded {len(self.patterns)} behavioral patterns")
        except Exception as e:
            logger.warning(f"⚠️ Could not load patterns: {e}")
    
    def _save(self):
        """Save learned patterns"""
        try:
            data = {"patterns": self.patterns, "version": "1.0"}
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("💾 Patterns saved")
        except Exception as e:
            logger.error(f"❌ Save failed: {e}")
    
    def learn_pattern(self, trigger: str, routine: List[str], 
                      frequency: int = 1, confidence: float = 0.7):
        """
        Learn a new behavioral pattern
        Example: trigger="9:00 AM", routine=["check email", "summarize tasks"]
        """
        key = f"{trigger}:{routine}"
        
        if key in self.patterns:
            self.patterns[key]["frequency"] = frequency
            self.patterns[key]["last_seen"] = datetime.now().isoformat()
            return True
        
        self.patterns[key] = {
            "trigger": trigger,
            "routine": routine,
            "frequency": frequency,
            "confidence": confidence,
            "last_seen": datetime.now().isoformat(),
            "learned_at": datetime.now().isoformat()
        }
        
        self._save()
        logger.info(f"📚 Learned pattern: {trigger} → {routine}")
        return True
    
    def find_pattern(self, current_time: str = None) -> Optional[Dict[str, Any]]:
        """
        Find matching patterns for current time/context
        """
        if current_time is None:
            current_time = datetime.now().isoformat()
        
        matches = []
        for key, pattern in self.patterns.items():
            trigger = pattern.get("trigger", "")
            
            # Check time-based triggers
            if self._matches_trigger(trigger, current_time):
                matches.append(pattern)
            
            # Check context-based triggers
            elif self._matches_context(trigger):
                matches.append(pattern)
        
        if matches:
            # Sort by confidence and frequency
            matches.sort(
                key=lambda x: (x.get("confidence", 0), x.get("frequency", 0)),
                reverse=True
            )
            return matches[0]
        
        return None
    
    def _matches_trigger(self, trigger: str, current_time: str) -> bool:
        """Check if trigger matches current time"""
        try:
            # Parse time patterns like "9:00 AM", "morning", "lunch time"
            if ":" in trigger:
                # Exact time match
                current = datetime.fromisoformat(current_time).strftime("%H:%M")
                return trigger.strip() == current
            
            # Fuzzy time match
            time_patterns = {
                "morning": "06:00-12:00",
                "afternoon": "12:00-18:00",
                "evening": "18:00-22:00",
                "night": "22:00-06:00"
            }
            
            for name, range_ in time_patterns.items():
                if name in trigger.lower():
                    return range_ in current_time.lower()
            
            return False
        except:
            return False
    
    def _matches_context(self, trigger: str) -> bool:
        """Check if trigger matches current context"""
        # Context could be: location, device, time of day, etc.
        # This can be extended with sensor data
        return False
    
    def get_all_patterns(self) -> List[Dict[str, Any]]:
        """Get all learned patterns"""
        return list(self.patterns.values())

# ═══════════════════════════════════════════════════════════════
# INTENT PREDICTOR - Predicts what user will ask next
# ═══════════════════════════════════════════════════════════════
class IntentPredictor:
    """
    Predicts upcoming user intents based on conversation history
    """
    
    def __init__(self):
        self.intent_history: List[Tuple[str, str]] = []  # (predicted, actual)
        self.intent_weights: Dict[str, float] = defaultdict(float)
        self._intent_sequences: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    
    def record_prediction(self, predicted_intent: str, actual_intent: Optional[str] = None):
        """Record a prediction and its accuracy"""
        self.intent_history.append((predicted_intent, actual_intent))
        
        # Update weights
        self.intent_weights[predicted_intent] += 1
        
        # Track sequences
        if actual_intent:
            self._intent_sequences[predicted_intent][actual_intent] += 1
    
    def predict_next_intent(self, current_intent: str, 
                           conversation_context: List[str] = None,
                           max_predictions: int = 3) -> List[Tuple[str, float]]:
        """
        Predict next likely intents
        Returns: List of (intent, confidence) tuples
        """
        predictions = []
        
        # 1. Sequence-based prediction
        if current_intent in self._intent_sequences:
            for next_intent, count in self._intent_sequences[current_intent].items():
                confidence = min(1.0, count / 10)  # Normalize
                predictions.append((next_intent, confidence))
        
        # 2. Weight-based prediction
        sorted_weights = sorted(
            self.intent_weights.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        for intent, weight in sorted_weights:
            if intent not in [p[0] for p in predictions]:
                # Normalize weight to confidence
                total_weight = sum(w for _, w in self.intent_weights.items())
                confidence = min(1.0, weight / total_weight * 5)
                predictions.append((intent, confidence))
        
        # 3. Context-based boosting
        if conversation_context:
            context_boost = self._context_boost(conversation_context)
            for intent, confidence in predictions:
                if context_boost.get(intent, 0) > 0:
                    confidence = min(1.0, confidence + context_boost[intent])
        
        # Sort by confidence
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:max_predictions]
    
    def _context_boost(self, context: List[str]) -> Dict[str, float]:
        """Boost predictions based on conversation context"""
        boosts = {}
        context_lower = " ".join(context).lower()
        
        # Domain-specific boosts
        domain_boosts = {
            "technical": ["documentation", "API", "code", "implementation"],
            "creative": ["inspiration", "ideas", "brainstorm"],
            "analytical": ["summary", "analysis", "breakdown"]
        }
        
        for domain, keywords in domain_boosts.items():
            if any(kw in context_lower for kw in keywords):
                for intent in keywords:
                    boosts[intent] = boosts.get(intent, 0) + 0.1
        
        return boosts
    
    def get_accuracy_stats(self) -> Dict[str, Any]:
        """Get prediction accuracy statistics"""
        if not self.intent_history:
            return {"total": 0, "accuracy": 0.0}
        
        correct = sum(1 for pred, actual in self.intent_history if pred == actual)
        return {
            "total": len(self.intent_history),
            "correct": correct,
            "accuracy": correct / len(self.intent_history) * 100
        }

# ═══════════════════════════════════════════════════════════════
# TASK ORCHESTRATOR - Breaks down and executes complex tasks
# ═══════════════════════════════════════════════════════════════
class TaskOrchestrator:
    """
    Decomposes complex tasks into executable sub-tasks
    """
    
    def __init__(self):
        self.task_queue: List[Dict[str, Any]] = []
        self.task_history: List[Dict[str, Any]] = []
    
    def is_complex_task(self, task: str) -> bool:
        """
        Determine if a task is complex enough to decompose
        """
        complexity_indicators = [
            r'\b(analyze|research|investigate|compile|summarize|compare)\b',
            r'\b(then|after|subsequently|finally|ultimately)\b',
            r'\b(multi-step|step-by-step|detailed)\b',
            r'\b(create|build|develop|implement).*\b(and|with|using)\b',
            len(task) > 100  # Long tasks are likely complex
        ]
        
        for indicator in complexity_indicators:
            if re.search(indicator, task, re.IGNORECASE):
                return True
        
        return False
    
    def decompose_task(self, task: str) -> List[Dict[str, Any]]:
        """
        Break down a complex task into sub-tasks
        """
        sub_tasks = []
        
        # Strategy 1: Split by conjunctions
        parts = re.split(r'\b(then|after|when|while|before|subsequently)\b', task, flags=re.IGNORECASE)
        if len(parts) > 2:
            for i, part in enumerate(parts[1:], 1):  # Skip first part (before conjunction)
                sub_task = self._clean_and_prioritize(part, priority=i)
                if sub_task:
                    sub_tasks.append(sub_task)
        
        # Strategy 2: Extract action-objects
        actions = [
            r'\b(understand|research|find out|investigate)\s+(.+?)(?:\s+(?:and|then))?',
            r'\b(create|build|make|develop)\s+(.+?)(?:\s+(?:and|then))?',
            r'\b(organize|structure|categorize)\s+(.+?)(?:\s+(?:and|then))?',
            r'\b(summarize|explain|document)\s+(.+?)(?:\s+(?:and|then))?'
        ]
        
        for pattern in actions:
            matches = re.findall(pattern, task, re.IGNORECASE)
            for match in matches:
                sub_task = self._clean_and_prioritize(match[0] if match else "", priority=len(sub_tasks))
                if sub_task:
                    sub_tasks.append(sub_task)
        
        # Strategy 3: Fallback - chunk by length
        if not sub_tasks and len(task) > 50:
            chunk_size = min(100, len(task) // 3)
            for i in range(0, len(task), chunk_size):
                chunk = task[i:i + chunk_size].strip()
                if chunk:
                    sub_tasks.append({
                        "description": chunk,
                        "priority": len(sub_tasks),
                        "estimated_effort": "medium"
                    })
        
        return sub_tasks if sub_tasks else [{"description": task, "priority": 1}]
    
    def _clean_and_prioritize(self, text: str, priority: int) -> Optional[Dict[str, Any]]:
        """Clean text and create task entry"""
        cleaned = re.sub(r'\b(then|after|when|while|before)\b', '', text, flags=re.IGNORECASE).strip()
        if not cleaned:
            return None
        
        return {
            "description": cleaned,
            "priority": priority,
            "estimated_effort": "low",
            "status": "pending"
        }
    
    def add_to_queue(self, task: Dict[str, Any]):
        """Add task to execution queue"""
        task["added_at"] = datetime.now().isoformat()
        self.task_queue.append(task)
        logger.info(f"📋 Task queued: {task['description'][:50]}...")
    
    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Get highest priority pending task"""
        pending = [t for t in self.task_queue if t["status"] == "pending"]
        if not pending:
            return None
        
        # Sort by priority
        pending.sort(key=lambda x: x.get("priority", 0))
        return pending[0]
    
    def mark_complete(self, task_id: str):
        """Mark a task as complete"""
        for task in self.task_queue:
            if task.get("id") == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                self.task_history.append(task.copy())
                logger.info(f"✅ Task completed: {task['description'][:50]}...")
                return True
        return False
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get queue status"""
        return {
            "total": len(self.task_queue),
            "pending": len([t for t in self.task_queue if t["status"] == "pending"]),
            "in_progress": len([t for t in self.task_queue if t["status"] == "in_progress"]),
            "completed": len([t for t in self.task_queue if t["status"] == "completed"])
        }

# ═══════════════════════════════════════════════════════════════
# MAIN PROACTIVE ASSISTANT CLASS
# ═══════════════════════════════════════════════════════════════
class ProactiveAssistant:
    """
    Main orchestrator combining all proactive intelligence components
    """
    
    def __init__(self):
        self.pattern_matcher = PatternMatcher()
        self.intent_predictor = IntentPredictor()
        self.task_orchestrator = TaskOrchestrator()
        self.reasoning_engine = None  # Will be set by kernel.py
        
        logger.info("🚀 Proactive Intelligence initialized")
    
    async def process_input(self, user_input: str, conversation_context: List[str] = None) -> Dict[str, Any]:
        """
        Main processing pipeline for proactive intelligence
        """
        result = {
            "original_input": user_input,
            "predictions": [],
            "actions": [],
            "pattern_match": None
        }
        
        # 1. Check for pattern matches
        pattern = self.pattern_matcher.find_pattern()
        if pattern:
            result["pattern_match"] = pattern
            result["actions"].append({
                "type": "routine_activation",
                "routine": pattern.get("routine"),
                "confidence": pattern.get("confidence")
            })
        
        # 2. Predict next intents
        predictions = self.intent_predictor.predict_next_intent(
            current_intent=user_input[:50],
            conversation_context=conversation_context or []
        )
        result["predictions"] = predictions
        
        # 3. Check if task needs decomposition
        if self.task_orchestrator.is_complex_task(user_input):
            sub_tasks = self.task_orchestrator.decompose_task(user_input)
            for sub_task in sub_tasks:
                self.task_orchestrator.add_to_queue(sub_task)
            result["actions"].append({
                "type": "task_decomposition",
                "sub_tasks_count": len(sub_tasks)
            })
        
        # 4. Generate reasoning if reasoning engine is available
        if self.reasoning_engine and pattern:
            action = pattern.get("routine", [user_input])[0] if pattern.get("routine") else user_input
            context = {
                "emotion": {"dominant_emotion": "curious"},
                "action": action,
                "topic": user_input[:50]
            }
            
            try:
                thought = await self.reasoning_engine.generate_rationalization(
                    action=action,
                    context=context
                )
                result["reasoning"] = {
                    "thought_id": thought.get("id"),
                    "rationalization": thought.get("content"),
                    "thought_type": thought.get("type"),
                    "processing_time_ms": thought.get("processing_time")
                }
            except Exception as e:
                logger.error(f"Reasoning generation error: {e}")
        
        # 5. Record this input for future prediction
        self.intent_predictor.record_prediction(
            predicted_intent="user_query",
            actual_intent=user_input[:100]
        )
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive status"""
        return {
            "patterns": len(self.pattern_matcher.patterns),
            "intent_accuracy": self.intent_predictor.get_accuracy_stats(),
            "task_queue": self.task_orchestrator.get_queue_status()
        }

# ═══════════════════════════════════════════════════════════════
# INITIALIZATION
# ═══════════════════════════════════════════════════════════════
proactive_assistant = ProactiveAssistant()