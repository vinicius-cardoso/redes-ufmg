import sys
import time
import socket
import threading
from struct import pack, unpack

class Roteador:
    def __init__(self, nome_roteador, arquivo_config):
        self.nome_roteador = nome_roteador
        self.vizinhos = {}
        self.tabela_roteamento = {}
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
                    self.vizinhos[nome] = (ip, int(porta))

    def lidar_com_pacote(self, pacote, endereco):
        if self.eh_pacote_de_configuracao(pacote):
            self.executa_configuracao(self, pacote, endereco)
        elif self.eh_pacote_de_dados(pacote):
            self.trata_pacote_de_dados(self, pacote, endereco)
        pass
    
    def eh_pacote_de_configuracao(self, pacote):
        try:
            return pacote.decode()[0] in 'CDTEI'
        except:
            raise UnicodeDecodeError
    
    def executa_configuracao(self, pacote, endereco):
        (config, argumento) = unpack(">c32s", pacote)
        match config:
            case 'C':
                pass
            case 'D':
                pass
            case 'T':
                pass
            case 'E':
                pass
            case 'I':
                pass
            case _:
                pass
    
    def eh_pacote_de_dados(self, pacote):
        try:
            return not self.eh_pacote_de_configuracao()
        except:
            return False
    
    def trata_pacote_de_dados(self, pacote, endereco):
        pass

    def executar(self):
        while True:
            pacote, endereco = self.socket.recvfrom(1024)  # tamanho do buffer é 1024 bytes
            threading.Thread(target=self.lidar_com_pacote, args=(pacote, endereco)).start()

    def enviar_info_roteamento(self):
        # Lógica para enviar informações de roteamento para vizinhos
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


"""
import socket
import threading
import sys
import time

# Constants
MAX_ROUTER_NAME_LENGTH = 32
MAX_MESSAGE_LENGTH = 64
UPDATE_INTERVAL = 10  # Intervalo em segundos para envio das atualizações de roteamento

# Parse command-line arguments
if len(sys.argv) != 3:
    print("Usage: router.py [ROUTER_NAME] [CONFIG_FILE]")
    sys.exit(1)

router_name = sys.argv[1]
config_file = sys.argv[2]

# Check router name length
if len(router_name) > MAX_ROUTER_NAME_LENGTH:
    print("Router name must be up to 32 characters.")
    sys.exit(1)

# Read configuration file and setup initial state
neighbours = {}  # Neighbours will be a dict with router name as key and (ip, port) as value
routing_table = {router_name: (None, 0)}  # Initial routing table with self route

def load_configuration(filename):
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) != 3:
                print("Invalid line in configuration file:", line)
                continue
            router, ip, port = parts
            neighbours[router] = (ip, int(port))

# Load the router's initial configuration
load_configuration(config_file)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((neighbours[router_name][0], neighbours[router_name][1]))

# Function to handle incoming messages
def handle_message(message, addr):
    if message.startswith('C'):
        # Handle connection message
        pass
    elif message.startswith('D'):
        # Handle disconnection message
        pass
    elif message.startswith('T'):
        # Handle print routing table message
        pass
    elif message.startswith('E'):
        # Handle data message
        pass
    elif message.startswith('I'):
        # Handle start periodic updates message
        pass

# Function to process incoming messages
def receive_messages():
    while True:
        data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        handle_message(data.decode(), addr)

# Function to send routing updates to all neighbours
def send_routing_updates():
    while True:
        time.sleep(UPDATE_INTERVAL)
        # Send the updates to neighbours

# Start the message receiver thread
receiver_thread = threading.Thread(target=receive_messages)
receiver_thread.daemon = True
receiver_thread.start()

# Start the routing updates thread
update_thread = threading.Thread(target=send_routing_updates)
update_thread.daemon = True
update_thread.start()

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down router...")
finally:
    sock.close()
"""