from core.settings import  ETCD_HOST,ETCD_PORT,USERCENTER_KEY
import etcd3,time

class ETCDClient:
    __cache_map={}
    _instance=None
    # 单例
    def __new__(cls):
        if cls._instance is None:
            cls._instance=super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._client:etcd3.Etcd3Client = etcd3.client(host=ETCD_HOST, port=ETCD_PORT)

    def get(self,key):
        # print(">>> get key: ", self.__cache_map)
        for k,v in self.__cache_map.items():
            if k.startswith(key):
                if isinstance(v,list):
                    # 随机返回一个
                    import random
                    return random.choice(v)
                return v
        try:
            value = self._client.get_prefix(key)
            targets = [target[0].decode() for target in value]
            if targets:
                self.__cache_map.update({key:targets})
                return self.get(key)
        except Exception as e:
            print(e,type(e))
            return None
    
