import grpc
import exibe_pb2
import exibe_pb2_grpc
from sys import argv
from time import sleep
from concurrent import futures

class Exibe(exibe_pb2_grpc.ExibeServicer):
    def __init__(self):
        self.is_terminado = False

    def exibe(self, request, response):
        # Exibir a mensagem recebida
        print(f'Mensagem de {request.origem}: {request.msg}')
        return exibe_pb2.ExibeResponse(response=0)
    
    def termina(self, request, response):
        # Encerrar a execução do servidor
        print("Servidor de exibição encerrando...")
        return exibe_pb2.ExibeResponse(response=0)     

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    exibe = Exibe()
    exibe_pb2_grpc.add_ExibeServicer_to_server(exibe, server)

    if len(argv) != 5:
        print(f"Uso: {argv[0]} id_cliente porto_exibidor host porto_servidor")
        return

    id_cliente = argv[1]
    porto_exibidor = argv[2]
    host = argv[3]
    porto_servidor = argv[4]

    server.add_insecure_port(f'[::]:{porto_exibidor}')
    server.start()
    print("Servidor de exibição iniciado.")

    try:
        while not exibe.is_terminado:
            # Manter o servidor ativo
            sleep(1)
    except KeyboardInterrupt:
        # Parar o servidor caso o usuário queira
        server.stop(0)

if __name__ == "__main__":
    serve()
