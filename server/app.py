from flask import Flask, jsonify
import time
import os
import threading
import os
import platform
import socket

# Cross-platform way to get host information
host_info = {
    'host': socket.gethostname(),  # Works on all platforms
    'system': platform.system(),   # e.g., 'Windows', 'Linux'
    'release': platform.release()  # OS version
}

print(host_info)
app = Flask(__name__)

# Simple in-memory state
state = {
    'requests_served': 0,
    'start_time': time.time(),
    'pid': os.getpid(),
    'host': os.uname().nodename
}

@app.route('/')
def home():
    state['requests_served'] += 1
    return jsonify({
        'message': f'Hello from server {state["pid"]}',
        'requests_served': state['requests_served'],
        'uptime': time.time() - state['start_time'],
        'host': state['host']
    })

@app.route('/state')
def get_state():
    return jsonify(state)

def start_server(port=5000):
    app.run(port=port)

if __name__ == '__main__':
    start_server()