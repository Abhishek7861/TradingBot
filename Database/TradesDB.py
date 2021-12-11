import sqlite3
DatabaseName = 'TradingBotDB.db'


def createTradeTable():
    con = sqlite3.connect(DatabaseName)
    cur = con.cursor()
    # Create table
    cur.execute('''CREATE TABLE IF NOT EXISTS trade
                   (ID INTEGER PRIMARY KEY AUTOINCREMENT, scripSymbol text, strike text, expiry text, optionType text, positionType text, 
                    Exch text, ExchType text, price text, active text, exitPrice text, basketId INTEGER,
                    CONSTRAINT fk_basket
                    FOREIGN KEY (basketId)
                    REFERENCES basket(id))''')
    # Save (commit) the changes
    con.commit()

def insertTrade(object,id):
    con = sqlite3.connect(DatabaseName)
    cur = con.cursor()
    # Insert a row of data
    query = "INSERT INTO trade (scripSymbol, strike , expiry , optionType , positionType , Exch , ExchType , price , active , exitPrice, basketId) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
    cur.execute(query,(object.scripSymbol,object.strike,object.expiry,object.optionType,object.positionType,object.Exch,object.ExchType,object.price,object.active,object.exitPrice,id))
    print("--------------------------------------")
    print("Inserted trade in Basket ID: ",id)
    print("--------------------------------------")
    # Save (commit) the changes
    con.commit()
    return cur.lastrowid


def getAllTrade(choice):
    trade = []
    con = sqlite3.connect(DatabaseName)
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM trade WHERE basketId = '+str(choice)):
        trade.append(row)
    # print(trade)
    return trade

def exitTrade(id,price):
    con = sqlite3.connect(DatabaseName)
    cur = con.cursor()
    cur.execute("UPDATE trade SET active = '0',exitPrice = "+str(price)+" WHERE ID = "+str(id)+";")
    con.commit()
    print("--------------------------------------")
    print("Exited trade with ID: ",cur.lastrowid)
    print("--------------------------------------")
