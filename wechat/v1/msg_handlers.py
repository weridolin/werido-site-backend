
DEFAULT_REPLY_CONTENT  = """查询内容格式有误,暂时只支持 [查询内容]:[查询参数的格式].例如: 天气:广州 """

TEXT_REPLY_XML_TEMPLATE="""
    <xml>
        <ToUserName><![CDATA[{to}]]></ToUserName>
        <FromUserName><![CDATA[{from_}]]></FromUserName>
        <CreateTime>12345678</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{content}]]></Content>
    </xml>
"""


def text_msg_handler(to:str,from_:str,content:str):

    # try:
    #     query_type,params = content.split(":",1)
    # except Exception as exc:
    return TEXT_REPLY_XML_TEMPLATE.format(
        to=to,
        from_=from_,
        content=DEFAULT_REPLY_CONTENT
    )