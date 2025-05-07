#!/usr/bin/env python3
# main.py - Interpretador de expressões por ficheiro e modo interativo

from exp_grammar01 import ExpGrammar
from exp_eval import ExpEval
import sys


def run_interactive_mode(grammar):
    """Modo interativo com prompt"""
    print("Interpretador de Expressões (Clique em Enter para sair)")
    for expr in iter(lambda: input(">> "), ""):
        try:
            result = grammar.parse(expr)
            if result is not None:
                print(f"<< {result}")
        except Exception as e:
            print(f"Erro: {e}", file=sys.stderr)


def run_file_mode(grammar, filename):
    """Modo de leitura do ficheiro"""
    try:
        with open(filename, "r") as file:
            contents = file.read()
            result = grammar.parse(contents)
            print(result)
    except FileNotFoundError:
        print(f"Erro: Ficheiro '{filename}' não encontrado.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    lg = ExpGrammar()
    lg.build()

    if len(sys.argv) == 2:
        run_file_mode(lg, sys.argv[1])
    else:
        run_interactive_mode(lg)


if __name__ == "__main__":
    main()
