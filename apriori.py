import pandas as pd
import pymysql.cursors

con = pymysql.connect(
  host='localhost',
  port=3306, ## porta padrão do mariaDB
  user='root',
  password='fatec',
  database='apriori',
  cursorclass=pymysql.cursors.DictCursor
)

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

readAndInsert()