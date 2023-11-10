import sys
import time
import socket
import threading
from struct import unpack

class Roteador:
    def __init__(self, nome_roteador, arquivo_config):
        self.nome_roteador = nome_roteador
        self.roteadores_na_rede = {}  # [nome]: (IP, port)
        self.vizinhos = {}            # [nome]: (IP, port)
        self.tabela_roteamento = {}   # [destino]: Caminho
        self.carregar_config(arquivo_config)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip_roteador, self.porta_roteador))
    
    class Caminho:
        def __init__(self, prox, dist):
            self.prox_passo = prox
            self.distancia = dist

        def __lt__(self, other):
            return self.distancia < other.distancia
        
        def __gt__(self, other):
            return self.distancia > other.distancia
        
        def __eq__(self, other):
            return self.distancia == other.distancia


    def carregar_config(self, arquivo_config):
        with open(arquivo_config, 'r') as arquivo:
            for linha in arquivo:
                nome, ip, porta = linha.strip().split()
                if nome == self.nome_roteador:
                    self.ip_roteador = ip
                    self.porta_roteador = int(porta)
                else:
                    self.roteadores_na_rede[nome] = (ip, int(porta))

    def lidar_com_pacote(self, pacote):
        if self.eh_pacote_de_configuracao(pacote):
            self.executa_configuracao(pacote)
        elif self.eh_pacote_de_dados(pacote):
            self.trata_pacote_de_dados(pacote)
    
    def eh_pacote_de_configuracao(self, pacote):
        return pacote.decode()[0] in 'CDTEI'
            
    def envia_pela_tabela(self, msg, destino):
        msg = b"M" + msg + b" " + destino
        self.socket.sendto(msg, self.tabela_roteamento[destino].prox_passo)
    
    def executa_configuracao(self, pacote):
        config = chr(pacote[0])
        if len(pacote) > 1:
            roteador_referido = unpack(">32s", pacote[1:34])[0].rstrip(b'\x00').decode()
        else:
            roteador_referido = 0
        match config:
            case 'C':
                self.vizinhos[roteador_referido] = self.roteadores_na_rede[roteador_referido]
                self.tabela_roteamento[roteador_referido] = self.Caminho(roteador_referido, 1)
            case 'D':
                self.vizinhos.pop(roteador_referido)
                for caminho in self.tabela_roteamento.values():
                    if caminho.prox_passo == roteador_referido:
                        del self.roteadores_na_rede[roteador_referido]
            case 'T':
                for destino, caminho in self.tabela_roteamento.items():
                    print('T' + destino + caminho.prox_passo + str(caminho.distancia))
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
        return [str(destino) for destino in self.tabela_roteamento.keys()]

    def trata_pacote_de_dados(self, pacote):
        # M: mensagem | R: roteamento
        tipo = chr(pacote[0])
        if tipo == 'M':
            msg, destino = pacote[1:].rsplit(maxsplit=1)
            if destino == self.nome_roteador:
                print("R" + msg.decode())
            elif destino in self.destinos_tabela_roteamento():
                self.envia_pela_tabela(msg, destino)
        elif tipo == 'R':
            origem, pacote = pacote[1:].split(maxsplit=1)

            self.tabela_roteamento[origem] = self.Caminho(origem, 1)

            linhas = pacote.splitlines()
            for linha in linhas:
                [destino, prox_passo, distancia] = linha.decode().split()
                if destino not in self.tabela_roteamento:
                    self.tabela_roteamento[destino] = self.Caminho(prox_passo, int(distancia) + 1)
                elif self.tabela_roteamento[destino].prox_passo == origem:
                    self.tabela_roteamento[destino] = self.Caminho(origem, distancia + 1)
                else:
                    self.tabela_roteamento[destino] = min(self.Caminho(prox_passo, int(distancia) + 1), self.tabela_roteamento[destino])
  

    def executar(self):
        while True:
            pacote, _ = self.socket.recvfrom(1024)
            self.lidar_com_pacote(pacote)

    def formata_tabela_roteamento(self):
        msg = ''
        for (destino, caminho) in self.tabela_roteamento.items():
            """ """
            print(destino, caminho.prox_passo)
            linha = ' '.join([destino, caminho.prox_passo, str(caminho.distancia)])
            msg += linha
        return msg

    def enviar_info_roteamento(self):
        msg = "R" + self.nome_roteador + " " + self.formata_tabela_roteamento()
        for vizinho in self.vizinhos.values():
            self.socket.sendto(msg.encode(), vizinho)

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
    roteador.socket.close()

if __name__ == "__main__":
    main()
