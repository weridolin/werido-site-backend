from typing import Any
import dataclasses  
import os

@dataclasses.dataclass
class ConfigItem:
    name: str 
    env_name:str = None
    default: Any = None
    description: str = None
    type: Any = str

    def __post_init__(self, env_name=None):
        if env_name is None:
            self.env_name = self.name.upper()
    
    def from_env(self):
        if hasattr(self.type, "from_env"):
            return self.type.from_env()
        return self._get_env_value()

    def _get_env_value(self):
        return os.getenv(self.env_name, self.default)     


class ConfigMixins:

    @classmethod
    def from_env(cls):
        instance = cls()
        for _, v in cls.__dict__.items():
            if isinstance(v, ConfigItem):
                setattr(instance, v.name, v.from_env())
        return instance
    
class RequestMixins:
    
    def build_request_params(self):
        if not isinstance(self, dataclasses.dataclass):
            raise TypeError("RequestMixins must be used with dataclass")
        return {k: v for k, v in dataclasses.asdict(self).items() if v is not None}
    

    def from_dict(self, data:dict):
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
        return self