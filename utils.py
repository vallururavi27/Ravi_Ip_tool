import pandas as pd
import sqlite3
from monitoring import start_monitoring

def load_ip_addresses(filepath):
    try:
        print("Reading Excel file...")
        df = pd.read_excel(filepath, engine='openpyxl')
        print("Excel file read successfully.")
        
        # Print column names to confirm
        print("Excel columns:", df.columns)

        print("Connecting to the database...")
        conn = sqlite3.connect('monitoring.db')
        cursor = conn.cursor()
        
        print("Inserting IP addresses into the database...")
        for index, row in df.iterrows():
            ip, host, city = row['IP'], row['Host'], row['City']
            cursor.execute('''INSERT INTO ip_addresses (ip, host, city, status, latency) VALUES (?, ?, ?, ?, ?)''',
                           (ip, host, city, 'Unknown', 'N/A'))
        conn.commit()
        conn.close()
        print("IP addresses inserted successfully. Starting monitoring...")
        start_monitoring()
    except Exception as e:
        print(f"An error occurred in utils.py: {str(e)}")
        input("Press Enter to exit...")
