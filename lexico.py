import sys, os
import ply.lex as lex


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
    'STR',
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
# t_COMMA =r'\,'
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
    r'[\']|[\"][a-zA-Z_0-9]*[\'|\"]'
    return token

def t_COMMENT (token):
    r'\"[a-zA-Z_0-9_\W]*\"'
    token.type = 'COMMENT'
    return token

def t_error (token):
    print (f'Caractere ilegal {token.value[0]}')
    token.lexer.skip(1)

    

tokens_list = []
#import pdb; pdb.set_trace()
for file_in_name in range(1, len(sys.argv)):
    
# leitura do arquivo para a memoria
    file_name = str(sys.argv[file_in_name]).split('.txt')
    working_file =  file_name[0] + '_Output' + '.wrk'
    output_file = open(working_file, 'w')
    with open(str(sys.argv[file_in_name]), 'r') as source:
        source_text = source.read()
        lexical = lex.lex()
        lexical.input(source_text)
        while True:
            tkn = lexical.token()
            if not tkn:
                break
            tokens_list.append(tkn)
        for element in tokens_list:
            print (element)