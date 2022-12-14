# -*- enconding: utf-8 -*-
#!/usr/bin/python
import sys, os
import ply.lex as lex
from src.file_handler import handler


reserved = {
    'class' : 'CLASS',
    'else' : 'ELSE',
    'false' : 'FALSE',
    'fi' : 'FI',
    'if' : 'IF',
    'in' : 'IN',
    'inherits' : 'INHERITS',
    'isvoid' : 'ISVOID',
    'let' : 'LET',
    'loop' : 'LOOP',
    'pool' : 'POOL',
    'then' : 'THEN',
    'while' : 'WHILE',
    'case' : 'CASE',
    'esac' : 'ESAC',
    'new' : 'NEW',
    'of' : 'OF',
    'not' : 'NOT',
    'true' : 'TRUE',
}

tokens = [
    'ID',
    'NUM',
    'STRING',
    'MINUS',
    'PLUS',
    'MPLY',
    'DIV',
    'EQUALS',
    'LESSTHEN',
    'LESSEQUALS',
    'DOT',
    'COMMA',
    'COMMADOT',
    'DOUBLEDOT',
    'ATTR',
    'OPENPTH',
    'CLOSEPTH',
    'OPENKEYS',
    'CLOSEKEYS',
    'ATT',
    'CASEAT',
    'TILDE',
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MPLY = r'\*'
t_DIV = r'\/'
t_LESSTHEN = r'\<'
t_LESSEQUALS = r'\<\='
t_EQUALS = r'\='
t_ATTR = r'\<\-'
t_DOT = r'\.'
t_COMMA =r'\,'
t_DOUBLEDOT = r'\:'
t_COMMADOT = r'\;'
t_OPENPTH = r'\('
t_CLOSEPTH = r'\)'
t_OPENKEYS = r'\{'
t_CLOSEKEYS = r'\}'
t_ATT = r'\@'
t_CASEAT = r'\=\>'
t_TILDE = r'\~'
t_ignore = ' \t'

def t_ID(token):
    r'[a-zA-Z_]+([a-zA-Z0-9_]*)'
    token.type = reserved.get(token.value.lower(), 'ID')
    return token

def t_NUM (token):
    r'\d+'
    return token

def t_CF (token):
    r'\n+'
    token.lexer.lineno += len(token.value)

def t_STRING (token):
    r'\"[^"]*\"'
    return token

def t_COMMENT(token):
    r'(\(\*(.|\n)*?\*\))|(--.*)'
    pass

def t_error (token):
    tk = token.value[0]
    print (f'Caractere ilegal: ' + str(tk))
    token.lexer.skip(1)


lexer = lex.lex()

# def execute (source):
#     tokens_list = []
#     tokens_warn = []
#     lexical = lex.lex()
#     lexical.input(source)
#     while True:
#         tkn = lexical.token()
#         if not tkn:
#             break
#         tokens_list.append(tkn)
#     return tokens_list

# if __name__ == "__main__":
#     final_tokens = []
#     for file_in_name in range(1, len(sys.argv)):
#         file_name = str(sys.argv[file_in_name]).split('.cl')
#         source, output_file = handler(file_name)
#         final_tokens = execute(source)
#         for i in final_tokens:
#             output_file.write(str(i)+'\n')
#         output_file.close()