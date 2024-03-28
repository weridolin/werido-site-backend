from rest_framework.decorators import action,api_view
from utils.helper import parse_ip,parse_user_agent,nativeTime2utcTime
from rest_framework.viewsets import ModelViewSet
from payment.models import Reward
from authenticationV1 import V1Authentication
from permission import V1IsAdminUser
from payment.const import PAY_CHANNEL,WX_PAY_CALLBACK
from utils.http_ import HTTPResponse
from rest_framework import status
from payment.platforms.wxpays.native_pay import create_native_pay_order,NativePayRequest,NativePayResponsePayload
import datetime,json
import uuid
from rest_framework.response import Response


class RewordApis(ModelViewSet):
    queryset = Reward.objects.all()
    authentication_classes = [V1Authentication]
    permission_classes = [V1IsAdminUser]

## 
@api_view(['GET'])
def reward_by_button(request):
    """
        通过普通按钮发送奖励,根据支付类型返回对应的支付链接二维码
    """
    pay_channel = request.query_params.get("pay_channel")
    amount = request.query_params.get("amount","5.00")
    pay_note= request.query_params.get("pay_note","")
    # 过期时间当前时间+15分钟
    expire_time = datetime.datetime.now() + datetime.timedelta(minutes=15)

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    location = parse_ip(ip=ip) or dict()
    ua,device = parse_user_agent(request.META.get('HTTP_USER_AGENT'))
    if not pay_channel or pay_channel not in PAY_CHANNEL.keys():
        return HTTPResponse(400, "支付类型错误")
    else:
        uuid = str(uuid.uuid4())
        if pay_channel == "wxpay":
            ## 先创建订单
            try:
                reward_order = Reward.objects.create(
                        id=uuid,
                        pay_channel=pay_channel,
                        amount=amount,
                        pay_status="unpay",
                        pay_note=pay_note,
                        expire_time=expire_time,
                        pay_ip=ip,
                        pay_location=json.dumps(location,ensure_ascii=False),
                        pay_callback=WX_PAY_CALLBACK.format(out_trade_no=uuid),
                        pay_callback_status="uncallback",
                        pay_device=device,
                        pay_user_agent=ua,
                        expire_time=expire_time
                    )
                ## 想微信支付平台发送请求
                request_params = NativePayRequest(
                    out_trade_no=uuid,
                    amount=amount,
                    attach="打赏",
                    notify_url=WX_PAY_CALLBACK.format(out_trade_no=uuid),
                    time_expire=nativeTime2utcTime(expire_time.strftime("%Y-%m-%d %H:%M:%S")),
                )
                res:Response = create_native_pay_order(request_params=request_params)
                if res.status_code == 200:
                    ## 拿到返回的支付链接
                    data:NativePayResponsePayload = NativePayResponsePayload.from_dict(res.json())
                    return HTTPResponse(data=data.to_qrcode(),content_type="image/png")
                else:
                    return HTTPResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        message=f"创建订单失败:{res.content}")
            except Exception as e:
                return HTTPResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR,message=f"创建订单失败:{e}")
        elif pay_channel == "alipay":
            return HTTPResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR,message="暂不支持")
        
@api_view(['GET'])
def union_pay(request):
    """
        聚合支付
    """
    pass