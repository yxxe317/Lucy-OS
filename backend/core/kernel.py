from fastapi import FastAPI, HTTPException, UploadFile, File, Header, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import asyncio
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from core.memory import memory
from core.llm import llm
from core.emotion import emotion
from core.autonomy import autonomy, heartbeat
from core.vector_memory import vector_memory
from core.personality import personality
from core.plugins import plugin_manager
from core.users import users
from core.auth import auth
from plugins.filesystem import filesystem
from plugins.voice import voice
#from plugins.vision import vision
#from plugins.live_stream import live_stream
from plugins.web import web
from core.code_executor import code_executor
from plugins.cyber_security import cyber_security
from plugins.security_analytics import security_analytics
from plugins.secure_dev import secure_dev
from plugins.soc_simulation import soc_simulation
from core.quantum_intelligence import quantum
from core.biological_integration import biological
from core.reality_manipulation import reality
from core.transcendent_ai import transcendent
from core.evolution import evolution
from core.memory_advanced import advanced_memory
from core.consciousness import consciousness
from core.world_builder import world_builder
from core.proactive import proactive_assistant
from core.vram_manager import vram_manager
from core.reasoning import reasoning_engine
from core.settings_routes import router as settings_router
from core.autonomy import BIOMETRIC_ENABLED
import httpx
from fastapi import HTTPException
import time
from fastapi import HTTPException, status
# ===== NEW MODULE IMPORTS - DO NOT REMOVE =====
from core.api_router import module_router
# ===== SECURITY MODULE IMPORTS - DO NOT REMOVE =====
from api.security import (
    train_biometric_model,
    verify_typing_rhythm,
    trigger_lockdown,
    get_security_status
)
# ===============================================

OPENSKY_URL = "https://opensky-network.org/api/states/all"

# ═══════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "kernel.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("LucyKernel")

app = FastAPI(title="LUCY OS", version="21.0.0")

# ===== NEW MODULE ROUTER - DO NOT REMOVE =====
app.include_router(module_router)
# Include settings routes for master config and VRAM management
app.include_router(settings_router)
# ==============================================

# Update CORS for audio and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://192.168.1.2:5173",
        "http://192.168.1.2:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversation_history: Dict[int, List[Dict]] = {}

@app.on_event("startup")
async def startup():
    await memory.init_db()
    logger.info("🧠 Lucy OS v21.0 Online - All Systems Ready")
    asyncio.create_task(autonomy.start_thought_loop())
    
    # Start autonomous heartbeat system
    try:
        await heartbeat.start()
        logger.info("💓 Autonomous Heartbeat System Started")
        
        # Register reasoning engine with proactive system
        from core.proactive import proactive_assistant
        proactive_assistant.reasoning_engine = reasoning_engine
        logger.info("🧠 Reasoning Tree integrated with Proactive System")
    except Exception as e:
        logger.error(f"Failed to start heartbeat: {e}")

@app.get("/health")
async def health():
    return {
        "status": "OK",
        "version": "21.0",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "active_sessions": len(auth.sessions)
    }

@app.get("/health/autonomous")
async def get_autonomous_health():
    """Get autonomous heartbeat system health status"""
    try:
        return heartbeat.get_health_status()
    except Exception as e:
        logger.error(f"Autonomous health check error: {e}")
        return {"error": str(e)}

@app.get("/proactive/tasks")
async def get_proactive_tasks():
    """Get available proactive tasks"""
    try:
        return heartbeat.get_proactive_tasks()
    except Exception as e:
        logger.error(f"Get proactive tasks error: {e}")
        return {"error": str(e)}

flight_cache = {
    "data": None,
    "timestamp": 0,
    "cache_duration": 60  # seconds
}

# Replace your existing /api/flights endpoint with this:
@app.get("/api/flights")
async def get_flights():
    """Proxy for OpenSky API with caching to handle rate limits"""
    try:
        # Check if we have recent cached data
        current_time = time.time()
        if flight_cache["data"] and (current_time - flight_cache["timestamp"] < flight_cache["cache_duration"]):
            logger.info("✅ Returning cached flight data")
            return flight_cache["data"]
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(OPENSKY_URL)
            
            if response.status_code == 200:
                data = response.json()
                # Update cache
                flight_cache["data"] = data
                flight_cache["timestamp"] = current_time
                logger.info(f"✅ Fetched {len(data.get('states', []))} flights from OpenSky")
                return data
                
            elif response.status_code == 429:
                # Rate limited - return cached data if available
                if flight_cache["data"]:
                    logger.warning("⚠️ OpenSky rate limited - returning cached data")
                    return flight_cache["data"]
                else:
                    # No cache, return empty response with rate limit info
                    logger.error("❌ OpenSky rate limited and no cache available")
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="OpenSky API rate limit exceeded. Please try again later."
                    )
            else:
                logger.error(f"❌ OpenSky API error: {response.status_code}")
                # Return cached data if available, otherwise error
                if flight_cache["data"]:
                    logger.warning("⚠️ Using cached flight data due to API error")
                    return flight_cache["data"]
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"OpenSky API returned {response.status_code}"
                )
                
    except httpx.TimeoutException:
        logger.error("❌ OpenSky API timeout")
        if flight_cache["data"]:
            logger.warning("⚠️ Using cached flight data due to timeout")
            return flight_cache["data"]
        raise HTTPException(status_code=504, detail="OpenSky API timeout")
        
    except Exception as e:
        logger.error(f"❌ Flight proxy error: {e}")
        if flight_cache["data"]:
            logger.warning("⚠️ Using cached flight data due to error")
            return flight_cache["data"]
        raise HTTPException(status_code=500, detail=str(e))

# ═══════════════════════════════════════════════════════════════
# AUTH ENDPOINTS
# ═══════════════════════════════════════════════════════════════
class RegisterRequest(BaseModel):
    username: str
    password: Optional[str] = None

@app.post("/auth/register")
async def register(request: RegisterRequest):
    result = users.create_user(request.username, request.password)
    if result.get("success"):
        token = auth.create_session(result["user_id"], result["username"])
        logger.info(f"✅ User registered: {result['username']}")
        return {
            "success": True,
            "token": token,
            "user_id": result["user_id"],
            "username": result["username"]
        }
    return result

@app.post("/users/login")
async def users_login(request: RegisterRequest):
    result = users.authenticate(request.username, request.password)
    if result.get("success"):
        token = auth.create_session(result["user_id"], result["username"])
        logger.info(f"✅ User logged in: {result['username']}")
        return {
            "success": True,
            "token": token,
            "user_id": result["user_id"],
            "username": result["username"]
        }
    return result

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/auth/login")
async def login(request: LoginRequest):
    result = users.authenticate(request.username, request.password)
    if result.get("success"):
        token = auth.create_session(result["user_id"], result["username"])
        logger.info(f"✅ User authenticated: {result['username']}")
        return {
            "success": True,
            "token": token,
            "user_id": result["user_id"],
            "username": result["username"]
        }
    return result

@app.post("/auth/logout")
async def logout(authorization: Optional[str] = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:].strip()
        success = auth.end_session(token)
        logger.info("✅ Session ended")
        return {"success": success}
    return {"success": False, "error": "No token"}

@app.get("/auth/me")
async def get_current_user(authorization: Optional[str] = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:].strip()
        user = auth.validate_session(token)
        if user:
            full_user = users.get_user(user["username"])
            return full_user
    return {"success": False, "error": "Not authenticated"}

@app.get("/users/list")
async def list_users():
    return {"users": users.get_all_users()}

def get_user_from_token(auth_header: str) -> Optional[Dict]:
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.warning(f"⚠️ Invalid auth header")
        return None
    token = auth_header[7:].strip()
    return auth.validate_session(token)

# ═══════════════════════════════════════════════════════════════
# USER PROFILE ENDPOINTS
# ═══════════════════════════════════════════════════════════════
@app.get("/users/profile")
async def get_user_profile(request: Request):
    auth_header = request.headers.get("Authorization", "")
    user = get_user_from_token(auth_header)
    if not user:
        return {"success": False, "message": "Invalid token"}
    return {
        "success": True,
        "profile": {
            "username": user.get("username", "User"),
            "email": "user@example.com",
            "bio": "Lucy OS user",
            "interests": ["AI", "Technology", "Learning"]
        }
    }

@app.post("/users/profile")
async def update_user_profile(request: Request):
    auth_header = request.headers.get("Authorization", "")
    user = get_user_from_token(auth_header)
    if not user:
        return {"success": False, "message": "Invalid token"}
    try:
        body = await request.json()
        username = body.get("username", "")
        logger.info(f"✅ Profile update requested for user {user.get('user_id')}")
        return {"success": True, "message": "Profile updated"}
    except Exception as e:
        logger.error(f"Profile update error: {e}")
        return {"success": False, "message": str(e)}

# ═══════════════════════════════════════════════════════════════
# QUERY ENDPOINTS
# ═══════════════════════════════════════════════════════════════
class QueryRequest(BaseModel):
    query: str
    research_mode: bool = False
    deep_research: bool = False

@app.post("/query")
async def handle_query(request: QueryRequest, authorization: Optional[str] = Header(None)):
    user_id = 1
    username = "Guest"
    
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:].strip()
        user = auth.validate_session(token)
        if user:
            user_id = user["user_id"]
            username = user["username"]
    
    try:
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        logger.info(f"📝 Query from {username}: {request.query[:50]}...")
        
        from core.humor import humor
        user_emotion = humor.detect_emotion_from_text(request.query)
        
        system_prompt = personality.get_personality_prompt()
        system_prompt += f"\n\n[CURRENT DATE: {current_date}]"
        
        sources_found = 0
        if request.deep_research or request.research_mode:
            num = 100 if request.deep_research else 25
            research = await web.deep_research(request.query, num)
            if research.get('success'):
                system_prompt += f"\n\n[RESEARCH:\n{research['summary']}]"
                sources_found = research.get('sources_found', 0)
        
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        response_text = await llm.generate(
            request.query, 
            system_prompt,
            user_id=user_id,
            emotion=user_emotion
        )
        
        conversation_history[user_id].append({"role": "user", "content": request.query})
        conversation_history[user_id].append({"role": "assistant", "content": response_text})
        users.save_conversation(user_id, "user", request.query)
        users.save_conversation(user_id, "assistant", response_text)
        
        spoke = False
        try:
            result = await voice.speak(response_text)
            spoke = result.get('status') == 'ready'
        except Exception as e:
            logger.error(f"Voice error: {e}")
        
        return {
            "query": request.query,
            "response": response_text,
            "research_mode": request.research_mode or request.deep_research,
            "sources_found": sources_found,
            "auto_spoke": spoke,
            "current_date": current_date,
            "user": username
        }
    except Exception as e:
        logger.error(f"Query error: {e}")
        return {"query": request.query, "response": f"Error: {str(e)}", "auto_spoke": False}

@app.post("/query/stream")
async def handle_query_stream(request: QueryRequest, authorization: Optional[str] = Header(None)):
    user_id = 1
    username = "Guest"
    
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:].strip()
        user = auth.validate_session(token)
        if user:
            user_id = user["user_id"]
            username = user["username"]
    
    async def generate():
        try:
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            logger.info(f"📝 Streaming query from {username}: {request.query[:50]}...")
            
            from core.humor import humor
            user_emotion = humor.detect_emotion_from_text(request.query)
            
            system_prompt = personality.get_personality_prompt()
            system_prompt += f"\n\n[CURRENT DATE: {current_date}]"
            
            sources_found = 0
            if request.deep_research or request.research_mode:
                num = 100 if request.deep_research else 25
                research = await web.deep_research(request.query, num)
                if research.get('success'):
                    system_prompt += f"\n\n[RESEARCH:\n{research['summary']}]"
                    sources_found = research.get('sources_found', 0)
            
            yield json.dumps({
                "type": "meta",
                "user": username,
                "emotion": user_emotion,
                "sources_found": sources_found
            }) + "\n"
            
            full_response = ""
            async for chunk in llm.generate_stream(request.query, system_prompt, user_id, user_emotion):
                full_response += chunk
                yield json.dumps({"type": "chunk", "content": chunk}) + "\n"
            
            if user_id not in conversation_history:
                conversation_history[user_id] = []
            conversation_history[user_id].append({"role": "user", "content": request.query})
            conversation_history[user_id].append({"role": "assistant", "content": full_response})
            users.save_conversation(user_id, "user", request.query)
            users.save_conversation(user_id, "assistant", full_response)
            
            audio_file = None
            try:
                speak_result = await voice.speak(full_response)
                if speak_result.get('status') == 'ready' and speak_result.get('file'):
                    audio_file = speak_result['file']
                    logger.info(f"✅ Audio generated: {audio_file}")
            except Exception as e:
                logger.error(f"Voice error: {e}")
            
            yield json.dumps({
                "type": "complete",
                "full_response": full_response,
                "audio_file": audio_file
            }) + "\n"
            
        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield json.dumps({"type": "error", "error": str(e)}) + "\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

# ═══════════════════════════════════════════════════════════════
# VOICE ENDPOINTS - FIXED FOR CORS
# ═══════════════════════════════════════════════════════════════
class SpeakRequest(BaseModel):
    text: str

@app.post("/voice/speak")
async def speak_endpoint(request: SpeakRequest):
    result = await voice.speak(request.text)
    return result

@app.get("/voice/audio/{filename}")
@app.head("/voice/audio/{filename}")
async def get_audio(filename: str):
    """Get audio file with proper CORS headers"""
    from urllib.parse import unquote
    filename = unquote(filename)
    filepath = Path(__file__).parent.parent / "temp_audio" / filename
    
    if not filepath.exists():
        logger.error(f"❌ Audio file not found: {filepath}")
        raise HTTPException(404, f"Audio file not found: {filename}")
    
    # Determine the origin from the request
    origin = "http://localhost:5173"  # default
    # You could also dynamically set based on request.headers.get("origin")
    
    return FileResponse(
        filepath, 
        media_type="audio/mpeg",
        headers={
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.options("/voice/audio/{filename}")
async def audio_options(filename: str):
    return Response(
        content="",
        media_type="application/json",
        headers={
            "Access-Control-Allow-Origin": "http://localhost:5173",
            "Access-Control-Allow-Origin": "https://lucy-os.vercel.app",
            "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "3600"
        }
    )

# ═══════════════════════════════════════════════════════════════
# CONVERSATION HISTORY
# ═══════════════════════════════════════════════════════════════
@app.get("/conversations")
async def get_conversations(authorization: Optional[str] = Header(None), limit: int = 50):
    if not authorization or not authorization.startswith("Bearer "):
        return {"error": "Not authenticated"}
    
    token = authorization[7:].strip()
    user = auth.validate_session(token)
    if not user:
        return {"error": "Invalid token"}
    
    try:
        conn = sqlite3.connect("data/users.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT role, content, timestamp FROM conversations 
            WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?
        ''', (user["user_id"], limit))
        
        conversations = [{"role": r[0], "content": r[1], "timestamp": r[2]} for r in cursor.fetchall()]
        conn.close()
        return {"conversations": conversations}
    except Exception as e:
        logger.error(f"Error fetching conversations: {e}")
        return {"conversations": []}

# ═══════════════════════════════════════════════════════════════
# EVOLUTION ENDPOINTS
# ═══════════════════════════════════════════════════════════════
@app.get("/evolution/stats")
async def get_evolution_stats():
    conn = sqlite3.connect("data/evolution.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM success_metrics")
    total_interactions = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM prompt_variants")
    total_variants = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM long_term_goals WHERE status = 'active'")
    active_goals = cursor.fetchone()[0]
    
    conn.close()
    return {
        "total_interactions": total_interactions,
        "prompt_variants": total_variants,
        "active_goals": active_goals,
        "evolution_ready": total_interactions > 100
    }

@app.post("/evolution/goals")
async def create_goal(request: Request):
    body = await request.json()
    goal = body.get("goal")
    priority = body.get("priority", 5)
    target_days = body.get("target_days", 30)
    
    if not goal:
        return {"error": "Goal text required"}
    
    conn = sqlite3.connect("data/evolution.db")
    cursor = conn.cursor()
    target_date = (datetime.now() + timedelta(days=target_days)).isoformat()
    
    cursor.execute('''
        INSERT INTO long_term_goals (goal_text, priority, progress, created_at, target_date, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (goal, priority, 0.0, datetime.now().isoformat(), target_date, "active"))
    
    goal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"success": True, "goal_id": goal_id}

@app.get("/evolution/goals")
async def get_goals():
    conn = sqlite3.connect("data/evolution.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, goal_text, priority, progress, created_at, target_date
        FROM long_term_goals WHERE status = 'active'
    ''')
    
    goals = [{
        "id": r[0], "goal": r[1], "priority": r[2],
        "progress": r[3], "created": r[4], "target": r[5]
    } for r in cursor.fetchall()]
    
    conn.close()
    return {"goals": goals}

@app.post("/evolution/evolve")
async def trigger_evolution():
    result = await evolution.evolve_prompts()
    return {"success": True, "new_variants": len(result)}

@app.post("/feedback")
async def submit_feedback(request: Request):
    body = await request.json()
    response_id = body.get("response_id")
    feedback = body.get("feedback")
    await llm.learn_from_feedback(response_id, feedback)
    return {"success": True}

# ═══════════════════════════════════════════════════════════════
# EVOLUTION ROUTINES ENDPOINTS (101-120)
# ═══════════════════════════════════════════════════════════════
from core.routines_evolution import (
    EvolutionRoutineManager,
    create_evolution_task,
    EvolutionTask
)

_evolution_manager = EvolutionRoutineManager()

@app.get("/evolution/routines/status")
async def get_evolution_routines_status():
    """Get evolution layer status"""
    try:
        return _evolution_manager.get_status()
    except Exception as e:
        logger.error(f"Evolution status error: {e}")
        return {"error": str(e)}

@app.post("/evolution/routines/start")
async def start_evolution_routines():
    """Start evolution layer routines"""
    try:
        _evolution_manager.start()
        return {"success": True, "message": "Evolution layer started"}
    except Exception as e:
        logger.error(f"Start evolution error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/evolution/routines/stop")
async def stop_evolution_routines():
    """Stop evolution layer routines"""
    try:
        _evolution_manager.stop()
        return {"success": True, "message": "Evolution layer stopped"}
    except Exception as e:
        logger.error(f"Stop evolution error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/evolution/routines/execute")
async def execute_evolution_routine(request: Request):
    """Execute a specific evolution routine"""
    try:
        body = await request.json()
        routine_number = body.get("routine_number")
        message = body.get("message", "")
        action_type = body.get("action_type", "")
        priority = body.get("priority", 5)
        metadata = body.get("metadata", {})
        
        task = create_evolution_task(
            behavior_name=f"Routine_{routine_number}",
            routine_number=routine_number,
            priority=priority,
            message=message,
            action_type=action_type,
            metadata=metadata
        )
        
        result = _evolution_manager.execute_evolution_task(task)
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"Execute evolution routine error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/pulse")
async def get_hardware_pulse():
    """Get hardware pulse data for UI breathing animation"""
    try:
        pulse_data = _evolution_manager.hardware_pulse.get_pulse_data()
        return {
            "success": True,
            "pulse": {
                "gpu_temp": pulse_data.gpu_temp,
                "gpu_load": pulse_data.gpu_load,
                "fan_speed": pulse_data.fan_speed,
                "disk_temp": pulse_data.disk_temp,
                "disk_cycles": pulse_data.disk_cycles,
                "vram_usage": pulse_data.vram_usage,
                "cpu_temp": pulse_data.cpu_temp,
                "cpu_load": pulse_data.cpu_load
            },
            "intensity": _evolution_manager.hardware_pulse.get_pulse_intensity()
        }
    except Exception as e:
        logger.error(f"Get pulse error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/red-team/reports")
async def get_red_team_reports():
    """Get all red team failure reports"""
    try:
        reports = _evolution_manager.red_team.get_reports()
        return {
            "success": True,
            "reports": [
                {
                    "report_id": r.report_id,
                    "project_name": r.project_name,
                    "failure_reasons": r.failure_reasons,
                    "risk_scores": r.risk_scores,
                    "recommendations": r.recommendations,
                    "severity": r.severity,
                    "timestamp": r.timestamp
                }
                for r in reports
            ]
        }
    except Exception as e:
        logger.error(f"Get red team reports error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/evolution/red-team/analyze")
async def analyze_with_red_team(request: Request):
    """Generate a red team failure report for a business plan"""
    try:
        body = await request.json()
        project_name = body.get("project_name", "")
        business_plan = body.get("business_plan", "")
        
        report = _evolution_manager.red_team.generate_failure_report(project_name, business_plan)
        return {
            "success": True,
            "report": {
                "report_id": report.report_id,
                "project_name": report.project_name,
                "failure_reasons": report.failure_reasons,
                "risk_scores": report.risk_scores,
                "recommendations": report.recommendations,
                "severity": report.severity,
                "timestamp": report.timestamp
            }
        }
    except Exception as e:
        logger.error(f"Red team analysis error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/core-memories")
async def get_core_memories():
    """Get compressed core memories from Memory Dreaming"""
    try:
        memories = _evolution_manager.memory_dreaming.get_core_memories()
        return {
            "success": True,
            "memories": [
                {
                    "memory_id": m.memory_id,
                    "type": m.type,
                    "content": m.content,
                    "timestamp": m.timestamp,
                    "confidence": m.confidence,
                    "tags": m.tags
                }
                for m in memories
            ]
        }
    except Exception as e:
        logger.error(f"Get core memories error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/social/decay")
async def get_social_decay_contacts():
    """Get contacts with social decay for outreach suggestions"""
    try:
        contacts = _evolution_manager.old_friend.get_decay_contacts()
        return {
            "success": True,
            "contacts": [
                {
                    "contact_name": c.contact_name,
                    "last_interaction": c.last_interaction,
                    "decay_score": c.decay_score,
                    "suggested_action": c.suggested_action,
                    "meme_suggestions": c.meme_suggestions
                }
                for c in contacts
            ]
        }
    except Exception as e:
        logger.error(f"Get social decay error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/tools/list")
async def list_created_tools():
    """List all tools created by Tool-Maker"""
    try:
        tools = _evolution_manager.tool_maker.list_tools()
        return {
            "success": True,
            "tools": [
                {
                    "name": t["name"],
                    "request": t["request"],
                    "path": t["path"],
                    "shortcut": t["shortcut"],
                    "created_at": t["created_at"],
                    "status": t["status"]
                }
                for t in tools
            ]
        }
    except Exception as e:
        logger.error(f"List tools error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/evolution/tools/create")
async def create_tool(request: Request):
    """Autonomously create a new Python tool"""
    try:
        body = await request.json()
        request_desc = body.get("request", "")
        
        tool_info = _evolution_manager.tool_maker.create_tool(request_desc)
        return {
            "success": True,
            "tool": {
                "name": tool_info["name"],
                "request": tool_info["request"],
                "path": tool_info["path"],
                "shortcut": tool_info["shortcut"],
                "created_at": tool_info["created_at"],
                "status": tool_info["status"]
            }
        }
    except Exception as e:
        logger.error(f"Create tool error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/personality/traits")
async def get_personality_traits():
    """Get current personality traits adjusted by Laughter Learning"""
    try:
        traits = _evolution_manager.laughter_learning.get_personality_traits()
        return {
            "success": True,
            "traits": traits
        }
    except Exception as e:
        logger.error(f"Get personality traits error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/biometric/data")
async def get_biometric_data():
    """Get rPPG heart rate and biometric data"""
    try:
        data = _evolution_manager.rppg_heart_rate.monitor()
        return {
            "success": True,
            "biometric": {
                "heart_rate": data.heart_rate,
                "blink_rate": data.blink_rate,
                "stress_level": data.stress_level,
                "timestamp": data.timestamp
            }
        }
    except Exception as e:
        logger.error(f"Get biometric data error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/research/results")
async def get_research_results():
    """Get deep research results"""
    try:
        results = _evolution_manager.deep_research.get_results()
        return {
            "success": True,
            "results": [
                {
                    "topic": r["topic"],
                    "duration_minutes": r["duration_minutes"],
                    "status": r["status"],
                    "findings": r["findings"],
                    "sources": r["sources"],
                    "summary": r["summary"]
                }
                for r in results
            ]
        }
    except Exception as e:
        logger.error(f"Get research results error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/evolution/research/conduct")
async def conduct_research(request: Request):
    """Conduct deep research on a topic"""
    try:
        body = await request.json()
        topic = body.get("topic", "")
        duration = body.get("duration_minutes", 30)
        
        result = _evolution_manager.deep_research.conduct_research(topic, duration)
        return {
            "success": True,
            "research": result
        }
    except Exception as e:
        logger.error(f"Conduct research error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/digital-legacy/letters")
async def get_digital_legacy_letters():
    """Get monthly self-reflection letters from Digital Legacy"""
    try:
        letters = _evolution_manager.digital_legacy.get_letters()
        return {
            "success": True,
            "letters": [
                {
                    "month": l["month"],
                    "generated_at": l["generated_at"],
                    "lessons_learned": l["lessons_learned"],
                    "achievements": l["achievements"],
                    "areas_for_improvement": l["areas_for_improvement"],
                    "reflection": l["reflection"]
                }
                for l in letters
            ]
        }
    except Exception as e:
        logger.error(f"Get digital legacy letters error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/evolution/reward")
async def update_reward_score(request: Request):
    """Update reward score for a task (increases priority)"""
    try:
        body = await request.json()
        task_id = body.get("task_id", "")
        reward = body.get("reward", 0.0)
        
        _evolution_manager.update_reward_score(task_id, reward)
        return {"success": True, "message": f"Reward {reward} applied to task {task_id}"}
    except Exception as e:
        logger.error(f"Update reward error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/screen/desaturation")
async def get_screen_desaturation_status():
    """Get screen desaturation status for focus mode"""
    try:
        status = _evolution_manager.screen_desaturation.get_status()
        return {
            "success": True,
            "status": status
        }
    except Exception as e:
        logger.error(f"Get desaturation status error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/evolution/screen/desaturate")
async def apply_screen_desaturation():
    """Apply screen desaturation for focus mode"""
    try:
        _evolution_manager.screen_desaturation.apply_desaturation()
        return {"success": True, "message": "Screen desaturation applied"}
    except Exception as e:
        logger.error(f"Apply desaturation error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/evolution/screen/desaturate/remove")
async def remove_screen_desaturation():
    """Remove screen desaturation"""
    try:
        _evolution_manager.screen_desaturation.remove_desaturation()
        return {"success": True, "message": "Screen desaturation removed"}
    except Exception as e:
        logger.error(f"Remove desaturation error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/code-smelling/smells")
async def get_code_smells():
    """Get detected code smells from Code Smelling analysis"""
    try:
        smells = _evolution_manager.code_smelling.smells
        return {
            "success": True,
            "smells": smells
        }
    except Exception as e:
        logger.error(f"Get code smells error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/evolution/code-smelling/analyze")
async def analyze_code_smells(request: Request):
    """Analyze a file for code smells"""
    try:
        body = await request.json()
        file_path = body.get("file_path", "")
        
        smells = _evolution_manager.code_smelling.analyze_file(file_path)
        return {
            "success": True,
            "smells": smells
        }
    except Exception as e:
        logger.error(f"Analyze code smells error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/vram/parking")
async def get_vram_parking_status():
    """Get VRAM parking status"""
    try:
        return {
            "success": True,
            "status": "ready",
            "threshold": _evolution_manager.vram_parking._parking_threshold,
            "advance_time": _evolution_manager.vram_parking._advance_time
        }
    except Exception as e:
        logger.error(f"Get VRAM parking status error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/evolution/vram/park")
async def park_vram(request: Request):
    """Park VRAM before heavy app launch"""
    try:
        body = await request.json()
        predicted_app = body.get("predicted_app", "")
        
        success = _evolution_manager.vram_parking.park_vram(predicted_app)
        return {
            "success": success,
            "message": "VRAM parked" if success else "VRAM parking failed"
        }
    except Exception as e:
        logger.error(f"Park VRAM error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/mood/lighting")
async def get_mood_lighting_status():
    """Get mood lighting status"""
    try:
        return {
            "success": True,
            "current_mood": _evolution_manager.mood_lighting._current_mood,
            "light_colors": _evolution_manager.mood_lighting._light_colors
        }
    except Exception as e:
        logger.error(f"Get mood lighting status error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/evolution/mood/lighting/set")
async def set_mood_lighting(request: Request):
    """Set mood lighting color"""
    try:
        body = await request.json()
        mood = body.get("mood", "neutral")
        
        color = _evolution_manager.mood_lighting.set_light_mood(mood)
        return {
            "success": True,
            "mood": mood,
            "color_rgb": list(color)
        }
    except Exception as e:
        logger.error(f"Set mood lighting error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/adaptive/whisper")
async def get_adaptive_whisper_status():
    """Get adaptive whisper status"""
    try:
        noise_level = _evolution_manager.adaptive_whisper.detect_ambient_noise()
        settings = _evolution_manager.adaptive_whisper.adjust_voice(noise_level)
        return {
            "success": True,
            "noise_level": noise_level,
            "settings": settings
        }
    except Exception as e:
        logger.error(f"Get adaptive whisper status error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/deja-vu/history")
async def get_deja_vu_history():
    """Get repeat error detection history"""
    try:
        history = _evolution_manager.deja_vu.error_history
        return {
            "success": True,
            "history": [
                {
                    "signature": e["signature"],
                    "message": e["message"],
                    "code_context": e["code_context"],
                    "timestamp": e["timestamp"],
                    "fix_applied": e["fix_applied"]
                }
                for e in history
            ]
        }
    except Exception as e:
        logger.error(f"Get déjà vu history error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/market/gaps")
async def get_market_gaps():
    """Get market gap analysis from B2B Market Scout"""
    try:
        gaps = _evolution_manager.market_scout.gaps_found
        return {
            "success": True,
            "gaps": gaps
        }
    except Exception as e:
        logger.error(f"Get market gaps error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/evolution/social/draft")
async def draft_social_reply(request: Request):
    """Draft a social media reply"""
    try:
        body = await request.json()
        platform = body.get("platform", "telegram")
        message = body.get("message", "")
        tone = body.get("tone", "friendly")
        
        draft = _evolution_manager.social_ghost.draft_reply(platform, message, tone)
        return {
            "success": True,
            "draft": draft
        }
    except Exception as e:
        logger.error(f"Draft social reply error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/evolution/social/draft/approve")
async def approve_social_draft(request: Request):
    """Approve a drafted social media reply"""
    try:
        body = await request.json()
        draft_id = body.get("draft_id", "")
        
        success = _evolution_manager.social_ghost.approve_draft(draft_id)
        return {
            "success": success,
            "message": "Draft approved" if success else "Draft not found"
        }
    except Exception as e:
        logger.error(f"Approve draft error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/evolution/memory/dream")
async def trigger_memory_dreaming():
    """Manually trigger memory compression and dreaming"""
    try:
        _evolution_manager.memory_dreaming._compress_and_dream()
        return {
            "success": True,
            "message": "Memory dreaming completed"
        }
    except Exception as e:
        logger.error(f"Trigger memory dreaming error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/evolution/legacy")
async def get_evolution_legacy():
    """Get complete evolution layer legacy data"""
    try:
        return {
            "success": True,
            "stats": _evolution_manager.get_status(),
            "core_memories_count": len(_evolution_manager.memory_dreaming.get_core_memories()),
            "red_team_reports_count": len(_evolution_manager.red_team.get_reports()),
            "social_decay_contacts_count": len(_evolution_manager.old_friend.get_decay_contacts()),
            "tools_created_count": len(_evolution_manager.tool_maker.list_tools()),
            "digital_legacy_letters_count": len(_evolution_manager.digital_legacy.get_letters())
        }
    except Exception as e:
        logger.error(f"Get evolution legacy error: {e}")
        return {"success": False, "error": str(e)}

# ═══════════════════════════════════════════════════════════════
# CODE ENDPOINTS
# ═══════════════════════════════════════════════════════════════
class CodeExecuteRequest(BaseModel):
    code: str
    language: str = "python"

@app.post("/code/execute")
async def execute_code(request: CodeExecuteRequest, authorization: Optional[str] = Header(None)):
    user_id = 1
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:].strip()
        user = auth.validate_session(token)
        if user:
            user_id = user["user_id"]
    
    if request.language != "python":
        return {"success": False, "error": "Only Python supported"}
    
    return code_executor.execute_python(request.code, user_id)

@app.get("/code/files")
async def list_code_files():
    return code_executor.list_files()

@app.get("/code/templates")
async def get_code_templates():
    return {"templates": [
        {"id": "hello", "name": "Hello World", "code": "print('Hello, World!')"},
        {"id": "math", "name": "Math Calculation", "code": "import math\nresult = math.sqrt(144)\nprint(f'Square root: {result}')"},
    ]}

# ═══════════════════════════════════════════════════════════════
# HUMOR ENDPOINTS
# ═══════════════════════════════════════════════════════════════
@app.get("/humor/joke")
async def get_joke(category: Optional[str] = None):
    from core.humor import humor
    return {"success": True, "joke": humor.get_joke(category)}

@app.get("/humor/fact")
async def get_fact():
    from core.humor import humor
    return {"success": True, "fact": humor.get_random_fact()}

@app.get("/humor/compliment")
async def get_compliment():
    from core.humor import humor
    return {"success": True, "compliment": humor.get_compliment()}

# ═══════════════════════════════════════════════════════════════
# PROACTIVE INTELLIGENCE ENDPOINTS
# ═══════════════════════════════════════════════════════════════
@app.get("/proactive/status")
async def get_proactive_status():
    """Get proactive intelligence system status"""
    try:
        from core.proactive import proactive_assistant
        return proactive_assistant.get_status()
    except Exception as e:
        logger.error(f"Proactive status error: {e}")
        return {"error": str(e)}

@app.post("/proactive/process")
async def process_input(request: Request):
    """Process input through proactive intelligence pipeline"""
    try:
        body = await request.json()
        user_input = body.get("input", "")
        conversation_context = body.get("context", [])
        
        from core.proactive import proactive_assistant
        result = proactive_assistant.process_input(user_input, conversation_context)
        
        return {
            "success": True,
            "pattern_match": result.get("pattern_match"),
            "predictions": result.get("predictions"),
            "actions": result.get("actions")
        }
    except Exception as e:
        logger.error(f"Proactive processing error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/proactive/patterns")
async def get_patterns():
    """Get all learned behavioral patterns"""
    try:
        from core.proactive import PatternMatcher
        matcher = PatternMatcher()
        return {"patterns": matcher.get_all_patterns()}
    except Exception as e:
        logger.error(f"Get patterns error: {e}")
        return {"error": str(e)}

@app.post("/proactive/patterns/learn")
async def learn_pattern(request: Request):
    """Learn a new behavioral pattern"""
    try:
        body = await request.json()
        trigger = body.get("trigger")
        routine = body.get("routine", [])
        frequency = body.get("frequency", 1)
        confidence = body.get("confidence", 0.7)
        
        from core.proactive import PatternMatcher
        matcher = PatternMatcher()
        matcher.learn_pattern(trigger, routine, frequency, confidence)
        
        return {"success": True, "message": f"Learned pattern: {trigger} → {routine}"}
    except Exception as e:
        logger.error(f"Learn pattern error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/proactive/predict")
async def predict_next_intent(request: Request):
    """Get intent predictions for given context"""
    try:
        body = await request.json()
        current_intent = body.get("intent", "")
        conversation_context = body.get("context", [])
        
        from core.proactive import IntentPredictor
        predictor = IntentPredictor()
        predictions = predictor.predict_next_intent(current_intent, conversation_context)
        
        return {"predictions": predictions}
    except Exception as e:
        logger.error(f"Intent prediction error: {e}")
        return {"error": str(e)}

@app.post("/proactive/task/decompose")
async def decompose_task(request: Request):
    """Decompose a complex task into sub-tasks"""
    try:
        body = await request.json()
        task = body.get("task", "")
        
        from core.proactive import TaskOrchestrator
        orchestrator = TaskOrchestrator()
        
        if orchestrator.is_complex_task(task):
            sub_tasks = orchestrator.decompose_task(task)
            for sub_task in sub_tasks:
                orchestrator.add_to_queue(sub_task)
            
            return {
                "is_complex": True,
                "sub_tasks": sub_tasks,
                "count": len(sub_tasks)
            }
        else:
            return {"is_complex": False, "message": "Task not complex enough to decompose"}
    except Exception as e:
        logger.error(f"Task decomposition error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/proactive/queue")
async def get_task_queue():
    """Get task execution queue status"""
    try:
        from core.proactive import TaskOrchestrator
        orchestrator = TaskOrchestrator()
        return orchestrator.get_queue_status()
    except Exception as e:
        logger.error(f"Task queue error: {e}")
        return {"error": str(e)}

@app.post("/proactive/queue/complete")
async def mark_task_complete(request: Request):
    """Mark a task as complete"""
    try:
        body = await request.json()
        task_id = body.get("task_id")
        
        from core.proactive import TaskOrchestrator
        orchestrator = TaskOrchestrator()
        orchestrator.mark_complete(task_id)
        
        return {"success": True, "message": "Task marked complete"}
    except Exception as e:
        logger.error(f"Mark complete error: {e}")
        return {"success": False, "error": str(e)}

# ═══════════════════════════════════════════════════════════════
# BIOMETRIC SECURITY ENDPOINTS
# ═══════════════════════════════════════════════════════════════
@app.post("/security/train-biometric")
async def train_biometric_model_endpoint(request: Request):
    """Train biometric model from typing data"""
    try:
        body = await request.json()
        typing_data = body.get("typing_data", [])
        
        result = await train_biometric_model(typing_data)
        return result
    except Exception as e:
        logger.error(f"Biometric training error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/security/verify-biometric")
async def verify_biometric_endpoint(request: Request):
    """Verify user identity through typing rhythm analysis"""
    try:
        body = await request.json()
        typing_data = body.get("typing_data", [])
        
        result = await verify_typing_rhythm(typing_data)
        return result
    except Exception as e:
        logger.error(f"Biometric verification error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/security/trigger-lockdown")
async def trigger_lockdown_endpoint(request: Request):
    """Trigger system lockdown for security"""
    try:
        result = await trigger_lockdown()
        return result
    except Exception as e:
        logger.error(f"Lockdown trigger error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/security/status")
async def get_security_status_endpoint():
    """Get current security system status"""
    try:
        result = await get_security_status()
        return result
    except Exception as e:
        logger.error(f"Security status error: {e}")
        return {"error": str(e)}


@app.post("/security/typing-event")
async def receive_typing_event(request: Request):
    """Receive typing events from frontend for biometric verification"""
    try:
        body = await request.json()
        event = body.get("event", {})
        
        # Add event to autonomy heartbeat system
        from core.autonomy import heartbeat
        await heartbeat.add_typing_event(event)
        
        return {
            "success": True,
            "message": "Typing event received"
        }
    except Exception as e:
        logger.error(f"Typing event error: {e}")
        return {"success": False, "error": str(e)}


@app.post("/security/typing-data")
async def receive_typing_data(request: Request):
    """Receive typing data for biometric verification (used during calibration)"""
    try:
        body = await request.json()
        typing_data = body.get("typing_data", body.get("keyData", []))
        
        # Verify typing rhythm against biometric model
        from api.security import verify_typing_rhythm
        result = await verify_typing_rhythm(typing_data)
        
        logger.info(f"Biometric verification result: {result.get('action', 'none')} - Score: {result.get('score', 0)}%")
        
        return result
    except Exception as e:
        logger.error(f"Typing data verification error: {e}")
        return {"success": False, "error": str(e)}


@app.get("/security/heartbeat/status")
async def get_heartbeat_status():
    """Get autonomous heartbeat status"""
    try:
        from core.autonomy import heartbeat
        return heartbeat.get_status()
    except Exception as e:
        logger.error(f"Heartbeat status error: {e}")
        return {"error": str(e)}

# ═══════════════════════════════════════════════════════════════
# REASONING TREE ENDPOINTS (131)
# ═══════════════════════════════════════════════════════════════
@app.get("/reasoning/thoughts")
async def get_thoughts(limit: int = 50):
    """Get recent thoughts from reasoning engine"""
    try:
        thoughts = reasoning_engine.get_thoughts(limit)
        return {
            "success": True,
            "thoughts": thoughts
        }
    except Exception as e:
        logger.error(f"Get thoughts error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/reasoning/stats")
async def get_reasoning_stats():
    """Get reasoning engine statistics"""
    try:
        stats = reasoning_engine.get_thought_stats()
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        logger.error(f"Get reasoning stats error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/reasoning/generate")
async def generate_rationalization(request: Request):
    """Generate a rationalization for an action"""
    try:
        body = await request.json()
        action = body.get("action", "")
        context = body.get("context", {})
        routine_id = body.get("routine_id")
        
        thought = await reasoning_engine.generate_rationalization(
            action=action,
            context=context,
            routine_id=routine_id
        )
        
        return {
            "success": True,
            "thought": thought
        }
    except Exception as e:
        logger.error(f"Generate rationalization error: {e}")
        return {"success": False, "error": str(e)}

@app.websocket("/ws/reasoning")
async def websocket_reasoning(websocket: WebSocket):
    """WebSocket for streaming thoughts in real-time"""
    await websocket.accept()
    logger.info("🧠 Reasoning WebSocket connected")
    
    try:
        while True:
            # Wait for a short time then send any new thoughts
            await asyncio.sleep(0.5)
            
            # Get recent thoughts
            thoughts = reasoning_engine.get_thoughts(limit=1)
            if thoughts:
                await websocket.send_json({
                    "type": "thought",
                    "data": thoughts[0]
                })
            
    except WebSocketDisconnect:
        logger.info("🧠 Reasoning WebSocket disconnected")
    except Exception as e:
        logger.error(f"Reasoning WebSocket error: {e}")

# ═══════════════════════════════════════════════════════════════
# WEBSOCKET ENDPOINTS
# ═══════════════════════════════════════════════════════════════
@app.websocket("/ws/heartbeat")
async def websocket_heartbeat(websocket: WebSocket):
    """WebSocket for real-time heartbeat and health updates"""
    await websocket.accept()
    logger.info("🔌 Heartbeat WebSocket connected")
    
    try:
        while True:
            # Send health status every 5 seconds
            await websocket.send_json({
                "type": "health_update",
                "data": heartbeat.get_health_status()
            })
            
            # Send proactive tasks
            tasks = heartbeat.get_proactive_tasks()
            if tasks:
                await websocket.send_json({
                    "type": "proactive_tasks",
                    "data": tasks
                })
            
            await asyncio.sleep(5)
            
    except WebSocketDisconnect:
        logger.info("🔌 Heartbeat WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    """WebSocket for streaming responses"""
    await websocket.accept()
    logger.info("🔌 Stream WebSocket connected")
    
    try:
        while True:
            # Wait for message
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
            
    except WebSocketDisconnect:
        logger.info("🔌 Stream WebSocket disconnected")
    except Exception as e:
        logger.error(f"Stream WebSocket error: {e}")

# ═══════════════════════════════════════════════════════════════
# Run
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
