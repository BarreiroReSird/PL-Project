import ply.yacc as yacc
from lexer import tokens
from interpreter import execute_command

precedence = ()

def p_program(p):
    """program : statements"""
    pass

def p_statements_multiple(p):
    """statements : statements statement"""
    pass

def p_statements_single(p):
    """statements : statement"""
    pass

def p_statement(p):
    """statement : command SEMICOLON"""
    execute_command(p[1])

def p_command_import(p):
    """command : IMPORT TABLE ID FROM STRING"""
    p[0] = ('IMPORT', p[3], p[5])

def p_command_export(p):
    """command : EXPORT TABLE ID TO STRING"""
    p[0] = ('EXPORT', p[3], p[5])

def p_command_discard(p):
    """command : DISCARD TABLE ID"""
    p[0] = ('DISCARD', p[3])

def p_command_rename(p):
    """command : RENAME TABLE ID TO ID"""
    p[0] = ('RENAME', p[3], p[5])

def p_command_print(p):
    """command : PRINT TABLE ID"""
    p[0] = ('PRINT', p[3])

def p_command_create(p):
    """command : CREATE TABLE ID FROM query"""
    p[0] = ('CREATE', p[3], p[5])

def p_command_call(p):
    """command : CALL ID"""
    p[0] = ('CALL', p[2])

def p_command_proc(p):
    """command : PROCEDURE ID BEGIN statements END"""
    p[0] = ('PROCEDURE', p[2], p[4])

def p_query(p):
    """query : SELECT field_list FROM ID where_clause limit_clause"""
    p[0] = ('SELECT', p[2], p[4], p[5], p[6])

def p_query_join(p):
    """query : SELECT field_list FROM ID JOIN ID ON ID EQ ID where_clause limit_clause"""
    p[0] = ('JOIN', p[2], p[4], p[6], p[8], p[10], p[11], p[12])

def p_field_list_all(p):
    """field_list : ASTERISK"""
    p[0] = ['*']

def p_field_list(p):
    """field_list : ID
                  | ID COMMA field_list"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_where_clause_empty(p):
    """where_clause : """
    p[0] = None

def p_where_clause_expr(p):
    """where_clause : WHERE condition"""
    p[0] = p[2]

def p_condition(p):
    """condition : ID EQUALS STRING
                 | ID EQ STRING
                 | ID GT STRING
                 | ID LT STRING
                 | ID GE STRING
                 | ID LE STRING
                 | ID NE STRING"""
    p[0] = (p[2], p[1], p[3])

def p_limit_clause_empty(p):
    """limit_clause : """
    p[0] = None

def p_limit_clause(p):
    """limit_clause : LIMIT NUMBER"""
    p[0] = p[2]

def p_error(p):
    if p:
        print(f"Erro de sintaxe na linha {p.lineno}, perto de '{p.value}'")
    else:
        print("Erro de sintaxe no fim do input")

parser = yacc.yacc()
