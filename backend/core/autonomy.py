# ============================================================================
# LUCY_OS 2.0 - Autonomous Heartbeat System
# HooRii Protocol v2.0 | Heartbeat Monitoring | System Health | Proactive Tasks
# ============================================================================
import asyncio
import logging
import time
import random
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from enum import Enum

from core.memory import memory
from core.emotion import emotion
from core.llm import llm
from core.routines import UnifiedRoutineEngine

logger = logging.getLogger("LucyAutonomy")

# Import security module for biometric verification
try:
    from api.security import (
        load_model,
        verify_typing_rhythm,
        trigger_lockdown,
        MODEL_PATH,
        anomaly_threshold
    )
    BIOMETRIC_ENABLED = True
except ImportError:
    BIOMETRIC_ENABLED = False
    logger.warning("Biometric verification module not available")

class SystemHealth(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    DEGRADED = "degraded"

class HeartbeatMonitor:
    """
    System heartbeat monitoring with proactive health checks
    
    Features:
    - Heartbeat tracking with timeout detection
    - System health scoring
    - Component status monitoring
    - Automatic recovery triggers
    """
    
    def __init__(self, heartbeat_timeout: int = 30):
        self.heartbeat_timeout = heartbeat_timeout
        self._heartbeats: Dict[str, float] = {}
        self._last_heartbeat: Dict[str, float] = {}
        self._health_score = 100
        self._components: Dict[str, Dict[str, Any]] = {
            "llm": {"status": "unknown", "last_heartbeat": None, "failures": 0},
            "memory": {"status": "unknown", "last_heartbeat": None, "failures": 0},
            "emotion": {"status": "unknown", "last_heartbeat": None, "failures": 0},
            "vision": {"status": "unknown", "last_heartbeat": None, "failures": 0},
            "voice": {"status": "unknown", "last_heartbeat": None, "failures": 0},
            "kernel": {"status": "unknown", "last_heartbeat": None, "failures": 0},
        }
        self._recovery_callbacks: List[Callable] = []
        self._running = False
        self._monitor_task: Optional[asyncio.Task] = None
    
    async def heartbeat(self, component: str):
        """Record heartbeat for a component"""
        self._heartbeats[component] = time.time()
        self._last_heartbeat[component] = datetime.now().isoformat()
        self._components[component]["status"] = "healthy"
        self._components[component]["failures"] = 0
        logger.debug(f"💓 {component} heartbeat recorded")
    
    async def check_health(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        now = time.time()
        issues = []
        degraded_components = []
        
        for component, data in self._components.items():
            last_hb = self._last_heartbeat.get(component)
            if last_hb:
                try:
                    age = datetime.now() - datetime.fromisoformat(last_hb)
                    if age.total_seconds() > self.heartbeat_timeout:
                        data["status"] = "unresponsive"
                        data["failures"] += 1
                        issues.append(f"{component} unresponsive for {age.total_seconds():.1f}s")
                        self._health_score -= 10
                    elif data["failures"] > 0:
                        data["status"] = "degraded"
                        degraded_components.append(component)
                        self._health_score -= 5
                except Exception as e:
                    logger.error(f"Health check error for {component}: {e}")
            else:
                data["status"] = "unknown"
                self._health_score -= 5
        
        # Clamp health score
        self._health_score = max(0, min(100, self._health_score))
        
        # Determine overall status
        if self._health_score >= 80:
            status = SystemHealth.HEALTHY
        elif self._health_score >= 60:
            status = SystemHealth.WARNING
        elif self._health_score >= 40:
            status = SystemHealth.DEGRADED
        else:
            status = SystemHealth.CRITICAL
        
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "status": status.value,
            "health_score": self._health_score,
            "components": self._components.copy(),
            "issues": issues,
            "degraded_components": degraded_components
        }
        
        logger.info(f"🏥 System Health: {status.value} (Score: {self._health_score})")
        
        # Trigger recovery if critical
        if status == SystemHealth.CRITICAL:
            await self._trigger_recovery()
        
        return health_report
    
    async def _trigger_recovery(self):
        """Trigger automatic recovery procedures"""
        logger.warning("🚨 System health critical - initiating recovery...")
        
        # Run recovery callbacks
        for callback in self._recovery_callbacks:
            try:
                await callback()
            except Exception as e:
                logger.error(f"Recovery callback error: {e}")
        
        # Reset health score
        self._health_score = 100
        for component in self._components.values():
            component["failures"] = 0
    
    def on_recovery(self, callback: Callable):
        """Register recovery callback"""
        self._recovery_callbacks.append(callback)
    
    async def start_monitoring(self, interval: int = 10):
        """Start continuous health monitoring"""
        self._running = True
        
        async def monitor_loop():
            while self._running:
                try:
                    await self.check_health()
                    await asyncio.sleep(interval)
                except Exception as e:
                    logger.error(f"Health monitoring error: {e}")
                    await asyncio.sleep(interval)
        
        self._monitor_task = asyncio.create_task(monitor_loop())
        logger.info(f"🏥 Health monitoring started (interval: {interval}s)")
    
    def stop_monitoring(self):
        """Stop health monitoring"""
        self._running = False
        if self._monitor_task:
            self._monitor_task.cancel()
        logger.info("🏥 Health monitoring stopped")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get current health status"""
        return {
            "health_score": self._health_score,
            "status": self._get_status_from_score(self._health_score),
            "components": self._components.copy()
        }
    
    def _get_status_from_score(self, score: int) -> str:
        if score >= 80:
            return SystemHealth.HEALTHY.value
        elif score >= 60:
            return SystemHealth.WARNING.value
        elif score >= 40:
            return SystemHealth.DEGRADED.value
        return SystemHealth.CRITICAL.value


class ProactiveTaskGenerator:
    """
    Generates proactive tasks based on system state and user patterns
    
    Features:
    - Pattern-based task generation
    - Time-based scheduling
    - Context-aware suggestions
    - Learning from user interactions
    """
    
    def __init__(self):
        self._user_patterns: Dict[str, Any] = {}
        self._task_history: List[Dict[str, Any]] = []
        self._task_templates = self._load_templates()
        self._learning_enabled = True
    
    def _load_templates(self) -> List[Dict[str, Any]]:
        """Load task generation templates"""
        return [
            {
                "name": "follow_up_research",
                "trigger": "conversation_completed",
                "template": "Based on our discussion about {topic}, I found some additional resources you might find interesting: {resources}",
                "priority": 3
            },
            {
                "name": "summarize_conversation",
                "trigger": "conversation_length_threshold",
                "template": "Here's a summary of our conversation: {summary}",
                "priority": 2
            },
            {
                "name": "proactive_assistance",
                "trigger": "user_seems_stuck",
                "template": "I noticed you might be having trouble with {task}. Let me help you with that.",
                "priority": 5
            },
            {
                "name": "knowledge_update",
                "trigger": "new_information_detected",
                "template": "I've learned something new: {information}. Would you like me to update my knowledge base?",
                "priority": 4
            },
            {
                "name": "wellness_check",
                "trigger": "time_based",
                "template": "How are you feeling today? I'm here if you need to talk.",
                "priority": 1
            },
            {
                "name": "task_suggestion",
                "trigger": "idle_time",
                "template": "I noticed you've been working on {context}. Would you like suggestions for next steps?",
                "priority": 3
            }
        ]
    
    async def generate_proactive_tasks(self, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Generate proactive tasks based on current context
        
        Args:
            context: Current system context
            
        Returns:
            List of proactive task suggestions
        """
        if context is None:
            context = {}
        
        tasks = []
        now = datetime.now()
        
        # Time-based tasks
        hour = now.hour
        if 9 <= hour <= 17:
            tasks.append({
                "type": "productivity",
                "message": "It's a great time to focus on your work. Is there anything you'd like help with?",
                "priority": 2,
                "timestamp": now.isoformat()
            })
        
        # Check for long idle periods
        if context.get("idle_time_minutes", 0) > 30:
            tasks.append({
                "type": "engagement",
                "message": "I've noticed you've been idle for a while. Is there anything I can help you with?",
                "priority": 3,
                "timestamp": now.isoformat()
            })
        
        # Emotion-based tasks
        emotion_state = context.get("emotion", {})
        if emotion_state.get("dominant_emotion") == "anxious":
            tasks.append({
                "type": "wellness",
                "message": "I sense you might be feeling anxious. Would you like to talk about what's on your mind?",
                "priority": 5,
                "timestamp": now.isoformat()
            })
        elif emotion_state.get("dominant_emotion") == "frustrated":
            tasks.append({
                "type": "support",
                "message": "I can see you're frustrated. Let me help you work through this.",
                "priority": 5,
                "timestamp": now.isoformat()
            })
        
        # Conversation-based tasks
        if context.get("conversation_length", 0) > 10:
            tasks.append({
                "type": "summarization",
                "message": "We've had quite a conversation. Would you like me to summarize the key points?",
                "priority": 2,
                "timestamp": now.isoformat()
            })
        
        # Learn from patterns
        if self._learning_enabled:
            pattern_tasks = await self._generate_from_patterns(context)
            tasks.extend(pattern_tasks)
        
        return tasks
    
    async def _generate_from_patterns(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate tasks based on learned user patterns"""
        tasks = []
        
        # Check for recurring topics
        recent_topics = context.get("topics", [])
        if len(recent_topics) >= 3:
            common_topic = max(set(recent_topics), key=recent_topics.count)
            tasks.append({
                "type": "topic_follow_up",
                "message": f"I notice we've been discussing {common_topic} frequently. Is there anything specific you'd like to explore?",
                "priority": 3,
                "timestamp": datetime.now().isoformat()
            })
        
        return tasks
    
    def record_interaction(self, interaction: Dict[str, Any]):
        """Record interaction for pattern learning"""
        self._task_history.append({
            "timestamp": datetime.now().isoformat(),
            "interaction": interaction,
            "user_response": interaction.get("response")
        })
        
        # Update patterns
        if interaction.get("topic"):
            self._user_patterns["topics"].append(interaction["topic"])
        
        # Keep only recent history
        if len(self._task_history) > 100:
            self._task_history = self._task_history[-50:]
    
    def get_user_patterns(self) -> Dict[str, Any]:
        """Get learned user patterns"""
        return {
            "topics": self._user_patterns.get("topics", []),
            "interaction_count": len(self._task_history)
        }


class BiometricVerifier:
    """
    Biometric typing rhythm verification system
    
    Features:
    - Real-time typing rhythm verification
    - One-Class SVM anomaly detection
    - Lock-Down Protocol trigger
    - Adaptive sensitivity based on user state
    """
    
    def __init__(self):
        self._key_buffer = []  # Buffer of recent key events
        self._key_buffer_size = 50  # Verify every 50 keystrokes
        self._verification_count = 0
        self._anomaly_count = 0
        self._last_warning_time = None
        self._sensitivity_multiplier = 1.0  # Adaptive sensitivity
        self._running = False
        self._verification_task: Optional[asyncio.Task] = None
    
    async def record_key_event(self, key_data: Dict[str, Any]):
        """Record a key event for biometric verification"""
        self._key_buffer.append(key_data)
        
        # Keep buffer size manageable
        if len(self._key_buffer) > 200:
            self._key_buffer = self._key_buffer[-100:]
        
        # Check if we should verify
        if len(self._key_buffer) >= self._key_buffer_size:
            await self._verify_rhythm()
    
    async def _verify_rhythm(self):
        """Verify typing rhythm against biometric model"""
        if not BIOMETRIC_ENABLED:
            return
        
        self._verification_count += 1
        
        try:
            # Get recent key events for verification
            recent_keys = self._key_buffer[-self._key_buffer_size:]
            
            if len(recent_keys) < 5:
                return
            
            # Prepare key data for verification
            key_data_for_api = []
            for key in recent_keys:
                key_data_for_api.append({
                    'dwellTime': key.get('dwellTime', 0),
                    'flightTime': key.get('flightTime', 0),
                    'totalTime': key.get('totalTime', 0),
                    'key': key.get('key', '')
                })
            
            # Verify against model
            result = await self._call_verify_api(key_data_for_api)
            
            if result.get('success'):
                score = result.get('score', 0)
                action = result.get('action', 'none')
                is_verified = result.get('is_verified', True)
                consecutive_anomalies = result.get('consecutive_anomalies', 0)
                
                # Handle verification result
                if action == 'lockdown':
                    logger.warning(f"🚨 Biometric anomaly detected! Score: {score}%")
                    await self._trigger_lockdown(reason=f"Typing rhythm anomaly: {score}%")
                    self._anomaly_count += 1
                    self._sensitivity_multiplier = 1.5  # Increase sensitivity after anomaly
                
                elif action == 'warning':
                    logger.info(f"⚠️ Typing rhythm warning: Score: {score}%")
                    await self._handle_warning(score)
                    self._anomaly_count += 1
                
                elif action == 'none':
                    # Normal verification - reset anomaly count
                    self._anomaly_count = 0
                    self._sensitivity_multiplier = max(0.8, self._sensitivity_multiplier - 0.1)  # Gradually decrease sensitivity
                    logger.debug(f"✅ Biometric verification passed: Score: {score}%")
                
                # Log verification
                logger.debug(f"Biometric verification #{self._verification_count}: Score={score}, Action={action}")
            
        except Exception as e:
            logger.error(f"Biometric verification error: {e}")
    
    async def _call_verify_api(self, key_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Call the security API for verification"""
        try:
            import urllib.request
            import urllib.error
            
            # Use kernel endpoint at port 8000
            url = "http://localhost:8000/security/verify-biometric"
            data = json.dumps({
                'typing_data': key_data,
                'threshold': anomaly_threshold * self._sensitivity_multiplier
            }).encode('utf-8')
            
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode('utf-8'))
                
        except Exception as e:
            logger.error(f"API verification failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'score': 0,
                'is_verified': True,
                'action': 'none'
            }
    
    async def _trigger_lockdown(self, reason: str):
        """Trigger the Lock-Down Protocol"""
        logger.critical(f"🚨 LOCK-DOWN PROTOCOL TRIGGERED: {reason}")
        
        try:
            import urllib.request
            import urllib.error
            
            url = "http://localhost:5000/api/security/lockdown"
            data = json.dumps({'reason': reason}).encode('utf-8')
            
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                logger.critical(f"Lockdown result: {result}")
                
        except Exception as e:
            logger.critical(f"Failed to trigger lockdown: {e}")
            # Fallback: Direct actions
            await self._execute_local_lockdown(reason)
    
    async def _execute_local_lockdown(self, reason: str):
        """Execute local lockdown actions"""
        try:
            # Lock screen
            lock_script = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'scripts',
                'lock_screen.py'
            )
            if os.path.exists(lock_script):
                import subprocess
                subprocess.run(['python', lock_script], capture_output=True)
                logger.info("Screen locked")
            
            # Mute audio
            mute_script = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'scripts',
                'mute_audio.py'
            )
            if os.path.exists(mute_script):
                import subprocess
                subprocess.run(['python', mute_script], capture_output=True)
                logger.info("Audio muted")
            
            # Send Telegram alert
            telegram_script = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'scripts',
                'send_telegram_alert.py'
            )
            if os.path.exists(telegram_script):
                import subprocess
                subprocess.run(['python', telegram_script, reason], capture_output=True)
                logger.info("Telegram alert sent")
                
        except Exception as e:
            logger.error(f"Local lockdown failed: {e}")
    
    async def _handle_warning(self, score: float):
        """Handle typing rhythm warning - speak to user"""
        if self._last_warning_time and (time.time() - self._last_warning_time) < 300:  # 5 min cooldown
            return
        
        self._last_warning_time = time.time()
        
        # Use E2-TTS to speak to user
        try:
            from plugins.voice import voice
            
            message = "I notice your typing rhythm is changing, Dahen. Are you feeling tired? I'm adjusting the sensitivity for you."
            
            # Call voice plugin with E2 TTS
            await voice.speak(message)
            
            logger.info(f"Speaking to user about rhythm change: {message}")
            
        except Exception as e:
            logger.error(f"Failed to speak warning message: {e}")
    
    def get_verification_status(self) -> Dict[str, Any]:
        """Get current biometric verification status"""
        return {
            'enabled': BIOMETRIC_ENABLED,
            'verification_count': self._verification_count,
            'anomaly_count': self._anomaly_count,
            'consecutive_anomalies': self._anomaly_count,
            'sensitivity_multiplier': self._sensitivity_multiplier,
            'model_path': MODEL_PATH,
            'threshold': anomaly_threshold * self._sensitivity_multiplier
        }
    
    def reset(self):
        """Reset biometric verifier state"""
        self._key_buffer = []
        self._verification_count = 0
        self._anomaly_count = 0
        self._sensitivity_multiplier = 1.0
        self._last_warning_time = None
        logger.info("Biometric verifier reset")


class AutonomousHeartbeat:
    """
    Main autonomous heartbeat system combining health monitoring and proactive tasks
    
    Features:
    - Continuous system health monitoring
    - Proactive task generation
    - Self-healing mechanisms
    - Learning and adaptation
    - 20 proactive behaviors from ProactiveRoutineManager
    - 20 advanced behaviors from AdvancedRoutineManager
    - Biometric typing rhythm verification
    """
    
    def __init__(self):
        self._heartbeat_monitor = HeartbeatMonitor()
        self._task_generator = ProactiveTaskGenerator()
        self._running = False
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._task_task: Optional[asyncio.Task] = None
        self._last_proactive_check = 0
        self._proactive_interval = 60  # Check every 60 seconds
        
        # Biometric verifier
        self._biometric_verifier = BiometricVerifier()
        
        # Register recovery callbacks
        self._heartbeat_monitor.on_recovery(self._on_recovery)
        
        # Initialize UnifiedRoutineEngine (combines Proactive + Advanced + Omega)
        self._routine_engine = UnifiedRoutineEngine()
    
    async def start(self):
        """Start autonomous heartbeat system"""
        self._running = True
        
        # Start health monitoring
        await self._heartbeat_monitor.start_monitoring(interval=10)
        
        # Start proactive task generation
        asyncio.create_task(self._proactive_task_loop())
        
        # Start UnifiedRoutineEngine (combines Proactive + Advanced + Omega)
        await self._routine_engine.start()
        
        # Start thought loop
        asyncio.create_task(self.start_thought_loop())
        
        logger.info("💓 Autonomous Heartbeat System Started")
        logger.info("🧠 ProactiveRoutineManager (20 behaviors) initialized")
        logger.info("🔬 AdvancedRoutineManager (20 advanced behaviors) initialized")
    
    async def stop(self):
        """Stop autonomous heartbeat system"""
        self._running = False
        
        self._heartbeat_monitor.stop_monitoring()
        
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        
        if self._task_task:
            self._task_task.cancel()
        
        # Stop UnifiedRoutineEngine
        await self._routine_engine.stop()
        
        logger.info("💓 Autonomous Heartbeat System Stopped")
        logger.info("🧠 ProactiveRoutineManager stopped")
        logger.info("🔬 AdvancedRoutineManager stopped")
    
    async def _proactive_task_loop(self):
        """Loop for generating proactive tasks"""
        while self._running:
            try:
                # Get current context
                context = await self._get_current_context()
                
                # Generate proactive tasks
                tasks = await self._task_generator.generate_proactive_tasks(context)
                
                if tasks:
                    logger.info(f"💡 Proactive tasks generated: {len(tasks)}")
                    # Send to kernel for processing
                    await self._send_to_kernel(tasks)
                
                await asyncio.sleep(self._proactive_interval)
                
            except Exception as e:
                logger.error(f"Proactive task loop error: {e}")
                await asyncio.sleep(self._proactive_interval)
    
    async def _get_current_context(self) -> Dict[str, Any]:
        """Get current system context"""
        return {
            "emotion": emotion.get_state(),
            "idle_time_minutes": 0,  # Would be calculated from activity tracking
            "conversation_length": 0,  # Would be tracked
            "topics": [],  # Would be extracted from conversation
            "health": self._heartbeat_monitor.get_health_status(),
            "routines": {
                "routine_engine": {
                    "status": self._routine_engine.get_status()
                }
            }
        }
    
    async def _send_to_kernel(self, tasks: List[Dict[str, Any]]):
        """Send proactive tasks to kernel for processing"""
        # This would integrate with the kernel module
        logger.info(f"📋 Sending {len(tasks)} proactive tasks to kernel")
    
    async def _on_recovery(self):
        """Callback after system recovery"""
        logger.info("✅ System recovery complete")
        emotion.set_state({
            "dominant_emotion": "relieved",
            "intensity": 0.5,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get current health status"""
        return self._heartbeat_monitor.get_health_status()
    
    def get_proactive_tasks(self) -> List[Dict[str, Any]]:
        """Get available proactive task templates"""
        return self._task_generator._task_templates
    
    def get_routine_status(self) -> Dict[str, Any]:
        """Get combined routine engine status"""
        return self._routine_engine.get_status()
    
    async def start_thought_loop(self):
        """Start the thought loop for reasoning integration"""
        while self._running:
            try:
                # Generate a rationalization every 30 seconds
                await asyncio.sleep(30)
                
                # Get current context
                context = await self._get_current_context()
                
                # Generate rationalization
                thought = await self._routine_engine.generate_rationalization(
                    action="system_thought",
                    context=context
                )
                
                if thought:
                    logger.debug(f"Thought: {thought}")
                    
            except Exception as e:
                logger.error(f"Thought loop error: {e}")
                await asyncio.sleep(30)


# ============================================================================
# GLOBAL INSTANCES
# ============================================================================
heartbeat = AutonomousHeartbeat()
autonomy = heartbeat  # Alias for backward compatibility
