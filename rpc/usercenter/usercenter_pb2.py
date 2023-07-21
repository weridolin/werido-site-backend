# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: usercenter.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10usercenter.proto\x12\x02pb\" \n\x0eGetUserInfoReq\x12\x0e\n\x06userId\x18\x01 \x01(\x03\"\xb3\x01\n\x0fGetUserInfoResp\x12\x0e\n\x06userId\x18\x01 \x01(\x03\x12\x10\n\x08userName\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\x12\x12\n\nuserMobile\x18\x04 \x01(\t\x12\x11\n\tuserEmail\x18\x05 \x01(\t\x12\x12\n\nuserAvatar\x18\x06 \x01(\t\x12\x0b\n\x03\x61ge\x18\x07 \x01(\x03\x12\x0e\n\x06gender\x18\x08 \x01(\x05\x12\x14\n\x0cisSuperAdmin\x18\t \x01(\x08\".\n\x1cGetUserResourcePermissionReq\x12\x0e\n\x06userId\x18\x01 \x01(\x03\"x\n\x13ResourcePermissions\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x12\n\nserverName\x18\x02 \x01(\t\x12\x0b\n\x03url\x18\x03 \x01(\t\x12\x0e\n\x06method\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x0f\n\x07version\x18\x06 \x01(\t\"U\n\x1dGetUserResourcePermissionResp\x12\x34\n\x13resourcePermissions\x18\x01 \x03(\x0b\x32\x17.pb.ResourcePermissions\"*\n\x18GetUserMenuPermissionReq\x12\x0e\n\x06userId\x18\x01 \x01(\x03\"\xa4\x01\n\x0fMenuPermissions\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x10\n\x08menuName\x18\x02 \x01(\t\x12\x15\n\rmenuComponent\x18\x03 \x01(\t\x12\x10\n\x08menuIcon\x18\x04 \x01(\t\x12\x0f\n\x07menuUrl\x18\x05 \x01(\t\x12\x15\n\rmenuRouteName\x18\x06 \x01(\t\x12\x10\n\x08parentId\x18\x07 \x01(\x03\x12\x10\n\x08menuType\x18\x08 \x01(\x05\"I\n\x19GetUserMenuPermissionResp\x12,\n\x0fmenuPermissions\x18\x01 \x03(\x0b\x32\x13.pb.MenuPermissions\"!\n\x10TokenValidateReq\x12\r\n\x05token\x18\x01 \x01(\t\"$\n\x11TokenValidateResp\x12\x0f\n\x07isValid\x18\x01 \x01(\x08\x32\xba\x02\n\nusercenter\x12\x36\n\x0bgetUserInfo\x12\x12.pb.GetUserInfoReq\x1a\x13.pb.GetUserInfoResp\x12`\n\x19getUserResourcePermission\x12 .pb.GetUserResourcePermissionReq\x1a!.pb.GetUserResourcePermissionResp\x12T\n\x15getUserMenuPermission\x12\x1c.pb.GetUserMenuPermissionReq\x1a\x1d.pb.GetUserMenuPermissionResp\x12<\n\rtokenValidate\x12\x14.pb.TokenValidateReq\x1a\x15.pb.TokenValidateRespB\x06Z\x04./pbb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'usercenter_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\004./pb'
  _globals['_GETUSERINFOREQ']._serialized_start=24
  _globals['_GETUSERINFOREQ']._serialized_end=56
  _globals['_GETUSERINFORESP']._serialized_start=59
  _globals['_GETUSERINFORESP']._serialized_end=238
  _globals['_GETUSERRESOURCEPERMISSIONREQ']._serialized_start=240
  _globals['_GETUSERRESOURCEPERMISSIONREQ']._serialized_end=286
  _globals['_RESOURCEPERMISSIONS']._serialized_start=288
  _globals['_RESOURCEPERMISSIONS']._serialized_end=408
  _globals['_GETUSERRESOURCEPERMISSIONRESP']._serialized_start=410
  _globals['_GETUSERRESOURCEPERMISSIONRESP']._serialized_end=495
  _globals['_GETUSERMENUPERMISSIONREQ']._serialized_start=497
  _globals['_GETUSERMENUPERMISSIONREQ']._serialized_end=539
  _globals['_MENUPERMISSIONS']._serialized_start=542
  _globals['_MENUPERMISSIONS']._serialized_end=706
  _globals['_GETUSERMENUPERMISSIONRESP']._serialized_start=708
  _globals['_GETUSERMENUPERMISSIONRESP']._serialized_end=781
  _globals['_TOKENVALIDATEREQ']._serialized_start=783
  _globals['_TOKENVALIDATEREQ']._serialized_end=816
  _globals['_TOKENVALIDATERESP']._serialized_start=818
  _globals['_TOKENVALIDATERESP']._serialized_end=854
  _globals['_USERCENTER']._serialized_start=857
  _globals['_USERCENTER']._serialized_end=1171
# @@protoc_insertion_point(module_scope)
