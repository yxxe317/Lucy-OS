import os
import time
import asyncio
from pathlib import Path
import logging
import re

logger = logging.getLogger("VoicePlugin")

AUDIO_DIR = Path(__file__).parent.parent / "temp_audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# EMOJI TO HUMAN-LIKE SOUNDS MAPPING
# ═══════════════════════════════════════════════════════════════
EMOJI_TO_SOUND = {
    # Laughing/Happy
    "😊": " hehe ",
    "😂": " hahaha ",
    "🤣": " hahahaha ",
    "😆": " haha ",
    "😄": " hehe ",
    "😁": " haha ",
    "😃": " ha ",
    "😀": " ha ",
    "😅": " hehe ",
    "😍": " aww ",
    "🥰": " aww ",
    "😘": " mwah ",
    "😗": " mwah ",
    "😚": " mwah ",
    "😙": " mwah ",
    "🥳": " yay ",
    "🎉": " yay ",
    "✨": " ooh ",
    "🌟": " wow ",
    "💖": " aww ",
    "❤️": " aww ",
    "💕": " aww ",
    "💗": " aww ",
    "💓": " aww ",
    "💝": " aww ",
    "🔥": " wow ",
    "💯": " yeah ",
    "👍": " mhm ",
    "👏": " yay ",
    "🙌": " yay ",
    "🎊": " yay ",
    
    # Thinking/Confused
    "🤔": " hmm ",
    "🤨": " hmm ",
    "😐": " um ",
    "😑": " um ",
    "😶": " um ",
    "🤷": " um ",
    "🤔": " hmm ",
    "💭": " hmm ",
    "❓": " hmm ",
    "🤔": " hmm ",
    
    # Sad/Concerned
    "😢": " aww ",
    "😭": " oh no ",
    "😿": " aww ",
    "💔": " oh no ",
    "😔": " hmm ",
    "😞": " hmm ",
    "😟": " oh ",
    "😕": " hmm ",
    "🙁": " hmm ",
    "😓": " oh ",
    "😥": " oh ",
    
    # Surprised/Excited
    "😮": " oh ",
    "😯": " oh ",
    "😲": " wow ",
    "😳": " oh ",
    "🤩": " wow ",
    "😱": " oh my ",
    "😨": " oh ",
    "😰": " oh ",
    "😦": " oh ",
    "🎉": " yay ",
    "🎊": " yay ",
    "🥳": " yay ",
    
    # Angry/Annoyed
    "😡": " ugh ",
    "😠": " ugh ",
    "🤬": " ugh ",
    "😤": " ugh ",
    "😒": " ugh ",
    "🙄": " ugh ",
    "😑": " um ",
    
    # Love/Affection
    "😍": " aww ",
    "🥰": " aww ",
    "😘": " mwah ",
    "💋": " mwah ",
    "❤️": " aww ",
    "💕": " aww ",
    "💖": " aww ",
    "💗": " aww ",
    "💓": " aww ",
    "💝": " aww ",
    "💘": " aww ",
    
    # Other expressions
    "🤗": " aww ",
    "🤭": " hehe ",
    "🤫": " shh ",
    "🤐": " mmm ",
    "😴": " zzz ",
    "💤": " zzz ",
    "😪": " zzz ",
    "🥱": " yawn ",
    "😋": " mmm ",
    "🤤": " mmm ",
    "😌": " ahh ",
    "😏": " hehe ",
    "😎": " yeah ",
    "🤓": " hmm ",
    "🧐": " hmm ",
    "😇": " aww ",
    "🤠": " yeehaw ",
    "👻": " boo ",
    "👽": " beep boop ",
    "🤖": " beep boop ",
    "💩": " eww ",
    "👀": " hmm ",
    "👁️": " hmm ",
    "👅": " mmm ",
    "👄": " mmm ",
    "💪": " yeah ",
    "🙏": " aww ",
    "🤝": " mhm ",
    "👋": " hey ",
    "🤙": " hey ",
    "👉": " hmm ",
    "👈": " hmm ",
    "👆": " hmm ",
    "👇": " hmm ",
    "✌️": " yeah ",
    "🤟": " yeah ",
    "🤘": " yeah ",
    "👌": " mhm ",
    "🤏": " hmm ",
    "✋": " hey ",
    "🤚": " hey ",
    "🖐️": " hey ",
    "🖖": " live long ",
    "👊": " yeah ",
    "✊": " yeah ",
    "🤛": " yeah ",
    "🤜": " yeah ",
    "👍": " mhm ",
    "👎": " ugh ",
    "✊": " yeah ",
    "👊": " yeah ",
    "🤛": " yeah ",
    "🤜": " yeah ",
    "👏": " yay ",
    "🙌": " yay ",
    "👐": " aww ",
    "🤲": " aww ",
    "🤝": " mhm ",
    "🙏": " aww ",
    "✍️": " hmm ",
    "💅": " mhm ",
    "🤳": " hmm ",
    "💁": " hmm ",
    "🙋": " hey ",
    "🧏": " hmm ",
    "🙆": " hmm ",
    "🙅": " no ",
    "💇": " hmm ",
    "💆": " ahh ",
    "🧖": " ahh ",
    "💃": " yeah ",
    "🕺": " yeah ",
    "👯": " yay ",
    "🕴️": " hmm ",
    "🚶": " hmm ",
    "🧍": " hmm ",
    "🧎": " hmm ",
    "🏃": " yeah ",
    "💃": " yeah ",
    "🕺": " yeah ",
    "👯": " yay ",
    "🧘": " omm ",
    "🛀": " ahh ",
    "🛌": " zzz ",
    "👭": " aww ",
    "👫": " aww ",
    "👬": " aww ",
    "💏": " mwah ",
    "💑": " aww ",
    "👨‍👩‍👧": " aww ",
    "👨‍👩‍👧‍👦": " aww ",
    "👨‍👩‍👦‍👦": " aww ",
    "👨‍👩‍👧‍👧": " aww ",
    "👨‍👩‍👦": " aww ",
    "👩‍👩‍👦": " aww ",
    "👩‍👩‍👧": " aww ",
    "👩‍👩‍👧‍👦": " aww ",
    "👩‍👩‍👦‍👦": " aww ",
    "👩‍👩‍👧‍👧": " aww ",
    "👨‍👨‍👦": " aww ",
    "👨‍👨‍👧": " aww ",
    "👨‍👨‍👧‍👦": " aww ",
    "👨‍👨‍👦‍👦": " aww ",
    "👨‍👨‍👧‍👧": " aww ",
    "👩‍👦": " aww ",
    "👩‍👧": " aww ",
    "👩‍👧‍👦": " aww ",
    "👩‍👦‍👦": " aww ",
    "👩‍👧‍👧": " aww ",
    "👨‍👦": " aww ",
    "👨‍👧": " aww ",
    "👨‍👧‍👦": " aww ",
    "👨‍👦‍👦": " aww ",
    "👨‍👧‍👧": " aww ",
}

def preprocess_text_for_speech(text: str) -> str:
    """
    Convert emojis to human-like sounds before TTS
    """
    result = text
    
    # Replace emojis with human-like sounds
    for emoji, sound in EMOJI_TO_SOUND.items():
        result = result.replace(emoji, sound)
    
    # Clean up multiple spaces
    result = re.sub(r'\s+', ' ', result).strip()
    
    return result

# Try F5-TTS first, then edge-tts, then pyttsx3
USE_F5_TTS = False
USE_EDGE_TTS = False
f5_model = None
f5_device = "cpu"

try:
    from f5_tts.model import F5TTS
    import torch
    import torchaudio
    
    f5_device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def init_f5():
        global f5_model
        if f5_model is None:
            logger.info(f"🎤 Loading F5-TTS on {f5_device}...")
            f5_model = F5TTS.from_pretrained("f5-tts-small")
            f5_model.to(f5_device)
            f5_model.eval()
            logger.info("✅ F5-TTS loaded")
        return f5_model
    
    USE_F5_TTS = True
    logger.info("✅ F5-TTS available")
except ImportError as e:
    logger.warning(f"⚠️ F5-TTS not available: {e}")
    try:
        import edge_tts
        USE_EDGE_TTS = True
        logger.info("✅ Edge-TTS available")
    except ImportError:
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            if len(voices) > 1:
                engine.setProperty('voice', voices[1].id)
            engine.setProperty('rate', 160)
            engine.setProperty('volume', 0.9)
            logger.info("✅ pyttsx3 available")
        except ImportError:
            logger.warning("⚠️ No TTS engine found")

class VoicePlugin:
    async def speak(self, text: str) -> dict:
        """Generate speech with human-like emoji sounds"""
        try:
            # Preprocess text - convert emojis to human sounds
            processed_text = preprocess_text_for_speech(text)
            
            timestamp = int(time.time() * 1000)
            filepath = None
            
            if USE_F5_TTS:
                filename = f"lucy_{timestamp}.wav"
                filepath = AUDIO_DIR / filename
                
                try:
                    model = init_f5()
                    ref_audio = Path(__file__).parent.parent / "voice" / "ref_female.wav"
                    
                    with torch.no_grad():
                        output = model.generate(
                            text=processed_text,
                            ref_audio=str(ref_audio) if ref_audio.exists() else None,
                            speed=1.0,
                            emotion="neutral"
                        )
                    
                    torchaudio.save(str(filepath), output, sample_rate=24000)
                except Exception as f5_err:
                    logger.warning(f"⚠️ F5-TTS failed: {f5_err}, falling back")
                    filepath = None
            
            if USE_EDGE_TTS and (not USE_F5_TTS or filepath is None or not filepath.exists()):
                filename = f"lucy_{timestamp}.mp3"
                filepath = AUDIO_DIR / filename
                communicate = edge_tts.Communicate(processed_text, "en-US-JennyNeural")
                await communicate.save(str(filepath))
                
            elif not USE_F5_TTS and not USE_EDGE_TTS and filepath is None:
                filename = f"lucy_{timestamp}.wav"
                filepath = AUDIO_DIR / filename
                engine.save_to_file(processed_text, str(filepath))
                engine.runAndWait()
            
            if filepath and filepath.exists() and filepath.stat().st_size > 100:
                logger.info(f"✅ Speech generated: {filename}")
                logger.info(f"📝 Original: {text[:50]}...")
                logger.info(f"📝 Processed: {processed_text[:50]}...")
                return {"status": "ready", "file": filename}
            else:
                return {"status": "error", "message": "File creation failed"}
                
        except Exception as e:
            logger.error(f"❌ Voice error: {e}")
            return {"status": "error", "message": str(e)}

voice = VoicePlugin()