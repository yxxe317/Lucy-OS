"""
Semantic memory - stores facts and general knowledge
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
import numpy as np

class SemanticMemory:
    """
    Stores facts and general knowledge with embeddings
    """
    
    def __init__(self, db_path="lucy_semantic.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
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
                related_facts TEXT,
                access_count INTEGER DEFAULT 0,
                last_accessed DATETIME
            )
        ''')
        
        # Categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                name TEXT PRIMARY KEY,
                description TEXT,
                parent TEXT,
                fact_count INTEGER DEFAULT 0
            )
        ''')
        
        # Relationships table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relationships (
                fact_id1 TEXT,
                fact_id2 TEXT,
                relation TEXT,
                strength REAL,
                PRIMARY KEY (fact_id1, fact_id2, relation)
            )
        ''')
        
        # Indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_facts_category ON facts(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_facts_confidence ON facts(confidence)')
        
        conn.commit()
        conn.close()
    
    def store(self, fact: str, category: str = "general", 
               confidence: float = 1.0, source: str = "user",
               related: List[str] = None) -> str:
        """
        Store a fact in semantic memory
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        fact_id = hashlib.md5(fact.encode()).hexdigest()[:16]
        embedding = self._create_embedding(fact)
        
        cursor.execute('''
            INSERT OR REPLACE INTO facts
            (id, fact, category, confidence, source, timestamp, embedding,
             related_facts, access_count, last_accessed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            fact_id, fact, category, confidence, source, datetime.now(),
            sqlite3.Binary(embedding.tobytes()),
            json.dumps(related or []), 0, datetime.now()
        ))
        
        # Update category count
        cursor.execute('''
            INSERT OR IGNORE INTO categories (name, fact_count)
            VALUES (?, 0)
        ''', (category,))
        
        cursor.execute('''
            UPDATE categories
            SET fact_count = fact_count + 1
            WHERE name = ?
        ''', (category,))
        
        conn.commit()
        conn.close()
        
        return fact_id
    
    def recall(self, query: str, category: Optional[str] = None,
                threshold: float = 0.5) -> List[Dict]:
        """
        Recall facts matching query
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simple text search for now
        if category:
            cursor.execute('''
                SELECT id, fact, category, confidence, source, timestamp,
                       access_count, related_facts
                FROM facts
                WHERE category = ? AND fact LIKE ?
                ORDER BY confidence DESC, access_count DESC
                LIMIT 10
            ''', (category, f'%{query}%'))
        else:
            cursor.execute('''
                SELECT id, fact, category, confidence, source, timestamp,
                       access_count, related_facts
                FROM facts
                WHERE fact LIKE ?
                ORDER BY confidence DESC, access_count DESC
                LIMIT 10
            ''', (f'%{query}%',))
        
        rows = cursor.fetchall()
        
        # Update access counts
        for row in rows:
            cursor.execute('''
                UPDATE facts
                SET access_count = ?, last_accessed = ?
                WHERE id = ?
            ''', (row[6] + 1, datetime.now(), row[0]))
        
        conn.commit()
        conn.close()
        
        return [{
            'id': row[0],
            'fact': row[1],
            'category': row[2],
            'confidence': row[3],
            'source': row[4],
            'timestamp': row[5],
            'access_count': row[6],
            'related': json.loads(row[7]) if row[7] else []
        } for row in rows]
    
    def get_category_facts(self, category: str, limit: int = 50) -> List[Dict]:
        """
        Get all facts in a category
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, fact, confidence, source, timestamp, access_count
            FROM facts
            WHERE category = ?
            ORDER BY confidence DESC, access_count DESC
            LIMIT ?
        ''', (category, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row[0], 'fact': row[1], 'confidence': row[2],
            'source': row[3], 'timestamp': row[4], 'access_count': row[5]
        } for row in rows]
    
    def add_relationship(self, fact_id1: str, fact_id2: str, 
                          relation: str, strength: float = 1.0):
        """
        Add relationship between facts
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO relationships
            (fact_id1, fact_id2, relation, strength)
            VALUES (?, ?, ?, ?)
        ''', (fact_id1, fact_id2, relation, strength))
        
        conn.commit()
        conn.close()
    
    def get_related(self, fact_id: str, relation: Optional[str] = None) -> List[Dict]:
        """
        Get facts related to given fact
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if relation:
            cursor.execute('''
                SELECT f.id, f.fact, f.category, f.confidence, r.relation, r.strength
                FROM facts f
                JOIN relationships r ON f.id = r.fact_id2
                WHERE r.fact_id1 = ? AND r.relation = ?
                ORDER BY r.strength DESC
            ''', (fact_id, relation))
        else:
            cursor.execute('''
                SELECT f.id, f.fact, f.category, f.confidence, r.relation, r.strength
                FROM facts f
                JOIN relationships r ON f.id = r.fact_id2
                WHERE r.fact_id1 = ?
                ORDER BY r.strength DESC
            ''', (fact_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row[0], 'fact': row[1], 'category': row[2],
            'confidence': row[3], 'relation': row[4], 'strength': row[5]
        } for row in rows]
    
    def count(self) -> int:
        """Get total number of facts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM facts')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def _create_embedding(self, text: str) -> np.ndarray:
        """
        Create embedding vector
        """
        # Simple random embedding for now
        return np.random.randn(384).astype(np.float32)