import reflex as reflexModule
import apriori as aprioriModule
import helper as helperModule

def reflexAgent():
  reflexModule.start()

def apriori():
  aprioriModule.start()

print('\n---------------------------------------------\n')
print('''SISTEMAS DE RECOMENDAÇÃO E ANÁLISE DE DADOS\n''')

print('\t1 - Agente reflexivo')
print('\t2 - Algoritmo Apriori')
print('\n\n\t3 - Sair')

print('\n---------------------------------------------\n')

options = {
  1: reflexAgent,
  2: apriori,
  3: exit
}

helper = helperModule.Helper()
menuInput = helper.getNumberInput(options)
options[menuInput]()