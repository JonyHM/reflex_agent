from unidecode import unidecode
import pymysql.cursors

# TODO:
# - Mudar nomes dos elementos da regra
# - Validar todas as funcionalidades 

con = pymysql.connect(
    host='localhost',
    user='root',
    password='fatec',
    database='reflex',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = con.cursor()
percepts = []

######## Eval engine #########

def evalRule(rule, percepts):
    relation = rule['relation']
    action = unidecode(rule['action'])
    evaluation = False
    ruleEval = []

    if len(rule['products']) > 1:
        for rulePercept in rule['products']:
            for inputPercept in percepts:
                inputPercept = unidecode(inputPercept)
                evaluation = eval(f'inputPercept {relation} rulePercept')
                if evaluation:
                    break
            ruleEval.append(evaluation)

        if len(ruleEval) == len(rule['products']) and all(ruleEval) and action not in percepts:
            return action

    else:
        for inputPercept in percepts:
            rulePercept = unidecode(rule['products'][0])
            inputPercept = unidecode(inputPercept)
            evaluation = eval(f'inputPercept {relation} rulePercept')
            if evaluation and action not in percepts:
                return action

    return None


def actionEngine(dbRule, percept):
    actions = []
    for rule in dbRule:
        ruleResult = evalRule(rule, percept)
        if ruleResult != None:
            actions.append(ruleResult)
    return actions


def addItemToCard(title='Informe o novo item da sua lista de compras: '):
    percept = input(title)
    percepts.append(percept)


def startShoppingCart():
    dbRules = createDict()

    if len(dbRules) > 0:
        addItemToCard()
        shoppingCartMenu()
    else:
        print('Você não possui nenhuma regra cadastrada! Cadastre uma para prosseguir.')
        createNewRule()


def evaluateRules():
    dbRules = createDict()
    print(actionEngine(dbRules, percepts))
    finalMenu()


######### Helpers #########

def getNumberInput(options, inputTitle='Selecione a opção do menu: '):
    inputValue = input(inputTitle)

    try:
        inputValue = int(inputValue)
        if inputValue <= len(options):
            return inputValue
        print('Opção inválida! Tente novamente')
    except:
        print('Opção inválida! Tente novamente')

    return getNumberInput(options, inputTitle)

def exitProject():
    con.close()
    exit()

def parse_sql(filename):
    data = open(filename, 'r').readlines()
    stmts = []
    DELIMITER = ';'
    stmt = ''

    for lineno, line in enumerate(data):
        if not line.strip():
            continue

        if line.startswith('--'):
            continue

        if 'DELIMITER' in line:
            DELIMITER = line.split()[1]
            continue

        if (DELIMITER not in line):
            stmt += line.replace(DELIMITER, ';')
            continue

        if stmt:
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())
    return stmts


######### DB #########

def createRuleAndProducts(rule):
    products = rule['products']
    relation = rule['relation']
    action = rule['action']

    ruleFunc = f"SELECT FNC_INSERT_RULE('{relation}', '{action}') as id"
    cursor.execute(ruleFunc)
    result = cursor.fetchone()
    con.commit()
    ruleId = 1

    if result['id'] != None:
        ruleId = result['id']

    for product in products:
        productFunc = f"SELECT FNC_INSERT_PRODUCT('{product}', {ruleId})"
        cursor.execute(productFunc)
    
    con.commit()

def deleteRuleFromDB(ruleId):
    deleteFunc = f"DELETE FROM rules WHERE id_rules = {ruleId};"
    cursor.execute(deleteFunc)
    con.commit()

def createDict():
    percepts = []
    relation = []
    cursor.execute('select * from all_percepts')
    result = cursor.fetchall()
    
    for i, val in enumerate(result):
        cursor.execute(f'select percept from all_percepts where id_rules = {i + 1}')
        result = cursor.fetchall()
        products = []
        for product in result:
            products.append(product['percept'])
        relation.append(products)
    
    for i, val in enumerate(relation):
        cursor.execute('select * from all_percepts')
        result = cursor.fetchall()
        percepts.append({
            'products': val,
            'relation': result[i]['relation'],
            'action': result[i]['action']
        })
    return percepts


######### Menus #########


def returnToMain(previousMethod):
    print('\n---------------------------------------------\n')

    print('\t1 - Ver menu anterior novamente')
    print('\t2 - voltar ao menu principal')
    print('\t3 - Sair')

    print('\n---------------------------------------------\n')

    options = {
        1: previousMethod,
        2: showMainMenu,
        3: exitProject
    }

    menuInput = getNumberInput(options)
    options[menuInput]()


def finalMenu():
    print('\n---------------------------------------------\n')

    print('\t1 - Voltar ao menu principal')
    print('\t2 - Sair')

    print('\n---------------------------------------------\n')

    options = {
        1: showMainMenu,
        2: exit
    }

    menuInput = getNumberInput(options)
    options[menuInput]()


def shoppingCartMenu():
    print('Gostaria de adicionar um novo item na lista?')
    print('\t1 - Sim')
    print('\t2 - Não\n')

    options = {
        1: startShoppingCart,
        2: evaluateRules
    }

    menuInput = getNumberInput(options)
    options[menuInput]()


def showManagementMenu():
    print('\n---------------------------------------------\n')
    print('Gerenciamento\n')

    print('\t1 - Criar nova regra')
    print('\t2 - Excluir item da lista')
    print('\t3 - Listar regras')
    print('\t4 - Voltar ao menu principal')
    print('\t5 - Sair')

    print('\n---------------------------------------------\n')

    options = {
        1: createNewRule,
        2: deleteSelection,
        3: listRules,
        4: showMainMenu,
        5: exitProject
    }

    menuInput = getNumberInput(options)
    options[menuInput]()


def showMainMenu():
    print('\n---------------------------------------------\n')
    print('Menu principal\n')

    print('\t1 - Gerenciamento de regras')
    print('\t2 - Iniciar compras')
    print('\t3 - Sair')

    print('\n---------------------------------------------\n')

    options = {
        1: showManagementMenu,
        2: startShoppingCart,
        3: exitProject
    }

    menuInput = getNumberInput(options)
    options[menuInput]()


######### Management #########

def listRules():
    showRules(True)


def showRules(returnToMainMenu=False):
    dbRules = createDict()
    for index, rule in enumerate(dbRules):
        products = '; '.join(rule['products'])
        relation = rule['relation']
        action = rule['action']
        
        print(f'\n{index + 1} -')
        print(f'Produtos: {products}')
        print(f'Relação: {relation}')
        print(f'Recomendação: {action}\n')

    if returnToMainMenu:
        returnToMain(showManagementMenu)


def createNewRule():
    print('\nCriar nova regra\n')

    rule = {}
    products = []
    product = input('Produto: ')
    products.append(product)
    response = None

    while response.lower() != 'n' or response.lower() != 's' or response != '':
        response = input(f'Adicionar mais um produto à regra? [S/n] ')

        if response.lower() == 'n':
            break
        elif response.lower() == 's' or response == '':
            product = input('Produto: ')
            products.append(product)

        else:
            print('Opção inválida! Insira S para sim ou N para não\n')

    rule['products'] = products
    rule['relation'] = '=='
    rule['action'] = input('Recomendação: ')

    createRuleAndProducts(rule)
    
    print('\nRegra criada com sucesso!\n')
    returnToMain(createNewRule)


def deleteRule(ruleId):
    response = input(f'Excluír regra {ruleId}? [S/n] ')

    if response.lower() == 'n':
        return
    elif response.lower() == 's' or response == '':
        deleteRuleFromDB(ruleId)
        print(f'\nRegra {ruleId} excluída com sucesso!')
    else:
        print('Opção inválida! Insira S para sim ou N para não\n')
        deleteRule(ruleId)


def deleteSelection():
    showRules()
    dbRules = createDict()
    ruleId = getNumberInput(
        dbRules, 'Insira o índice da regra a ser excluída (0 para voltar): ')

    if ruleId == 0:
        showManagementMenu()

    deleteRule(ruleId)
    returnToMain(deleteSelection)


######### Initialization #########

# stmts = parse_sql('db\\tables.sql')
# for line in stmts:
#     print(line)
#     cursor.execute(line)

# rules = cursor.fetchall()
# rule = rules[0]
# print(rule['action_rules'])

showMainMenu()

# rule = {}
# rule['products'] = ['café', 'açúcar', 'queijo', 'leite']
# rule['relation'] = '=='
# rule['action'] = 'pão'

# createRuleAndProducts(rule)
# ruleId = input('id: ')
# deleteRuleFromDB(int(ruleId))
