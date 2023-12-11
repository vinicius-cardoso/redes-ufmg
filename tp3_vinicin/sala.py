from sys import argv
import grpc
import sala_pb2
import sala_pb2_grpc
import exibe_pb2
import exibe_pb2_grpc
from concurrent import futures

class SalaServidor(sala_pb2_grpc.SalaServicer):
    def __init__(self):
        self.usuarios = {}

    def registra_entrada(self, request, context):
        id = request.id

        if id in self.usuarios:
            return sala_pb2.RegistraResponse(quantidade_programas=-1)
        else:
            self.usuarios[id] = ('entrada', None)

            return sala_pb2.RegistraResponse(
                quantidade_programas=len(self.usuarios)
            )

    def registra_saida(self, request, context):
        id = request.id
        fqdn = request.fqdn
        port = request.port

        if id in self.usuarios:
            return sala_pb2.RegistraResponse(quantidade_programas=-1)
        else:
            self.usuarios[id] = ('saida', (fqdn, port))

            return sala_pb2.RegistraResponse(
                quantidade_programas=len(self.usuarios)
            )

    def lista(self, request, context):
        usuarios = [id for id in self.usuarios]

        return sala_pb2.UserList(usuarios=usuarios)

    def finaliza_registro(self, request, context):
        id = request.id

        if id in self.usuarios:
            del self.usuarios[id]
            return sala_pb2.TerminaResponse(terminado=True)
        else:
            return sala_pb2.TerminaResponse(terminado=False)

    def termina(self, request, context):
        for id, usuario in self.usuarios.items():
            tipo, dados = usuario

            if tipo == 'saida':
                fqdn, port = dados

                # Encerra os exibidores
                try:
                    with grpc.insecure_channel(f'{fqdn}:{port}') as channel:
                        stub = exibe_pb2_grpc.ExibeStub(channel)
                        stub.termina(exibe_pb2.Empty())
                except Exception as e:
                    print(f"Erro ao encerrar o exibidor {id}: {e}")
                    return sala_pb2.TerminaResponse(terminado=False)
        
        # Encerra o servidor
        context.abort(grpc.StatusCode.OK, "Servidor terminado")

        return sala_pb2.TerminaResponse(terminado=True)

    def envia(self, request, context):
        destino = request.destino
        msg = request.msg
        vezes_enviada = 0

        if destino == 'todos':
            # Enviar para todos os exibidores
            for id, usuario in self.usuarios.items():
                tipo, dados = usuario

                if tipo == 'saida':
                    fqdn, port = dados
                    self._enviar_para_exibidor(fqdn, port, msg)
                    vezes_enviada += 1
        else:
            # Enviar para um exibidor específico
            if destino in self.usuarios and self.usuarios[destino][0] == 'saida':
                fqdn, port = self.usuarios[destino][1]
                self._enviar_para_exibidor(fqdn, port, msg)
                vezes_enviada = 1

        return sala_pb2.EnviaResponse(vezes_enviada=vezes_enviada)

    def _enviar_para_exibidor(self, fqdn, port, msg):
        try:
            with grpc.insecure_channel(f'{fqdn}:{port}') as channel:
                stub = exibe_pb2_grpc.ExibeStub(channel)
                stub.exibe(exibe_pb2.ExibeRequest(msg=msg, origem='Servidor'))
        except Exception as e:
            print(f'Erro ao enviar para exibidor {fqdn}:{port}: {e}')

def serve():
    if len(argv) != 2:
        print(f"Uso: {argv[0]} porto")
        return

    porto = argv[1]

    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sala_pb2_grpc.add_SalaServicer_to_server(SalaServidor(), servidor)
    servidor.add_insecure_port(f'[::]:{porto}')
    servidor.start()
    print("Servidor de Sala iniciado.")
    servidor.wait_for_termination()

if __name__ == "__main__":
    serve()
