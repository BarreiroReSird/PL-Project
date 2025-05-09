# main.py - Este ficheiro contém a função principal


from grammar import CQLGrammar
import sys


def run_file_mode(grammar, filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            contents = file.read()
            results = grammar.parse(contents)
            for result in results:
                if result is not None:
                    print(f"Result: {result}")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file.fca>")
        sys.exit(1)

    grammar = CQLGrammar()
    grammar.build()
    run_file_mode(grammar, sys.argv[1])


if __name__ == "__main__":
    main()
