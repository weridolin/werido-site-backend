from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateQueryResultRequest(_message.Message):
    __slots__ = ("reply_content", "query_message_id", "interrupt", "interrupt_reason", "error", "error_code", "error_detail")
    REPLY_CONTENT_FIELD_NUMBER: _ClassVar[int]
    QUERY_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    INTERRUPT_FIELD_NUMBER: _ClassVar[int]
    INTERRUPT_REASON_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_DETAIL_FIELD_NUMBER: _ClassVar[int]
    reply_content: str
    query_message_id: str
    interrupt: bool
    interrupt_reason: str
    error: bool
    error_code: str
    error_detail: str
    def __init__(self, reply_content: _Optional[str] = ..., query_message_id: _Optional[str] = ..., interrupt: bool = ..., interrupt_reason: _Optional[str] = ..., error: bool = ..., error_code: _Optional[str] = ..., error_detail: _Optional[str] = ...) -> None: ...

class UpdateQueryResultReply(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class UpdateDataFakerGenerateResultRequest(_message.Message):
    __slots__ = ("record_key", "file_path", "download_code")
    RECORD_KEY_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_CODE_FIELD_NUMBER: _ClassVar[int]
    record_key: str
    file_path: str
    download_code: str
    def __init__(self, record_key: _Optional[str] = ..., file_path: _Optional[str] = ..., download_code: _Optional[str] = ...) -> None: ...

class UpdateDataFakerGenerateResultReply(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
