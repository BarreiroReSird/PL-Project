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

        elif cmd_type == 'CREATE_SELECT':
             new_table_name = cmd[1]
             columns = cmd[2]
             table_name = cmd[3]
             condition = cmd[4] if len(cmd) > 4 else None
             limit = cmd[5] if len(cmd) > 5 else None
             return self.processor.create_from_select(new_table_name, table_name, columns, condition, limit)
    
        elif cmd_type == 'CREATE_JOIN':
            new_table_name = cmd[1]
            table1_name = cmd[2]
            table2_name = cmd[3]
            join_column = cmd[4]
            print(f"Debug: Creating join - {new_table_name} from {table1_name} and {table2_name} on {join_column}")  # Debug
            return self.processor.create_from_join(new_table_name, table1_name, table2_name, join_column)
        
        elif cmd_type == 'SELECT':
            columns = cmd[1]
            table_name = cmd[2]
            condition = cmd[3] if len(cmd) > 3 else None
            limit = cmd[4] if len(cmd) > 4 else None

            if columns == '*' or (isinstance(columns, list) and '*' in columns):
                return self.processor.select_all_raw(table_name, condition, limit)
            elif isinstance(columns, list):
                return self.processor.select_columns(table_name, columns, condition, limit)
            else:
                return self.processor.select_columns(table_name, [columns], condition, limit)

        else:
            raise ValueError(f"Unknown command: {cmd_type}")
