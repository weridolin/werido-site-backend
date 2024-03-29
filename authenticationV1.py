from rest_framework import authentication
from rest_framework import exceptions

class V1Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user_id = request.META.get('HTTP_X_USER_ID') or request.META.get('HTTP_X_USER')
        print(">>>",request.META)
        if not user_id:
            raise exceptions.AuthenticationFailed('user auth failed,please login first')
        return (user_id, None)
    



# class V1IsAdmin(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         user_id = request.META.get('X_User_ID')
#         if not user_id:
#             raise exceptions.AuthenticationFailed('user auth failed')
#         print(">>>> get user id: ", user_id)
#         user_info = get_user_info(user_id)
#         if user_info.isSuperAdmin:
#             return (user_id, None)
#         else:
#             raise exceptions.AuthenticationFailed('user is not super admin')


class AsyncHttpConsumerMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # print(">",scope, receive, send)
        if not self.is_authenticated(scope):
            # If the user is not authenticated, retun a 403 error
            await send({
                "type": "http.response.start",
                "status": 401,
                "headers": [
                    (b"content-type", b"text/plain"),
                ],
            })
            await send({
                "type": "http.response.body",
                "body": b"User not authenticated",
            })
            return
        return await self.app(scope, receive, send)
    
    def is_authenticated(self, scope):
        # return True
        headers = scope['headers']  
        for header in headers:
            key,value = header  
            if key == b'x-user-id' or key == b'x-user':
                scope['user_id'] = value.decode('utf-8')
                return True
        return False