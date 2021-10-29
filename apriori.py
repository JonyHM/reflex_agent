import helper
import pandas as pd
import pymysql.cursors
import aprioriAlgorithm
import matplotlib.pyplot as plt

con = pymysql.connect(
  host='localhost',
  port=3306, ## porta padrão do mariaDB
  user='root',
  password='fatec',
  database='apriori',
  cursorclass=pymysql.cursors.DictCursor
)

helper = helper.Helper()

def readAndInsert():
  basket = pd.read_csv(r'./files/basket.csv')
  df = pd.DataFrame(basket)
  cursor = con.cursor()

  for row in df.itertuples():
    sql = f'''INSERT INTO basket(bsk_transaction, bsk_item, bsk_date_time, bsk_period_day, bsk_weekday_weekend) 
    VALUES ("{row.Transaction}", "{row.Item}", STR_TO_DATE("{row.date_time}", "%d-%m-%Y %H:%i"), "{row.period_day}", "{row.weekday_weekend}");'''
    print(sql)
    cursor.execute(sql)
  con.commit()
  print("dados inseridos com sucesso!!")
  sair()

def populateProduct():
  cursor = con.cursor()
  cursor.execute('SELECT distinct bsk_item as tipos from basket;')
  result = cursor.fetchall()

  items = [item['tipos'] for item in result if item['tipos']]

  for item in items:
    sql = f'''INSERT INTO product_base(pb_name) VALUES ("{item}");'''
    print(sql)
    cursor.execute(sql)
  con.commit()
  sair()

def selectTypes():
  cursor = con.cursor()
  cursor.execute('SELECT count(distinct bsk_item) as tipos from basket;')
  result = cursor.fetchall()
  print(result[0]['tipos'])
  sair()

def plotb():
  items = {}
  cursor = con.cursor()
  cursor.execute('SELECT distinct bsk_item as product from basket;')
  result = cursor.fetchall()
  
  for item in result:
    product = item['product']
    cursor.execute(f'''SELECT count(bsk_item) as total from basket where bsk_item = "{product}";''')
    
    result = cursor.fetchall()
    total = result[0]['total']
    items[product] = total
  
  names = list(items.keys())
  values = list(items.values())
  values = sorted(values)

  plt.figure(figsize=(10,100))
  plt.yticks(fontsize=8)
  plt.barh(range(len(items)), values, tick_label=names)
  plt.show()
  sair()

def plotc():
  items = {}
  cursor = con.cursor()
  cursor.execute('SELECT distinct bsk_item as product from basket;')
  result = cursor.fetchall()
  
  for item in result:
    product = item['product']
    cursor.execute(f'''SELECT count(bsk_item) as total from basket where bsk_item = "{product}" and 
    bsk_period_day = "morning";''')
    
    result = cursor.fetchall()
    total = result[0]['total']
    items[product] = total
  
  names = list(items.keys())
  values = list(items.values())
  values = sorted(values)

  plt.figure(figsize=(10,100))
  plt.yticks(fontsize=8)
  plt.barh(range(len(items)), values, tick_label=names)
  plt.show()
  sair()

def plotd():
  items = {}
  cursor = con.cursor()
  cursor.execute('SELECT distinct bsk_item as product from basket;')
  result = cursor.fetchall()
  
  for item in result:
    product = item['product']
    cursor.execute(f'''SELECT count(bsk_item) as total from basket where bsk_item = "{product}" and 
    bsk_period_day = "afternoon";''')
    
    result = cursor.fetchall()
    total = result[0]['total']
    items[product] = total
  
  names = list(items.keys())
  values = list(items.values())
  values = sorted(values)

  plt.figure(figsize=(10,100))
  plt.yticks(fontsize=8)
  plt.barh(range(len(items)), values, tick_label=names)
  plt.show()
  sair()

def plote():
  items = {}
  cursor = con.cursor()
  cursor.execute('SELECT distinct bsk_item as product from basket;')
  result = cursor.fetchall()
  
  for item in result:
    product = item['product']
    cursor.execute(f'''SELECT count(bsk_item) as total from basket where bsk_item = "{product}" and 
    bsk_period_day = "evening";''')
    
    result = cursor.fetchall()
    total = result[0]['total']
    items[product] = total
  
  names = list(items.keys())
  values = list(items.values())
  values = sorted(values)

  plt.figure(figsize=(10,100))
  plt.yticks(fontsize=8)
  plt.barh(range(len(items)), values, tick_label=names)
  plt.show()
  sair()

def apriori():
  items = []
  transactions = []

  cursor = con.cursor()
  cursor.execute('SELECT distinct pb_name as tipos from product_base;')
  result = cursor.fetchall()

  items = [item['tipos'] for item in result if item['tipos']]

  cursor.execute('select distinct bsk_transaction as value from basket;')
  result = cursor.fetchall()

  for transaction in result:
    value = transaction['value']
    cursor.execute(f'SELECT bsk_item as item FROM basket WHERE bsk_transaction = {value};')
    result = cursor.fetchall()
    values = [value['item'] for value in result if value['item']]
    transactions.append(values)
  
  ap = aprioriAlgorithm.Apriori(items, transactions)
  ap.start()
  sair()

def sair():
  con.close()
  exit()

def start():
  print('\n---------------------------------------------\n')
  print('''SISTEMAS DE RECOMENDAÇÃO E ANÁLISE DE DADOS USANDO
      AGENTES RACIONAIS E ALGORITMO APRIORI\n''')

  print('\t1 - Quantidade de tipos de produtos do mercado')
  print('\t2 - Gráfico com total de vendas de cada produto')
  print('\t3 - Gráfico com total de vendas de cada produto ocorridas de manhã')
  print('\t4 - Gráfico com total de vendas de cada produto ocorridas de tarde')
  print('\t5 - Gráfico com total de vendas de cada produto ocorridas de noite')
  print('\t6 - Associações fortes com apriori')

  print('\n\t7 - Popular banco de transações')
  print('\t8 - Popular banco de produtos')

  print('\n\n\t9 - Sair')

  print('\n---------------------------------------------\n')

  options = {
    1: selectTypes,
    2: plotb,
    3: plotc,
    4: plotd,
    5: plote,
    6: apriori,
    7: readAndInsert,
    8: populateProduct,
    9: sair
  }

  menuInput = helper.getNumberInput(options)
  options[menuInput]()