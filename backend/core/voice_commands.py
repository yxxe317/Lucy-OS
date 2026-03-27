import re
import logging
from typing import Dict, List, Tuple, Optional, Any

logger = logging.getLogger("VoiceCommands")

# ═══════════════════════════════════════════════════════════════
# INTENT PATTERN MATCHING
# ═══════════════════════════════════════════════════════════════
COMMAND_PATTERNS: Dict[str, List[Tuple[str, str]]] = {
    "greeting": [
        (r"hello\s+lucy", "greeting"),
        (r"hi\s+lucy", "greeting"),
        (r"hey\s+lucy", "greeting"),
        (r"welcome\s+lucy", "greeting"),
        (r"good\s+morning\s+lucy", "greeting"),
        (r"good\s+evening\s+lucy", "greeting"),
        (r"good\s+night\s+lucy", "greeting"),
    ],
    "status": [
        (r"how\s+are\s+you", "status"),
        (r"what's\s+up", "status"),
        (r"tell\s+me\s+about\s+yourself", "status"),
        (r"who\s+are\s+you", "status"),
        (r"introduce\s+yourself", "status"),
    ],
    "time_date": [
        (r"what\s+time\s+is\s+it", "time"),
        (r"tell\s+me\s+the\s+time", "time"),
        (r"what\s+date\s+is\s+it", "date"),
        (r"what's\s+today's\s+date", "date"),
        (r"what\s+day\s+is\s+it", "day"),
    ],
    "joke": [
        (r"tell\s+a\s+joke", "joke"),
        (r"make\s+me\s+laugh", "joke"),
        (r"i\s+need\s+a\s+laugh", "joke"),
        (r"entertain\s+me", "joke"),
        (r"something\s+funny", "joke"),
    ],
    "help": [
        (r"help\s+lucy", "help"),
        (r"what\s+can\s+you\s+do", "help"),
        (r"show\s+me\s+your\s+commands", "help"),
        (r"capabilities", "help"),
        (r"features", "help"),
    ],
    "emotion": [
        (r"i\s+am\s+happy", "happy"),
        (r"i\s+am\s+sad", "sad"),
        (r"i\s+am\s+angry", "angry"),
        (r"i\s+am\s+excited", "excited"),
        (r"i\s+am\s+confused", "confused"),
        (r"i\s+am\s+worried", "worried"),
        (r"i\s+am\s+tired", "tired"),
        (r"i\s+am\s+happy", "happy"),
        (r"i\s+am\s+sad", "sad"),
        (r"i\s+am\s+angry", "angry"),
        (r"i\s+am\s+excited", "excited"),
        (r"i\s+am\s+confused", "confused"),
        (r"i\s+am\s+worried", "worried"),
        (r"i\s+am\s+tired", "tired"),
    ],
    "default": [
        (r".+", "default"),
    ],
}

# ═══════════════════════════════════════════════════════════════
# RESPONSE TEMPLATES
# ═══════════════════════════════════════════════════════════════
RESPONSE_TEMPLATES: Dict[str, List[str]] = {
    "greeting": [
        "Hello! I'm Lucy, your AI companion. How can I assist you today?",
        "Greetings! I'm Lucy. What would you like to talk about?",
        "Hi there! I'm Lucy. I'm here to help you with anything you need.",
        "Welcome! I'm Lucy, your AI assistant. What can I do for you?",
    ],
    "status": [
        "I'm Lucy, an AI designed to assist and converse with you. I can help with information, conversation, and various tasks. What would you like to discuss?",
        "I'm Lucy, your AI companion. I'm here to help with questions, conversation, and assistance. How can I be useful to you today?",
        "I'm Lucy, an AI assistant created to be helpful and engaging. I can assist with a wide range of topics and tasks. What interests you?",
    ],
    "time": [
        "The current time is {hour}:{minute} {ampm}. Is there anything else you'd like to know?",
        "It's currently {hour}:{minute} {ampm} for you. What else can I help you with?",
        "The time is {hour}:{minute} {ampm}. I'm here if you need anything else!",
    ],
    "date": [
        "Today is {month} {day}, {year}. Is there anything I can help you with?",
        "The current date is {month} {day}, {year}. What would you like to discuss?",
        "It's {month} {day}, {year}. I'm Lucy, and I'm here to assist you!",
    ],
    "joke": [
        "Why did the AI cross the road? To optimize the other side's algorithm!",
        "I told my AI a joke about recursion. It just said 'I'm still working on the punchline'.",
        "What's an AI's favorite type of music? Anything with good algorithms!",
        "Why don't AI systems tell secrets? Because they have too many firewalls!",
    ],
    "help": [
        "I can help you with greetings, time and date, telling jokes, understanding your emotions, and having general conversations. Just ask me anything!",
        "Here's what I can do: greet you, tell you the time and date, share jokes, detect your emotions, and chat about anything. What would you like to try?",
        "I'm capable of: greeting, time/date queries, joke-telling, emotion detection, and general conversation. Feel free to ask me anything!",
    ],
    "happy": [
        "I'm so glad to hear you're happy! What made you smile today?",
        "Your happiness is contagious! Tell me more about what's making you feel this way.",
        "I'm delighted to hear you're happy! What's the occasion?",
    ],
    "sad": [
        "I'm sorry to hear you're having a tough time. I'm here to listen if you want to talk about it.",
        "I understand that you're feeling sad. Remember, I'm here for you whenever you need to talk.",
        "I'm sorry you're feeling down. Would you like to share what's on your mind?",
    ],
    "angry": [
        "I'm sorry you're feeling angry. Is there something I can help you with or resolve?",
        "I understand you're upset. I'm here to help if there's anything I can do to assist.",
        "I'm sorry to hear you're angry. Please let me know if there's something I can help with.",
    ],
    "excited": [
        "Your excitement is wonderful! What's got you so pumped up?",
        "I love your enthusiasm! Tell me more about what's exciting you.",
        "Your excitement is contagious! What's making you so thrilled?",
    ],
    "confused": [
        "I understand confusion. Is there something specific I can clarify or help you with?",
        "It's okay to be confused. I'm here to help explain or assist with whatever you need.",
        "I'm here to help clear things up. What's confusing you right now?",
    ],
    "worried": [
        "I'm here for you. If you're worried about something, please let me know how I can help.",
        "I understand your concerns. Is there something specific I can assist you with?",
        "I'm here to support you. What's worrying you, and how can I help?",
    ],
    "tired": [
        "I hope you get some rest soon. Take care of yourself!",
        "Rest is important. I hope you're able to recharge soon.",
        "I hope you're able to get some good rest. Take care!",
    ],
    "default": [
        "That's interesting! Tell me more.",
        "I see. What else would you like to discuss?",
        "Fascinating! Is there more you'd like to share?",
        "I'm listening. What else is on your mind?",
    ],
}

# ═══════════════════════════════════════════════════════════════
# VOICE PROCESSOR CLASS
# ═══════════════════════════════════════════════════════════════
class VoiceProcessor:
    """
    Voice command processor for intent detection and response generation
    """
    
    def __init__(self):
        self.logger = logger
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for efficient matching"""
        self.compiled_patterns: Dict[str, List[Tuple[re.Pattern, str]]] = {}
        for intent, patterns in COMMAND_PATTERNS.items():
            compiled = []
            for pattern_str, intent_name in patterns:
                try:
                    compiled.append((re.compile(pattern_str, re.IGNORECASE), intent_name))
                except re.error as e:
                    self.logger.warning(f"Invalid regex pattern '{pattern_str}': {e}")
            self.compiled_patterns[intent] = compiled
    
    def detect_intent(self, text: str) -> Tuple[str, float]:
        """
        Detect the intent from voice input text
        
        Args:
            text: The input text to analyze
            
        Returns:
            Tuple of (intent_name, confidence_score)
        """
        if not text or not text.strip():
            return ("default", 0.0)
        
        text = text.strip()
        max_confidence = 0.0
        best_intent = "default"
        
        # Check each intent category
        for intent_name, patterns in self.compiled_patterns.items():
            if intent_name == "default":
                continue
            
            for pattern, _ in patterns:
                if pattern.match(text):
                    # Higher confidence for more specific patterns
                    confidence = min(len(pattern.pattern) / 50.0, 1.0)
                    if confidence > max_confidence:
                        max_confidence = confidence
                        best_intent = intent_name
        
        return (best_intent, max_confidence)
    
    def generate_response(self, intent: str, text: str) -> str:
        """
        Generate an appropriate response based on detected intent
        
        Args:
            intent: The detected intent name
            text: The original input text
            
        Returns:
            A human-like response string
        """
        templates = RESPONSE_TEMPLATES.get(intent, RESPONSE_TEMPLATES["default"])
        response = templates[len(templates) - 1]  # Pick last template
        
        # Replace placeholders with actual values
        if intent in ["time", "date"]:
            import datetime
            now = datetime.datetime.now()
            response = response.replace("{hour}", str(now.hour))
            response = response.replace("{minute}", str(now.minute).zfill(2))
            response = response.replace("{ampm}", "AM" if now.hour < 12 else "PM")
            response = response.replace("{month}", now.strftime("%B"))
            response = response.replace("{day}", str(now.day))
            response = response.replace("{year}", str(now.year))
        
        return response
    
    def process_command(self, text: str) -> Dict[str, Any]:
        """
        Process a voice command and return structured result
        
        Args:
            text: The input voice command text
            
        Returns:
            Dictionary containing intent, response, and confidence
        """
        intent, confidence = self.detect_intent(text)
        response = self.generate_response(intent, text)
        
        return {
            "intent": intent,
            "confidence": round(confidence, 3),
            "response": response,
            "input": text,
            "processor": "voice_commands"
        }

# ═══════════════════════════════════════════════════════════════
# MODULE EXPORTS
# ═══════════════════════════════════════════════════════════════
voice_processor = VoiceProcessor()