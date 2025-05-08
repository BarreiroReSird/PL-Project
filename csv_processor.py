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
