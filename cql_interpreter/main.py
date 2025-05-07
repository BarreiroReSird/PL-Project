from lexer import lexer
from parser import parser
import sys

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <ficheiro_comandos.cql>")
        return

    filepath = sys.argv[1]

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
        parser.parse(code, lexer=lexer)
    except FileNotFoundError:
        print(f"Erro: Ficheiro '{filepath}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
