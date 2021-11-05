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
      self.deleteRule(ruleId, idToShow)

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
