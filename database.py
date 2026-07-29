# utils/database.py
import sqlite3
from datetime import datetime

DB_PATH = 'data/progress.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            created_at TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            user_id TEXT,
            level INTEGER,
            score INTEGER,
            streak INTEGER,
            updated_at TEXT
        )
    ''')
    conn.commit()
    conn.close()
    return True

def save_progress(user_id, data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO progress (user_id, level, score, streak, updated_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, data.get('level', 1), data.get('score', 0),
          data.get('streak', 0), datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_progress(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT level, score, streak FROM progress WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {'level': result[0], 'score': result[1], 'streak': result[2]}
    return None
