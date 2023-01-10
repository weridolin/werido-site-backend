
DEFAULT_REPLY_CONTENT  = """查询内容格式有误,暂时只支持 [功能]:[参数1],[参数2].例如: 天气:广州,揭阳 """

TEXT_REPLY_XML_TEMPLATE="""
    <xml>
        <ToUserName><![CDATA[{to}]]></ToUserName>
        <FromUserName><![CDATA[{from_}]]></FromUserName>
        <CreateTime>12345678</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{content}]]></Content>
    </xml>
"""


WELCOME_CONETENT = """感谢关注!您可以输入[功能]:[参数1],[参数2]的形式,获取对应的信息.
例如: 天气:广州
"""

from redis.client import Redis
from django_redis import get_redis_connection
from utils.redis_keys import WECHAT
def text_msg_handler(to:str,from_:str,content:str):
    try:
        query_type,params = content.split(":",1)
        if query_type=="天气":
            conn:Redis = get_redis_connection() 
    except Exception as exc:
        return TEXT_REPLY_XML_TEMPLATE.format(
            to=to,
            from_=from_,
            content=DEFAULT_REPLY_CONTENT
        )