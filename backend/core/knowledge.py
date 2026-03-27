import logging
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger("KnowledgeBase")

class KnowledgeBase:
    """
    Knowledge base for storing, retrieving, and updating information
    Supports facts, memories, and semantic search
    """
    
    def __init__(self, db_path: str = "backend/data/knowledge.json"):
        self.db_path = Path(db_path)
        self.knowledge: Dict[str, Dict[str, Any]] = {}
        self._load()
    
    def _load(self):
        """Load knowledge from storage"""
        try:
            if self.db_path.exists():
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.knowledge = data.get("knowledge", {})
                    logger.info(f"✅ Loaded {len(self.knowledge)} knowledge entries")
        except Exception as e:
            logger.warning(f"⚠️ Could not load knowledge: {e}")
            self.knowledge = {}
    
    def _save(self):
        """Save knowledge to storage"""
        try:
            data = {"knowledge": self.knowledge, "version": "1.0"}
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("💾 Knowledge saved")
        except Exception as e:
            logger.error(f"❌ Save failed: {e}")
    
    def add_fact(self, subject: str, predicate: str, object_: Any, 
                  confidence: float = 0.9, source: str = "user") -> bool:
        """
        Add a fact to knowledge base
        Example: {"subject": "user", "predicate": "name", "object": "John"}
        """
        key = f"{subject}:{predicate}:{object_}"
        
        if key in self.knowledge:
            # Update existing
            self.knowledge[key]["object"] = object_
            self.knowledge[key]["timestamp"] = datetime.now().isoformat()
            return True
        
        self.knowledge[key] = {
            "subject": subject,
            "predicate": predicate,
            "object": object_,
            "confidence": confidence,
            "source": source,
            "timestamp": datetime.now().isoformat()
        }
        
        self._save()
        logger.info(f"➕ Added fact: {subject} {predicate} {object_}")
        return True
    
    def update_fact(self, subject: str, predicate: str, object_: Any) -> bool:
        """Update an existing fact"""
        key = f"{subject}:{predicate}:{object_}"
        if key in self.knowledge:
            self.knowledge[key]["object"] = object_
            self.knowledge[key]["timestamp"] = datetime.now().isoformat()
            self._save()
            return True
        return False
    
    def delete_fact(self, subject: str, predicate: str, object_: Any) -> bool:
        """Delete a fact"""
        key = f"{subject}:{predicate}:{object_}"
        if key in self.knowledge:
            del self.knowledge[key]
            self._save()
            return True
        return False
    
    def query(self, subject: Optional[str] = None, 
              predicate: Optional[str] = None,
              object_: Optional[Any] = None) -> List[Dict[str, Any]]:
        """
        Query knowledge base with optional filters
        """
        results = []
        for key, fact in self.knowledge.items():
            if subject and fact.get("subject") != subject:
                continue
            if predicate and fact.get("predicate") != predicate:
                continue
            if object_ is not None and fact.get("object") != object_:
                continue
            results.append(fact)
        return results
    
    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Semantic search using keyword matching and relevance scoring
        """
        query_terms = query.lower().split()
        scored = []
        
        for key, fact in self.knowledge.items():
            fact_text = f"{fact.get('subject', '')} {fact.get('predicate', '')} {fact.get('object', '')}".lower()
            match_count = sum(1 for term in query_terms if term in fact_text)
            if match_count > 0:
                relevance = match_count / len(query_terms)
                confidence = fact.get("confidence", 0.5)
                score = relevance * confidence * 100
                scored.append((score, fact))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [fact for _, fact in scored[:top_k]]
    
    def get_all_subjects(self) -> List[str]:
        """Get all unique subjects"""
        subjects = set()
        for fact in self.knowledge.values():
            subjects.add(fact.get("subject", ""))
        return list(subjects)
    
    def get_all_predicates(self) -> List[str]:
        """Get all unique predicates"""
        predicates = set()
        for fact in self.knowledge.values():
            predicates.add(fact.get("predicate", ""))
        return list(predicates)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        return {
            "total_facts": len(self.knowledge),
            "subjects": len(self.get_all_subjects()),
            "predicates": len(self.get_all_predicates()),
            "recent": sorted(
                self.knowledge.values(),
                key=lambda x: x.get("timestamp", ""),
                reverse=True
            )[:10]
        }
    
    def clear(self):
        """Clear all knowledge"""
        self.knowledge = {}
        self._save()
        logger.info("🗑️ Knowledge cleared")

# ═══════════════════════════════════════════════════════════════
# MEMORY SYSTEM FOR CONVERSATIONS
# ═══════════════════════════════════════════════════════════════
class ConversationMemory:
    """
    Short-term memory for conversation context
    """
    
    def __init__(self, max_context: int = 10):
        self.max_context = max_context
        self.context: List[Dict[str, Any]] = []
        self.user_preferences: Dict[str, Any] = {}
    
    def add_turn(self, user: str, assistant: str):
        """Add a conversation turn"""
        turn = {
            "user": user,
            "assistant": assistant,
            "timestamp": datetime.now().isoformat()
        }
        self.context.append(turn)
        
        # Trim if exceeding max
        if len(self.context) > self.max_context:
            self.context = self.context[-self.max_context:]
    
    def get_context(self, n: int = 5) -> List[str]:
        """Get recent conversation context as strings"""
        return [
            f"User: {t['user']}\nAssistant: {t['assistant']}"
            for t in self.context[-n:]
        ]
    
    def set_preference(self, key: str, value: Any):
        """Set a user preference"""
        self.user_preferences[key] = value
        logger.info(f"💡 Preference set: {key} = {value}")
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a user preference"""
        return self.user_preferences.get(key, default)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all preferences"""
        return self.user_preferences.copy()

# ═══════════════════════════════════════════════════════════════
# INITIALIZATION
# ═══════════════════════════════════════════════════════════════
knowledge_base = KnowledgeBase()
conversation_memory = ConversationMemory()