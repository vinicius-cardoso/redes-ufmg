# -*- coding: utf-8 -*-

import sys
import socket

if len(sys.argv) != 4:
    print(f"Argumentos: {sys.argv[0]} end_pong porto_pong porto_ping")
    exit()

# recebe os enderecos e portas a partir do terminal
end_ping = str(socket.INADDR_ANY)
end_pong = str(sys.argv[1])
porto_pong = int(sys.argv[2])
porto_ping = int(sys.argv[3])

# cria um socket UDP e um socket TCP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # liga o socket TCP ao porto_ping
    tcp_socket.bind((end_ping, porto_ping))

    # prepara o socket TCP para receber conexões
    tcp_socket.listen()

    # monta uma mensagem msg_de_ping
    msg_de_ping = str(porto_ping)

    # envia msg_de_ping para (end_pong,porto_pong) no socket UDP
    udp_socket.sendto(msg_de_ping.encode(), (end_pong, porto_pong))

    # prepara para aceitar a conexão TCP vinda de pong (accept)
    conn, addr = tcp_socket.accept()

    # espera pela msg_de_pong no socket da conexão
    with conn: msg_pong = conn.recv(1024)

    # extrai de msg_de_pong o tamanho da msg_pong
    tamanho_msg_pong = len(msg_pong)

    # recebe a msg_pong e exibe seu conteúdo na saída
    print(msg_pong.decode())
except Exception as e:
    print(f"Erro: {e}")

# fecha a conexão e termina
udp_socket.close()
tcp_socket.close()
