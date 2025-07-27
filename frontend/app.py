import grpc
import migration_pb2
import migration_pb2_grpc
from flask import Flask, render_template
import requests
import time
from flask import Flask, render_template, request, jsonify 
app = Flask(__name__)
import platform
import socket

# Cross-platform way to get host information
host_info = {
    'host': socket.gethostname(),  # Works on all platforms
    'system': platform.system(),   # e.g., 'Windows', 'Linux'
    'release': platform.release()  # OS version
}
SERVERS = {
    'server1': 'http://localhost:5000',
    'server2': 'http://localhost:5001'
}
@app.route('/migrate')
def migrate():
    target = request.args.get('target', 'server2')
    
    
    source_pid = 123  # This would be dynamic in a real implementation
    
    channel = grpc.insecure_channel('localhost:50051')
    stub = migration_pb2_grpc.ProcessMigrationStub(channel)
    
    response = stub.Migrate(migration_pb2.MigrateRequest(
        source_pid=source_pid,
        target_host=target
    ))
    
    return jsonify({
        'status': f"Migration from PID {source_pid} to {target} initiated",
        'target_pid': response.target_pid
    })

def get_server_status(url):
    try:
        response = requests.get(url + '/state', timeout=1)
        return response.json()
    except:
        return {'error': 'Server not responding'}

@app.route('/')
def dashboard():
    status = {name: get_server_status(url) for name, url in SERVERS.items()}
    return render_template('dashboard.html', servers=status)

if __name__ == '__main__':
    app.run(port=8080)