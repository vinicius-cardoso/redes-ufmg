# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import exibe_pb2 as exibe__pb2


class exibeStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.exibe = channel.unary_unary(
                '/exibe.exibe/exibe',
                request_serializer=exibe__pb2.mensagem.SerializeToString,
                response_deserializer=exibe__pb2.Empty.FromString,
                )
        self.termina = channel.unary_unary(
                '/exibe.exibe/termina',
                request_serializer=exibe__pb2.Empty.SerializeToString,
                response_deserializer=exibe__pb2.Empty.FromString,
                )


class exibeServicer(object):
    """Missing associated documentation comment in .proto file."""

    def exibe(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def termina(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_exibeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'exibe': grpc.unary_unary_rpc_method_handler(
                    servicer.exibe,
                    request_deserializer=exibe__pb2.mensagem.FromString,
                    response_serializer=exibe__pb2.Empty.SerializeToString,
            ),
            'termina': grpc.unary_unary_rpc_method_handler(
                    servicer.termina,
                    request_deserializer=exibe__pb2.Empty.FromString,
                    response_serializer=exibe__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'exibe.exibe', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class exibe(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def exibe(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exibe.exibe/exibe',
            exibe__pb2.mensagem.SerializeToString,
            exibe__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def termina(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exibe.exibe/termina',
            exibe__pb2.Empty.SerializeToString,
            exibe__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)