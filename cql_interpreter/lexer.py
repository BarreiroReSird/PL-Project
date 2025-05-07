import ply.lex as lex

reserved = {
    'import': 'IMPORT',
    'export': 'EXPORT',
    'discard': 'DISCARD',
    'rename': 'RENAME',
    'to': 'TO',
    'as': 'AS',
    'print': 'PRINT',
    'table': 'TABLE',
    'create': 'CREATE',
    'from': 'FROM',
    'select': 'SELECT',
    'where': 'WHERE',
    'limit': 'LIMIT',
    'join': 'JOIN',
    'on': 'ON',
    'procedure': 'PROCEDURE',
    'begin': 'BEGIN',
    'end': 'END',
    'call': 'CALL'
}

tokens = [
    'ID', 'STRING', 'NUMBER',
    'COMMA', 'DOT', 'SEMICOLON', 'EQUALS',
    'GT', 'LT', 'GE', 'LE', 'NE', 'EQ',
    'ASTERISK' 
] + list(reserved.values())

t_COMMA = r','
t_DOT = r'\.'
t_SEMICOLON = r';'
t_EQUALS = r'='
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_NE = r'<>'
t_EQ = r'=='
t_ASTERISK = r'\*'

t_ignore = ' \t\r'

def t_COMMENT(t):
    r'\-\-.*'
    pass

def t_BLOCK_COMMENT(t):
    r'\{\-[\s\S]*?\-\}'
    pass

def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
