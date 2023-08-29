#################################################################
# -*- coding: latin-1 -*-
# pecrc.py - protocolo ponto-a-ponto simples com retransmissão
#          - entrega interface semelhante a um socket
#################################################################
# fornece a classe PECRC, que tem os métodos:
#
# contrutor: pode receber um ou dois parâmetros, para criar um
#            canal que implementa o protocolo PECRC;
#            - o servidor cria o objeto apenas com o porta;
#            - o cliente cria o objeto com host e porta.
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


class PECRC:

    def __init__(self, port, host=''):
        self.link = canal_tp1.Link(port, host)

    def close(self):
        self.link.close()

####################################################################
# A princípio, só é preciso alterar as duas funções a seguir.

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
        #            print("Timeout") # cuidaria da retransmissão
        #        return frame
        #

        self.link.send(message)

    def recv(self):
        # Aqui, PPSRT deve fazer:
        #   - identificar começo de um quadro,
        #   - receber a mensagem byte-a-byte, para retirar o stuffing,
        #   - detectar o fim do quadro,
        #   - calcular o checksum do quadro recebido,
        #   - descartar silenciosamente quadros com erro,
        #   - enviar uma confirmação para quadros recebidos corretamente,
        #   - conferir a ordem dos quadros e descartar quadros repetidos.
        return self.link.recv(1500)
