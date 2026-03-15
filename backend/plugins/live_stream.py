import logging
from pathlib import Path
import pyautogui
import mss
import base64
from PIL import Image
import io
import asyncio
from datetime import datetime
import json

logger = logging.getLogger("LucyLiveStream")

class LiveStreamPlugin:
    def __init__(self):
        self.stream_dir = Path(__file__).parent.parent / "uploads" / "streams"
        self.stream_dir.mkdir(parents=True, exist_ok=True)
        self.is_streaming = False
        self.stream_fps = 5  # Frames per second (keep low for performance)
        self.current_frame = None
        self.session_id = None
        self.recording = False
        self.frames_recorded = []
        
        logger.info(f"📹 Live Stream Plugin Initialized")

    async def start_stream(self):
        """Start screen streaming"""
        self.is_streaming = True
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"🔴 Stream started: {self.session_id}")
        return {"status": "started", "session_id": self.session_id}

    async def stop_stream(self):
        """Stop screen streaming"""
        self.is_streaming = False
        session_id = self.session_id
        self.session_id = None
        
        # Save recording if enabled
        if self.recording and self.frames_recorded:
            await self._save_recording()
        
        self.recording = False
        self.frames_recorded = []
        
        logger.info(f"⏹️ Stream stopped: {session_id}")
        return {"status": "stopped", "session_id": session_id}

    async def capture_frame(self) -> str:
        """Capture current screen frame as base64"""
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                
                img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                
                # Resize for streaming (optimize for speed)
                img = img.resize((800, 600), Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=70)
                frame_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                self.current_frame = frame_base64
                
                # Store frame if recording
                if self.recording:
                    self.frames_recorded.append({
                        "timestamp": datetime.now().isoformat(),
                        "frame": frame_base64
                    })
                
                return frame_base64
                
        except Exception as e:
            logger.error(f"Capture frame error: {e}")
            return ""

    async def _save_recording(self):
        """Save recorded session"""
        try:
            recording_path = self.stream_dir / f"recording_{self.session_id}.json"
            
            with open(recording_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "session_id": self.session_id,
                    "frames": self.frames_recorded,
                    "fps": self.stream_fps
                }, f)
            
            logger.info(f"💾 Recording saved: {recording_path}")
            
        except Exception as e:
            logger.error(f"Save recording error: {e}")

    def start_recording(self):
        """Start recording the stream"""
        self.recording = True
        self.frames_recorded = []
        logger.info("🔴 Recording started")
        return {"status": "recording_started"}

    def stop_recording(self):
        """Stop recording the stream"""
        self.recording = False
        logger.info("⏹️ Recording stopped")
        return {"status": "recording_stopped", "frames": len(self.frames_recorded)}

    def get_stream_status(self) -> dict:
        """Get current stream status"""
        return {
            "is_streaming": self.is_streaming,
            "session_id": self.session_id,
            "recording": self.recording,
            "fps": self.stream_fps,
            "frames_recorded": len(self.frames_recorded)
        }

    def list_recordings(self) -> list:
        """List all recorded sessions"""
        try:
            recordings = []
            for file in self.stream_dir.glob("recording_*.json"):
                recordings.append({
                    "name": file.name,
                    "path": str(file),
                    "size": file.stat().st_size,
                    "created": datetime.fromtimestamp(file.stat().st_ctime).isoformat()
                })
            return sorted(recordings, key=lambda x: x['created'], reverse=True)
        except Exception as e:
            logger.error(f"List recordings error: {e}")
            return []

live_stream = LiveStreamPlugin()