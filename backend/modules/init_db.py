# init_db.py
import sqlite3
from pathlib import Path

print("🚀 Initializing all Lucy OS databases...")

# Create data directory
Path("data").mkdir(exist_ok=True)

# ==================== MEMORY DATABASES ====================
def init_memory_db():
    conn = sqlite3.connect("data/long_term.db")
    cursor = conn.cursor()
    
    # Long Term Memory
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            timestamp DATETIME,
            role TEXT,
            content TEXT,
            embedding BLOB,
            sentiment REAL,
            topics TEXT,
            importance REAL DEFAULT 1.0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facts (
            id TEXT PRIMARY KEY,
            fact TEXT,
            category TEXT,
            confidence REAL,
            source TEXT,
            timestamp DATETIME,
            embedding BLOB,
            last_accessed DATETIME,
            access_count INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Long Term Memory DB initialized")

def init_episodic_db():
    conn = sqlite3.connect("data/episodic.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS episodes (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            start_time DATETIME,
            end_time DATETIME,
            summary TEXT,
            messages TEXT,
            topics TEXT,
            sentiment_avg REAL,
            importance REAL,
            tags TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            episode_id TEXT,
            timestamp DATETIME,
            role TEXT,
            content TEXT,
            embedding BLOB,
            FOREIGN KEY(episode_id) REFERENCES episodes(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Episodic Memory DB initialized")

def init_semantic_db():
    conn = sqlite3.connect("data/semantic.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facts (
            id TEXT PRIMARY KEY,
            fact TEXT,
            category TEXT,
            confidence REAL,
            source TEXT,
            timestamp DATETIME,
            embedding BLOB,
            related_facts TEXT,
            access_count INTEGER DEFAULT 0,
            last_accessed DATETIME
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            name TEXT PRIMARY KEY,
            description TEXT,
            parent TEXT,
            fact_count INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Semantic Memory DB initialized")

def init_procedural_db():
    conn = sqlite3.connect("data/procedural.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            category TEXT,
            steps TEXT,
            prerequisites TEXT,
            examples TEXT,
            success_rate REAL,
            times_used INTEGER DEFAULT 0,
            created DATETIME,
            last_used DATETIME,
            tags TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Procedural Memory DB initialized")

def init_emotional_db():
    conn = sqlite3.connect("data/emotional.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emotional_tags (
            memory_id TEXT,
            memory_type TEXT,
            emotion TEXT,
            intensity REAL,
            timestamp DATETIME,
            context TEXT,
            PRIMARY KEY (memory_id, memory_type, emotion)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Emotional Memory DB initialized")

def init_database_db():
    conn = sqlite3.connect("lucy_data.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at DATETIME
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database DB initialized")

# ==================== RUN ALL INITIALIZATIONS ====================
init_memory_db()
init_episodic_db()
init_semantic_db()
init_procedural_db()
init_emotional_db()
init_database_db()

print("\n🎉 All databases initialized successfully!")
print("📁 Data files created in /data directory")