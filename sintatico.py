import ply.yacc as yacc
import os, sys
from lexico import tokens, lexer
from src.file_handler import handler

VERBOSE = 1

def p_program(p):
    'program : class_list'
    p[0]=[p[1]]
    pass

def p_class_list(p):
    '''class_list : class_list  class COMMADOT
    | class COMMADOT '''

    if len(p) == 3:
        p[0] = [p[1]]
    else: 
        p[0] = p[1]
        p[0].append(p[2])
    pass

def p_class(p):
    '''class : CLASS ID OPENKEYS feature_list CLOSEKEYS
    | CLASS ID INHERITS ID OPENKEYS feature_list CLOSEKEYS'''
    if len(p) == 6:
        p[0] = ('class', p[2], p[4])
    else:
        p[0] = ('classInherits', p[2], p[4], p[6])
    pass

def p_feature_list(p):
    '''feature_list : feature_list feature
    | empty'''

    if len(p) == 2:
	    p[0] = None
    else:
        p[0] = [p[1]]
        p[0].append(p[2])
    pass

def p_feature_a(p):
    'feature : ID OPENPTH formal_list CLOSEPTH DOUBLEDOT ID OPENKEYS expr CLOSEKEYS COMMADOT'
    p[0]= ('featureparameter',p[1],p[3],p[6],p[8])
    pass


def p_feature_b(p):
    '''feature : ID DOUBLEDOT ID COMMADOT
    | ID DOUBLEDOT ID ATTR expr COMMADOT
    | empty'''
    if len(p) == 5:
        p[0] = ('featureDeclaration', p[1],p[3])
    elif len(p) == 7:
        p[0] = ('featureAnonymous', p[1], p[3], p[5])
    else:
        p[0] = None
    pass


def p_formal_list(p):
    '''formal_list : formal_list COMMA formal
    | empty
    | formal'''
    if len(p) == 4:
        p[0]=p[1]
        p[0].append(p[3])
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = None
    pass

def p_formal(p):
    'formal : ID DOUBLEDOT ID'
    p[0]=('formal', p[1],p[3])
    pass







def p_expr_Value(p):
    '''expr : ISVOID expr
     | TILDE expr
     | NOT expr
     | NEW ID
     | ID
     | NUM
     | STRING
     | TRUE
     | FALSE'''
    if len(p) == 2:
        p[0] = ('expValue',p[1])
    elif len(p) == 3:
        p[0] = ('expModifier', p[1], p[2])
    pass

def p_expr_comparator(p):
    '''expr : expr LESSTHEN expr
     | expr LESSEQUALS expr
     | expr EQUALS expr'''
    p[0] = ('exprComparator',p[2], p[1], p[3])
    pass

def p_expr_operator(p):
    '''expr : expr PLUS expr
     | expr MINUS expr 
     | expr MPLY expr
     | expr DIV expr'''
    p[0] = ('exprOperator',p[2], p[1], p[3])
    pass

def p_expr_atrib(p):
    'expr : ID ATTR expr'
    p[0] = ('exprAttr', p[1], p[2], p[3])
    pass

def p_expr_pth(p):
    'expr : OPENPTH expr CLOSEPTH'
    p[0] = ('exprPth', p[2])
    pass

def p_expr_extends_att(p):
    '''expr : expr ATT ID DOT ID OPENPTH expr_list CLOSEPTH
     | expr DOT ID OPENPTH expr_list CLOSEPTH'''

    if len(p) == 7:
        p[0] = ('expr', p[1],p[3],p[5])
    else:
        p[0] = ('exprAtt',p[1], p[3], p[5], p[7])
    pass

def p_expr_id(p):
    'expr : ID OPENPTH expr_list CLOSEPTH'
    p[0] = ('exprMethodFunction', p[1], p[3])
    pass

def p_expr_if(p):
    'expr : IF expr THEN expr ELSE expr FI'
    p[0] = ('exprIf', p[2], p[4], p[6])
    pass

def p_expr_while(p):
    'expr : WHILE expr LOOP expr POOL'
    p[0] = ('exprWhile', p[2], p[4])
    pass

def p_expr_lista(p):
    'expr : OPENKEYS exprlista CLOSEKEYS'
    p[0] = ('expr_Lista',p[2])
    pass

def p_expr_let(p):
    '''expr : LET ID DOUBLEDOT ID exprlistlet IN expr
     | LET ID DOUBLEDOT ID ATTR expr exprlistlet IN expr'''

    if len(p) == 8:
        p[0] = ('exprLet', p[2], p[4], p[5], p[7])
    else:
        p[0] = ('exprLet2', p[2], p[4], p[6], p[7], p[9])
    pass

def p_expr_case(p):
    'expr : CASE expr OF exprlistcase ESAC'
    p[0] = ('exprCase', p[2], p[4])
    pass

def p_exprlista(p):
    '''exprlista : exprlista expr COMMADOT
     | expr COMMADOT'''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[2])
    pass

def p_expr_list(p):
    '''expr_list : expr_list COMMA expr
     | expr
     | empty'''
    
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = None
    pass

def p_exprlistlet(p):
    '''exprlistlet : exprlistlet letexpr  
     | letexpr'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]
    pass

def p_letexpr(p):
    '''letexpr : COMMA ID DOUBLEDOT ID 
     | COMMA ID DOUBLEDOT ID ATTR expr
     | empty'''
    
    if len(p) == 5:
        p[0] = ('exprType', p[2], p[4])
    elif len(p) == 7:
        p[0] = ('exprType2', p[2], p[4],p[6])
    else:
        p[0] = None
    pass


def p_exprlistcase(p):
    '''exprlistcase : exprlistcase exprcase
     | exprcase'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]
    pass 

def p_exprcase(p):
    'exprcase : ID DOUBLEDOT ID CASEAT expr COMMADOT'
    p[0] = ('exprCase', p[1], p[3], p[5])
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if VERBOSE:
        if p is not None:
            print ("Erro de sintaxe na linha:" + str(p.lexer.lineno)+"  erro de Contexto " + str(p.value))
        else:
            print ("Erro no lexico na linha: " + str(lexico.lexer.lineno))
    else:
        raise Exception('Syntax', 'error')

    
parser = yacc.yacc()
file_name = str(sys.argv[1]).split('.cl')
source, output_file = handler(file_name)
tree = parser.parse(source, lexer=lexer)


if __name__ == "__main__":
    final_tokens = []
    for file_in_name in range(1, len(sys.argv)):
        file_name = str(sys.argv[file_in_name]).split('.cl')
        source, output_file = handler(file_name)
        tree = parser.parse(source, lexer=lexer)
        if tree:
            print (tree)
            output_file.write(str(tree))
        output_file.close()