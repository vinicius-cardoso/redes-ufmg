from sys import argv

class salaServicer():
  pass

def main():
    if len(argv) != 2:
        print(f"Uso: {argv[0]} numero_porto")
        return

    numero_porto = argv[1]

if __name__ == "__main__":
    main()