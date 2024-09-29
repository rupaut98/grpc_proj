import grpc
import task_pb2
import task_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = task_pb2_grpc.TaskServiceStub(channel)

        create_response = stub.CreateTask(
            task_pb2.CreateTaskRequest(id=1, description="Learn gRPC", priority=1)
        )
        print(f"CreateTask Response: {create_response.response}")

        # Get the task
        get_response = stub.GetTask(task_pb2.GetTaskRequest(id=1))
        print(f"GetTask Response: Description - {get_response.description}, Priority - {get_response.priority}, Response - {get_response.response}")

        # Update the task
        update_response = stub.UpdateTask(
            task_pb2.UpdateTaskRequest(id=1, description="Learn gRPC in Python", priority=2)
        )
        print(f"UpdateTask Response: {update_response.response}")

        # Get the updated task
        get_updated_response = stub.GetTask(task_pb2.GetTaskRequest(id=1))
        print(f"Updated GetTask Response: Description - {get_updated_response.description}, Priority - {get_updated_response.priority}, Response - {get_updated_response.response}")

        # Delete the task
        delete_response = stub.DeleteTask(task_pb2.DeleteTaskRequest(id=1))
        print(f"DeleteTask Response: {delete_response.response}")

        # Try getting the deleted task
        get_deleted_response = stub.GetTask(task_pb2.GetTaskRequest(id=1))
        print(f"Get Deleted Task Response: {get_deleted_response.response}")

if __name__ == "__main__":
    run()