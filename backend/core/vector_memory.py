import logging
from pathlib import Path
from datetime import datetime
import hashlib
import json
import sqlite3
from typing import List, Dict
import numpy as np

logger = logging.getLogger("LucyVectorMemory")

class VectorMemorySystem:
    def __init__(self):
        # Create persistent storage directory
        self.persist_dir = Path(__file__).parent.parent / "vector_db"
        self.persist_dir.mkdir(exist_ok=True)
        
        # SQLite database for storing embeddings
        self.db_path = self.persist_dir / "memories.db"
        self._init_db()
        
        logger.info(f"💾 Vector Memory Initialized at {self.persist_dir}")

    def _init_db(self):
        """Initialize SQLite database for memories"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT,
                embedding TEXT,
                timestamp TEXT,
                query_preview TEXT,
                response_preview TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("📊 Memory database initialized")

    def _generate_id(self, text: str) -> str:
        """Generate unique ID from text"""
        return hashlib.md5(text.encode()).hexdigest()

    def _simple_embedding(self, text: str) -> np.ndarray:
        """Create simple embedding (word frequency based)"""
        # Simple bag-of-words embedding for demo
        # In production, use sentence-transformers
        words = text.lower().split()
        embedding = np.zeros(100)
        
        for i, word in enumerate(words[:100]):
            # Hash word to position
            pos = hash(word) % 100
            embedding[pos] += 1
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)

    async def add_memory(self, query: str, response: str, metadata: dict = None):
        """Add conversation to vector memory"""
        try:
            # Combine query and response for full context
            content = f"User: {query}\nLucy: {response}"
            
            # Generate embedding
            embedding = self._simple_embedding(content)
            
            # Generate unique ID
            mem_id = self._generate_id(content)
            
            # Connect to database
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Insert or replace
            cursor.execute('''
                INSERT OR REPLACE INTO memories 
                (id, content, embedding, timestamp, query_preview, response_preview)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                mem_id,
                content,
                json.dumps(embedding.tolist()),
                datetime.now().isoformat(),
                query[:100],
                response[:100]
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"💾 Memory added: {query[:50]}...")
            
        except Exception as e:
            logger.error(f"Add memory error: {e}")

    async def search_memories(self, query: str, limit: int = 5) -> list:
        """Search for relevant memories"""
        try:
            # Generate query embedding
            query_embedding = self._simple_embedding(query)
            
            # Connect to database
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Get all memories
            cursor.execute('SELECT id, content, embedding, timestamp FROM memories')
            rows = cursor.fetchall()
            conn.close()
            
            # Calculate similarity for each memory
            memories_with_score = []
            for row in rows:
                mem_id, content, embedding_json, timestamp = row
                embedding = np.array(json.loads(embedding_json))
                
                similarity = self._cosine_similarity(query_embedding, embedding)
                
                memories_with_score.append({
                    "id": mem_id,
                    "content": content,
                    "timestamp": timestamp,
                    "similarity": similarity,
                    "metadata": {"timestamp": timestamp}
                })
            
            # Sort by similarity (highest first)
            memories_with_score.sort(key=lambda x: x["similarity"], reverse=True)
            
            # Return top results
            results = memories_with_score[:limit]
            
            logger.info(f"🔍 Found {len(results)} relevant memories")
            return results
            
        except Exception as e:
            logger.error(f"Search memory error: {e}")
            return []

    async def get_all_memories(self, limit: int = 50) -> list:
        """Get recent memories"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT id, content, timestamp FROM memories ORDER BY timestamp DESC LIMIT ?',
                (limit,)
            )
            rows = cursor.fetchall()
            conn.close()
            
            memories = []
            for row in rows:
                memories.append({
                    "id": row[0],
                    "content": row[1],
                    "metadata": {"timestamp": row[2]}
                })
            
            return memories
            
        except Exception as e:
            logger.error(f"Get memories error: {e}")
            return []

    async def delete_memory(self, memory_id: str) -> bool:
        """Delete specific memory"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute('DELETE FROM memories WHERE id = ?', (memory_id,))
            conn.commit()
            deleted = cursor.rowcount > 0
            conn.close()
            
            if deleted:
                logger.info(f"🗑️ Memory deleted: {memory_id}")
            return deleted
            
        except Exception as e:
            logger.error(f"Delete memory error: {e}")
            return False

    def get_stats(self) -> dict:
        """Get memory statistics"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM memories')
            count = cursor.fetchone()[0]
            conn.close()
            
            return {
                "total_memories": count,
                "persist_dir": str(self.persist_dir)
            }
        except:
            return {
                "total_memories": 0,
                "persist_dir": str(self.persist_dir)
            }

# Global Instance
vector_memory = VectorMemorySystem()