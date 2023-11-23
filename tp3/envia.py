from sys import argv

def main():
    if len(argv) != 4:
        print(f"Uso: {argv[0]} id_cliente nome_host num_porto")
        return

    id_cliente = argv[1]
    nome_host  = argv[2]
    num_porto  = argv[3]

    # registra entrada

    comando = input().split(',')

    if comando[0] == 'M':
        destino, mensagem = comando[1], comando[2]
        pass
    elif comando[0] == 'L':
        pass
    elif comando[0] == 'F':
        pass
    elif comando[0] == 'T':
        pass
    
    

if __name__ == "__main__":
    main()