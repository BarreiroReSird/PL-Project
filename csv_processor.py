# csv_processor.py - Processador de CSV

import csv


class CSVProcessor:
    def __init__(self):
        self.tables = {}

    def import_table(self, table_name, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                # Ignorar linhas de comentário
                lines = [line for line in file if not line.strip().startswith('#')]
                reader = csv.DictReader(lines)
                self.tables[table_name] = {
                    'headers': reader.fieldnames,
                    'rows': list(reader)
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
                writer = csv.DictWriter(
                    file, fieldnames=self.tables[table_name]['headers'])
                writer.writeheader()

                # Ensure all rows match the headers
                for row in self.tables[table_name]['rows']:
                    sanitized_row = {key: row.get(
                        key, '') for key in self.tables[table_name]['headers']}
                    writer.writerow(sanitized_row)

            return True
        except Exception as e:
            print(f"Error exporting table: {e}")
            return False

    # Implementar outras operações: select, join, etc...
