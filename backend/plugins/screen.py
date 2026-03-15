import logging
from pathlib import Path
import pyautogui
import mss
import base64
from PIL import Image
import io
from datetime import datetime

logger = logging.getLogger("LucyScreen")

class ScreenPlugin:
    def __init__(self):
        self.screenshot_dir = Path(__file__).parent.parent / "uploads" / "screenshots"
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"🖥️ Screen Plugin Initialized. Dir: {self.screenshot_dir}")

    def take_screenshot(self, filename: str = None) -> str:
        """Take a screenshot and save it"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            filepath = self.screenshot_dir / filename
            
            # Take screenshot using mss (faster than pyautogui)
            with mss.mss() as sct:
                # Capture primary monitor
                monitor = sct.monitors[1]  # Monitor 1 is primary
                screenshot = sct.grab(monitor)
                
                # Convert to PIL Image
                img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                img.save(str(filepath), "PNG")
            
            logger.info(f"✅ Screenshot saved: {filename}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            raise

    def get_screenshot_base64(self, filename: str) -> str:
        """Convert screenshot to base64 for LLM"""
        try:
            filepath = self.screenshot_dir / filename
            with open(filepath, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Base64 error: {e}")
            return ""

    def list_screenshots(self) -> list:
        """List all screenshots"""
        try:
            screenshots = []
            for file in self.screenshot_dir.glob("*.png"):
                screenshots.append({
                    "name": file.name,
                    "path": str(file),
                    "size": file.stat().st_size,
                    "created": datetime.fromtimestamp(file.stat().st_ctime).isoformat()
                })
            return sorted(screenshots, key=lambda x: x['created'], reverse=True)
        except Exception as e:
            logger.error(f"List screenshots error: {e}")
            return []

    def get_screen_info(self) -> dict:
        """Get screen information"""
        try:
            width, height = pyautogui.size()
            return {
                "width": width,
                "height": height,
                "monitors": len(pyautogui.position())  # Simplified
            }
        except Exception as e:
            logger.error(f"Screen info error: {e}")
            return {}

screen = ScreenPlugin()