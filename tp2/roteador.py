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
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # cria um socket UDP para
        self.socket.bind((self.ip_roteador, self.porta_roteador))       # conecta ao roteador pelo ip e porta
        self.tabelaLock = threading.Lock()
        self.vizinhosLock = threading.Lock()
        self.iniciouRoteamento = False

    class Caminho:
        def __init__(self, prox, dist):
            self.prox_passo = prox
            self.distancia = dist

        def __lt__(self, other):
            return self.distancia < other.distancia     # retorna verdadeiro se a distancia do objeto for menor que a do outro

        def __gt__(self, other):
            return self.distancia > other.distancia     # retorna verdadeiro se a distancia do objeto for maior que a do outro

        def __eq__(self, other):
            return self.distancia == other.distancia    # retorna verdadeiro se a distancia do objeto for igual a do outro


    def carregar_config(self, arquivo_config):
        with open(arquivo_config, 'r') as arquivo:                          # abre o arquivo de configuracao como leitura
            for linha in arquivo:                                           # para cada linha do arquivo de roteadores...
                nome, ip, porta = linha.strip().split()                     # divide o conteudo da linha em nome, ip e porta
                if nome == self.nome_roteador:                              # se o nome do roteador do arquivo for igual ao nome do roteador do objeto
                    self.ip_roteador = ip                                   # adiciona o ip ao objeto do roteador
                    self.porta_roteador = int(porta)                        # adiciona a porta ao objeto do roteador
                    self.tabela_roteamento[nome] = self.Caminho(nome, 0)    # adiciona a tabela de roteamento ao objeto do roteador
                else:                                                       # se nao...
                    self.roteadores_na_rede[nome] = (ip, int(porta))        # adiciona o roteador do arquivo na lista de roteador da rede


    def destinos_tabela_roteamento(self):
        return [str(destino) for destino in self.tabela_roteamento.keys()]  # retorna a lista de destinos da tabela de roteamento


    def envia_pela_tabela(self, msg, destino):
        if destino not in self.tabela_roteamento:           # se não está na tabeça de roteamento...
            return                                          # não tenta enviar
        msg = b"M" + msg + b" " + destino.encode()          # monta a mensagem contendo a mensagem e o destino
        prox = self.tabela_roteamento[destino].prox_passo   # define o proximo como sendo o proximo passo do destino na tabela de roteamento
        endereco_prox = self.roteadores_na_rede[prox]       # armazena o endereco do destino
        self.socket.sendto(msg, endereco_prox)              # envia a mensagem para o destino via socket UDP


    def eh_pacote_de_configuracao(self, pacote):
        return pacote.decode()[0] in 'CDTEI'                # retorna verdadeiro se o comando eh um dos comandos de configuracao


    def eh_pacote_de_dados(self, pacote):
        return not self.eh_pacote_de_configuracao(pacote)   # retorna verdadeiro se nao for pacote de configuracao (se não for nenhum, emite erro)


    def executa_configuracao(self, pacote):
        config = chr(pacote[0])                                                             # converte um numero de unicode em seu respectivo caractere
        if len(pacote) > 1:                                                                 # se o pacote tiver tamanho maior que um...
            roteador_referido = unpack(">32s", pacote[1:33])[0].rstrip(b'\x00').decode()    # obtem o nome do roteador
        else:                                                                               # se nao...
            roteador_referido = None                                                        # a informação não é relevante

        if config == 'C':                                                                   # se for configuracao de conexao...
            self.vizinhos[roteador_referido] = self.roteadores_na_rede[roteador_referido]   # adiciona o roteador na posicao do roteador calculada dentro da lista de vizinhos
            self.tabela_roteamento[roteador_referido] = self.Caminho(roteador_referido, 1)  # adiciona o caminho na posicao do roteador calculada dentro da tabela de roteamento
        elif config == 'D':                                                                 # se for configuracao de desconexao...
            self.vizinhos.pop(roteador_referido)                                            # remove o elemento da posicao do roteador calculada da lista de vizinhos
            destinos_a_retirar = []
            for destino, caminho in self.tabela_roteamento.items():                   # para cada caminho na tabela de roteamento...
                if caminho.prox_passo == roteador_referido:                           # se o proximo passo for a posicao do roteador calculada...
                    destinos_a_retirar.append(destino)                                # registra que deve o retirar
            for entrada in destinos_a_retirar:                                        # para cada caminho a ser retirado...
                self.tabela_roteamento.pop(entrada)                                   # o retira
        elif config == 'T':                                                           # se for configuracao de tabela...
            for destino, caminho in self.tabela_roteamento.items():                   # para cada destino e caminho na tabela de roteamento...
                print("T", destino, caminho.prox_passo, caminho.distancia)            # imprime na tela o destino, proximo passo e destino
        elif config == 'E':                                                           # se for configuracao de envio...
            msg = pacote[33:98]                                                       # capta a mensagem no pacote
            self.envia_pela_tabela(msg, roteador_referido)                            # e envia para o roteador de destino
        elif config == 'I':                                                           # se for configuracao de inicio...
            if not self.iniciouRoteamento:                                            # se não está roteando
                threading.Thread(target=self.iniciar_roteamento, daemon=True).start() # inicia o envio de informacoes do vetor de distancia para os vizinhos
                self.iniciouRoteamento = True                                         # registra que está roteando


    def trata_pacote_de_dados(self, pacote):
        # M: mensagem | R: roteamento
        tipo = chr(pacote[0])                                   # obtem o tipo de pacote de dados
        if tipo == 'M':                                         # se o pacote for de mensagem...
            msg, destino = pacote[1:].rsplit(maxsplit=1)        # armazena a mensagem e o destino vindas do pacote
            destino = destino.decode()                          # decodifica o destino
            if destino == self.nome_roteador:                   # se o destino for o roteador atual...
                print("R", msg.decode())                        # imprime 'R' e o a mensagem decodificada
            elif destino in self.destinos_tabela_roteamento():  # se o destino estiver nos destinos da tabela de roteamento...
                self.envia_pela_tabela(msg, destino)            # envia a mensagem para o destino pela tabela
        elif tipo == 'R':                                       # se o pacote for de roteamento...
            origem, pacote = pacote[1:].split(maxsplit=1)       # armazena a origem e o o pacote
            origem = origem.decode()                            # decodifica a origem

            if origem not in self.vizinhos:                     # se quem me enviou não é mais vizinho
                return                                          # a informação não será relevante

            self.tabela_roteamento[origem] = self.Caminho(origem, 1)                                  # inicializa um caminho na tabela de roteamento para 'origem' com distancia mínima de 1

            linhas = pacote.splitlines()                                                              # obtem as linhas do pacote
            for linha in linhas:                                                                      # para cada linha em linhas...
                [destino, prox_passo, distancia] = linha.decode().split()                             # armazena o destino, proximo passo e distancia em uma lista
                if prox_passo == self.nome_roteador:                                                  # se o próximo passo sou eu...
                    continue                                                                          # não será relevante
                if destino not in self.tabela_roteamento:                                             # se não está na tabela...
                    self.tabela_roteamento[destino] = self.Caminho(origem, int(distancia) + 1)        # o caminho informado é adicionado
                elif self.tabela_roteamento[destino].prox_passo == origem:                            # se a distancia por este próximo passo mudou, a atualiza
                    self.tabela_roteamento[destino] = self.Caminho(origem, int(distancia) + 1)        # atualiza a tabela de roteamento para 'destino' com um caminho que tem 'origem' como proximo passo e incrementa a distancia em 1
                else:                                                                                 # se nao...
                    self.tabela_roteamento[destino] = min(
                        self.Caminho(prox_passo, int(distancia) + 1), self.tabela_roteamento[destino] # # define a rota para 'destino' como o menor entre o novo caminho e o caminho existente na tabela de roteamento.
                    )


    def lidar_com_pacote(self, pacote):
        if self.eh_pacote_de_configuracao(pacote):  # se for pacote de configuracao...
            self.executa_configuracao(pacote)       # executa configuracao
        elif self.eh_pacote_de_dados(pacote):       # se for pacote de dados...
            self.trata_pacote_de_dados(pacote)      # trata o pacote de dados


    def executar(self):
        while True:                                 # cria um loop infinito que...
            pacote, _ = self.socket.recvfrom(1024)  # recebe o pacote e uma tupla com ip e porta
            self.lidar_com_pacote(pacote)           # chama uma funcao que vai lidar com o pacote


    def formata_tabela_roteamento(self):
        msg = ''
        with self.tabelaLock:                                                           # tomando controle dos dados compartilhados...
            for (destino, caminho) in self.tabela_roteamento.items():                   # para cada destino e caminho na tabela de roteamento...
                linha = ' '.join([destino, caminho.prox_passo, str(caminho.distancia)]) # concatena 'destino', 'prox_passo' e 'distancia' em uma string unica, separados por espacos.
                msg += linha + "\n"                                                     # adiciona a linha a mensagem com uma quebra de linha
        return msg                                                                      # retorna a mensagem


    def enviar_info_roteamento(self):
        msg = "R" + self.nome_roteador + " " + self.formata_tabela_roteamento() # cria a mensagem contendo o tipo de pacote, nome do roteador e a mensagem
        with self.vizinhosLock:                                                 # tomando controle dos dados compartilhados...
            for vizinho in self.vizinhos.values():                              # para cada vizinho do roteador...
                self.socket.sendto(msg.encode(), vizinho)                       # envia a mensagem atraves de um socket UDP


    def iniciar_roteamento(self):
        while True:                         # cria um loop infinito
            self.enviar_info_roteamento()   # enviar as informacoes de roteamento
            time.sleep(1)                   # espera um segundo



def main():
    if len(sys.argv) != 3:                                          # se o usuario colocar uma quantidade errada de argumentos...
        print(f"Uso: {sys.argv[0]} nome_roteador arquivo_config")   # retorna o uso correto dos argumentos do programa
        return

    nome_roteador = sys.argv[1]
    arquivo_config = sys.argv[2]

    roteador = Roteador(nome_roteador, arquivo_config)
    roteador.executar()
    roteador.socket.close()


if __name__ == "__main__":
    main()
