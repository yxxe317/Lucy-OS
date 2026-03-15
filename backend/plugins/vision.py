import logging
from pathlib import Path
from PIL import Image
import base64
import io

logger = logging.getLogger("LucyVision")

class VisionPlugin:
    def __init__(self):
        self.upload_dir = Path(__file__).parent.parent / "uploads" / "images"
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"👁️ Vision Plugin Initialized. Upload dir: {self.upload_dir}")

    def save_image(self, file_bytes: bytes, filename: str) -> str:
        """Save uploaded image"""
        try:
            filepath = self.upload_dir / filename
            with open(filepath, 'wb') as f:
                f.write(file_bytes)
            logger.info(f"✅ Image saved: {filename}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Save image error: {e}")
            raise

    def get_image_info(self, filepath: str) -> dict:
        """Get image metadata"""
        try:
            with Image.open(filepath) as img:
                return {
                    "format": img.format,
                    "size": img.size,
                    "mode": img.mode,
                    "width": img.width,
                    "height": img.height
                }
        except Exception as e:
            logger.error(f"Get image info error: {e}")
            return {}

    def image_to_base64(self, filepath: str) -> str:
        """Convert image to base64 for LLM"""
        try:
            with open(filepath, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Image to base64 error: {e}")
            return ""

    def list_images(self) -> list:
        """List all uploaded images"""
        try:
            images = []
            for file in self.upload_dir.glob("*"):
                if file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
                    images.append({
                        "name": file.name,
                        "path": str(file),
                        "size": file.stat().st_size
                    })
            return images
        except Exception as e:
            logger.error(f"List images error: {e}")
            return []

vision = VisionPlugin()