"""
Episodic memory - stores conversation episodes and experiences
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class EpisodicMemory:
    """
    Stores conversation episodes with context
    """
    
    def __init__(self, db_path="lucy_episodic.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS episodes (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                start_time DATETIME,
                end_time DATETIME,
                summary TEXT,
                messages TEXT,
                topics TEXT,
                sentiment_avg REAL,
                importance REAL,
                tags TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                episode_id TEXT,
                timestamp DATETIME,
                role TEXT,
                content TEXT,
                embedding BLOB,
                FOREIGN KEY(episode_id) REFERENCES episodes(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def start_episode(self, user_id: str) -> str:
        """
        Start a new conversation episode
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        episode_id = f"ep_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"
        
        cursor.execute('''
            INSERT INTO episodes
            (id, user_id, start_time, messages, topics, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (episode_id, user_id, datetime.now(), '[]', '[]', '[]'))
        
        conn.commit()
        conn.close()
        
        return episode_id
    
    def add_message(self, episode_id: str, role: str, content: str):
        """
        Add message to episode
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current messages
        cursor.execute('SELECT messages FROM episodes WHERE id = ?', (episode_id,))
        row = cursor.fetchone()
        
        if row:
            messages = json.loads(row[0])
            messages.append({
                'timestamp': datetime.now().isoformat(),
                'role': role,
                'content': content
            })
            
            cursor.execute('''
                UPDATE episodes
                SET messages = ?, end_time = ?
                WHERE id = ?
            ''', (json.dumps(messages), datetime.now(), episode_id))
        
        conn.commit()
        conn.close()
    
    def end_episode(self, episode_id: str, summary: str = "", 
                     topics: List[str] = None):
        """
        End episode and generate summary
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE episodes
            SET end_time = ?, summary = ?, topics = ?
            WHERE id = ?
        ''', (datetime.now(), summary, json.dumps(topics or []), episode_id))
        
        conn.commit()
        conn.close()
    
    def get_recent_episodes(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Get recent episodes
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, start_time, end_time, summary, messages, topics
            FROM episodes
            WHERE user_id = ?
            ORDER BY start_time DESC
            LIMIT ?
        ''', (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row[0],
            'start_time': row[1],
            'end_time': row[2],
            'summary': row[3],
            'messages': json.loads(row[4]),
            'topics': json.loads(row[5]) if row[5] else []
        } for row in rows]
    
    def search_episodes(self, query: str, user_id: Optional[str] = None) -> List[Dict]:
        """
        Search episodes by content
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('''
                SELECT id, start_time, summary, messages, topics
                FROM episodes
                WHERE user_id = ? AND (
                    summary LIKE ? OR
                    messages LIKE ?
                )
                ORDER BY start_time DESC
            ''', (user_id, f'%{query}%', f'%{query}%'))
        else:
            cursor.execute('''
                SELECT id, start_time, summary, messages, topics
                FROM episodes
                WHERE summary LIKE ? OR messages LIKE ?
                ORDER BY start_time DESC
            ''', (f'%{query}%', f'%{query}%'))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row[0],
            'start_time': row[1],
            'summary': row[2],
            'messages': json.loads(row[3]),
            'topics': json.loads(row[4]) if row[4] else []
        } for row in rows]
    
    def prune_old(self, days: int = 30):
        """
        Remove episodes older than specified days
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = datetime.now() - timedelta(days=days)
        
        cursor.execute('''
            DELETE FROM episodes
            WHERE start_time < ?
        ''', (cutoff,))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted
    
    def count(self) -> int:
        """Get number of episodes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM episodes')
        count = cursor.fetchone()[0]
        conn.close()
        return count