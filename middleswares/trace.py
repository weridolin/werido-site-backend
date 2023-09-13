from core import settings
try:
    # Django >= 1.10
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object
from middleswares.utils import *
from opentelemetry.sdk.trace import Tracer

"""
00-480e22a2781fe54d992d878662248d94-b4b37b64bb3f6141-00

version: 8 位，系统适配的追踪上下文版本，当前位 00
trace-id: 16 字节，追踪整体的标识。用于在系统中标识一个分布式追踪整体。
parent-id/span-id: 8 字节，用来表述在进入请求中，或者对外请求中，当前跨度的父级。
trace-flags: 8 位，调用者的建议标志，可以考虑为调用者的建议，限制为 3 个原因：信息或是滥用，调用方的错误，或者在调用方与被调用方的不同负载。


"""

from opentelemetry import trace
from rest_framework.response import Response
from django.http import HttpRequest
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.trace.propagation import _SPAN_KEY
from opentelemetry import context as context_api
from opentelemetry.trace.span import Span
from opentelemetry.trace import StatusCode, Status
from opentelemetry.trace import SpanKind
from utils.http_ import HTTPResponse
import traceback
import json

def use_span(
    span: Span,
    record_exception: bool = True,
    set_status_on_exception: bool = True,
):
    """
        参考:trace.use_span,返回改成token

    """
    try:
        token = context_api.attach(context_api.set_value(_SPAN_KEY, span))
        # try:
        #     yield span
        # finally:
        #     context_api.detach(token)
        return token
    except Exception as exc:  # pylint: disable=broad-except
        if isinstance(span, Span) and span.is_recording():
            # Record the exception as an event
            if record_exception:
                span.record_exception(exc)
            # Set status in case exception was raised
            if set_status_on_exception:
                span.set_status(
                    Status(
                        status_code=StatusCode.ERROR,
                        description=f"{type(exc).__name__}: {exc}",
                    )
                )
        raise


class OpenTracingMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.span = None
        self.tracer = trace.get_tracer(__name__)
        super().__init__(get_response)

    def process_view(self, request, view_func, view_args, view_kwargs):
        headers = format_request_headers(request.META)
        ctx = TraceContextTextMapPropagator().extract(headers)
        self.span = self.tracer.start_span(name=request.path, context=ctx)
        self.token = use_span(self.span)
        request.span = self.span
        self.span.set_attributes({
            "http.method": request.method,
            "http.server_name": "rest-old-site-backend",
            "http.scheme":request.scheme,
            "host.port": 8000,
            "http.host": request.get_host(),
            "http.url": request.get_full_path(),
            "http.peer.addr":headers.get("x-real-ip","")
        })
        

    def process_exception(self, request, exception:Exception):
        """
            process a exception
        """
        # print(">>>>",exception,type(exception))
        self.span.set_attribute("http.status_code",500)
        self.span.set_attribute("http.err_msg",str(exception) or "")
        import traceback
        self.span.set_attribute("http_err_stack",traceback.format_exc())
        self.span.end()
        context_api.detach(self.token)

    def process_response(self, request, response: HTTPResponse):
        if isinstance(response,HTTPResponse):
            self.span.set_attribute("http.status_code",response.status_code)
            self.span.set_attribute("http.res_msg",response.data.get('message',None) or "")    
            self.span.set_attribute("http.response.data",json.dumps(response.data) if response.data else "")   
        carrier = dict()
        TraceContextTextMapPropagator().inject(carrier)
        self.span.end()
        context_api.detach(self.token)
        # print("carrier", carrier,type(response))
        if 'traceparent' in carrier.keys():
            response['Traceparent']=carrier.get('traceparent')
        return response
