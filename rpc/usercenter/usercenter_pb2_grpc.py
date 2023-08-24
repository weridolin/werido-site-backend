# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import usercenter_pb2 as usercenter__pb2


class usercenterStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getUserInfo = channel.unary_unary(
                '/pb.usercenter/getUserInfo',
                request_serializer=usercenter__pb2.GetUserInfoReq.SerializeToString,
                response_deserializer=usercenter__pb2.GetUserInfoResp.FromString,
                )
        self.getUserResourcePermission = channel.unary_unary(
                '/pb.usercenter/getUserResourcePermission',
                request_serializer=usercenter__pb2.GetUserResourcePermissionReq.SerializeToString,
                response_deserializer=usercenter__pb2.GetUserResourcePermissionResp.FromString,
                )
        self.getUserMenuPermission = channel.unary_unary(
                '/pb.usercenter/getUserMenuPermission',
                request_serializer=usercenter__pb2.GetUserMenuPermissionReq.SerializeToString,
                response_deserializer=usercenter__pb2.GetUserMenuPermissionResp.FromString,
                )
        self.tokenValidate = channel.unary_unary(
                '/pb.usercenter/tokenValidate',
                request_serializer=usercenter__pb2.TokenValidateReq.SerializeToString,
                response_deserializer=usercenter__pb2.TokenValidateResp.FromString,
                )
        self.getMutipleUserInfo = channel.unary_unary(
                '/pb.usercenter/getMutipleUserInfo',
                request_serializer=usercenter__pb2.GetMutipleUserInfoReq.SerializeToString,
                response_deserializer=usercenter__pb2.GetMutipleUserInfoResp.FromString,
                )


class usercenterServicer(object):
    """Missing associated documentation comment in .proto file."""

    def getUserInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getUserResourcePermission(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getUserMenuPermission(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def tokenValidate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getMutipleUserInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_usercenterServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getUserInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.getUserInfo,
                    request_deserializer=usercenter__pb2.GetUserInfoReq.FromString,
                    response_serializer=usercenter__pb2.GetUserInfoResp.SerializeToString,
            ),
            'getUserResourcePermission': grpc.unary_unary_rpc_method_handler(
                    servicer.getUserResourcePermission,
                    request_deserializer=usercenter__pb2.GetUserResourcePermissionReq.FromString,
                    response_serializer=usercenter__pb2.GetUserResourcePermissionResp.SerializeToString,
            ),
            'getUserMenuPermission': grpc.unary_unary_rpc_method_handler(
                    servicer.getUserMenuPermission,
                    request_deserializer=usercenter__pb2.GetUserMenuPermissionReq.FromString,
                    response_serializer=usercenter__pb2.GetUserMenuPermissionResp.SerializeToString,
            ),
            'tokenValidate': grpc.unary_unary_rpc_method_handler(
                    servicer.tokenValidate,
                    request_deserializer=usercenter__pb2.TokenValidateReq.FromString,
                    response_serializer=usercenter__pb2.TokenValidateResp.SerializeToString,
            ),
            'getMutipleUserInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.getMutipleUserInfo,
                    request_deserializer=usercenter__pb2.GetMutipleUserInfoReq.FromString,
                    response_serializer=usercenter__pb2.GetMutipleUserInfoResp.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'pb.usercenter', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class usercenter(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def getUserInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.usercenter/getUserInfo',
            usercenter__pb2.GetUserInfoReq.SerializeToString,
            usercenter__pb2.GetUserInfoResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getUserResourcePermission(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.usercenter/getUserResourcePermission',
            usercenter__pb2.GetUserResourcePermissionReq.SerializeToString,
            usercenter__pb2.GetUserResourcePermissionResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getUserMenuPermission(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.usercenter/getUserMenuPermission',
            usercenter__pb2.GetUserMenuPermissionReq.SerializeToString,
            usercenter__pb2.GetUserMenuPermissionResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def tokenValidate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.usercenter/tokenValidate',
            usercenter__pb2.TokenValidateReq.SerializeToString,
            usercenter__pb2.TokenValidateResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getMutipleUserInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.usercenter/getMutipleUserInfo',
            usercenter__pb2.GetMutipleUserInfoReq.SerializeToString,
            usercenter__pb2.GetMutipleUserInfoResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)