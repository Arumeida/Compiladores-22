import sys, os
import ply.lex as lex


class LexAnalyser(object):
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
    'CLOSKEYS',
    ]

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

    def t_ID (self, token):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        token.type = self.reserved.get(t.value.lower(),'ID')
        return token

    def t_NUM (self, token):
        r'\d+'
        return token

    def t_CF (self, token):
        r'\n+'
        t.lexer.lineno

    def t_STRING (self, token):
        r'[\'|\"'

    def t_COMMENT (self, token):
        r'[\*[[.|\n]?]\*]|[\-\-.]'
        token.type = self.reserved.get(t.value.lower(),'COMMENT')
        return 