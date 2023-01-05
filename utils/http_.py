# from http import HTTPStatus
from http import HTTPStatus
import dataclasses
from typing import Any
from rest_framework.response import Response
import json
from rest_framework import status

CODE_DEFAULT_DESC_REF = {
    i.value:i.description for i in HTTPStatus
}

APP_CODE_REF = {
    "article":100,
    "auth":101,
    "dataFaker":102,
    "drug":103,
    "filebroker":104,
    "home":105,
    "oauth":106
}


@dataclasses.dataclass
class Payload(object):
    data:Any = ""
    message:str = ""
    code:int  = 0
    app_code:int =-1
    status:int = 200

    def to_dict(self):
        return {
            "data":self.data,
            "message":self.message,
            "code":self.code,
            "app_code":self.app_code,
            "status":self.status
        }

    def to_json(self):
        return json.dumps(
            self.to_dict(),ensure_ascii=False
        )


class HTTPResponse(Response):
    def __init__(self, data=None, status=200, message=None,code=0,app_code=-1,template_name=None, headers=None, exception=False, content_type=None):
        if not message:
            try:
                message = CODE_DEFAULT_DESC_REF.gte(code,None)
            except:
                message = None
        if isinstance(app_code,str):
            app_code = APP_CODE_REF.get(app_code,-1)
        payload = Payload(data=data,message=message,app_code=app_code,code=code,status=status).to_dict()

        if status == HTTPStatus.NO_CONTENT:
            payload = None
        super().__init__(payload, status, template_name, headers, exception, content_type)
