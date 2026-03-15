import logging
import sqlite3
from pathlib import Path
from datetime import datetime
import hashlib

logger = logging.getLogger("LucyUsers")

class UserManager:
    def __init__(self):
        self.db_path = Path(__file__).parent.parent / "data" / "users.db"
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_db()
        logger.info("👥 User Database Initialized")
    
    def _init_db(self):
        """Initialize users database"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                theme TEXT DEFAULT 'dark',
                communication_style TEXT DEFAULT 'balanced',
                response_length TEXT DEFAULT 'medium'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
         
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Users table created")

    def _hash_password(self, password: str) -> str:
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username: str, password: str = None) -> dict:
        """Create new user (with or without password)"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            password_hash = self._hash_password(password) if password else None
             
            cursor.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            conn.commit()
             
            user_id = cursor.lastrowid
            conn.close()
            
            logger.info(f"✅ User created: {username} (ID: {user_id})")
            return {"success": True, "user_id": user_id, "username": username}
        except sqlite3.IntegrityError:
            return {"success": False, "error": "Username already exists"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def authenticate(self, username: str, password: str) -> dict:
        """Authenticate user with password"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            password_hash = self._hash_password(password)
            
            cursor.execute(
                'SELECT id, username, password_hash FROM users WHERE username = ? AND password_hash = ?',
                (username, password_hash)
            )
            user = cursor.fetchone()
            conn.close()
            
            if user:
                self._update_last_login(user[0])
                logger.info(f"✅ User authenticated: {username}")
                return {"success": True, "user_id": user[0], "username": user[1]}
            else:
                return {"success": False, "error": "Invalid username or password"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_user(self, username: str) -> dict:
        """Get user by username"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, username, theme, communication_style, response_length FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    "success": True,
                    "user_id": user[0],
                    "username": user[1],
                    "theme": user[2],
                    "communication_style": user[3],
                    "response_length": user[4]
                }
            return {"success": False, "error": "User not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_all_users(self) -> list:
        """Get all users (for switching)"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, username, created_at FROM users ORDER BY username')
            users = cursor.fetchall()
            conn.close()
            
            return [{"user_id": u[0], "username": u[1], "created_at": u[2]} for u in users]
        except Exception as e:
            return []

    def _update_last_login(self, user_id: int):
        """Update last login timestamp"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()

    def save_conversation(self, user_id: int, role: str, content: str):
        """Save conversation for user"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO conversations (user_id, role, content) VALUES (?, ?, ?)',
                (user_id, role, content)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Save conversation error: {e}")

    def get_conversations(self, user_id: int, limit: int = 20) -> list:
        """Get user's conversation history"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute(
                'SELECT role, content, timestamp FROM conversations WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
                (user_id, limit)
            )
            convos = cursor.fetchall()
            conn.close()
            return [{"role": c[0], "content": c[1], "timestamp": c[2]} for c in convos]
        except Exception as e:
            return []

    def clear_conversations(self, user_id: int):
        """Clear user's conversation history"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute('DELETE FROM conversations WHERE user_id = ?', (user_id,))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Clear conversations error: {e}")

    def update_settings(self, user_id: int, theme: str = None, communication_style: str = None, response_length: str = None) -> dict:
        """Update user settings"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            updates = []
            values = []
            
            if theme:
                updates.append("theme = ?")
                values.append(theme)
            if communication_style:
                updates.append("communication_style = ?")
                values.append(communication_style)
            if response_length:
                updates.append("response_length = ?")
                values.append(response_length)
            
            if updates:
                values.append(user_id)
                query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, values)
                conn.commit()
            
            conn.close()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_stats(self, user_id: int) -> dict:
        """Get user statistics"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM conversations WHERE user_id = ?", (user_id,))
            conv_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM conversations WHERE user_id = ?", (user_id,))
            timestamps = cursor.fetchone()
            
            cursor.execute("SELECT created_at, last_login FROM users WHERE id = ?", (user_id,))
            user_info = cursor.fetchone()
            
            conn.close()
            
            return {
                "success": True,
                "total_conversations": conv_count,
                "member_since": user_info[0] if user_info else "Unknown",
                "last_active": timestamps[1] or user_info[1] if user_info else "Unknown",
                "first_activity": timestamps[0]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete_user(self, user_id: int) -> dict:
        """Delete user and all their data"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM user_memories WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ User {user_id} deleted")
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_activity_log(self, user_id: int, limit: int = 20) -> list:
        """Get user activity log"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT role, content, timestamp FROM conversations WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
                (user_id, limit)
            )
            activities = cursor.fetchall()
            conn.close()
            
            return [{"role": a[0], "content": a[1][:100], "timestamp": a[2]} for a in activities]
        except Exception as e:
            return []

users = UserManager()