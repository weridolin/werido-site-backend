from thirdApis.gpt.base import BaseConfig
import dataclasses

@dataclasses.dataclass
class AliChatConfig(BaseConfig):
    
    URI:str = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"