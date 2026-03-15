"""
Emotional memory - links emotions to memories
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

class EmotionalMemory:
    """
    Stores emotional associations with memories
    """
    
    def __init__(self, db_path="lucy_emotional.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Emotional tags table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotional_tags (
                memory_id TEXT,
                memory_type TEXT,
                emotion TEXT,
                intensity REAL,
                timestamp DATETIME,
                context TEXT,
                PRIMARY KEY (memory_id, memory_type, emotion)
            )
        ''')
        
        # Emotional patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotional_patterns (
                id TEXT PRIMARY KEY,
                trigger TEXT,
                emotional_response TEXT,
                intensity REAL,
                frequency INTEGER,
                last_occurrence DATETIME
            )
        ''')
        
        # Emotional stats
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotional_stats (
                date DATE,
                dominant_emotion TEXT,
                emotion_counts TEXT,
                avg_intensity REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def tag_memory(self, memory_id: str, memory_type: str, 
                    emotion: str, intensity: float = 0.5,
                    context: Dict = None):
        """
        Tag a memory with emotional content
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO emotional_tags
            (memory_id, memory_type, emotion, intensity, timestamp, context)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (memory_id, memory_type, emotion, intensity, datetime.now(),
              json.dumps(context or {})))
        
        conn.commit()
        conn.close()
    
    def get_memory_emotions(self, memory_id: str, memory_type: str) -> List[Dict]:
        """
        Get emotional tags for a memory
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT emotion, intensity, timestamp, context
            FROM emotional_tags
            WHERE memory_id = ? AND memory_type = ?
            ORDER BY intensity DESC
        ''', (memory_id, memory_type))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'emotion': row[0],
            'intensity': row[1],
            'timestamp': row[2],
            'context': json.loads(row[3]) if row[3] else {}
        } for row in rows]
    
    def find_memories_by_emotion(self, emotion: str, 
                                   min_intensity: float = 0.3,
                                   limit: int = 50) -> List[Dict]:
        """
        Find memories with specific emotion
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT memory_id, memory_type, intensity, timestamp, context
            FROM emotional_tags
            WHERE emotion = ? AND intensity >= ?
            ORDER BY intensity DESC, timestamp DESC
            LIMIT ?
        ''', (emotion, min_intensity, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'memory_id': row[0],
            'memory_type': row[1],
            'intensity': row[2],
            'timestamp': row[3],
            'context': json.loads(row[4]) if row[4] else {}
        } for row in rows]
    
    def add_pattern(self, trigger: str, emotional_response: str,
                     intensity: float = 0.5):
        """
        Add an emotional response pattern
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if pattern exists
        cursor.execute('''
            SELECT id, frequency
            FROM emotional_patterns
            WHERE trigger = ? AND emotional_response = ?
        ''', (trigger, emotional_response))
        
        row = cursor.fetchone()
        
        if row:
            # Update existing
            cursor.execute('''
                UPDATE emotional_patterns
                SET frequency = ?, last_occurrence = ?, intensity = ?
                WHERE id = ?
            ''', (row[1] + 1, datetime.now(), intensity, row[0]))
        else:
            # Create new
            import hashlib
            pattern_id = hashlib.md5(f"{trigger}{emotional_response}".encode()).hexdigest()[:16]
            
            cursor.execute('''
                INSERT INTO emotional_patterns
                (id, trigger, emotional_response, intensity, frequency, last_occurrence)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (pattern_id, trigger, emotional_response, intensity, 1, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def predict_emotion(self, trigger: str) -> Optional[Dict]:
        """
        Predict emotional response to trigger
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT emotional_response, intensity, frequency
            FROM emotional_patterns
            WHERE trigger LIKE ?
            ORDER BY frequency DESC, last_occurrence DESC
            LIMIT 1
        ''', (f'%{trigger}%',))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'emotion': row[0],
                'intensity': row[1],
                'confidence': min(1.0, row[2] / 10)
            }
        return None
    
    def get_emotional_summary(self, days: int = 7) -> Dict:
        """
        Get emotional summary for period
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = datetime.now().date() - timedelta(days=days)
        
        cursor.execute('''
            SELECT emotion, COUNT(*), AVG(intensity)
            FROM emotional_tags
            WHERE date(timestamp) >= ?
            GROUP BY emotion
            ORDER BY COUNT(*) DESC
        ''', (cutoff,))
        
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            return {
                'dominant': rows[0][0],
                'emotions': {r[0]: {'count': r[1], 'avg_intensity': r[2]} for r in rows},
                'total': sum(r[1] for r in rows)
            }
        return {'dominant': 'neutral', 'emotions': {}, 'total': 0}