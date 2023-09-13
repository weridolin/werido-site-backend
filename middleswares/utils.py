import opentracing
import six
from jaeger_client import Config
from opentracing.ext.tags import *

TRACE_ID = 'trace_id'

REQUEST_ID = 'request_id'

LOGGER = 'logger'

SPAN_KIND_LOG = 'log'

LOG_ERROR = 'log.error'


# Name of the HTTP header used to encode trace ID
DEFAULT_TRACE_ID_HEADER = 'Traceparent' if six.PY3 else b'Traceparent'


def init_tracer(service_name: str, config: dict):
    """
    initialize the global tracer
    :param service_name:
    :param config:
    :return:
    """
    assert isinstance(config, dict)
    # default use `trace_id` replace jaeger `uber-trace-id`
    config['trace_id_header'] = config.get('trace_id_header',DEFAULT_TRACE_ID_HEADER)

    config = Config(config=config, service_name=service_name, validate=True)

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


def format_request_headers(request_meta):
    headers = {}
    for k, v in six.iteritems(request_meta):
        k = k.lower().replace('_', '-')
        if k.startswith('http-'):
            k = k[5:]
            headers[k] = v
        # TODO feature
    return headers


def format_hex_trace_id(trace_id: int):
    return '{:x}'.format(trace_id)


def before_request_trace(tracer, request, view_func):
    """
    Helper function to avoid rewriting for middleware and decorator.
    Returns a new span from the request with logged attributes and
    correct operation name from the view_func.
    """
    # strip headers for trace info
    headers = format_request_headers(request.META)
    print("headers -> ",headers)
    # start new span from trace info
    operation_name = view_func.__name__
    try:
        span_ctx = tracer.extract(opentracing.Format.HTTP_HEADERS, headers)
        scope = tracer.start_active_span(operation_name, child_of=span_ctx)
        print(span_ctx,scope)
    except (opentracing.InvalidCarrierException,
            opentracing.SpanContextCorruptedException):
        scope = tracer.start_active_span(operation_name)
        import traceback
        print(traceback.format_exc())

    span = scope.span
    span.set_tag(COMPONENT, 'Django')
    span.set_tag(TRACE_ID, format_hex_trace_id(span.trace_id))
    span.set_tag(SPAN_KIND, SPAN_KIND_RPC_SERVER)
    span.set_tag(HTTP_METHOD, request.method)
    span.set_tag(HTTP_URL, request.get_full_path())

    request_id = headers.get(REQUEST_ID)
    if request_id:
        span.set_tag(REQUEST_ID, request_id)

    request.scope = scope

    return scope


def after_request_trace(request, response=None, error=None):
    scope = getattr(request, 'scope', None)

    if scope is None:
        return

    if response is not None:
        scope.span.set_tag(HTTP_STATUS_CODE, response.status_code)
    if error is not None:
        scope.span.set_tag(ERROR, True)
        scope.span.log_kv({
            'event': ERROR,
            'error.kind': type(error),
            'error.object': error,
            'error.stack': error.__traceback__,
            'request.headers': format_request_headers(request.META),
            'request.args': request.GET,
            'request.data': request.POST
        })

    scope.close()


def trace(tracer):
    """
    Function decorator that traces functions such as Views
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            before_request_trace(tracer, request, view_func)
            try:
                response = view_func(request, *args, **kwargs)
            except Exception as e:
                after_request_trace(request, error=e)
                raise e
            else:
                after_request_trace(request, response)

            return response

        wrapper.__name__ = view_func.__name__
        return wrapper

    return decorator


