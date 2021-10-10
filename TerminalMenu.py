from py5paisa.logging import log_response
import Login as user
from PaperTrade import paperTrade
import json

def start():
    client = user.loginUser()
    while True:
        print("choose Among the below")
        print("1: check holding")
        print("2: check margin")
        print("3: check position")
        print("4: check order book")
        print("5: check trade book")
        print("6: make options paper trade")
        print("0: Exit")
        choice = input()
        if choice=='1':
            print(json.dumps(client.holdings(), indent = 3))
        if choice=='2':
            print(client.margin())
        if choice=='3':
            print(client.positions())
        if choice=='4':
            print(client.order_book())
        if choice=='5':
            print(client.get_tradebook())
        if choice=='6':
            obj = paperTrade(client)
            obj.makeTrade()
        if choice =='0':
            break    
        else:
            print("choose among given options")
 
start()
