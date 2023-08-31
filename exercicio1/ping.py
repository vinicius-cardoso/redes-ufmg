import sys
import socket

HOST = "127.0.0.1"

end_pong = sys.argv[1]
porto_pong = int(sys.argv[2])
porto_ping = int(sys.argv[3])

# cria um socket UDP e um socket TCP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# liga o socket TCP ao porto_ping
tcp_socket.bind((HOST, porto_ping))

# prepara o socket TCP para receber conexões
tcp_socket.listen()

# monta uma mensagem msg_de_ping
msg_de_ping = f"{HOST}:{porto_ping}"

# envia msg_de_ping para (end_pong,porto_pong) no socket UDP
udp_socket.sendto(msg_de_ping.encode("utf-8"), (end_pong, porto_pong))

# prepara para aceitar a conexão TCP vinda de pong (accept)
conn, addr = tcp_socket.accept()

# espera pela msg_de_pong no socket da conexão
print("Aguardando mensagem de pong...")

# extrai de msg_de_pong o tamanho da string_pong
# string_pong = conn.recv(1024)
# tam_string_pong = len(string_pong)

# recebe a string_pong e exibe seu conteúdo na saída
data = conn.recv(1024)
string_pong = data.decode("utf-8")
print(string_pong)

# fecha a conexão e termina
udp_socket.close()
conn.close()
tcp_socket.close()
