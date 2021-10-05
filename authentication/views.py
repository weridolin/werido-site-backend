'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-09-05 23:51:59
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-09-06 08:49:14
'''
from django.shortcuts import render
import json
# Create your views here.

from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import login as _login

@api_view(http_method_names=["post"])
@parser_classes([FormParser,MultiPartParser])
def login(request):
    # print(type(request)) class 'rest_framework.request.Request'
    username= request.POST.get("username",None)
    pwd = request.POST.get("password",None)
    if username and pwd:
        user = authenticate(request._request, username=username, password=pwd)
        if user is not None:
            _login(request._request, user)
            return Response({"msg":f"{username} login  success!"},
            status=status.HTTP_200_OK)
        else:
            # Return an 'invalid login' error message.
            return Response(
                {"msg":f"INVALID USERNAME OR WRONG PASSWORD!"},
                status=status.HTTP_403_FORBIDDEN)
    else:
        return HttpResponseBadRequest(
            json.dumps({"msg":F"invalid username or password"},
            ensure_ascii=False))


def logout():
    ...