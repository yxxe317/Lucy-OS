# backend/core/f5_tts.py
import torch
import torchaudio
from pathlib import Path
from f5_tts.model import F5TTS
import logging

logger = logging.getLogger("F5TTS")

class F5TTSVoice:
    def __init__(self):
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"🎤 F5-TTS Device: {self.device}")
        
    def load_model(self):
        """Load F5-TTS model"""
        try:
            self.model = F5TTS.from_pretrained("f5-tts-small")
            self.model.to(self.device)
            self.model.eval()
            logger.info("✅ F5-TTS Model Loaded")
            return True
        except Exception as e:
            logger.error(f"❌ F5-TTS Load Error: {e}")
            return False
    
    def generate(self, text, output_path, voice="female"):
        """Generate speech from text"""
        try:
            if not self.model:
                self.load_model()
            
            # Female voice preset (F5-TTS has excellent female voices)
            ref_audio = "backend/voice/ref_female.wav"  # Reference audio for voice cloning
            
            # Generate speech
            with torch.no_grad():
                output = self.model.generate(
                    text=text,
                    ref_audio=ref_audio if Path(ref_audio).exists() else None,
                    speed=1.0,
                    emotion="neutral"
                )
            
            # Save audio
            torchaudio.save(output_path, output, sample_rate=24000)
            logger.info(f"✅ F5-TTS Generated: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ F5-TTS Generate Error: {e}")
            return False

# Global instance
f5_voice = F5TTSVoice()