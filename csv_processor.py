# csv_processor.py - Processador de CSV

import csv
import re


class CSVProcessor:
    def __init__(self):
        self.tables = {}

    def _parse_line(self, line):
        """Parseia uma linha manualmente para tratar colchetes corretamente"""
        in_quotes = False
        in_brackets = False
        current_field = []
        fields = []

        i = 0
        while i < len(line):
            char = line[i]

            if char == '"' and not in_brackets:
                in_quotes = not in_quotes
                i += 1
                continue

            if char == '[' and not in_quotes:
                in_brackets = True
                current_field.append(char)
                i += 1
                continue

            if char == ']' and in_brackets and not in_quotes:
                in_brackets = False
                current_field.append(char)
                i += 1
                continue

            if char == ',' and not in_quotes and not in_brackets:
                fields.append(''.join(current_field))
                current_field = []
                i += 1
                continue

            current_field.append(char)
            i += 1

        # Adiciona o último campo
        if current_field:
            fields.append(''.join(current_field))

        return [field.strip('"') for field in fields]

    def _evaluate_condition(self, row, condition):
        if condition is None:
            return True

        if condition[0] == 'AND':
            return (self._evaluate_condition(row, condition[1]) and
                    self._evaluate_condition(row, condition[2]))

        op, column, value = condition
        try:
            row_value = float(row.get(column, ''))
            value = float(value)
        except ValueError:
            return False

        if op == '<':
            return row_value < value
        elif op == '>':
            return row_value > value
        elif op == '<=':
            return row_value <= value
        elif op == '>=':
            return row_value >= value
        elif op == '=':
            return row_value == value
        elif op == '<>':
            return row_value != value
        return False

    def import_table(self, table_name, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                # Ignorar linhas de comentário
                lines = [line.strip() for line in file if not line.strip(
                ).startswith('#') and line.strip()]

                if not lines:
                    return False

                # Processar cabeçalhos
                headers = self._parse_line(lines[0])

                # Processar linhas de dados
                rows = []
                for line in lines[1:]:
                    if not line:
                        continue

                    values = self._parse_line(line)
                    if len(values) != len(headers):
                        continue  # Ignorar linhas mal formadas

                    row = dict(zip(headers, values))
                    rows.append(row)

                self.tables[table_name] = {
                    'headers': headers,
                    'rows': rows
                }
            return True
        except Exception as e:
            print(f"Error importing table: {e}")
            return False

    def export_table(self, table_name, filename):
        if table_name not in self.tables:
            print(f"Table '{table_name}' not found")
            return False

        try:
            with open(filename, 'w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)

                # Escrever cabeçalhos
                writer.writerow(self.tables[table_name]['headers'])

                # Escrever linhas de dados
                for row in self.tables[table_name]['rows']:
                    writer.writerow(
                        [row.get(header, '')
                         for header in self.tables[table_name]['headers']]
                    )

            return True
        except Exception as e:
            print(f"Error exporting table: {e}")
            return False

    def discard_table(self, table_name):
        if table_name in self.tables:
            del self.tables[table_name]
            return f"Table '{table_name}' discarded successfully"
        else:
            return f"Error: Table '{table_name}' not found"

    def rename_table(self, old_name, new_name):
        if old_name not in self.tables:
            return f"Error: Table '{old_name}' not found"

        if new_name in self.tables:
            return f"Error: Table '{new_name}' already exists"

        self.tables[new_name] = self.tables.pop(old_name)
        return f"Table '{old_name}' renamed to '{new_name}' successfully"

    def print_table(self, table_name):
        if table_name not in self.tables:
            return f"Error: Table '{table_name}' not found"

        table = self.tables[table_name]

        # Determinar a largura máxima de cada coluna
        col_widths = []
        for header in table['headers']:
            max_width = len(header)
            for row in table['rows']:
                value = str(row.get(header, ''))
                if len(value) > max_width:
                    max_width = len(value)
            col_widths.append(max_width + 2)  # Adiciona um pouco de espaço

        # Imprimir cabeçalhos
        header_line = " | ".join(
            f"{header:<{col_widths[i]}}"
            for i, header in enumerate(table['headers']))
        print(header_line)

        # Imprimir separador
        print("-" * len(header_line))

        # Imprimir linhas de dados
        for row in table['rows']:
            print(" | ".join(
                f"{str(row.get(header, '')):<{col_widths[i]}}"
                for i, header in enumerate(table['headers'])))

        return f"Table '{table_name}' printed successfully"

    def select_all_raw(self, table_name, condition=None, limit=None):
        if table_name not in self.tables:
            return f"Error: Table '{table_name}' not found"

        table = self.tables[table_name]
        print(",".join(table['headers']))
        count = 0
        for row in table['rows']:
            if self._evaluate_condition(row, condition):
                print(",".join(str(row.get(header, '')) for header in table['headers']))
                count += 1
                if limit is not None and count >= int(limit):
                    break
        return f"Raw data from table '{table_name}'"

    def select_columns(self, table_name, columns, condition=None, limit=None):
        if table_name not in self.tables:
            return f"Error: Table '{table_name}' not found"

        table = self.tables[table_name]
        for col in columns:
            if col not in table['headers']:
                return f"Error: Column '{col}' not found in table '{table_name}'"

        print(",".join(columns))
        count = 0
        for row in table['rows']:
            if self._evaluate_condition(row, condition):
                print(",".join(str(row.get(col, '')) for col in columns))
                count += 1
                if limit is not None and count >= int(limit):
                    break
        return f"Selected columns {columns} from table '{table_name}'"

    def create_from_select(self, new_table_name, source_table, columns, condition=None, limit=None):
        if source_table not in self.tables:
            return f"Error: Source table '{source_table}' not found"
    
        source_data = self.tables[source_table]
    
    # Verifica colunas se não for *
        if columns != '*' and isinstance(columns, list):
            for col in columns:
                if col not in source_data['headers']:
                 return f"Error: Column '{col}' not found in source table"
    
    # Filtra as colunas se necessário
        if columns == '*':
            headers = source_data['headers']
        else:
         headers = columns if isinstance(columns, list) else [columns]
    
    # Filtra as linhas baseado na condição
        filtered_rows = []
        for row in source_data['rows']:
             if self._evaluate_condition(row, condition):
                filtered_rows.append(row)
    
    # Aplica o limite se existir
        if limit is not None:
            filtered_rows = filtered_rows[:int(limit)]
    
    # Cria a nova tabela
        self.tables[new_table_name] = {
        'headers': headers,
        'rows': filtered_rows
    }
    
        return f"Table '{new_table_name}' created successfully with {len(filtered_rows)} rows"
    
    def create_from_join(self, new_table_name, table1_name, table2_name, join_column):
        print(f"Debug: Joining {table1_name} and {table2_name} on column '{join_column}'")  # Debug
    
        if table1_name not in self.tables:
            return f"Error: Table '{table1_name}' not found"
        if table2_name not in self.tables:
            return f"Error: Table '{table2_name}' not found"
    
        table1 = self.tables[table1_name]
        table2 = self.tables[table2_name]
    
    # Verificação mais robusta da coluna de join
        if join_column not in table1['headers']:
            return f"Error: Join column '{join_column}' not found in table '{table1_name}'"
        if join_column not in table2['headers']:
            return f"Error: Join column '{join_column}' not found in table '{table2_name}'"
    
    # Cria os cabeçalhos da nova tabela (todos os campos de ambas as tabelas)
    # Adiciona prefixos para evitar colisão de nomes
        headers = (
            [f"{table1_name}.{h}" for h in table1['headers']] +
            [f"{table2_name}.{h}" for h in table2['headers'] if h != join_column]
        )
    
    # Cria um índice para a tabela2 baseado na coluna de join
        table2_index = {}
        for row in table2['rows']:
            key = row[join_column]
            if key not in table2_index:
                table2_index[key] = []
            table2_index[key].append(row)
    
    # Realiza o join
        joined_rows = []
        for row1 in table1['rows']:
            join_key = row1[join_column]
            if join_key in table2_index:
                for row2 in table2_index[join_key]:
                # Combina as linhas
                    new_row = {}
                # Adiciona todos os campos da tabela1
                    for h in table1['headers']:
                        new_row[f"{table1_name}.{h}"] = row1[h]
                # Adiciona campos da tabela2 (exceto a coluna de join)
                    for h in table2['headers']:
                        if h != join_column:
                            new_row[f"{table2_name}.{h}"] = row2[h]
                    joined_rows.append(new_row)
    
    # Cria a nova tabela
        self.tables[new_table_name] = {
            'headers': headers,
            'rows': joined_rows
        }
    
        return f"Table '{new_table_name}' created successfully with {len(joined_rows)} rows from JOIN"