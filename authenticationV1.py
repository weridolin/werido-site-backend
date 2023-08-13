from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
# from rpc.usercenter.client import get_user_info
import os

class V1Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user_id = request.META.get('HTTP_X_USER_ID')
        print(">>>",request.META)
        if not user_id:
            raise exceptions.AuthenticationFailed('user auth failed')
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
