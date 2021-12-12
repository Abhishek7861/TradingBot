from py5paisa.logging import log_response
from requests.models import Response
import Login as user
from PaperTrade import paperTrade
from Database.TradesDB import *
from Database.basketDB import *
import json
import time
import os
from Objects.basket import Basket
from datetime import datetime

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
        print( " | Entry: "+str(TradeObject.price)," | LTP: "+str(currentprice)+" |  PNL: ",(TradeObject.price-currentprice)*Qty)
    if TradeObject.positionType == 'BUY' and TradeObject.active:
        TradeObject.printTrade()
        print( " | Entry: "+str(TradeObject.price)," | LTP: "+str(currentprice)+" |  PNL: ",(currentprice-TradeObject.price)*Qty)

def getPNL(TradeObject,Qty,obj):
    currentprice = obj.getLTP(TradeObject.Exch,TradeObject.ExchType,TradeObject.scripSymbol,TradeObject.expiry,TradeObject.strike,TradeObject.optionType)['Data'][0]['LastRate']
    if TradeObject.positionType == 'SELL' and TradeObject.active:
        return (TradeObject.price-currentprice)*Qty
    if TradeObject.positionType == 'BUY' and TradeObject.active:
        return (currentprice-TradeObject.price)*Qty

def getExitedPNL(TradeObject,Qty):
    if TradeObject.positionType == 'SELL' and TradeObject.active:
        return (TradeObject.price-TradeObject.exitPrice)*Qty
    if TradeObject.positionType == 'BUY' and TradeObject.active:
        return (TradeObject.exitPrice-TradeObject.price)*Qty

def createBasket():
    print("Insert STOP LOSS Percentage")
    slPercent = int(input())
    print("Insert BOOK PROFIT Percentage")
    bpPercent = int(input())
    now = datetime.now()
    basket = Basket(0,now,slPercent,bpPercent,True)
    basket.id = insertBasket(basket)
    print("Basket CREATED")
    return basket

def viewActiveBasket(obj):
    print("Select id to view Basket")
    baskets = getAllActiveBasket()
    if len(baskets)==0:
        print("No Active Basket Found")
        return
    for idx, basket in enumerate(baskets):
        if(basket[4] == True):
            basketObject = Basket(basket[0],basket[1],basket[2],basket[3],basket[4])
            basketObject.display()
    choice = input()
    for trade in getAllTrade(choice):
        TradeObject = OptionTrade(trade[0],trade[1],trade[2],trade[3],trade[4],trade[5],trade[6],trade[7],trade[8])
        currentprice = obj.getLTP(TradeObject.Exch,TradeObject.ExchType,TradeObject.scripSymbol,TradeObject.expiry,TradeObject.strike,TradeObject.optionType)['Data'][0]['LastRate']
        printPNL(TradeObject,currentprice,Qty)

def viewExitBasket():
    print("Select id to view Basket")
    baskets = getAllExitedBasket()
    if len(baskets)==0:
        print("No Exited Basket Found")
        return
    for idx, basket in enumerate(baskets):
        if(basket[4] == False):
            basketObject = Basket(basket[0],basket[1],basket[2],basket[3],basket[4])
            basketObject.display()
    choice = int(input())
    positions = []
    for trade in getAllTrade(choice):
        TradeObject = OptionTrade(trade[0],trade[1],trade[2],trade[3],trade[4],trade[5],trade[6],trade[7],trade[8])
        TradeObject.exitPrice = float(trade[-2])
        positions.append(TradeObject)
    PNL = 0
    for position in positions:
        PNL = PNL+getExitedPNL(position,Qty)
        position.printTrade()
        print()
    print("PNL: ",PNL)

def editActiveBasket():
    print("Select id to edit ")
    baskets = getAllActiveBasket()
    for idx, basket in enumerate(baskets):
        if(basket[4] == True):
            basketObject = Basket(basket[0],basket[1],basket[2],basket[3],basket[4])
            basketObject.display()
    choice = int(input())
    print("Insert new STOP LOSS Percentage")
    slPercent = int(input())
    print("Insert new BOOK PROFIT Percentage")
    bpPercent = int(input())
    basketObject.slPercent = slPercent
    basketObject.bpPercent = bpPercent
    updateBasket(basketObject,choice)

def addTradeToBasket(obj):
    print("Select id of Basket")
    baskets = getAllActiveBasket()
    if len(baskets)==0:
        print("No Basket Found")
        return
    for idx, basket in enumerate(baskets):
        if(basket[4] == True):
            basketObject = Basket(basket[0],basket[1],basket[2],basket[3],basket[4])
            basketObject.display()
    choice = int(input())
    response = obj.makeTrade()
    print(response)
    TradeObject = OptionTrade(0,response[0],response[1],response[2],response[3],response[4],response[5],response[6],response[7])
    insertTrade(TradeObject,choice)

def RunAlgo(obj):
    print("Select index of Basket")
    baskets = getAllActiveBasket()
    if len(baskets)==0:
        print("No Basket Found")
        return
    for idx, basket in enumerate(baskets):
        if(basket[4] == True):
            print("index :",idx)
            basketObject = Basket(basket[0],basket[1],basket[2],basket[3],basket[4])
            basketObject.display()
    choice = int(input())
    basket = baskets[choice]
    basketObject = Basket(basket[0],basket[1],basket[2],basket[3],basket[4])
    positions = []
    for trade in getAllTrade(basketObject.id):
        TradeObject = OptionTrade(trade[0],trade[1],trade[2],trade[3],trade[4],trade[5],trade[6],trade[7],trade[8])
        positions.append(TradeObject)
    while True:
        MTM = 0
        value = 0
        StopLoss = 0
        BookProfit = 0
        for position in positions:
            if TradeObject.positionType == 'SELL':
                value = value+position.price
            MTM = MTM+ getPNL(position,Qty,obj)
        StopLoss = -1*(value*basketObject.slPercent)/100
        BookProfit = (value*basketObject.slPercent)/100
        print("MTM: ",MTM)
        print("Value: ",value)
        print("StopLoss: ",StopLoss*Qty)
        print("BookProfit: ",BookProfit*Qty)
        if MTM >= BookProfit*Qty or MTM <= StopLoss*Qty:
            for position in positions:
                currentprice = obj.getLTP(position.Exch,position.ExchType,position.scripSymbol,position.expiry,position.strike,position.optionType)['Data'][0]['LastRate']
                exitTrade(position.tradeId,currentprice)
            exitBasket(basketObject.id)
            return
        time.sleep(1)
        clear()


def init():
    client = user.loginUser()
    obj = paperTrade(client)
    while(1):
        print("---------------------------------")
        print("-------------BASKET--------------")
        print("---------------------------------")
        print("choose below options")
        print("1: Create New Basket")
        print("2: View Active Basket")
        print("3: Edit Active Basket")
        print("4: Exit All Basket Trades")
        print("5: View Exited Baskets")
        print("6: Add Trade to Basket")
        print("7: Exit Trade from Basket")
        print("8: Run Algo")
        print("0: Exit")
        choice = input()
        clear()
        if choice == '1':
            retval = createBasket()
            retval.display()
        if choice == '2':
            viewActiveBasket(obj)
        if choice == '3':
            editActiveBasket()
        if choice == '4':
            print("TODO!")
        if choice == '5':
            viewExitBasket()
        if choice == '6':
            addTradeToBasket(obj)
        if choice == '7':
            print("TODO")
        if choice == '8':
            RunAlgo(obj)
        if choice == '0':
            return

clear = lambda: os.system('clear')
# start()
Qty = 100
createBasketTable()
createTradeTable()
init()