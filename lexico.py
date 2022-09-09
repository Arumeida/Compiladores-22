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
    'io' : 'IO',
    'sbject' : 'OBJECT',
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
    'LESSTH',
    'LESSEQ',
    'DOT',
    'COMMA',
    'COMMADOT',
    'DOUBLEDOT',
    'ATTR',
    'OPENPTH',
    'CLOSEPTH',
    'OPENKEYS',
    'CLOSEKEYS',
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MPLY = r'\*'
t_DIV = r'\/'
t_LESSTH = r'\<'
t_LESSEQ = r'\<\='
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
t_ignore = ' \t'

def t_ID (token):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    token.type = reserved.get(token.value.lower(),'ID')
    return token

def t_NUM (token):
    r'\d+'
    return token

def t_CF (token):
    r'\n+'
    token.lexer.lineno

def t_STRING (token):
    r'\"[^"]*\"'
    return token

def t_COMMENT (token):
    r'(\(\*[^\)\*]*\*\)) | \-\-.*'
    token.type = 'COMMENT'
    return token

def t_error (token):
    tk = token.value[0]
    print (f'Caractere ilegal: ' + str(token))
    token.lexer.skip(1)


def execute (source):
    tokens_list = []
    tokens_warn = []
    lexical = lex.lex()
    lexical.input(source)
    while True:
        tkn = lexical.token()
        if not tkn:
            break
        tokens_list.append(tkn)
    return tokens_list


if __name__ == "__main__":
    final_tokens = []
    for file_in_name in range(1, len(sys.argv)):
        file_name = str(sys.argv[file_in_name]).split('.cl')
        source, output_file = handler(file_name)
        final_tokens = execute(source)
        for i in final_tokens:
            output_file.write(str(i)+'\n')
        output_file.close()