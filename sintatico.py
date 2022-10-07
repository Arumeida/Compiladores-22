# -*- enconding: utf-8 -*-
#!/usr/bin/python
import ply.yacc as yacc
import os, sys
from lexico import tokens, lexer
from src.file_handler import handler

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

def p_feature_list(p):
    '''feature_list : feature_list feature COMMADOT
    | empty'''
    pass

def p_feature(p):
    '''feature : ID OPENPTH formal_list CLOSEPTH DOUBLEDOT ID OPENKEYS expression CLOSEKEYS
    | ID DOUBLEDOT ID
    | ID DOUBLEDOT ID ATTR expression
    | empty'''
    pass

def p_formal_list(p):
    '''formal_list : formal_list COMMA formal
    | formal
    | empty'''
    pass

def p_formal(p):
    'formal : ID DOUBLEDOT ID'
    pass

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
    pass

def p_expression_list_case(p):
    '''expression_list_case : expression_list_case expression_case COMMADOT
    | expression_case COMMADOT
    | empty'''
    pass

def p_expression_case(p):
    '''expression_case : ID DOUBLEDOT ID CASEAT expression
    | empty'''
    pass


def p_expression_1(p):
    '''expression : ID ATTR expression
    | expression DOT ID OPENPTH CLOSEPTH
    | expression DOT ID OPENPTH expression_list CLOSEPTH
    | expression ATT ID DOT ID OPENPTH CLOSEPTH
    | expression ATT ID DOT ID OPENPTH expression_list CLOSEPTH
    | ID OPENPTH CLOSEPTH
    | ID OPENPTH expression_list CLOSEPTH
    | IF expression THEN expression ELSE expression FI
    | WHILE expression LOOP expression POOL
    | OPENKEYS expression_list CLOSEKEYS
    | LET ID DOUBLEDOT ID expression_let_list IN expression
    | LET ID DOUBLEDOT ID ATT expression_let_list IN expression
    | CASE expression OF expression_list_case ESAC
    | NEW ID
    | ISVOID expression
    | expression PLUS expression
    | expression MINUS expression
    | expression MPLY expression
    | expression DIV expression
    | expression EQUALS expression
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

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    #print str(dir(p))
    #print str(dir(c_lexer))
    if VERBOSE:
        if p is not None:
            print ("Error en Sintaxis linea:" + str(p.lexer.lineno)+"  Error de Contexto " + str(p.value))
        else:
            print ("Error en Lexico linea: " + str(lexico.lexer.lineno))
    else:
        raise Exception('Syntax', 'error')
    
parser = yacc.yacc()


if __name__ == "__main__":
    final_tokens = []
    for file_in_name in range(1, len(sys.argv)):
        file_name = str(sys.argv[file_in_name]).split('.cl')
        source, output_file = handler(file_name)
        # print (source)
        result = parser.parse(source, lexer=lexer)
        if result:
            output_file.write(str(result))
        output_file.close()