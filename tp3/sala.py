from sys import argv
import grpc
import sala_pb2 as chat
import sala_pb2_grpc as rpc
import exibe_pb2 as exibidor
import exibe_pb2_grpc as exibidor_rpc
from concurrent import futures
import threading

import logging

class SalaServidor(rpc.SalaServicer):
    def __init__(self, evento_parada):
        self.entradas = []
        self.saidas: {str: (str, str, str)} = {}
        self.evento_parada = evento_parada

    def registra_entrada(self, request, context):
        resposta = chat.qtd()
        
        if request.id in self.entradas:
            resposta.quantidade = -1
        else:
            self.entradas.append(request.id)
            resposta.quantidade = len(self.entradas)

        return resposta
    
    def registra_saida(self, request, context):
        resposta = chat.qtd()
        
        if request.id in self.saidas:
            resposta.quantidade = -1
        else:
            endereco = '[::]:' + request.port
            canal = grpc.insecure_channel(endereco)
            conexao = exibidor_rpc.exibeStub(canal)
            self.saidas[request.fqdn] = (endereco, conexao, request.id)
            resposta.quantidade = len(self.saidas)

        return resposta
    
    def lista(self, request, context):
        resposta = chat.slista()
        resposta.lista_id = ''

        ids_tipos = []
        for id in self.entradas:
            ids_tipos.append((id, "entrada"))
        for (_, _, id) in self.saidas.values():
            ids_tipos.append((id, "saidas"))

        for id_, tipo in ids_tipos:
            resposta.lista_id += (id_ + ' ' + tipo + '\n')

        return resposta
        
    
    def finaliza_registro(self, request, context):
        resposta = chat.qtd()

        id = dict(context.invocation_metadata()).get('id')
        self.entradas.remove(id)

        for fqdn, _, _, id_saida in self.saidas.items():
            if id_saida == id:
                self.saidas.pop(fqdn)
                resposta.quantidade = 1
            
        resposta.quantidade = 0
        return resposta
    
    def termina(self, request, context):
        resposta = chat.Empty()

        for (_, conexao, _) in self.saidas.values():
            conexao.termina(exibidor.Empty())
        self.evento_parada.set()
        return resposta
    
    def envia(self, request, context):
        envio = exibidor.mensagem()
        envio.origem = context.peer()
        envio.smensagem = request.msg

        resposta = chat.qtd()

        if request.destino == "todos":
            for (_, conexao, _) in self.saidas.values():
                conexao.exibe(envio)
            resposta.quantidade = len(self.saidas)
        else:
            destino = self.saidas.get(request.destino)
            if destino:
                destino[1].exibe(envio)
                resposta.quantidade = 1
            else:
                resposta.quantidade = 0
        return resposta

def main():
    
    logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger('grpc')
    logger.setLevel(logging.DEBUG)

    if len(argv) != 2:
        print(f"Uso: {argv[0]} numero_porto")
        return

    numero_porto = argv[1]

    evento_parada = threading.Event()
    servidor = grpc.server(futures.ThreadPoolExecutor())
    rpc.add_SalaServicer_to_server(SalaServidor(evento_parada), servidor)
    servidor.add_insecure_port('[::]:' + numero_porto)
    servidor.start()
    servidor.wait_for_termination()
    servidor.stop(0)
if __name__ == "__main__":
    main()