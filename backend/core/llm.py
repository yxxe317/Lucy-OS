"""
LUCY_OS 2.0 - Dual-LLM Switchboard Architecture
HooRii Protocol v2.0 | RTX 4070 Vision Core | OmniCoder-9B Reasoning Core
"""

import httpx
import logging
import asyncio
import json
import base64
from typing import Optional, Dict, AsyncGenerator, List, Any, Tuple
from datetime import datetime
from enum import Enum
from core.evolution import evolution

logger = logging.getLogger("LLMSwitchboard")

# ============================================================================
# LLM TARGET ENUMS
# ============================================================================
class LLMTarget(Enum):
    """LLM Target routing for different task types"""
    VISION_GEMMA = "gemma-3-4b"          # Port 1234 - Vision & Perception
    REASONING_OMNICODER = "omnicoder-9b" # Port 8012 - Logic & Coding
    DEFAULT_LMSTUDIO = "local-model"     # Port 1234 - Fallback


# ============================================================================
# CONFIGURATION
# ============================================================================
class LLMConfig:
    """Dual-LLM Configuration"""
    
    # Vision Core (Gemma-3-4B) - Port 1234
    VISION_URL = "http://127.0.0.1:1234/v1"
    VISION_CONTEXT_WINDOW = 32768  # 32k tokens
    VISION_MAX_TOKENS = 4096
    VISION_TEMPERATURE = 0.3
    VISION_TOP_P = 0.9
    
    # Reasoning Core (OmniCoder-9B) - Port 8012
    REASONING_URL = "http://127.0.0.1:8012/v1"
    REASONING_CONTEXT_WINDOW = 131072  # 128k tokens
    REASONING_MAX_TOKENS = 8192
    REASONING_TEMPERATURE = 0.2
    REASONING_TOP_P = 0.95
    
    # Fallback (LM Studio) - Port 1234
    FALLBACK_URL = "http://127.0.0.1:1234/v1"
    FALLBACK_MODEL = "local-model"
    FALLBACK_MAX_TOKENS = 4096
    FALLBACK_TEMPERATURE = 0.7


# ============================================================================
# LLM ROUTING DECISION ENGINE
# ============================================================================
class RoutingDecision:
    """Represents a routing decision for an LLM call"""
    
    def __init__(self, target: LLMTarget, priority: int = 0):
        self.target = target
        self.priority = priority
        self.reason: str = ""
        self.fallback: bool = False
    
    def __repr__(self):
        return f"RoutingDecision(target={self.target.value}, priority={self.priority})"


class RoutingEngine:
    """
    Smart Switchboard Pattern for Dual-LLM Routing
    
    Routes requests based on content analysis:
    - VISION: Contains images, image_url, screen capture, visual data
    - REASONING: Coding, logic, system analysis, complex reasoning
    - DEFAULT: General queries
    """
    
    # Keywords that indicate vision-related tasks
    VISION_KEYWORDS = [
        'image', 'visual', 'screen', 'capture', 'photo', 'picture',
        'screenshot', 'camera', 'webcam', 'face', 'expression',
        'see', 'look', 'view', 'display', 'monitor', 'pixel',
        'color', 'shape', 'object', 'detect', 'recognize',
        'vision', 'perception', 'retina', 'gemma', 'vision'
    ]
    
    # Keywords that indicate reasoning/coding tasks
    REASONING_KEYWORDS = [
        'code', 'function', 'class', 'variable', 'algorithm',
        'debug', 'error', 'fix', 'optimize', 'refactor',
        'python', 'javascript', 'sql', 'database', 'api',
        'logic', 'reason', 'calculate', 'compute', 'analyze',
        'system', 'architecture', 'design', 'pattern', 'omnicoder'
    ]
    
    def __init__(self):
        self.vision_available = False
        self.reasoning_available = False
        self.fallback_available = True
        self.routing_stats = {
            'vision': 0,
            'reasoning': 0,
            'fallback': 0
        }
    
    async def check_connectivity(self) -> Dict[str, bool]:
        """Check connectivity to all LLM endpoints"""
        results = {}
        
        # Check Vision Core (Port 1234)
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{LLMConfig.VISION_URL}/models")
                if response.status_code == 200:
                    results['vision'] = True
                    logger.info("✅ Vision Core (Gemma-3-4B) online")
                else:
                    results['vision'] = False
                    logger.warning("⚠️ Vision Core returned non-200")
        except Exception as e:
            results['vision'] = False
            logger.warning(f"⚠️ Vision Core unreachable: {e}")
        
        # Check Reasoning Core (Port 8012)
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{LLMConfig.REASONING_URL}/models")
                if response.status_code == 200:
                    results['reasoning'] = True
                    logger.info("✅ Reasoning Core (OmniCoder-9B) online")
                else:
                    results['reasoning'] = False
                    logger.warning("⚠️ Reasoning Core returned non-200")
        except Exception as e:
            results['reasoning'] = False
            logger.warning(f"⚠️ Reasoning Core unreachable: {e}")
        
        # Check Fallback (Port 1234)
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{LLMConfig.FALLBACK_URL}/models")
                if response.status_code == 200:
                    results['fallback'] = True
                    logger.info("✅ Fallback (LM Studio) online")
                else:
                    results['fallback'] = False
                    logger.warning("⚠️ Fallback returned non-200")
        except Exception as e:
            results['fallback'] = False
            logger.warning(f"⚠️ Fallback unreachable: {e}")
        
        return results
    
    def analyze_content(self, content: str, has_image: bool = False) -> RoutingDecision:
        """
        Analyze content and decide which LLM to route to
        
        Args:
            content: The text content to analyze
            has_image: Whether the request contains an image
            
        Returns:
            RoutingDecision with target and reason
        """
        content_lower = content.lower()
        
        # Check for vision indicators
        has_vision_keywords = any(kw in content_lower for kw in self.VISION_KEYWORDS)
        has_vision_request = has_image or 'vision' in content_lower or 'image' in content_lower
        
        # Check for reasoning indicators
        has_reasoning_keywords = any(kw in content_lower for kw in self.REASONING_KEYWORDS)
        has_reasoning_request = has_reasoning_keywords or 'code' in content_lower or 'logic' in content_lower
        
        # Decision logic
        if has_vision_request:
            decision = RoutingDecision(LLMTarget.VISION_GEMMA, priority=10)
            decision.reason = f"Vision request detected: {has_vision_keywords}"
            self.routing_stats['vision'] += 1
            return decision
        
        if has_reasoning_request:
            decision = RoutingDecision(LLMTarget.REASONING_OMNICODER, priority=10)
            decision.reason = f"Reasoning request detected: {has_reasoning_keywords}"
            self.routing_stats['reasoning'] += 1
            return decision
        
        # Default to fallback for general queries
        decision = RoutingDecision(LLMTarget.DEFAULT_LMSTUDIO, priority=0)
        decision.reason = "General query - using fallback"
        self.routing_stats['fallback'] += 1
        return decision
    
    def get_stats(self) -> Dict[str, int]:
        """Get routing statistics"""
        return self.routing_stats.copy()
    
    def reset_stats(self):
        """Reset routing statistics"""
        self.routing_stats = {
            'vision': 0,
            'reasoning': 0,
            'fallback': 0
        }


# ============================================================================
# DUAL-LLM CLIENT
# ============================================================================
class DualLLMClient:
    """
    High-performance Dual-LLM Client with intelligent routing
    
    Features:
    - Automatic routing based on content analysis
    - Connection health monitoring
    - Graceful fallback handling
    - Streaming support for both LLMs
    """
    
    def __init__(self):
        self.routing_engine = RoutingEngine()
        self.vision_client: Optional[httpx.AsyncClient] = None
        self.reasoning_client: Optional[httpx.AsyncClient] = None
        self.fallback_client: Optional[httpx.AsyncClient] = None
        self._clients_initialized = False
        
        # Connection tracking
        self._vision_connected = False
        self._reasoning_connected = False
        self._fallback_connected = False
    
    async def initialize_clients(self):
        """Initialize HTTP clients for all LLM endpoints"""
        if self._clients_initialized:
            return
        
        logger.info("🔧 Initializing Dual-LLM clients...")
        
        # Vision Client (Gemma-3-4B)
        self.vision_client = httpx.AsyncClient(
            timeout=120.0,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        
        # Reasoning Client (OmniCoder-9B)
        self.reasoning_client = httpx.AsyncClient(
            timeout=180.0,  # Longer timeout for complex reasoning
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        
        # Fallback Client (LM Studio)
        self.fallback_client = httpx.AsyncClient(
            timeout=120.0,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        
        self._clients_initialized = True
        logger.info("✅ Dual-LLM clients initialized")
    
    async def close_clients(self):
        """Close all HTTP clients"""
        if self.vision_client:
            await self.vision_client.aclose()
        if self.reasoning_client:
            await self.reasoning_client.aclose()
        if self.fallback_client:
            await self.fallback_client.aclose()
        self._clients_initialized = False
        logger.info("🔌 Dual-LLM clients closed")
    
    async def ensure_connectivity(self) -> Dict[str, bool]:
        """Ensure all LLM endpoints are reachable"""
        if not self._clients_initialized:
            await self.initialize_clients()
        
        return await self.routing_engine.check_connectivity()
    
    async def _build_messages(self, system_prompt: str, user_content: str) -> List[Dict]:
        """Build message structure for LLM API"""
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": user_content
        })
        
        return messages
    
    async def _call_vision_llm(
        self,
        messages: List[Dict],
        max_tokens: int = LLMConfig.VISION_MAX_TOKENS,
        temperature: float = LLMConfig.VISION_TEMPERATURE
    ) -> str:
        """Call Vision Core (Gemma-3-4B)"""
        if not self.vision_client:
            raise RuntimeError("Vision client not initialized")
        
        try:
            response = await self.vision_client.post(
                f"{LLMConfig.VISION_URL}/chat/completions",
                json={
                    "model": "gemma-3-4b",
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                return f"Vision Core Error: {response.status_code}"
                
        except httpx.ConnectError:
            logger.error("❌ Vision Core connection failed")
            raise
        except Exception as e:
            logger.error(f"❌ Vision Core error: {e}")
            raise
    
    async def _call_reasoning_llm(
        self,
        messages: List[Dict],
        max_tokens: int = LLMConfig.REASONING_MAX_TOKENS,
        temperature: float = LLMConfig.REASONING_TEMPERATURE
    ) -> str:
        """Call Reasoning Core (OmniCoder-9B)"""
        if not self.reasoning_client:
            raise RuntimeError("Reasoning client not initialized")
        
        try:
            response = await self.reasoning_client.post(
                f"{LLMConfig.REASONING_URL}/chat/completions",
                json={
                    "model": "omnicoder-9b",
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                return f"Reasoning Core Error: {response.status_code}"
                
        except httpx.ConnectError:
            logger.error("❌ Reasoning Core connection failed")
            raise
        except Exception as e:
            logger.error(f"❌ Reasoning Core error: {e}")
            raise
    
    async def _call_fallback_llm(
        self,
        messages: List[Dict],
        max_tokens: int = LLMConfig.FALLBACK_MAX_TOKENS,
        temperature: float = LLMConfig.FALLBACK_TEMPERATURE
    ) -> str:
        """Call Fallback LLM (LM Studio)"""
        if not self.fallback_client:
            raise RuntimeError("Fallback client not initialized")
        
        try:
            response = await self.fallback_client.post(
                f"{LLMConfig.FALLBACK_URL}/chat/completions",
                json={
                    "model": LLMConfig.FALLBACK_MODEL,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                return f"LM Studio Error: {response.status_code}"
                
        except httpx.ConnectError:
            logger.error("❌ LM Studio connection failed")
            raise
        except Exception as e:
            logger.error(f"❌ LM Studio error: {e}")
            raise
    
    async def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        user_id: int = 1,
        emotion: str = "neutral",
        force_vision: bool = False,
        force_reasoning: bool = False
    ) -> str:
        """
        Generate response with intelligent routing
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            user_id: User ID for tracking
            emotion: User emotion state
            force_vision: Force vision LLM
            force_reasoning: Force reasoning LLM
            
        Returns:
            Generated response text
        """
        await self.ensure_connectivity()
        
        # Analyze content for routing
        routing = self.routing_engine.analyze_content(prompt)
        
        # Apply force overrides
        if force_vision:
            routing = RoutingDecision(LLMTarget.VISION_GEMMA, priority=100)
        elif force_reasoning:
            routing = RoutingDecision(LLMTarget.REASONING_OMNICODER, priority=100)
        
        logger.info(f"🎯 Routing: {routing.target.value} ({routing.reason})")
        
        # Build messages
        messages = await self._build_messages(system_prompt, prompt)
        
        # Route to appropriate LLM
        try:
            if routing.target == LLMTarget.VISION_GEMMA:
                response = await self._call_vision_llm(messages)
                logger.info("👁️ Vision Core responded")
                return response
            
            elif routing.target == LLMTarget.REASONING_OMNICODER:
                response = await self._call_reasoning_llm(messages)
                logger.info("🧠 Reasoning Core responded")
                return response
            
            else:  # FALLBACK
                response = await self._call_fallback_llm(messages)
                logger.info("📡 Fallback LLM responded")
                return response
                
        except Exception as e:
            logger.error(f"❌ Generation failed: {e}")
            
            # Try fallback if primary failed
            if routing.target == LLMTarget.VISION_GEMMA:
                try:
                    logger.info("🔄 Falling back to Reasoning Core...")
                    messages = await self._build_messages(system_prompt, prompt)
                    return await self._call_reasoning_llm(messages)
                except:
                    pass
            
            if routing.target == LLMTarget.REASONING_OMNICODER:
                try:
                    logger.info("🔄 Falling back to Vision Core...")
                    messages = await self._build_messages(system_prompt, prompt)
                    return await self._call_vision_llm(messages)
                except:
                    pass
            
            # Last resort fallback
            try:
                logger.info("🔄 Final fallback to LM Studio...")
                messages = await self._build_messages(system_prompt, prompt)
                return await self._call_fallback_llm(messages)
            except:
                return f"❌ All LLMs unavailable. Please check your connections."
    
    async def generate_stream(
        self,
        prompt: str,
        system_prompt: str = "",
        user_id: int = 1,
        emotion: str = "neutral",
        force_vision: bool = False,
        force_reasoning: bool = False
    ) -> AsyncGenerator[str, None]:
        """
        Generate response with streaming and intelligent routing
        
        Yields text chunks as they arrive
        """
        await self.ensure_connectivity()
        
        # Analyze content for routing
        routing = self.routing_engine.analyze_content(prompt)
        
        # Apply force overrides
        if force_vision:
            routing = RoutingDecision(LLMTarget.VISION_GEMMA, priority=100)
        elif force_reasoning:
            routing = RoutingDecision(LLMTarget.REASONING_OMNICODER, priority=100)
        
        logger.info(f"🎯 Streaming Routing: {routing.target.value} ({routing.reason})")
        
        # Build messages
        messages = await self._build_messages(system_prompt, prompt)
        
        # Route to appropriate LLM with streaming
        try:
            if routing.target == LLMTarget.VISION_GEMMA:
                async for chunk in self._stream_vision_llm(messages):
                    yield chunk
                logger.info("👁️ Vision Core streaming complete")
                return
            
            elif routing.target == LLMTarget.REASONING_OMNICODER:
                async for chunk in self._stream_reasoning_llm(messages):
                    yield chunk
                logger.info("🧠 Reasoning Core streaming complete")
                return
            
            else:  # FALLBACK
                async for chunk in self._stream_fallback_llm(messages):
                    yield chunk
                logger.info("📡 Fallback LLM streaming complete")
                return
                
        except Exception as e:
            logger.error(f"❌ Streaming failed: {e}")
            yield f"Error: {str(e)}"
    
    async def _stream_vision_llm(
        self,
        messages: List[Dict]
    ) -> AsyncGenerator[str, None]:
        """Stream from Vision Core"""
        if not self.vision_client:
            raise RuntimeError("Vision client not initialized")
        
        try:
            async with self.vision_client.stream(
                "POST",
                f"{LLMConfig.VISION_URL}/chat/completions",
                json={
                    "model": "gemma-3-4b",
                    "messages": messages,
                    "temperature": LLMConfig.VISION_TEMPERATURE,
                    "max_tokens": LLMConfig.VISION_MAX_TOKENS,
                    "stream": True
                }
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        
                        try:
                            chunk = json.loads(data)
                            if "choices" in chunk and chunk["choices"]:
                                delta = chunk["choices"][0].get("delta", {})
                                if "content" in delta:
                                    content = delta["content"]
                                    yield content
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            logger.error(f"Vision stream error: {e}")
            yield f"Error: {str(e)}"
    
    async def _stream_reasoning_llm(
        self,
        messages: List[Dict]
    ) -> AsyncGenerator[str, None]:
        """Stream from Reasoning Core"""
        if not self.reasoning_client:
            raise RuntimeError("Reasoning client not initialized")
        
        try:
            async with self.reasoning_client.stream(
                "POST",
                f"{LLMConfig.REASONING_URL}/chat/completions",
                json={
                    "model": "omnicoder-9b",
                    "messages": messages,
                    "temperature": LLMConfig.REASONING_TEMPERATURE,
                    "max_tokens": LLMConfig.REASONING_MAX_TOKENS,
                    "stream": True
                }
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        
                        try:
                            chunk = json.loads(data)
                            if "choices" in chunk and chunk["choices"]:
                                delta = chunk["choices"][0].get("delta", {})
                                if "content" in delta:
                                    content = delta["content"]
                                    yield content
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            logger.error(f"Reasoning stream error: {e}")
            yield f"Error: {str(e)}"
    
    async def _stream_fallback_llm(
        self,
        messages: List[Dict]
    ) -> AsyncGenerator[str, None]:
        """Stream from Fallback LLM"""
        if not self.fallback_client:
            raise RuntimeError("Fallback client not initialized")
        
        try:
            async with self.fallback_client.stream(
                "POST",
                f"{LLMConfig.FALLBACK_URL}/chat/completions",
                json={
                    "model": LLMConfig.FALLBACK_MODEL,
                    "messages": messages,
                    "temperature": LLMConfig.FALLBACK_TEMPERATURE,
                    "max_tokens": LLMConfig.FALLBACK_MAX_TOKENS,
                    "stream": True
                }
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        
                        try:
                            chunk = json.loads(data)
                            if "choices" in chunk and chunk["choices"]:
                                delta = chunk["choices"][0].get("delta", {})
                                if "content" in delta:
                                    content = delta["content"]
                                    yield content
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            logger.error(f"Fallback stream error: {e}")
            yield f"Error: {str(e)}"
    
    def get_routing_stats(self) -> Dict[str, int]:
        """Get routing statistics"""
        return self.routing_engine.get_stats()
    
    def reset_routing_stats(self):
        """Reset routing statistics"""
        self.routing_engine.reset_stats()


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================
llm = DualLLMClient()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
async def check_llm_health() -> Dict[str, Any]:
    """Check health of all LLM endpoints"""
    client = DualLLMClient()
    await client.initialize_clients()
    connectivity = await client.ensure_connectivity()
    stats = client.get_routing_stats()
    await client.close_clients()
    
    return {
        "status": "healthy" if all(connectivity.values()) else "degraded",
        "connectivity": connectivity,
        "routing_stats": stats
    }


async def get_llm_stats() -> Dict[str, Any]:
    """Get LLM routing statistics"""
    client = DualLLMClient()
    stats = client.get_routing_stats()
    await client.close_clients()
    
    return {
        "vision_calls": stats['vision'],
        "reasoning_calls": stats['reasoning'],
        "fallback_calls": stats['fallback'],
        "total_calls": sum(stats.values())
    }