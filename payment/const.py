WX_NATIVE_API = "https://api.mch.weixin.qq.com/v3/pay/transactions/native"
WX_PAY_CALLBACK = "https://api.mch.weixin.qq.com/v3/pay/transactions/out-trade-no/{out_trade_no}/callback"
WX_PUBLIC_ERROR = {
    403: {
        "desc":"交易错误",
        "solve":"因业务原因交易失败，请查看接口返回的详细信息 "
    },
    400: {
        "desc":"请求参数错误",
        "solve":"请根据接口返回的详细信息检查请求参数 "
    },
    500: {
        "desc":"系统错误",
        "solve":"系统异常，请用相同参数重新调用"
    },
    
}

PAY_CHANNEL = {
    "wxpay":"微信支付",
    "alipay":"支付宝支付",
    "applepay":"苹果支付",
    "unionpay":"银联支付",
    "paypal":"PayPal支付",
    "stripe":"Stripe支付",
    "other":"其他支付",
}

PAY_STATUS = {
    "unpay":"未支付",
    "success":"支付成功",
    "failed":"支付失败",
    "cancel":"支付取消",
    "refund":"支付退款",
    "other":"其他支付状态"
}

CALLBACK_STATUS = {
    "uncallback":"未回调",
    "callback":"已回调",
    "failed":"回调失败",
}