from grpc_interceptor import ServerInterceptor
from grpc_interceptor.exceptions import Aborted, Unauthenticated
import sys
import logging

sys.path.append("/Users/rupakraut/Desktop/learning/grpc/grpc_todo_project/src")

from app.auth.auth import decode_jwt
from app.auth.thread_local import set_current_user

class AuthInterceptor(ServerInterceptor):

    def intercept(self, method, request, context, method_name):
        logging.debug(f"Intercepting method: {method_name}")
        
        if method_name not in self.exempt_methods:
            metadata = dict(context.invocation_metadata())
            logging.debug(f"Metadata received: {metadata}")

            token = metadata.get('authorization')
            if token is None:
                logging.error("Authorization token missing.")
                raise Aborted(details="No auth token")
            
            if not isinstance(token, str):
                logging.error(f"Invalid type for token: {type(token)}")
                raise Aborted(details="Authorization token must be a string")

            user_id = decode_jwt(token)
            if user_id is None:
                logging.error("Invalid JWT token.")
                raise Unauthenticated(details="Invalid auth token")
            
            set_current_user(user_id)
        
        return method(request, context)

