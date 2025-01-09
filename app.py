from flask import Flask, render_template
from flask_socketio import SocketIO
import requests
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Function to fetch cryptocurrency data
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,binancecoin",
        "vs_currencies": "usd",
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {}

# Background task to emit real-time data
def emit_crypto_data():
    while True:
        data = fetch_crypto_data()
        socketio.emit("crypto-data", data)
        time.sleep(5)  # Update every 5 seconds

# Start background thread
thread = threading.Thread(target=emit_crypto_data)
thread.daemon = True
thread.start()

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5002)
