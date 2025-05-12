# lexer.py - ...

import re
import ply.lex as lex


class CQLLexer:
    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.lexer.comment_level = 0

    states = (
        ('multicomment', 'exclusive'),
    )

    tokens = (
        'IMPORT', 'EXPORT', 'DISCARD', 'RENAME', 'PRINT',
        'SELECT', 'FROM', 'WHERE', 'CREATE', 'TABLE',
        'JOIN', 'USING', 'PROCEDURE', 'DO', 'END', 'CALL',
        'LIMIT', 'AND', 'AS', 'STAR',
        'ID', 'NUMBER', 'STRING', 'COMMA', 'SEMICOLON',
        'EQ', 'NE', 'LT', 'GT', 'LE', 'GE',
        'LPAREN', 'RPAREN'
    )

    t_STAR = r'\*'
    t_ignore = ' \t'

    def t_COMMENT(self, t):
        r'--[^\n]*'
        pass

    def t_MULTICOMMENT_START(self, t):
        r'\{-'
        t.lexer.begin('multicomment')
        t.lexer.comment_level = 1
        pass

    t_multicomment_ignore = ''

    def t_multicomment_CONTENT(self, t):
        r'[^\{\}-]+'
        pass

    def t_multicomment_NESTED_START(self, t):
        r'\{-'
        t.lexer.comment_level += 1
        pass

    def t_multicomment_NESTED_END(self, t):
        r'-\}'
        t.lexer.comment_level -= 1
        if t.lexer.comment_level == 0:
            t.lexer.begin('INITIAL')
        pass

    def t_multicomment_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_multicomment_error(self, t):
        print(f"Illegal character in comment: '{t.value[0]}'")
        t.lexer.skip(1)

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

    keywords = {
        'import': 'IMPORT',
        'export': 'EXPORT',
        'discard': 'DISCARD',
        'rename': 'RENAME',
        'print': 'PRINT',
        'select': 'SELECT',
        'from': 'FROM',
        'where': 'WHERE',
        'create': 'CREATE',
        'table': 'TABLE',
        'join': 'JOIN',
        'using': 'USING',
        'procedure': 'PROCEDURE',
        'do': 'DO',
        'end': 'END',
        'call': 'CALL',
        'limit': 'LIMIT',
        'and': 'AND',
        'as': 'AS'
    }

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.keywords.get(t.value.lower(), 'ID')
        return t

    def t_NUMBER(self, t):
        r'\d+(\.\d+)?'
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    def t_STRING(self, t):
        r'\"([^\\\"]|\\.)*\"'
        t.value = t.value[1:-1]
        return t

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
