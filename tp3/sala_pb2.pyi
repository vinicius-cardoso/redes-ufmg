from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class qtd(_message.Message):
    __slots__ = ["quantidade"]
    QUANTIDADE_FIELD_NUMBER: _ClassVar[int]
    quantidade: int
    def __init__(self, quantidade: _Optional[int] = ...) -> None: ...

class slista(_message.Message):
    __slots__ = ["lista_id"]
    LISTA_ID_FIELD_NUMBER: _ClassVar[int]
    lista_id: str
    def __init__(self, lista_id: _Optional[str] = ...) -> None: ...

class canal_envio(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class exibidor(_message.Message):
    __slots__ = ["id", "fqdn", "port"]
    ID_FIELD_NUMBER: _ClassVar[int]
    FQDN_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    id: str
    fqdn: str
    port: int
    def __init__(self, id: _Optional[str] = ..., fqdn: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class envio(_message.Message):
    __slots__ = ["msg", "destino"]
    MSG_FIELD_NUMBER: _ClassVar[int]
    DESTINO_FIELD_NUMBER: _ClassVar[int]
    msg: str
    destino: str
    def __init__(self, msg: _Optional[str] = ..., destino: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
