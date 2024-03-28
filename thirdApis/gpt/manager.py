import logging

logger = logging.getLogger(__name__)

class GptReqManager:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(GptReqManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        self.req_map = dict()

    def register_req(self,uuid,conn):
        if  uuid not in self.req_map:
            self.req_map[uuid] = conn
        else:
            logger.error(f"uuid {uuid} already exists,try to stop...")
            self.get_req(uuid).stop()
            self.req_map[uuid] = conn

    def remove_req(self,uuid):
        if uuid in self.req_map:
            del self.req_map[uuid]
        
    def get_req(self,uuid):
        return self.req_map.get(uuid,None)

    def stop_req(self,uuid):
        req = self.get_req(uuid)
        if req:
            req.stop()
            self.remove_req(uuid)
            return True
        return False

__manager = None    

def get_manager():
    global __manager
    if __manager is None:
        __manager = GptReqManager()
    return __manager
