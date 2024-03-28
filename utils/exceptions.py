from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken,AuthenticationFailed
from .http_ import HTTPResponse
from rest_framework.exceptions import \
    ValidationError,PermissionDenied,MethodNotAllowed,UnsupportedMediaType,NotAcceptable
from rest_framework import status
import json

def exceptions_handler(exc,content):
    # print(exc,type(exc),">>")
    if isinstance(exc,(InvalidToken,AuthenticationFailed)):
        # exc.detail
        return HTTPResponse(
            code=-1,
            status=status.HTTP_401_UNAUTHORIZED,
            message="token is invalid or expired,please login again",
            # message=exc.detail,
            app_code="auth"
        )
    if isinstance(exc,ValidationError):
        err_messages= "请求的参数错误,详细如下:"
        for field,ErrorDetailList in exc.detail.items():
            print(field,ErrorDetailList)
            err_messages += f"[{field}]:"
            for ErrorDetail in ErrorDetailList:
                err_messages += f"{str(ErrorDetail)}  ."
        # err_messages+=" not invalid value"
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
            message=f"操作不被允许!({exc.detail})",
            app_code="oauth"
        )  
    if isinstance(exc,MethodNotAllowed):
        return HTTPResponse(
            code=-1,
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            message=f"请求方法不被允许"
        )   
    if isinstance(exc,UnsupportedMediaType):
        return HTTPResponse(
            code=-1,
            status = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            message=exc.detail
        )  
    if isinstance(exc,NotAcceptable):
        return HTTPResponse(
            code=-1,
            status = status.HTTP_406_NOT_ACCEPTABLE,
            message=exc.detail
        ) 
    if isinstance(exc,UnsupportedMediaType):
        return HTTPResponse(
            code=-1,
            status = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            message=f"请求body的类型无法解析!"
        )  
    # print(">>>>>" ,exc,type(exc))
    return exception_handler(exc,content)

class ResponseError(Exception):pass