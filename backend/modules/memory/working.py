"""
Working memory - short-term, limited capacity (7±2 chunks)
"""

from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class WorkingMemory:
    """
    Working memory with limited capacity
    Implements the 7±2 chunks principle
    """
    
    def __init__(self, capacity: int = 7, ttl_seconds: int = 3600):
        self.capacity = capacity
        self.ttl = ttl_seconds
        self.items = OrderedDict()
        self.attention_focus = None
        
    def add(self, item: Dict[str, Any], item_id: Optional[str] = None):
        """
        Add an item to working memory
        """
        if item_id is None:
            item_id = f"item_{datetime.now().timestamp()}"
        
        # Add timestamp
        item['_timestamp'] = datetime.now()
        item['_id'] = item_id
        
        # Store item
        self.items[item_id] = item
        
        # Maintain capacity
        if len(self.items) > self.capacity:
            # Remove oldest (FIFO)
            self.items.popitem(last=False)
    
    def get(self, item_id: str) -> Optional[Dict]:
        """
        Retrieve an item
        """
        item = self.items.get(item_id)
        if item:
            # Update timestamp (recently used)
            item['_timestamp'] = datetime.now()
            # Move to end (mark as recently used)
            self.items.move_to_end(item_id)
        return item
    
    def search(self, query: str) -> List[Dict]:
        """
        Search working memory
        """
        results = []
        query_lower = query.lower()
        
        for item_id, item in self.items.items():
            # Simple text search
            if any(query_lower in str(v).lower() for v in item.values()):
                results.append(item)
        
        return results
    
    def focus_on(self, item_id: str):
        """
        Focus attention on a specific item
        """
        if item_id in self.items:
            self.attention_focus = item_id
            # Move to end (most recent)
            self.items.move_to_end(item_id)
    
    def clear_focus(self):
        """Clear attention focus"""
        self.attention_focus = None
    
    def prune_expired(self):
        """
        Remove expired items
        """
        now = datetime.now()
        expired = []
        
        for item_id, item in self.items.items():
            age = now - item['_timestamp']
            if age.total_seconds() > self.ttl:
                expired.append(item_id)
        
        for item_id in expired:
            del self.items[item_id]
        
        return len(expired)
    
    def get_all(self) -> List[Dict]:
        """Get all items"""
        return list(self.items.values())
    
    def clear(self):
        """Clear working memory"""
        self.items.clear()
        self.attention_focus = None
    
    def capacity_remaining(self) -> int:
        """Get remaining capacity"""
        return max(0, self.capacity - len(self.items))