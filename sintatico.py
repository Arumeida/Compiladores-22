# -*- enconding: utf-8 -*-
#!/usr/bin/python
import ply.yacc as yacc
import os, sys
from lexico import tokens

VERBOSE = 2


def p_program(p):
    'program : class_list'
    pass

def p_class_list(p):
    '''class_list : class_list  class
    | class
    | empty'''
    #p[0] = p[1] + p[2]
    pass

def p_class(p):
    '''class : class_definition
    | empty'''
    pass

def p_class_definition_1(p):
    '''class_definition : CLASS ID feature_list
    | CLASS ID INHERITS ID feature_list
    | empty'''
    pass

# def p_class_definition_2(p):
#     'class_definition : CLASS ID INHERITS ID feature_list'
#     pass

def p_feature_list(p):
    '''feature_list : feature_list feature COMMADOT
    | empty'''
    pass

def p_feature_1(p):
    'feature : ID OPENPTH formal_list CLOSEPTH DOUBLEDOT ID OPENKEYS expression CLOSEKEYS'
    pass

def p_feature_2(p):
    '''feature : ID DOUBLEDOT ID
    | ID DOUBLEDOT ID ATTR expression
    | empty'''
    pass

def p_formal_list(p):
    '''formal_list : formal_list COMMA formal
    | empty
    | formal'''
    pass

def p_formal(p):
    'formal : ID DOUBLEDOT ID'
    pass

# def p_local_declarations_1(p):
#     'local_declarations : local_declarations var_declaration'
#     pass

# def p_local_declarations_2(p):
#     'local_declarations : empty'
#     pass

# def p_declaration(p):
#     '''declaration : var_declaration
#     | fun_declaration
#     | HASH INCLUDE LESS ID GREATER
#     | USING NAMESPACE STD SEMICOLON'''
#     pass

def p_expression_list(p):
    '''expression_list : expression_list expression COMMADOT
    | expression COMMADOT
    | empty'''
    pass

def p_expression_let_list(p):
    '''expression_let_list : expression_let_list expression_let COMMADOT
    | expression_let COMMADOT'''
    pass

def p_expression_let(p):
    '''expression_let : ID DOUBLEDOT ID
    | ID DOUBLEDOT ID ATTR expression
    | LET expression LET expression
    | empty'''


def p_expression_1(p):
    '''expression : ID ATTR expression
    | IF expression THEN expression ELSE expression FI
    | WHILE expression LOOP expression POOL
    | OPENKEYS expression_list expression CLOSEKEYS
    | CASE expression OF expression_list_case IN expression ESAC
    | NEW ID COMMADOT
    | ISVOID expression COMMADOT
    | expression PLUS expression COMMADOT
    | expression MINUS expression COMMADOT
    | expression MPLY expression COMMADOT
    | expression DIV expression COMMADOT
    | expression EQUALS expression COMMADOT
    | NOT expression
    | TILDE expression COMMADOT
    | expression LESSTHEN expression COMMADOT
    | expression LESSEQUALS COMMADOT
    | OPENPTH expression CLOSEPTH
    | ID
    | STRING
    | TRUE
    | FALSE'''
    pass

def p_expression_2(p):
    '''expression : ID OPENPTH CLOSEPTH
    | ID OPENPTH expression_list CLOSEPTH'''
    pass

def p_expression_3(p):
    '''expression : LET ID DOUBLEDOT ID
    | LET ID DOUBLEDOT ID ATT expression_let_list IN expression'''

def p_expression_4(p):
    '''expression : expression DOT ID OPENPTH CLOSEPTH
    | expression ID DOT ID OPENPTH CLOSEPTH
    | expression ID DOT ID OPENPTH expression_list CLOSEPTH
    | expression DOT ID OPENPTH expression_list CLOSEPTH'''
    pass


def p_empty(p):
    'empty :'
    pass

def p_error(p):
    #print str(dir(p))
    #print str(dir(c_lexer))
    if VERBOSE:
        if p is not None:
            print ("Error en Sintaxis linea:" + str(p.lex.lineno)+"  Error de Contexto " + str(p.value))
        else:
            print ("Error en Lexico linea: " + str(lexico.lex.lineno))
    else:
        raise Exception('Syntax', 'error')
    
parser = yacc.yacc()

if __name__ == '__main__':

    if (len(sys.argv) > 1):
        fin = sys.argv[1]
    else:
        fin = 'fuente/c.c'

    f = open(fin,'r')
    data = f.read()
    #"print (data)
    #parser.parse(data, tracking=True)
    sintax(fin)

if __name__ == "__main__":
    final_tokens = []
    for file_in_name in range(1, len(sys.argv)):
        file_name = str(sys.argv[file_in_name]).split('.cl')
        source, output_file = handler(file_name)
        syntatic = sintax(source)
        for i in final_tokens:
            output_file.write(str(i)+'\n')
        output_file.close()