from aprioriAlgorithm import Apriori

class Shopping:
  
  def __init__(self, reflex, dbConnect, management, helper, products = {}):
    self.reflex = reflex
    self.dbConnect = dbConnect
    self.management = management
    self.management.setShopping(self)
    self.helper = helper
    self.products = products

  def addItemToCard(self, title='Informe o novo item da sua lista de compras: '):
    percept = self.helper.getNumberInput(self.products, title)
    index = int(percept)
    print(f'Adicionando: {self.products[index]}')
    self.reflex.percepts.append(self.products[index])

  def startShoppingCart(self):
    self.listProducts()
    self.dbConnect.updateRules()

    self.addItemToCard()
    self.shoppingCartMenu()
    # if len(self.dbConnect.getDbRules()) > 0:
    # else:
    #   print('Você não possui nenhuma regra cadastrada! Cadastre uma para prosseguir.')
    #   self.management.createNewRule()

  def evaluateRules(self):
    self.dbConnect.updateRules()
    self.dbConnect.insertNewTransaction(self.reflex.getPercepts())

    engineReturn = self.reflex.actionEngine(self.dbConnect.getDbRules())
    print(engineReturn)
    self.finalMenu()
  
  def listProducts(self):
    self.products = self.dbConnect.listProducts()

  def applyAprioriEngine(self):
    items, transactions = self.dbConnect.listTransactions()
    
    ap = Apriori(items, transactions)
    rules = ap.start(0.6, 0.8)
    for rule in rules:
      self.dbConnect.createRuleAndProducts(rule)    
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
    print('\t4 - Criar novo produto')
    print('\t5 - Excluir produto da lista')
    print('\t6 - Listar produtos')

    print('\n\t7 - Voltar ao menu principal')
    print('\n\n\t8 - Sair')

    print('\n---------------------------------------------\n')

    options = {
      1: self.management.createNewRule,
      2: self.management.deleteSelection,
      3: self.management.listRules,
      4: self.management.createNewProduct,
      5: self.management.productDeleteSelection,
      6: self.management.listProducts,
      7: self.showMainMenu,
      8: self.exitProject
    }

    menuInput = self.helper.getNumberInput(options)
    options[menuInput]()

  def showMainMenu(self):
    print('\n---------------------------------------------\n')
    print('Menu principal\n')

    print('\t1 - Gerenciamento de regras e produtos')
    print('\t2 - Iniciar compras')
    print('\t3 - Algoritmo Apriori')
    print('\n\n\t4 - Sair')

    print('\n---------------------------------------------\n')

    options = {
      1: self.showManagementMenu,
      2: self.startShoppingCart,
      3: self.applyAprioriEngine,
      4: self.exitProject
    }

    menuInput = self.helper.getNumberInput(options)
    options[menuInput]()

  def exitProject(self):
    self.dbConnect.exitProject() 