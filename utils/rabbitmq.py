import pika
from pika import DeliveryMode
from pika.exchange_type import ExchangeType

__instance = None

def get_client():
    global __instance
    if not __instance:
        credentials = pika.PlainCredentials('werido', '359066432')
        parameters = pika.ConnectionParameters('www.weridolin.cn',
            30003, 
            credentials=credentials,
            virtual_host='/',
            heartbeat=2,)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        __instance = channel
    return __instance

def public_message(exchange, routing_key, message):
    # credentials = pika.PlainCredentials('werido', '359066432')
    # parameters = pika.ConnectionParameters('www.weridolin.cn',30003, credentials=credentials)
    # connection = pika.BlockingConnection(parameters)
    # client = connection.channel()
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

