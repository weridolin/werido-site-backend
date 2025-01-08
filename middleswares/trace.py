# trace.py

from core import settings
try:
    # Django >= 1.10
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object
from middleswares.utils import *

"""
00-480e22a2781fe54d992d878662248d94-b4b37b64bb3f6141-00

version: 8 位，系统适配的追踪上下文版本，当前位 00
trace-id: 16 字节，追踪整体的标识。用于在系统中标识一个分布式追踪整体。
parent-id/span-id: 8 字节，用来表述在进入请求中，或者对外请求中，当前跨度的父级。
trace-flags: 8 位，调用者的建议标志，可以考虑为调用者的建议，限制为 3 个原因：信息或是滥用，调用方的错误，或者在调用方与被调用方的不同负载。


"""

from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.trace.propagation import _SPAN_KEY
from opentelemetry import context as context_api
from opentelemetry.trace.span import Span
from opentelemetry.trace import StatusCode, Status
from opentelemetry.trace import SpanKind
from utils.http_ import HTTPResponse
import traceback
import json
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.proto.grpc import JaegerExporter
import os


class OpenTracingMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response
        # 初始化 TracerProvider
        trace.set_tracer_provider(TracerProvider())
        # 从环境变量中读取 Jaeger gRPC 端点
        jaeger_endpoint = os.getenv("JAEGER_ENDPOINT", "jaeger:14250")
        print(f"Using Jaeger endpoint: {jaeger_endpoint}")
        # 创建 Jaeger 导出器
        jaeger_exporter = JaegerExporter(
            collector_endpoint=jaeger_endpoint,
            insecure=True
        )
        # 创建 BatchSpanProcessor 并添加导出器
        span_processor = BatchSpanProcessor(jaeger_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)
        self.tracer = trace.get_tracer(__name__)
        super().__init__(get_response)

    def process_view(self, request, view_func, view_args, view_kwargs):
        headers = format_request_headers(request.META)
        ctx = TraceContextTextMapPropagator().extract(headers) # 生成上下文
        self.span = self.tracer.start_span(name=request.path, context=ctx) # 开启记录一个新的span
        self.token = context_api.attach(ctx)
        carrier = dict()
        TraceContextTextMapPropagator().inject(carrier)
        print("trace middleware carrier ->",carrier)
        if 'traceparent' in carrier.keys():
            request.traceparent = carrier.get('traceparent')
            request.span = self.span
            self.span.set_attributes({
                "http.method": request.method,
                "http.server_name": "rest-old-site-backend",
                "http.scheme": request.scheme,
                "host.port": 8000,
                "http.host": request.get_host(),
                "http.url": request.get_full_path(),
                "http.peer.addr": headers.get("x-real-ip", ""),
                "span.kind": SpanKind.INTERNAL.name,
            })

        # # 调用视图函数
        # response = self.get_response(request)

        # return response

    def process_exception(self, request, exception: Exception):
        """
            process a exception
        """
        if hasattr(request, 'span'):
            span = request.span
            span.set_attribute("error", True)
            span.set_attribute("otel.status_code", StatusCode.ERROR.value)
            span.set_attribute("http.err_msg", str(exception) or "")
            import traceback
            span.set_attribute("http_err_stack", traceback.format_exc())
            span.end()
            if hasattr(self, 'token'):
                context_api.detach(self.token)

    def process_response(self, request, response: HTTPResponse):
        if hasattr(request, 'span'):
            span = request.span
            if isinstance(response, HTTPResponse):
                span.set_attribute("otel.status_code", response.status_code)
                span.set_attribute("http.res_msg", response.data.get('message', None) or "")
                span.set_attribute("http.response.data", json.dumps(response.data) if response.data else "") 
            carrier = dict()
            TraceContextTextMapPropagator().inject(carrier)
            span.end()
            if hasattr(self, 'token'):
                context_api.detach(self.token)
            if 'traceparent' in carrier.keys():
                response['Traceparent'] = carrier.get('traceparent')
        return response