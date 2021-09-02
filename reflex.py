from unidecode import unidecode
import pymysql.cursors


######## Eval engine #########

class Reflex:
   
    def __init__(self, percepts):
        self.percepts = percepts
    

    def getPercepts(self):
        return self.percepts


    def setPercepts(self, percepts):
        self.percepts = percepts


    def evalRule(self, rule):
        relation = rule['relation']
        action = rule['action']
        evaluation = False
        ruleEval = []

        if len(rule['products']['values']) > 1:
            for rulePercept in rule['products']['values']:
                for inputPercept in self.percepts:
                    inputPercept = unidecode(inputPercept)
                    rulePercept = unidecode(rulePercept)
                    evaluation = eval(f'inputPercept {relation} rulePercept')
                    if evaluation:
                        break
                ruleEval.append(evaluation)

            if len(ruleEval) == len(rule['products']['values']) and all(ruleEval) and action not in self.percepts:
                return action

        else:
            for inputPercept in self.percepts:
                rulePercept = unidecode(rule['products']['values'][0])
                inputPercept = unidecode(inputPercept)
                evaluation = eval(f'inputPercept {relation} rulePercept')
                if evaluation and action not in self.percepts:
                    return action

        return None


    def actionEngine(self, dbRules):
        actions = []

        for rule in dbRules:
            ruleResult = self.evalRule(rule)
            if ruleResult != None and ruleResult not in actions:
                actions.append(ruleResult)

        self.setPercepts([])       
        
        return actions
    


######### DB #########

class DBConnect:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.dbRules = []


    def getConnection(self):
        return self.connection


    def setConnection(self, connection):
        self.connection = connection


    def getCursor(self):
        return self.cursor


    def setCursor(self, cursor):
        self.cursor = cursor


    def getDbRules(self):
        self.updateRules()
        return self.dbRules
    

    def setDbRules(self, rules):
        self.dbRules = rules


    def exitProject(self):
        self.connection.close()
        exit()


    def updateRules(self):
        self.dbRules = []
        self.dbRules = self.createDict()


    def createDict(self):
        percepts = []
        relation = []
        self.cursor.execute('select * from rules')
        result = self.cursor.fetchall()
        for i, val in enumerate(result):
            self.cursor.execute(f'select percept from all_percepts where id_rules = {val["id_rules"]}')
            result = self.cursor.fetchall()
            products = {}
            products['values'] = []
            products['id'] = val["id_rules"]
            for product in result:
                products['values'].append(product['percept'])
            relation.append(products)
        
        for i, val in enumerate(relation):
            self.cursor.execute('select * from rules')
            result = self.cursor.fetchall()
            percepts.append({
                'products': val,
                'relation': result[i]['relation'],
                'action': result[i]['action_rules']
            })
        return percepts


    def createRuleAndProducts(self, rule):
        products = rule['products']
        relation = rule['relation']
        action = rule['action']

        ruleFunc = f"SELECT FNC_INSERT_RULE('{relation}', '{action}') as id"
        self.cursor.execute(ruleFunc)
        result = self.cursor.fetchone()
        self.connection.commit()
        ruleId = 1

        if result['id'] != None:
            ruleId = result['id']

        for product in products:
            productFunc = f"SELECT FNC_INSERT_PRODUCT('{product}', {ruleId})"
            self.cursor.execute(productFunc)
        
        self.connection.commit()


    def deleteRuleFromDB(self, ruleId):
        deleteFunc = f"DELETE FROM rules WHERE id_rules = {ruleId};"
        self.cursor.execute(deleteFunc)
        self.connection.commit()







class Shopping:

    def __init__(self, reflex, dbConnect, management, helper):
        self.reflex = reflex
        self.dbConnect = dbConnect
        self.management = management
        self.management.setShopping(self)
        self.helper = helper


    def addItemToCard(self, title='Informe o novo item da sua lista de compras: '):
        percept = input(title)
        self.reflex.percepts.append(percept)


    def startShoppingCart(self):
        self.dbConnect.updateRules()

        if len(self.dbConnect.getDbRules()) > 0:
            self.addItemToCard()
            self.shoppingCartMenu()
        else:
            print('Você não possui nenhuma regra cadastrada! Cadastre uma para prosseguir.')
            self.management.createNewRule()


    def evaluateRules(self):
        self.dbConnect.updateRules()
        engineReturn = self.reflex.actionEngine(self.dbConnect.getDbRules())

        print(engineReturn)
        self.finalMenu()


    ######### Menus #########

    def returnToMain(self, previousMethod):
        print('\n---------------------------------------------\n')

        print('\t1 - Voltar ao menu anterior')
        print('\n\t2 - voltar ao menu principal')
        print('\n\n\t3 - Sair')

        print('\n---------------------------------------------\n')

        options = {
            1: previousMethod,
            2: self.showMainMenu,
            3: self.exitProject
        }

        menuInput = self.helper.getNumberInput(options)
        options[menuInput]()


    def finalMenu(self):
        print('\n---------------------------------------------\n')

        print('\t1 - Voltar ao menu principal')
        print('\n\n\t2 - Sair')

        print('\n---------------------------------------------\n')

        options = {
            1: self.showMainMenu,
            2: self.exitProject
        }

        menuInput = self.helper.getNumberInput(options)
        options[menuInput]()


    def shoppingCartMenu(self):
        
        while True:
            response = input(f'Gostaria de adicionar um novo item na lista? [S/n] ')

            if response.lower() == 'n':
                self.evaluateRules()
                break
            elif response.lower() == 's' or response == '':
                self.startShoppingCart()
            else:
                print('Opção inválida! Insira S para sim ou N para não\n')


    def showManagementMenu(self):
        print('\n---------------------------------------------\n')
        print('Gerenciamento\n')

        print('\t1 - Criar nova regra')
        print('\t2 - Excluir item da lista')
        print('\t3 - Listar regras')
        print('\n\t4 - Voltar ao menu principal')
        print('\n\n\t5 - Sair')

        print('\n---------------------------------------------\n')

        options = {
            1: self.management.createNewRule,
            2: self.management.deleteSelection,
            3: self.management.listRules,
            4: self.showMainMenu,
            5: self.exitProject
        }

        menuInput = self.helper.getNumberInput(options)
        options[menuInput]()


    def showMainMenu(self):
        print('\n---------------------------------------------\n')
        print('Menu principal\n')

        print('\t1 - Gerenciamento de regras')
        print('\t2 - Iniciar compras')
        print('\n\n\t3 - Sair')

        print('\n---------------------------------------------\n')

        options = {
            1: self.showManagementMenu,
            2: self.startShoppingCart,
            3: self.exitProject
        }

        menuInput = self.helper.getNumberInput(options)
        options[menuInput]()


    def exitProject(self):
        self.dbConnect.exitProject()



######### Helpers #########

class Helper:
        
    def getNumberInput(self, options, inputTitle='Selecione a opção do menu: '):
        inputValue = input(inputTitle)

        try:
            inputValue = int(inputValue)
            if inputValue <= len(options):
                return inputValue
            print('Opção inválida! Tente novamente')
        except:
            print('Opção inválida! Tente novamente')

        return self.getNumberInput(options, inputTitle)

    

######### Management #########

class Management:

    def __init__(self, dbConnect, shopping, helper):
        self.dbConnect = dbConnect
        self.shopping = shopping
        self.helper = helper


    def getDbConnect(self):
        return self.dbConnect


    def setDbConnect(self, connect):
        self.dbConnect = connect


    def getShopping(self):
        return self.shopping


    def setShopping(self, shopping):
        self.shopping = shopping


    def listRules(self):
        self.showRules(True)


    def showRules(self, returnToMainMenu=False):
        self.dbConnect.updateRules()
        dbRules = self.dbConnect.getDbRules()

        if len(dbRules) > 0:
            for index, rule in enumerate(dbRules):
                products = '; '.join(rule['products']['values'])
                relation = rule['relation']
                action = rule['action']
                
                print(f'\n{index + 1} -')
                print(f'Produtos: {products}')
                print(f'Relação: {relation}')
                print(f'Recomendação: {action}\n')

            if returnToMainMenu:
                self.shopping.returnToMain(self.shopping.showManagementMenu)
        else:
            print('Você não possui nenhuma regra cadastrada! Cadastre uma para prosseguir.')
            self.createNewRule()


    def createNewRule(self):
        print('\nCriar nova regra\n')

        rule = {}
        products = []
        product = input('Produto: ')
        products.append(product)

        while True:
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

        self.dbConnect.createRuleAndProducts(rule)
        
        print('\nRegra criada com sucesso!\n')
        self.shopping.returnToMain(self.createNewRule)


    def deleteRule(self, ruleId, idToShow):
        response = input(f'Excluír regra {idToShow}? [S/n] ')

        if response.lower() == 'n':
            return
        elif response.lower() == 's' or response == '':
            self.dbConnect.deleteRuleFromDB(ruleId)
            print(f'\nRegra {idToShow} excluída com sucesso!')
        else:
            print('Opção inválida! Insira S para sim ou N para não\n')
            self.deleteRule(ruleId)


    def deleteSelection(self):
        self.showRules()
        self.dbConnect.updateRules()
        dbRules = self.dbConnect.getDbRules()

        ruleId = self.helper.getNumberInput(dbRules, 'Insira o índice da regra a ser excluída (0 para voltar): ')

        if ruleId == 0:
            self.shopping.showManagementMenu()

        idToDelete = dbRules[ruleId - 1]['products']['id']
        self.deleteRule(idToDelete, ruleId)
        self.shopping.returnToMain(self.deleteSelection)



######### Initialization #########

def start():

    con = pymysql.connect(
        host='localhost',
        port=3306, ## porta padrão do mariaDB
        user='root',
        password='fatec',
        database='reflex',
        cursorclass=pymysql.cursors.DictCursor
    )

    reflex = Reflex([])
    db = DBConnect(con)
    helper = Helper()
    mgmt = Management(db, None, helper)
    shopping = Shopping(reflex, db, mgmt, helper)

    shopping.showMainMenu()


start()