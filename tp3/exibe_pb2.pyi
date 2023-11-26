from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class mensagem(_message.Message):
    __slots__ = ["smensagem", "origem"]
    SMENSAGEM_FIELD_NUMBER: _ClassVar[int]
    ORIGEM_FIELD_NUMBER: _ClassVar[int]
    smensagem: str
    origem: str
    def __init__(self, smensagem: _Optional[str] = ..., origem: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
