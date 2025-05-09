# grammar.py - Definição da gramática para expressões matemáticas

from lexer import CQLLexer
from parser import CQLParser
from csv_processor import CSVProcessor


class CQLGrammar:
    def __init__(self):
        self.lexer = CQLLexer()
        self.parser = CQLParser(self.lexer)
        self.processor = CSVProcessor()

    def build(self):
        self.parser.build()

    def parse(self, text):
        if not hasattr(self.parser, 'parser'):
            self.build()

        ast = self.parser.parse(text)
        return self.execute(ast)

    def execute(self, ast):
        if ast[0] == 'PROGRAM':
            results = []
            for cmd in ast[1]:
                results.append(self.execute_command(cmd))
            return results
        return self.execute_command(ast)

    def execute_command(self, cmd):
        cmd_type = cmd[0]

        if cmd_type == 'IMPORT':
            table_name = cmd[1]
            filename = cmd[2]
            return self.processor.import_table(table_name, filename)

        elif cmd_type == 'EXPORT':
            table_name = cmd[1]
            filename = cmd[2]
            return self.processor.export_table(table_name, filename)

        elif cmd_type == 'DISCARD':
            table_name = cmd[1]
            return self.processor.discard_table(table_name)

        elif cmd_type == 'RENAME':
            old_name = cmd[1]
            new_name = cmd[2]
            return self.processor.rename_table(old_name, new_name)

        elif cmd_type == 'PRINT':
            table_name = cmd[1]
            return self.processor.print_table(table_name)

        elif cmd_type == 'SELECT':
            column = cmd[1]
            table_name = cmd[2]
            if column == '*':
                # Se for SELECT *, apenas imprima a tabela inteira
                return self.processor.print_table(table_name)
            else:
                # Implemente aqui a lógica para selecionar colunas específicas
                return f"Selected column '{column}' from table '{table_name}'"

        elif cmd_type == 'SELECT':
            column = cmd[1]
            table_name = cmd[2]
            return self.processor.select_columns(table_name, column)

        elif cmd_type == 'SELECT':
            columns = cmd[1] 
            table_name = cmd[2]
            if isinstance(columns, list) and '*' in columns:
                return self.processor.print_table(table_name)
            elif isinstance(columns, list):
                return self.processor.select_columns(table_name, columns)
            elif columns == '*':
                return self.processor.print_table(table_name)
            else:
                return self.processor.select_columns(table_name, [columns])

        else:
            raise ValueError(f"Unknown command: {cmd_type}")
