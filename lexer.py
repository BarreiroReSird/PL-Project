# lexer.py - Analisador léxico para CQL

import re
import ply.lex as lex


class CQLLexer:
    def __init__(self):
        self.lexer = lex.lex(module=self)

    # Lista de tokens
    tokens = (
        'IMPORT', 'EXPORT', 'DISCARD', 'RENAME', 'PRINT',
        'SELECT', 'FROM', 'WHERE', 'CREATE', 'TABLE',
        'JOIN', 'USING', 'PROCEDURE', 'DO', 'END', 'CALL',
        'LIMIT', 'AND', 'AS',
        'ID', 'NUMBER', 'STRING', 'COMMA', 'SEMICOLON',
        'EQ', 'NE', 'LT', 'GT', 'LE', 'GE',
        'LPAREN', 'RPAREN'
    )

    # Expressões regulares para tokens simples
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_EQ = r'='
    t_NE = r'<>'
    t_LT = r'<'
    t_GT = r'>'
    t_LE = r'<='
    t_GE = r'>='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    # Palavras-chave
    keywords = {
        'IMPORT': 'IMPORT',
        'EXPORT': 'EXPORT',
        'DISCARD': 'DISCARD',
        'RENAME': 'RENAME',
        'PRINT': 'PRINT',
        'SELECT': 'SELECT',
        'FROM': 'FROM',
        'WHERE': 'WHERE',
        'CREATE': 'CREATE',
        'TABLE': 'TABLE',
        'JOIN': 'JOIN',
        'USING': 'USING',
        'PROCEDURE': 'PROCEDURE',
        'DO': 'DO',
        'END': 'END',
        'CALL': 'CALL',
        'LIMIT': 'LIMIT',
        'AND': 'AND',
        'AS': 'AS'
    }

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.keywords.get(t.value.upper(), 'ID')
        return t

    def t_NUMBER(self, t):
        r'\d+(\.\d+)?'
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    def t_STRING(self, t):
        r'\"([^\\\"]|\\.)*\"'
        t.value = t.value[1:-1]  # Remove as aspas
        return t

    # Ignorar espaços em branco e comentários
    t_ignore = ' \t'

    def t_COMMENT(self, t):
        r'--.*'
        pass

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def tokenize(self, text):
        self.lexer.input(text)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append((tok.type, tok.value))
        return tokens
