import sys
import time
import socket
import threading

class Roteador:
    def __init__(self, nome_roteador, arquivo_config):
        self.nome_roteador = nome_roteador
        self.vizinhos = {}
        self.tabela_roteamento = {}
        self.carregar_config(arquivo_config)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip_roteador, self.porta_roteador))

    def carregar_config(self, arquivo_config):
        with open(arquivo_config, 'r') as arquivo:
            for linha in arquivo:
                nome, ip, porta = linha.strip().split()
                if nome == self.nome_roteador:
                    self.ip_roteador = ip
                    self.porta_roteador = int(porta)
                else:
                    self.vizinhos[nome] = (ip, int(porta))

    def lidar_com_pacote(self, pacote, endereco):
        # Lógica para lidar com pacotes recebidos
        pass

    def executar(self):
        while True:
            pacote, endereco = self.socket.recvfrom(1024)  # tamanho do buffer é 1024 bytes
            threading.Thread(target=self.lidar_com_pacote, args=(pacote, endereco)).start()

    def enviar_info_roteamento(self):
        # Lógica para enviar informações de roteamento para vizinhos
        pass

    def iniciar_roteamento(self):
        while True:
            self.enviar_info_roteamento()
            time.sleep(1)  # intervalo configurável

def main():
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} nome_roteador arquivo_config")
        return

    nome_roteador = sys.argv[1]
    arquivo_config = sys.argv[2]

    roteador = Roteador(nome_roteador, arquivo_config)
    roteador.executar()

if __name__ == "__main__":
    main()
