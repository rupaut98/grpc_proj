import grpc
from concurrent import futures
import sys
import logging

sys.path.append("/Users/rupakraut/Desktop/learning/grpc/grpc_todo_project/src")

from app.auth.auth_interceptor import AuthInterceptor
from app.auth.thread_local import get_current_user
from generated import task_pb2, task_pb2_grpc

tasks = {}

logging.basicConfig(level=logging.DEBUG)

class TaskService(task_pb2_grpc.TaskServiceServicer):

    def CreateTask(self, request, context):
        logging.debug(f"Received CreateTask request with id: {request.id}, description: {request.description}, priority: {request.priority}")
        
        try:
            user_id = get_current_user()
            logging.debug(f"user_id: {user_id}")
            if request.id in tasks:
                return task_pb2.CreateTaskResponse(response=0)
            
            tasks[request.id] = {
                "description": request.description,
                "priority": request.priority
            }
            return task_pb2.CreateTaskResponse(response=1)
        except Exception as e:
            logging.error(f"Exception in CreateTask: {str(e)}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
            return task_pb2.CreateTaskResponse(response=0)
    
    def GetTask(self, request, context):
        if request.id in tasks:
            return task_pb2.GetTaskResponse(description = tasks[request.id]["description"], priority=tasks[request.id]["priority"], response = 1)
        else:
            return task_pb2.GetTaskResponse(response = 0)
        
    def DeleteTask(self, request, context):
        if request.id in tasks:
            tasks.pop(request.id)
            return task_pb2.DeleteTaskResponse(response = 1)
        else:
            return task_pb2.DeleteTaskResponse(response = 0)
        
    def UpdateTask(self, request, context):
        if request.id in tasks:
            if request.description:
                tasks[request.id]["description"] = request.description
            if request.priority:
                tasks[request.id]["priority"] = request.priority

            return task_pb2.UpdateTaskResponse(response = 1)
        else:
            return task_pb2.UpdateTaskResponse(response = 0)

def serve():
    auth_interceptor = AuthInterceptor()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10), interceptors=[auth_interceptor])
    task_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

