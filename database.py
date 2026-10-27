import sqlite3
import os

DB_NAME = "prospects_history.db"

def init_db():
    """Inicializa la base de datos SQLite para control de duplicados."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_posts (
            post_id TEXT PRIMARY KEY,
            username TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def is_already_processed(post_id: str) -> bool:
    """Verifica si un post ya fue procesado y alertado previamente."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM processed_posts WHERE post_id = ?', (post_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_as_processed(post_id: str, username: str):
    """Registra un post como procesado en la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO processed_posts (post_id, username) VALUES (?, ?)', (post_id, username))
    conn.commit()
    conn.close()