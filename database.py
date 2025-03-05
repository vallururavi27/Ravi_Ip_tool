import sqlite3

def init_db():
    conn = sqlite3.connect('monitoring.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ip_addresses (
        id INTEGER PRIMARY KEY,
        ip TEXT NOT NULL,
        host TEXT,
        city TEXT,
        status TEXT,
        latency TEXT
    )''')
    conn.commit()
    conn.close()

def get_ip_addresses():
    conn = sqlite3.connect('monitoring.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ip, host, city, status, latency FROM ip_addresses')
    rows = cursor.fetchall()
    conn.close()

    ip_addresses = {}
    for row in rows:
        ip_addresses[row[0]] = {
            'host': row[1],
            'city': row[2],
            'status': row[3],
            'latency': row[4]
        }
    return ip_addresses
