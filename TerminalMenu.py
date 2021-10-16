from py5paisa.logging import log_response
from requests.models import Response
import Login as user
from PaperTrade import paperTrade
import json

positions = []

class OptionTrade:
    def __init__(self,scripSymbol,strike,expiry,optionType,positionType,Exch,ExchType,price):
        self.scripSymbol = scripSymbol
        self.strike = strike
        self.expiry = expiry
        self.optionType = optionType
        self.positionType = positionType
        self.Exch = Exch
        self.ExchType = ExchType
        self.price = price
   
    def printTrade(self):
        output = self.scripSymbol+" "+self.positionType+" "+str(self.price)
        print(output, end=' ')

    def editTrade(self,price):
        self.price = price
        print("Price updated!")



def start():
    client = user.loginUser()
    obj = paperTrade(client)
    while True:
        print("choose Among the below")
        print("1: check holding")
        print("2: load position")
        print("3: check position")
        print("4: Edit position")
        print("5: check trade book")
        print("6: make options paper trade")
        print("0: Exit")
        choice = input()
        if choice=='1':
            print(json.dumps(client.holdings(), indent = 3))
        if choice=='2':
            print(client.margin())
        if choice=='3':
            if len(positions)==0:
                print("No Positions")
                continue
            for position in positions:
                currentprice = obj.getLTP(position.Exch,position.ExchType,position.scripSymbol,position.expiry,position.strike,position.optionType)['Data'][0]['LastRate']
                position.printTrade()
                if position.positionType == 'SELL':
                    print( " PNL: ",position.price-currentprice)
                if position.positionType == 'BUY':
                    print( " PNL: ",currentprice-position.price)
                print("---------------------------------------------")
        if choice=='4':
            if len(positions)==0:
                print("No Positions")
                continue
            for i in range(len(positions)):
                print(i,end=' ')
                positions[i].printTrade()
                print("\n---------------------------------------------")
            choice = int(input())
            print("Enter Price:")
            price  = int(input())
            positions[choice].editTrade(price)
        if choice=='5':
            print(client.get_tradebook())
        if choice=='6':
            response = obj.makeTrade()
            print(response)
            TradeObject = OptionTrade(response[0],response[1],response[2],response[3],response[4],response[5],response[6],response[7])
            positions.append(TradeObject)
        if choice =='0':
            break    
        else:
            print("choose among given options")
 
start()
