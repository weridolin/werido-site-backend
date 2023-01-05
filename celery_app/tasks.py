import time
import asyncio
from redis.client import Redis
from django_redis import get_redis_connection
from jinja2 import Environment
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import datetime
import smtplib
import os
import sys
import json
from core.celery import app
# import requests
from datetime import timedelta
from utils.redis_keys import WECHAT, Weather
from utils.exceptions import ResponseError
from functools import partial

@app.task(name="celeryTask.resource.remove_file")
def remove_file(file_path):
    if isinstance(file_path, list):
        for path in file_path:
            if os.path.exists(path):
                os.remove(path)
    else:
        if os.path.exists(file_path):
            os.remove(file_path)


@app.task(name="celeryTask.auth.send_welcome_email_after_register")
def send_welcome_mail(receiver, number):
    # host = getattr(settings,"EMAIL_HOST","smtp.qq.com")
    # mail_user = getattr(settings,"EMAIL_USER","weridolin@qq.com")   # 密码(部分邮箱为授权码)
    mail_pass = os.environ.get("EMAIL_PWD", None)   # 邮件发送方邮箱地址
    host = "smtp.qq.com"
    mail_user = "weridolin@qq.com"
    sender = mail_user
    # receivers = ["359066432@qq.com;notification@ibrpa.com"]  # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receiver = [f"{receiver};{sender}"]
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "email_notice.html"), encoding="utf-8") as f:
        mail_body = f.read()

    mail_body = Environment().from_string(mail_body).render(
        date=datetime.datetime.now().strftime('%Y-%m-%d'),
        number=number)

    message = MIMEMultipart("alternative")
    message.attach(MIMEText(mail_body, _subtype='html', _charset='utf-8'))

    content_img_path = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), "static", "content.jpg")
    if os.path.exists(content_img_path):
        with open(content_img_path, "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", "<content>")
        message.attach(img)

    message['Subject'] = Header("注册成功", "utf-8")  # 发送方信息
    message['From'] = Header("林叔叔是个怪叔叔", "utf-8")  # 接受方信息
    message['To'] = ','.join(receiver)   # 登录并发送邮件

    # import time
    # time.sleep(10)
    try:
        conn = smtplib.SMTP_SSL(host=host, port=465)  # 连接到服务器
        # smtpObj.connect(host,25) #登录到服务器
        conn.login(mail_user, mail_pass)  # 发送
        conn.sendmail(sender, receiver, message.as_string())  # 退出
    except Exception as e:
        raise
    finally:
        conn.quit()


@app.task(name="celeryTask.wechat.refresh_wechat_token")
def refresh_wechat_token():
    import requests
    res = requests.get(
        url="https://api.weixin.qq.com/cgi-bin/token",
        params={
            "grant_type": "client_credential",
            "appid": os.environ.get("WECHAT_APP_ID"),
            "secret": os.environ.get("WECHAT_APP_SECRET")
        }
    )
    if res.json().get("errcode") == 0:
        access_token = res.json().get("access_token")
        expire_in = res.json().get("expires_in")
        conn: Redis = get_redis_connection()
        access_token = conn.set(
            name=WECHAT.access_token_key(),
            value=access_token,
            ex=expire_in-5*60
        )
        print(">>> refresh token success", access_token)

    else:
        err_msg = {
            -1: "系统繁忙，此时请开发者稍候再试",
            40001: "AppSecret错误或者 AppSecret 不属于这个公众号，请开发者确认 AppSecret 的正确性",
            40002: "请确保grant_type字段值为client_credential",
            40164: "调用接口的 IP 地址不在白名单中，请在接口 IP 白名单中进行设置.",
            89503: "此 IP 调用需要管理员确认,请联系管理员.",
            89501: "此 IP 正在等待管理员确认,请联系管理员.",
            89506: "24小时内该 IP 被管理员拒绝调用两次,24小时内不可再使用该 IP 调用",
            89507: "1小时内该 IP 被管理员拒绝调用一次,1小时内不可再使用该 IP 调用"
        }
        print(">>> celery task error", err_msg.get(res.json().get("errcode")))


@app.task(name="celeryTask.wechat.get_city_weather",bind=True)
def get_city_weather(self):
    import gevent
    from gevent import monkey
    monkey.patch_all()
    import requests

    def callback(gl,city_id=None):
        res = gl.value
        if not isinstance(res,requests.Response):
            print(">>> 返回的响应类型错误")
            # raise self.retry("返回的响应类型错误",countdown=1)
        if res.status_code>=300:
            print(">>> 请求失败")
            # raise self.retry("请求失败",countdown=1)
        else:
            print(res.json())
            conn: Redis = get_redis_connection()
            conn.set(
                name=Weather.get_city_weather_key(city_id),
                value=json.dumps(res.json()),
                ex=24*60*60
        )
    print(">>> start get weather",datetime.datetime.now())
    with open(os.path.join(os.path.dirname(__file__),"city.json"),"r") as f:
        city_infos = json.load(f)

        for city in city_infos:
            gl = gevent.spawn(requests.get,
                f"https://v0.yiketianqi.com/api",
                {
                    "appid": os.environ.get("WEATHER_API_APP_ID"),
                    "appsecret": os.environ.get("WEATHER_API_APP_SECRET"),
                    "version": "v62",
                    "cityid": city["id"]
                }
            )
            gl.link_value(callback=partial(callback,city_id=city["id"]))
    print(">>> finish get weather",datetime.datetime.now())
