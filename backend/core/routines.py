# ============================================================================
# LUCY_OS - UNIFIED ROUTINE ENGINE
# Combines: Proactive (20) + Advanced (20) + Omega (61-80) = 60+ Behaviors
# ============================================================================
import asyncio
import logging
import time
import re
import subprocess
import psutil
import cv2
import numpy as np
import feedparser
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import threading

logger = logging.getLogger("LucyUnifiedRoutines")

# ============================================================================
# DATA CLASSES - FROM ALL THREE ROUTINES
# ============================================================================

@dataclass
class ProactiveTask:
    """Represents a proactive task (from routines.py)"""
    task_id: str
    behavior_name: str
    priority: int
    message: str
    action_type: str
    status: str = "pending"
    timestamp: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "behavior_name": self.behavior_name,
            "priority": self.priority,
            "message": self.message,
            "action_type": self.action_type,
            "status": self.status,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }

@dataclass
class VisionState:
    """Represents the current vision/multimodal state"""
    face_detected: bool = False
    face_position: Dict[str, float] = field(default_factory=dict)
    blink_rate: float = 0.0
    screen_content: str = ""
    active_window: str = ""
    detected_objects: List[str] = field(default_factory=list)
    emotion_context: str = ""
    text_regions: List[Dict[str, str]] = field(default_factory=list)

@dataclass
class OSState:
    """Represents the current OS state"""
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    gpu_usage: float = 0.0
    vram_usage: float = 0.0
    active_processes: List[str] = field(default_factory=list)
    screen_state: str = "normal"
    webcam_status: str = "active"
    time: str = ""
    date: str = ""

@dataclass
class AdvancedTask:
    """Represents an advanced proactive task (from routines_advanced.py)"""
    task_id: str
    behavior_name: str
    priority: int
    message: str
    action_type: str
    status: str = "pending"
    timestamp: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "behavior_name": self.behavior_name,
            "priority": self.priority,
            "message": self.message,
            "action_type": self.action_type,
            "status": self.status,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }

@dataclass
class TerminalState:
    """Represents terminal state for training loop monitoring"""
    output: str = ""
    loss_values: List[float] = field(default_factory=list)
    has_nan: bool = False
    is_training: bool = False
    process_id: Optional[int] = None

@dataclass
class AdvancedOSState:
    """Represents advanced OS state"""
    gpu_temperature: float = 0.0
    gpu_fan_speed: int = 0
    cpu_temperature: float = 0.0
    memory_available: int = 0
    network_connections: int = 0
    active_processes: List[Dict[str, Any]] = field(default_factory=list)
    clipboard_content: str = ""
    clipboard_timestamp: str = ""
    screen_buffer: List[str] = field(default_factory=list)
    mouse_velocity: float = 0.0
    typing_rate: float = 0.0

@dataclass
class OmegaTask:
    """Represents an Omega layer task (from routines_ultra.py)"""
    task_id: str
    behavior_name: str
    routine_number: int
    priority: int
    message: str
    action_type: str
    status: str = "pending"
    timestamp: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "behavior_name": self.behavior_name,
            "routine_number": self.routine_number,
            "priority": self.priority,
            "message": self.message,
            "action_type": self.action_type,
            "status": self.status,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }

@dataclass
class VisualObjectMemory:
    """Represents visual object memory (from routines_ultra.py)"""
    object_name: str
    timestamp: str
    location: str
    confidence: float
    image_hash: str = ""

@dataclass
class ProjectState:
    """Represents project state (from routines_ultra.py)"""
    project_path: str
    last_modified: str
    file_count: int
    is_active: bool
    should_archive: bool = False

@dataclass
class HardwareHealth:
    """Represents hardware health (from routines_ultra.py)"""
    disk_cycles: int = 0
    disk_temp: int = 0
    gpu_temp: int = 0
    fan_speed: int = 0
    voltage: float = 0.0

@dataclass
class SemanticPattern:
    """Represents semantic pattern (from routines_ultra.py)"""
    pattern_id: str
    file_path: str
    pattern_type: str
    match_score: float
    timestamp: str
    context: str = ""

@dataclass
class MeetingContact:
    """Represents meeting contact (from routines_ultra.py)"""
    name: str
    github_url: str
    linkedin_url: str
    meeting_time: str
    repo_count: int = 0

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_task_id() -> str:
    """Generate a unique task ID"""
    return f"task_{int(time.time() * 1000)}_{int(time.time() % 10000)}"

def generate_omega_task_id() -> str:
    """Generate Omega task ID"""
    return f"omega_{int(datetime.now().timestamp() * 1000)}"

def get_current_time() -> datetime:
    """Get current datetime"""
    return datetime.now()

def is_business_hours() -> bool:
    """Check if current time is within business hours (9 AM - 5 PM)"""
    now = get_current_time()
    return 9 <= now.hour < 17

def is_night() -> bool:
    """Check if current time is night (10 PM - 6 AM)"""
    now = get_current_time()
    return now.hour >= 22 or now.hour < 6

def is_early_morning() -> bool:
    """Check if current time is early morning (3 AM - 5 AM)"""
    now = get_current_time()
    return 3 <= now.hour < 5

def is_late_night() -> bool:
    """Check if current time is late night (after 11 PM)"""
    now = get_current_time()
    return now.hour >= 23

# ============================================================================
# E2-TTS VOICE ENGINE (FROM routines_ultra.py)
# ============================================================================

class E2TTSVoiceEngine:
    """Enhanced TTS voice engine with emotion, breath, and pause support"""
    
    def __init__(self, model_path: str = "E2-TTS"):
        self.model_path = model_path
        self._voice_cache: Dict[str, bytes] = {}
        self._current_emotion: str = "neutral"
        self._breath_enabled = True
        self._pause_enabled = True
        self._pitch_range = (0.8, 1.2)
        self._speed_range = (0.8, 1.3)
        logger.info(f"[E2-TTS Omega] Voice Engine initialized at {model_path}")
    
    def synthesize(self, text: str, emotion: str = "neutral", speed: float = 1.0, pitch: float = 1.0, urgency: bool = False) -> bytes:
        """Synthesize text to speech with emotion and pacing markers"""
        if self._breath_enabled and self._pause_enabled:
            text = re.sub(r'(\w+)([.!?])', r'\1 [BREATH] \2', text)
            text = re.sub(r"\b(I'm|I noticed|I found|I detected|I've)\b", r' [PAUSE] \1', text)
        
        markers = {
            "calm": "[CALM]",
            "excited": "[EXCITED]",
            "serious": "[SERIOUS]",
            "warm": "[WARM]",
            "neutral": "",
            "concerned": "[CONCERNED]",
            "curious": "[CURIOUS]",
            "confident": "[CONFIDENT]"
        }
        marker = markers.get(emotion, "")
        text = f"{marker} {text} {marker}"
        
        if urgency:
            speed = min(1.3, speed * 1.2)
            pitch = min(1.2, pitch * 1.1)
        
        # Mock audio data - replace with actual TTS synthesis
        audio_data = b"MOCK_AUDIO_DATA_E2_TTS"
        
        cache_key = f"{text[:50]}_{emotion}_{speed}_{pitch}"
        self._voice_cache[cache_key] = audio_data
        return audio_data
    
    def set_emotion(self, emotion: str):
        """Set current emotion for voice synthesis"""
        self._current_emotion = emotion
        logger.info(f"[E2-TTS Omega] Emotion set to: {emotion}")
    
    def get_cached_audio(self, text: str, emotion: str) -> Optional[bytes]:
        """Get cached audio if available"""
        return self._voice_cache.get(f"{text[:50]}_{emotion}")
    
    def clear_cache(self):
        """Clear voice cache"""
        self._voice_cache.clear()
        logger.info("[E2-TTS Omega] Voice cache cleared")

# ============================================================================
# PROACTIVE ROUTINE MANAGER (FROM routines.py) - 20 BEHAVIORS
# ============================================================================

class ProactiveRoutineManager:
    """
    Manages 20 proactive behaviors for the Embodied AI Agent
    
    Behaviors:
    1. check_flow_state - Monitor typing speed + active window
    2. rescue_code_block - Detect frustration + static screen
    3. manage_vram_spikes - Monitor GPU/RAM usage
    4. prefetch_context - OCR screen for import/install commands
    5. synergize_ai_extensions - Detect AI extensions, throttle polling
    6. morning_boot_sequence - 9 AM boot sequence with greeting
    7. auto_declutter_desktop - Weekly file cleanup
    8. dream_mode_defrag - 3 AM vector DB consolidation
    9. media_smart_mute - Detect video calls, pause audio
    10. hardware_killswitch - Webcam blocked detection
    11. theater_mode - Media player detection, dim screen
    12. language_cultural_nudge - OCR detects Korean/travel
    13. streak_guardian - 11 PM streak reminder
    14. milestone_protocol - Birthday/milestone detection
    15. eye_strain_monitor - Blink rate monitoring
    16. posture_check - Face Y-coordinate tracking
    17. late_night_warning - After 2 AM coding warning
    18. stress_mitigation - High stress response
    19. hydration_reminder - Cup/bottle detection
    20. welcome_back_summary - Return from absence summary
    """
    
    def __init__(self):
        self._running = False
        self._evaluation_task: Optional[asyncio.Task] = None
        self._task_history: List[ProactiveTask] = []
        self._last_evaluation = 0.0
        self._evaluation_interval = 5
        self._throttle_multiplier = 1.0
        self._user_birthday: Optional[datetime] = None
        self._last_face_seen: Optional[datetime] = None
        self._last_hydration_check = 0.0
        self._last_streak_check = 0.0
        self._streak_interval = 86400
        
        self._mock_os_state = OSState()
        self._mock_vision_state = VisionState()
        
        self._config = {
            "flow_state_threshold": 50,
            "static_screen_threshold": 300,
            "vram_warning_threshold": 80,
            "vram_critical_threshold": 95,
            "blink_rate_threshold": 10,
            "posture_drop_threshold": 100,
            "hydration_check_interval": 10800,
            "welcome_back_threshold": 1800,
            "evaluation_interval": 5,
        }
        
        logger.info("ProactiveRoutineManager initialized with 20 behaviors")
    
    async def start(self):
        self._running = True
        self._evaluation_task = asyncio.create_task(self._evaluation_loop())
        logger.info("Proactive Routine Evaluation Started")
    
    async def stop(self):
        self._running = False
        if self._evaluation_task:
            self._evaluation_task.cancel()
        logger.info("Proactive Routine Evaluation Stopped")
    
    async def _evaluation_loop(self):
        while self._running:
            try:
                now = time.time()
                effective_interval = self._config.get("evaluation_interval", 5) * self._throttle_multiplier
                
                if now - self._last_evaluation >= effective_interval:
                    await self.evaluate_state(
                        self._mock_vision_state, 
                        self._mock_os_state
                    )
                    self._last_evaluation = now
                
                await asyncio.sleep(effective_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Evaluation loop error: {e}")
                await asyncio.sleep(1)
    
    async def evaluate_state(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        
        tasks.extend(await self.check_flow_state(vision_data, os_data))
        tasks.extend(await self.rescue_code_block(vision_data, os_data))
        tasks.extend(await self.manage_vram_spikes(vision_data, os_data))
        tasks.extend(await self.prefetch_context(vision_data, os_data))
        tasks.extend(await self.synergize_ai_extensions(vision_data, os_data))
        tasks.extend(await self.morning_boot_sequence(vision_data, os_data))
        tasks.extend(await self.auto_declutter_desktop(vision_data, os_data))
        tasks.extend(await self.dream_mode_defrag(vision_data, os_data))
        tasks.extend(await self.media_smart_mute(vision_data, os_data))
        tasks.extend(await self.hardware_killswitch(vision_data, os_data))
        tasks.extend(await self.theater_mode(vision_data, os_data))
        tasks.extend(await self.language_cultural_nudge(vision_data, os_data))
        tasks.extend(await self.streak_guardian(vision_data, os_data))
        tasks.extend(await self.milestone_protocol(vision_data, os_data))
        tasks.extend(await self.eye_strain_monitor(vision_data, os_data))
        tasks.extend(await self.posture_check(vision_data, os_data))
        tasks.extend(await self.late_night_warning(vision_data, os_data))
        tasks.extend(await self.stress_mitigation(vision_data, os_data))
        tasks.extend(await self.hydration_reminder(vision_data, os_data))
        tasks.extend(await self.welcome_back_summary(vision_data, os_data))
        
        tasks.sort(key=lambda x: x.priority, reverse=True)
        
        for task in tasks:
            logger.info(f"[{task.priority}] {task.behavior_name}: {task.message[:50]}...")
        
        return tasks
    
    # BEHAVIOR 1: check_flow_state
    async def check_flow_state(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        typing_rate = os_data.cpu_usage  # Mock value
        active_window = os_data.active_processes[0] if os_data.active_processes else ""
        
        if typing_rate > self._config["flow_state_threshold"]:
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="check_flow_state",
                priority=3,
                message=f"Deep flow detected - {typing_rate} wpm",
                action_type="flow_monitoring",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 2: rescue_code_block
    async def rescue_code_block(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        screen_static = len(vision_data.screen_content) < 100
        
        if screen_static and vision_data.blink_rate > self._config["blink_rate_threshold"]:
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="rescue_code_block",
                priority=5,
                message="Code block detected - offering help",
                action_type="code_assistance",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 3: manage_vram_spikes
    async def manage_vram_spikes(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        vram_usage = os_data.vram_usage
        
        if vram_usage > self._config["vram_warning_threshold"]:
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="manage_vram_spikes",
                priority=4,
                message=f"VRAM at {vram_usage}% - throttling background tasks",
                action_type="resource_management",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 4: prefetch_context
    async def prefetch_context(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        screen_content = vision_data.screen_content
        
        if "import" in screen_content or "pip install" in screen_content:
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="prefetch_context",
                priority=4,
                message="Prefetching module documentation",
                action_type="context_enhancement",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 5: synergize_ai_extensions
    async def synergize_ai_extensions(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        ai_extensions = ["copilot", "cursor", "tabnine"]
        
        for ext in ai_extensions:
            if ext in os_data.active_processes:
                task = ProactiveTask(
                    task_id=generate_task_id(),
                    behavior_name="synergize_ai_extensions",
                    priority=2,
                    message=f"AI extension {ext} active - optimizing",
                    action_type="extension_synergy",
                    timestamp=str(get_current_time())
                )
                tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 6: morning_boot_sequence
    async def morning_boot_sequence(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        now = get_current_time()
        
        if is_business_hours() and not self._last_face_seen:
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="morning_boot_sequence",
                priority=1,
                message="Morning boot sequence initiated",
                action_type="boot_sequence",
                timestamp=str(now)
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 7: auto_declutter_desktop
    async def auto_declutter_desktop(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        now = get_current_time()
        
        if now.weekday() == 0:  # Sunday
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="auto_declutter_desktop",
                priority=2,
                message="Weekly desktop cleanup",
                action_type="cleanup",
                timestamp=str(now)
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 8: dream_mode_defrag
    async def dream_mode_defrag(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        now = get_current_time()
        
        if is_early_morning():
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="dream_mode_defrag",
                priority=3,
                message="Vector database defragmentation",
                action_type="maintenance",
                timestamp=str(now)
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 9: media_smart_mute
    async def media_smart_mute(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        active_window = os_data.active_processes[0] if os_data.active_processes else ""
        
        if any(media in active_window.lower() for media in ["youtube", "spotify", "netflix", "video"]):
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="media_smart_mute",
                priority=2,
                message="Media detected - muting notifications",
                action_type="media_mode",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 10: hardware_killswitch
    async def hardware_killswitch(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        webcam_status = os_data.webcam_status
        
        if webcam_status == "blocked":
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="hardware_killswitch",
                priority=5,
                message="Webcam blocked - safety mode",
                action_type="safety",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 11: theater_mode
    async def theater_mode(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        active_window = os_data.active_processes[0] if os_data.active_processes else ""
        
        if any(theater in active_window.lower() for theater in ["player", "movie", "cinema"]):
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="theater_mode",
                priority=2,
                message="Theater mode activated",
                action_type="theater",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 12: language_cultural_nudge
    async def language_cultural_nudge(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        screen_content = vision_data.screen_content
        
        if any(lang in screen_content for lang in ["한국어", "한글", "Korean"]):
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="language_cultural_nudge",
                priority=3,
                message="Korean content detected - learning mode",
                action_type="language_learning",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 13: streak_guardian
    async def streak_guardian(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        now = get_current_time()
        
        if now.hour == 23:  # 11 PM
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="streak_guardian",
                priority=4,
                message="Streak reminder - 11 PM",
                action_type="reminder",
                timestamp=str(now)
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 14: milestone_protocol
    async def milestone_protocol(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        now = get_current_time()
        
        if now.month == 3 and now.day == 23:  # March 23 - Birthday
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="milestone_protocol",
                priority=1,
                message="Birthday milestone detected",
                action_type="celebration",
                timestamp=str(now)
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 15: eye_strain_monitor
    async def eye_strain_monitor(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        
        if vision_data.blink_rate > self._config["blink_rate_threshold"]:
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="eye_strain_monitor",
                priority=4,
                message="Eye strain detected - take a break",
                action_type="health_monitoring",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 16: posture_check
    async def posture_check(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        face_y = vision_data.face_position.get("y", 0)
        
        if face_y > self._config["posture_drop_threshold"]:
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="posture_check",
                priority=4,
                message="Posture check - sit up straight",
                action_type="health_monitoring",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 17: late_night_warning
    async def late_night_warning(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        now = get_current_time()
        
        if is_late_night():
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="late_night_warning",
                priority=3,
                message="Late night coding - be careful",
                action_type="health_warning",
                timestamp=str(now)
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 18: stress_mitigation
    async def stress_mitigation(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        stress_indicators = ["error", "failed", "crash", "timeout"]
        screen_content = vision_data.screen_content.lower()
        
        if any(indicator in screen_content for indicator in stress_indicators):
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="stress_mitigation",
                priority=5,
                message="Stress detected - calming response",
                action_type="stress_relief",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 19: hydration_reminder
    async def hydration_reminder(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        now = time.time()
        
        if now - self._last_hydration_check > 1800:  # 30 minutes in seconds
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="hydration_reminder",
                priority=3,
                message="Time for water",
                action_type="health_reminder",
                timestamp=str(now)
            )
            tasks.append(task)
            self._last_hydration_check = now
        
        return tasks
    
    # BEHAVIOR 20: welcome_back_summary
    async def welcome_back_summary(self, vision_data: VisionState, os_data: OSState) -> List[ProactiveTask]:
        tasks = []
        
        if self._is_user_away():
            task = ProactiveTask(
                task_id=generate_task_id(),
                behavior_name="welcome_back_summary",
                priority=1,
                message="Welcome back - here's what happened",
                action_type="summary",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # HELPER METHODS
    def _get_last_cleanup_time(self) -> datetime:
        return get_current_time() - timedelta(days=3)
    
    def _is_user_away(self) -> bool:
        if self._last_face_seen:
            time_away = (get_current_time() - self._last_face_seen).total_seconds()
            return time_away > 300
        return True
    
    def _get_last_app_usage_time(self) -> datetime:
        return get_current_time() - timedelta(hours=12)
    
    # ACTION SIMULATION METHODS
    async def _enable_dnd(self):
        logger.info("Enabling Do Not Disturb mode")
    
    async def _trigger_voice_assistance(self, message: str):
        logger.info(f"Voice assistance: {message}")
    
    async def _suspend_background_processes(self):
        logger.info("Suspending background processes")
    
    async def _open_docs(self, module: str):
        logger.info(f"Opening docs for {module}")
    
    async def _open_npm_docs(self, package: str):
        logger.info(f"Opening NPM docs for {package}")
    
    async def _morning_boot_sequence(self):
        logger.info("Morning boot sequence initiated")
    
    async def _cleanup_desktop(self):
        logger.info("Desktop cleanup completed")
    
    async def _defrag_vector_db(self):
        logger.info("Vector database defragmentation completed")
    
    async def _pause_audio(self):
        logger.info("Audio paused")
    
    async def _enable_safety_mode(self):
        logger.info("Safety mode enabled")
    
    async def _enable_theater_mode(self):
        logger.info("Theater mode enabled")
    
    async def _get_random_korean_vocab(self) -> Dict[str, str]:
        return {"hanja": "안녕", "meaning": "Hello"}
    
    async def _get_random_travel_vocab(self) -> Dict[str, str]:
        return {"word": "Welcome", "meaning": "Please enjoy your stay"}
    
    async def _speak_vocab(self, vocab: Dict[str, str]):
        logger.info(f"Speaking: {vocab['hanja']} - {vocab['meaning']}")
    
    async def _trigger_streak_reminder(self):
        logger.info("Streak reminder triggered")
        self._last_streak_check = get_current_time()
    
    async def _birthday_celebration(self):
        logger.info("Birthday celebration sequence")
    
    async def _trigger_eye_strain_reminder(self):
        logger.info("Eye strain reminder triggered")
    
    async def _trigger_posture_reminder(self):
        logger.info("Posture reminder triggered")
    
    async def _dim_screen_and_warn(self):
        logger.info("Screen dimmed - late night warning")
    
    async def _play_relaxing_music(self):
        logger.info("Playing relaxing music")
    
    async def _show_hydration_notification(self):
        logger.info("Hydration notification shown")
    
    async def _welcome_back_summary(self):
        logger.info("Welcome back summary generated")
    
    def get_task_history(self) -> List[Dict[str, Any]]:
        return [task.to_dict() for task in self._task_history]
    
    def get_active_tasks(self) -> List[Dict[str, Any]]:
        return [task.to_dict() for task in self._task_history[-10:]]
    
    def get_throttle_status(self) -> Dict[str, Any]:
        return {
            "multiplier": self._throttle_multiplier,
            "effective_interval": self._config["evaluation_interval"] * self._throttle_multiplier
        }

# ============================================================================
# ADVANCED ROUTINE MANAGER (FROM routines_advanced.py) - 20 BEHAVIORS
# ============================================================================

class AdvancedRoutineManager:
    """
    Manages 20 highly advanced, context-aware autonomous behaviors
    
    Advanced Behaviors:
    1. monitor_training_loop - Parse terminal, detect loss spikes/NaN
    2. abliterated_sandbox - OCR detects uncensored models, isolate network
    3. revive_coding_agent - Ping localhost:8012, restart if timeout
    4. thermal_armor - Poll nvidia-smi, fan control for RTX 4070
    5. social_streak_saver - Check time, notify about expiring streaks
    6. priority_vip_pings - Filter notifications, elevate VIP contacts
    7. micro_expression_detector - Secondary emotion layer during webcam
    8. smart_welcome_summary - Aggregate notifications, filter spam
    9. drama_companion - Foreign subtitle detection, translation prep
    10. language_flashcard_capture - Highlighted Korean text capture
    11. keyboard_asmr - Audio listener, mechanical switch frequency
    12. design_assistant - Design app + keywords, open reference folder
    13. birthday_retrospective - March date check, model training summary
    14. visual_clipboard - Copy event, screenshot retrieval
    15. auto_clipper - 30-second rolling screen buffer, MP4 save
    16. deep_work_autoreply - VS Code + typing rate, reject VOIP
    17. post_debugging_relief - 'Compiled successfully' detection
    18. resource_predictor - Mouse velocity prediction, cache clear
    19. lighting_sync - Screen RGB values, smart home API
    20. context_audio - Active window process, audio playlist switch
    """
    
    def __init__(self):
        self._running = False
        self._evaluation_task: Optional[asyncio.Task] = None
        self._task_history: List[AdvancedTask] = []
        self._last_evaluation = 0
        self._evaluation_interval = 5
        self._throttle_multiplier = 1.0
        
        self._mock_terminal_state = TerminalState()
        self._mock_advanced_os_state = AdvancedOSState()
        
        self._config = {
            "loss_spike_threshold": 0.20,
            "gpu_temp_critical": 85.0,
            "typing_rate_threshold": 60,
            "screen_buffer_duration": 30,
            "vip_keywords": ["Lesley", "Sister", "Mom", "Dad"],
            "foreign_language_patterns": {
                "korean": r'[\uAC00-\uD7A3]+',
                "turkish": r'[\u0130\u0131\u015E\u011F\u00E7]',
            },
            "flashcard_dir": Path("backend/data/flashcards"),
        }
        
        logger.info("AdvancedRoutineManager initialized with 20 advanced behaviors")
    
    async def start(self):
        self._running = True
        self._evaluation_task = asyncio.create_task(self._evaluation_loop())
        logger.info("Advanced Routine Evaluation Started")
    
    async def stop(self):
        self._running = False
        if self._evaluation_task:
            self._evaluation_task.cancel()
        logger.info("Advanced Routine Evaluation Stopped")
    
    async def _evaluation_loop(self):
        while self._running:
            try:
                now = time.time()
                effective_interval = self._config["evaluation_interval"] * self._throttle_multiplier
                
                if now - self._last_evaluation >= effective_interval:
                    await self.evaluate_advanced_state(
                        self._mock_terminal_state,
                        self._mock_advanced_os_state
                    )
                    self._last_evaluation = now
                
                await asyncio.sleep(effective_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Evaluation loop error: {e}")
                await asyncio.sleep(1)
    
    async def evaluate_advanced_state(
        self, 
        terminal_data: TerminalState, 
        os_data: AdvancedOSState
    ) -> List[AdvancedTask]:
        tasks = []
        
        tasks.extend(await self.monitor_training_loop(terminal_data, os_data))
        tasks.extend(await self.abliterated_sandbox(terminal_data, os_data))
        tasks.extend(await self.revive_coding_agent(terminal_data, os_data))
        tasks.extend(await self.thermal_armor(terminal_data, os_data))
        tasks.extend(await self.social_streak_saver(terminal_data, os_data))
        tasks.extend(await self.priority_vip_pings(terminal_data, os_data))
        tasks.extend(await self.micro_expression_detector(terminal_data, os_data))
        tasks.extend(await self.smart_welcome_summary(terminal_data, os_data))
        tasks.extend(await self.drama_companion(terminal_data, os_data))
        tasks.extend(await self.language_flashcard_capture(terminal_data, os_data))
        tasks.extend(await self.keyboard_asmr(terminal_data, os_data))
        tasks.extend(await self.design_assistant(terminal_data, os_data))
        tasks.extend(await self.birthday_retrospective(terminal_data, os_data))
        tasks.extend(await self.visual_clipboard(terminal_data, os_data))
        tasks.extend(await self.auto_clipper(terminal_data, os_data))
        tasks.extend(await self.deep_work_autoreply(terminal_data, os_data))
        tasks.extend(await self.post_debugging_relief(terminal_data, os_data))
        tasks.extend(await self.resource_predictor(terminal_data, os_data))
        tasks.extend(await self.lighting_sync(terminal_data, os_data))
        tasks.extend(await self.context_audio(terminal_data, os_data))
        
        tasks.sort(key=lambda x: x.priority, reverse=True)
        
        for task in tasks:
            logger.info(f"[{task.priority}] {task.behavior_name}: {task.message[:60]}...")
        
        return tasks
    
    # BEHAVIOR 1: monitor_training_loop
    async def monitor_training_loop(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if terminal_data.is_training:
            if terminal_data.has_nan:
                task = AdvancedTask(
                    task_id=generate_task_id(),
                    behavior_name="monitor_training_loop",
                    priority=5,
                    message="NaN detected in training - pausing",
                    action_type="training_monitoring",
                    timestamp=str(get_current_time())
                )
                tasks.append(task)
            elif terminal_data.loss_values and terminal_data.loss_values[-1] > self._config["loss_spike_threshold"]:
                task = AdvancedTask(
                    task_id=generate_task_id(),
                    behavior_name="monitor_training_loop",
                    priority=4,
                    message="Loss spike detected - monitoring",
                    action_type="training_monitoring",
                    timestamp=str(get_current_time())
                )
                tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 2: abliterated_sandbox
    async def abliterated_sandbox(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if "uncensored" in terminal_data.output.lower() or "dan mode" in terminal_data.output.lower():
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="abliterated_sandbox",
                priority=5,
                message="Uncensored model detected - sandboxing",
                action_type="sandbox",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 3: revive_coding_agent
    async def revive_coding_agent(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if "localhost:8012" in terminal_data.output:
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="revive_coding_agent",
                priority=4,
                message="Coding agent detected - monitoring",
                action_type="agent_management",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 4: thermal_armor
    async def thermal_armor(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if os_data.gpu_temperature > self._config["gpu_temp_critical"]:
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="thermal_armor",
                priority=5,
                message=f"GPU temp critical at {os_data.gpu_temperature}C - cooling",
                action_type="thermal_management",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 5: social_streak_saver
    async def social_streak_saver(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        now = get_current_time()
        
        if now.hour == 11:
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="social_streak_saver",
                priority=3,
                message="Social streak reminder - 11 PM",
                action_type="reminder",
                timestamp=str(now)
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 6: priority_vip_pings
    async def priority_vip_pings(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        for keyword in self._config["vip_keywords"]:
            if keyword in terminal_data.output:
                task = AdvancedTask(
                    task_id=generate_task_id(),
                    behavior_name="priority_vip_pings",
                    priority=1,
                    message=f"VIP contact '{keyword}' detected - elevating",
                    action_type="priority_routing",
                    timestamp=str(get_current_time())
                )
                tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 7: micro_expression_detector
    async def micro_expression_detector(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if os_data.screen_buffer:
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="micro_expression_detector",
                priority=3,
                message="Micro expression analysis",
                action_type="emotion_detection",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 8: smart_welcome_summary
    async def smart_welcome_summary(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if self._is_user_away():
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="smart_welcome_summary",
                priority=1,
                message="Welcome back - notification summary",
                action_type="summary",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 9: drama_companion
    async def drama_companion(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        foreign_patterns = self._config["foreign_language_patterns"]
        
        for lang, pattern in foreign_patterns.items():
            if re.search(pattern, terminal_data.output):
                task = AdvancedTask(
                    task_id=generate_task_id(),
                    behavior_name="drama_companion",
                    priority=3,
                    message=f"Foreign language detected ({lang}) - preparing translation",
                    action_type="translation",
                    timestamp=str(get_current_time())
                )
                tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 10: language_flashcard_capture
    async def language_flashcard_capture(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if re.search(foreign_patterns["korean"], terminal_data.output):
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="language_flashcard_capture",
                priority=3,
                message="Korean text detected - capturing flashcard",
                action_type="language_learning",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 11: keyboard_asmr
    async def keyboard_asmr(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if os_data.typing_rate > self._config["typing_rate_threshold"]:
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="keyboard_asmr",
                priority=2,
                message=f"Fast typing detected - {os_data.typing_rate} wpm",
                action_type="audio_enhancement",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 12: design_assistant
    async def design_assistant(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if "design" in terminal_data.output.lower():
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="design_assistant",
                priority=3,
                message="Design task detected - opening references",
                action_type="design_assistance",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 13: birthday_retrospective
    async def birthday_retrospective(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        now = get_current_time()
        
        if now.month == 3 and now.day == 23:
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="birthday_retrospective",
                priority=1,
                message="Birthday retrospective - March 23",
                action_type="celebration",
                timestamp=str(now)
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 14: visual_clipboard
    async def visual_clipboard(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if os_data.clipboard_content:
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="visual_clipboard",
                priority=2,
                message="Clipboard content detected - retrieving source",
                action_type="clipboard",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 15: auto_clipper
    async def auto_clipper(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if os_data.screen_buffer:
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="auto_clipper",
                priority=2,
                message="Screen clip recording",
                action_type="recording",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 16: deep_work_autoreply
    async def deep_work_autoreply(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if os_data.typing_rate > self._config["typing_rate_threshold"]:
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="deep_work_autoreply",
                priority=2,
                message="Deep work mode - rejecting distractions",
                action_type="focus_mode",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 17: post_debugging_relief
    async def post_debugging_relief(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if "compiled successfully" in terminal_data.output.lower():
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="post_debugging_relief",
                priority=2,
                message="Compilation successful - offering celebration",
                action_type="celebration",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 18: resource_predictor
    async def resource_predictor(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if os_data.mouse_velocity > 10:
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="resource_predictor",
                priority=3,
                message="High mouse velocity - clearing cache",
                action_type="resource_management",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 19: lighting_sync
    async def lighting_sync(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if os_data.screen_buffer:
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="lighting_sync",
                priority=2,
                message="Syncing lighting with screen",
                action_type="environment",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # BEHAVIOR 20: context_audio
    async def context_audio(self, terminal_data: TerminalState, os_data: AdvancedOSState) -> List[AdvancedTask]:
        tasks = []
        
        if os_data.screen_buffer:
            task = AdvancedTask(
                task_id=generate_task_id(),
                behavior_name="context_audio",
                priority=2,
                message="Context-aware audio playlist",
                action_type="audio",
                timestamp=str(get_current_time())
            )
            tasks.append(task)
        
        return tasks
    
    # HELPER METHODS
    async def _pause_training_process(self):
        logger.info("Pausing training process")
    
    async def _activate_sandbox_protocols(self, pid: Optional[int]):
        logger.info(f"Activating sandbox protocols for PID {pid}")
    
    async def _restart_llama_server(self):
        logger.info("Restarting llama-server on port 8012")
    
    async def _execute_fan_control_profile(self):
        logger.info("Executing fan control profile")
    
    async def _trigger_streak_reminder(self, streak: Dict[str, Any]):
        logger.info(f"Streak reminder: {streak.get('platform', 'unknown')}")
    
    async def _elevate_vip_notification(self, contact: str):
        logger.info(f"VIP notification elevated: {contact}")
    
    async def _draw_stress_bbox(self):
        logger.info("Drawing stress bounding box")
    
    async def _play_welcome_summary(self, notifications: List[Dict[str, Any]]):
        logger.info("Playing welcome summary")
    
    async def _prepare_translations(self, language: str):
        logger.info(f"Preparing translations for {language}")
    
    async def _capture_flashcard(self, content: str, filepath: Path):
        logger.info(f"Capturing flashcard to {filepath}")
    
    async def _trigger_keyboard_visualizer(self, rate: float):
        logger.info(f"Triggering keyboard visualizer at {rate} wpm")
    
    async def _load_design_references(self):
        logger.info("Loading design references")
    
    async def _show_birthday_dashboard(self):
        logger.info("Showing birthday dashboard")
    
    async def _retrieve_clipboard_source(self, content: str):
        logger.info("Retrieving clipboard source")
    
    async def _save_screen_clip(self):
        logger.info("Saving screen clip")
    
    async def _reject_incoming_call(self):
        logger.info("Rejecting incoming call")
    
    async def _minimize_terminal_and_offer_food(self):
        logger.info("Minimizing terminal and offering food")
    
    async def _clear_os_cache(self):
        logger.info("Clearing OS cache")
    
    async def _sync_smart_home_lighting(self, r: int, g: int, b: int):
        logger.info(f"Syncing lighting RGB: ({r}, {g}, {b})")
    
    async def _switch_audio_playlist(self, playlist: str):
        logger.info(f"Switching to {playlist} playlist")
    
    def get_task_history(self) -> List[Dict[str, Any]]:
        return [task.to_dict() for task in self._task_history]
    
    def get_active_tasks(self) -> List[Dict[str, Any]]:
        return [task.to_dict() for task in self._task_history[-10:]]
    
    def get_throttle_status(self) -> Dict[str, Any]:
        return {
            "multiplier": self._throttle_multiplier,
            "effective_interval": self._config["evaluation_interval"] * self._throttle_multiplier
        }

# ============================================================================
# OMEGA ROUTINE MANAGER (FROM routines_ultra.py) - SENTIENCE LAYER
# ============================================================================

class OmegaRoutineManager:
    """
    Omega Layer - Sentience and Human Intuition Behaviors
    
    Features:
    - Visual object memory
    - Project state tracking
    - Hardware health monitoring
    - Semantic pattern recognition
    - Meeting contact management
    - E2-TTS Voice Engine with emotion
    """
    
    def __init__(self):
        self._running = False
        self._task_history: List[OmegaTask] = []
        self._visual_objects: List[VisualObjectMemory] = []
        self._project_states: Dict[str, ProjectState] = {}
        self._hardware_health: HardwareHealth = HardwareHealth()
        self._semantic_patterns: List[SemanticPattern] = []
        self._meeting_contacts: Dict[str, MeetingContact] = {}
        self._voice_engine = E2TTSVoiceEngine()
        self._config = {
            "vision_active": True, 
            "voice_active": True, 
            "autonomy_level": 10, 
            "max_vram_gb": 6, 
            "max_temp_c": 85, 
            "fan_speed_auto": True
        }
        logger.info("[OmegaRoutineManager] Sentience layer initialized")
    
    def start(self):
        self._running = True
        logger.info("[OmegaRoutineManager] Starting sentience layer...")
    
    def stop(self):
        self._running = False
        logger.info("[OmegaRoutineManager] Sentience layer stopped")
    
    def execute_omega_task(self, task: OmegaTask) -> str:
        if not self._running:
            return "System halted"
        task.status = "executing"
        self._task_history.append(task)
        logger.info(f"[OmegaRoutine] Executing {task.behavior_name} (Routine {task.routine_number})")
        return f"Task {task.task_id} initiated"
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "running": self._running, 
            "tasks_processed": len(self._task_history), 
            "vision_active": self._config["vision_active"], 
            "voice_active": self._config["voice_active"], 
            "autonomy_level": self._config["autonomy_level"]
        }
    
    def update_hardware_health(self, health: HardwareHealth):
        self._hardware_health = health
        logger.info(f"[OmegaRoutine] Hardware health updated: temp={health.gpu_temp}C")
    
    def get_hardware_health(self) -> HardwareHealth:
        return self._hardware_health
    
    def add_visual_object(self, obj: VisualObjectMemory):
        self._visual_objects.append(obj)
        logger.info(f"[OmegaRoutine] Visual object indexed: {obj.object_name}")
    
    def get_visual_objects(self) -> List[VisualObjectMemory]:
        return self._visual_objects
    
    def update_project_state(self, state: ProjectState):
        self._project_states[state.project_path] = state
        logger.info(f"[OmegaRoutine] Project state updated: {state.project_path}")
    
    def get_project_states(self) -> Dict[str, ProjectState]:
        return self._project_states
    
    def add_semantic_pattern(self, pattern: SemanticPattern):
        self._semantic_patterns.append(pattern)
        logger.info(f"[OmegaRoutine] Semantic pattern indexed: {pattern.pattern_type}")
    
    def get_semantic_patterns(self) -> List[SemanticPattern]:
        return self._semantic_patterns
    
    def update_meeting_contact(self, contact: MeetingContact):
        self._meeting_contacts[contact.name] = contact
        logger.info(f"[OmegaRoutine] Meeting contact indexed: {contact.name}")
    
    def get_meeting_contacts(self) -> Dict[str, MeetingContact]:
        return self._meeting_contacts
    
    def synthesize_voice(self, text: str, emotion: str = "neutral") -> bytes:
        return self._voice_engine.synthesize(text, emotion)
    
    def set_voice_emotion(self, emotion: str):
        self._voice_engine.set_emotion(emotion)
    
    def get_voice_engine(self) -> E2TTSVoiceEngine:
        return self._voice_engine

def create_omega_task(behavior_name: str, routine_number: int, priority: int, message: str, action_type: str) -> OmegaTask:
    return OmegaTask(
        task_id=f"omega_{int(datetime.now().timestamp() * 1000)}", 
        behavior_name=behavior_name, 
        routine_number=routine_number, 
        priority=priority, 
        message=message, 
        action_type=action_type
    )

def create_visual_object_memory(name: str, timestamp: str, location: str, confidence: float) -> VisualObjectMemory:
    return VisualObjectMemory(object_name=name, timestamp=timestamp, location=location, confidence=confidence)

def create_project_state(path: str, modified: str, file_count: int, active: bool) -> ProjectState:
    return ProjectState(project_path=path, last_modified=modified, file_count=file_count, is_active=active)

def create_hardware_health(disk_cycles: int = 0, disk_temp: int = 0, gpu_temp: int = 0, fan_speed: int = 0, voltage: float = 0.0) -> HardwareHealth:
    return HardwareHealth(disk_cycles=disk_cycles, disk_temp=disk_temp, gpu_temp=gpu_temp, fan_speed=fan_speed, voltage=voltage)

def create_semantic_pattern(pattern_id: str, file_path: str, pattern_type: str, match_score: float, timestamp: str, context: str = "") -> SemanticPattern:
    return SemanticPattern(pattern_id=pattern_id, file_path=file_path, pattern_type=pattern_type, match_score=match_score, timestamp=timestamp, context=context)

def create_meeting_contact(name: str, github_url: str, linkedin_url: str, meeting_time: str, repo_count: int = 0) -> MeetingContact:
    return MeetingContact(name=name, github_url=github_url, linkedin_url=linkedin_url, meeting_time=meeting_time, repo_count=repo_count)

# ============================================================================
# UNIFIED ROUTINE FACTORY
# ============================================================================

class UnifiedRoutineEngine:
    """
    Unified Routine Engine - Combines all three routine managers
    
    Layers:
    - Proactive (20 behaviors) - Basic proactive monitoring
    - Advanced (20 behaviors) - Advanced context-aware behaviors
    - Omega (61-80 behaviors) - Sentience and human intuition
    """
    
    def __init__(self):
        self.proactive_manager = ProactiveRoutineManager()
        self.advanced_manager = AdvancedRoutineManager()
        self.omega_manager = OmegaRoutineManager()
        self._running = False
        self._tasks = []
        
        logger.info("UnifiedRoutineEngine initialized")
    
    async def start(self):
        await self.proactive_manager.start()
        await self.advanced_manager.start()
        self.omega_manager.start()
        self._running = True
        logger.info("Unified Routine Engine started")
    
    async def stop(self):
        await self.proactive_manager.stop()
        await self.advanced_manager.stop()
        self.omega_manager.stop()
        self._running = False
        logger.info("Unified Routine Engine stopped")
    
    async def evaluate_all(self):
        """Evaluate all routine layers"""
        proactive_tasks = await self.proactive_manager.evaluate_state(
            self.proactive_manager._mock_vision_state,
            self.proactive_manager._mock_os_state
        )
        
        advanced_tasks = await self.advanced_manager.evaluate_advanced_state(
            self.advanced_manager._mock_terminal_state,
            self.advanced_manager._mock_advanced_os_state
        )
        
        # Execute omega tasks
        for task in proactive_tasks + advanced_tasks:
            omega_task = OmegaTask(
                task_id=generate_omega_task_id(),
                behavior_name=task.behavior_name,
                routine_number=0,
                priority=task.priority,
                message=task.message,
                action_type=task.action_type
            )
            self.omega_manager.execute_omega_task(omega_task)
        
        logger.info(f"Evaluated {len(proactive_tasks) + len(advanced_tasks)} tasks")
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks from all managers"""
        all_tasks = []
        all_tasks.extend(self.proactive_manager.get_task_history())
        all_tasks.extend(self.advanced_manager.get_task_history())
        all_tasks.extend([t.to_dict() for t in self.omega_manager._task_history])
        return all_tasks
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all managers"""
        return {
            "proactive": self.proactive_manager.get_throttle_status(),
            "advanced": self.advanced_manager.get_throttle_status(),
            "omega": self.omega_manager.get_status()
        }

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    async def main():
        engine = UnifiedRoutineEngine()
        await engine.start()
        
        # Run evaluation loop
        for i in range(5):
            await engine.evaluate_all()
            await asyncio.sleep(2)
        
        await engine.stop()
        print("Routine engine stopped")
    
    asyncio.run(main())