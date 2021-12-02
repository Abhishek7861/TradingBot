from py5paisa.logging import log_response
from requests.models import Response
import Login as user
from PaperTrade import paperTrade
from Database.main import *
import json

class OptionTrade:
    def __init__(self,tradeId,scripSymbol,strike,expiry,optionType,positionType,Exch,ExchType,Entryprice):
        self.scripSymbol = scripSymbol
        self.strike = strike
        self.expiry = expiry
        self.optionType = optionType
        self.positionType = positionType
        self.Exch = Exch
        self.ExchType = ExchType
        self.price = float(Entryprice)
        self.active = True
        self.exitPrice = 0
        self.tradeId=tradeId
   
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
            



def printPNL(TradeObject,currentprice,Qty):
    if TradeObject.positionType == 'SELL' and TradeObject.active:
        TradeObject.printTrade()
        print( " PNL: ",(TradeObject.price-currentprice)*Qty)
    if TradeObject.positionType == 'BUY' and TradeObject.active:
        TradeObject.printTrade()
        print( " PNL: ",(currentprice-TradeObject.price)*Qty)


def start():
    client = user.loginUser()
    obj = paperTrade(client)
    createDB()
    positions = []
    Qty = 100


    while True:
        print("choose Among the below")
        print("1: Load Trade")
        print("2: Check Exited positions")
        print("3: check Active positions")
        print("4: Edit position")
        print("5: Exit Trade")
        print("6: make options paper trade")
        print("0: Exit")
        choice = input()
        if choice=='1':
            positions = []
            for trade in getAllTrade():
                if(trade[-2]=='1'):
                    TradeObject = OptionTrade(trade[0],trade[1],trade[2],trade[3],trade[4],trade[5],trade[6],trade[7],trade[8])
                    positions.append(TradeObject)
            print("--------------------------------")
            print("------Trade load Success--------")
            print("--------------------------------")




        if choice=='2':
            for trade in getAllTrade():
                if(trade[-2]=='0'):
                    TradeObject = OptionTrade(trade[0],trade[1],trade[2],trade[3],trade[4],trade[5],trade[6],trade[7],trade[8])
                    currentprice = float(trade[-1])
                    print(currentprice)
                    printPNL(TradeObject,currentprice,Qty)
                    print("---------------------------------------------")


                                    
        if choice=='3':
            if len(positions)==0:
                print("--------------------------------")
                print("---------No Positions-----------")
                print("--------------------------------")
                continue
            for position in positions:
                currentprice = obj.getLTP(position.Exch,position.ExchType,position.scripSymbol,position.expiry,position.strike,position.optionType)['Data'][0]['LastRate']
                printPNL(TradeObject,currentprice,Qty)
                print("---------------------------------------------")

        if choice=='4':
            # if len(positions)==0:
            #     print("No Positions")
            #     continue
            # print("choose a trade to edit")
            # for i in range(len(positions)):
            #     print(i,end=' ')
            #     positions[i].printTrade()
            #     print("\n---------------------------------------------")
            # choice = int(input())
            # print("Enter Price:")
            # price  = int(input())
            # print(positions[choice].tradeId)
            # positions[choice].editTrade(price)
            print("-----------------------------------")
            print("---------------TODO----------------")
            print("-----------------------------------")
            pass

        if choice=='5':
            if len(positions)==0:
                print("No Positions")
                continue
            for i in range(len(positions)):
                currentprice = obj.getLTP(positions[i].Exch,positions[i].ExchType,positions[i].scripSymbol,positions[i].expiry,positions[i].strike,positions[i].optionType)['Data'][0]['LastRate']
                print(i,end=' ')
                printPNL(positions[i],currentprice,Qty)
                print("---------------------------------------------")
            print("choose trade to exit")
            choice = int(input())
            currentprice = obj.getLTP(positions[choice].Exch,positions[choice].ExchType,positions[choice].scripSymbol,positions[choice].expiry,positions[choice].strike,positions[choice].optionType)['Data'][0]['LastRate']
            exitTrade(positions[choice].tradeId,currentprice)
            positions[choice].exitTrade(currentprice)

        if choice=='6':
            response = obj.makeTrade()
            print(response)
            TradeObject = OptionTrade(0,response[0],response[1],response[2],response[3],response[4],response[5],response[6],response[7])
            tradeId = insertTrade(TradeObject)
            TradeObject.tradeId = tradeId
            positions.append(TradeObject)
        if choice =='0':
            break    
        else:
            print("choose among given options")
 
start()
