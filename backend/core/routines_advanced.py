# ============================================================================
# LUCY_OS 2.0 - ADVANCED COGNITIVE ROUTINES (PART 2)
# AdvancedRoutineManager - 20 Highly Advanced Context-Aware Behaviors
# ============================================================================
import asyncio
import logging
import time
import re
import subprocess
import psutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import threading

logger = logging.getLogger("LucyAdvancedRoutines")

# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class AdvancedTask:
    """Represents an advanced proactive task"""
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

# ============================================================================
# AdvancedRoutineManager Class
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
        self._last_evaluation = 0.0
        self._evaluation_interval = 5
        self._throttle_multiplier = 1.0
        
        # Mock data for demonstration
        self._mock_terminal_state = TerminalState()
        self._mock_advanced_os_state = AdvancedOSState()
        
        # Configuration
        self._config = {
            "loss_spike_threshold": 0.20,  # 20% spike
            "gpu_temp_critical": 85.0,  # Celsius
            "typing_rate_threshold": 60,  # wpm
            "screen_buffer_duration": 30,  # seconds
            "vip_keywords": ["Lesley", "Sister", "Mom", "Dad"],
            "foreign_language_patterns": {
                "korean": r'[\uAC00-\uD7A3]+',
                "turkish": r'[\u0130\u0131\u015E\u011F\u00E7\u011F\u00F6\u00C7\u00FC\u00D6\u0131\u015F\u011F\u00E7\u00F6\u00C7\u00FC]',
            },
            "flashcard_dir": Path("backend/data/flashcards"),
            "evaluation_interval": 5,
        }
        
        logger.info("🧠 AdvancedRoutineManager initialized with 20 advanced behaviors")
    
    async def start(self):
        """Start the advanced routine evaluation loop"""
        self._running = True
        self._evaluation_task = asyncio.create_task(self._evaluation_loop())
        logger.info("🔄 Advanced Routine Evaluation Started")
    
    async def stop(self):
        """Stop the advanced routine evaluation loop"""
        self._running = False
        if self._evaluation_task:
            self._evaluation_task.cancel()
        logger.info("🛑 Advanced Routine Evaluation Stopped")
    
    async def _evaluation_loop(self):
        """Main evaluation loop"""
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
        """
        Evaluate current state and trigger advanced behaviors
        
        Args:
            terminal_data: Current terminal state
            os_data: Current advanced OS state
            
        Returns:
            List of triggered advanced tasks
        """
        tasks = []
        
        # Run all 20 advanced behaviors
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
        
        # Sort by priority (higher priority first)
        tasks.sort(key=lambda x: x.priority, reverse=True)
        
        # Log triggered tasks
        for task in tasks:
            logger.info(f"📌 [{task.priority}] {task.behavior_name}: {task.message[:60]}...")
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 1: monitor_training_loop
    # ========================================================================
    async def monitor_training_loop(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        Parse terminal stdout. IF 'loss' spikes > 20% OR 'NaN' appears 
        during a long run -> Pause process.
        
        TTS: "Training alert. The loss curve just spiked. I'm pausing the script 
        so we don't lose the last 12 hours of progress."
        """
        tasks = []
        
        # Check if currently training
        if terminal.is_training and terminal.output:
            # Check for NaN
            if "nan" in terminal.output.lower() or "NaN" in terminal.output:
                task = AdvancedTask(
                    task_id=f"train_{int(time.time() * 1000)}",
                    behavior_name="monitor_training_loop",
                    priority=10,
                    message="Training alert. The loss curve just spiked. I'm pausing the script so we don't lose the last 12 hours of progress.",
                    action_type="process_control",
                    timestamp=datetime.now().isoformat(),
                    metadata={
                        "action": "pause_training",
                        "issue": "NaN_detected"
                    }
                )
                tasks.append(task)
                await self._pause_training_process()
            
            # Check for loss spike
            loss_match = re.search(r'loss[:\s=]+([0-9.]+)', terminal.output)
            if loss_match:
                try:
                    current_loss = float(loss_match.group(1))
                    if terminal.loss_values and len(terminal.loss_values) > 1:
                        prev_loss = terminal.loss_values[-2]
                        if prev_loss > 0:
                            spike = (current_loss - prev_loss) / prev_loss
                            if spike > self._config["loss_spike_threshold"]:
                                task = AdvancedTask(
                                    task_id=f"train_{int(time.time() * 1000)}",
                                    behavior_name="monitor_training_loop",
                                    priority=10,
                                    message="Training alert. The loss curve just spiked. I'm pausing the script so we don't lose the last 12 hours of progress.",
                                    action_type="process_control",
                                    timestamp=datetime.now().isoformat(),
                                    metadata={
                                        "action": "pause_training",
                                        "current_loss": current_loss,
                                        "previous_loss": prev_loss,
                                        "spike_percentage": spike * 100
                                    }
                                )
                                tasks.append(task)
                                await self._pause_training_process()
                except (ValueError, IndexError):
                    pass
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 2: abliterated_sandbox
    # ========================================================================
    async def abliterated_sandbox(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        OCR detects 'abliterated' or 'uncensored' in model filename -> 
        Isolate network access for that PID.
        
        TTS: "Uncensored model loaded into memory. Activating secure sandbox protocols."
        """
        tasks = []
        
        # Check for uncensored/abliterated keywords
        uncensored_keywords = ['abliterated', 'uncensored', 'unfiltered', 'nsfw']
        
        for keyword in uncensored_keywords:
            if keyword in terminal.output.lower() or keyword in os_state.clipboard_content.lower():
                # Find the process ID
                pid = os_state.active_processes[0].get('pid') if os_state.active_processes else None
                
                task = AdvancedTask(
                    task_id=f"sandbox_{int(time.time() * 1000)}",
                    behavior_name="abliterated_sandbox",
                    priority=9,
                    message="Uncensored model loaded into memory. Activating secure sandbox protocols.",
                    action_type="network_isolation",
                    timestamp=datetime.now().isoformat(),
                    metadata={
                        "action": "isolate_network",
                        "pid": pid,
                        "keyword_detected": keyword
                    }
                )
                tasks.append(task)
                await self._activate_sandbox_protocols(pid)
                break
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 3: revive_coding_agent
    # ========================================================================
    async def revive_coding_agent(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        Ping localhost:8012. IF timeout during VS Code activity -> 
        restart llama-server subprocess.
        
        TTS: "Connection to the coding agent dropped. I'm rebooting the local 
        server on port 8012."
        """
        tasks = []
        
        # Check if coding agent is active
        if "vscode" in os_state.clipboard_content.lower() or "code" in os_state.clipboard_content.lower():
            # Try to ping localhost:8012
            try:
                result = await asyncio.wait_for(
                    asyncio.create_subprocess_exec(
                        'curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://localhost:8012/health'
                    ),
                    timeout=2.0
                )
                status = await result.stdout.read().decode()
                
                if status != '200':
                    task = AdvancedTask(
                        task_id=f"agent_{int(time.time() * 1000)}",
                        behavior_name="revive_coding_agent",
                        priority=9,
                        message="Connection to the coding agent dropped. I'm rebooting the local server on port 8012.",
                        action_type="process_restart",
                        timestamp=datetime.now().isoformat(),
                        metadata={
                            "action": "restart_llama_server",
                            "port": 8012,
                            "http_status": status
                        }
                    )
                    tasks.append(task)
                    await self._restart_llama_server()
            except asyncio.TimeoutError:
                task = AdvancedTask(
                    task_id=f"agent_{int(time.time() * 1000)}",
                    behavior_name="revive_coding_agent",
                    priority=9,
                    message="Connection to the coding agent dropped. I'm rebooting the local server on port 8012.",
                    action_type="process_restart",
                    timestamp=datetime.now().isoformat(),
                    metadata={
                        "action": "restart_llama_server",
                        "port": 8012,
                        "issue": "timeout"
                    }
                )
                tasks.append(task)
                await self._restart_llama_server()
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 4: thermal_armor
    # ========================================================================
    async def thermal_armor(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        Poll nvidia-smi for RTX 4070. IF temp > 85C -> execute fan control profile.
        
        TTS: "The GPU is running a bit hot. Ramping up the cooling fans to protect the hardware."
        """
        tasks = []
        
        if os_state.gpu_temperature > self._config["gpu_temp_critical"]:
            task = AdvancedTask(
                task_id=f"thermal_{int(time.time() * 1000)}",
                behavior_name="thermal_armor",
                priority=10,
                message=f"The GPU is running a bit hot. Ramping up the cooling fans to protect the hardware.",
                action_type="hardware_control",
                timestamp=datetime.now().isoformat(),
                metadata={
                    "action": "increase_fan_speed",
                    "current_temp": os_state.gpu_temperature,
                    "critical_threshold": self._config["gpu_temp_critical"]
                }
            )
            tasks.append(task)
            await self._execute_fan_control_profile()
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 5: social_streak_saver
    # ========================================================================
    async def social_streak_saver(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        Check local time and API/Notification logs. IF 22:00 and no activity 
        for tracked streaks -> TTS.
        
        TTS: "Just a heads up, your Snapchat streak is going to expire in two hours. 
        Don't leave them on read."
        """
        tasks = []
        now = datetime.now()
        
        # Check if it's around 22:00
        if 21 <= now.hour <= 23:
            # Check streak status (mock data)
            streaks_at_risk = [
                {"platform": "Snapchat", "hours_remaining": 2, "contact": "BestFriend"},
                {"platform": "Discord", "hours_remaining": 4, "contact": "GamingBuddy"},
            ]
            
            for streak in streaks_at_risk:
                if streak["hours_remaining"] <= 2:
                    task = AdvancedTask(
                        task_id=f"streak_{int(time.time() * 1000)}",
                        behavior_name="social_streak_saver",
                        priority=7,
                        message=f"Just a heads up, your {streak['platform']} streak is going to expire in {streak['hours_remaining']} hours. Don't leave them on read.",
                        action_type="notification",
                        timestamp=datetime.now().isoformat(),
                        metadata={
                            "action": "streak_reminder",
                            "platform": streak["platform"],
                            "hours_remaining": streak["hours_remaining"]
                        }
                    )
                    tasks.append(task)
                    await self._trigger_streak_reminder(streak)
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 6: priority_vip_pings
    # ========================================================================
    async def priority_vip_pings(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        Filter incoming OS notifications. IF regex matches 'Lesley' OR 'Sister' 
        -> Elevate UI priority.
        
        TTS: "Your sister is trying to reach you. I've pinned her message to the HUD."
        """
        tasks = []
        
        # Check for VIP keywords in notifications
        for keyword in self._config["vip_keywords"]:
            if keyword in os_state.clipboard_content.lower() or keyword in terminal.output.lower():
                task = AdvancedTask(
                    task_id=f"vip_{int(time.time() * 1000)}",
                    behavior_name="priority_vip_pings",
                    priority=10,
                    message=f"Your {keyword.lower()} is trying to reach you. I've pinned her message to the HUD.",
                    action_type="ui_priority",
                    timestamp=datetime.now().isoformat(),
                    metadata={
                        "action": "elevate_notification",
                        "vip_contact": keyword,
                        "priority": "highest"
                    }
                )
                tasks.append(task)
                await self._elevate_vip_notification(keyword)
                break
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 7: micro_expression_detector
    # ========================================================================
    async def micro_expression_detector(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        During active webcam usage by other apps, run secondary Haar-cascade/
        emotion layer. IF stress detected -> Draw bounding box.
        
        TTS: "Command Center is active. Their baseline stress level just spiked 
        on that last question."
        """
        tasks = []
        
        # Check if webcam is being used by another app
        if os_state.active_processes:
            for proc in os_state.active_processes:
                if proc.get('name', '').lower() in ['zoom', 'teams', 'webcam', 'camera']:
                    # Simulate stress detection
                    stress_detected = True  # Would be from emotion analysis
                    
                    if stress_detected:
                        task = AdvancedTask(
                            task_id=f"micro_{int(time.time() * 1000)}",
                            behavior_name="micro_expression_detector",
                            priority=8,
                            message="Command Center is active. Their baseline stress level just spiked on that last question.",
                            action_type="emotion_alert",
                            timestamp=datetime.now().isoformat(),
                            metadata={
                                "action": "draw_stress_bbox",
                                "stress_level": "high",
                                "app_using_webcam": proc.get('name')
                            }
                        )
                        tasks.append(task)
                        await self._draw_stress_bbox()
                    break
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 8: smart_welcome_summary
    # ========================================================================
    async def smart_welcome_summary(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        Aggregate notifications during user absence. Filter out spam.
        
        TTS: "Welcome back. Lesley sent a meme, and your local model just finished compiling."
        """
        tasks = []
        
        # Simulate welcome back scenario
        welcome_notifications = [
            {"sender": "Lesley", "type": "meme", "content": "funny_cat.jpg"},
            {"sender": "System", "type": "build", "content": "Model compilation complete"},
            {"sender": "SpamBot", "type": "spam", "content": "BUY NOW!!!", "filtered": True},
        ]
        
        # Filter out spam
        filtered_notifications = [n for n in welcome_notifications if not n.get("filtered", False)]
        
        if filtered_notifications:
            summary = ", ".join([f"{n['sender']} sent {n['type']}" for n in filtered_notifications])
            
            task = AdvancedTask(
                task_id=f"welcome_{int(time.time() * 1000)}",
                behavior_name="smart_welcome_summary",
                priority=8,
                message=f"Welcome back. {summary}.",
                action_type="voice_summary",
                timestamp=datetime.now().isoformat(),
                metadata={
                    "action": "welcome_summary",
                    "notifications_count": len(filtered_notifications),
                    "filtered_spam_count": len([n for n in welcome_notifications if n.get("filtered")])
                }
            )
            tasks.append(task)
            await self._play_welcome_summary(filtered_notifications)
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 9: drama_companion
    # ========================================================================
    async def drama_companion(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        OCR detects media players with foreign subtitles (Turkish/Korean).
        
        TTS: "Oh, the plot is thickening. I've got the translations and character 
        maps ready on the side."
        """
        tasks = []
        
        # Check for media players with foreign content
        media_indicators = ['netflix', 'prime', 'youtube', 'korean', 'turkish']
        
        for indicator in media_indicators:
            if indicator in os_state.clipboard_content.lower() or indicator in terminal.output.lower():
                task = AdvancedTask(
                    task_id=f"drama_{int(time.time() * 1000)}",
                    behavior_name="drama_companion",
                    priority=6,
                    message="Oh, the plot is thickening. I've got the translations and character maps ready on the side.",
                    action_type="translation_prep",
                    timestamp=datetime.now().isoformat(),
                    metadata={
                        "action": "prepare_translations",
                        "language_detected": indicator,
                        "feature": "character_maps"
                    }
                )
                tasks.append(task)
                await self._prepare_translations(indicator)
                break
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 10: language_flashcard_capture
    # ========================================================================
    async def language_flashcard_capture(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        Detect highlighted Korean text -> Save screenshot to flashcards/ dir.
        
        TTS: "I grabbed that vocabulary word and added it to your Korea trip deck."
        """
        tasks = []
        
        # Check for Korean text (using regex pattern)
        korean_pattern = re.compile(r'[\uAC00-\uD7A3]+')
        
        if korean_pattern.search(os_state.clipboard_content) or korean_pattern.search(terminal.output):
            # Create flashcard directory
            flashcard_dir = self._config["flashcard_dir"]
            flashcard_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"flashcard_{timestamp}.png"
            filepath = flashcard_dir / filename
            
            task = AdvancedTask(
                task_id=f"flashcard_{int(time.time() * 1000)}",
                behavior_name="language_flashcard_capture",
                priority=7,
                message="I grabbed that vocabulary word and added it to your Korea trip deck.",
                action_type="screenshot_capture",
                timestamp=datetime.now().isoformat(),
                metadata={
                    "action": "save_flashcard",
                    "filepath": str(filepath),
                    "language": "korean"
                }
            )
            tasks.append(task)
            await self._capture_flashcard(os_state.clipboard_content, filepath)
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 11: keyboard_asmr
    # ========================================================================
    async def keyboard_asmr(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        Audio listener detects rapid mechanical switch frequencies -> trigger 
        React UI visualizer via WebSocket.
        
        TTS: "The keyboard is sounding crisp today. You're hitting 90 words per minute."
        """
        tasks = []
        
        # Check typing rate
        if os_state.typing_rate > 80:  # High typing rate
            task = AdvancedTask(
                task_id=f"asmr_{int(time.time() * 1000)}",
                behavior_name="keyboard_asmr",
                priority=5,
                message=f"The keyboard is sounding crisp today. You're hitting {int(os_state.typing_rate)} words per minute.",
                action_type="visualizer_trigger",
                timestamp=datetime.now().isoformat(),
                metadata={
                    "action": "trigger_visualizer",
                    "typing_rate": os_state.typing_rate,
                    "websocket_endpoint": "/api/visualizer"
                }
            )
            tasks.append(task)
            await self._trigger_keyboard_visualizer(os_state.typing_rate)
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 12: design_assistant
    # ========================================================================
    async def design_assistant(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        Detect Photoshop/Design app + 'book cover' or 'biography' keywords -> 
        Open reference folder.
        
        TTS: "Your typography is looking sharp. I've loaded some modern biography 
        references onto the secondary board."
        """
        tasks = []
        
        # Check for design apps and keywords
        design_apps = ['photoshop', 'illustrator', 'design', 'figma']
        design_keywords = ['book cover', 'biography', 'typography', 'design']
        
        clipboard_lower = os_state.clipboard_content.lower()
        terminal_lower = terminal.output.lower()
        
        is_design_app = any(app in clipboard_lower or app in terminal_lower for app in design_apps)
        has_design_keyword = any(keyword in clipboard_lower or keyword in terminal_lower for keyword in design_keywords)
        
        if is_design_app and has_design_keyword:
            task = AdvancedTask(
                task_id=f"design_{int(time.time() * 1000)}",
                behavior_name="design_assistant",
                priority=6,
                message="Your typography is looking sharp. I've loaded some modern biography references onto the secondary board.",
                action_type="reference_load",
                timestamp=datetime.now().isoformat(),
                metadata={
                    "action": "open_reference_folder",
                    "app_detected": "photoshop",
                    "keywords_found": [k for k in design_keywords if k in clipboard_lower or k in terminal_lower]
                }
            )
            tasks.append(task)
            await self._load_design_references()
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 13: birthday_retrospective
    # ========================================================================
    async def birthday_retrospective(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        Date check for March. Trigger special UI dashboard.
        
        TTS: "Happy Birthday month! I compiled a list of every local model we've 
        trained and tested together this year."
        """
        tasks = []
        now = datetime.now()
        
        # Check if it's March (birthday month)
        if now.month == 3:
            task = AdvancedTask(
                task_id=f"birthday_{int(time.time() * 1000)}",
                behavior_name="birthday_retrospective",
                priority=10,
                message="Happy Birthday month! I compiled a list of every local model we've trained and tested together this year.",
                action_type="dashboard_trigger",
                timestamp=datetime.now().isoformat(),
                metadata={
                    "action": "birthday_dashboard",
                    "month": now.month,
                    "feature": "model_training_history"
                }
            )
            tasks.append(task)
            await self._show_birthday_dashboard()
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 14: visual_clipboard
    # ========================================================================
    async def visual_clipboard(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        On OS 'copy' event, save a 300x300 cropped screenshot of mouse coordinates.
        
        TTS: "You copied that Python snippet an hour ago. I've retrieved the exact 
        file it came from."
        """
        tasks = []
        
        # Check if clipboard content looks like code
        if os_state.clipboard_content and re.search(r'import|def |class |print', os_state.clipboard_content):
            task = AdvancedTask(
                task_id=f"clipboard_{int(time.time() * 1000)}",
                behavior_name="visual_clipboard",
                priority=7,
                message="You copied that Python snippet an hour ago. I've retrieved the exact file it came from.",
                action_type="clipboard_retrieval",
                timestamp=datetime.now().isoformat(),
                metadata={
                    "action": "retrieve_clipboard_source",
                    "content_type": "python_code",
                    "timestamp": os_state.clipboard_timestamp
                }
            )
            tasks.append(task)
            await self._retrieve_clipboard_source(os_state.clipboard_content)
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 15: auto_clipper
    # ========================================================================
    async def auto_clipper(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        Maintain a 30-second rolling screen buffer. Save to MP4 on major task 
        completion.
        
        TTS: "That generation was flawless. I clipped the last 30 seconds for your records."
        """
        tasks = []
        
        # Check for task completion indicators
        completion_indicators = ['compiled successfully', 'generated', 'complete', 'done']
        
        for indicator in completion_indicators:
            if indicator in terminal.output.lower():
                task = AdvancedTask(
                    task_id=f"clip_{int(time.time() * 1000)}",
                    behavior_name="auto_clipper",
                    priority=6,
                    message="That generation was flawless. I clipped the last 30 seconds for your records.",
                    action_type="video_capture",
                    timestamp=datetime.now().isoformat(),
                    metadata={
                        "action": "save_screen_clip",
                        "duration": 30,
                        "format": "mp4"
                    }
                )
                tasks.append(task)
                await self._save_screen_clip()
                break
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 16: deep_work_autoreply
    # ========================================================================
    async def deep_work_autoreply(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        If VS Code is active and typing rate > 60wpm, reject VOIP/Calls.
        
        TTS: "You're in the zone. I muted the incoming call and sent a busy text."
        """
        tasks = []
        
        # Check for deep work conditions
        is_vs_code = "vscode" in os_state.clipboard_content.lower() or "code" in os_state.clipboard_content.lower()
        high_typing_rate = os_state.typing_rate > self._config["typing_rate_threshold"]
        
        if is_vs_code and high_typing_rate:
            task = AdvancedTask(
                task_id=f"deepwork_{int(time.time() * 1000)}",
                behavior_name="deep_work_autoreply",
                priority=9,
                message="You're in the zone. I muted the incoming call and sent a busy text.",
                action_type="call_rejection",
                timestamp=datetime.now().isoformat(),
                metadata={
                    "action": "reject_voip",
                    "typing_rate": os_state.typing_rate,
                    "active_app": "vscode"
                }
            )
            tasks.append(task)
            await self._reject_incoming_call()
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 17: post_debugging_relief
    # ========================================================================
    async def post_debugging_relief(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        OCR terminal for 'Compiled successfully' after previous errors -> 
        Minimize terminal.
        
        TTS: "Bug squashed. You've earned a break. Shall I pull up the food 
        delivery menu?"
        """
        tasks = []
        
        # Check for successful compilation after errors
        if "compiled successfully" in terminal.output.lower() or "build succeeded" in terminal.output.lower():
            task = AdvancedTask(
                task_id=f"relief_{int(time.time() * 1000)}",
                behavior_name="post_debugging_relief",
                priority=7,
                message="Bug squashed. You've earned a break. Shall I pull up the food delivery menu?",
                action_type="ui_minimize",
                timestamp=datetime.now().isoformat(),
                metadata={
                    "action": "minimize_terminal",
                    "offer": "food_delivery_menu"
                }
            )
            tasks.append(task)
            await self._minimize_terminal_and_offer_food()
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 18: resource_predictor
    # ========================================================================
    async def resource_predictor(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        Track mouse velocity towards heavy IDE icons -> call OS cache clear.
        
        TTS: "Clearing up RAM. The system is fully prepped for your next command."
        """
        tasks = []
        
        # Check for high mouse velocity (predicting heavy app launch)
        if os_state.mouse_velocity > 50:  # High velocity threshold
            task = AdvancedTask(
                task_id=f"resource_{int(time.time() * 1000)}",
                behavior_name="resource_predictor",
                priority=8,
                message="Clearing up RAM. The system is fully prepped for your next command.",
                action_type="cache_clear",
                timestamp=datetime.now().isoformat(),
                metadata={
                    "action": "clear_os_cache",
                    "mouse_velocity": os_state.mouse_velocity,
                    "predicted_action": "heavy_app_launch"
                }
            )
            tasks.append(task)
            await self._clear_os_cache()
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 19: lighting_sync
    # ========================================================================
    async def lighting_sync(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        Average screen RGB values -> Send to smart home cluster API.
        
        TTS: "Adjusting the cluster lighting to match the mood on screen."
        """
        tasks = []
        
        # Simulate screen RGB analysis
        if os_state.screen_buffer:
            # Calculate average RGB (mock)
            avg_r, avg_g, avg_b = 128, 128, 128
            
            task = AdvancedTask(
                task_id=f"lighting_{int(time.time() * 1000)}",
                behavior_name="lighting_sync",
                priority=5,
                message="Adjusting the cluster lighting to match the mood on screen.",
                action_type="smart_home_control",
                timestamp=datetime.now().isoformat(),
                metadata={
                    "action": "sync_lighting",
                    "rgb_values": {"r": avg_r, "g": avg_g, "b": avg_b},
                    "api_endpoint": "https://smart-home-api.local/v1/lighting"
                }
            )
            tasks.append(task)
            await self._sync_smart_home_lighting(avg_r, avg_g, avg_b)
        
        return tasks
    
    # ========================================================================
    # BEHAVIOR 20: context_audio
    # ========================================================================
    async def context_audio(
        self, 
        terminal: TerminalState, 
        os_state: AdvancedOSState
    ) -> List[AdvancedTask]:
        """
        Check active window process name -> Switch local audio playlist.
        
        TTS: "Switching the audio track to deep focus mode."
        """
        tasks = []
        
        # Check active window for context
        active_app = os_state.active_processes[0].get('name', '') if os_state.active_processes else ''
        
        if 'code' in active_app.lower():
            playlist = "deep_focus"
        elif 'video' in active_app.lower() or 'netflix' in active_app.lower():
            playlist = "movie_background"
        elif 'music' in active_app.lower():
            playlist = "ambient"
        else:
            playlist = "default"
        
        task = AdvancedTask(
            task_id=f"audio_{int(time.time() * 1000)}",
            behavior_name="context_audio",
            priority=4,
            message=f"Switching the audio track to {playlist} mode.",
            action_type="audio_switch",
            timestamp=datetime.now().isoformat(),
            metadata={
                "action": "switch_playlist",
                "playlist": playlist,
                "active_app": active_app
            }
        )
        tasks.append(task)
        await self._switch_audio_playlist(playlist)
        
        return tasks
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    async def _pause_training_process(self):
        """Pause training process"""
        logger.info("⏸️ Pausing training process")
    
    async def _activate_sandbox_protocols(self, pid: Optional[int]):
        """Activate sandbox protocols"""
        logger.info(f"🔒 Activating sandbox protocols for PID {pid}")
    
    async def _restart_llama_server(self):
        """Restart llama-server"""
        logger.info("🔄 Restarting llama-server on port 8012")
    
    async def _execute_fan_control_profile(self):
        """Execute fan control profile"""
        logger.info("🌬️ Executing fan control profile")
    
    async def _trigger_streak_reminder(self, streak: Dict[str, Any]):
        """Trigger streak reminder"""
        logger.info(f"📈 Streak reminder: {streak['platform']}")
    
    async def _elevate_vip_notification(self, contact: str):
        """Elevate VIP notification"""
        logger.info(f"🔔 VIP notification elevated: {contact}")
    
    async def _draw_stress_bbox(self):
        """Draw stress bounding box"""
        logger.info("📦 Drawing stress bounding box")
    
    async def _play_welcome_summary(self, notifications: List[Dict[str, Any]]):
        """Play welcome summary"""
        logger.info("👋 Playing welcome summary")
    
    async def _prepare_translations(self, language: str):
        """Prepare translations"""
        logger.info(f"🌐 Preparing translations for {language}")
    
    async def _capture_flashcard(self, content: str, filepath: Path):
        """Capture flashcard"""
        logger.info(f"💾 Capturing flashcard to {filepath}")
    
    async def _trigger_keyboard_visualizer(self, rate: float):
        """Trigger keyboard visualizer"""
        logger.info(f"🎨 Triggering keyboard visualizer at {rate} wpm")
    
    async def _load_design_references(self):
        """Load design references"""
        logger.info("🎨 Loading design references")
    
    async def _show_birthday_dashboard(self):
        """Show birthday dashboard"""
        logger.info("🎂 Showing birthday dashboard")
    
    async def _retrieve_clipboard_source(self, content: str):
        """Retrieve clipboard source"""
        logger.info("📋 Retrieving clipboard source")
    
    async def _save_screen_clip(self):
        """Save screen clip"""
        logger.info("🎬 Saving screen clip")
    
    async def _reject_incoming_call(self):
        """Reject incoming call"""
        logger.info("📞 Rejecting incoming call")
    
    async def _minimize_terminal_and_offer_food(self):
        """Minimize terminal and offer food"""
        logger.info("🍕 Minimizing terminal and offering food")
    
    async def _clear_os_cache(self):
        """Clear OS cache"""
        logger.info("🧹 Clearing OS cache")
    
    async def _sync_smart_home_lighting(self, r: int, g: int, b: int):
        """Sync smart home lighting"""
        logger.info(f"💡 Syncing lighting RGB: ({r}, {g}, {b})")
    
    async def _switch_audio_playlist(self, playlist: str):
        """Switch audio playlist"""
        logger.info(f"🎵 Switching to {playlist} playlist")
    
    # ========================================================================
    # GETTERS
    # ========================================================================
    
    def get_task_history(self) -> List[Dict[str, Any]]:
        """Get task history"""
        return [task.to_dict() for task in self._task_history]
    
    def get_active_tasks(self) -> List[Dict[str, Any]]:
        """Get currently active tasks"""
        return [task.to_dict() for task in self._task_history[-10:]]
    
    def get_throttle_status(self) -> Dict[str, Any]:
        """Get current throttle status"""
        return {
            "multiplier": self._throttle_multiplier,
            "effective_interval": self._config["evaluation_interval"] * self._throttle_multiplier
        }


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================
advanced_routine_manager = AdvancedRoutineManager()