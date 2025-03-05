import subprocess
import threading
import time
import sqlite3

def update_status(ip, status, latency):
    conn = sqlite3.connect('monitoring.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE ip_addresses SET status = ?, latency = ? WHERE ip = ?''',
                   (status, latency, ip))
    conn.commit()
    conn.close()

def ping(ip, host, city):
    while True:
        result = subprocess.run(["ping", "-n", "1", ip], capture_output=True)
        if "Request timed out" in result.stdout.decode():
            update_status(ip, "Down", "N/A")
        else:
            latency = result.stdout.decode().split("time=")[-1].split("ms")[0]
            update_status(ip, "Up", latency)
        time.sleep(5)  # Ping every 5 seconds

def start_monitoring():
    conn = sqlite3.connect('monitoring.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT ip, host, city FROM ip_addresses''')
    rows = cursor.fetchall()
    for row in rows:
        ip, host, city = row[0], row[1], row[2]
        threading.Thread(target=ping, args=(ip, host, city)).start()
    conn.close()
