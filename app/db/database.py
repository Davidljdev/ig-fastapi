import sqlite3
from pathlib import Path

DB_PATH = Path("ig-urls.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            deleted_at DATETIME
        )
    """)

    conn.commit()
    conn.close()
