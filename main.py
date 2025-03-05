from database import init_db
from utils import load_ip_addresses

try:
    print("Initializing the database...")
    init_db()
    print("Database initialized.")

    print("Loading IP addresses from Excel file...")
    load_ip_addresses('ip_addresses.xlsx')
    print("IP addresses loaded successfully.")
except Exception as e:
    print(f"An error occurred in main.py: {str(e)}")
    input("Press Enter to exit...")
