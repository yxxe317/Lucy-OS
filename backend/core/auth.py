import logging
import secrets
from datetime import datetime, timedelta
from typing import Optional

# ⚠️ CRITICAL: This MUST match kernel.py exactly
SECRET_KEY = "lucy-os-secret-key-2026"
ALGORITHM = "HS256"

logger = logging.getLogger("LucyAuth")

class SessionManager:
    def __init__(self):
        self.sessions = {}  # token -> {user_id, username, expires}
        self.session_duration = timedelta(hours=24)
        logger.info("🔐 Session Manager Initialized")
    
    def create_session(self, user_id: int, username: str) -> str:
        """Create new session token"""
        token = secrets.token_urlsafe(32)
        expires = datetime.now() + self.session_duration
        
        self.sessions[token] = {
            "user_id": user_id,
            "username": username,
            "expires": expires
        }
        
        logger.info(f"✅ Session created for {username} (Token: {token[:10]}...)")
        return token
    
    def validate_session(self, token: str) -> Optional[dict]:
        """Validate session token"""
        if not token:
            return None
            
        if token not in self.sessions:
            logger.warning(f"⚠️ Session not found for token: {token[:10]}...")
            return None
        
        session = self.sessions[token]
        
        if datetime.now() > session["expires"]:
            del self.sessions[token]
            logger.warning(f"⏰ Session expired for {session['username']}")
            return None
        
        return {"user_id": session["user_id"], "username": session["username"]}
    
    def end_session(self, token: str) -> bool:
        """End/logout session"""
        if token in self.sessions:
            username = self.sessions[token]["username"]
            del self.sessions[token]
            logger.info(f"✅ Session ended for {username}")
            return True
        logger.warning(f"⚠️ Session not found for logout: {token[:10]}...")
        return False
    
    def cleanup_expired(self):
        """Remove expired sessions"""
        now = datetime.now()
        expired = [t for t, s in self.sessions.items() if now > s["expires"]]
        for token in expired:
            del self.sessions[token]
        if expired:
            logger.info(f"🧹 Cleaned up {len(expired)} expired sessions")

# Global instance
auth = SessionManager()