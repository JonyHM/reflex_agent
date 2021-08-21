## TODO: 
# - Conexão com o MariaDB; 
# - Gerenciamento de regras (criar, excluir e visualizar regras)
# - Menu para escolher entre gerenciamento e validação de regras.

dbRule = [
  {
    'percept': 'pão',
    'relation': '==',
    'action': 'leite'
  },
  {
    'percept': '1',
    'relation': '==',
    'action': 'dois'
  }
]

def evalRule(rule, percept):
  relation = rule['relation']
  rulePercept = rule['percept']
  if eval(f'percept {relation} rulePercept'):
    return rule['action']
  else:
    return None

def actionEngine(dbRule, percept):
  actions = []
  for rule in dbRule:
    ruleResult = evalRule(rule, percept)
    if ruleResult != None:
     actions.append(ruleResult)
  return actions

percept = input()
print(actionEngine(dbRule, percept))

