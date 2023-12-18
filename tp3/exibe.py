"""
Autores:
- Eduardo Henrique Basilio de Carvalho
- Vinicius Cardoso Antunes
"""

import grpc
import socket
import threading
from sys import argv
from concurrent.futures import ThreadPoolExecutor

import exibe_pb2
import exibe_pb2_grpc
import sala_pb2
import sala_pb2_grpc

class Exibidor(exibe_pb2_grpc.ExibeServicer):
    def __init__(self, id, porta_exibidor, host, porta_sala, evento_parada):
        self.id = id
        self.porta_exibidor = porta_exibidor
        self.host = host
        self.porta_sala = porta_sala
        self.evento_parada = evento_parada

    def exibe(self, request, response):
        print(f'Mensagem de {request.origem}: {request.msg}')

        return exibe_pb2.ExibeResponse(response=0)
    
    def termina(self, request, response):
        self.evento_parada.set()

        return exibe_pb2.ExibeResponse(response=0)

    def registrar_exibidor(self):
        try:
            with grpc.insecure_channel(
                f'{self.host}:{self.porta_sala}'
            ) as channel:
                stub = sala_pb2_grpc.SalaStub(channel)
                resposta = stub.registra_saida(
                    sala_pb2.RegistraSaidaRequest(
                        id=self.id, 
                        fqdn=socket.getfqdn(), 
                        port=int(self.porta_exibidor)
                    )
                )

                print(resposta.quantidade_programas)
        except Exception as e:
            print(e)

def iniciar_exibidor():
    evento_parada = threading.Event()
    servidor = grpc.server(ThreadPoolExecutor(max_workers=10))

    if len(argv) != 5:
        print(f"Uso: {argv[0]} id porta_exibidor host porta_sala")
        return

    exibidor = Exibidor(argv[1], int(argv[2]), argv[3], argv[4], evento_parada)
    exibe_pb2_grpc.add_ExibeServicer_to_server(exibidor, servidor)
    servidor.add_insecure_port(f'[::]:{exibidor.porta_exibidor}')

    exibidor.registrar_exibidor()

    servidor.start()
    evento_parada.wait()
    server.stop(None)
    exit()

if __name__ == "__main__":
    iniciar_exibidor()
