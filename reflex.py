import pymysql.cursors
from helper import Helper
from shopping import Shopping
from dbConnect import DBConnect
from reflexEngine import Reflex
from management import Management

def start():
    con = pymysql.connect(
        host='localhost',
        port=3306, ## porta padrão do mariaDB
        user='root',
        password='fatec',
        database='reflex',
        cursorclass=pymysql.cursors.DictCursor
    )

    reflex = Reflex([])
    db = DBConnect(con)
    helper = Helper()
    mgmt = Management(db, None, helper)
    shopping = Shopping(reflex, db, mgmt, helper)

    shopping.showMainMenu()
