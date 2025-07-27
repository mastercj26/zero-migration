import requests
import time
import grpc
import migration_pb2
import migration_pb2_grpc

def test_web_server(host='http://localhost:5000'):
    """Continuously query the web server"""
    while True:
        try:
            response = requests.get(host)
            print(f"Response: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        time.sleep(1)

def test_migration():
    """Test migration between servers"""
    channel = grpc.insecure_channel('localhost:50051')
    stub = migration_pb2_grpc.ProcessMigrationStub(channel)
    
    # Simulate migration from PID 123 to host "server2"
    response = stub.Migrate(migration_pb2.MigrateRequest(
        source_pid=123,
        target_host="server2"
    ))
    print(f"Migration response: {response}")

if __name__ == '__main__':
    # Run the web server tester by default
    test_web_server()