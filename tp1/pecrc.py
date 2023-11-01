# Eduardo Henrique Basilio de Carvalho | Vinicius Cardoso Antunes
#################################################################
# -*- coding: latin-1 -*-
# pecrc.py - protocolo ponto-a-ponto simples com retransmissão
#          - entrega interface semelhante a um socket
#################################################################
# fornece a classe PECRC, que tem os métodos:
#
# contrutor: pode receber um ou dois parâmetros, para criar um
#            canal que implementa o protocolo PECRC;
#            - o servidor cria o objeto apenas com o porto;
#            - o cliente cria o objeto com host e porto.
# close: encerra o enlace
# send(m): envia o array de bytes m pelo canal, calculando o 
#           checksum, fazendo o enquadramento e controlando a
#           retransmissão, se necessário.
# recv(): recebe um quadro e retorna-o como um array de bytes,
#         conferindo o enquadramento, conferindo o checksum e
#         enviando uma mensagem de confirmação, se for o caso.
# OBS: o tamanho da mensagem enviada/recebida pode variar, 
#      mas não deve ser maior que 1500 bytes.
################################################################
# PECRC utiliza o módulo canal_tp1 como API para envio e recepção
#        pelo enlace; o qual não deve ser alterado.
# PECRC não pode utilizar a interface de sockets diretamente.
################################################################

import canal_tp1

################################################################################################

class PECRC:
  
    def __init__(self, port, host='' ):
        self.link = canal_tp1.Link(port,host)

    def close(self):
        self.link.close()
        
####################################################################
    MAX_BYTES   = 1500
    MIN_BYTES   = 6
    BYTES_CTRL  = 6 # bytes de controle: 1 abertura, 1 identificador tipo, 1 identificador bloco, 2 checksum, 1 fechamento
    BYTES_DADOS = MAX_BYTES - BYTES_CTRL

    # posições de inicio de cada informacao no quadro
    POS_ID_TIPO  = 1
    POS_ID_BLOCO = 2
    POS_CHECKSUM = 3
    POS_INICIO_D = 5

    ACK_CHECKSUM = [b'\xBC\xCF', b'\xBC\xCE']

    @staticmethod                                               # não acessa a classe nem seus objetos, mas faz sentido para ela
    def checksum(msg, cs = 0):                                  # calcula o checksum da mensagem
        soma_total = 0                                          # não depende das outras mensagens, então restaura a soma
        tam = len(msg)                                          # armazena o tamnho da mensagem p/ ñ precisar calcular duas vezes
        if tam % 2 != 0: msg = msg + b'\0'                      # se tiver tamanho impar, acrescenta um elemento nulo p/ iterar 2 a 2
        for indice in range(0, tam, 2):                         # do primeiro ao ultimo byte, com passo 2...
            soma_parcial = (msg[indice] << 8) | msg[indice + 1] # computa o inteiro correspontende ao par de bytes
            soma_total += soma_parcial                          # o soma ao aculumador
            if soma_total > 0xFFFF:                             # se o acumulador tiver mais do que 16 bits significativos...
                soma_total &= 0xFFFF                            # o trunca para 16 bits
                soma_total += 1                                 # soma 1 ao novo valor
        soma_total += cs                                        # soma o checksum recebido
        soma_total = (0xFFFF - soma_total) & 0xFFFF             # computa o complemento de 1
        soma_bytes = soma_total.to_bytes(2, 'big')              # monta o objeto de bytes
        return soma_bytes                                       # retorna o checksum
    
    @staticmethod
    def eh_bloco_esperado(id_bloco, id_esperado, cs):
        return id_bloco == id_esperado and cs == PECRC.ACK_CHECKSUM[int(chr(id_esperado))] # retorna verdadeiro se o id do bloco for igual ao esperado
  
    def send(self, message):
        # Aqui, PPSRT deve fazer:
        #   - fazer o encapsulamento de cada mensagem em um quadro,
        #   - calcular o Checksum do quadro e incluído,
        #   - fazer o byte stuffing durante o envio da mensagem,
        #   - aguardar pela mensagem de confirmação,
        #   - retransmitir a mensagem se a confirmação não chegar.
        #        Para controlar a retransmissão, use algo como:
        #        try:
        #            frame = self.link.recv(1500)
        #        except TimeoutError: # use para tratar temporizações
        #            TODO # cuidaria da retransmissão
        #        return frame

        message = bytearray(message) # converte em um objeto sobre o qual podemos iterar

        tamanho = len(message)                # armazena o tamanho p/ acelerar o registro de suas atualizações
        indice = 0                            # prepara o indice para a iteração
        while indice < tamanho:               # enquanto a iteração não alcançar o fim da lista
            if message[indice] in b'[!]':     # se o caractere desta posição for um dos caracteres especiais
                message[indice:indice] = b'!' # adiciona um caractere de escape antes dele
                tamanho += 1                  # registra o aumento no tamanho da lista
                indice += 1                   # avança a iteração para não avaliar o mesmo caractere multiplas vezes
            indice += 1                       # avança a iteração
        
        while message:  # enquanto não tiver operado sobre toda a mensagem
            try: self.numerador = b'1' if self.numerador == b'0' else b'0' # tenta alterar o valor do numerador para seu complemento
            except AttributeError: self.numerador = b'0'                   # se o numerador não estiver inicializado, o inicializa

            bloco, message = message[:self.BYTES_DADOS], message[self.BYTES_DADOS:] # extrai os primeiros (1500 - bytes de controle) bytes e armazena o restante

            bloco = b'[D' + self.numerador + PECRC.checksum(bloco) + bloco + b']' # calcula o checksum e manda o bloco a ser enviado

            confirmado = False        # prepara o indicador de confirmação do bloco
            while not confirmado:     # enquanto não for confirmado...
                self.link.send(bloco) # envia o bloco
                try:
                    confirmacao = self.link.recv(1500) # tenta receber a confirmação
                    if len(confirmacao) < self.MIN_BYTES: continue  # se receber menos do que MIN_BYTES bytes, não é uma mensagem útil

                    id_bloco = confirmacao[self.POS_ID_BLOCO]                      # extrai o byte de confirmação
                    cs = confirmacao[self.POS_CHECKSUM:self.POS_CHECKSUM + 2]      # armazena o checksum da confirmação
                    if PECRC.eh_bloco_esperado(id_bloco, ord(self.numerador), cs): # se a confirmação for para o bloco enviado...
                        confirmado = True                                          # foi adequadamente confirmado

                except TimeoutError:   # se o temporizador estourou...
                    confirmado = False # não foi confirmado e deve enviar novamente
        return

    def recv(self):
        # Aqui, PPSRT deve fazer:
        #   - identificar começo de um quadro,
        #   - receber a mensagem byte-a-byte, para retirar o stuffing,
        #   - detectar o fim do quadro,
        #   - calcular o checksum do quadro recebido,
        #   - descartar silenciosamente quadros com erro,
        #   - enviar uma confirmação para quadros recebidos corretamente,
        #   - conferir a ordem dos quadros e descartar quadros repetidos.

        try: self.numerador_esperado = b'1' if self.numerador_esperado == b'0' else b'0' # tenta alterar o valor do numerador para seu complemento
        except AttributeError: self.numerador_esperado = b'0'                             # se o numerador não estiver inicializado, o inicializa

        while True:                       # enquanto não for forçado a interromper
            quadro = self.link.recv(1500) # extrai até 1500 bytes da fila de recepção

            if len(quadro) < 1: # quando não houver nada...
                return None     # a transmição acabou
            
            inicio = quadro.find(b'[')               # computa indice do indicador de abertura de quadro
            if inicio > -1: quadro = quadro[inicio:] # se encontrou, descarta todo o conteúdo anterior
            else: continue                           # se não, o quadro não é útil

            if len(quadro) < self.MIN_BYTES: continue # se restarem menos do que MIN_BYTES bytes, o quadro não é útil

            inseriu_escape = False # restaura o registro de ter inserido o escape pendente

            if quadro[self.POS_ID_TIPO] == ord(b'D'): # se for um quadro de dados...
                try: self.escapa_primeiro_c           # verifica se o respectivo registro de necessidade de inserção de escape foi inicializado
                except AttributeError: self.escapa_primeiro_c = False # se não foi, o inicializa

                if self.escapa_primeiro_c:                                                  # se há um escape pendente...
                    quadro = quadro[:self.POS_INICIO_D] + b'!' + quadro[self.POS_INICIO_D:] # o insere no quadro antes de processar os escapes
                    inseriu_escape = True                                                   # registra que inseriu o escape pendente

            encontrou_fechamento = False     # controle para registrar ter encontrado o fim do quadro
            indice_atual = self.POS_INICIO_D # restaura o indice do indicador de fechamento
            try:
                while not encontrou_fechamento:                                       # enquanto não encontrar o fechamento...
                    indice_aux = indice_atual = quadro.index(b']', indice_atual + 1)  # registra a posição do próximo indicador de fechamento
                    verificou_escape = False                                          # restaura o registro de ter concluído a verificação de escape
                    contador_escape = 0         # restaura o contador de '!'
                    while not verificou_escape: # enquanto não concluir a verificação
                        byte_anterior = quadro[indice_aux - 1] # registra o byte anterior ao indice verificado
                        indice_aux -= 1                        # decrementa o indice
                        if byte_anterior == ord(b'!'):         # se for um byte de escape...
                            contador_escape += 1               # incrementa o contador
                        else:
                            if contador_escape % 2 == 0 or indice_atual == len(quadro) - 1: # se a quantidade de bytes de escape for par, não está escapado
                                                                                            # se o último byte do quadro recebido for um ']', é considerado
                                                                                            # fechamento mesmo que esteja escapado. isso é necessário porque
                                                                                            # pode haver um byte de escape destinado ao próximo quadro. caso
                                                                                            # considere um fechamento errôneo decorrente de corrupção na
                                                                                            # transmissão, o checksum capturará a falha e, no próximo
                                                                                            # recebimento, esta tende a não ocorrer
                                encontrou_fechamento = True # registra que encontrou o fechamento
                            verificou_escape = True         # registra que verificou se está escapado
            except ValueError: continue      # se não encontrar fechamento, o quadro não é útil
            indice_fechamento = indice_atual # registra o indice do fechamento

            quadro = quadro[:indice_fechamento + 1]   # descarta o que estiver após o fechamento
            if len(quadro) < self.MIN_BYTES: continue # se restarem menos do que MIN_BYTES bytes, o quadro não é útil

            id_bloco = quadro[self.POS_ID_BLOCO].to_bytes(1, 'big')     # registra o byte referente à identificação do bloco
            id_tipo  = quadro[self.POS_ID_TIPO]                         # registra o inteiro correspondente ao tipo do bloco
            try: cs_ack = self.ACK_CHECKSUM[int(id_bloco)]              # tenta extrair o checksum
            except ValueError: continue                                 # se não puder, o bloco está corrompido

            if id_tipo == ord(b'D'):                                 # se for de dado...
                if id_bloco != bytes(self.numerador_esperado):       # se não for o bloco esperado...
                    confirmacao = (b'[C' + id_bloco + cs_ack + b']') # confirma que o recebeu
                    self.link.send(confirmacao)                      # envia a confirmação
                    continue                                         # mas não o processa
            elif id_tipo == ord(b'C'):  # se for um bloco de confirmação...
                return id_bloco         # retorna o identificador do bloco
            else:                       # se não for nenhum dos dois...
                continue                # não é útil
            
            inicio_checksum = self.POS_INICIO_D # restaura o indice inicial da parte considerada no calculo do checksum
            if inseriu_escape:                  # se inseriu um byte de escape...
                inicio_checksum += 1            # incrementa o indice inicial, para não tomar este byte no calculo
                
            soma_recebida = int.from_bytes(quadro[self.POS_CHECKSUM:self.POS_INICIO_D], 'big')        # captura o checksum transmitido
            soma_calculada = PECRC.checksum(quadro[inicio_checksum:indice_fechamento], soma_recebida) # calcula o checksum do quadro recebido

            if soma_calculada != b'\x00\x00': # se forem diferentes
                continue                      # a mensagem não é útil
            
            if inseriu_escape:                 # se já inseriu o escape pendente
                self.escapa_primeiro_c = False # não precisará inserir outro

            quadro = list(quadro)                        # transforma em lista para modificar
            indice = self.POS_INICIO_D                   # prepara o indice para iteração
            tamanho = len(quadro)                        # armazena o tamanho para não o computar desnecessariamente
            while indice < tamanho:                      # enquanto o indice for menor do que o tamanho atual do quadro
                if quadro[indice] == ord(b'!'):          # se o caractere deste indice for o caractere de escape...
                    if indice == tamanho - 2:            # se esta for a ultima posicao do quadro...
                        self.escapa_primeiro_c = True    # registra que o primeiro caractere do próximo quadro deve ser escapado
                    for i in range(indice, tamanho - 1): # para todos os caracteres entre o indice atual e o ultimo do quadro...
                        quadro[i] = quadro[i + 1]        # sobrescreve este caractere com o da posição seguinte
                    quadro.pop()                         # retira o ultimo caractere do quadro
                    tamanho -= 1                         # atualiza o registro do tamanho do quadro
                indice += 1                              # incrementa o indice
            quadro = bytearray(quadro)                   # retorna a um objeto de bytes
            
            confirmacao = b'[C' + id_bloco + cs_ack + b']' # monta a confirmação
            self.link.send(confirmacao)                    # envia a confirmação
            return quadro[self.POS_INICIO_D:tamanho - 1]   # retorna os dados recebidos
