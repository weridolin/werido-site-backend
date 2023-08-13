from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetUserInfoReq(_message.Message):
    __slots__ = ["userId"]
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: int
    def __init__(self, userId: _Optional[int] = ...) -> None: ...

class GetUserInfoResp(_message.Message):
    __slots__ = ["userId", "userName", "password", "userMobile", "userEmail", "userAvatar", "age", "gender", "isSuperAdmin"]
    USERID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    USERMOBILE_FIELD_NUMBER: _ClassVar[int]
    USEREMAIL_FIELD_NUMBER: _ClassVar[int]
    USERAVATAR_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    ISSUPERADMIN_FIELD_NUMBER: _ClassVar[int]
    userId: int
    userName: str
    password: str
    userMobile: str
    userEmail: str
    userAvatar: str
    age: int
    gender: int
    isSuperAdmin: bool
    def __init__(self, userId: _Optional[int] = ..., userName: _Optional[str] = ..., password: _Optional[str] = ..., userMobile: _Optional[str] = ..., userEmail: _Optional[str] = ..., userAvatar: _Optional[str] = ..., age: _Optional[int] = ..., gender: _Optional[int] = ..., isSuperAdmin: bool = ...) -> None: ...

class GetUserResourcePermissionReq(_message.Message):
    __slots__ = ["userId"]
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: int
    def __init__(self, userId: _Optional[int] = ...) -> None: ...

class ResourcePermissions(_message.Message):
    __slots__ = ["id", "serverName", "url", "method", "description", "version"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SERVERNAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    id: int
    serverName: str
    url: str
    method: str
    description: str
    version: str
    def __init__(self, id: _Optional[int] = ..., serverName: _Optional[str] = ..., url: _Optional[str] = ..., method: _Optional[str] = ..., description: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class GetUserResourcePermissionResp(_message.Message):
    __slots__ = ["resourcePermissions"]
    RESOURCEPERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    resourcePermissions: _containers.RepeatedCompositeFieldContainer[ResourcePermissions]
    def __init__(self, resourcePermissions: _Optional[_Iterable[_Union[ResourcePermissions, _Mapping]]] = ...) -> None: ...

class GetUserMenuPermissionReq(_message.Message):
    __slots__ = ["userId"]
    USERID_FIELD_NUMBER: _ClassVar[int]
    userId: int
    def __init__(self, userId: _Optional[int] = ...) -> None: ...

class MenuPermissions(_message.Message):
    __slots__ = ["id", "menuName", "menuComponent", "menuIcon", "menuUrl", "menuRouteName", "parentId", "menuType"]
    ID_FIELD_NUMBER: _ClassVar[int]
    MENUNAME_FIELD_NUMBER: _ClassVar[int]
    MENUCOMPONENT_FIELD_NUMBER: _ClassVar[int]
    MENUICON_FIELD_NUMBER: _ClassVar[int]
    MENUURL_FIELD_NUMBER: _ClassVar[int]
    MENUROUTENAME_FIELD_NUMBER: _ClassVar[int]
    PARENTID_FIELD_NUMBER: _ClassVar[int]
    MENUTYPE_FIELD_NUMBER: _ClassVar[int]
    id: int
    menuName: str
    menuComponent: str
    menuIcon: str
    menuUrl: str
    menuRouteName: str
    parentId: int
    menuType: int
    def __init__(self, id: _Optional[int] = ..., menuName: _Optional[str] = ..., menuComponent: _Optional[str] = ..., menuIcon: _Optional[str] = ..., menuUrl: _Optional[str] = ..., menuRouteName: _Optional[str] = ..., parentId: _Optional[int] = ..., menuType: _Optional[int] = ...) -> None: ...

class GetUserMenuPermissionResp(_message.Message):
    __slots__ = ["menuPermissions"]
    MENUPERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    menuPermissions: _containers.RepeatedCompositeFieldContainer[MenuPermissions]
    def __init__(self, menuPermissions: _Optional[_Iterable[_Union[MenuPermissions, _Mapping]]] = ...) -> None: ...

class TokenValidateReq(_message.Message):
    __slots__ = ["token"]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class TokenValidateResp(_message.Message):
    __slots__ = ["isValid"]
    ISVALID_FIELD_NUMBER: _ClassVar[int]
    isValid: bool
    def __init__(self, isValid: bool = ...) -> None: ...

class GetMutipleUserInfoReq(_message.Message):
    __slots__ = ["userIds"]
    USERIDS_FIELD_NUMBER: _ClassVar[int]
    userIds: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, userIds: _Optional[_Iterable[int]] = ...) -> None: ...

class GetMutipleUserInfoResp(_message.Message):
    __slots__ = ["userInfos"]
    USERINFOS_FIELD_NUMBER: _ClassVar[int]
    userInfos: _containers.RepeatedCompositeFieldContainer[GetUserInfoResp]
    def __init__(self, userInfos: _Optional[_Iterable[_Union[GetUserInfoResp, _Mapping]]] = ...) -> None: ...
