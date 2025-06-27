import sqlite3
from datetime import datetime

def log_sqli_attempt(ip: str, payload: str):
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sqli_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        payload TEXT,
        timestamp TEXT
    )''')
    c.execute("INSERT INTO sqli_logs (ip, payload, timestamp) VALUES (?, ?, ?)",
              (ip, payload, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
