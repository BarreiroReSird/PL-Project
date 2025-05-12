# PL-Project

Este projeto implementa uma linguagem de consulta de dados (CQL) inspirada em SQL, com suporte a manipulação de tabelas CSV, consultas, joins e procedimentos.

## Estrutura do Projeto

- `main.py` — Ponto de entrada do programa.
- `grammar.py` — Implementação da gramática e execução dos comandos.
- `lexer.py` — Lexer para a linguagem CQL (usando PLY).
- `parser.py` — Parser para a linguagem CQL (usando PLY).
- `csv_processor.py` — Manipulação de tabelas CSV em memória.
- Ficheiros `.csv` — Exemplos de dados.
- Ficheiros `.fca` — Scripts de comandos de teste.

## Como executar

1. Instala as dependências necessárias (PLY):

   ```sh
   pip install ply
   ```

2. Executa o programa com um ficheiro de comandos:

   ```sh
   python main.py commands.fca
   ```

## Testes

Testes adicionais podem ser encontrados em [commands.fca](commands.fca) e [tests.fca](tests.fca).