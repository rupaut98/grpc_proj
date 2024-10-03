import grpc
import sys
import logging

sys.path.append("/Users/rupakraut/Desktop/learning/grpc/grpc_todo_project/src")

from generated import task_pb2, task_pb2_grpc
from app.auth.auth import generate_jwt

logging.basicConfig(level=logging.DEBUG)

def run():
    token = generate_jwt(user_id=1)
    logging.debug(f"Generated JWT token: {token}")
    metadata = [('authorization', str(token))]

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = task_pb2_grpc.TaskServiceStub(channel)

        try:
            create_response = stub.CreateTask(
                task_pb2.CreateTaskRequest(id=1, description="Learn gRPC", priority=1), metadata=metadata
            )
            logging.debug(f"CreateTask Response: {create_response.response}")
        except grpc.RpcError as e:
            logging.error(f"gRPC error in CreateTask: {e.details()}")
            logging.error(f"gRPC status code: {e.code()}")
            return


        # Get the task
        get_response = stub.GetTask(task_pb2.GetTaskRequest(id=1), metadata=metadata)
        print(f"GetTask Response: Description - {get_response.description}, Priority - {get_response.priority}, Response - {get_response.response}")

        # Update the task
        update_response = stub.UpdateTask(
            task_pb2.UpdateTaskRequest(id=1, description="Learn gRPC in Python", priority=2), metadata=metadata)
        print(f"UpdateTask Response: {update_response.response}")

        # Get the updated task
        get_updated_response = stub.GetTask(task_pb2.GetTaskRequest(id=1), metadata=metadata)
        print(f"Updated GetTask Response: Description - {get_updated_response.description}, Priority - {get_updated_response.priority}, Response - {get_updated_response.response}")

        # Delete the task
        delete_response = stub.DeleteTask(task_pb2.DeleteTaskRequest(id=1), metadata=metadata)
        print(f"DeleteTask Response: {delete_response.response}")

        # Try getting the deleted task
        get_deleted_response = stub.GetTask(task_pb2.GetTaskRequest(id=1), metadata=metadata)
        print(f"Get Deleted Task Response: {get_deleted_response.response}")

if __name__ == "__main__":
    run()
