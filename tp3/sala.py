"""
Autores:
- Eduardo Henrique Basilio de Carvalho
- Vinicius Cardoso Antunes
"""

import grpc
import threading
from sys import argv
from concurrent.futures import ThreadPoolExecutor

import sala_pb2
import sala_pb2_grpc
import exibe_pb2
import exibe_pb2_grpc

class SalaServidor(sala_pb2_grpc.SalaServicer):
    def __init__(self, evento_parada):
        self.entradas = []
        self.saidas = []
        self.portas = {}
        self.evento_parada = evento_parada

    def registra_entrada(self, request, context):
        if request.id in self.entradas:
            return sala_pb2.RegistraResponse(quantidade_programas=-1)

        self.entradas.append(request.id)

        return sala_pb2.RegistraResponse(
            quantidade_programas=len(self.entradas)
        )

    def registra_saida(self, request, context):
        if request.id in self.saidas:
            return sala_pb2.RegistraResponse(quantidade_programas=-1)

        self.saidas.append(request.id)
        self.portas[request.id] = (request.port, request.fqdn)

        return sala_pb2.RegistraResponse(
            quantidade_programas=len(self.saidas)
        )

    def lista(self, request, context):
        entrada_str = f', '.join(self.entradas)
        saida_str = f', '.join(self.saidas)

        return sala_pb2.UserList(
            usuarios=f'Entrada: {entrada_str}\nSaída: {saida_str}'
        )

    def finaliza_registro(self, request, context):
        cliente_id = self.processar_metadados(context.invocation_metadata())

        if cliente_id in self.entradas:
            self.entradas.remove(cliente_id)

            if cliente_id in self.saidas:
                endereco, porta = self.portas[cliente_id]

                self.saidas.remove(cliente_id)
                self.portas.pop(cliente_id)

                with grpc.insecure_channel(f'{endereco}:{porta}') as channel:
                    stub = exibe_pb2_grpc.ExibeStub(channel)
                    stub.termina(exibe_pb2.Empty())

                return sala_pb2.TerminaResponse(terminado=True)
            return sala_pb2.TerminaResponse(terminado=False)

    def processar_metadados(self, context):
        for key, value in context:
            if key == 'id':
                return value

    def termina(self, request, context):
        self.evento_parada.set()

        for value in self.portas.values():
            host = value[1]
            porta = value[0]

            with grpc.insecure_channel(f'{host}:{porta}') as channel:
                stub = exibe_pb2_grpc.ExibeStub(channel)
                response = stub.termina(
                    exibe_pb2.ExibeResponse(terminado=True)
                )

    def envia(self, request, context):
        try:
            fqdn = self.processar_metadados(context.invocation_metadata())

            if request.destino == 'todos':
                envios = sum(
                    1 for _ in self.tentar_enviar_para_todos(request, fqdn)
                )

                if envios != len(self.saidas):
                    return sala_pb2.EnviaResponse(contador=envios)
                else:
                    return sala_pb2.EnviaResponse(contador=len(self.saidas))
            elif request.destino in self.portas.keys():
                self.tentar_enviar(request, fqdn, self.portas[request.destino])

                return sala_pb2.EnviaResponse(contador=1)

            return sala_pb2.EnviaResponse(contador=0)
        except Exception as e:
            return sala_pb2.EnviaResponse(contador=0)

    def tentar_enviar_para_todos(self, request, fqdn):
        for endereco in self.portas.values():
            if self.tentar_enviar(request, fqdn, endereco):
                # produz um valor e pausa a função
                # retomando-a na próxima iteração
                yield 1

    def tentar_enviar(self, request, fqdn, endereco):
        host = endereco[1]
        porta = endereco[0]
        
        try:
            with grpc.insecure_channel(f'{host}:{porta}') as channel:
                stub = exibe_pb2_grpc.ExibeStub(channel)
                stub.exibe(exibe_pb2.ExibeRequest(
                    msg=request.msg, origem=fqdn)
                )

            return True
        except Exception as e:
            print(e)

            return False

def iniciar_sala():
    if len(argv) != 2:
        print(f"Uso: {argv[0]} porta")
        return

    evento_parada = threading.Event()
    servidor = grpc.server(ThreadPoolExecutor(max_workers=10))

    sala_servidor = SalaServidor(evento_parada)

    sala_pb2_grpc.add_SalaServicer_to_server(sala_servidor, servidor)
    servidor.add_insecure_port(f'[::]:{argv[1]}')
    servidor.start()
    evento_parada.wait()
    servidor.stop(None)

    exit()

if __name__ == "__main__":
    iniciar_sala()
