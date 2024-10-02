from grpc_interceptor import ServerInterceptor
from grpc_interceptor.exceptions import AbortRpc
from auth import decode_jwt

class AuthInterceptor(ServerInterceptor):

    def __init__(self, exempt_methods=None):
        if exempt_methods is None:
            exempt_methods = []
        self.exempt_methods = exempt_methods

    def intercept(self, method, request, context, method_name):
        if method_name not in self.exempt_methods:
            metadata = dict(context.invocation.metadata())
            token = metadata.get('authorization')

            if token is None:
                raise AbortRpc(grpc.StatusCode.UNAUTHENTICATED, "No auth token")
            
            user_id = decode_jwt(token)
            if user_id is None:
                raise AbortRpc(grpc.StatusCode.UNAUTHENTICATED, "Invalid auth token")
            
            context.user_id = user_id

        return method(request, context)