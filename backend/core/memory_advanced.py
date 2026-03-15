# backend/core/memory_advanced.py
"""
Advanced Memory System for Lucy OS
Features 11-20: Memory compression, emotion-linked storage, contradiction detection
"""
import json
import sqlite3
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import hashlib
import logging

logger = logging.getLogger("AdvancedMemory")

class AdvancedMemory:
    """
    Next-gen memory system with:
    11. Memory compression AI
    12. Emotion-linked memory storage
    13. Memory contradiction detector
    14. Memory influence slider
    15. Forgotten idea recovery
    16. Parallel memory layers
    17. Memory lineage graph
    18. Memory trust score
    19. Predictive memory retrieval
    20. Memory rollback system
    """
    
    def __init__(self, db_path: str = "data/advanced_memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_db()
        self.influence_factor = 1.0  # Memory influence slider
        self.compression_ratio = 0.3  # Compress to 30% of original
        
    def _init_db(self):
        """Initialize advanced memory database"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Main memories table with emotion and metadata
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_hash TEXT UNIQUE,
                content TEXT,
                compressed_content TEXT,
                emotion TEXT,
                emotion_intensity REAL,
                layer TEXT,
                trust_score REAL,
                created_at DATETIME,
                last_accessed DATETIME,
                access_count INTEGER,
                importance REAL,
                lineage TEXT,
                version INTEGER
            )
        ''')
        
        # Memory relationships (lineage)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_lineage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id INTEGER,
                parent_id INTEGER,
                relationship TEXT,
                confidence REAL,
                FOREIGN KEY(memory_id) REFERENCES memories(id),
                FOREIGN KEY(parent_id) REFERENCES memories(id)
            )
        ''')
        
        # Memory contradictions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contradictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_a_id INTEGER,
                memory_b_id INTEGER,
                contradiction_type TEXT,
                resolved BOOLEAN,
                detected_at DATETIME,
                FOREIGN KEY(memory_a_id) REFERENCES memories(id),
                FOREIGN KEY(memory_b_id) REFERENCES memories(id)
            )
        ''')
        
        # Memory snapshots (for rollback)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id TEXT,
                created_at DATETIME,
                description TEXT,
                data TEXT
            )
        ''')
        
        # Predictive patterns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictive_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trigger_context TEXT,
                predicted_memory_ids TEXT,
                success_rate REAL,
                times_used INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Advanced memory system initialized")
    
    async def store_memory(self,
                          content: str,
                          emotion: str = "neutral",
                          emotion_intensity: float = 0.5,
                          layer: str = "default",
                          importance: float = 0.5,
                          parent_id: Optional[int] = None) -> Dict:
        """
        Feature 12: Store memory with emotional context
        """
        memory_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Compress memory (Feature 11)
        compressed = await self._compress_memory(content)
        
        # Calculate initial trust score
        trust_score = await self._calculate_trust_score(content, emotion, importance)
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Check if exists
        cursor.execute('SELECT id, version FROM memories WHERE memory_hash = ?', (memory_hash,))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing
            mem_id, version = existing
            cursor.execute('''
                UPDATE memories
                SET access_count = access_count + 1,
                    last_accessed = ?,
                    trust_score = (trust_score + ?) / 2
                WHERE id = ?
            ''', (datetime.now().isoformat(), trust_score, mem_id))
        else:
            # Insert new
            cursor.execute('''
                INSERT INTO memories
                (memory_hash, content, compressed_content, emotion, emotion_intensity,
                 layer, trust_score, created_at, last_accessed, access_count, importance, version)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                memory_hash, content, compressed, emotion, emotion_intensity,
                layer, trust_score, datetime.now().isoformat(), datetime.now().isoformat(),
                1, importance, 1
            ))
            mem_id = cursor.lastrowid
            
            # Add lineage
            if parent_id:
                cursor.execute('''
                    INSERT INTO memory_lineage (memory_id, parent_id, relationship, confidence)
                    VALUES (?, ?, ?, ?)
                ''', (mem_id, parent_id, "derived_from", 0.9))
        
        conn.commit()
        
        # Check for contradictions
        asyncio.create_task(self._detect_contradictions(mem_id, content))
        
        # Update predictive patterns
        asyncio.create_task(self._update_predictive_patterns())
        
        conn.close()
        
        return {
            "memory_id": mem_id,
            "hash": memory_hash,
            "compressed_size": len(compressed) / len(content) if content else 0,
            "trust_score": trust_score
        }
    
    async def _compress_memory(self, content: str) -> str:
        """
        Feature 11: Compress memory to core knowledge
        """
        if not content or len(content) < 100:
            return content
            
        # Simple compression - in production, use an actual LLM
        # Extract key sentences
        sentences = content.split('. ')
        target_length = max(1, int(len(sentences) * self.compression_ratio))
        
        # Keep first few and last few sentences (often most important)
        if len(sentences) > target_length * 2:
            compressed = sentences[:target_length//2] + ["..."] + sentences[-target_length//2:]
        else:
            compressed = sentences
            
        return '. '.join(compressed)
    
    async def _calculate_trust_score(self, content: str, emotion: str, importance: float) -> float:
        """
        Feature 18: Calculate trust score for memory
        """
        score = 0.7  # Base
        
        # Emotional intensity affects trust
        if emotion in ["strong", "excited", "confident"]:
            score += 0.1
        elif emotion in ["uncertain", "confused"]:
            score -= 0.1
            
        # Importance factor
        score += (importance - 0.5) * 0.2
        
        return max(0.1, min(1.0, score))
    
    async def retrieve_memory(self,
                             context: str,
                             layer: str = "default",
                             min_trust: float = 0.3,
                             limit: int = 10) -> List[Dict]:
        """
        Feature 19: Predictive memory retrieval based on context
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Get predictive suggestion first
        predicted = await self._get_predicted_memories(context)
        
        if predicted:
            # Load predicted memories
            placeholders = ','.join(['?'] * len(predicted))
            cursor.execute(f'''
                SELECT id, content, emotion, trust_score, importance, created_at
                FROM memories
                WHERE id IN ({placeholders})
                ORDER BY trust_score DESC, importance DESC
            ''', predicted)
        else:
            # Fallback to keyword search
            keywords = context.lower().split()[:5]
            like_clauses = ' OR '.join(['content LIKE ?'] * len(keywords))
            params = [f'%{k}%' for k in keywords]
            
            cursor.execute(f'''
                SELECT id, content, emotion, trust_score, importance, created_at
                FROM memories
                WHERE ({like_clauses}) AND layer = ? AND trust_score >= ?
                ORDER BY trust_score * importance DESC
                LIMIT ?
            ''', params + [layer, min_trust, limit])
        
        rows = cursor.fetchall()
        conn.close()
        
        # Apply influence slider (Feature 14)
        memories = []
        for row in rows:
            mem = {
                "id": row[0],
                "content": row[1],
                "emotion": row[2],
                "trust_score": row[3],
                "importance": row[4],
                "created_at": row[5]
            }
            # Adjust importance by influence factor
            mem["adjusted_importance"] = mem["importance"] * self.influence_factor
            memories.append(mem)
        
        return memories
    
    async def _get_predicted_memories(self, context: str) -> List[int]:
        """
        Feature 19: Predict which memories will be needed
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Find matching predictive patterns
        cursor.execute('''
            SELECT predicted_memory_ids, success_rate
            FROM predictive_patterns
            WHERE ? LIKE '%' || trigger_context || '%'
            ORDER BY success_rate DESC
            LIMIT 1
        ''', (context,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return json.loads(result[0])
        return []
    
    async def _detect_contradictions(self, memory_id: int, content: str):
        """
        Feature 13: Detect contradictions in memory
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Get recent similar memories
        cursor.execute('''
            SELECT id, content FROM memories
            WHERE id != ? AND content LIKE ?
            ORDER BY created_at DESC
            LIMIT 5
        ''', (memory_id, f'%{content[:50]}%'))
        
        similar = cursor.fetchall()
        
        for sim_id, sim_content in similar:
            # Simple contradiction check
            # In production, use semantic similarity + contradiction detection
            contradiction_score = await self._check_contradiction(content, sim_content)
            
            if contradiction_score > 0.8:
                cursor.execute('''
                    INSERT INTO contradictions
                    (memory_a_id, memory_b_id, contradiction_type, detected_at, resolved)
                    VALUES (?, ?, ?, ?, ?)
                ''', (memory_id, sim_id, "semantic", datetime.now().isoformat(), False))
                
                logger.info(f"⚠️ Detected contradiction between memories {memory_id} and {sim_id}")
        
        conn.commit()
        conn.close()
    
    async def _check_contradiction(self, mem1: str, mem2: str) -> float:
        """Check if two memories contradict each other"""
        # Simple check - in production, use NLP
        if "not" in mem1.lower() and "not" not in mem2.lower():
            # Possible contradiction
            return 0.7
        return 0.0
    
    async def get_contradictions(self, resolved: bool = False) -> List[Dict]:
        """Get all contradictions"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.id, m1.content, m2.content, c.contradiction_type, c.detected_at
            FROM contradictions c
            JOIN memories m1 ON c.memory_a_id = m1.id
            JOIN memories m2 ON c.memory_b_id = m2.id
            WHERE c.resolved = ?
        ''', (resolved,))
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": r[0],
                "memory_a": r[1][:100] + "...",
                "memory_b": r[2][:100] + "...",
                "type": r[3],
                "detected": r[4]
            }
            for r in rows
        ]
    
    async def set_influence_factor(self, factor: float):
        """
        Feature 14: Control how strongly memory affects answers
        """
        self.influence_factor = max(0.0, min(2.0, factor))
        logger.info(f"🎚️ Memory influence set to {self.influence_factor}")
        return {"influence_factor": self.influence_factor}
    
    async def recover_forgotten_idea(self, context: str, days_old: int = 30) -> Optional[Dict]:
        """
        Feature 15: Resurface old ideas when context matches
        """
        cutoff = (datetime.now() - timedelta(days=days_old)).isoformat()
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, content, emotion, importance, created_at
            FROM memories
            WHERE created_at < ? AND access_count < 3
            ORDER BY importance DESC
            LIMIT 20
        ''', (cutoff,))
        
        old_memories = cursor.fetchall()
        conn.close()
        
        # Find best match to current context
        best_match = None
        best_score = 0
        
        for mem in old_memories:
            # Simple keyword matching
            score = sum(1 for word in context.lower().split() 
                       if word in mem[1].lower())
            if score > best_score:
                best_score = score
                best_match = {
                    "id": mem[0],
                    "content": mem[1],
                    "emotion": mem[2],
                    "importance": mem[3],
                    "created_at": mem[4]
                }
        
        if best_match and best_score > 0:
            logger.info(f"💡 Recovered forgotten idea: {best_match['content'][:50]}...")
            return best_match
        return None
    
    async def create_snapshot(self, description: str = "") -> str:
        """
        Feature 20: Create memory snapshot for rollback
        """
        snapshot_id = hashlib.md5(f"snapshot_{datetime.now()}".encode()).hexdigest()[:8]
        
        # Export all memories
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM memories')
        memories = cursor.fetchall()
        
        # Get column names
        cursor.execute('PRAGMA table_info(memories)')
        columns = [col[1] for col in cursor.fetchall()]
        
        # Convert to dict list
        memory_data = []
        for row in memories:
            memory_data.append(dict(zip(columns, row)))
        
        # Store snapshot
        cursor.execute('''
            INSERT INTO memory_snapshots
            (snapshot_id, created_at, description, data)
            VALUES (?, ?, ?, ?)
        ''', (snapshot_id, datetime.now().isoformat(), description, json.dumps(memory_data)))
        
        conn.commit()
        conn.close()
        
        logger.info(f"📸 Created memory snapshot: {snapshot_id}")
        return snapshot_id
    
    async def rollback_to_snapshot(self, snapshot_id: str):
        """
        Feature 20: Rollback memory to previous state
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Get snapshot
        cursor.execute('''
            SELECT data FROM memory_snapshots
            WHERE snapshot_id = ?
        ''', (snapshot_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return {"error": "Snapshot not found"}
        
        snapshot_data = json.loads(result[0])
        
        # Clear current memories
        cursor.execute('DELETE FROM memories')
        
        # Restore from snapshot
        for mem in snapshot_data:
            placeholders = ','.join(['?'] * len(mem))
            cursor.execute(f'''
                INSERT INTO memories ({','.join(mem.keys())})
                VALUES ({placeholders})
            ''', list(mem.values()))
        
        conn.commit()
        conn.close()
        
        logger.info(f"⏪ Rolled back to snapshot {snapshot_id}")
        return {"success": True, "snapshot": snapshot_id}
    
    async def get_lineage(self, memory_id: int) -> Dict:
        """
        Feature 17: Get memory lineage graph
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Get memory
        cursor.execute('SELECT content, created_at FROM memories WHERE id = ?', (memory_id,))
        memory = cursor.fetchone()
        
        # Get ancestors
        cursor.execute('''
            SELECT parent_id, relationship FROM memory_lineage
            WHERE memory_id = ?
            ORDER BY confidence DESC
        ''', (memory_id,))
        ancestors = cursor.fetchall()
        
        # Get descendants
        cursor.execute('''
            SELECT memory_id, relationship FROM memory_lineage
            WHERE parent_id = ?
            ORDER BY confidence DESC
        ''', (memory_id,))
        descendants = cursor.fetchall()
        
        conn.close()
        
        return {
            "memory": {
                "id": memory_id,
                "content": memory[0][:100] + "..." if memory else "Unknown",
                "created": memory[1] if memory else None
            },
            "ancestors": [
                {"id": a[0], "relationship": a[1]}
                for a in ancestors
            ],
            "descendants": [
                {"id": d[0], "relationship": d[1]}
                for d in descendants
            ]
        }
    
    async def _update_predictive_patterns(self):
        """Update predictive patterns based on memory access"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Find sequences of memory accesses
        cursor.execute('''
            SELECT id, last_accessed FROM memories
            WHERE last_accessed > datetime('now', '-1 day')
            ORDER BY last_accessed
        ''')
        recent = cursor.fetchall()
        
        if len(recent) > 10:
            # Simple pattern: if A then B
            for i in range(len(recent) - 1):
                trigger = recent[i][0]
                predicted = recent[i+1][0]
                
                cursor.execute('''
                    INSERT OR REPLACE INTO predictive_patterns
                    (trigger_context, predicted_memory_ids, success_rate, times_used)
                    VALUES (?, ?, ?, ?)
                ''', (
                    f"memory_{trigger}",
                    json.dumps([predicted]),
                    0.7,
                    1
                ))
        
        conn.commit()
        conn.close()

# Global instance
advanced_memory = AdvancedMemory()