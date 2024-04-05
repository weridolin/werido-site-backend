import pika
from pika import DeliveryMode
from pika.exchange_type import ExchangeType
import os


def get_client():
    credentials = pika.PlainCredentials(os.environ.get('RABBITMQ_DEFAULT_USER','werido'), os.environ.get('RABBITMQ_DEFAULT_PASS','359066432'))
    parameters = pika.ConnectionParameters(os.environ.get("RABBITMQ_SVC_NAME",'www.weridolin.cn'),
        os.environ.get("RABBITMQ_PORT",30003), 
        credentials=credentials,
        virtual_host='/',
        heartbeat=60,  # 设置心跳周期，防止网络故障导致的假死
        blocked_connection_timeout=300,  # 当连接被服务器阻塞时的超时时间
        connection_attempts=3,  # 连接失败后的重试次数
        retry_delay=5,  # 两次连接尝试之间的延迟
        socket_timeout=10,  # 套接字操作超时时间
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    return channel

def public_message(exchange, routing_key, message):
    client = get_client()
    client.exchange_declare(exchange=exchange,
        exchange_type=ExchangeType.topic,
        durable=True,
        auto_delete=False)
    client.basic_publish(
        exchange=exchange, 
        routing_key=routing_key, 
        body=message, 
        properties=pika.BasicProperties(delivery_mode=DeliveryMode.Persistent))
    print(f"send message to {exchange} with routing key {routing_key} message -> {message}")
    return True

