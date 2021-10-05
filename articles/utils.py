'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-09-05 10:05:41
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-02 17:40:06
'''
import json
from articles.models import *

class DatetimeJsonEncoder(json.JSONEncoder):
    """
        应对datetime.datetime() 对象的序列化,参考:
        https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def model2json(model):
    assert isinstance(model,BaseModel),"model to json fail!"
    d = {}
    for key,value in model.__dict__.items():
        if not key.startswith("_"):
            d[key]=value
    
    return json.dumps(d,ensure_ascii=False,cls=DatetimeJsonEncoder)
