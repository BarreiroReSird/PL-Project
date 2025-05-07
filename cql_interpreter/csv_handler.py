import csv

def load_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def save_csv(data, path):
    if not data:
        print("Não há dados para exportar.")
        return
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def print_table(data):
    if not data:
        print("Tabela vazia.")
        return
    headers = data[0].keys()
    print(" | ".join(headers))
    print("-" * 50)
    for row in data:
        print(" | ".join(str(row[h]) for h in headers))
