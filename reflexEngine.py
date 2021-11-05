from unidecode import unidecode

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
