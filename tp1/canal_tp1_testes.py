#################################################################
# -*- coding: latin-1 -*-
# canal_tp1.py - encapsulamento do socket para facilitar testes
#               - PPPSRT deve usar esta interface, não socket
#               - este arquivo não deve ser alterado
#################################################################
# Durante os testes da avaliação, uma versão alterada deste 
# arquivo será usada pelo professor, mas a interface não mudará.
#################################################################

import socket
import random
from time import sleep

class Link:
  
    def __init__(self, port = 0, host = '' ):
        if host == '':
            orig = (host, int(port))
            listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listen_socket.bind(orig)
            listen_socket.listen(1)
            self.tcp_socket, client = listen_socket.accept()
        else:
            dest = (host,int(port))
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.settimeout(0.5) # usando 0.5 segundos
            self.tcp_socket.connect(dest)
  
    def send(self,message):
        meio = len(message) // 2
        string = ''
        for i in range(random.randint(1, 10)):
            string += random.choice(['[', '!', ']', '\0', '|'])
        erro = bytes(string, "latin-1")
        match random.randint(0, 20):
            case 0:
                print("insere string no meio da mensagem")
                message = message[:meio] + erro + message[meio:]
            case 1:
                print("insere byte")
                message = message[:meio] + b'\0' + message[meio:]
            case 2:
                print("extrai caractere")
                message = message[:meio] + message[meio + 1:]
            case 3:
                print("extrai byte")
                message = message[:meio] + message[meio + 1:]
            case 5:
                print("troca byte")
                message = message[:meio] + b'\0' + message[meio + 1:]
            case 6:
                print("duplicado")
                self.tcp_socket.send(message)
            case 7:
                print("perdido")
                return
            case 8:
                print("insere string no fim da mensagem")
                message = message + erro
            case 9:
                print("insere string no comeco da mensagem")
                message = erro + message
            case 10:
                print("remove", end=' ')
                match random.randint(0, 1):
                    case 0:
                        print("abertura")
                        message = message[1:]
                    case 1:
                        print("fechamento")
                        message = message[:len(message) - 1]
            case _:
                print("sem erro")
        self.tcp_socket.send(message)

    def recv(self,nbytes):
        try: # essa estrutura repassa temporizações para PPPSRT
            some_bytes = self.tcp_socket.recv(nbytes)
        except socket.timeout:
            raise TimeoutError

        if random.randint(0, 20) == 0:
            print("demora pra receber")
            sleep(0.5)

        return some_bytes

    def close(self):
        self.tcp_socket.close()