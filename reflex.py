from unidecode import unidecode

## TODO: 
# - possibilidade de mais de uma percepção

dbRules = [
  {
    'pecepts': [
      {
        'percept': 'pao',
        'relation': '=='
      },
      {
        'percept': 'intolerancia',
        'relation': '!='
      }
    ],
    'action': 'leite'
  },
  {
    'percept': '1',
    'relation': '==',
    'action': 'dois'
  }
]


######### Eval engine #########

def evalRule(rule, percept):
  percept = unidecode(percept)
  relation = rule['relation']
  rulePercept = rule['percept']
  evaluation = True

  if len(rule['percepts']) > 1:
    for percept in rule['percepts']:
        evaluation = eval(f'percept {relation} rulePercept') and evaluation
        
    if evaluation:
      return rule['action']
    
  elif eval(f'percept {relation} rulePercept'):
    return rule['action']
  
  return None

def actionEngine(dbRule, percept):
  actions = []
  for rule in dbRule:
    ruleResult = evalRule(rule, percept)
    if ruleResult != None:
     actions.append(ruleResult)
  return actions

def startShoppingCart():
  percept = input('Informe o item da sua lista de compras: ')
  ## ask for a new item or eval
  print(actionEngine(dbRules, percept.lower()))


######### Helpers #########

def getNumberInput(options, inputTitle = 'Selecione a opção do menu: '):
  inputValue = input(inputTitle)

  try:
    inputValue = int(inputValue)
    if inputValue <= len(options):
      return inputValue
    print('Opção inválida! Tente novamente')
  except:
    print('Opção inválida! Tente novamente')
  
  return getNumberInput(options, inputTitle)

  
######### Menus #########

def returnToMain(previousMethod):
  print('\n---------------------------------------------\n')

  print('\t1 - Ver menu anterior novamente')
  print('\t2 - voltar ao menu principal')
  print('\t3 - Sair')

  print('\n---------------------------------------------\n')

  options = { 
    1 : previousMethod, 
    2 : showMainMenu,
    3 : exit
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
    1 : createNewRule, 
    2 : deleteSelection,
    3 : listRules,
    4 : showMainMenu,
    5 : exit
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
    1 : showManagementMenu, 
    2 : startShoppingCart,
    3 : exit
  }

  menuInput = getNumberInput(options)
  options[menuInput]()


######### Management #########

def listRules():
  showRules(True)

def showRules(returnToMainMenu = False):
  for index, rule in enumerate(dbRules):
    perception = rule['percept']
    opperator = rule['relation']
    action = rule['action']
    print(f'\n{index+1} -')
    print(f'Percepção: {perception}')
    print(f'Relação: {opperator}')
    print(f'Ação: {action}\n')

  if returnToMainMenu:
    returnToMain(lambda: showRules(returnToMainMenu))

def createNewRule():
  print('\nCriar nova regra\n')

  rule = {}

  rule['percept'] = input('Percepção: ')
  rule['relation'] = input('Relação: ')
  rule['action'] = input('Ação: ')

  dbRules.append(rule)
  print('\nRegra criada com sucesso!\n')
  returnToMain(createNewRule)  

def deleteRule(ruleId):
  response = input(f'Excluír regra {ruleId}? [S/n]')
  
  if response.lower() == 'n':
    return
  elif response.lower() != 's' or response != '':
    dbRules.pop(ruleId-1)
    print(f'\nRegra {ruleId} excluída com sucesso!')
  else:
    print('Opção inválida! Insira S para sim ou N para não\n')
    deleteRule(ruleId)
        
def deleteSelection():
  showRules()
  ruleId = getNumberInput(dbRules, 'Insira o índice da regra a ser excluída (0 para voltar): ')
  
  if ruleId == 0:
    showManagementMenu()
  
  deleteRule(ruleId)
  returnToMain(deleteSelection)


######### Initialization #########

showMainMenu()