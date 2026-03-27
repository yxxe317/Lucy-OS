# backend/core/api_router.py
import httpx
import json
import logging
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
# Add at the very top
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

logger = logging.getLogger("APIRouter")

CONFIG_PATH = Path(__file__).parent.parent / "config" / "ai_config.json"

# ==================== EXISTING AI PROVIDER CODE (PRESERVED) ====================

class AIProvider:
    """Base class for AI providers"""
    def __init__(self, name: str, config: Dict):
        self.name = name
        self.config = config
        self.base_url = config.get("base_url", "")
        self.model = config.get("model", "")
        self.api_key = config.get("api_key")
        self.enabled = config.get("enabled", False)
        self.timeout = 120
    
    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Override in child classes"""
        raise NotImplementedError

class LMStudioProvider(AIProvider):
    """LM Studio local provider"""
    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json={
                        "model": self.model if self.model != "auto-detect" else "local-model",
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 2048,
                        "stream": False
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"].strip()
                return f"Error: LM Studio returned {response.status_code}"
                
        except httpx.ConnectError:
            return "❌ Cannot connect to LM Studio. Please start the server in LM Studio (File → Start Server)."
        except Exception as e:
            return f"Error: {str(e)}"

class OpenAIProvider(AIProvider):
    """OpenAI API provider"""
    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key:
            return "❌ OpenAI API key not configured"
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 2048
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"].strip()
                return f"Error: OpenAI returned {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"

class GeminiProvider(AIProvider):
    """Google Gemini API provider"""
    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key:
            return "❌ Gemini API key not configured"
        
        try:
            # Gemini uses a different format
            contents = []
            if system_prompt:
                contents.append({
                    "role": "user",
                    "parts": [{"text": f"System: {system_prompt}\n\nUser: {prompt}"}]
                })
            else:
                contents.append({"role": "user", "parts": [{"text": prompt}]})
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}",
                    headers={"Content-Type": "application/json"},
                    json={
                        "contents": contents,
                        "generationConfig": {
                            "temperature": 0.7,
                            "maxOutputTokens": 2048
                        }
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["candidates"][0]["content"]["parts"][0]["text"].strip()
                return f"Error: Gemini returned {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"

class AnthropicProvider(AIProvider):
    """Anthropic Claude API provider"""
    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key:
            return "❌ Anthropic API key not configured"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "system": system_prompt if system_prompt else "You are a helpful AI assistant.",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 2048,
                        "temperature": 0.7
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["content"][0]["text"].strip()
                return f"Error: Anthropic returned {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"

class OllamaProvider(AIProvider):
    """Ollama local provider"""
    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": False
                    }
                )
                if response.status_code == 200:
                    result = response.json()
                    return result["message"]["content"].strip()
                return f"Error: Ollama returned {response.status_code}"
        except httpx.ConnectError:
            return "❌ Cannot connect to Ollama. Please run 'ollama serve'."
        except Exception as e:
            return f"Error: {str(e)}"

class APIRouter:
    """Router to select and use AI providers"""
    
    PROVIDERS = {
        "lm_studio": LMStudioProvider,
        "openai": OpenAIProvider,
        "gemini": GeminiProvider,
        "anthropic": AnthropicProvider,
        "ollama": OllamaProvider
    }
    
    def __init__(self):
        self.config = self._load_config()
        self.providers = {}
        self._init_providers()
    
    def _load_config(self) -> Dict:
        """Load AI config from file"""
        try:
            if CONFIG_PATH.exists():
                with open(CONFIG_PATH, "r") as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load AI config: {e}")
        
        # Return defaults if config missing - USING OLLAMA AS DEFAULT
        return {
            "default_provider": "ollama",
            "providers": {
                "lm_studio": {"enabled": True, "base_url": "http://127.0.0.1:1234/v1"},
                "ollama": {"enabled": True, "base_url": "http://127.0.0.1:11434", "model": "llama3"}
            },
            "fallback_to_lm_studio": False
        }
    
    def _init_providers(self):
        """Initialize enabled providers"""
        providers_config = self.config.get("providers", {})
        
        for name, provider_config in providers_config.items():
            if provider_config.get("enabled", False) and name in self.PROVIDERS:
                try:
                    self.providers[name] = self.PROVIDERS[name](name, provider_config)
                    logger.info(f"✅ Initialized provider: {name}")
                except Exception as e:
                    logger.error(f"❌ Failed to initialize {name}: {e}")
    
    def get_provider(self, provider_name: Optional[str] = None) -> Optional[AIProvider]:
        """Get a specific provider or the default"""
        if provider_name and provider_name in self.providers:
            return self.providers[provider_name]
        
        # Try default
        default = self.config.get("default_provider", "lm_studio")
        if default in self.providers:
            return self.providers[default]
        
        # Fallback to any enabled provider
        if self.providers:
            return next(iter(self.providers.values()))
        
        return None
    
    async def generate(self, prompt: str, system_prompt: str = "", provider: Optional[str] = None) -> str:
        """Generate response using selected provider"""
        ai_provider = self.get_provider(provider)
        
        if not ai_provider:
            return "❌ No AI provider configured. Please enable at least one provider in config/ai_config.json"
        
        logger.info(f"🤖 Using provider: {ai_provider.name} with model: {ai_provider.model}")
        
        try:
            response = await ai_provider.generate(prompt, system_prompt)
            return response
        except Exception as e:
            # Fallback to LM Studio if enabled
            if self.config.get("fallback_to_lm_studio", True) and "lm_studio" in self.providers:
                logger.warning(f"⚠️ Provider {ai_provider.name} failed, falling back to LM Studio")
                return await self.providers["lm_studio"].generate(prompt, system_prompt)
            return f"Error: {str(e)}"
    
    def get_available_providers(self) -> list:
        """Get list of enabled providers"""
        return list(self.providers.keys())
    
    def reload_config(self):
        """Reload config and reinitialize providers"""
        self.config = self._load_config()
        self.providers = {}
        self._init_providers()
        logger.info("🔄 AI config reloaded")

# Global instance
api_router = APIRouter()

# ==================== NEW MODULE ENDPOINTS (ADDED) ====================

# Create a FastAPI router for module endpoints - FIXED
from fastapi import APIRouter as FastAPIRouter
module_router = FastAPIRouter(prefix="/api", tags=["modules"])

# ==================== REQUEST MODELS ====================

class EmotionTrigger(BaseModel):
    emotion: str

class QuantumEntangleRequest(BaseModel):
    thought1: str
    thought2: str

class QuantumDecideRequest(BaseModel):
    options: List[str]

class DreamRequest(BaseModel):
    seed: Optional[str] = None

class TimePerceptionRequest(BaseModel):
    seconds: float
    mental_state: str = "excitement"

class TranslateRequest(BaseModel):
    text: str
    target: str = "es"
    source: str = "en"

class FactRequest(BaseModel):
    fact: str
    category: str = "general"

class GoalRequest(BaseModel):
    description: str
    priority: int = 1

class ActionRequest(BaseModel):
    action: str
    context: Dict[str, Any] = {}

# ==================== TRY IMPORT ALL MODULES ====================

# Memory modules
try:
    from modules.memory.long_term import LongTermMemory
    from modules.memory.working import WorkingMemory
    from modules.memory.episodic import EpisodicMemory
    from modules.memory.semantic import SemanticMemory
    from modules.memory.procedural import ProceduralMemory
    from modules.memory.emotional import EmotionalMemory
    from modules.memory.memory_palace import MemoryPalace
    from modules.memory.consolidation import MemoryConsolidation
    from modules.memory.forgetting import ForgettingCurve
    MEMORY_AVAILABLE = True
    logger.info("✅ Memory modules loaded")
except ImportError as e:
    logger.warning(f"Memory modules not available: {e}")
    MEMORY_AVAILABLE = False

# Emotion modules
try:
    from modules.emotion.mood_engine import MoodEngine
    from modules.emotion.personality import Personality
    from modules.emotion.empathy import Empathy
    from modules.emotion.humor import Humor
    EMOTION_AVAILABLE = True
    logger.info("✅ Emotion modules loaded")
except ImportError:
    EMOTION_AVAILABLE = False

# Knowledge modules
try:
    from modules.knowledge.knowledge_graph import KnowledgeGraph
    from modules.knowledge.wikipedia import Wikipedia
    from modules.knowledge.web_search import WebSearch
    from modules.knowledge.reasoning import ReasoningEngine
    from modules.knowledge.fact_check import FactChecker
    from modules.knowledge.scientific import ScientificReasoning
    from modules.knowledge.mathematical import MathematicalReasoning
    from modules.knowledge.misinformation import MisinformationDetector
    KNOWLEDGE_AVAILABLE = True
    logger.info("✅ Knowledge modules loaded")
except ImportError:
    KNOWLEDGE_AVAILABLE = False

# Language modules
try:
    from modules.language.translator import Translator
    from modules.language.stt import SpeechToText
    from modules.language.creative import CreativeWriter
    from modules.language.summarizer import TextSummarizer
    from modules.language.negotiator import Negotiator
    from modules.language.tutor import LanguageTutor
    LANGUAGE_AVAILABLE = True
    logger.info("✅ Language modules loaded")
except ImportError:
    LANGUAGE_AVAILABLE = False

# Integration modules
try:
    from modules.integrations.weather import Weather
    from modules.integrations.news import News
    from modules.integrations.stocks import Stocks
    from modules.integrations.crypto import Crypto
    from modules.integrations.email_client import EmailClient
    from modules.integrations.calendar import Calendar
    from modules.integrations.smart_home import SmartHome
    from modules.integrations.github import GitHub
    from modules.integrations.web_browser import WebBrowser
    from modules.integrations.api_gateway import APIGateway
    from modules.integrations.database import Database
    INTEGRATIONS_AVAILABLE = True
    logger.info("✅ Integration modules loaded")
except ImportError:
    INTEGRATIONS_AVAILABLE = False

# Quantum modules
try:
    from modules.quantum.quantum_algorithm import QuantumAlgorithm
    from modules.quantum.entanglement import QuantumEntanglement
    from modules.quantum.quantum_memory import QuantumMemory
    from modules.quantum.quantum_decision import QuantumDecision
    from modules.quantum.quantum_sim import QuantumSimulator
    QUANTUM_AVAILABLE = True
    logger.info("✅ Quantum modules loaded")
except ImportError:
    QUANTUM_AVAILABLE = False

# Creativity modules
try:
    from modules.creativity.poetry import PoetryGenerator
    from modules.creativity.story import StoryGenerator
    from modules.creativity.music import MusicGenerator
    from modules.creativity.visual import VisualArtGenerator
    from modules.creativity.design import DesignGenerator
    CREATIVITY_AVAILABLE = True
    logger.info("✅ Creativity modules loaded")
except ImportError:
    CREATIVITY_AVAILABLE = False

# Autonomy modules
try:
    from modules.autonomy.goal_planner import GoalPlanner
    from modules.autonomy.task_executor import TaskExecutor
    from modules.autonomy.scheduler import Scheduler
    from modules.autonomy.resource_manager import ResourceManager
    from modules.autonomy.learning import AutonomousLearning
    AUTONOMY_AVAILABLE = True
    logger.info("✅ Autonomy modules loaded")
except ImportError:
    AUTONOMY_AVAILABLE = False

# Ethics modules
try:
    from modules.ethics.ethical_framework import EthicalFramework
    from modules.ethics.safety import SafetyModule
    from modules.ethics.bias_detection import BiasDetector
    from modules.ethics.privacy import PrivacyModule
    from modules.ethics.audit import AuditModule
    ETHICS_AVAILABLE = True
    logger.info("✅ Ethics modules loaded")
except ImportError:
    ETHICS_AVAILABLE = False

# Advanced modules
try:
    from modules.advanced.brain_computer import BrainComputerInterface
    from modules.advanced.consciousness import QuantumConsciousness
    from modules.advanced.dream import DreamSimulator
    from modules.advanced.time_perception import TimePerception
    from modules.advanced.multiverse import MultiverseExplorer
    ADVANCED_AVAILABLE = True
    logger.info("✅ Advanced modules loaded")
except ImportError:
    ADVANCED_AVAILABLE = False

# ==================== MEMORY ENDPOINTS ====================

@module_router.get("/memory/status")
async def memory_status():
    """Get memory system status"""
    if not MEMORY_AVAILABLE:
        return {"available": False, "message": "Memory modules not installed"}
    
    try:
        ltm = LongTermMemory(":memory:")
        stats = {
            "long_term": True,
            "working": True,
            "episodic": True,
            "semantic": True,
            "procedural": True,
            "emotional": True,
            "memory_palace": True
        }
        return {"available": True, "stats": stats}
    except Exception as e:
        return {"available": True, "error": str(e)}

# ==================== EMOTION ENDPOINTS ====================

@module_router.get("/emotion/mood")
async def get_mood():
    """Get current emotional state"""
    if not EMOTION_AVAILABLE:
        return {"joy": 0.5, "sadness": 0.1, "anger": 0.1, "fear": 0.1}
    
    mood = MoodEngine()
    return mood.get_current_mood()

@module_router.post("/emotion/trigger")
async def trigger_emotion(request: EmotionTrigger):
    """Trigger an emotional event"""
    if not EMOTION_AVAILABLE:
        return {"success": True, "message": "Emotion simulated"}
    
    mood = MoodEngine()
    mood.trigger_event(request.emotion)
    return {"success": True, "mood": mood.get_current_mood()}

@module_router.get("/emotion/personality")
async def get_personality():
    """Get personality traits"""
    if not EMOTION_AVAILABLE:
        return {"openness": 0.7, "conscientiousness": 0.6, "extraversion": 0.5}
    
    p = Personality()
    return p.get_traits()

@module_router.get("/emotion/humor/joke")
async def get_joke(category: Optional[str] = None):
    """Get a joke"""
    if not EMOTION_AVAILABLE:
        return {"joke": "Why did the chicken cross the road? To get to the other side!"}
    
    h = Humor()
    return {"joke": h.tell_joke(category)}

# ==================== KNOWLEDGE ENDPOINTS ====================

@module_router.post("/knowledge/fact")
async def add_fact(request: FactRequest):
    """Add a fact to knowledge graph"""
    if not KNOWLEDGE_AVAILABLE:
        return {"success": True, "entity_id": "simulated"}
    
    kg = KnowledgeGraph()
    entity_id = kg.add_entity(request.fact, request.category)
    return {"success": True, "entity_id": entity_id}

@module_router.get("/knowledge/search/{query}")
async def search_knowledge(query: str):
    """Search knowledge graph"""
    if not KNOWLEDGE_AVAILABLE:
        return {"results": []}
    
    kg = KnowledgeGraph()
    results = kg.find_entity(query)
    return {"results": results}

@module_router.get("/knowledge/wikipedia/{query}")
async def wikipedia_search(query: str):
    """Search Wikipedia"""
    if not KNOWLEDGE_AVAILABLE:
        return {"results": []}
    
    wiki = Wikipedia()
    return {"results": wiki.search(query)}

@module_router.post("/knowledge/factcheck")
async def fact_check(request: dict):
    """Check a fact"""
    if not KNOWLEDGE_AVAILABLE:
        return {"verdict": "unknown", "confidence": 0.5}
    
    claim = request.get("claim", "")
    fc = FactChecker()
    return fc.check(claim)

# ==================== LANGUAGE ENDPOINTS ====================

@module_router.post("/language/translate")
async def translate_text(request: TranslateRequest):
    """Translate text"""
    if not LANGUAGE_AVAILABLE:
        return {"original": request.text, "translation": f"[{request.target}] {request.text}"}
    
    t = Translator()
    translation = t.translate(request.text, request.target, request.source)
    return {"original": request.text, "translation": translation}

@module_router.post("/language/summarize")
async def summarize_text(request: dict):
    """Summarize text"""
    if not LANGUAGE_AVAILABLE:
        text = request.get("text", "")
        return {"summary": text[:100] + "..." if len(text) > 100 else text}
    
    ts = TextSummarizer()
    text = request.get("text", "")
    ratio = request.get("ratio", 0.3)
    summary = ts.summarize(text, ratio)
    return {"summary": summary}

@module_router.post("/language/creative/poem")
async def generate_poem(request: dict):
    """Generate a poem"""
    if not LANGUAGE_AVAILABLE or not CREATIVITY_AVAILABLE:
        return {
            "title": "Nature's Beauty",
            "lines": ["The sun rises high", "Birds sing in the sky", "Nature's lullaby"],
            "form": "haiku"
        }
    
    cw = CreativeWriter()
    theme = request.get("theme", "nature")
    poem = cw.generate_haiku(theme)
    return {"title": f"Poem about {theme}", "lines": poem.split('\n'), "form": "haiku"}

@module_router.post("/language/stt")
async def speech_to_text(request: dict):
    """Convert speech to text (placeholder)"""
    if not LANGUAGE_AVAILABLE:
        return {"text": "Simulated speech to text result"}
    
    stt = SpeechToText()
    # In real implementation, you'd receive audio file here
    return {"text": stt.listen_once()}

# ==================== INTEGRATION ENDPOINTS ====================

@module_router.get("/integrations/weather/{location}")
async def get_weather(location: str):
    """Get weather for location"""
    if not INTEGRATIONS_AVAILABLE:
        return {
            "location": location,
            "temperature": 22,
            "conditions": "clear sky",
            "humidity": 65
        }
    
    w = Weather()
    return w.get_current(location)

@module_router.get("/integrations/news")
async def get_news(country: str = "us", category: Optional[str] = None):
    """Get news headlines"""
    if not INTEGRATIONS_AVAILABLE:
        return {"headlines": [{"title": "Sample News", "source": "AP"}]}
    
    n = News()
    return {"headlines": n.get_top_headlines(country, category)}

@module_router.get("/integrations/stocks/{symbol}")
async def get_stock(symbol: str):
    """Get stock quote"""
    if not INTEGRATIONS_AVAILABLE:
        return {"symbol": symbol, "price": 100.0, "change": 0.5}
    
    s = Stocks()
    return s.get_quote(symbol)

@module_router.get("/integrations/crypto/{coin}")
async def get_crypto(coin: str = "bitcoin"):
    """Get crypto price"""
    if not INTEGRATIONS_AVAILABLE:
        return {"coin": coin, "price": 50000}
    
    c = Crypto()
    return c.get_price(coin)

@module_router.get("/integrations/github/{username}")
async def get_github_user(username: str):
    """Get GitHub user info"""
    if not INTEGRATIONS_AVAILABLE:
        return {"login": username, "name": username, "public_repos": 10}
    
    gh = GitHub()
    return gh.get_user(username)

# ==================== QUANTUM ENDPOINTS ====================

@module_router.post("/quantum/entangle")
async def entangle_thoughts(request: QuantumEntangleRequest):
    """Entangle two thoughts"""
    if not QUANTUM_AVAILABLE and not ADVANCED_AVAILABLE:
        return {
            "success": True,
            "entanglement_id": "simulated",
            "thoughts": [request.thought1, request.thought2]
        }
    
    try:
        from modules.quantum.entanglement import QuantumEntanglement
        qe = QuantumEntanglement()
        ent_id = qe.create_bell_pair(0, 1)  # Simplified
        return {
            "success": True,
            "entanglement_id": ent_id,
            "thoughts": [request.thought1, request.thought2]
        }
    except:
        qc = QuantumConsciousness()
        ent_id = qc.entangle_thoughts(request.thought1, request.thought2)
        return {
            "success": True,
            "entanglement_id": ent_id,
            "thoughts": [request.thought1, request.thought2]
        }

@module_router.post("/quantum/decide")
async def quantum_decision(request: QuantumDecideRequest):
    """Make quantum decision"""
    if not QUANTUM_AVAILABLE:
        import random
        return {"choice": random.choice(request.options) if request.options else None}
    
    qd = QuantumDecision()
    choice = qd.superposition_choice(request.options)
    return {"choice": choice, "options": request.options}

# ==================== CREATIVITY ENDPOINTS ====================

@module_router.get("/creativity/poem")
async def generate_poem(theme: Optional[str] = None, form: str = "haiku"):
    """Generate a poem"""
    if not CREATIVITY_AVAILABLE:
        return {
            "title": "Nature's Beauty",
            "lines": ["The sun rises high", "Birds sing in the sky", "Nature's lullaby"],
            "form": "haiku"
        }
    
    pg = PoetryGenerator()
    poem = pg.generate_poem(form, theme)
    return poem

@module_router.get("/creativity/story")
async def generate_story(genre: Optional[str] = None):
    """Generate a story"""
    if not CREATIVITY_AVAILABLE:
        return {
            "title": "The Adventure",
            "genre": genre or "fantasy",
            "logline": "A hero embarks on a journey"
        }
    
    sg = StoryGenerator()
    story = sg.generate_story(genre)
    return story

@module_router.get("/creativity/music")
async def generate_music(key: str = "C", scale: str = "major"):
    """Generate a melody"""
    if not CREATIVITY_AVAILABLE:
        return {"melody": [{"note": "C4", "duration": "quarter"}]}
    
    mg = MusicGenerator()
    melody = mg.generate_melody(key, scale, 8)
    return {"melody": melody}

@module_router.get("/creativity/art")
async def generate_art():
    """Generate art concept"""
    if not CREATIVITY_AVAILABLE:
        return {
            "title": "Abstract Composition",
            "movement": "modern",
            "description": "A beautiful artwork"
        }
    
    va = VisualArtGenerator()
    return va.generate_art_concept()

@module_router.get("/creativity/design/brand")
async def generate_brand():
    """Generate brand identity"""
    if not CREATIVITY_AVAILABLE:
        return {
            "company_name": "Creative Solutions",
            "tagline": "Innovate the future"
        }
    
    dg = DesignGenerator()
    return dg.generate_brand_identity()

# ==================== AUTONOMY ENDPOINTS ====================

@module_router.post("/autonomy/goal")
async def create_goal(request: GoalRequest):
    """Create a new goal"""
    if not AUTONOMY_AVAILABLE:
        return {"id": "temp", "description": request.description}
    
    gp = GoalPlanner()
    goal = gp.create_goal(request.description, request.priority)
    return goal

@module_router.get("/autonomy/goals")
async def get_goals():
    """Get all active goals"""
    if not AUTONOMY_AVAILABLE:
        return {"goals": []}
    
    gp = GoalPlanner()
    return {"goals": gp.get_active_goals()}

@module_router.post("/autonomy/task")
async def add_task(request: dict):
    """Add a task"""
    if not AUTONOMY_AVAILABLE:
        return {"task_id": "temp"}
    
    te = TaskExecutor()
    task_id = te.add_task(
        request.get("name", "Task"),
        priority=request.get("priority", 1)
    )
    return {"task_id": task_id}

@module_router.get("/autonomy/schedule")
async def get_schedule():
    """Get today's schedule"""
    if not AUTONOMY_AVAILABLE:
        return {"events": []}
    
    sched = Scheduler()
    return {"events": sched.get_today_schedule()}

# ==================== ETHICS ENDPOINTS ====================

@module_router.post("/ethics/evaluate")
async def evaluate_action(request: ActionRequest):
    """Evaluate ethical implications"""
    if not ETHICS_AVAILABLE:
        return {
            "action": request.action,
            "ethical_score": 5.0,
            "recommendation": "Proceed with caution"
        }
    
    ef = EthicalFramework()
    return ef.evaluate_action(request.action, request.context)

@module_router.post("/ethics/safety/assess")
async def assess_safety(request: ActionRequest):
    """Assess safety of action"""
    if not ETHICS_AVAILABLE:
        return {"risk_level": "low", "risk_score": 0}
    
    sm = SafetyModule()
    return sm.assess_risk(request.action, request.context)

@module_router.post("/ethics/bias/analyze")
async def analyze_bias(request: dict):
    """Analyze text for bias"""
    if not ETHICS_AVAILABLE:
        return {"bias_score": 0, "findings": []}
    
    bd = BiasDetector()
    text = request.get("text", "")
    return bd.analyze_text(text)

# ==================== ADVANCED ENDPOINTS ====================

@module_router.get("/advanced/dream")
async def generate_dream():
    """Generate a dream"""
    if not ADVANCED_AVAILABLE:
        return {
            "title": "Mysterious Dream",
            "phase": "REM",
            "narrative": "A strange dream...",
            "emotion": "curiosity"
        }
    
    ds = DreamSimulator()
    return ds.generate_dream()

@module_router.post("/advanced/time")
async def time_perception(request: TimePerceptionRequest):
    """Test time perception"""
    if not ADVANCED_AVAILABLE:
        return {
            "real_duration": request.seconds,
            "subjective_duration": request.seconds,
            "experience": "normal"
        }
    
    tp = TimePerception()
    return tp.subjective_duration(request.seconds, request.mental_state)

@module_router.get("/advanced/multiverse")
async def explore_multiverse():
    """Explore multiverse"""
    if not ADVANCED_AVAILABLE:
        return {
            "statistics": {"total_universes": 1},
            "new_universe": "prime"
        }
    
    me = MultiverseExplorer()
    stats = me.get_multiverse_statistics()
    new_universe = me.create_branch_universe("API request", 0.5)
    return {
        "statistics": stats,
        "new_universe": new_universe
    }

@module_router.get("/advanced/bci/read")
async def read_neural_signals():
    """Read simulated neural signals"""
    if not ADVANCED_AVAILABLE:
        return {"signals": {}, "interpretation": "resting state"}
    
    bci = BrainComputerInterface()
    signals = bci.read_neural_signals()
    interpretation = bci.interpret_thought(signals)
    return {"signals": signals, "interpretation": interpretation}

@module_router.get("/advanced/consciousness/state")
async def consciousness_state():
    """Get quantum consciousness state"""
    if not ADVANCED_AVAILABLE:
        return {"state": "unknown", "level": 0.5}
    
    qc = QuantumConsciousness()
    obs = qc.quantum_observation({})
    return {"state": obs["observed_state"], "level": obs["consciousness_level"]}

# ==================== MODULES STATUS ====================

@module_router.get("/modules/status")
async def modules_status():
    """Get status of all modules"""
    return {
        "memory": MEMORY_AVAILABLE,
        "emotion": EMOTION_AVAILABLE,
        "knowledge": KNOWLEDGE_AVAILABLE,
        "language": LANGUAGE_AVAILABLE,
        "integrations": INTEGRATIONS_AVAILABLE,
        "quantum": QUANTUM_AVAILABLE,
        "creativity": CREATIVITY_AVAILABLE,
        "autonomy": AUTONOMY_AVAILABLE,
        "ethics": ETHICS_AVAILABLE,
        "advanced": ADVANCED_AVAILABLE
    }

# ==================== SEARCH CONFIGURATION ====================

class SearchConfig:
    def __init__(self):
        # You can get a free API key from serpapi.com
        self.serpapi_key = os.getenv("SERPAPI_KEY", "597a4bb2b90c3b8300faf82e56db5d43207f4adc")
        self.webscrapingapi_key = os.getenv("WEBSCRAPINGAPI_KEY", "")
        self.searchapi_key = os.getenv("SEARCHAPI_KEY", "")
        
    def get_serpapi_url(self, query, num=5):
        return f"https://serpapi.webscrapingapi.com/v2?api_key={self.serpapi_key}&q={query}&engine=duckduckgo&num={num}"
    
    def get_searchapi_url(self, query):
        return f"https://www.searchapi.io/api/v1/search?api_key={self.searchapi_key}&q={query}&engine=duckduckgo"

search_config = SearchConfig()

# ==================== WEB SEARCH ENDPOINT ====================

@module_router.get("/integrations/web/search")
async def web_search(q: str = Query(..., description="Search query"), num: int = 5):
    """Search the web using DuckDuckGo API"""
    try:
        # Try SerpApi first (most reliable)
        if search_config.serpapi_key:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(search_config.get_serpapi_url(q, num))
                
                if response.status_code == 200:
                    data = response.json()
                    results = []
                    
                    # Parse organic results
                    if "organic_results" in data:
                        for item in data["organic_results"][:num]:
                            results.append({
                                "title": item.get("title", ""),
                                "url": item.get("link", ""),
                                "snippet": item.get("snippet", ""),
                                "position": item.get("position", 0)
                            })
                    
                    # Also get answer box if available
                    answer = None
                    if "answer_box" in data:
                        answer = {
                            "title": data["answer_box"].get("title", ""),
                            "answer": data["answer_box"].get("answer", ""),
                            "snippet": data["answer_box"].get("snippet", "")
                        }
                    
                    return {
                        "success": True,
                        "query": q,
                        "results": results,
                        "answer": answer,
                        "total": len(results)
                    }
        
        # Try SearchAPI.io as fallback
        if search_config.searchapi_key:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(search_config.get_searchapi_url(q))
                
                if response.status_code == 200:
                    data = response.json()
                    results = []
                    
                    if "organic_results" in data:
                        for item in data["organic_results"][:num]:
                            results.append({
                                "title": item.get("title", ""),
                                "url": item.get("link", ""),
                                "snippet": item.get("snippet", ""),
                                "position": item.get("position", 0)
                            })
                    
                    return {
                        "success": True,
                        "query": q,
                        "results": results,
                        "total": len(results)
                    }
        
        # If no APIs work, fallback to Wikipedia
        async with httpx.AsyncClient(timeout=10.0) as client:
            wiki_response = await client.get(
                f"https://en.wikipedia.org/api/rest_v1/page/summary/{q.replace(' ', '_')}"
            )
            if wiki_response.status_code == 200:
                wiki_data = wiki_response.json()
                return {
                    "success": True,
                    "query": q,
                    "results": [{
                        "title": wiki_data.get("title", q),
                        "url": wiki_data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                        "snippet": wiki_data.get("extract", ""),
                        "position": 0,
                        "source": "Wikipedia"
                    }],
                    "total": 1
                }
        
        return {
            "success": False,
            "query": q,
            "error": "No search API available",
            "results": []
        }
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return {
            "success": False,
            "query": q,
            "error": str(e),
            "results": []
        }

# ==================== EVOLUTION LAYER ENDPOINTS (Routines 101-120) ====================

# Import Evolution routines
try:
    from core.routines_evolution import (
        EvolutionRoutineManager,
        EvolutionTask,
        create_evolution_task,
        E2TTSVoiceEngine,
        DejaVuDetector,
        MarketScout,
        HardwarePulse,
        SocialGhost,
        RedTeamAnalyzer,
        MemoryDreaming,
        OldFriendProtocol,
        ToolMaker,
        CodeDocumentary,
        ScreenDesaturation,
        CodeSmelling,
        DeepResearchAgent,
        DigitalLegacy
    )
    EVOLUTION_AVAILABLE = True
    logger.info("✅ Evolution layer loaded")
except ImportError as e:
    logger.warning(f"Evolution layer not available: {e}")
    EVOLUTION_AVAILABLE = False

# Evolution task model
class EvolutionTaskRequest(BaseModel):
    behavior_name: str
    routine_number: int
    priority: int
    message: str
    action_type: str

class HardwarePulseRequest(BaseModel):
    gpu_temp: int = 0
    gpu_load: float = 0.0
    fan_speed: int = 0
    disk_temp: int = 0
    disk_cycles: int = 0
    vram_usage: float = 0.0
    cpu_temp: int = 0
    cpu_load: float = 0.0

class RedTeamReportRequest(BaseModel):
    project_name: str
    business_plan: str

class SocialDecayRequest(BaseModel):
    contact_name: str
    last_interaction: str

class MemoryDreamingRequest(BaseModel):
    log_path: str = "backend/logs/memory.jsonl"

class DeepResearchRequest(BaseModel):
    topic: str
    duration_minutes: int = 30

class DigitalLegacyRequest(BaseModel):
    month: str = ""

# Global evolution manager instance
_evolution_manager: Optional[EvolutionRoutineManager] = None

def _init_evolution_manager():
    """Initialize evolution manager on first request"""
    global _evolution_manager
    if _evolution_manager is None:
        _evolution_manager = EvolutionRoutineManager()
        _evolution_manager.start()
        logger.info("[Evolution] Manager initialized and started")

@module_router.get("/evolution/status")
async def evolution_status():
    """Get evolution layer status"""
    if not EVOLUTION_AVAILABLE:
        return {"available": False, "message": "Evolution layer not installed"}
    
    _init_evolution_manager()
    return _evolution_manager.get_status()

@module_router.post("/evolution/task")
async def execute_evolution_task(request: EvolutionTaskRequest):
    """Execute an evolution routine task"""
    if not EVOLUTION_AVAILABLE:
        return {"success": False, "message": "Evolution layer not installed"}
    
    _init_evolution_manager()
    
    task = create_evolution_task(
        behavior_name=request.behavior_name,
        routine_number=request.routine_number,
        priority=request.priority,
        message=request.message,
        action_type=request.action_type
    )
    
    result = _evolution_manager.execute_evolution_task(task)
    return {"success": True, "result": result, "task": task.to_dict()}

@module_router.get("/evolution/hardware-pulse")
async def get_hardware_pulse():
    """Get current hardware pulse data"""
    if not EVOLUTION_AVAILABLE:
        return {"available": False, "pulse": None}
    
    _init_evolution_manager()
    pulse = _evolution_manager.hardware_pulse.get_pulse_data()
    return {
        "available": True,
        "pulse": {
            "gpu_temp": pulse.gpu_temp,
            "gpu_load": pulse.gpu_load,
            "fan_speed": pulse.fan_speed,
            "disk_temp": pulse.disk_temp,
            "vram_usage": pulse.vram_usage,
            "cpu_temp": pulse.cpu_temp,
            "cpu_load": pulse.cpu_load,
            "intensity": _evolution_manager.hardware_pulse.get_pulse_intensity()
        }
    }

@module_router.post("/evolution/red-team")
async def generate_red_team_report(request: RedTeamReportRequest):
    """Generate red team failure report"""
    if not EVOLUTION_AVAILABLE:
        return {"success": False, "message": "Evolution layer not installed"}
    
    _init_evolution_manager()
    report = _evolution_manager.red_team.generate_failure_report(
        project_name=request.project_name,
        business_plan=request.business_plan
    )
    return {
        "success": True,
        "report": {
            "report_id": report.report_id,
            "project_name": report.project_name,
            "failure_reasons": report.failure_reasons,
            "risk_scores": report.risk_scores,
            "recommendations": report.recommendations,
            "severity": report.severity
        }
    }

@module_router.get("/evolution/social-decay")
async def get_social_decay():
    """Get contacts with social decay"""
    if not EVOLUTION_AVAILABLE:
        return {"available": False, "contacts": []}
    
    _init_evolution_manager()
    contacts = _evolution_manager.old_friend.get_decay_contacts()
    return {
        "available": True,
        "contacts": [
            {
                "name": c.contact_name,
                "last_interaction": c.last_interaction,
                "decay_score": c.decay_score,
                "suggested_action": c.suggested_action,
                "meme_suggestions": c.meme_suggestions
            }
            for c in contacts
        ]
    }

@module_router.post("/evolution/social-draft")
async def draft_social_reply(platform: str = "telegram", message: str = "Hello!", tone: str = "friendly"):
    """Draft a social reply"""
    if not EVOLUTION_AVAILABLE:
        return {"success": False, "message": "Evolution layer not installed"}
    
    _init_evolution_manager()
    draft = _evolution_manager.social_ghost.draft_reply(platform, message, tone)
    return {
        "success": True,
        "draft": {
            "platform": draft.platform,
            "original_message": draft.original_message,
            "draft": draft.draft,
            "tone": draft.tone,
            "emoji": draft.emoji,
            "status": draft.status
        }
    }

@module_router.post("/evolution/memory-dream")
async def trigger_memory_dreaming(request: MemoryDreamingRequest):
    """Trigger memory dreaming/compression"""
    if not EVOLUTION_AVAILABLE:
        return {"success": False, "message": "Evolution layer not installed"}
    
    _init_evolution_manager()
    _evolution_manager.memory_dreaming._compress_and_dream()
    memories = _evolution_manager.memory_dreaming.get_core_memories()
    return {
        "success": True,
        "memories_created": len(memories),
        "memories": [m.to_dict() for m in memories[:10]]
    }

@module_router.post("/evolution/deja-vu")
async def check_deja_vu(error_message: str, code_context: str = ""):
    """Check for repeat errors (Déjà Vu)"""
    if not EVOLUTION_AVAILABLE:
        return {"success": False, "message": "Evolution layer not installed"}
    
    _init_evolution_manager()
    result = _evolution_manager.deja_vu.detect_repeat_error(error_message, code_context)
    return {
        "success": True,
        "found": result.get("found", False),
        "occurrence": result.get("occurrence", 1),
        "first_seen": result.get("first_seen"),
        "last_seen": result.get("last_seen"),
        "fix_applied": result.get("fix_applied", False)
    }

@module_router.post("/evolution/market-scout")
async def scout_market_gaps(topics: List[str] = ["AI Agents", "Automation", "LLM"]):
    """Scout market gaps"""
    if not EVOLUTION_AVAILABLE:
        return {"success": False, "message": "Evolution layer not installed"}
    
    _init_evolution_manager()
    gaps = _evolution_manager.market_scout.scout_market_gaps(topics)
    return {
        "success": True,
        "gaps": gaps,
        "trending_products": _evolution_manager.market_scout.get_trending_products()
    }

@module_router.post("/evolution/deep-research")
async def conduct_deep_research(request: DeepResearchRequest):
    """Conduct deep research on a topic"""
    if not EVOLUTION_AVAILABLE:
        return {"success": False, "message": "Evolution layer not installed"}
    
    _init_evolution_manager()
    result = _evolution_manager.deep_research.conduct_research(
        topic=request.topic,
        duration_minutes=request.duration_minutes
    )
    return {
        "success": True,
        "research": {
            "topic": result["topic"],
            "duration_minutes": result["duration_minutes"],
            "findings": result["findings"],
            "sources": result["sources"],
            "summary": result["summary"]
        }
    }

@module_router.post("/evolution/digital-legacy")
async def generate_digital_legacy(request: DigitalLegacyRequest):
    """Generate monthly digital legacy letter"""
    if not EVOLUTION_AVAILABLE:
        return {"success": False, "message": "Evolution layer not installed"}
    
    _init_evolution_manager()
    letter = _evolution_manager.digital_legacy.generate_monthly_letter()
    return {
        "success": True,
        "letter": {
            "month": letter["month"],
            "lessons_learned": letter["lessons_learned"],
            "achievements": letter["achievements"],
            "areas_for_improvement": letter["areas_for_improvement"],
            "reflection": letter["reflection"]
        }
    }

@module_router.get("/evolution/tool-maker/list")
async def list_created_tools():
    """List all tools created by Tool Maker"""
    if not EVOLUTION_AVAILABLE:
        return {"available": False, "tools": []}
    
    _init_evolution_manager()
    tools = _evolution_manager.tool_maker.list_tools()
    return {
        "available": True,
        "tools": tools
    }

@module_router.post("/evolution/tool-maker/create")
async def create_tool(request: dict):
    """Create a new tool"""
    if not EVOLUTION_AVAILABLE:
        return {"success": False, "message": "Evolution layer not installed"}
    
    _init_evolution_manager()
    request_text = request.get("request", "")
    tool_info = _evolution_manager.tool_maker.create_tool(request_text)
    return {
        "success": True,
        "tool": tool_info
    }

@module_router.get("/evolution/code-smell")
async def analyze_code_smells(file_path: str = "backend/core/kernel.py"):
    """Analyze code for smells"""
    if not EVOLUTION_AVAILABLE:
        return {"available": False, "smells": []}
    
    _init_evolution_manager()
    smells = _evolution_manager.code_smelling.analyze_file(file_path)
    return {
        "available": True,
        "file": file_path,
        "smells": smells
    }

@module_router.get("/evolution/code-documentary")
async def generate_documentary(project_path: str = "backend"):
    """Generate code documentary"""
    if not EVOLUTION_AVAILABLE:
        return {"available": False, "documentary": None}
    
    _init_evolution_manager()
    documentary = _evolution_manager.code_documentary.generate_documentary(project_path)
    return {
        "available": True,
        "documentary": {
            "title": documentary["title"],
            "commits_count": documentary["commits_count"],
            "script": documentary["script"]
        }
    }

@module_router.get("/evolution/screen-desaturation")
async def get_screen_desaturation_status():
    """Get screen desaturation status"""
    if not EVOLUTION_AVAILABLE:
        return {"available": False, "status": None}
    
    _init_evolution_manager()
    status = _evolution_manager.screen_desaturation.get_status()
    return {
        "available": True,
        "status": status
    }

@module_router.post("/evolution/screen-desaturation/apply")
async def apply_desaturation():
    """Apply screen desaturation"""
    if not EVOLUTION_AVAILABLE:
        return {"success": False, "message": "Evolution layer not installed"}
    
    _init_evolution_manager()
    _evolution_manager.screen_desaturation.apply_desaturation()
    return {"success": True, "message": "Desaturation applied"}

@module_router.post("/evolution/screen-desaturation/remove")
async def remove_desaturation():
    """Remove screen desaturation"""
    if not EVOLUTION_AVAILABLE:
        return {"success": False, "message": "Evolution layer not installed"}
    
    _init_evolution_manager()
    _evolution_manager.screen_desaturation.remove_desaturation()
    return {"success": True, "message": "Desaturation removed"}

@module_router.post("/evolution/voice/synthesize")
async def synthesize_voice(text: str, emotion: str = "neutral", speed: float = 1.0, pitch: float = 1.0):
    """Synthesize voice with E2-TTS"""
    if not EVOLUTION_AVAILABLE:
        return {"success": False, "message": "Evolution layer not installed"}
    
    _init_evolution_manager()
    engine = E2TTSVoiceEngine()
    audio = engine.synthesize(text, emotion, speed, pitch)
    return {
        "success": True,
        "audio_data": audio.decode() if isinstance(audio, bytes) else audio,
        "emotion": emotion,
        "speed": speed,
        "pitch": pitch
    }

@module_router.post("/evolution/voice/emotion")
async def set_voice_emotion(emotion: str):
    """Set voice emotion"""
    if not EVOLUTION_AVAILABLE:
        return {"success": False, "message": "Evolution layer not installed"}
    
    _init_evolution_manager()
    _evolution_manager.voice_engine.set_emotion(emotion)
    return {"success": True, "emotion": emotion}

@module_router.get("/evolution/memory/letters")
async def get_digital_legacy_letters():
    """Get all digital legacy letters"""
    if not EVOLUTION_AVAILABLE:
        return {"available": False, "letters": []}
    
    _init_evolution_manager()
    letters = _evolution_manager.digital_legacy.get_letters()
    return {
        "available": True,
        "letters": letters
    }

@module_router.get("/evolution/memory/core")
async def get_core_memories():
    """Get core memories"""
    if not EVOLUTION_AVAILABLE:
        return {"available": False, "memories": []}
    
    _init_evolution_manager()
    memories = _evolution_manager.memory_dreaming.get_core_memories()
    return {
        "available": True,
        "memories": [m.to_dict() for m in memories]
    }

@module_router.get("/evolution/voice/cache")
async def get_voice_cache():
    """Get voice cache status"""
    if not EVOLUTION_AVAILABLE:
        return {"available": False, "cache_size": 0}
    
    _init_evolution_manager()
    cache_size = len(_evolution_manager.voice_engine._voice_cache)
    return {
        "available": True,
        "cache_size": cache_size
    }

@module_router.post("/evolution/voice/cache/clear")
async def clear_voice_cache():
    """Clear voice cache"""
    if not EVOLUTION_AVAILABLE:
        return {"success": False, "message": "Evolution layer not installed"}
    
    _init_evolution_manager()
    _evolution_manager.voice_engine.clear_cache()
    return {"success": True, "message": "Voice cache cleared"}
