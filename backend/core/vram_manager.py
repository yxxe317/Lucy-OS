# ============================================================================
# LUCY_OS 2.0 - VRAM MANAGER
# VRAM Auctioning System for Multi-Model Context Switching
# ============================================================================
import psutil
import os
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import threading
import time

logger = logging.getLogger("LucyVRAMManager")

@dataclass
class VRAMAllocation:
    model_name: str
    allocated_gb: float
    timestamp: str
    priority: int
    is_active: bool = True

@dataclass
class VRAMBid:
    model_name: str
    requested_gb: float
    priority: int
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class VRAMState:
    total_gb: float = 0.0
    used_gb: float = 0.0
    available_gb: float = 0.0
    allocations: List[VRAMAllocation] = field(default_factory=list)
    last_update: str = ""

class VRAMManager:
    """
    VRAM Auctioning System for Multi-Model Context Switching
    
    Manages GPU memory allocation across multiple LLM models using an auction-based
    allocation strategy. Supports dynamic reallocation based on priority and usage.
    """
    
    def __init__(self, total_vram_gb: float = 6.0):
        self._total_vram_gb = total_vram_gb
        self._state = VRAMState(total_gb=total_vram_gb)
        self._lock = threading.RLock()
        self._auction_history: List[Dict[str, Any]] = []
        self._config = {
            "auction_interval": 5,  # seconds
            "min_allocation_gb": 0.5,
            "max_allocation_gb": total_vram_gb,
            "priority_boost": 1.5,
            "eviction_threshold": 0.8,  # 80% usage triggers auction
            "models": {
                "llama-3-8b": {"base_gb": 4.0, "priority": 1},
                "llama-3-70b": {"base_gb": 14.0, "priority": 2},
                "mistral-7b": {"base_gb": 5.0, "priority": 1},
                "phi-3": {"base_gb": 3.0, "priority": 1}
            }
        }
        logger.info(f"[VRAMManager] Initialized with {total_vram_gb}GB VRAM")
    
    def get_state(self) -> VRAMState:
        """Get current VRAM state"""
        with self._lock:
            return self._state
    
    def get_available_vram(self) -> float:
        """Get available VRAM in GB"""
        with self._lock:
            return self._state.available_gb
    
    def get_used_vram(self) -> float:
        """Get used VRAM in GB"""
        with self._lock:
            return self._state.used_gb
    
    def allocate(self, model_name: str, requested_gb: float, priority: int = 1) -> Tuple[bool, str]:
        """
        Allocate VRAM for a model
        
        Args:
            model_name: Name of the model
            requested_gb: Amount of VRAM requested
            priority: Priority level (higher = more likely to win auction)
            
        Returns:
            Tuple of (success, message)
        """
        with self._lock:
            if requested_gb <= 0 or requested_gb > self._total_vram_gb:
                return False, f"Invalid allocation: {requested_gb}GB"
            
            if self._state.available_gb < requested_gb:
                # Not enough VRAM, trigger auction
                success, message = self._run_auction(model_name, requested_gb, priority)
                if not success:
                    return False, message
            
            # Allocate VRAM
            allocation = VRAMAllocation(
                model_name=model_name,
                allocated_gb=requested_gb,
                timestamp=datetime.now().isoformat(),
                priority=priority,
                is_active=True
            )
            self._state.allocations.append(allocation)
            self._state.used_gb = sum(a.allocated_gb for a in self._state.allocations)
            self._state.available_gb = self._total_vram_gb - self._state.used_gb
            self._state.last_update = datetime.now().isoformat()
            
            logger.info(f"[VRAMManager] Allocated {requested_gb}GB to {model_name}")
            return True, f"Allocated {requested_gb}GB to {model_name}"
    
    def deallocate(self, model_name: str) -> Tuple[bool, str]:
        """Deallocate VRAM for a model"""
        with self._lock:
            for i, alloc in enumerate(self._state.allocations):
                if alloc.model_name == model_name and alloc.is_active:
                    self._state.allocations[i].is_active = False
                    self._state.used_gb -= alloc.allocated_gb
                    self._state.available_gb += alloc.allocated_gb
                    self._state.last_update = datetime.now().isoformat()
                    
                    logger.info(f"[VRAMManager] Deallocated {alloc.allocated_gb}GB from {model_name}")
                    return True, f"Deallocated {alloc.allocated_gb}GB from {model_name}"
            
            return False, f"No active allocation found for {model_name}"
    
    def _run_auction(self, bidder: str, bid_amount: float, bidder_priority: int) -> Tuple[bool, str]:
        """
        Run VRAM auction
        
        Args:
            bidder: Name of the model bidding
            bid_amount: Amount being bid
            bidder_priority: Priority of the bidder
            
        Returns:
            Tuple of (success, message)
        """
        current_allocations = [a for a in self._state.allocations if a.is_active]
        current_usage = sum(a.allocated_gb for a in current_allocations)
        available = self._total_vram_gb - current_usage
        
        if available >= bid_amount:
            return True, f"Auction passed: {bidder} won {bid_amount}GB"
        
        # Calculate effective bid with priority boost
        effective_bid = bid_amount * self._config["priority_boost"] ** (bidder_priority - 1)
        
        # Check if bidder can win
        if effective_bid >= available:
            # Evict lower priority models
            evicted = self._evict_models(bid_amount, bidder_priority)
            if evicted:
                self._state.used_gb -= sum(e.allocated_gb for e in evicted)
                self._state.available_gb += sum(e.allocated_gb for e in evicted)
                
                # Record auction history
                self._auction_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "bidder": bidder,
                    "bid_amount": bid_amount,
                    "evicted_models": [e.model_name for e in evicted],
                    "new_allocation": bid_amount
                })
                
                logger.info(f"[VRAMManager] Auction: {bidder} won {bid_amount}GB, evicted {[e.model_name for e in evicted]}")
                return True, f"Auction passed: {bidder} won {bid_amount}GB"
        
        return False, f"Auction failed: insufficient VRAM for {bidder}"
    
    def _evict_models(self, needed_gb: float, new_priority: int) -> List[VRAMAllocation]:
        """Evict lower priority models to free up VRAM"""
        evicted = []
        current_allocations = [a for a in self._state.allocations if a.is_active]
        
        # Sort by priority (lowest first)
        sorted_allocs = sorted(current_allocations, key=lambda x: x.priority)
        
        freed = 0
        for alloc in sorted_allocs:
            if freed >= needed_gb:
                break
            
            # Only evict if new bidder has higher priority
            if alloc.priority < new_priority:
                evicted.append(alloc)
                freed += alloc.allocated_gb
        
        return evicted
    
    def run_periodic_auction(self):
        """Run periodic auction check"""
        while True:
            time.sleep(self._config["auction_interval"])
            state = self.get_state()
            usage_ratio = state.used_gb / self._total_vram_gb if self._total_vram_gb > 0 else 0
            
            if usage_ratio > self._config["eviction_threshold"]:
                logger.info(f"[VRAMManager] High VRAM usage detected ({usage_ratio:.2%}), running auction")
                # Trigger auction for highest priority model
                self._run_periodic_auction()
    
    def _run_periodic_auction(self):
        """Internal periodic auction"""
        current_allocations = [a for a in self._state.allocations if a.is_active]
        if not current_allocations:
            return
        
        # Find highest priority model
        highest_priority = max(a.priority for a in current_allocations)
        highest_models = [a for a in current_allocations if a.priority == highest_priority]
        
        if len(highest_models) == 1:
            # Single highest priority model, try to allocate more
            model = highest_models[0]
            needed = self._config["models"].get(model.model_name, {}).get("base_gb", model.allocated_gb)
            if model.allocated_gb < needed:
                success, msg = self.allocate(model.model_name, needed - model.allocated_gb, highest_priority)
                logger.info(f"[VRAMManager] Periodic auction: {msg}")
    
    def get_auction_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent auction history"""
        return self._auction_history[-limit:]
    
    def reset(self):
        """Reset VRAM state"""
        with self._lock:
            self._state.allocations = []
            self._state.used_gb = 0.0
            self._state.available_gb = self._total_vram_gb
            self._state.last_update = datetime.now().isoformat()
            logger.info("[VRAMManager] VRAM state reset")
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self._config.copy()
    
    def set_config(self, config: Dict[str, Any]):
        """Update configuration"""
        self._config.update(config)
        logger.info(f"[VRAMManager] Configuration updated: {config}")


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================
vram_manager = VRAMManager(total_vram_gb=6.0)