import sqlite3
DatabaseName = 'TradingBotDB.db'


def createBasketTable():
    con = sqlite3.connect(DatabaseName)
    cur = con.cursor()
    # Create table
    cur.execute('''CREATE TABLE IF NOT EXISTS basket
                   (ID INTEGER PRIMARY KEY AUTOINCREMENT, name text, slPercent INTEGER(10), bpPercent INTEGER(10), active BOOLEAN)''')
    # Save (commit) the changes
    con.commit()

def insertBasket(object):
    con = sqlite3.connect(DatabaseName)
    cur = con.cursor()
    # Insert a row of data
    query = "INSERT INTO basket (name, slPercent , bpPercent , active) VALUES (?,?,?,?)"
    cur.execute(query,(object.name,object.slPercent,object.bpPercent,object.active))
    print("--------------------------------------")
    print("Created basket with ID: ",cur.lastrowid)
    print("--------------------------------------")
    # Save (commit) the changes
    con.commit()
    return cur.lastrowid

def getAllExitedBasket():
    basket = []
    con = sqlite3.connect(DatabaseName)
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM Basket WHERE active = 0'):
        basket.append(row)
    # print(basket)
    return basket

def getAllActiveBasket():
    basket = []
    con = sqlite3.connect(DatabaseName)
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM Basket WHERE active = 1'):
        basket.append(row)
    # print(basket)
    return basket

def updateBasket(object,id):
    object.display()
    con = sqlite3.connect(DatabaseName)
    cur = con.cursor()
    cur.execute("UPDATE Basket SET slPercent = "+str(object.slPercent)+",bpPercent = "+str(object.bpPercent)+" WHERE ID = "+str(id)+";")
    con.commit()
    print("--------------------------------------")
    print("Updated Basket with ID: ",cur.lastrowid)
    print("--------------------------------------")

def exitBasket(id):
    con = sqlite3.connect(DatabaseName)
    cur = con.cursor()
    cur.execute("UPDATE Basket SET active = "+str(0)+" WHERE ID = "+str(id)+";")
    con.commit()
    print("--------------------------------------")
    print("Exited Basket with ID: ",cur.lastrowid)
    print("--------------------------------------")

# createBasketTable()
# print(getAllBasket())