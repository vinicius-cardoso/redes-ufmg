import grpc
import exibe_pb2
import exibe_pb2_grpc
from sys import argv

class Exibe():
    pass

def main():
    if len(argv) != 5:
        print(f"Uso: {argv[0]} id_cliente num_porto_cmd nome_host num_porto_serv")
        return

    id_cliente     = argv[1]
    num_porto_cmd  = argv[2]
    nome_host      = argv[3]
    num_porto_serv = argv[4]

    # registra saída

if __name__ == "__main__":
    main()