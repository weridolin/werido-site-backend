
import os
import sys
import json
from utils.redis_keys import WECHAT
from django_redis import get_redis_connection
from redis.client import Redis
from utils.redis_keys import WECHAT, Weather

DEFAULT_REPLY_CONTENT = """查询内容格式有误,暂时只支持 [功能]:[参数1],[参数2].例如: 天气:广州,揭阳 """

TEXT_REPLY_XML_TEMPLATE = """
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


CITY_ADCODE = dict()
with open(os.path.join(os.path.dirname(__file__), "city_adcode.json"), "r") as f:
    CITY_ADCODE = json.load(f)


def text_msg_handler(to: str, from_: str, content: str):
    try:
        query_type, params = content.split(":", 1)
        if query_type == "天气":
            city_list = params.split(",")
            conn: Redis = get_redis_connection()
            res = ""
            for city_cn_name in city_list:
                city_adcode = CITY_ADCODE.get("city_cn_name")
                if not city_adcode:
                    res = f"输入的查询参数:{params}有误"
                    break
                info = conn.get(Weather.get_city_weather_key(city_adcode))
                res += f"""[{city_cn_name}] 天气:{json.dumps(info)}\n"""
            content = res

    except Exception as exc:
        print(">>>  处理微信文本消息异常", str(exc))
        content = DEFAULT_REPLY_CONTENT

    return TEXT_REPLY_XML_TEMPLATE.format(
        to=to,
        from_=from_,
        content=content
    )
