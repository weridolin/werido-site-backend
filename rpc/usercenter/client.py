from rpc.usercenter import client
from rpc.usercenter import usercenter_pb2 
from rpc.usercenter import usercenter_pb2_grpc 
import os
import grpc


def get_user_info(user_id,target) -> usercenter_pb2.GetUserInfoResp:
    with grpc.insecure_channel(target) as channel:
        stub = usercenter_pb2_grpc.usercenterStub(channel)
        response = stub.getUserInfo(usercenter_pb2.GetUserInfoReq(userId=int(user_id))) 
        return response
    


def get_user_menu_permission(user_id,target) -> usercenter_pb2.GetUserMenuPermissionResp:
    with grpc.insecure_channel(target) as channel:
        stub = usercenter_pb2_grpc.usercenterStub(channel)
        response = stub.getUserMenuPermission(usercenter_pb2.GetUserMenuPermissionReq(user_id=user_id)) 
        return response


def get_user_resource_permission(user_id) -> usercenter_pb2.GetUserResourcePermissionResp:
    with grpc.insecure_channel(target) as channel:
        stub = usercenter_pb2_grpc.usercenterStub(channel)
        response = stub.getUserResourcePermission(usercenter_pb2.GetUserResourcePermissionReq(user_id=user_id)) 
        return response
    

def is_token_valid(token,target) -> usercenter_pb2.TokenValidateResp:
    with grpc.insecure_channel(target) as channel:
        stub = usercenter_pb2_grpc.usercenterStub(channel)
        response = stub.tokenValidate(usercenter_pb2.TokenValidateReq(token=token)) 
        return response
    
def get_multiple_user_info(user_ids,target) -> usercenter_pb2.GetMutipleUserInfoResp:
    with grpc.insecure_channel(target) as channel:
        stub = usercenter_pb2_grpc.usercenterStub(channel)
        response = stub.getMultipleUserInfo(usercenter_pb2.GetMultipleUserInfoReq(user_ids=user_ids)) 
        return response