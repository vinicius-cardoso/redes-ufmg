from sys import argv
import grpc
import sala_pb2 as chat
import sala_pb2_grpc as rpc
import exibe_pb2 as exibidor
import exibe_pb2_grpc as exibidor_rpc
from concurrent import futures
import threading

class SalaServidor(rpc.salaServicer):
    def __init__(self, evento_parada):
        self.entradas = []
        self.saidas: {str: (str, str, str)} = {}
        self.evento_parada = evento_parada

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
            endereco = '[::]:' + request.port
            canal = grpc.insecure_channel(endereco)
            conexao = exibidor_rpc.exibeStub(canal)
            self.saidas[request.fqdn] = (endereco, conexao, request.id)
            return len(self.saidas)
    
    def lista(self, request, context):
        ids_tipos = []
        for id in self.entradas:
            ids_tipos.append((id, "entrada"))
        for (_, _, id) in self.saidas.values():
            ids_tipos.append((id, "saidas"))
        return ids_tipos
    
    def finaliza_registro(self, request, context):
        # enunciado manda remover registro de quem chamou
        # a chamada não informa o id do cliente
        # o registro só armazena o id do cliente (no caso de entradas)
        return super().finaliza_registro(request, context)
    
    def termina(self, request, context):
        for (_, conexao, _) in self.saidas.values():
            conexao.termina()
        self.evento_parada.set()
        return
    
    def envia(self, request, context):
        envio = exibidor.mensagem()
        envio.origem = context.peer()
        envio.smensagem = request.msg

        if request.destino == "todos":
            for (_, conexao, _) in self.saidas.values():
                conexao.exibe(envio)
            qtd = len(self.saidas)
        else:
            destino = self.saidas.get(request.destino)
            if destino:
                destino[1].exibe(envio)
                qtd = 1
            else:
                qtd = 0
        return qtd

def main():
    if len(argv) != 2:
        print(f"Uso: {argv[0]} numero_porto")
        return

    numero_porto = argv[1]

    evento_parada = threading.Event()
    servidor = grpc.server(futures.ThreadPoolExecutor())
    rpc.add_ChatServerServicer_to_server(SalaServidor(evento_parada), servidor)
    servidor.add_insecure_port('[::]:' + numero_porto)
    servidor.start()
    servidor.wait_for_termination()
    servidor.stop(0)
if __name__ == "__main__":
    main()