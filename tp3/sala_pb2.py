# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sala.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nsala.proto\x12\x04sala\"\x19\n\x03qtd\x12\x12\n\nquantidade\x18\x01 \x01(\x05\"\x1a\n\x06slista\x12\x10\n\x08lista_id\x18\x01 \x01(\t\"\x19\n\x0b\x63\x61nal_envio\x12\n\n\x02id\x18\x01 \x01(\t\"2\n\x08\x65xibidor\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04\x66qdn\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\x05\"%\n\x05\x65nvio\x12\x0b\n\x03msg\x18\x01 \x01(\t\x12\x0f\n\x07\x64\x65stino\x18\x02 \x01(\t\"\x07\n\x05\x45mpty2\x88\x02\n\x04sala\x12\x32\n\x10registra_entrada\x12\x11.sala.canal_envio\x1a\t.sala.qtd\"\x00\x12-\n\x0eregistra_saida\x12\x0e.sala.exibidor\x1a\t.sala.qtd\"\x00\x12$\n\x05lista\x12\x0b.sala.Empty\x1a\x0c.sala.slista\"\x00\x12-\n\x11\x66inaliza_registro\x12\x0b.sala.Empty\x1a\t.sala.qtd\"\x00\x12%\n\x07termina\x12\x0b.sala.Empty\x1a\x0b.sala.Empty\"\x00\x12!\n\x05\x65nvia\x12\x0b.sala.envio\x1a\t.sala.qtd\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sala_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_QTD']._serialized_start=20
  _globals['_QTD']._serialized_end=45
  _globals['_SLISTA']._serialized_start=47
  _globals['_SLISTA']._serialized_end=73
  _globals['_CANAL_ENVIO']._serialized_start=75
  _globals['_CANAL_ENVIO']._serialized_end=100
  _globals['_EXIBIDOR']._serialized_start=102
  _globals['_EXIBIDOR']._serialized_end=152
  _globals['_ENVIO']._serialized_start=154
  _globals['_ENVIO']._serialized_end=191
  _globals['_EMPTY']._serialized_start=193
  _globals['_EMPTY']._serialized_end=200
  _globals['_SALA']._serialized_start=203
  _globals['_SALA']._serialized_end=467
# @@protoc_insertion_point(module_scope)