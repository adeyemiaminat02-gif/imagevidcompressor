import sqlite3
from datetime import datetime
from utils.config import DATABASE_URL

def init_db():
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            joined_at TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            user_id INTEGER PRIMARY KEY,
            img_level TEXT DEFAULT 'medium',
            vid_level TEXT DEFAULT 'balanced',
            preserve_metadata INTEGER DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT,
            original_size INTEGER,
            compressed_size INTEGER,
            timestamp TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(user_id: int, username: str):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", (user_id, username, datetime.now().isoformat()))
    cursor.execute("INSERT OR IGNORE INTO settings (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def get_settings(user_id: int):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT img_level, vid_level, preserve_metadata FROM settings WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"img_level": row[0], "vid_level": row[1], "preserve_metadata": row[2]}
    return {"img_level": "medium", "vid_level": "balanced", "preserve_metadata": 1}

def update_settings(user_id: int, key: str, value: str | int):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE settings SET {key} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()

def log_history(user_id: int, filename: str, orig_size: int, comp_size: int):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (user_id, filename, original_size, compressed_size, timestamp) VALUES (?, ?, ?, ?, ?)",
                   (user_id, filename, orig_size, comp_size, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_history(user_id: int):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT filename, original_size, compressed_size, timestamp FROM history WHERE user_id = ? ORDER BY id DESC LIMIT 10", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows
