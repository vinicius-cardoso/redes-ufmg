import os
import time
import subprocess

def excluir_arquivos_e_executar_protoc():
    # Lista dos arquivos a serem excluídos
    arquivos_para_excluir = [
        'exibe_pb2_grpc.py', 'exibe_pb2.py', 
        'sala_pb2.py', 'sala_pb2_grpc.py'
    ]

    # Excluindo os arquivos
    for arquivo in arquivos_para_excluir:
        if os.path.exists(arquivo):
            os.remove(arquivo)
            print(f"Arquivo {arquivo} excluído.")
        else:
            print(f"Arquivo {arquivo} não encontrado.")

    time.sleep(1)

    # Executando o comando protoc
    comando = (
        "python -m grpc_tools.protoc -I ./ --python_out=. --grpc_python_out=. sala.proto exibe.proto"
    )
    subprocess.run(comando, shell=True)
    
    print("Arquivos de protobuffer gerados.")

if __name__ == "__main__":
    excluir_arquivos_e_executar_protoc()
