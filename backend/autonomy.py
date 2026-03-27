"""
Autonomy Core - Autonomous Heartbeat & Rhythm Verification
Monitors typing rhythm every 50 keystrokes and triggers E2-TTS feedback
"""

import os
import json
import time
import asyncio
import logging
import threading
from datetime import datetime
from typing import Dict, List, Optional, Callable
from pathlib import Path

# Import security module for biometric verification
from api.security import verify_typing_rhythm, anomaly_threshold

# Configuration
BASE_DIR = Path(__file__).parent
HEARTBEAT_LOG_PATH = os.path.join(BASE_DIR, 'logs', 'heartbeat_verification.jsonl')
RHYTHM_HISTORY_PATH = os.path.join(BASE_DIR, 'data', 'rhythm_history.json')
E2_TTS_AVAILABLE = True  # Will be set based on actual availability

# Ensure directories exist
os.makedirs(os.path.dirname(HEARTBEAT_LOG_PATH), exist_ok=True)
os.makedirs(os.path.dirname(RHYTHM_HISTORY_PATH), exist_ok=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [AUTONOMY] %(message)s'
)
logger = logging.getLogger("Autonomy")

# Global state
typing_events: List[Dict] = []
verification_count = 0
last_verification_time = None
rhythm_history: List[Dict] = []
heartbeat_interval = 50  # Verify every 50 keystrokes
anomaly_callbacks: List[Callable] = []
normal_callbacks: List[Callable] = []

# E2-TTS client (placeholder)
class E2TTSClient:
    """E2-TTS client for voice feedback"""
    
    def __init__(self):
        self.base_url = os.getenv("E2_TTS_URL", "http://localhost:8080")
        self.api_key = os.getenv("E2_TTS_API_KEY", "")
    
    async def speak(self, text: str, pitch: float = 1.0, speed: float = 1.0) -> bool:
        """Speak text using E2-TTS"""
        try:
            import requests
            payload = {
                "text": text,
                "pitch": pitch,
                "speed": speed
            }
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.post(
                f"{self.base_url}/tts",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"✅ E2-TTS spoke: {text[:50]}...")
                return True
            else:
                logger.warning(f"⚠️ E2-TTS response: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"E2-TTS error: {e}")
            return False
    
    async def speak_rhythm_change(self, old_rhythm: float, new_rhythm: float) -> bool:
        """Speak when rhythm changes significantly"""
        if abs(old_rhythm - new_rhythm) > 0.3:  # 30% change threshold
            change_type = "slowed down" if new_rhythm < old_rhythm else "speeded up"
            text = f"I notice you've {change_type}. Adjusting my response accordingly."
            return await self.speak(text)
        return False


# Global E2-TTS client
e2_tts_client = E2TTSClient()


def log_heartbeat(result: Dict):
    """Log heartbeat verification result"""
    os.makedirs(os.path.dirname(HEARTBEAT_LOG_PATH), exist_ok=True)
    
    with open(HEARTBEAT_LOG_PATH, 'a') as f:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'verification_count': verification_count,
            'score': result.get('score', 0),
            'action': result.get('action', 'none'),
            'is_verified': result.get('is_verified', False)
        }
        f.write(json.dumps(log_entry) + '\n')


def save_rhythm_history(history: List[Dict]):
    """Save rhythm history to file"""
    with open(RHYTHM_HISTORY_PATH, 'w') as f:
        json.dump(history, f, indent=2)


def load_rhythm_history() -> List[Dict]:
    """Load rhythm history from file"""
    if os.path.exists(RHYTHM_HISTORY_PATH):
        with open(RHYTHM_HISTORY_PATH, 'r') as f:
            return json.load(f)
    return []


class AutonomousHeartbeat:
    """
    Autonomous Heartbeat - Verifies typing rhythm every 50 keystrokes
    and triggers E2-TTS feedback when rhythm changes
    """
    
    def __init__(self):
        self.is_running = False
        self.heartbeat_thread = None
        self.lock = asyncio.Lock()
        
        # Load existing rhythm history
        self.rhythm_history = load_rhythm_history()
        
        logger.info("✅ AutonomousHeartbeat initialized")
    
    async def add_typing_event(self, event: Dict) -> bool:
        """Add a typing event to the queue"""
        async with self.lock:
            typing_events.append(event)
            
            # Check if we should verify (every 50 keystrokes)
            if len(typing_events) >= heartbeat_interval:
                await self._perform_verification()
            
            return True
    
    async def _perform_verification(self):
        """Perform biometric verification"""
        global verification_count, last_verification_time
        
        try:
            # Get recent typing events
            recent_events = typing_events[-heartbeat_interval:]
            
            # Prepare typing data for verification
            typing_data = []
            for event in recent_events:
                typing_data.append({
                    'dwellTime': event.get('dwellTime', 0),
                    'flightTime': event.get('flightTime', 0),
                    'totalTime': event.get('totalTime', 0),
                    'key': event.get('key', '')
                })
            
            # Perform verification
            result = await verify_typing_rhythm(typing_data)
            
            # Log result
            log_heartbeat(result)
            
            # Update verification count
            verification_count += 1
            last_verification_time = datetime.now().isoformat()
            
            # Handle verification result
            if result.get('is_verified', False):
                await self._handle_normal_verification(result)
            else:
                await self._handle_anomaly(result)
            
            # Save rhythm history
            self._update_rhythm_history(result.get('score', 0))
            
        except Exception as e:
            logger.error(f"Verification failed: {e}")
    
    async def _handle_normal_verification(self, result: Dict):
        """Handle normal (successful) verification"""
        score = result.get('score', 0)
        
        # Log normal verification
        logger.info(f"✅ Heartbeat verified (#{verification_count}): Score={score:.1f}%")
        
        # Call normal callbacks
        for callback in normal_callbacks:
            try:
                await callback(result)
            except Exception as e:
                logger.error(f"Normal callback error: {e}")
    
    async def _handle_anomaly(self, result: Dict):
        """Handle anomalous (failed) verification"""
        score = result.get('score', 0)
        
        # Log anomaly
        logger.warning(f"⚠️ Heartbeat anomaly (#{verification_count}): Score={score:.1f}%")
        
        # Call anomaly callbacks
        for callback in anomaly_callbacks:
            try:
                await callback(result)
            except Exception as e:
                logger.error(f"Anomaly callback error: {e}")
    
    def _update_rhythm_history(self, score: float = 0):
        """Update rhythm history with latest verification"""
        global verification_count
        
        history_entry = {
            'verification_count': verification_count,
            'timestamp': datetime.now().isoformat(),
            'score': score
        }
        
        self.rhythm_history.append(history_entry)
        
        # Keep only last 100 entries
        if len(self.rhythm_history) > 100:
            self.rhythm_history = self.rhythm_history[-100:]
        
        save_rhythm_history(self.rhythm_history)
    
    async def start(self):
        """Start the heartbeat monitoring"""
        if self.is_running:
            logger.warning("Heartbeat already running")
            return
        
        self.is_running = True
        logger.info("🚀 Starting Autonomous Heartbeat...")
        
        # Start heartbeat thread
        self.heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            daemon=True
        )
        self.heartbeat_thread.start()
        
        logger.info("✅ Autonomous Heartbeat started")
    
    def _heartbeat_loop(self):
        """Background heartbeat loop"""
        while self.is_running:
            time.sleep(1)  # Check every second
    
    async def stop(self):
        """Stop the heartbeat monitoring"""
        self.is_running = False
        
        if self.heartbeat_thread:
            self.heartbeat_thread.join(timeout=2)
        
        logger.info("⏸️ Autonomous Heartbeat stopped")
    
    def on_anomaly(self, callback: Callable):
        """Register callback for anomaly events"""
        anomaly_callbacks.append(callback)
        logger.info(f"✅ Anomaly callback registered")
    
    def on_normal(self, callback: Callable):
        """Register callback for normal verification events"""
        normal_callbacks.append(callback)
        logger.info(f"✅ Normal callback registered")
    
    def get_status(self) -> Dict:
        """Get current heartbeat status"""
        return {
            'is_running': self.is_running,
            'verification_count': verification_count,
            'last_verification': last_verification_time,
            'typing_events_count': len(typing_events),
            'rhythm_history_count': len(self.rhythm_history)
        }


# Global heartbeat instance
heartbeat = AutonomousHeartbeat()


async def main():
    """Main function to run the heartbeat system"""
    global e2_tts_client
    
    # Initialize E2-TTS client
    e2_tts_client = E2TTSClient()
    
    # Start heartbeat
    await heartbeat.start()
    
    # Register callbacks
    @heartbeat.on_anomaly
    async def on_anomaly(result: Dict):
        """Callback when anomaly detected"""
        await e2_tts_client.speak("Security alert: Unusual typing pattern detected.")
    
    @heartbeat.on_normal
    async def on_normal(result: Dict):
        """Callback on normal verification"""
        score = result.get('score', 0)
        if score > anomaly_threshold * 0.8:  # 80% of threshold
            await e2_tts_client.speak_rhythm_change(
                old_rhythm=anomaly_threshold,
                new_rhythm=score
            )
    
    logger.info("🚀 Autonomous Heartbeat system ready")


if __name__ == "__main__":
    asyncio.run(main())