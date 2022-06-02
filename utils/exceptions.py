from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken
from .http_ import HTTPResponse
from rest_framework.exceptions import ValidationError,PermissionDenied
from rest_framework import status
import json

def exceptions_handler(exc,content):
    print(exc,type(exc))
    if isinstance(exc,InvalidToken):
        # exc.detail
        return HTTPResponse(
            code=-1,
            status=status.HTTP_401_UNAUTHORIZED,
            message="token is invalid or expired,please login again",
            # message=exc.detail,
            app_code="auth"
        )
    if isinstance(exc,ValidationError):
        err_messages= ""
        for field,_ in exc.detail.items():
            err_messages += f"[{field}] "
        err_messages+=" not invalid value"
        return HTTPResponse(
            code=-1,
            status = status.HTTP_400_BAD_REQUEST,
            message=err_messages,
            app_code="oauth"
        )
    if isinstance(exc,PermissionDenied):
        return HTTPResponse(
            code=-1,
            status = status.HTTP_403_FORBIDDEN,
            message="当前用户没有改操作的权限",
            app_code="oauth"
        )    
    return exception_handler(exc,content)