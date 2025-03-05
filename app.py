from flask import Flask, jsonify, render_template
import os
from database import init_db, get_ip_addresses

app = Flask(__name__)

# Initialize the database
init_db()

@app.route('/')
def index():
    statuses = get_ip_addresses()
    return render_template('index.html', statuses=statuses)

@app.route('/status')
def status():
    statuses = get_ip_addresses()
    return jsonify(statuses)

if __name__ == '__main__':
    try:
        print("Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"An error occurred while running the Flask server: {str(e)}")
        input("Press Enter to exit...")
