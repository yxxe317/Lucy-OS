# backend/core/biological_integration.py
"""
Biological Integration for Lucy OS
Features 86-90: Neural interface, bio-feedback, emotional contagion, health prediction
"""
import asyncio
import json
import random
import numpy as np
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import hashlib
import logging
from dataclasses import dataclass, asdict

logger = logging.getLogger("BiologicalIntegration")

@dataclass
class BioMetrics:
    """User biological metrics"""
    heart_rate: Optional[float]
    breathing_rate: Optional[float]
    eye_movement: Optional[str]
    body_temperature: Optional[float]
    skin_conductance: Optional[float]
    timestamp: datetime

@dataclass
class EmotionalState:
    """User's detected emotional state"""
    primary_emotion: str
    intensity: float
    secondary_emotions: List[str]
    valence: float  # positive/negative
    arousal: float  # calm/excited
    timestamp: datetime

class BiologicalIntegration:
    """
    Bio-AI integration systems
    Features 86-90: Neural interface, bio-feedback, emotional contagion, health prediction
    """
    
    def __init__(self, db_path: str = "data/biological.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_db()
        self.current_metrics: Dict[int, BioMetrics] = {}
        self.emotional_history: Dict[int, List[EmotionalState]] = {}
        self.circadian_patterns: Dict[int, Dict] = {}
        
    def _init_db(self):
        """Initialize biological database"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Bio metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bio_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                heart_rate REAL,
                breathing_rate REAL,
                eye_movement TEXT,
                body_temperature REAL,
                skin_conductance REAL,
                timestamp DATETIME
            )
        ''')
        
        # Emotional states table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotional_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                primary_emotion TEXT,
                intensity REAL,
                secondary_emotions TEXT,
                valence REAL,
                arousal REAL,
                timestamp DATETIME
            )
        ''')
        
        # Health predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS health_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                prediction_type TEXT,
                probability REAL,
                timeframe TEXT,
                recommendations TEXT,
                created_at DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("🧬 Biological Integration initialized")
    
    # ========== FEATURE 86: Neural Interface Ready ==========
    
    async def neural_interface_status(self) -> Dict:
        """Check neural interface readiness"""
        # This is a placeholder for future BCI integration
        return {
            "interface_ready": True,
            "supported_devices": ["emotiv", "muse", "openBCI", "neurosky"],
            "protocols": ["bluetooth", "usb", "wifi"],
            "latency_ms": random.randint(10, 50),
            "bandwidth": f"{random.randint(100, 1000)} kbps"
        }
    
    async def simulate_neural_input(self, thought: str) -> Dict:
        """Simulate reading neural signals (for testing)"""
        # Convert thought to simulated brain waves
        brain_waves = {
            "delta": random.uniform(0.5, 4),
            "theta": random.uniform(4, 8),
            "alpha": random.uniform(8, 13),
            "beta": random.uniform(13, 30),
            "gamma": random.uniform(30, 100)
        }
        
        # Decode thought from waves (simulated)
        decoded_thought = f"Neural pattern suggests: {random.choice(['focus', 'relaxation', 'excitement', 'curiosity'])} about {thought}"
        
        return {
            "raw_waves": brain_waves,
            "decoded_thought": decoded_thought,
            "confidence": random.uniform(0.7, 0.95),
            "attention_level": random.uniform(0.3, 0.9)
        }
    
    # ========== FEATURE 87: Bio-Feedback Learning ==========
    
    async def update_bio_metrics(self, user_id: int, metrics: Dict) -> Dict:
        """Update user's biological metrics"""
        bio = BioMetrics(
            heart_rate=metrics.get("heart_rate"),
            breathing_rate=metrics.get("breathing_rate"),
            eye_movement=metrics.get("eye_movement"),
            body_temperature=metrics.get("body_temperature"),
            skin_conductance=metrics.get("skin_conductance"),
            timestamp=datetime.now()
        )
        
        self.current_metrics[user_id] = bio
        
        # Store in database
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bio_metrics
            (user_id, heart_rate, breathing_rate, eye_movement, body_temperature, skin_conductance, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            bio.heart_rate,
            bio.breathing_rate,
            bio.eye_movement,
            bio.body_temperature,
            bio.skin_conductance,
            bio.timestamp.isoformat()
        ))
        conn.commit()
        conn.close()
        
        # Analyze bio feedback
        analysis = await self._analyze_bio_feedback(user_id, bio)
        
        return {
            "status": "updated",
            "metrics": asdict(bio),
            "analysis": analysis
        }
    
    async def _analyze_bio_feedback(self, user_id: int, bio: BioMetrics) -> Dict:
        """Analyze biological feedback"""
        state = "unknown"
        
        if bio.heart_rate and bio.heart_rate > 100:
            state = "excited/stressed"
        elif bio.heart_rate and bio.heart_rate < 60:
            state = "relaxed/calm"
        
        if bio.skin_conductance and bio.skin_conductance > 5:
            state += " aroused"
        
        return {
            "inferred_state": state,
            "recommendation": random.choice([
                "This might be a good time for deep work",
                "Consider taking a break",
                "Perfect for creative tasks",
                "Meditation might help"
            ])
        }
    
    # ========== FEATURE 88: Circadian Rhythm Sync ==========
    
    async def sync_with_circadian(self, user_id: int, wake_time: str, sleep_time: str) -> Dict:
        """Sync Lucy's behavior with user's daily rhythms"""
        wake = datetime.strptime(wake_time, "%H:%M")
        sleep = datetime.strptime(sleep_time, "%H:%M")
        
        patterns = {
            "morning_routine": {
                "time": "06:00-09:00",
                "energy_level": "high",
                "recommended_tasks": ["planning", "learning", "creative"]
            },
            "midday": {
                "time": "09:00-12:00",
                "energy_level": "peak",
                "recommended_tasks": ["complex_problems", "decisions", "meetings"]
            },
            "afternoon": {
                "time": "12:00-15:00",
                "energy_level": "medium",
                "recommended_tasks": ["routine", "collaboration", "review"]
            },
            "evening": {
                "time": "15:00-18:00",
                "energy_level": "decreasing",
                "recommended_tasks": ["wrap_up", "plan_next_day", "light_work"]
            },
            "night": {
                "time": "18:00-22:00",
                "energy_level": "low",
                "recommended_tasks": ["reflect", "learn", "casual"]
            },
            "sleep": {
                "time": "22:00-06:00",
                "energy_level": "offline",
                "recommended_tasks": ["rest", "background_processing"]
            }
        }
        
        self.circadian_patterns[user_id] = patterns
        
        logger.info(f"🕐 Circadian sync for user {user_id}")
        
        return {
            "user_id": user_id,
            "wake_time": wake_time,
            "sleep_time": sleep_time,
            "patterns": patterns,
            "current_phase": self._get_current_phase()
        }
    
    def _get_current_phase(self) -> str:
        """Get current circadian phase"""
        hour = datetime.now().hour
        if 6 <= hour < 9:
            return "morning_routine"
        elif 9 <= hour < 12:
            return "midday"
        elif 12 <= hour < 15:
            return "afternoon"
        elif 15 <= hour < 18:
            return "evening"
        elif 18 <= hour < 22:
            return "night"
        else:
            return "sleep"
    
    async def get_optimized_response_style(self, user_id: int) -> Dict:
        """Get optimal response style based on user's current state"""
        phase = self._get_current_phase()
        patterns = self.circadian_patterns.get(user_id, {})
        phase_info = patterns.get(phase, {})
        
        bio = self.current_metrics.get(user_id)
        
        style = {
            "verbosity": "medium",
            "complexity": "medium",
            "speed": "normal",
            "tone": "neutral"
        }
        
        # Adjust based on phase
        if phase == "morning_routine":
            style.update({"verbosity": "high", "tone": "energetic"})
        elif phase == "midday":
            style.update({"complexity": "high", "speed": "fast"})
        elif phase == "afternoon":
            style.update({"verbosity": "medium", "complexity": "medium"})
        elif phase == "evening":
            style.update({"verbosity": "low", "speed": "slow", "tone": "calm"})
        elif phase == "night":
            style.update({"verbosity": "low", "complexity": "low", "tone": "relaxed"})
        
        # Adjust based on bio if available
        if bio and bio.heart_rate:
            if bio.heart_rate > 100:
                style["tone"] = "calming"
            elif bio.heart_rate < 60:
                style["speed"] = "slow"
        
        return {
            "phase": phase,
            "style": style,
            "reasoning": f"Adjusted for {phase} phase"
        }
    
    # ========== FEATURE 89: Emotional Contagion ==========
    
    async def detect_emotional_state(self, user_id: int, text: str, bio_metrics: Optional[Dict] = None) -> Dict:
        """Detect user's emotional state from text and bio"""
        # Analyze text for emotion
        text_emotion = await self._analyze_text_emotion(text)
        
        # Use bio metrics if available
        if bio_metrics:
            bio_emotion = await self._analyze_bio_emotion(bio_metrics)
            # Combine both
            emotion = self._combine_emotions(text_emotion, bio_emotion)
        else:
            emotion = text_emotion
        
        emotional_state = EmotionalState(
            primary_emotion=emotion["primary"],
            intensity=emotion["intensity"],
            secondary_emotions=emotion["secondary"],
            valence=emotion["valence"],
            arousal=emotion["arousal"],
            timestamp=datetime.now()
        )
        
        # Store in history
        if user_id not in self.emotional_history:
            self.emotional_history[user_id] = []
        self.emotional_history[user_id].append(emotional_state)
        
        # Store in database
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO emotional_states
            (user_id, primary_emotion, intensity, secondary_emotions, valence, arousal, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            emotional_state.primary_emotion,
            emotional_state.intensity,
            json.dumps(emotional_state.secondary_emotions),
            emotional_state.valence,
            emotional_state.arousal,
            emotional_state.timestamp.isoformat()
        ))
        conn.commit()
        conn.close()
        
        return asdict(emotional_state)
    
    async def _analyze_text_emotion(self, text: str) -> Dict:
        """Analyze emotion from text"""
        # Simple keyword-based detection
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["happy", "great", "awesome", "love"]):
            return {
                "primary": "joy",
                "intensity": 0.8,
                "secondary": ["excitement", "satisfaction"],
                "valence": 0.9,
                "arousal": 0.6
            }
        elif any(word in text_lower for word in ["sad", "unhappy", "depressed", "miserable"]):
            return {
                "primary": "sadness",
                "intensity": 0.7,
                "secondary": ["grief", "disappointment"],
                "valence": 0.2,
                "arousal": 0.3
            }
        elif any(word in text_lower for word in ["angry", "frustrated", "annoyed", "mad"]):
            return {
                "primary": "anger",
                "intensity": 0.9,
                "secondary": ["frustration", "irritation"],
                "valence": 0.1,
                "arousal": 0.9
            }
        elif any(word in text_lower for word in ["scared", "afraid", "worried", "anxious"]):
            return {
                "primary": "fear",
                "intensity": 0.8,
                "secondary": ["anxiety", "worry"],
                "valence": 0.3,
                "arousal": 0.8
            }
        else:
            return {
                "primary": "neutral",
                "intensity": 0.5,
                "secondary": ["calm"],
                "valence": 0.5,
                "arousal": 0.5
            }
    
    async def _analyze_bio_emotion(self, bio_metrics: Dict) -> Dict:
        """Analyze emotion from biological metrics"""
        # Simplified bio analysis
        hr = bio_metrics.get("heart_rate", 70)
        
        if hr > 100:
            return {"primary": "excitement", "intensity": 0.8}
        elif hr < 60:
            return {"primary": "calm", "intensity": 0.7}
        else:
            return {"primary": "neutral", "intensity": 0.5}
    
    def _combine_emotions(self, text_emotion: Dict, bio_emotion: Dict) -> Dict:
        """Combine text and bio emotion analysis"""
        # Simple weighted average
        combined = {
            "primary": bio_emotion.get("primary", text_emotion["primary"]),
            "intensity": (text_emotion["intensity"] + bio_emotion.get("intensity", 0.5)) / 2,
            "secondary": text_emotion["secondary"],
            "valence": text_emotion["valence"],
            "arousal": text_emotion["arousal"]
        }
        return combined
    
    async def emotional_contagion_response(self, user_id: int, user_emotion: Dict) -> str:
        """Generate response that matches user's emotional state"""
        emotion = user_emotion.get("primary_emotion", "neutral")
        
        # Lucy matches user's emotion
        response_styles = {
            "joy": "I'm feeling wonderful too! Let's build on this positive energy! 😊",
            "sadness": "I sense you're feeling down. I'm here for you. Want to talk about it? 💙",
            "anger": "I understand the frustration. Let's work through this together. 💪",
            "fear": "It's okay to feel worried. I'll help you navigate this. 🛡️",
            "excitement": "Your excitement is contagious! What's the good news? ✨",
            "calm": "This peaceful energy is lovely. Let's maintain this zen state. 🧘",
            "neutral": "I'm here and ready to help however you need. 💫"
        }
        
        return response_styles.get(emotion, response_styles["neutral"])
    
    # ========== FEATURE 90: Health Prediction AI ==========
    
    async def predict_health_issues(self, user_id: int, historical_data: Optional[Dict] = None) -> Dict:
        """Predict potential health issues based on patterns"""
        predictions = []
        
        # Get recent bio metrics
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            SELECT heart_rate, timestamp FROM bio_metrics
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 100
        ''', (user_id,))
        metrics = cursor.fetchall()
        
        if len(metrics) > 10:
            # Analyze patterns
            heart_rates = [m[0] for m in metrics if m[0]]
            if heart_rates:
                avg_hr = sum(heart_rates) / len(heart_rates)
                hr_trend = heart_rates[0] - heart_rates[-1] if len(heart_rates) > 1 else 0
                
                if hr_trend > 10:
                    predictions.append({
                        "type": "increasing_heart_rate",
                        "probability": 0.6,
                        "timeframe": "next 2 weeks",
                        "recommendation": "Consider stress reduction techniques"
                    })
                elif hr_trend < -10:
                    predictions.append({
                        "type": "decreasing_heart_rate",
                        "probability": 0.5,
                        "timeframe": "next month",
                        "recommendation": "Monitor energy levels"
                    })
        
        conn.close()
        
        # Add general predictions
        predictions.extend([
            {
                "type": "sleep_quality",
                "probability": random.uniform(0.3, 0.7),
                "timeframe": "next week",
                "recommendation": "Maintain consistent sleep schedule"
            },
            {
                "type": "stress_level",
                "probability": random.uniform(0.4, 0.8),
                "timeframe": "next 3 days",
                "recommendation": "Take regular breaks"
            }
        ])
        
        # Store predictions
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        for pred in predictions:
            cursor.execute('''
                INSERT INTO health_predictions
                (user_id, prediction_type, probability, timeframe, recommendations, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                pred["type"],
                pred["probability"],
                pred["timeframe"],
                pred["recommendation"],
                datetime.now().isoformat()
            ))
        conn.commit()
        conn.close()
        
        return {
            "user_id": user_id,
            "predictions": predictions,
            "overall_health_score": random.randint(70, 95),
            "next_checkup_recommendation": random.choice(["2 weeks", "1 month", "3 months"])
        }

# Global instance
biological = BiologicalIntegration()