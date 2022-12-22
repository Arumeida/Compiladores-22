from sintatico import tree
import copy

#lista de tipos (<nome>, <pai>, <metodos>, <atributos>)
TypeList = [('Object', None, [('abort', [], 'Object'), ('type_name', [], 'String'), ('copy', [], 'SELF_TYPE')], [('self', 'Object')]),
            ('SELF_TYPE', None, [], []), ('IO', 'Object', [('out_string', [('x', 'String')], 'SELF_TYPE'), ('out_int', [('x', 'Int')], 'SELF_TYPE'), ('in_string', [], 'String'),
    ('in_int', [], 'Int')], []), ('Int', 'IO', [], []), ('String', 'IO',
[('length', [], 'Int'), ('concat', [('s', 'String')], 'String'), ('substr', [('i', 'Int'), ('l', 'Int')], 'String')],
[]), ('Bool', 'IO', [], [])]

MethodsList = []
IDsList = []

scope = 'program'

for Type in TypeList:
    for method in Type[2]:
        MethodsList.append(method)


for Type in TypeList:
    for ID in Type[3]:
        IDsList.append(ID)


def percorretree( token ):
    if type(token) == list or type(token) == tuple:
        for child in token:
            percorretree(child)
        print(token[0])


def execute( token, IDsList, MethodsList, TypeList ):
    if token == None:
        return

    newTypeList = []
    newIDsList = []
    newMethodsList = []
    newTypeList = TypeList



    if isNewScopeClass(token[0]):
        global scope
        scope = token[1]
        newMethodsList = copy.deepcopy(MethodsList)
        newIDsList = IDsList
    elif isNewScopeMethod(token[0]) or isNewScopeLet(token[0]):
        newIDsList = copy.deepcopy(IDsList)
        newMethodsList = MethodsList
    else:
        newTypeList = TypeList
        newIDsList = IDsList
        newMethodsList = MethodsList

    if token[0] == 'idType':
        get_IdType(token, IDsList, newTypeList)
    elif token[0] == 'expID':
        get_ExprId(token, newIDsList)
    elif token[0] == 'expType':
        get_ExprLetSeta(token, newIDsList, newTypeList)
        execute(token[5], newIDsList, newMethodsList, newTypeList)
    elif token[0] == 'expLet':
        get_ExprLet(token, newIDsList, newTypeList)
        execute(token[4], newIDsList, newMethodsList, newTypeList)
    elif token[0] == 'expBetweenKeys':
        execute(token[1], newIDsList, newMethodsList, newTypeList)
    elif token[0] == 'expWhile':
        get_ExprWhile(token, newIDsList)
        execute(token[3], newIDsList, newMethodsList, newTypeList)
    elif token[0] == 'expIf':
        get_ExprIf(token, newIDsList)
        execute(token[2], newIDsList, newMethodsList, newTypeList)
        execute(token[3], newIDsList, newMethodsList, newTypeList)
    elif token[0] == 'exprCallMethod':
        get_ExprCallMethod(token, newMethodsList, newIDsList)
    elif token[0] == 'expATT':
        nome = None
        methodName = None
        if token[1][0] == 'exprCallMethod':
            nome = getMetodo(token[1][1], newMethodsList)[2]
            methodName = token[1][1]
        else:
            aux = getId(token[1][1], newIDsList)
            methodName = t[2][1]
            if aux != None:
                nome = aux[1]

        if nome != None:
            tipo = getType(nome, newTypeList)
            if nome == 'SELF_TYPE':
                configSelfType(newIDsList, newMethodsList, newTypeList)
            if not isInListMethod(t[2][1], tipo[2]):
                print("Erro de chamada: metodo %s não pertence ao tipo %s" % methodName, nome)
        execute(token[1], newIDsList, newMethodsList, newTypeList)
    elif token[0] == 'expWithoutAtt':
        nome = None
        methodName = None
        if token[1][0] == 'exprCallMethod':
            nome = getMetodo(t[1][1], newMethodsList)[2]
            methodName = token[1][1]
        else:
            aux = getId(t[1][1], newIDsList)
            methodName = token[2][1]
            if aux != None:
                nome = aux[1]

        if nome != None:
            tipo = getType(nome, newTypeList)
            if nome == 'SELF_TYPE':
                configSelfType(newIDsList, newMethodsList, newTypeList)
            if not isInListMetodo(methodName, tipo[2]):
                print("Erro de chamada: metodo %s não pertence ao tipo %s" % methodName, nome)
        execute(token[1], newIDsList, newMethodsList, newTypeList)
    elif token[0] == 'exprEntreParenteses':
        execute(t[1], newIDsList, newMethodsList, newTypeList)
    elif token[0] == 'expAtrib':
        get_ExprSeta(token, newIDsList)
    elif token[0] == 'exprOperator':
        get_Op(token, newIDsList)
    elif token[0] == 'exprComparator':
        get_Comp(token, newIDsList)
    elif token[0] == 'expNew':
        get_ExprNew(token, newIDsList)
    elif token[0] == 'expValue':
        get_ExprVoid(token, newIDsList)
    elif token[0] == 'expNot':
        get_ExprNot(token, newIDsList)
    elif token[0] == 'formal':
        get_Formal(token, newIDsList, newTypeList)
    elif token[0] == 'featureReturnParametro':
        get_FeatureRetornoParametro(token, newIDsList, newMethodsList, newTypeList)
        for formal in token[4]:
            execute(formal, newIDsList, newMethodsList, newTypeList)
    elif token[0] == 'featureReturn':
        get_FeatureRetorno(token, newMethodsList, newTypeList)
        execute(token[3], newIDsList, newMethodsList, newTypeList)
    elif token[0] == 'featureAnonimus':
        get_featureAnonima(token, newIDsList, newTypeList)
        for formal in token[2]:
            execute(formal, newIDsList, newMethodsList, newTypeList)
    elif token[0] == 'featureDeclaration':
        get_FeatureDeclaration(token, newIDsList, newTypeList)
    elif token[0] == 'class':
        for formal in token[2]:
            execute(formal, newIDsList, newMethodsList, newTypeList)
    elif token[0] == 'classInherits':
        get_ClasseInherits(token, newTypeList)
        for formal in token[3]:
            if type(formal) == list:
                for i in formal:
                    execute(i, newIDsList, newMethodsList, newTypeList)
            else:
                execute(formal, newIDsList, newMethodsList, newTypeList)
    else:
        if type(token) == list:
            for i in token:
                execute(i, newIDsList, newMethodsList, newTypeList)


def get_IdType( token, IDsList, TypeList ):
    if len(token) == 4:
        aux = ('featureAnonima', token[1], token[2], token[3])
        get_featureAnonima(aux, IDsList, TypeList)
    elif len(token) == 3:
        aux = ('featureDeclaration', token[1], token[2])
        get_FeatureDeclaration(aux, IDsList, TypeList)
    pass


def get_ExprId( token, IDsList ):
    if not isInListId(token[1], IDsList):
        print(f"Erro de declaração: {token[1]} não foi declarado")


def get_ExprLetAtrib( token, IDsList, TypeList ):
    aux = ('featureAnonima', token[1], token[2])
    get_featureAnonima(aux, IDsList, TypeList)
    for fanonima in token[3]:
        if fanonima != None:
            get_IdType(fanonima, IDsList, TypeList)


def get_ExprLet( token, IDsList, TypeList ):
    aux = ('featureDeclaration', token[1], token[2])
    get_FeatureDeclaration(aux, IDsList, TypeList)
    for fanonima in token[3]:
        if fanonima != None:
            get_IdType(fanonima, IDsList, TypeList)


def get_ExprWhile( token, IDsList ):
    if token[1][0] == 'exprComparator':
        get_Comparation(token[1], IDsList)
        return
    if token[1][0] == 'expNot':
        get_ExprNot(token[1], IDsList)
        return
    print(f'Erro de declaração: expressão {token[1]} não é booleano')


def get_ExprIf( token, IDsList ):
    if token[1][0] == 'exprComparator':
        get_Comparation(token[1], IDsList)
        return
    if token[1][0] == 'expNot':
        get_ExprNottoken([1], IDsList)
        return
    print(f"Erro de declaração: expressão {token[1]} não é booleano")


def get_ExprCallMethod( token, MethodsList, IDsList ):
    if not isInListMetodo(token[1], MethodsList):
        print(f"Erro de chamada: metodo {token[1]} não declarado" % token[1])
    verificaParametroCall(token[2], getMetodo(token[1], MethodsList), IDsList)


def get_ExprBetweenParenthesis( token ):
    pass


def get_ExprAtrib( token, IDsList ):
    if getId(token[1], IDsList) == None:
        print(f"Erro de atribuição: {token[1]} não foi declarada")
    elif token[3][0] == 'operation':
        get_Operation(token[3], IDsList)
    elif token[3][0] == 'expID':
        id = getId(token[3][1], IDsList)
        if id == None:
            print(f"Erro de atribuição: {token[1]} não foi declarada")
    return token[1]


def get_Operation( token, IDsList ):
    id1 = getId(token[2], IDsList)
    id2 = getId(token[3], IDsList)

    if id1 == None:
        tryParseInt(token[2][1], IDsList)
    elif id1[1] != "Int":
        print(f"Erro de operação: {id1[0]} deve ser do tipo Int")
    if id2 == None:
        tryParseInt(token[3][1], IDsList)
    elif id2[1] != "Int":
        print(f"Erro de operação: {id2[0]} deve ser do tipo Int")


def get_Comparation( token, IDsList ):
    if token[2][0] == 'expNot':
        id1 = getId(token[2][2][1], IDsList)
    elif token[2][0] == 'operation':
        get_Op(token[2], IDsList)
        id1 = (0, 'Int')
    else:
        id1 = getId(token[2][1], IDsList)
    if t[3][0] == 'expNot':
        id2 = getId(token[3][2][1], IDsList)
    elif token[3][0] == 'opration':
        get_Op(token[3], IDsList)
        id2 = (0, 'Int')
    else:
        id2 = getId(t[3][1], IDsList)

    if id1 == None:
        if type(tryConvertInt(token[2][1])) != int:
            print(f"Erro de declaração: {token[2][1]} não foi declarado" % token[2][1])
        id1 = (str(tryConvertInt(token[2][1])), 'Int')
    if id2 == None:
        if type(tryConvertInt(token[3][1])) != int:
            print(f"Erro de declaração: {token[3][1]} não foi declarado" % token[3][1])
        id2 = (str(tryConvertInt(token[3][1])), 'Int')
    if id1[1] != id2[1]:
        print(f"Erro de comparação: {id1[0]} {id2[0]} devem ser do mesmo tipo" % id1[0], id2[0])


def get_ExprNew( token, TypeList ):
    if not isInListType(token[2], TypeList):
        print(f"Erro de declaração: tipo {token[2]} não foi declarado")


def get_ExprValue( token, IDsList ):
    if not isInListId(token[2], IDsList):
        print(f"Erro de declaração: {token[2]} não foi declarado")


def get_ExprNot( token, IDsList ):
    if token[2][0] == 'exprComparator':
        get_Comparation(token[2], IDsList)
        return
    print(f"Erro de declaração: expressão {token[2]} não é booleano")


def get_Formal( token, IDsList, TypeList ):
    if isInListId(token[1], IDsList):
        print(f"Erro de declaração: {token[1]} já declarado")
    if not isInListType(token[2], TypeList):
        print(f"Erro de declaração: tipo {token[2]} não foi declarado")
    IDsList.append((token[1], token[2]))


def get_FeatureRetornoParametro( token, IDsList, MethodsList, TypeList ):
    if isInListMetodo(token[1], MethodsList):
        print(f"Erro de declaração: method {token[1]} já declarado")
    if not isInListType(token[3], TypeList):
        print(f"Erro de declaração: tipo {token[3]} não foi declarado")
    verificaParametro(token[2], TypeList)
    method = (token[1], [], token[3])
    tipo = getType(scope, TypeList)
    if tipo != None:
        tipo[2].append(method)
    for id in token[2]:
        newId = (id[1], id[2])
        IDsList.append(newId)   
        method[1].append(newId)
    MethodsList.append(method)


def get_FeatureRetorno( token, MethodList, TypeList ):
    if isInListMetodo(token[1], MethodList):
        print(f"Erro de declaração: method {token[1]} já declarado")
    if not isInListType(token[2], TypeList):
        print(f"Erro de declaração: tipo {token[2]} não foi declarado")
    method = (token[1], [], token[2])
    tipo = getType(scope, TypeList)
    if tipo != None:
        tipo[2].append(method)
    MethodList.append(method)


def get_featureAnonima( token, IDsList, TypeList ):
    if isInListId(token[1], IDsList):
        print(f"Erro de declaração: variavel {token[1]} já declarada")
    if not isInListType(token[2], TypeList):
        print(f"Erro de declaração: tipo {token[2]} não foi declarado")
    if token[2] == 'String':
        if type(token[3][1]) != str:
            print(f"Erro de declaração: valor incompativel com a variavel {token[1]}")
    if token[2] == 'Int':
        if type(token[3][1]) != int:
            print(f"Erro de declaração: valor incompativel com a variavel {token[1]}")

    IDsList.append((token[1], token[2]))


def get_FeatureDeclaration( token, IDsList, TypeList ):
    if isInListId(token[1], IDsList):
        print(f"Erro de declaração: variavel {token[1]} já declarada")
    if not isInListType(token[2], TypeList):
        print(f"Erro de declaração: tipo {token[1]} não foi declarado")
    IDsList.append((token[1], token[2]))


def get_ClasseInherits( token, TypeList ):
    inherits = getType(token[2], TypeList)
    classe = getType(token[1], TypeList)
    if inherits == None:
        print(f"Tipo '{token[2]}' não declarado")
    else:
        for method in inherits[2]:
            classe[2].append(method)
        for id in inherits[3]:
            classe[3].append(id)


def isInListType( item, lista ):
    for i in lista:
        if item == i[0]:
            return True
    return False


def isInListId( item, lista ):
    for i in lista:
        if item == i[0]:
            return True
    return False


def getId( nome, lista ):
    for item in lista:
        if item[0] == nome:
            return item
    return None


def tryParseInt( valor, IDsList ):
    try:
        valor = int(valor)
    except:
        if isInListId(valor, IDsList):
            tipo = getId(valor, IDsList)[1]
            if tipo == 'Int':
                return
        print(f'Erro de conversão: {valor} não é do tipo inteiro')


def tryConvertInt( s ):
    try:
        return int(s)
    except:
        return s


def isInListMetodo( metodo, lista ):
    for i in lista:
        if metodo == i[0]:
            return True
    return False


def verificaParametro( parametros, TypeList ):
    idsParametros = []
    for parametro in parametros:
        if not isInListType(parametro[2], TypeList):
            print(f"Erro de declaração: tipo {parametro[2]} não foi declarado")
        if parametro[1] in idsParametros:
            print(f"Erro de declaração: id {parametro[1]} já utilizado por outro parametro")
        idsParametros.append(parametro[1])


def verificaParametroCall( parametros, metodo, IDsList ):
    if parametros[0] == None:
        del (parametros[0])
    if len(parametros) != len(metodo[1]):
        print(f"Erro de chamada: metodo {metodo[0]} deve conter {metodo[1]} parametros" % metodo[0], len(metodo[1]))
    for i in range(0, len(parametros)):
        if not isInListId(parametros[i][1], IDsList):
            if metodo[1][i][1] == 'Int':
                tryParseInt(parametros[i][1], IDsList)
            elif metodo[1][i][1] != 'String':
                print(f'Erro de chamada: parametro {parametros[i][1]} de tipo incorreto')
            if parametros[i][0] != 'exprValores':
                print(f'Erro de chamada: id {parametros[i][1]} não foi declarado')
        else:
            parametro = getId(parametros[i][1], IDsList)
            if parametro[1] != metodo[1][i][1]:
                print(f"Erro de chamada: parametro {parametros[i][1]} de tipo incorreto" % parametros[i][1])


def getMetodo( nome, MethodList ):
    for method in MethodList:
        if nome == method[0]:
            return method
    return None


def getType( nome, TypeList ):
    for tipo in TypeList:
        if nome == tipo[0]:
            return tipo
    return None


def isNewScopeClass(s):
    return s == 'classInherits' or s == 'class'


def isNewScopeMethod( s ):
    return s == 'featureRetornoParametro' or s == 'featureRetorno'


def isNewScopeLet( s ):
    return s == 'exprLetAtrib' or s == 'exprLet'


def configSelfType( IDsList, MethodsList, TypeList ):
    selftype = getType('SELF_TYPE', TypeList)
    selftype[2].clear()
    selftype[3].clear()
    for metodo in MethodsList:
        selftype[2].append(metodo)
    for id in IDsList:
        selftype[3].append(id)


for child in tree[0]:
    if type(child) == tuple:
        if isInListType(child[1], TypeList):
            print(f"Erro de declaração: tipo {child[1]} já foi declarado")
        if child[0] == 'class':
            TypeList.append((child[1], None, [], []))
        elif child[0] == 'classInherits':
            TypeList.append((child[1], child[2], [], []))

for child in tree[0]:
    execute(child, IDsList, MethodsList, TypeList)

