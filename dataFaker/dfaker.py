"""
    WS收到开始任务信息 --> 根据条数分割产生任务()--> 开始执行 --> 每完成1%通过WS返回 
"""

import asyncio,os,csv,json
from concurrent.futures import ThreadPoolExecutor
import re
from dataFaker import generator

# threadsPool = ThreadPoolExecutor(max_workers=os.cpu_count()*3)

# def create_task(dataCount,filename):
#     with open(os.path.join(os.path.dirname(__file__),"select_options.json"),"rb") as f:
#         field_info = json.load(f)    
#     thehold = dataCount // 100
#     with open('1a.csv','wt') as f2:
#         cw = csv.writer(f2, lineterminator = '\n')
#         #采用writerow()方法
#         for item in FakerDataFactory(data_count=32000,fields_info=field_info):
#             cw.writerow(item) #将列表的每个元素写到csv文件的一行
#         #或采用writerows()方法
#         #cw.writerows(l) #将嵌套列表内容写入csv文件，每个外层元素为一行，每个内层元素为一个数据

import aiofiles
from dataFaker.models import DataFakerRecordInfo,file_directory_path
from aiocsv import AsyncWriter
from ws.const import WSMessageType
from  asgiref.sync import sync_to_async


@sync_to_async
def get_record(record_key):
    return DataFakerRecordInfo.objects.filter(record_key=record_key).first()

@sync_to_async
def update_record(record,**kwargs):
    for k,v in kwargs.items():
        if hasattr(record,k):
            setattr(record,k,v)
    record.save()

async def create_task_async(record_key=None,ws=None):
    try:
        if not record_key:
            raise DataFakerRecordInfo.DoesNotExist
        record = await get_record(record_key=record_key)
        target_path = file_directory_path(instance=record)
        data_count = record.count
        fields_info = record.fields
    except DataFakerRecordInfo.DoesNotExist:
        payload = {
            "type":WSMessageType.error,
            "data":{
                "message":"未找到对应的记录，请重新提交"
            },
            "record_key":record_key
        }   
        await ws.send(text_data=json.dumps(payload,ensure_ascii=False))
        return None,None

    if not os.path.exists(os.path.dirname(target_path)):
        os.makedirs(os.path.dirname(target_path))

    async with aiofiles.open(target_path, mode= 'w') as f:
        writer = AsyncWriter(f,lineterminator = '\n')
        index,threshold =0,data_count // 100
        for item in FakerDataFactory(data_count=data_count,fields_info=fields_info):  
            index+=1
            if index % threshold==0:
                # ws send progress
                payload = {
                    "type":WSMessageType.progress,
                    "data":{
                        "progress":int(index/data_count*100)
                    },
                    "record_key":record_key
                }   
                await ws.send(text_data=json.dumps(payload,ensure_ascii=False))
            await writer.writerow(item) #将列表的每个元素写到csv文件的一行
    await ws.send(text_data=json.dumps({"type":WSMessageType.finish,"record_key":record_key},ensure_ascii=False))
    await update_record(record=record,file=target_path,is_finish=True)
    return target_path,ws



class FakerDataFactory():
    
    def __init__(self,data_count=None,fields_info=None) -> None:
        self.data_count = data_count
        self.fields_info:dict = fields_info or {}
        self.already_count = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.already_count > self.data_count:
            raise StopIteration
        data = self.create()
        self.already_count+=1
        return data

    @property
    def field_titles(self):
        return [item.get("name","undefined_field_name") for item in self.fields_info]

    def create(self)->list:
        if not self.fields_info:
            return ["please","set","fields","first","!","!","!"]
        else:
            res = []
            for item in self.fields_info:
                generator_str,condition = item.get("generator"),item.get("condition")
                generator_class=getattr(generator,generator_str)
                value = generator_class().generate(**self._convert_params2dict(condition=condition))
                res.append(value)
            return res

    @staticmethod
    def _convert_params2dict(condition:list):
        kwargs = dict()
        for con in condition:
            kwargs.update({
                con.get("type"):con.get("value")
            })
        return kwargs

if __name__ == "__main__":
    asyncio.run(create_task_async())