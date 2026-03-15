# backend/core/model_router.py
import logging
from typing import Optional, Dict, List
from enum import Enum

logger = logging.getLogger("ModelRouter")

class TaskType(Enum):
    REASONING = "reasoning"
    VISION = "vision"
    RESEARCH = "research"
    CODE = "code"
    CHAT = "chat"
    VOICE = "voice"
    GENERAL = "general"

class ModelCapabilities:
    """Define what each model can do"""
    def __init__(self, model_id: str, capabilities: List[str], priority: int = 1):
        self.model_id = model_id
        self.capabilities = set(capabilities)  # e.g., ['reasoning', 'code', 'fast']
        self.priority = priority  # Higher = preferred when multiple match

# Define available models and their capabilities
AVAILABLE_MODELS = {
    "llama-3-70b-instruct": ModelCapabilities(
        model_id="llama-3-70b-instruct",
        capabilities=["reasoning", "chat", "general"],
        priority=10
    ),
    "llava-1.5-13b": ModelCapabilities(
        model_id="llava-1.5-13b",
        capabilities=["vision", "chat"],
        priority=8
    ),
    "codellama-34b-instruct": ModelCapabilities(
        model_id="codellama-34b-instruct",
        capabilities=["code", "reasoning"],
        priority=9
    ),
    "mistral-7b-instruct": ModelCapabilities(
        model_id="mistral-7b-instruct",
        capabilities=["chat", "fast", "general"],
        priority=5
    ),
    # Add more models as you load them in LM Studio
}

class ModelRouter:
    def __init__(self):
        self.active_models = {}  # model_id -> connection/client
        self.default_model = "mistral-7b-instruct"
        
    def register_model(self, model_id: str, client, capabilities: List[str]):
        """Register a model loaded in LM Studio"""
        AVAILABLE_MODELS[model_id] = ModelCapabilities(model_id, capabilities)
        self.active_models[model_id] = client
        logger.info(f"✅ Registered model: {model_id} with capabilities: {capabilities}")
    
    def detect_task_type(self, query: str, context: Dict = None) -> TaskType:
        """Analyze query to determine best task type"""
        query_lower = query.lower()
        
        # Vision tasks
        if any(word in query_lower for word in ["image", "picture", "photo", "see", "visual", "screenshot", "what do you see"]):
            return TaskType.VISION
        
        # Code tasks
        if any(word in query_lower for word in ["code", "python", "javascript", "function", "script", "program", "debug", "write code"]):
            return TaskType.CODE
        
        # Research tasks
        if any(word in query_lower for word in ["search", "find", "research", "look up", "web", "internet", "current", "news"]):
            return TaskType.RESEARCH
        
        # Complex reasoning
        if any(word in query_lower for word in ["solve", "analyze", "explain", "why", "how does", "compare", "evaluate", "think"]):
            return TaskType.REASONING
        
        # Voice/speech specific
        if context and context.get("is_voice_mode"):
            return TaskType.VOICE
        
        return TaskType.GENERAL
    
    def select_best_model(self, task_type: TaskType, query: str = "") -> str:
        """Select the best model for the task"""
        candidates = []
        
        for model_id, caps in AVAILABLE_MODELS.items():
            if model_id not in self.active_models:
                continue  # Skip models not loaded in LM Studio
            
            # Check if model has required capability
            if task_type.value in caps.capabilities or "general" in caps.capabilities:
                candidates.append((model_id, caps.priority))
        
        if not candidates:
            logger.warning(f"⚠️ No model found for task {task_type}, using default")
            return self.default_model
        
        # Sort by priority (highest first) and return best match
        candidates.sort(key=lambda x: x[1], reverse=True)
        selected = candidates[0][0]
        
        logger.info(f"🎯 Selected model '{selected}' for task: {task_type.value}")
        return selected
    
    async def generate(self, query: str, system_prompt: str = "", context: Dict = None, **kwargs):
        """Main entry point - auto-routes to best model"""
        # 1. Detect task type
        task_type = self.detect_task_type(query, context)
        
        # 2. Select best model
        model_id = self.select_best_model(task_type, query)
        
        # 3. Get model client
        client = self.active_models.get(model_id)
        if not client:
            logger.error(f"❌ Model {model_id} not available")
            return f"Error: Model '{model_id}' is not loaded in LM Studio."
        
        # 4. Add model selection info to system prompt (for transparency)
        enhanced_prompt = f"{system_prompt}\n\n[Using model: {model_id} for {task_type.value} task]"
        
        # 5. Generate response (delegate to actual model client)
        # This assumes each client has a .generate() method
        try:
            response = await client.generate(query, enhanced_prompt, **kwargs)
            # Add metadata about which model was used
            return {
                "response": response,
                "model_used": model_id,
                "task_type": task_type.value
            }
        except Exception as e:
            logger.error(f"❌ Generation error with {model_id}: {e}")
            # Fallback to default model
            if model_id != self.default_model:
                fallback_client = self.active_models.get(self.default_model)
                if fallback_client:
                    return await fallback_client.generate(query, system_prompt, **kwargs)
            return f"Error: {str(e)}"

# Global instance
model_router = ModelRouter()