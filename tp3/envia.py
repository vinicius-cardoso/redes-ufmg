from sys import argv
import grpc
import sala_pb2 as chat
import sala_pb2_grpc as rpc

import logging

class Cliente:
    def __init__(self, id, endereco, porto):
        self.id = id
        self.nome = endereco
        self.porto = porto
        canal = grpc.insecure_channel(endereco + ':' + porto)
        self.conexao = rpc.SalaStub(canal)

    def registrar(self):
        canal_envio = chat.canal_envio()
        canal_envio.id = self.id
        return self.conexao.registra_entrada(canal_envio)

    def enviar(self, destino, mensagem):
        envio = chat.envio()
        envio.destino = destino
        envio.msg = mensagem
        return self.conexao.envia(envio)
    
    def finaliza_registro(self):
        return self.conexao.finaliza_registro(metadata=[('id', self.id)])
    
    def termina(self):
        return self.conexao.termina()
    
    def lista(self):
        return self.conexao.lista()


def main():
    
    logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger('grpc')
    logger.setLevel(logging.DEBUG)

    if len(argv) != 4:
        print(f"Uso: {argv[0]} id_cliente nome_host num_porto")
        return

    cliente = Cliente(argv[1], argv[2], argv[3])

    qtd = cliente.registrar()
    print(qtd)

    while True:
        comando = input().split(',')
        if comando[0] == 'M':
            destino, mensagem = comando[1], comando[2]
            qtd = cliente.enviar(destino, mensagem)
            print(qtd)
        elif comando[0] == 'L':
            for id, tipo in cliente.lista():
                print(id, tipo)
        elif comando[0] == 'F':
            cliente.finaliza_registro()
        elif comando[0] == 'T':
            cliente.termina()
    
    

if __name__ == "__main__":
    main()