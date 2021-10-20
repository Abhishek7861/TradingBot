import sqlite3

def createDB():
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    # Create table
    cur.execute('''CREATE TABLE stocks
                   (scripSymbol text, strike text, expiry text, optionType text, positionType text, 
                   Exch text, ExchType text, price text, active text, exitPrice text)''')
    # Save (commit) the changes
    con.commit()

def insertTrade(object):
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    # Insert a row of data
    query = "INSERT INTO stocks (scripSymbol, strike , expiry , optionType , positionType , Exch , ExchType , price , active , exitPrice ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",object.scripSymbol,object.strike,object.expiry,object.optionType,object.positionType,object.Exch,object.ExchType,object.price,object.active,object.exitPrice
    print(query)
    cur.execute(query)
    # Save (commit) the changes
    con.commit()


def getAllTrade():
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM stocks'):
        print(row)

# createDB()
# getAllTrade()