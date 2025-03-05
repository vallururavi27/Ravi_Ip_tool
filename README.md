# Ravi_Ip_tool
Network Monitoring Tool is a web-based application that monitors the status and latency of specified IP addresses. It provides a user-friendly interface to view the monitoring results and upload new IP addresses to be monitored.

Project Overview
The Network Monitoring Tool is a web-based application that monitors the status and latency of specified IP addresses. It provides a user-friendly interface to view the monitoring results and upload new IP addresses to be monitored.

Requirements
Python 3.x

Flask

pandas

openpyxl

sqlite3 (part of Python standard library)

Directory Structure
NetworkMonitoringTool
│   app.py
│   database.py
│   monitoring.py
│   utils.py
│   main.py
│   monitoring.db
│   ip_addresses.xlsx
├───templates
│       index.html
Setup Instructions
Clone the Repository (if using version control):

sh
git clone <repository_url>
cd NetworkMonitoringTool
Create and Activate Virtual Environment:

sh
python -m venv myenv
.\myenv\Scripts\Activate
Install Required Libraries:

sh
pip install Flask pandas openpyxl
Prepare the Excel File (ip_addresses.xlsx): Create an Excel file named ip_addresses.xlsx with columns IP, Host, and City.

Example:

Code Explanation
1. main.py
Initializes the database and loads IP addresses from the Excel file.

python
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
2. database.py
Handles database initialization and retrieves IP addresses.

python
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
3. utils.py
Loads IP addresses from the Excel file and starts monitoring.

python
import pandas as pd
import sqlite3
from monitoring import start_monitoring

def load_ip_addresses(filepath):
    try:
        print("Reading Excel file...")
        df = pd.read_excel(filepath, engine='openpyxl')
        print("Excel file read successfully.")

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
4. monitoring.py
Pings IP addresses and updates their status.

python
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
5. app.py
Runs the Flask web server and handles routes.

python
from flask import Flask, jsonify, render_template, request
import os
from database import init_db, get_ip_addresses
from utils import load_ip_addresses

app = Flask(__name__)

# Initialize the database
init_db()

# Ensure the 'uploads' directory exists
uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

@app.route('/')
def index():
    statuses = get_ip_addresses()
    return render_template('index.html', statuses=statuses)

@app.route('/status')
def status():
    statuses = get_ip_addresses()
    return jsonify(statuses)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        file_path = os.path.join(uploads_dir, file.filename)
        try:
            file.save(file_path)
            load_ip_addresses(file_path)
            return "File uploaded and IP addresses added"
        except PermissionError as e:
            return f"Permission error: {str(e)}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    try:
        print("Starting Flask server...")
        app.run(debug=True)
    except Exception as

    ****
6. index.html (continued)
html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Network Monitoring Dashboard</title>
    <link href="https://fonts.googleapis.com/css?family=Roboto:400,500,700" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #4CAF50;
            padding: 20px;
            text-align: center;
            color: white;
        }
        h1 {
            margin: 0;
            font-size: 24px;
        }
        .container {
            width: 90%;
            margin: 20px auto;
            background: #fff;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 16px;
        }
        th, td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
            text-align: left;
            font-weight: 500;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .upload-form {
            margin: 20px 0;
            text-align: center;
        }
        .upload-form input[type="file"] {
            display: inline-block;
            padding: 10px;
            font-size: 16px;
        }
        .upload-form input[type="submit"] {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .upload-form input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <header>
        <h1>Network Monitoring Dashboard</h1>
    </header>
    <div class="container">
        <div class="upload-form">
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <input type="submit" value="Upload">
            </form>
        </div>
        <table>
            <thead>
                <tr>
                    <th>IP Address</th>
                    <th>Host Name</th>
                    <th>City</th>
                    <th>Status</th>
                    <th>Latency (ms)</th>
                </tr>
            </thead>
            <tbody id="status-table-body">
                <!-- Rows will be populated dynamically -->
            </tbody>
        </table>
    </div>
    <script>
        function updateStatusTable() {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    const tableBody = document.querySelector('#status-table-body');
                    tableBody.innerHTML = '';
                    for (const [ip, details] of Object.entries(data)) {
                        const row = document.createElement('tr');
                        const ipCell = document.createElement('td');
                        ipCell.textContent = ip;
                        const hostCell = document.createElement('td');
                        hostCell.textContent = details.host;
                        const cityCell = document.createElement('td');
                        cityCell.textContent = details.city;
                        const statusCell = document.createElement('td');
                        statusCell.textContent = details.status;
                        const latencyCell = document.createElement('td');
                        latencyCell.textContent = details.latency;
                        row.appendChild(ipCell);
                        row.appendChild(hostCell);
                        row.appendChild(cityCell);
                        row.appendChild(statusCell);
                        row.appendChild(latencyCell);
                        tableBody.appendChild(row);
                    }
                });
        }

        setInterval(updateStatusTable, 5000); // Refresh the table every 5 seconds
    </script>
</body>
</html>
Running the Application
Run main.py to initialize the database and load IP addresses:

sh
python main.py
Run app.py to start the Flask server:

sh
python app.py
Open your web browser and navigate to:

plaintext
http://127.0.0.1:5000/
Web Interface
Dashboard: Displays the IP addresses, their host names, cities, status, and latency.

Upload Form: Allows you to upload a new Excel file with IP addresses to be monitored.

Troubleshooting
Database Errors: Ensure the database schema in database.py includes all required columns.

Import Errors: Verify all functions are correctly imported and defined.

Flask Server Issues: Check for error messages in the Command Prompt or PowerShell window and ensure Flask is properly installed.

Common Issues
ImportError: Ensure all necessary functions are defined and imported.

FileNotFoundError: Verify the file paths are correct and files exist.

Connection Refused: Ensure the Flask server is running and there are no firewall issues.
    
