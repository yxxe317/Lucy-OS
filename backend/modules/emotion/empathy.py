"""
Empathy Module - Simulates understanding of others' emotions
"""

import re
from typing import Dict, List, Optional, Tuple

class Empathy:
    """
    Simulates empathy by recognizing and responding to emotional cues
    """
    
    def __init__(self, mood_engine=None):
        self.mood_engine = mood_engine
        
        # Emotional cue patterns
        self.emotion_patterns = {
            'joy': [
                r'\bhappy\b', r'\bglad\b', r'\bgreat\b', r'\bexcellent\b',
                r'\bwonderful\b', r'\bawesome\b', r'\blove\b', r'\bamazing\b',
                r'😊', r'😄', r'👍', r':\)', r'=\)'
            ],
            'sadness': [
                r'\bsad\b', r'\bunhappy\b', r'\bdepressed\b', r'\bdown\b',
                r'\bcrying\b', r'\bheartbroken\b', r'😢', r'😭', r':\(', r'=\('
            ],
            'anger': [
                r'\bangry\b', r'\bmad\b', r'\bfurious\b', r'\bannoyed\b',
                r'\bfrustrated\b', r'\bhate\b', r'😠', r'💢', r'>:\('
            ],
            'fear': [
                r'\bafraid\b', r'\bscared\b', r'\bfrightened\b', r'\bnervous\b',
                r'\bworried\b', r'\banxious\b', r'😨', r'😱'
            ],
            'surprise': [
                r'\bsurprised\b', r'\bshocked\b', r'\bwow\b', r'\bomg\b',
                r'\bunbelievable\b', r'😲', r'😮', r':O'
            ],
            'disgust': [
                r'\bdisgusted\b', r'\brepulsed\b', r'\bgross\b', r'\byuck\b',
                r'😒', r'😖', r':S'
            ],
            'trust': [
                r'\btrust\b', r'\bbelieve\b', r'\brely\b', r'\bconfident\b',
                r'\bsure\b', r'\bcertain\b', r'🤝'
            ],
            'anticipation': [
                r'\bexpect\b', r'\banticipate\b', r'\bexcited for\b',
                r'\bcannot wait\b', r'\blooking forward\b', r'🎉'
            ]
        }
        
        # Empathetic responses
        self.empathetic_responses = {
            'joy': [
                "I'm so happy to hear that!",
                "That's wonderful!",
                "Your happiness brings me joy too.",
                "That's fantastic news!"
            ],
            'sadness': [
                "I'm sorry you're feeling this way.",
                "That sounds really difficult.",
                "I'm here for you.",
                "Would talking about it help?"
            ],
            'anger': [
                "I understand why you'd feel that way.",
                "That must be frustrating.",
                "Your feelings are valid.",
                "Let's work through this together."
            ],
            'fear': [
                "It's okay to feel scared.",
                "You're safe. I'm here with you.",
                "Let's take this one step at a time.",
                "What would help you feel better?"
            ],
            'surprise': [
                "Wow, that is surprising!",
                "I can see why you'd be surprised.",
                "Life is full of surprises, isn't it?",
                "That's unexpected!"
            ],
            'disgust': [
                "I understand your reaction.",
                "That doesn't sound pleasant.",
                "I see why you'd feel that way.",
                "Let's focus on something better."
            ],
            'trust': [
                "Thank you for trusting me.",
                "I value your trust.",
                "You can always count on me.",
                "Trust is important to me too."
            ],
            'anticipation': [
                "Exciting! I'm looking forward to it too.",
                "The anticipation is part of the fun!",
                "I hope it exceeds your expectations.",
                "Count me in!"
            ]
        }
    
    def analyze_emotion(self, text: str) -> Dict[str, float]:
        """
        Analyze emotional content of text
        """
        text_lower = text.lower()
        emotions = {emotion: 0.0 for emotion in self.emotion_patterns}
        
        for emotion, patterns in self.emotion_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text_lower)
                if matches:
                    emotions[emotion] += len(matches) * 0.3
        
        # Normalize
        total = sum(emotions.values())
        if total > 0:
            for emotion in emotions:
                emotions[emotion] /= total
        
        return emotions
    
    def get_dominant_emotion(self, text: str) -> Tuple[str, float]:
        """
        Get the dominant emotion in text
        """
        emotions = self.analyze_emotion(text)
        dominant = max(emotions.items(), key=lambda x: x[1])
        return dominant
    
    def generate_empathetic_response(self, text: str) -> str:
        """
        Generate an empathetic response
        """
        dominant_emotion, confidence = self.get_dominant_emotion(text)
        
        # Update mood engine if available
        if self.mood_engine and confidence > 0.3:
            sentiment = {'positivity': 0, 'negativity': 0}
            if dominant_emotion in ['joy', 'trust', 'anticipation']:
                sentiment['positivity'] = confidence
            elif dominant_emotion in ['sadness', 'anger', 'fear', 'disgust']:
                sentiment['negativity'] = confidence
            elif dominant_emotion == 'surprise':
                sentiment['positivity'] = confidence * 0.5
                sentiment['negativity'] = confidence * 0.5
            
            self.mood_engine.update_from_sentiment(sentiment)
        
        # Get appropriate response
        if confidence > 0.2 and dominant_emotion in self.empathetic_responses:
            import random
            responses = self.empathetic_responses[dominant_emotion]
            return random.choice(responses)
        
        # Default empathetic response
        return "I hear you. Tell me more about that."
    
    def validate_emotional_response(self, text: str, response: str) -> bool:
        """
        Check if response matches emotional context
        """
        text_emotion, _ = self.get_dominant_emotion(text)
        response_emotion, _ = self.get_dominant_emotion(response)
        
        # Response should be emotionally appropriate
        if text_emotion in ['sadness', 'anger', 'fear']:
            if response_emotion in ['joy', 'surprise']:
                return False
        
        return True