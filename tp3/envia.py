"""
Autores:
- Eduardo Henrique Basilio de Carvalho
- Vinicius Cardoso Antunes
"""

import grpc
from sys import argv

import sala_pb2
import sala_pb2_grpc

class Cliente:
    def __init__(self, id_cliente, host, porta):
        self.id_cliente = id_cliente
        self.host = host
        self.porta = porta

    def enviar_mensagem(self, comando, stub):
        split_word_list = comando.strip().split(',')
        destino = split_word_list[1].strip()
        
        if len(split_word_list) == 3:
            mensagem = split_word_list[2].rstrip()
        else:
            mensagem = ','.join(split_word_list[2:])

        resposta = stub.envia(
            sala_pb2.EnviaRequest(
                msg=mensagem, destino=destino
            ), 
            metadata = (('id', self.id_cliente),)
        )

        print(resposta.contador)

    def listar_comandos(self, stub):
        while True:
            print('\nComandos:')
            print('- M,destino,mensagem: Envia uma mensagem para o destino') 
            print('- L: Lista os programas registrados no servidor') 
            print('- F: Finaliza um servidor de envio ou exibição específico') 
            print('- T: Termina o servidor de mensagens') 
            print('- sair\n')

            comando = input('Comando: ')

            if comando.startswith('M,'):
                self.enviar_mensagem(comando, stub)
            elif comando == 'L':
                resposta = stub.lista(sala_pb2.UserList())
                print(resposta.usuarios)
            elif comando == 'F':
                stub.finaliza_registro(
                    sala_pb2.Empty(), 
                    metadata = (('id', self.id_cliente),)
                )

                break
            elif comando == 'T':
                stub.termina(sala_pb2.Empty())
            elif comando == 'sair':
                break
            else:
                print('Opção inválida!')

    def registrar_cliente(self):
        try:
            with grpc.insecure_channel(f'{self.host}:{self.porta}') as channel:
                stub = sala_pb2_grpc.SalaStub(channel)
                resposta = stub.registra_entrada(
                    sala_pb2.RegistraEntradaRequest(id=self.id_cliente)
                )

                print(resposta.quantidade_programas)

                self.listar_comandos(stub)
        except Exception as e:
            print(e)

def iniciar_cliente():
    if len(argv) != 4:
        print(f'Uso: {argv[0]} id_cliente host port')
        return

    cliente = Cliente(argv[1], argv[2], argv[3])

    cliente.registrar_cliente()

if __name__ == '__main__':
    iniciar_cliente()
