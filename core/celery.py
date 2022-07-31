import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('site')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.autodiscover_tasks()

import smtplib
import datetime
from core import settings
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
from jinja2 import Environment

@app.task
def send_welcome_mail(receiver,number):
        # host = getattr(settings,"EMAIL_HOST","smtp.qq.com")  
        # mail_user = getattr(settings,"EMAIL_USER","weridolin@qq.com")   # 密码(部分邮箱为授权码)
        mail_pass = os.environ.get("EMAIL_PWD",None)   # 邮件发送方邮箱地址
        host = "smtp.qq.com"
        mail_user = "weridolin@qq.com"   
        sender = mail_user
        # receivers = ["359066432@qq.com;notification@ibrpa.com"]  # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        receiver =[f"{receiver};{sender}"]
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),"templates", "email_notice.html"), encoding="utf-8") as f:
            mail_body = f.read()
        
        mail_body = Environment().from_string(mail_body).render(
        date=datetime.datetime.now().strftime('%Y-%m-%d'),
        number=number)
    
        message = MIMEMultipart("alternative")
        message.attach(MIMEText(mail_body, _subtype='html', _charset='utf-8'))
        
        content_img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"static", "content.jpg")
        if os.path.exists(content_img_path):
            with open(content_img_path, "rb") as f:
                img = MIMEImage(f.read())
            img.add_header("Content-ID", "<content>")
            message.attach(img)

        message['Subject'] = Header("注册成功","utf-8") # 发送方信息
        message['From'] = Header("林叔叔是个怪叔叔","utf-8")  # 接受方信息
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

