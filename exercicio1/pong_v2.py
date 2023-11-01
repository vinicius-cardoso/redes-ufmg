# -*- coding: utf-8 -*-

import sys
import socket

BUFFER_SIZE = 1024
MSG_SIZE_BUFFER = 4

# recebe os enderecos e portas a partir do terminal
end_pong = str(socket.INADDR_ANY)
porto_pong = int(sys.argv[1])
string_pong = str(sys.argv[2])

# cria um socket UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# cria um socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # liga o socket UDP ao porto_pong
    udp_socket.bind((end_pong, porto_pong))

    print(f"Conexao UDP estabelecida: {end_pong}:{porto_pong}")
    
    #espera uma mensagem msg_de_ping naquele socket UDP
    print("Aguardando mensagem de ping via UDP...")

    # espera uma mensagem msg_de_ping naquele socket UDP
    msg_de_ping = udp_socket.recvfrom(BUFFER_SIZE)

    # extrai da mensagem o endereço end_ping e porto_ping
    porto_ping, (end_ping, _) = msg_de_ping
    porto_ping = int(porto_ping.decode())

    print(f"Mensagem recebida: {porto_ping}")

    # conecta o socket TCP com (end_ping, porto_ping)
    tcp_socket.connect((end_ping, porto_ping))

    print(f"Conexão TCP estabelecida: {end_ping}:{porto_ping}")

    # monta a mensagem msg_de_pong a ser enviada
    msg_de_pong = string_pong.encode()

    # envia o tamanho da mensagem de pong convertendo em um numero de 4 bytes
    tamanho_msg_de_pong = len(string_pong)
    tcp_socket.send(tamanho_msg_de_pong.to_bytes(MSG_SIZE_BUFFER, byteorder="big"))

    # envia a mensagem msg_de_pong pela conexão
    tcp_socket.send(msg_de_pong)

    print(f"Mensagem enviada: {msg_de_pong}")
except Exception as e:
    print(f"Erro: {e}")

# fecha a conexão e termina
udp_socket.close()
tcp_socket.close()

print("Conexões fechadas")
