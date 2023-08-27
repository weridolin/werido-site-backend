# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: usercenter.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='usercenter.proto',
  package='pb',
  syntax='proto3',
  serialized_options=b'Z\004./pb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x10usercenter.proto\x12\x02pb\" \n\x0eGetUserInfoReq\x12\x0e\n\x06userId\x18\x01 \x01(\x03\"\xb3\x01\n\x0fGetUserInfoResp\x12\x0e\n\x06userId\x18\x01 \x01(\x03\x12\x10\n\x08userName\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\x12\x12\n\nuserMobile\x18\x04 \x01(\t\x12\x11\n\tuserEmail\x18\x05 \x01(\t\x12\x12\n\nuserAvatar\x18\x06 \x01(\t\x12\x0b\n\x03\x61ge\x18\x07 \x01(\x03\x12\x0e\n\x06gender\x18\x08 \x01(\x05\x12\x14\n\x0cisSuperAdmin\x18\t \x01(\x08\".\n\x1cGetUserResourcePermissionReq\x12\x0e\n\x06userId\x18\x01 \x01(\x03\"x\n\x13ResourcePermissions\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x12\n\nserverName\x18\x02 \x01(\t\x12\x0b\n\x03url\x18\x03 \x01(\t\x12\x0e\n\x06method\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x0f\n\x07version\x18\x06 \x01(\t\"U\n\x1dGetUserResourcePermissionResp\x12\x34\n\x13resourcePermissions\x18\x01 \x03(\x0b\x32\x17.pb.ResourcePermissions\"*\n\x18GetUserMenuPermissionReq\x12\x0e\n\x06userId\x18\x01 \x01(\x03\"\xa4\x01\n\x0fMenuPermissions\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x10\n\x08menuName\x18\x02 \x01(\t\x12\x15\n\rmenuComponent\x18\x03 \x01(\t\x12\x10\n\x08menuIcon\x18\x04 \x01(\t\x12\x0f\n\x07menuUrl\x18\x05 \x01(\t\x12\x15\n\rmenuRouteName\x18\x06 \x01(\t\x12\x10\n\x08parentId\x18\x07 \x01(\x03\x12\x10\n\x08menuType\x18\x08 \x01(\x05\"I\n\x19GetUserMenuPermissionResp\x12,\n\x0fmenuPermissions\x18\x01 \x03(\x0b\x32\x13.pb.MenuPermissions\"!\n\x10TokenValidateReq\x12\r\n\x05token\x18\x01 \x01(\t\"$\n\x11TokenValidateResp\x12\x0f\n\x07isValid\x18\x01 \x01(\x08\"(\n\x15GetMutipleUserInfoReq\x12\x0f\n\x07userIds\x18\x01 \x03(\x03\"@\n\x16GetMutipleUserInfoResp\x12&\n\tuserInfos\x18\x01 \x03(\x0b\x32\x13.pb.GetUserInfoResp2\x87\x03\n\nusercenter\x12\x36\n\x0bgetUserInfo\x12\x12.pb.GetUserInfoReq\x1a\x13.pb.GetUserInfoResp\x12`\n\x19getUserResourcePermission\x12 .pb.GetUserResourcePermissionReq\x1a!.pb.GetUserResourcePermissionResp\x12T\n\x15getUserMenuPermission\x12\x1c.pb.GetUserMenuPermissionReq\x1a\x1d.pb.GetUserMenuPermissionResp\x12<\n\rtokenValidate\x12\x14.pb.TokenValidateReq\x1a\x15.pb.TokenValidateResp\x12K\n\x12getMutipleUserInfo\x12\x19.pb.GetMutipleUserInfoReq\x1a\x1a.pb.GetMutipleUserInfoRespB\x06Z\x04./pbb\x06proto3'
)




_GETUSERINFOREQ = _descriptor.Descriptor(
  name='GetUserInfoReq',
  full_name='pb.GetUserInfoReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='userId', full_name='pb.GetUserInfoReq.userId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=56,
)


_GETUSERINFORESP = _descriptor.Descriptor(
  name='GetUserInfoResp',
  full_name='pb.GetUserInfoResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='userId', full_name='pb.GetUserInfoResp.userId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='userName', full_name='pb.GetUserInfoResp.userName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='password', full_name='pb.GetUserInfoResp.password', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='userMobile', full_name='pb.GetUserInfoResp.userMobile', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='userEmail', full_name='pb.GetUserInfoResp.userEmail', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='userAvatar', full_name='pb.GetUserInfoResp.userAvatar', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='age', full_name='pb.GetUserInfoResp.age', index=6,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gender', full_name='pb.GetUserInfoResp.gender', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='isSuperAdmin', full_name='pb.GetUserInfoResp.isSuperAdmin', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=59,
  serialized_end=238,
)


_GETUSERRESOURCEPERMISSIONREQ = _descriptor.Descriptor(
  name='GetUserResourcePermissionReq',
  full_name='pb.GetUserResourcePermissionReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='userId', full_name='pb.GetUserResourcePermissionReq.userId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=240,
  serialized_end=286,
)


_RESOURCEPERMISSIONS = _descriptor.Descriptor(
  name='ResourcePermissions',
  full_name='pb.ResourcePermissions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='pb.ResourcePermissions.id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='serverName', full_name='pb.ResourcePermissions.serverName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='pb.ResourcePermissions.url', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='method', full_name='pb.ResourcePermissions.method', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='pb.ResourcePermissions.description', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='pb.ResourcePermissions.version', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=288,
  serialized_end=408,
)


_GETUSERRESOURCEPERMISSIONRESP = _descriptor.Descriptor(
  name='GetUserResourcePermissionResp',
  full_name='pb.GetUserResourcePermissionResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resourcePermissions', full_name='pb.GetUserResourcePermissionResp.resourcePermissions', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=410,
  serialized_end=495,
)


_GETUSERMENUPERMISSIONREQ = _descriptor.Descriptor(
  name='GetUserMenuPermissionReq',
  full_name='pb.GetUserMenuPermissionReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='userId', full_name='pb.GetUserMenuPermissionReq.userId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=497,
  serialized_end=539,
)


_MENUPERMISSIONS = _descriptor.Descriptor(
  name='MenuPermissions',
  full_name='pb.MenuPermissions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='pb.MenuPermissions.id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='menuName', full_name='pb.MenuPermissions.menuName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='menuComponent', full_name='pb.MenuPermissions.menuComponent', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='menuIcon', full_name='pb.MenuPermissions.menuIcon', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='menuUrl', full_name='pb.MenuPermissions.menuUrl', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='menuRouteName', full_name='pb.MenuPermissions.menuRouteName', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='parentId', full_name='pb.MenuPermissions.parentId', index=6,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='menuType', full_name='pb.MenuPermissions.menuType', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=542,
  serialized_end=706,
)


_GETUSERMENUPERMISSIONRESP = _descriptor.Descriptor(
  name='GetUserMenuPermissionResp',
  full_name='pb.GetUserMenuPermissionResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='menuPermissions', full_name='pb.GetUserMenuPermissionResp.menuPermissions', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=708,
  serialized_end=781,
)


_TOKENVALIDATEREQ = _descriptor.Descriptor(
  name='TokenValidateReq',
  full_name='pb.TokenValidateReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='token', full_name='pb.TokenValidateReq.token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=783,
  serialized_end=816,
)


_TOKENVALIDATERESP = _descriptor.Descriptor(
  name='TokenValidateResp',
  full_name='pb.TokenValidateResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='isValid', full_name='pb.TokenValidateResp.isValid', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=818,
  serialized_end=854,
)


_GETMUTIPLEUSERINFOREQ = _descriptor.Descriptor(
  name='GetMutipleUserInfoReq',
  full_name='pb.GetMutipleUserInfoReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='userIds', full_name='pb.GetMutipleUserInfoReq.userIds', index=0,
      number=1, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=856,
  serialized_end=896,
)


_GETMUTIPLEUSERINFORESP = _descriptor.Descriptor(
  name='GetMutipleUserInfoResp',
  full_name='pb.GetMutipleUserInfoResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='userInfos', full_name='pb.GetMutipleUserInfoResp.userInfos', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=898,
  serialized_end=962,
)

_GETUSERRESOURCEPERMISSIONRESP.fields_by_name['resourcePermissions'].message_type = _RESOURCEPERMISSIONS
_GETUSERMENUPERMISSIONRESP.fields_by_name['menuPermissions'].message_type = _MENUPERMISSIONS
_GETMUTIPLEUSERINFORESP.fields_by_name['userInfos'].message_type = _GETUSERINFORESP
DESCRIPTOR.message_types_by_name['GetUserInfoReq'] = _GETUSERINFOREQ
DESCRIPTOR.message_types_by_name['GetUserInfoResp'] = _GETUSERINFORESP
DESCRIPTOR.message_types_by_name['GetUserResourcePermissionReq'] = _GETUSERRESOURCEPERMISSIONREQ
DESCRIPTOR.message_types_by_name['ResourcePermissions'] = _RESOURCEPERMISSIONS
DESCRIPTOR.message_types_by_name['GetUserResourcePermissionResp'] = _GETUSERRESOURCEPERMISSIONRESP
DESCRIPTOR.message_types_by_name['GetUserMenuPermissionReq'] = _GETUSERMENUPERMISSIONREQ
DESCRIPTOR.message_types_by_name['MenuPermissions'] = _MENUPERMISSIONS
DESCRIPTOR.message_types_by_name['GetUserMenuPermissionResp'] = _GETUSERMENUPERMISSIONRESP
DESCRIPTOR.message_types_by_name['TokenValidateReq'] = _TOKENVALIDATEREQ
DESCRIPTOR.message_types_by_name['TokenValidateResp'] = _TOKENVALIDATERESP
DESCRIPTOR.message_types_by_name['GetMutipleUserInfoReq'] = _GETMUTIPLEUSERINFOREQ
DESCRIPTOR.message_types_by_name['GetMutipleUserInfoResp'] = _GETMUTIPLEUSERINFORESP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetUserInfoReq = _reflection.GeneratedProtocolMessageType('GetUserInfoReq', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERINFOREQ,
  '__module__' : 'usercenter_pb2'
  # @@protoc_insertion_point(class_scope:pb.GetUserInfoReq)
  })
_sym_db.RegisterMessage(GetUserInfoReq)

GetUserInfoResp = _reflection.GeneratedProtocolMessageType('GetUserInfoResp', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERINFORESP,
  '__module__' : 'usercenter_pb2'
  # @@protoc_insertion_point(class_scope:pb.GetUserInfoResp)
  })
_sym_db.RegisterMessage(GetUserInfoResp)

GetUserResourcePermissionReq = _reflection.GeneratedProtocolMessageType('GetUserResourcePermissionReq', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERRESOURCEPERMISSIONREQ,
  '__module__' : 'usercenter_pb2'
  # @@protoc_insertion_point(class_scope:pb.GetUserResourcePermissionReq)
  })
_sym_db.RegisterMessage(GetUserResourcePermissionReq)

ResourcePermissions = _reflection.GeneratedProtocolMessageType('ResourcePermissions', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCEPERMISSIONS,
  '__module__' : 'usercenter_pb2'
  # @@protoc_insertion_point(class_scope:pb.ResourcePermissions)
  })
_sym_db.RegisterMessage(ResourcePermissions)

GetUserResourcePermissionResp = _reflection.GeneratedProtocolMessageType('GetUserResourcePermissionResp', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERRESOURCEPERMISSIONRESP,
  '__module__' : 'usercenter_pb2'
  # @@protoc_insertion_point(class_scope:pb.GetUserResourcePermissionResp)
  })
_sym_db.RegisterMessage(GetUserResourcePermissionResp)

GetUserMenuPermissionReq = _reflection.GeneratedProtocolMessageType('GetUserMenuPermissionReq', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERMENUPERMISSIONREQ,
  '__module__' : 'usercenter_pb2'
  # @@protoc_insertion_point(class_scope:pb.GetUserMenuPermissionReq)
  })
_sym_db.RegisterMessage(GetUserMenuPermissionReq)

MenuPermissions = _reflection.GeneratedProtocolMessageType('MenuPermissions', (_message.Message,), {
  'DESCRIPTOR' : _MENUPERMISSIONS,
  '__module__' : 'usercenter_pb2'
  # @@protoc_insertion_point(class_scope:pb.MenuPermissions)
  })
_sym_db.RegisterMessage(MenuPermissions)

GetUserMenuPermissionResp = _reflection.GeneratedProtocolMessageType('GetUserMenuPermissionResp', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERMENUPERMISSIONRESP,
  '__module__' : 'usercenter_pb2'
  # @@protoc_insertion_point(class_scope:pb.GetUserMenuPermissionResp)
  })
_sym_db.RegisterMessage(GetUserMenuPermissionResp)

TokenValidateReq = _reflection.GeneratedProtocolMessageType('TokenValidateReq', (_message.Message,), {
  'DESCRIPTOR' : _TOKENVALIDATEREQ,
  '__module__' : 'usercenter_pb2'
  # @@protoc_insertion_point(class_scope:pb.TokenValidateReq)
  })
_sym_db.RegisterMessage(TokenValidateReq)

TokenValidateResp = _reflection.GeneratedProtocolMessageType('TokenValidateResp', (_message.Message,), {
  'DESCRIPTOR' : _TOKENVALIDATERESP,
  '__module__' : 'usercenter_pb2'
  # @@protoc_insertion_point(class_scope:pb.TokenValidateResp)
  })
_sym_db.RegisterMessage(TokenValidateResp)

GetMutipleUserInfoReq = _reflection.GeneratedProtocolMessageType('GetMutipleUserInfoReq', (_message.Message,), {
  'DESCRIPTOR' : _GETMUTIPLEUSERINFOREQ,
  '__module__' : 'usercenter_pb2'
  # @@protoc_insertion_point(class_scope:pb.GetMutipleUserInfoReq)
  })
_sym_db.RegisterMessage(GetMutipleUserInfoReq)

GetMutipleUserInfoResp = _reflection.GeneratedProtocolMessageType('GetMutipleUserInfoResp', (_message.Message,), {
  'DESCRIPTOR' : _GETMUTIPLEUSERINFORESP,
  '__module__' : 'usercenter_pb2'
  # @@protoc_insertion_point(class_scope:pb.GetMutipleUserInfoResp)
  })
_sym_db.RegisterMessage(GetMutipleUserInfoResp)


DESCRIPTOR._options = None

_USERCENTER = _descriptor.ServiceDescriptor(
  name='usercenter',
  full_name='pb.usercenter',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=965,
  serialized_end=1356,
  methods=[
  _descriptor.MethodDescriptor(
    name='getUserInfo',
    full_name='pb.usercenter.getUserInfo',
    index=0,
    containing_service=None,
    input_type=_GETUSERINFOREQ,
    output_type=_GETUSERINFORESP,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='getUserResourcePermission',
    full_name='pb.usercenter.getUserResourcePermission',
    index=1,
    containing_service=None,
    input_type=_GETUSERRESOURCEPERMISSIONREQ,
    output_type=_GETUSERRESOURCEPERMISSIONRESP,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='getUserMenuPermission',
    full_name='pb.usercenter.getUserMenuPermission',
    index=2,
    containing_service=None,
    input_type=_GETUSERMENUPERMISSIONREQ,
    output_type=_GETUSERMENUPERMISSIONRESP,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='tokenValidate',
    full_name='pb.usercenter.tokenValidate',
    index=3,
    containing_service=None,
    input_type=_TOKENVALIDATEREQ,
    output_type=_TOKENVALIDATERESP,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='getMutipleUserInfo',
    full_name='pb.usercenter.getMutipleUserInfo',
    index=4,
    containing_service=None,
    input_type=_GETMUTIPLEUSERINFOREQ,
    output_type=_GETMUTIPLEUSERINFORESP,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_USERCENTER)

DESCRIPTOR.services_by_name['usercenter'] = _USERCENTER

# @@protoc_insertion_point(module_scope)
