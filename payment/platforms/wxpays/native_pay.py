from payment.platforms.wxpays.config import NativePayConfig
from payment.platforms.mixins import RequestMixins
from typing import List
import dataclasses
import requests
from oldbackend.payment.const import WX_NATIVE_API
from payment.platforms.wxpays.base import error_handler
import qrcode
from io import BytesIO
from rest_framework.response import Response

@dataclasses.dataclass
class Account(RequestMixins):
    total:int # 总金额
    currency:str # 货币类型

@dataclasses.dataclass
class Detail(RequestMixins):
    ## 商品优惠功能
    cost_price:int = None # 订单原价
    invoice_id:str = None # 商品小票ID
    goods_detail:List

@dataclasses.dataclass
class StoreInfo(RequestMixins):
    ## 商户门店信息
    id:str # 商户门店编号
    name:str=None # 商户门店名称
    area_code:str=None # 地区编码
    address:str=None # 详细街道地址

@dataclasses.dataclass
class SceneInfo(RequestMixins):
    ## 场景信息
    payer_client_ip:str # 用户终端IP
    device_id:str=None # 商户端设备号
    store_info:StoreInfo=None # 商户门店信息

@dataclasses.dataclass
class SettleInfo(RequestMixins):
    # 结算信息  
    profit_sharing:bool # 是否分账

@dataclasses.dataclass
class NativePayRequest(RequestMixins):
    out_trade_no:str # 商户订单号
    time_expire:str=None # 订单失效时间
    attach:str=None # 附加数据
    goods_tag:str=None # 订单优惠商品标记
    support_fapiao:bool=False # 是支持开发票  
    account:Account #订单金额
    detail:Detail = None # 订单优惠功能
    scene_info:SceneInfo = None # 商店门户信息
    settle_info:SettleInfo = None #结算信息
    notify_url:str # 通知地址

@dataclasses.dataclass
class NativePayResponsePayload(RequestMixins):
    code_url:str # 二维码链接,此URL用于生成支付二维码，然后提供给用户扫码支付。

    ##转换为二维码链接
    def to_qrcode(self):
        # 创建二维码对象
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        # 添加数据
        qr.add_data(self.code_url)
        qr.make(fit=True)
        # 生成二维码图片
        img = qr.make_image(fill_color="black", back_color="white")
        # 将二维码图片转换为BytesIO对象
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        # 获取缓冲区中的二进制数据
        qr_code_png = buffer.getvalue()
        return qr_code_png


@dataclasses.dataclass
class NativePayResponse:
    ...

## 生成微信支付订单
def create_native_pay_order(config:NativePayConfig = None,params:NativePayRequest=None) -> Response:
    ##https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter3_4_1.shtml
    config = config or  NativePayConfig.from_env()
    params = params.build_request_params()
    params.update({
        "appid":config.app_id,
        "mch_id":config.mch_id,
        "return_url":config.return_url
    })
    print("生成微信支付订单 -> ",params)
    res = requests.post(
        WX_NATIVE_API,
        json=params,
    )
    return res

