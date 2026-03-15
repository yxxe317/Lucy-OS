"""
Database Integration - SQLite wrapper for persistent storage
"""

import sqlite3
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

class Database:
    """
    SQLite database wrapper for persistent storage
    """
    
    def __init__(self, db_path: str = "lucy_data.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User preferences
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id TEXT PRIMARY KEY,
                preferences TEXT,
                updated_at DATETIME
            )
        ''')
        
        # Conversation history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                timestamp DATETIME,
                role TEXT,
                content TEXT,
                metadata TEXT
            )
        ''')
        
        # Tasks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                title TEXT,
                description TEXT,
                due_date DATETIME,
                priority INTEGER,
                status TEXT,
                created_at DATETIME,
                completed_at DATETIME
            )
        ''')
        
        # Notes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                title TEXT,
                content TEXT,
                tags TEXT,
                created_at DATETIME,
                updated_at DATETIME
            )
        ''')
        
        # Settings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_preference(self, user_id: str, preferences: Dict) -> bool:
        """Save user preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO user_preferences
                (user_id, preferences, updated_at)
                VALUES (?, ?, ?)
            ''', (user_id, json.dumps(preferences), datetime.now()))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
    
    def get_preference(self, user_id: str) -> Optional[Dict]:
        """Get user preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT preferences FROM user_preferences
                WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            return {}
        finally:
            conn.close()
    
    def save_conversation(self, user_id: str, role: str, content: str, 
                           metadata: Dict = None) -> str:
        """Save conversation message"""
        import uuid
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        msg_id = str(uuid.uuid4())[:8]
        
        try:
            cursor.execute('''
                INSERT INTO conversations
                (id, user_id, timestamp, role, content, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (msg_id, user_id, datetime.now(), role, content,
                  json.dumps(metadata or {})))
            
            conn.commit()
            return msg_id
        finally:
            conn.close()
    
    def get_conversations(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get conversation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, timestamp, role, content, metadata
                FROM conversations
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            
            rows = cursor.fetchall()
            return [{
                'id': r[0],
                'timestamp': r[1],
                'role': r[2],
                'content': r[3],
                'metadata': json.loads(r[4]) if r[4] else {}
            } for r in rows]
        finally:
            conn.close()
    
    def add_task(self, user_id: str, title: str, description: str = "",
                  due_date: str = None, priority: int = 1) -> str:
        """Add a task"""
        import uuid
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        task_id = str(uuid.uuid4())[:8]
        
        try:
            cursor.execute('''
                INSERT INTO tasks
                (id, user_id, title, description, due_date, priority,
                 status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (task_id, user_id, title, description, due_date,
                  priority, 'pending', datetime.now()))
            
            conn.commit()
            return task_id
        finally:
            conn.close()
    
    def get_tasks(self, user_id: str, status: str = None) -> List[Dict]:
        """Get user tasks"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            if status:
                cursor.execute('''
                    SELECT id, title, description, due_date, priority,
                           status, created_at, completed_at
                    FROM tasks
                    WHERE user_id = ? AND status = ?
                    ORDER BY due_date, priority DESC
                ''', (user_id, status))
            else:
                cursor.execute('''
                    SELECT id, title, description, due_date, priority,
                           status, created_at, completed_at
                    FROM tasks
                    WHERE user_id = ?
                    ORDER BY due_date, priority DESC
                ''', (user_id,))
            
            rows = cursor.fetchall()
            return [{
                'id': r[0],
                'title': r[1],
                'description': r[2],
                'due_date': r[3],
                'priority': r[4],
                'status': r[5],
                'created_at': r[6],
                'completed_at': r[7]
            } for r in rows]
        finally:
            conn.close()
    
    def complete_task(self, task_id: str) -> bool:
        """Mark task as complete"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE tasks
                SET status = ?, completed_at = ?
                WHERE id = ?
            ''', ('completed', datetime.now(), task_id))
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def save_note(self, user_id: str, title: str, content: str,
                   tags: List[str] = None) -> str:
        """Save a note"""
        import uuid
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        note_id = str(uuid.uuid4())[:8]
        now = datetime.now()
        
        try:
            cursor.execute('''
                INSERT INTO notes
                (id, user_id, title, content, tags, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (note_id, user_id, title, content,
                  json.dumps(tags or []), now, now))
            
            conn.commit()
            return note_id
        finally:
            conn.close()
    
    def get_notes(self, user_id: str, tag: str = None) -> List[Dict]:
        """Get user notes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, title, content, tags, created_at, updated_at
                FROM notes
                WHERE user_id = ?
                ORDER BY updated_at DESC
            ''', (user_id,))
            
            rows = cursor.fetchall()
            notes = []
            for r in rows:
                note = {
                    'id': r[0],
                    'title': r[1],
                    'content': r[2],
                    'tags': json.loads(r[3]) if r[3] else [],
                    'created_at': r[4],
                    'updated_at': r[5]
                }
                if not tag or tag in note['tags']:
                    notes.append(note)
            
            return notes
        finally:
            conn.close()
    
    def set_setting(self, key: str, value: Any) -> bool:
        """Save a setting"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO settings
                (key, value, updated_at)
                VALUES (?, ?, ?)
            ''', (key, json.dumps(value), datetime.now()))
            
            conn.commit()
            return True
        finally:
            conn.close()
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT value FROM settings
                WHERE key = ?
            ''', (key,))
            
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            return default
        finally:
            conn.close()