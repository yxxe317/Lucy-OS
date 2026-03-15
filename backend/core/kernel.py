from fastapi import FastAPI, HTTPException, UploadFile, File, Header, Request, Response
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
from core.autonomy import autonomy
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
import httpx
from fastapi import HTTPException
import time
from fastapi import HTTPException, status
# ===== NEW MODULE IMPORTS - DO NOT REMOVE =====
from core.api_router import module_router
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
# ==============================================

# Update CORS for audio and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://lucy-os.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

conversation_history: Dict[int, List[Dict]] = {}

@app.on_event("startup")
async def startup():
    await memory.init_db()
    logger.info("🧠 Lucy OS v21.0 Online - All Systems Ready")
    asyncio.create_task(autonomy.start_thought_loop())

@app.get("/health")
async def health():
    return {
        "status": "OK",
        "version": "21.0",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "active_sessions": len(auth.sessions)
    }

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
# Run
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)