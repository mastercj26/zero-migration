from concurrent import futures
import grpc
import time
import logging
import checkpoint
import migration_pb2
import migration_pb2_grpc

class MigrationService(migration_pb2_grpc.ProcessMigrationServicer):
    def Checkpoint(self, request, context):
        logging.info(f"Received checkpoint request for PID {request.pid}")
        filename = checkpoint.take_checkpoint(request.pid)
        return migration_pb2.CheckpointResponse(filename=filename)
    
    def Restore(self, request, context):
        logging.info(f"Received restore request with file {request.filename}")
        process_info = checkpoint.restore_process(request.filename)
        return migration_pb2.RestoreResponse(
            pid=process_info['pid'],
            status="RESTORED"
        )
    
    def Migrate(self, request, context):
        logging.info(f"Received migrate request from {request.source_pid} to {request.target_host}")
        process_info = checkpoint.migrate_process(request.source_pid, request.target_host)
        return migration_pb2.MigrateResponse(
            target_pid=process_info['pid'],
            status="MIGRATED"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    migration_pb2_grpc.add_ProcessMigrationServicer_to_server(MigrationService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Migration service running on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()