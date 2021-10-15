from NSE_TOOL_LIB.getSymbolLot import *
from NSE_WEB_API.nse_api import *
from DateConvertor import *

class paperTrade:
    def __init__(self,client):
        self.quote = optionQuotes()
        self.client = client

    def makeTrade(self):
        print("Choose a SCRIP Number")
        SymbolList = self.quote.getAllOptionSymbol()
        # print(SymbolList)
        for i in range(len(SymbolList)):
            print(str(i)+":"+SymbolList[i],end='   ')
        print()
        symbolChoice = int(input())
        symbol = SymbolList[symbolChoice]
        
        print("Choose a Expiry")
        expiryList = getScripExpiry(SymbolList[symbolChoice])
        for i in range(len(expiryList)):
            print(str(i)+":"+expiryList[i],end='   ')
        print()
        expiryChoice = int(input())
        date = expiryList[expiryChoice]

        print("Choose a Strike")
        strikeList = getScripStrike(SymbolList[symbolChoice])
        for i in range(len(strikeList)):
            print(str(i)+":"+str(strikeList[i]),end='   ')
        print()
        strikeChoice = int(input())
        strike = strikeList[strikeChoice]

        print("Choose a Option Type")
        print("0: CE")
        print("1: PE")
        optionType = int(input())
        if optionType==0:
            optionType='CE'
        elif optionType==1:
            optionType='PE'

        print("Choose a Position Type")
        print("0: SELL")
        print("1: BUY")
        positionType = int(input())
        if positionType==0:
            positionType="SELL"
        elif positionType==1:
            positionType='BUY'

        scripSymbol = symbol+" "+str(dateWithSpace(date))+" "+optionType+" "+str(strike)+".00"
        expiry = charToNum(date)
        Exch='N'
        ExchType='D'

        price = self.getLTP(Exch,ExchType,scripSymbol,expiry,strike,optionType)['Data'][0]['LastRate']
        print("Order placed at : ",price)
        return (scripSymbol,strike,expiry,optionType,positionType,Exch,ExchType,price)

    def getLTP(self,Exch,ExchType,scripSymbol,expiry,strike,optionType):
        req_list_=[{"Exch":Exch,"ExchType":ExchType,"Symbol":scripSymbol,"Expiry":expiry,"StrikePrice":str(strike),"OptionType":optionType}]
        return self.client.fetch_market_feed(req_list_)

