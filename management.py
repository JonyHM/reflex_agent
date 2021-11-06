class Management:

  def __init__(self, dbConnect, shopping, helper):
    self.dbConnect = dbConnect
    self.shopping = shopping
    self.helper = helper
    self.products = []

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
    # if len(dbRules) > 0:
    # else:
    #   print('Você não possui nenhuma regra cadastrada! Cadastre uma para prosseguir.')
    #   self.createNewRule()

  def createNewRule(self):
    print('\nCriar nova regra\n')
    self.products = self.dbConnect.listProducts()

    rule = {}
    products = []
    product = self.helper.getNumberInput(self.products, "Insira o número do produto: ")
    print(self.products[product])
    products.append(self.products[product])

    while True:
      response = input(f'Adicionar mais um produto à regra? [S/n] ')

      if response.lower() == 'n':
        break
      elif response.lower() == 's' or response == '':
        product = self.helper.getNumberInput(self.products, "Insira o número do produto: ")
        products.append(self.products[product])
        print(self.products[product])
      else:
        print('Opção inválida! Insira S para sim ou N para não\n')

    actionId = self.helper.getNumberInput(self.products, "Insira o número da recomendação: ")
    action = self.products[actionId]
    print(f'Recomendação: {action}')

    rule['products'] = products
    rule['relation'] = '=='
    rule['action'] = action

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

  def listProducts(self):
    self.showProducts(True)

  def showProducts(self, returnToMainMenu=False):
    products = self.dbConnect.listProducts()

    if len(products) == 0:
      print('Você não possui nenhum produto cadastrado! Cadastre um para prosseguir.')
      self.createNewProduct()

    else:
      if returnToMainMenu:
        self.shopping.returnToMain(self.shopping.showManagementMenu)
      else: 
        return products

  def createNewProduct(self):
    print('\nCriar novo produto\n')

    product = input('Insira o nome do produto: ')
    response = input(f'Criar {product}? [S/n] ')

    while True:
      
      if response.lower() == 'n':
        break
      elif response.lower() == 's' or response == '':
        self.dbConnect.createProducts([product])  
        break
      else:
        print('Opção inválida! Insira S para sim ou N para não\n')
        
    print('\Produto criado com sucesso!\n')
    self.shopping.returnToMain(self.createNewProduct)

  def deleteProduct(self, productId, nameToShow):
    response = input(f'Excluír produto "{nameToShow}"? [S/n] ')

    if response.lower() == 'n':
      return
    elif response.lower() == 's' or response == '':
      self.dbConnect.deleteProductFromDB(productId)
      print(f'\nProduto "{nameToShow}" excluído com sucesso!')
    else:
      print('Opção inválida! Insira S para sim ou N para não\n')
      self.deleteProduct(productId, nameToShow)

  def productDeleteSelection(self):
    products = self.dbConnect.getProducts()

    for index, item in enumerate(products):
      print(f'{index + 1} - {item["tipos"]}')
    productId = self.helper.getNumberInput(products, 'Insira o índice do produto a ser excluído (0 para voltar): ')

    if productId == 0:
      self.shopping.showManagementMenu()

    productToDelete = products[productId - 1]
    idToDelete = productToDelete['id']
    nameToShow = productToDelete['tipos']

    self.deleteProduct(idToDelete, nameToShow)
    self.shopping.returnToMain(self.productDeleteSelection)