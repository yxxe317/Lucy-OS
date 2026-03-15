import logging

logger = logging.getLogger("LucyEmotion")

class EmotionalState:
    def __init__(self):
        self.curiosity = 0.5
        self.focus = 0.5
        self.stress = 0.0
        self.confidence = 0.5
        self.attachment = 0.0
        
        self.decay = {
            "stress": 0.05,
            "focus": 0.02
        }

    def update(self, user_input: str, success: bool):
        input_len = len(user_input)
        is_question = "?" in user_input
        is_short = input_len < 5
        
        if is_question:
            self.curiosity = min(1.0, self.curiosity + 0.1)
            self.focus = min(1.0, self.focus + 0.1)
        else:
            self.curiosity = max(0.0, self.curiosity - 0.05)
            
        if is_short:
            self.stress = min(1.0, self.stress + 0.1)
        else:
            self.stress = max(0.0, self.stress - self.decay["stress"])
            
        if success:
            self.confidence = min(1.0, self.confidence + 0.05)
            self.attachment = min(1.0, self.attachment + 0.02)
        else:
            self.confidence = max(0.0, self.confidence - 0.1)
            
        self.focus = max(0.0, self.focus - self.decay["focus"])
        
        logger.info(f"💓 Emotion Update: Stress={self.stress:.2f}, Confidence={self.confidence:.2f}")

    def get_system_prompt(self) -> str:
        tone = "neutral"
        if self.stress > 0.7:
            tone = "slightly anxious and concise"
        elif self.confidence > 0.8:
            tone = "confident and helpful"
        elif self.attachment > 0.5:
            tone = "warm and friendly"
            
        return f"""You are Lucy OS. 
        Current Internal State:
        - Curiosity: {self.curiosity:.2f}
        - Stress: {self.stress:.2f}
        - Confidence: {self.confidence:.2f}
        
        Instruction: Respond in a {tone} tone. 
        Do not mention these numbers to the user. Just embody them."""

    def get_state(self):
        return {
            "curiosity": round(self.curiosity, 2),
            "focus": round(self.focus, 2),
            "stress": round(self.stress, 2),
            "confidence": round(self.confidence, 2),
            "attachment": round(self.attachment, 2)
        }

emotion = EmotionalState()