import grpc
import exibe_pb2
import exibe_pb2_grpc
from sys import argv
from time import sleep
from concurrent import futures

class Exibe(exibe_pb2_grpc.ExibeServicer):
    def __init__(self, id_cliente, porto_exibidor, host, porto_servidor):
        self.id_cliente = id_cliente
        self.porto_exibidor = porto_exibidor
        self.host = host
        self.porto_servidor = porto_servidor
        self.is_terminado = False

    def exibe(self, request, response):
        # Exibir a mensagem recebida
        print(f'Mensagem de {request.origem}: {request.msg}')

        return exibe_pb2.ExibeResponse(response=0)
    
    def termina(self, request, response):
        # Encerrar a execução do servidor
        self.is_terminado = True
        print("Servidor de exibição encerrando...")

        return exibe_pb2.ExibeResponse(response=0)     

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Verifica se o usuário colocou a quantidade correta de argumentos
    if len(argv) != 5:
        print(f"Uso: {argv[0]} id_cliente porto_exibidor host porto_servidor")
        return

    # Recebe as informações necessárias da linha de comando
    id_cliente = argv[1]
    porto_exibidor = int(argv[2])
    host = argv[3]
    porto_servidor = int(argv[4])

    # Cria um objeto da classe Exibe
    exibe = Exibe(id_cliente, porto_exibidor, host, porto_servidor)

    exibe_pb2_grpc.add_ExibeServicer_to_server(exibe, server)

    # Inicia um servidor com a porta fornecida pelo usuário
    server.add_insecure_port(f'[::]:{exibe.porto_exibidor}')
    server.start()
    print("Servidor de exibição iniciado.")

    try:
        while not exibe.is_terminado:
            # Mantém o servidor ativo
            sleep(1)
    except KeyboardInterrupt:
        # Para o servidor caso o usuário queira
        server.stop(0)

if __name__ == "__main__":
    serve()
