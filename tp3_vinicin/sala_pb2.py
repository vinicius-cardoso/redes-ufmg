# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sala.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nsala.proto\x12\x04sala\"$\n\x16RegistraEntradaRequest\x12\n\n\x02id\x18\x01 \x01(\t\">\n\x14RegistraSaidaRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04\x66qdn\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\x05\"0\n\x10RegistraResponse\x12\x1c\n\x14quantidade_programas\x18\x01 \x01(\x05\"\x07\n\x05\x45mpty\"\x1c\n\x08UserList\x12\x10\n\x08usuarios\x18\x01 \x03(\t\"$\n\x0fTerminaResponse\x12\x11\n\tterminado\x18\x01 \x01(\x08\",\n\x0c\x45nviaRequest\x12\x0b\n\x03msg\x18\x01 \x01(\t\x12\x0f\n\x07\x64\x65stino\x18\x02 \x01(\t\"!\n\rEnviaResponse\x12\x10\n\x08\x63ontador\x18\x01 \x01(\x05\x32\xe2\x02\n\x04Sala\x12J\n\x10registra_entrada\x12\x1c.sala.RegistraEntradaRequest\x1a\x16.sala.RegistraResponse\"\x00\x12\x46\n\x0eregistra_saida\x12\x1a.sala.RegistraSaidaRequest\x1a\x16.sala.RegistraResponse\"\x00\x12&\n\x05lista\x12\x0b.sala.Empty\x1a\x0e.sala.UserList\"\x00\x12\x39\n\x11\x66inaliza_registro\x12\x0b.sala.Empty\x1a\x15.sala.TerminaResponse\"\x00\x12/\n\x07termina\x12\x0b.sala.Empty\x1a\x15.sala.TerminaResponse\"\x00\x12\x32\n\x05\x65nvia\x12\x12.sala.EnviaRequest\x1a\x13.sala.EnviaResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sala_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_REGISTRAENTRADAREQUEST']._serialized_start=20
  _globals['_REGISTRAENTRADAREQUEST']._serialized_end=56
  _globals['_REGISTRASAIDAREQUEST']._serialized_start=58
  _globals['_REGISTRASAIDAREQUEST']._serialized_end=120
  _globals['_REGISTRARESPONSE']._serialized_start=122
  _globals['_REGISTRARESPONSE']._serialized_end=170
  _globals['_EMPTY']._serialized_start=172
  _globals['_EMPTY']._serialized_end=179
  _globals['_USERLIST']._serialized_start=181
  _globals['_USERLIST']._serialized_end=209
  _globals['_TERMINARESPONSE']._serialized_start=211
  _globals['_TERMINARESPONSE']._serialized_end=247
  _globals['_ENVIAREQUEST']._serialized_start=249
  _globals['_ENVIAREQUEST']._serialized_end=293
  _globals['_ENVIARESPONSE']._serialized_start=295
  _globals['_ENVIARESPONSE']._serialized_end=328
  _globals['_SALA']._serialized_start=331
  _globals['_SALA']._serialized_end=685
# @@protoc_insertion_point(module_scope)
