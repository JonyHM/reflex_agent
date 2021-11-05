import pymysql.cursors

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

    if isinstance(products, list):
      for product in products:
        productFunc = f"SELECT FNC_INSERT_PRODUCT('{product}', {ruleId})"
        self.cursor.execute(productFunc)
    else:
      productFunc = f"SELECT FNC_INSERT_PRODUCT('{products}', {ruleId})"
      self.cursor.execute(productFunc)
    
    self.connection.commit()

  def listProducts(self):
    items = []
    transactions = []
    products = {}

    self.cursor.execute('SELECT distinct pb_name as tipos from product_base;')
    result = self.cursor.fetchall()
    
    items = [item['tipos'] for item in result if item['tipos']]

    for index, item in enumerate(items):
      print(f'{index + 1} - {item}')
      products[index + 1] = item
    
    return products
  
  def insertNewTransaction(self, transactionItems):
    self.cursor.execute("select nextval(id_transaction) as ID from dual;")
    result = self.cursor.fetchone()

    transactionId = result['ID']
    
    for item in transactionItems:
      bskInsert = f'''INSERT INTO basket (bsk_transaction_id, bsk_item_name)
        VALUES ({transactionId}, "{item}");'''
      self.cursor.execute(bskInsert)  

    self.connection.commit()

  def listTransactions(self):
    transactions = []

    self.cursor.execute('SELECT distinct pb_name as tipos from product_base;')
    result = self.cursor.fetchall()

    items = [item['tipos'] for item in result if item['tipos']]

    self.cursor.execute("select distinct bsk_transaction_id as id from basket;")
    result = self.cursor.fetchall()

    ids = [item['id'] for item in result if item['id']]

    for value in ids:
      self.cursor.execute(f'SELECT bsk_item_name as item FROM basket WHERE bsk_transaction_id = {value};')
      result = self.cursor.fetchall()
      values = set([value['item'] for value in result if value['item']])
      transactions.append(values)

    return (items, transactions)

  def deleteRuleFromDB(self, ruleId):
    deleteFunc = f"DELETE FROM rules WHERE id_rules = {ruleId};"
    self.cursor.execute(deleteFunc)
    self.connection.commit()