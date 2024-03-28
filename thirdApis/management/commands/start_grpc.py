from django.core.management.base import BaseCommand
import asyncio,os
import grpc
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
from thirdApis.gpt import gpt_pb2_grpc
from thirdApis.gpt.apis import GptMessageRpcImpl

_cleanup_coroutines = []

async def serve(addr:str):
    server = grpc.aio.server()
    
    gpt_pb2_grpc.add_GptMessageServicer_to_server(GptMessageRpcImpl(), server)
    server.add_insecure_port('[::]:50001')  # 设置gRPC服务端口
    await server.start()
    print(f"gRPC server started on address {addr}")

    
    async def server_graceful_shutdown():
        print("Starting graceful shutdown...")
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(5)

    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()


class Command(BaseCommand):

    help = 'start grpc server'
    def add_arguments(self, parser):
        # 添加任何命令行参数
        parser.add_argument('--addr', type=str, help='grpc server address')

    def handle(self, *args, **options):
        # input_value = options['input']
        addr = options['addr']
        loop = asyncio.get_event_loop()
        # stop = loop.create_future()
        # loop.create_task(serve(addr))

        try:
            loop.run_until_complete(serve(addr))
        finally:
            loop.run_until_complete(*_cleanup_coroutines)
            loop.close()