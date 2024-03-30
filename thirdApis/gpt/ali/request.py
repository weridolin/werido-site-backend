import dataclasses
from typing import List,Dict
from thirdApis.models import GptMessage
import sys,os
from thirdApis.gpt.ali.config import AliChatConfig
from thirdApis.gpt.base import HttpMixins,EventStream
from rest_framework import status
import aiohttp,requests,logging
import json
logger = logging.getLogger(__name__)

@dataclasses.dataclass
class AliRequestInputParam:
    prompt:str=None
    messages:List[Dict]=None

@dataclasses.dataclass
class AliRequestParameters:
    seed:int=1234
    max_tokens:int=1500
    top_p:float=0.9
    top_k:int=40
    repetition_penalty:float=1.1
    temperature:float=0.9
    stop=None
    stream:bool=True
    enable_search:bool=False
    result_format:str="message"
    incremental_output:bool=True

@dataclasses.dataclass
class AliRequestBody:
    model:str
    input:AliRequestInputParam
    parameters:AliRequestParameters


class HttpRequest(HttpMixins):

    def __init__(self, message_id,async_consumer) -> None:
        super().__init__(message_id)
        self.async_consumer=async_consumer

    async def request(
        self,
        model:str,
        messages:List[str]=None,
        prompt:str=None,
        stream:bool=True,
        enable_search:bool=False,
        incremental_output:bool=True,
        response = None,
        conversation_id:str=None,
        api_key = None
    ):
        config = AliChatConfig.from_env()
        config.API_KEY = api_key
        header = {
            "Authorization": f"Bearer {config.API_KEY}",
            "Content-Type": "application/json",
        }
        if stream:
            header["Accept"] = "text/event-stream"
    
        body = dataclasses.asdict(AliRequestBody(
                model=model,
                input=AliRequestInputParam(messages=messages) if messages else AliRequestInputParam(prompt=prompt),
                parameters=AliRequestParameters(
                    stream=stream,
                    enable_search=enable_search,
                    incremental_output=incremental_output
                )
            )
        )
        async with aiohttp.ClientSession() as session:
            async with session.post(url=config.URI,headers=header,json=body) as response:
                if response.status == 200:
                    await self.async_consumer.send_headers(headers=[
                        (b'Cache-Control', b'no-cache'),
                        (b'Content-Type', b'text/event-stream'),
                        # (b"Transfer-Encoding", b"chunked"),
                        (b'Access-Control-Allow-Origin', b'*'),
                        (b'X-Accel-Buffering',b"no")
                    ])                   
                    async for res in response.content:
                        res = res.decode('utf8') 
                        res = res.rstrip('\n').rstrip('\r')
                        event = self.parse_raw(res)
                        if self.interrupt:
                            logger.info(f"ali gpt request was interrupted,break the loop...")
                            break
                        if isinstance(event,EventStream):
                            data = json.loads(event.event_data)
                            # print(data,">")
                            message = json.dumps({
                                "message":data["output"]["choices"][0]["message"]["content"],
                                "query_message_uuid":self.message_id,
                                "finish_reason":data["output"]["choices"][0]["finish_reason"],
                                "conversation_id":conversation_id,
                            },ensure_ascii=False)
                            await self.async_consumer.send_body(
                                f"event:message\ndata:{message}\n\n".encode('utf8'),
                                more_body=True)
                else:
                    res = json.loads(await response.text())
                    logger.error(f"ali gpt request error -> {res} ")
                    if res.get("code")=="InvalidApiKey":
                        self.error = True
                        self.error_code = res.get("code")
                        self.error_detail = res.get("message")
        await self.async_consumer.send_body(b"",more_body=False)
        self.on_finish()

    def on_event(self,event:EventStream):
        if event.event_type == "result":
            ## 处理结果 
            try:
                data = json.loads(event.event_data)
                content = data["output"]["choices"][0]["message"]["content"]
                self.total_reply += content                
            except json.JSONDecodeError:
                data = event.event_data
                self.total_reply += data
            
    def on_finish(self):
        logger.info(f"ali gpt request finish,update result back to DB")
        res = GptMessage.objects.filter(uuid=self.message_id).update(
                reply_content=self.total_reply,
                interrupt=self.interrupt,
                interrupt_reason=self.interrupt_reason,
                error=self.error,
                error_code=self.error_code,
                error_detail=self.error_detail,
                reply_finish=True,
                has_sended=True,
            )
        if res:
            logger.info(f"update replay content to DB success")
        else:
            logger.error(f"update replay content to DB error")

        
if __name__ =="__main__":
    import asyncio,os
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(HttpRequest().request("qwen-max",prompt="你好吗？"))
    # loop.close()
