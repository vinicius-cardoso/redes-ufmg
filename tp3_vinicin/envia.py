import grpc
import socket
import sala_pb2
import sala_pb2_grpc
from sys import argv

class Cliente:
    def __init__(self, id_cliente, host, porto):
        self.id_cliente = id_cliente
        self.channel = grpc.insecure_channel(f'{host}:{porto}')
        self.stub = sala_pb2_grpc.SalaStub(self.channel)

    def registra_entrada(self):
        return self.stub.registra_entrada(
            sala_pb2.RegistraEntradaRequest(id=self.id_cliente)
        )

    def registra_saida(self, port):
        fqdn = socket.getfqdn()

        return self.stub.registra_saida(
            sala_pb2.RegistraSaidaRequest(
                id=self.id_cliente, fqdn=fqdn, port=port
            )
        )

    def envia_mensagem(self, destino, mensagem):
        return self.stub.envia(sala_pb2.EnviaRequest(
            msg=mensagem, destino=destino)
        )

    def lista_usuarios(self):
        return self.stub.lista(sala_pb2.Empty())

    def finaliza_registro(self):
        self.stub.finaliza_registro(sala_pb2.Empty())

    def termina_servidor(self):
        self.stub.termina(sala_pb2.Empty())

    def processa_comandos(self):
        try:
            while True:
                print('Comandos:')
                print('- M,destino,mensagem: Envia uma mensagem para o destino') 
                print('- L: Lista os programas registrados no servidor') 
                print('- F: Finaliza um servidor de envio ou exibição específico') 
                print('- T: Termina o servidor de mensagens') 
                print('- sair')

                comando = input('Comando: ')

                if comando.startswith('M,'):
                    _, destino, mensagem = comando.split(',', 2)
                    resposta = self.envia_mensagem(destino, mensagem)
                    print(f"Mensagem enviada {resposta.contador} vezes.")
                elif comando == 'L':
                    resposta = self.lista_usuarios()
                    print("Usuários:", ', '.join(resposta.usuarios))
                elif comando == 'F':
                    self.finaliza_registro()
                    break
                elif comando == 'T':
                    self.termina_servidor()
                    break
                elif comando == 'sair':
                    break
                else:
                    print('Opção inválida!')
        except KeyboardInterrupt:
            print("Interrompido pelo usuário.")
        finally:
            self.finaliza_registro()
            print("Registro finalizado.")

def main():
    if len(argv) != 4:
        print(f'Uso: {argv[0]} id_cliente host port')
        return

    id_cliente = argv[1]
    host = argv[2]
    porto = argv[3]

    cliente = Cliente(id_cliente, host, porto)

    # Registrar a saída antes de registrar a entrada
    resposta_saida = cliente.registra_saida(porto)
    if resposta_saida.quantidade_programas == -1:
        print("Erro: ID já registrado para saída.")
        return

    resposta_entrada = cliente.registra_entrada()
    if resposta_entrada.quantidade_programas == -1:
        print("Erro: ID já registrado para entrada.")
        return

    cliente.processa_comandos()

if __name__ == '__main__':
    main()
