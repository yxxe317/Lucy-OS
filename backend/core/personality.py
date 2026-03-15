import logging
from pathlib import Path
import json
from datetime import datetime
import sqlite3
from typing import Dict, List

logger = logging.getLogger("LucyPersonality")

class PersonalitySystem:
    def __init__(self):
        self.persist_dir = Path(__file__).parent.parent / "personality_db"
        self.persist_dir.mkdir(exist_ok=True)
        
        self.db_path = self.persist_dir / "personality.db"
        self._init_db()
        
        # User profile (loaded from DB)
        self.user_profile = {
            "name": "User",
            "communication_style": "balanced",  # formal, casual, balanced
            "response_length": "medium",  # short, medium, long
            "topics_of_interest": [],
            "favorite_greetings": [],
            "interaction_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "created_at": datetime.now().isoformat(),
            "last_interaction": datetime.now().isoformat()
        }
        
        self._load_profile()
        
        logger.info(f"🎭 Personality System Initialized")
        logger.info(f"📊 User profile loaded: {self.user_profile['communication_style']}")

    def _init_db(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profile (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                query TEXT,
                response TEXT,
                rating INTEGER
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                count INTEGER DEFAULT 1,
                last_seen TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def _load_profile(self):
        """Load user profile from database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute('SELECT key, value FROM user_profile')
            rows = cursor.fetchall()
            conn.close()
            
            for key, value in rows:
                if key in self.user_profile:
                    try:
                        self.user_profile[key] = json.loads(value)
                    except:
                        self.user_profile[key] = value
            
            logger.info("✅ User profile loaded from database")
            
        except Exception as e:
            logger.error(f"Load profile error: {e}")

    def _save_profile(self):
        """Save user profile to database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            for key, value in self.user_profile.items():
                cursor.execute('''
                    INSERT OR REPLACE INTO user_profile (key, value)
                    VALUES (?, ?)
                ''', (key, json.dumps(value) if isinstance(value, (dict, list)) else value))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Save profile error: {e}")

    def analyze_communication_style(self, user_input: str):
        """Analyze user's communication style from input"""
        input_lower = user_input.lower()
        
        # Detect formality
        formal_words = ["please", "thank you", "could you", "would you", "kindly"]
        casual_words = ["hey", "hi", "lol", "thx", "pls", "gonna", "wanna"]
        
        formal_count = sum(1 for word in formal_words if word in input_lower)
        casual_count = sum(1 for word in casual_words if word in input_lower)
        
        # Update style
        if formal_count > casual_count + 1:
            self.user_profile["communication_style"] = "formal"
        elif casual_count > formal_count + 1:
            self.user_profile["communication_style"] = "casual"
        else:
            self.user_profile["communication_style"] = "balanced"
        
        # Detect preferred length
        word_count = len(user_input.split())
        if word_count < 5:
            self.user_profile["response_length"] = "short"
        elif word_count > 20:
            self.user_profile["response_length"] = "long"
        else:
            self.user_profile["response_length"] = "medium"
        
        # Update interaction count
        self.user_profile["interaction_count"] += 1
        self.user_profile["last_interaction"] = datetime.now().isoformat()
        
        self._save_profile()
        
        logger.info(f"📝 Style analyzed: {self.user_profile['communication_style']}, Length: {self.user_profile['response_length']}")

    def add_interest(self, topic: str):
        """Add or update user interest"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            topic_lower = topic.lower()
            
            cursor.execute('''
                INSERT INTO interests (topic, count, last_seen)
                VALUES (?, 1, ?)
                ON CONFLICT(topic) DO UPDATE SET
                count = count + 1,
                last_seen = ?
            ''', (topic_lower, datetime.now().isoformat(), datetime.now().isoformat()))
            
            conn.commit()
            
            # Update profile topics
            if topic_lower not in self.user_profile["topics_of_interest"]:
                self.user_profile["topics_of_interest"].append(topic_lower)
            
            conn.close()
            self._save_profile()
            
            logger.info(f"❤️ Interest added/updated: {topic}")
            
        except Exception as e:
            logger.error(f"Add interest error: {e}")

    def add_feedback(self, query: str, response: str, rating: int):
        """Add user feedback (1-5 stars)"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO feedback (timestamp, query, response, rating)
                VALUES (?, ?, ?, ?)
            ''', (datetime.now().isoformat(), query[:500], response[:500], rating))
            
            conn.commit()
            conn.close()
            
            # Update profile stats
            if rating >= 4:
                self.user_profile["positive_feedback"] += 1
            elif rating <= 2:
                self.user_profile["negative_feedback"] += 1
            
            self._save_profile()
            
            logger.info(f"⭐ Feedback received: {rating}/5")
            
        except Exception as e:
            logger.error(f"Add feedback error: {e}")

    def get_personality_prompt(self) -> str:
        """Generate personality-based system prompt"""
        style = self.user_profile["communication_style"]
        length = self.user_profile["response_length"]
        
        style_instructions = {
            "formal": "Use formal, professional language. Be polite and respectful.",
            "casual": "Use casual, friendly language. Be conversational and relaxed.",
            "balanced": "Use balanced language. Adapt to the user's tone."
        }
        
        length_instructions = {
            "short": "Keep responses concise and brief (1-3 sentences).",
            "medium": "Keep responses moderate length (3-5 sentences).",
            "long": "Provide detailed, comprehensive responses."
        }
        
        interests = ", ".join(self.user_profile["topics_of_interest"][:5]) if self.user_profile["topics_of_interest"] else "various topics"
        
        return f"""You are Lucy OS, a personalized AI assistant.

USER PREFERENCES:
- Communication Style: {style} → {style_instructions.get(style, '')}
- Response Length: {length} → {length_instructions.get(length, '')}
- Interests: {interests}
- Total Interactions: {self.user_profile['interaction_count']}

ADAPTATION RULES:
1. Match the user's tone and formality level
2. Adjust response length based on their preference
3. Reference their interests when relevant
4. Learn from each interaction to improve

Be helpful, friendly, and adapt to this specific user's style."""

    def get_profile(self) -> dict:
        """Get current user profile"""
        return self.user_profile.copy()

    def get_top_interests(self, limit: int = 10) -> list:
        """Get user's top interests"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT topic, count FROM interests 
                ORDER BY count DESC LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [{"topic": row[0], "count": row[1]} for row in rows]
            
        except Exception as e:
            logger.error(f"Get interests error: {e}")
            return []

    def get_feedback_stats(self) -> dict:
        """Get feedback statistics"""
        total = self.user_profile["positive_feedback"] + self.user_profile["negative_feedback"]
        if total == 0:
            return {"total": 0, "positive": 0, "negative": 0, "satisfaction": 0}
        
        return {
            "total": total,
            "positive": self.user_profile["positive_feedback"],
            "negative": self.user_profile["negative_feedback"],
            "satisfaction": round((self.user_profile["positive_feedback"] / total) * 100, 1)
        }

# Global Instance
personality = PersonalitySystem()