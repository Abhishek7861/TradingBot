from py5paisa.logging import log_response
from requests.models import Response
import Login as user
from PaperTrade import paperTrade
from Database.main import *
import json

positions = []

class OptionTrade:
    def __init__(self,scripSymbol,strike,expiry,optionType,positionType,Exch,ExchType,Entryprice):
        self.scripSymbol = scripSymbol
        self.strike = strike
        self.expiry = expiry
        self.optionType = optionType
        self.positionType = positionType
        self.Exch = Exch
        self.ExchType = ExchType
        self.price = Entryprice
        self.active = True
        self.exitPrice = 0
   
    def printTrade(self):
        output = self.scripSymbol+" "+self.positionType+" "+str(self.price)
        print(output, end=' ')

    def editTrade(self,price):
        self.price = price
        print("Price updated!")

    def exitTrade(self,exitPrice):
        self.active = False
        self.exitPrice = exitPrice
        print("Exited at ",exitPrice)

    def getTradePNL(self):
        if self.active == False:
            if self.positionType=='SELL':
                return self.price - self.exitPrice
            elif self.positionType=='BUY':
                return self.exitPrice - self.price
            




def start():
    client = user.loginUser()
    obj = paperTrade(client)
    while True:
        print("choose Among the below")
        print("1: View all trades")
        print("2: Check Exited positions")
        print("3: check Active positions")
        print("4: Edit position")
        print("5: Exit Trade")
        print("6: make options paper trade")
        print("0: Exit")
        choice = input()
        if choice=='1':
            # getAllTrade()
            pass
        if choice=='2':
            if len(positions)==0:
                print("No Positions")
                continue
            for position in positions:
                currentprice = obj.getLTP(position.Exch,position.ExchType,position.scripSymbol,position.expiry,position.strike,position.optionType)['Data'][0]['LastRate']
                if not position.active:
                    position.printTrade()
                    print( " PNL: ",position.getTradePNL())
                print("---------------------------------------------")
        if choice=='3':
            if len(positions)==0:
                print("No Positions")
                continue
            for position in positions:
                currentprice = obj.getLTP(position.Exch,position.ExchType,position.scripSymbol,position.expiry,position.strike,position.optionType)['Data'][0]['LastRate']
                position.printTrade()
                if position.positionType == 'SELL' and position.active:
                    print( " PNL: ",position.price-currentprice)
                if position.positionType == 'BUY' and position.active:
                    print( " PNL: ",currentprice-position.price)
                print("---------------------------------------------")
        if choice=='4':
            if len(positions)==0:
                print("No Positions")
                continue
            print("choose a trade to edit")
            for i in range(len(positions)):
                print(i,end=' ')
                positions[i].printTrade()
                print("\n---------------------------------------------")
            choice = int(input())
            print("Enter Price:")
            price  = int(input())
            positions[choice].editTrade(price)
        if choice=='5':
            if len(positions)==0:
                print("No Positions")
                continue
            print("choose trade to exit")
            for i in range(len(positions)):
                currentprice = obj.getLTP(positions[i].Exch,positions[i].ExchType,positions[i].scripSymbol,positions[i].expiry,positions[i].strike,positions[i].optionType)['Data'][0]['LastRate']
                if positions[i].positionType == 'SELL' and positions[i].active:
                    print(i,end=' ')
                    positions[i].printTrade()
                    print( str(i)+" PNL: ",positions[i].price-currentprice)
                if positions[i].positionType == 'BUY' and positions[i].active:
                    print(i,end=' ')
                    positions[i].printTrade()
                    print( str(i)+" PNL: ",currentprice-positions[i].price)
                print("---------------------------------------------")
                choice = int(input())
                currentprice = obj.getLTP(positions[choice].Exch,positions[choice].ExchType,positions[choice].scripSymbol,positions[choice].expiry,positions[choice].strike,positions[choice].optionType)['Data'][0]['LastRate']
                positions[choice].exitTrade(currentprice)
        if choice=='6':
            response = obj.makeTrade()
            print(response)
            TradeObject = OptionTrade(response[0],response[1],response[2],response[3],response[4],response[5],response[6],response[7])
            # insertTrade(TradeObject)
            positions.append(TradeObject)
        if choice =='0':
            break    
        else:
            print("choose among given options")
 
start()
