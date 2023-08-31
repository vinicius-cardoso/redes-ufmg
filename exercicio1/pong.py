import sys
import socket

HOST = "127.0.0.1"
BUFFER_SIZE = 1024

end_ping = None
porto_ping = None

porto_pong = int(sys.argv[1])
string_pong = sys.argv[2]

# cria um socket UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# liga o socket UDP ao porto_pong
udp_socket.bind((HOST, porto_pong))

#espera uma mensagem msg_de_ping naquele socket UDP
print("Aguardando mensagem de ping...")

# espera uma mensagem msg_de_ping naquele socket UDP
data, addr = udp_socket.recvfrom(BUFFER_SIZE)
data = data.decode("utf-8")

# extrai da mensagem o endereço end_ping e porto_ping
end_ping = data.split(':')[0]
porto_ping = int(data.split(':')[1])

# debug
print(f"{end_ping}:{porto_ping}")

# cria um socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# conecta o socket TCP com (end_ping, porto_ping)
tcp_socket.connect((end_ping, porto_ping))

# monta a mensagem msg_de_pong a ser enviada
msg_de_pong = string_pong.encode("utf-8")

# envia a mensagem msg_de_pong pela conexão
tcp_socket.sendall(msg_de_pong)

# fecha a conexão e termina
udp_socket.close()
tcp_socket.close()
