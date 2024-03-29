# gunicorn.conf
#GRPC 跨进程使用: #https://github.com/grpc/grpc/blob/master/doc/fork_support.md#111
import os
os.environ.setdefault("GRPC_ENABLE_FORK_SUPPORT","1")
import multiprocessing
import threading
import uuid
import socket
import etcd3
from etcd3 import exceptions 
# import opentelemetry.trace as trace
from opentelemetry import trace
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

def post_fork(server, worker):
    print("post fork worker...setting jaeger exporter")
    jaeger_exporter = JaegerExporter(
        agent_host_name="jaeger",
        agent_port= 6831,
    )
    resource = Resource.create(attributes={
        "service.name": "api-old-backend"
    })

    trace.set_tracer_provider(TracerProvider(resource=resource))
    span_processor = BatchSpanProcessor(
        jaeger_exporter
    )
    trace.get_tracer_provider().add_span_processor(span_processor)

    # tracer = trace.get_tracer(__name__)
    # with tracer.start_as_current_span('foo'):
    #     print('Hello world!')

# 并行工作进程数
if os.environ.get('STANDLONE',None) == '1':
    print("only start one worker")
    workers = 1
else:
    workers = multiprocessing.cpu_count() * 2 + 1
# 指定每个工作者的线程数
threads = 2
# 监听内网端口5000
bind = '0.0.0.0:8000'
# 设置守护进程,将进程交给supervisor管理
daemon = 'false'
# 工作模式协程
# worker_class = 'gevent' # 只支持WSGI
worker_class = 'uvicorn.workers.UvicornWorker' # 支持ASGI
# 设置最大并发量
worker_connections = 1000
# 设置进程文件目录
pidfile = 'gunicorn.pid'
# 设置访问日志和错误信息日志路径
accesslog = 'gunicorn_acess.log'
errorlog = 'gunicorn_error.log'
# 设置日志记录水平
loglevel = 'info'

# docker 部署下，服务注册到ETCD 
APP_KEYS = {
    "drug":F"/site/withoutauth/drug/rest/{str(uuid.uuid4())}",
    "home":f"/site/withauth/home/rest/{str(uuid.uuid4())}",
    "blog":f"/site/withauth/blog/rest/{str(uuid.uuid4())}",
    "fileBroker":f"/site/withoutauth/fileBroker/rest/{str(uuid.uuid4())}",
    "dataFaker":f"/site/withoutauth/dataFaker/rest/{str(uuid.uuid4())}",
    "shortUrl":f"/site/withoutauth/shortUrl/rest/{str(uuid.uuid4())}",
    "apiCollector":f"/site/withauth/apiCollector/rest/{str(uuid.uuid4())}",
    "gpt":f"/site/withauth/gpt/rest/{str(uuid.uuid4())}",
    "covid19":f"/site/withoutauth/covid19/rest/{str(uuid.uuid4())}",
    "dataFakerWs":f"/site/withoutauth/dataFaker/ws/{str(uuid.uuid4())}",
    
}

## 注册到 etcd  
#   为什么不放在app的ready中 -> 用gunicorn部署时启动多个worker去运行APP,会产生注册多次的情况
if os.environ.get('K8S',None) != '1':
    def when_ready(server):
        print("gunicorn server started ... begin to register to etcd")
        from core import settings
        etcd = etcd3.client(host=settings.ETCD_HOST, port=settings.ETCD_PORT)
        lease = etcd.lease(20)
        lease.refresh()
        ## 获取服务所在的IP
        # 获取本机计算机名称
        hostname = socket.gethostname()
        # 获取本机ip
        ip = socket.gethostbyname(hostname)
        print(f"local machine ip -> :{ip}")
        for _,value in APP_KEYS.items():
            print(f"register {value} to etcd,value -> http://{ip}:8000")
            etcd.put(value, f'{ip}:8000',lease)
        stop_event = threading.Event()
        stop_event.clear()
        keep_alive_thread = threading.Thread(target=etcd_keep_alive, args=(lease,stop_event,ip))
        keep_alive_thread.start()
        setattr(server, "keep_alive_thread", keep_alive_thread)
        setattr(server, "keep_alive_thread_stop_event", stop_event)
else:
    print("k8s env,not register to etcd")

if os.environ.get('K8S',None) != '1':
    def on_exit(server):
        print("gunicorn server exit ... begin to stop keep alive thread")
        from core import settings
        etcd = etcd3.client(host=settings.ETCD_HOST, port=settings.ETCD_PORT)
        for key in APP_KEYS:
            etcd.delete(key)
        if hasattr(server, "keep_alive_thread_stop_event"):
            getattr(server,"keep_alive_thread_stop_event").set()


def etcd_keep_alive(lease,stop_event:threading.Event,local_ip=None):
    retry_time_count = 0
    while not stop_event.isSet():
        try:
            lease.refresh()
            if retry_time_count > 6:
                ## 重新注册下key
                print("retry register to etcd")
                for _,value in APP_KEYS.items():
                    print(f"register {value} to etcd,value -> http://{local_ip}:8000")
                    etcd_client.put(value, f'{local_ip}:8000',lease)
            retry_time_count = 0
            for _ in range(3):
                if stop_event.isSet():
                    break
                stop_event.wait(1)
        except exceptions.ConnectionFailedError as e:
            from core import settings   
            import traceback
            print("refresh leave error,retry after 3 seconds -> ",e,type(e))
            print(traceback.format_exc())
            stop_event.wait(3)
            etcd_client = etcd3.client(host=settings.ETCD_HOST, port=settings.ETCD_PORT)
            lease.etcd_client = etcd_client
            retry_time_count+=3
            continue
    print("gunicorn server exit ... keep alive thread stop...")

