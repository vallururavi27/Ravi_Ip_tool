import sqlite3

def init_db():
    conn = sqlite3.connect('monitoring.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ip_addresses (
        id INTEGER PRIMARY KEY,
        ip TEXT NOT NULL,
        status TEXT,
        latency TEXT
    )''')
    conn.commit()
    conn.close()
