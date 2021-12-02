import sqlite3
DatabaseName = 'trades.db'


def createDB():
    con = sqlite3.connect(DatabaseName)
    cur = con.cursor()
    # Create table
    cur.execute('''CREATE TABLE IF NOT EXISTS stocks
                   (ID INTEGER PRIMARY KEY AUTOINCREMENT, scripSymbol text, strike text, expiry text, optionType text, positionType text, 
                   Exch text, ExchType text, price text, active text, exitPrice text)''')
    # Save (commit) the changes
    con.commit()

def insertTrade(object):
    con = sqlite3.connect(DatabaseName)
    cur = con.cursor()
    # Insert a row of data
    query = "INSERT INTO stocks (scripSymbol, strike , expiry , optionType , positionType , Exch , ExchType , price , active , exitPrice ) VALUES (?,?,?,?,?,?,?,?,?,?)"
    cur.execute(query,(object.scripSymbol,object.strike,object.expiry,object.optionType,object.positionType,object.Exch,object.ExchType,object.price,object.active,object.exitPrice))
    print("--------------------------------------")
    print("Inserted trade with ID: ",cur.lastrowid)
    print("--------------------------------------")
    # Save (commit) the changes
    con.commit()
    return cur.lastrowid


def getAllTrade():
    trades = []
    con = sqlite3.connect(DatabaseName)
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM stocks'):
        trades.append(row)
    # print(trades)
    return trades

def exitTrade(id,price):
    con = sqlite3.connect(DatabaseName)
    cur = con.cursor()
    cur.execute("UPDATE stocks SET active = '0',exitPrice = "+str(price)+" WHERE ID = "+str(id)+";")
    con.commit()
    print("--------------------------------------")
    print("Exited trade with ID: ",cur.lastrowid)
    print("--------------------------------------")
