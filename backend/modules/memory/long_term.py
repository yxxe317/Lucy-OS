"""
Long-term memory system for Lucy AI
Stores conversations and knowledge persistently
"""

import sqlite3
import json
import hashlib
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import numpy as np

class LongTermMemory:
    """
    Persistent memory using SQLite
    Stores conversations, facts, and embeddings
    """
    
    def __init__(self, db_path="lucy_memory.db"):
        self.db_path = db_path
        self._init_db()
        self.cache = {}
        self.cache_size = 100
        
    def _init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                timestamp DATETIME,
                role TEXT,
                content TEXT,
                embedding BLOB,
                sentiment REAL,
                topics TEXT,
                importance REAL DEFAULT 1.0
            )
        ''')
        
        # Facts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facts (
                id TEXT PRIMARY KEY,
                fact TEXT,
                category TEXT,
                confidence REAL,
                source TEXT,
                timestamp DATETIME,
                embedding BLOB,
                last_accessed DATETIME,
                access_count INTEGER DEFAULT 0
            )
        ''')
        
        # Memory stats
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_stats (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated DATETIME
            )
        ''')
        
        # Indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_time ON conversations(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_facts_category ON facts(category)')
        
        conn.commit()
        conn.close()
    
    def store_conversation(self, user_id: str, role: str, content: str, 
                           sentiment: float = 0.0, topics: List[str] = None,
                           importance: float = 1.0) -> str:
        """
        Store a conversation entry
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Generate ID
        timestamp = datetime.now()
        conv_id = hashlib.md5(f"{user_id}{timestamp}{content[:50]}".encode()).hexdigest()[:16]
        
        # Create embedding (simplified - just store for now)
        embedding = self._create_embedding(content)
        
        cursor.execute('''
            INSERT INTO conversations 
            (id, user_id, timestamp, role, content, embedding, sentiment, topics, importance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            conv_id, user_id, timestamp, role, content, 
            sqlite3.Binary(pickle.dumps(embedding)),
            sentiment, json.dumps(topics or []), importance
        ))
        
        conn.commit()
        conn.close()
        
        # Update cache
        self.cache[conv_id] = {
            'id': conv_id, 'user_id': user_id, 'timestamp': timestamp,
            'role': role, 'content': content, 'sentiment': sentiment,
            'topics': topics, 'importance': importance
        }
        
        return conv_id
    
    def get_conversation_history(self, user_id: str, limit: int = 50, 
                                  offset: int = 0) -> List[Dict]:
        """
        Get conversation history for a user
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, role, content, sentiment, topics, importance
            FROM conversations
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        ''', (user_id, limit, offset))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row[0],
            'timestamp': row[1],
            'role': row[2],
            'content': row[3],
            'sentiment': row[4],
            'topics': json.loads(row[5]) if row[5] else [],
            'importance': row[6]
        } for row in rows]
    
    def search_memories(self, query: str, user_id: Optional[str] = None, 
                         limit: int = 10) -> List[Dict]:
        """
        Search memories by semantic similarity
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simple text search for now
        if user_id:
            cursor.execute('''
                SELECT id, timestamp, role, content, sentiment, importance
                FROM conversations
                WHERE user_id = ? AND content LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, f'%{query}%', limit))
        else:
            cursor.execute('''
                SELECT id, timestamp, role, content, sentiment, importance
                FROM conversations
                WHERE content LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (f'%{query}%', limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row[0], 'timestamp': row[1], 'role': row[2],
            'content': row[3], 'sentiment': row[4], 'importance': row[5]
        } for row in rows]
    
    def store_fact(self, fact: str, category: str = "general", 
                    confidence: float = 1.0, source: str = "user") -> str:
        """
        Store a fact in knowledge base
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        fact_id = hashlib.md5(fact.encode()).hexdigest()[:16]
        embedding = self._create_embedding(fact)
        
        cursor.execute('''
            INSERT OR REPLACE INTO facts 
            (id, fact, category, confidence, source, timestamp, embedding, 
             last_accessed, access_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            fact_id, fact, category, confidence, source, datetime.now(),
            sqlite3.Binary(pickle.dumps(embedding)),
            datetime.now(), 0
        ))
        
        conn.commit()
        conn.close()
        return fact_id
    
    def recall_fact(self, query: str, category: Optional[str] = None) -> Optional[str]:
        """
        Recall a fact by query
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute('''
                SELECT fact, confidence, access_count
                FROM facts
                WHERE category = ? AND fact LIKE ?
                ORDER BY confidence DESC, access_count DESC
                LIMIT 1
            ''', (category, f'%{query}%'))
        else:
            cursor.execute('''
                SELECT fact, confidence, access_count
                FROM facts
                WHERE fact LIKE ?
                ORDER BY confidence DESC, access_count DESC
                LIMIT 1
            ''', (f'%{query}%',))
        
        row = cursor.fetchone()
        if row:
            # Update access count
            cursor.execute('''
                UPDATE facts
                SET access_count = ?, last_accessed = ?
                WHERE fact = ?
            ''', (row[2] + 1, datetime.now(), row[0]))
            conn.commit()
            conn.close()
            return row[0]
        
        conn.close()
        return None
    
    def get_important_memories(self, user_id: str, days: int = 7, 
                                 min_importance: float = 0.7) -> List[Dict]:
        """
        Get important memories for memory consolidation
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = datetime.now() - timedelta(days=days)
        
        cursor.execute('''
            SELECT id, timestamp, role, content, importance
            FROM conversations
            WHERE user_id = ? AND timestamp > ? AND importance >= ?
            ORDER BY importance DESC, timestamp DESC
        ''', (user_id, cutoff, min_importance))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row[0], 'timestamp': row[1],
            'role': row[2], 'content': row[3],
            'importance': row[4]
        } for row in rows]
    
    def consolidate(self, force: bool = False):
        """
        Consolidate memory - move important items to long-term storage
        """
        # This would normally reorganize indexes, compress old data, etc.
        print("🔄 Consolidating long-term memory...")
        # Implementation here
    
    def _create_embedding(self, text: str) -> np.ndarray:
        """
        Create a simple embedding vector
        For production, use sentence-transformers
        """
        # Simple random embedding for now
        return np.random.randn(384).astype(np.float32)
    
    def forget_old(self, days: int = 365):
        """
        Forget memories older than specified days
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = datetime.now() - timedelta(days=days)
        
        cursor.execute('''
            DELETE FROM conversations
            WHERE timestamp < ? AND importance < 0.5
        ''', (cutoff,))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"🧹 Forgot {deleted} old, unimportant memories")
        return deleted
    
    def count(self) -> int:
        """Get total number of stored items"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM conversations')
        count = cursor.fetchone()[0]
        conn.close()
        return count