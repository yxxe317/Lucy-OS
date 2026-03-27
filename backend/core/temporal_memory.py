"""
Temporal Memory Module - Time-aware memory with decay and consolidation
"""
import asyncio
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import heapq

class TemporalMemory:
    def __init__(self):
        self.memory_path = Path("data/temporal_memory")
        self.memory_path.mkdir(exist_ok=True)
        self.memory_store: Dict[str, dict] = {}
        self.decay_rates = {
            "short_term": 0.95,
            "medium_term": 0.98,
            "long_term": 0.995
        }
        self.consolidation_threshold = 3600  # 1 hour
    
    def encode_memory(self, content: str, metadata: dict = None) -> str:
        """Encode content into temporal signature"""
        timestamp = datetime.now().isoformat()
        signature = hashlib.sha256(
            f"{content}{timestamp}{id(self)}".encode()
        ).hexdigest()[:16]
        return signature
    
    def store(self, key: str, content: str, importance: float = 1.0, 
              category: str = "general") -> dict:
        """Store memory with temporal metadata"""
        import hashlib
        
        signature = self.encode_memory(content)
        now = time.time()
        
        self.memory_store[key] = {
            "content": content,
            "signature": signature,
            "timestamp": now,
            "importance": importance,
            "category": category,
            "access_count": 0,
            "last_accessed": now,
            "consolidated": False
        }
        
        self._persist()
        return {"key": key, "signature": signature, "stored": True}
    
    def retrieve(self, query: str, max_results: int = 10) -> List[dict]:
        """Retrieve memories by semantic similarity"""
        import hashlib
        
        query_hash = hashlib.sha256(query.encode()).hexdigest()
        results = []
        
        for key, memory in self.memory_store.items():
            # Simulate similarity scoring
            similarity = 0.5 + (hash(query_hash + key) % 100) / 100
            if similarity > 0.5:
                results.append({
                    "key": key,
                    "content": memory["content"][:200] + "..." if len(memory["content"]) > 200 else memory["content"],
                    "similarity": round(similarity, 3),
                    "timestamp": datetime.fromtimestamp(memory["timestamp"]).isoformat()
                })
        
        return sorted(results, key=lambda x: x["similarity"], reverse=True)[:max_results]
    
    def decay(self) -> int:
        """Apply decay to all memories"""
        now = time.time()
        decayed = 0
        
        for key, memory in self.memory_store.items():
            age = now - memory["timestamp"]
            
            # Determine decay rate based on age
            if age < 3600:
                rate = self.decay_rates["short_term"]
            elif age < 86400:
                rate = self.decay_rates["medium_term"]
            else:
                rate = self.decay_rates["long_term"]
            
            # Update importance (decay)
            memory["importance"] = max(0.1, memory["importance"] * rate)
            memory["last_accessed"] = now
            
            if memory["importance"] < 0.1:
                del self.memory_store[key]
                decayed += 1
        
        self._persist()
        return decayed
    
    def consolidate(self) -> dict:
        """Consolidate frequently accessed memories"""
        consolidated = []
        
        for key, memory in self.memory_store.items():
            if memory["access_count"] > 5 and not memory["consolidated"]:
                memory["consolidated"] = True
                memory["importance"] = min(1.0, memory["importance"] + 0.2)
                consolidated.append(key)
        
        self._persist()
        return {"consolidated": len(consolidated), "keys": consolidated[:10]}
    
    def _persist(self):
        """Persist memory to disk"""
        data = {
            "memories": self.memory_store,
            "last_decay": datetime.now().isoformat()
        }
        
        with open(self.memory_path / "store.json", 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self):
        """Load persisted memory"""
        store_file = self.memory_path / "store.json"
        if store_file.exists():
            with open(store_file, 'r') as f:
                data = json.load(f)
                self.memory_store = data.get("memories", {})
    
    def clear(self):
        """Clear all memories"""
        self.memory_store.clear()
        self._persist()

# Global instance
temporal_memory = TemporalMemory()