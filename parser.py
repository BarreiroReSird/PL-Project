# parser.py - Analisador sintático para CQL

import ply.yacc as yacc
from lexer import CQLLexer


class CQLParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)

    def parse(self, text):
        return self.parser.parse(text, lexer=self.lexer.lexer)

    # Precedência dos operadores
    precedence = (
        ('left', 'AND'),
        ('left', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'),
    )

    # Regras gramaticais
    def p_program(self, p):
        '''program : command_list'''
        p[0] = ('PROGRAM', p[1])

    def p_command_list(self, p):
        '''command_list : command SEMICOLON
                       | command SEMICOLON command_list'''
        if len(p) == 3:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_command(self, p):
        '''command : import_cmd
                  | export_cmd
                  | discard_cmd
                  | rename_cmd
                  | print_cmd
                  | select_cmd
                  | create_cmd
                  | procedure_def
                  | procedure_call'''
        p[0] = p[1]

    # Comandos de configuração de tabelas
    def p_import_cmd(self, p):
        'import_cmd : IMPORT TABLE ID FROM STRING'
        p[0] = ('IMPORT', p[3], p[5])

    def p_export_cmd(self, p):
        'export_cmd : EXPORT TABLE ID AS STRING'
        p[0] = ('EXPORT', p[3], p[5])

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at end of input")

    def build(self):
        self.parser = yacc.yacc(module=self)

    def p_discard_cmd(self, p):
        'discard_cmd : DISCARD TABLE ID'
        p[0] = ('DISCARD', p[3])

    def p_rename_cmd(self, p):
        'rename_cmd : RENAME TABLE ID ID'
        p[0] = ('RENAME', p[3], p[4])

    def p_print_cmd(self, p):
        'print_cmd : PRINT TABLE ID'
        p[0] = ('PRINT', p[3])

    def p_select_cmd(self, p):
        '''select_cmd : SELECT select_list FROM table_reference
                     | SELECT select_list FROM table_reference WHERE condition
                     | SELECT select_list FROM table_reference LIMIT NUMBER
                     | SELECT select_list FROM table_reference WHERE condition LIMIT NUMBER'''
        if len(p) == 5:
            p[0] = ('SELECT', p[2], p[4], None, None)
        elif len(p) == 7 and p[5] == 'LIMIT':
            p[0] = ('SELECT', p[2], p[4], None, p[6])
        elif len(p) == 7:
            p[0] = ('SELECT', p[2], p[4], p[6], None)
        else:
            p[0] = ('SELECT', p[2], p[4], p[6], p[8])

    def p_table_reference(self, p):
        '''table_reference : ID
                          | TABLE ID'''
        p[0] = p[1] if len(p) == 2 else p[2]

    def p_select_list(self, p):
        '''select_list : STAR
                      | ID
                      | select_list COMMA ID'''
        if len(p) == 2:
            if p[1] == '*':
                p[0] = '*'  # Caso especial para *
            else:
                p[0] = [p[1]]  # Para um único ID
        else:
            if p[1] == '*':
                p[0] = '*'  # Mantém * se estiver presente
            elif isinstance(p[1], list):
                p[0] = p[1] + [p[3]]  # Adiciona mais um ID à lista
            else:
                p[0] = [p[1], p[3]]  # Cria lista com dois IDs

    def p_condition(self, p):
        '''condition : expression
                    | condition AND condition'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('AND', p[1], p[3])

    def p_expression(self, p):
        '''expression : ID LT NUMBER
                     | ID GT NUMBER
                     | ID LE NUMBER
                     | ID GE NUMBER
                     | ID EQ NUMBER
                     | ID NE NUMBER'''
        p[0] = (p[2], p[1], p[3])

    def p_create_cmd(self, p):
        '''create_cmd : CREATE TABLE ID
                 | CREATE TABLE ID select_cmd'''
        if len(p) == 4:
            p[0] = ('CREATE', p[3])
        else:
        # Transforma o SELECT em um comando normal, mas marcado para criação de tabela
            select_cmd = p[4]
        select_cmd = ('CREATE_SELECT', p[3], *select_cmd[1:])  # Adiciona o nome da nova tabela
        p[0] = select_cmd

    def p_procedure_def(self, p):
        'procedure_def : PROCEDURE ID DO command_list END'
        p[0] = ('PROCEDURE_DEF', p[2], p[4])

    def p_procedure_call(self, p):
        'procedure_call : CALL ID'
        p[0] = ('PROCEDURE_CALL', p[2])
