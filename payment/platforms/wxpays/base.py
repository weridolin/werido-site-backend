from oldbackend.payment.platforms.mixins import ConfigMixins,ConfigItem
from requests import Response

# class Account(ConfigMixins):
#     total = ConfigItem(name="total",description="总金额",type=int)
#     currency = ConfigItem(name="currency",description="货币类型",type=str)


class BaseConfig(ConfigMixins):
    # 微信支付配置
    app_id = ConfigItem(name="app_id",description="应用ID",type=str) 
    mch_id = ConfigItem(name="mch_id",description="商户号",type=str) 
    # description = ConfigItem(name="description",description="商品描述",type=str) 
    # notify_url = ConfigItem(name="notify_url",description="通知地址",type=str)
    # out_trade_no = ConfigItem(name="out_trade_no",description="商户订单号",type=str)
    return_url = ConfigItem(name="return_url",description="返回地址",type=str)
    # time_expire  = ConfigItem(name="time_expire",description="订单失效时间",type=str)
    # attach = ConfigItem(name="attach",description="附加数据",type=str)
    # goods_tag = ConfigItem(name="goods_tag",description="商品标记",type=str)
    # support_fapiao = ConfigItem(name="support_fapiao",description="支持开发票",type=bool,default=False)
    # account:Account = ConfigItem(name="account",description="账户",type=Account)
    
def error_handler(res:Response):
    if res.status_code == 403:
        ...
    elif res.status_code == 400:
        ...
    elif res.status_code == 500:
        ...