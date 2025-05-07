from memory import tables, procedures
from csv_handler import load_csv, save_csv, print_table

def execute_procedure(statements):
    """Executa os comandos de um procedimento."""
    for stmt in statements:
        execute_command(stmt)

def execute_command(cmd):
    """Executa o comando CQL especificado."""
    if cmd[0] == 'IMPORT':
        _, table_name, path = cmd
        tables[table_name] = load_csv(path)
        print(f"Tabela '{table_name}' importada de '{path}'.")

    elif cmd[0] == 'EXPORT':
        _, table_name, path = cmd
        if table_name in tables:
            save_csv(tables[table_name], path)
            print(f"Tabela '{table_name}' exportada para '{path}'.")
        else:
            print(f"Tabela '{table_name}' não existe.")

    elif cmd[0] == 'DISCARD':
        _, table_name = cmd
        if table_name in tables:
            del tables[table_name]
            print(f"Tabela '{table_name}' descartada.")
        else:
            print(f"Tabela '{table_name}' não existe.")

    elif cmd[0] == 'RENAME':
        _, old_name, new_name = cmd
        if old_name in tables:
            tables[new_name] = tables.pop(old_name)
            print(f"Tabela renomeada de '{old_name}' para '{new_name}'.")
        else:
            print(f"Tabela '{old_name}' não existe.")

    elif cmd[0] == 'PRINT':
        _, table_name = cmd
        if table_name in tables:
            print_table(tables[table_name])
        else:
            print(f"Tabela '{table_name}' não existe.")

    elif cmd[0] == 'CREATE':
        _, new_name, query = cmd
        tables[new_name] = execute_query(query)
        print(f"Tabela '{new_name}' criada com sucesso.")

    elif cmd[0] == 'CALL':
        _, proc_name = cmd
        if proc_name in procedures:
            for stmt in procedures[proc_name]:
                execute_command(stmt)
        else:
            print(f"Procedimento '{proc_name}' não existe.")

    elif cmd[0] == 'PROCEDURE':
        _, name, body = cmd
        procedures[name] = body
        print(f"Procedimento '{name}' guardado.")

def execute_query(query):
    """Executa a consulta SQL-like na tabela carregada."""
    if query[0] == 'SELECT':
        _, fields, table_name, where, limit = query
        if table_name not in tables:
            print(f"Tabela '{table_name}' não existe.")
            return []

        rows = tables[table_name]
        if where:
            op, col, val = where
            rows = filter_rows(rows, op, col, val)
        if limit:
            rows = rows[:limit]
        if fields == ['*']:
            return rows
        return [{k: row[k] for k in fields if k in row} for row in rows]

    elif query[0] == 'JOIN':
        _, fields, t1, t2, c1, c2, where, limit = query
        if t1 not in tables or t2 not in tables:
            print(f"Uma das tabelas '{t1}' ou '{t2}' não existe.")
            return []

        joined = []
        for r1 in tables[t1]:
            for r2 in tables[t2]:
                if r1[c1] == r2[c2]:
                    merged = {**r1, **r2}
                    joined.append(merged)

        if where:
            op, col, val = where
            joined = filter_rows(joined, op, col, val)
        if limit:
            joined = joined[:limit]
        if fields == ['*']:
            return joined
        return [{k: row[k] for k in fields if k in row} for row in joined]

def filter_rows(rows, op, col, val):
    """Filtra as linhas de acordo com a condição."""
    ops = {
        '=': lambda a, b: a == b,
        '==': lambda a, b: a == b,
        '>': lambda a, b: a > b,
        '<': lambda a, b: a < b,
        '>=': lambda a, b: a >= b,
        '<=': lambda a, b: a <= b,
        '<>': lambda a, b: a != b
    }
    return [r for r in rows if col in r and ops[op](r[col], val)]
