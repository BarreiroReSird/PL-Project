# main.py - Interpretador de expressões por ficheiro e modo interativo

from grammar import CQLGrammar
import sys


def run_interactive_mode(grammar):
    print("CQL interpreter (Type 'exit' to quit)")
    buffer = ""
    while True:
        try:
            line = input("CQL> " if not buffer else "... ")
            if line.lower() == 'exit':
                break

            buffer += line + " "

            # Verifica se temos um comando completo (terminado com ;)
            if ';' in buffer:
                try:
                    result = grammar.parse(buffer)
                    if result is not None:
                        for res in result:
                            print(f"Result: {res}")
                except Exception as e:
                    print(f"Error: {e}", file=sys.stderr)
                buffer = ""

        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nType 'exit' to quit")
            buffer = ""


def run_file_mode(grammar, filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            contents = file.read()
            results = grammar.parse(contents)
            for result in results:
                print(f"Result: {result}")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    grammar = CQLGrammar()
    grammar.build()

    if len(sys.argv) == 2:
        run_file_mode(grammar, sys.argv[1])
    else:
        run_interactive_mode(grammar)


if __name__ == "__main__":
    main()
