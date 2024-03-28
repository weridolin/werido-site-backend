import dataclasses,sys,os

@dataclasses.dataclass
class BaseConfig:
    API_KEY :str
    URI:str = None
    
    @classmethod
    def from_env(cls):
        return cls(
            API_KEY = os.getenv("API_KEY")
        )
    

@dataclasses.dataclass
class EventStream:
    event_type:str = None
    event_data:str = None
    event_id:str = None
    


class HttpMixins:
    ## 请求混合类

    def __init__(self,message_id=None,api_key=None) -> None:
        self.event_type = "undefined"
        self.event_data = ""
        self.event_id = ""
        self.total_reply = ""
        self.error = False
        self.error_code = ""
        self.error_detail =""
        self.interrupt = False # 是否中途停止
        self.interrupt_reason = "" # 默认手动停止
        self.message_id = message_id
        self.api_key =api_key

    def request(self):
        raise NotImplementedError
    

    async def async_request(self):
        raise NotImplementedError
    

    def start_event_stream(self):
        ## event-stream
        ## 每次读取一行
        raise NotImplementedError
    

    def on_event(self,event:EventStream):
        raise NotImplementedError
    
    def parse_raw(self,res:str):                       
        if res=="":
            #当前行为空，说明上一次的数据已经结束
            return self._event_end()
            ...
        if res[0]==":":
            ## 注释行，直接忽略
            return
        if ':' in res:
            # contains ':'
            fields = res.split(':', 1)
            field_name = fields[0]
            field_value = fields[1].lstrip(' ')
            self._process_field(field_name, field_value)
        else:
            pass
    
    def _process_field(self,field_name,field_value):
        if field_name == "data":
            self.event_data += field_value
        elif field_name == "event":
            self.event_type = field_value
        elif field_name == "id":
            if not self.event_id=="":
                raise ValueError("id already exists")
            self.event_id = field_value
        elif field_name == "retry":
            raise NotImplementedError("retry not implemented yet")
        else:
            raise NotImplementedError(f"unknown field -> {field_name}")
    
    def _event_end(self):
        ## 事件结束
        event = EventStream(
            event_type=self.event_type,
            event_data=self.event_data,
            event_id=self.event_id
        )
        if hasattr(self,"on_event"):
            self.on_event(event)

        self.event_type = "undefined"
        self.event_data = ""
        self.event_id = ""
        return event

    def on_finish(self):
        raise NotImplementedError("on_finish not implemented yet")