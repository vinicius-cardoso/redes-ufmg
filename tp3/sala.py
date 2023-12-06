from sys import argv
import grpc
import sala_pb2 as chat
import sala_pb2_grpc as rpc
from concurrent import futures

class SalaServidor(rpc.salaServicer):
    def __init__(self):
        self.entradas = []
        self.saidas = {}

    def registra_entrada(self, request, context):
        if request.id in self.entradas:
            return -1
        else:
            self.entradas.append(request.id)
            return len(self.entradas)
    
    def registra_saida(self, request, context):
        if request.id in self.saidas:
            return -1
        else:
            self.saidas[request.id] = (request.fqdn, request.port)
        return super().registra_saida(request, context)
    
    def lista(self, request, context):
        ids_tipos = []
        for id in self.entradas:
            ids_tipos.append((id, "entrada"))
        for id in self.saidas.keys():
            ids_tipos.append((id, "saidas"))
        return ids_tipos
    
    def finaliza_registro(self, request, context):
        # enunciado manda remover registro de quem chamou
        # a chamada não informa o id do cliente
        # o registro só armazena o id do cliente (no caso de entradas)
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