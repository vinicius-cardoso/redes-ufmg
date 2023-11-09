import sys
import time
import socket
import threading
from struct import pack, unpack

class Roteador:
    def __init__(self, nome_roteador, arquivo_config):
        self.nome_roteador = nome_roteador
        self.roteadores_na_rede = {}
        self.vizinhos = {}
        self.tabela_roteamento = []
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
                    self.roteadores_na_rede[nome] = (ip, int(porta))

    def lidar_com_pacote(self, pacote, endereco):
        if self.eh_pacote_de_configuracao(pacote):
            self.executa_configuracao(pacote)
        elif self.eh_pacote_de_dados(pacote):
            self.trata_pacote_de_dados(self, pacote, endereco)
    
    def eh_pacote_de_configuracao(self, pacote):
        return pacote.decode()[0] in 'CDTEI'

    def extrai_prox_passo(self, destino):
        for linha in self.tabela_roteamento:
            destino_tabela, prox_passo, _ = linha.strip().split()
            if destino == destino_tabela:
                return prox_passo
            
    def envia_pela_tabela(self, msg, destino):
        msg = b"M" + msg + b" " + destino
        self.socket.sendto(msg, self.extrai_prox_passo(destino))
    
    def executa_configuracao(self, pacote):
        config = chr(pacote[0])
        if len(pacote) > 1:
            roteador_referido = unpack(">32s", pacote[1:34])
        else:
            roteador_referido = 0
        match config:
            case 'C':
                self.vizinhos[roteador_referido] = self.roteadores_na_rede[roteador_referido]
            case 'D':
                self.vizinhos.pop(roteador_referido)
            case 'T':
                for linha in self.tabela_roteamento:
                    destino, prox_passo, distancia = linha.strip().split()
                    print('T' + destino + prox_passo + str(distancia))
            case 'E':
                msg = pacote[34:99]
                self.envia_pela_tabela(msg, roteador_referido)
                pass
            case 'I':
                threading.Thread(target=self.iniciar_roteamento, daemon=True).start()
            case _:
                pass
    
    def eh_pacote_de_dados(self, pacote):
        return not self.eh_pacote_de_configuracao(pacote)
    
    def destinos_tabela_roteamento(self):
        return [linha[0] for linha in self.tabela_roteamento]

    
    def trata_pacote_de_dados(self, pacote, origem):
        # M: mensagem | R: roteamento
        tipo = unpack(">c", pacote[0])
        if tipo == 'M':
            msg, destino = pacote[1:].rsplit(maxsplit=1)
            if destino == self.nome_roteador:
                print("R" + msg.decode())
            elif destino in self.destinos_tabela_roteamento():
                self.envia_pela_tabela(msg, destino)
        elif tipo == 'R':
            # é mais eficiente implementar após implementar enviar_info_roteamento
            pass

    def executar(self):
        while True:
            pacote, endereco = self.socket.recvfrom(1024)  # tamanho do buffer é 1024 bytes
            self.lidar_com_pacote(pacote, endereco)

    def enviar_info_roteamento(self):
        # Lógica para enviar informações de roteamento para vizinhos
        msg = 'R' + str(len(self.tabela_roteamento)) + self.tabela_roteamento
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
