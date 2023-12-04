from sys import argv
import grpc
import sala_pb2 as chat
import sala_pb2_grpc as rpc
from concurrent import futures
from time import sleep

class SalaServidor(rpc.salaServicer):
    def __init__(self):
        self.programas = []

    def registra_entrada(self, request, context):
        return super().registra_entrada(request, context)
    
    def registra_saida(self, request, context):
        return super().registra_saida(request, context)
    
    def lista(self, request, context):
        return super().lista(request, context)
    
    def finaliza_registro(self, request, context):
        return super().finaliza_registro(request, context)
    
    def termina(self, request, context):
        return super().termina(request, context)
    
    def envia(self, request, context):
        return super().envia(request, context)

def main():
    if len(argv) != 2:
        print(f"Uso: {argv[0]} numero_porto")
        return

    numero_porto = argv[1]

    servidor = grpc.server(futures.ThreadPoolExecutor())
    rpc.add_ChatServerServicer_to_server(SalaServidor(), servidor)
    servidor.add_insecure_port('[::]:' + numero_porto)
    servidor.start()
    servidor.wait_for_termination()

if __name__ == "__main__":
    main()