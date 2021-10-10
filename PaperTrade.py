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

        scripSymbol = symbol+" "+str(dateWithSpace(date))+" CE "+str(strike)+".00"
        expiry = charToNum(date)
        print(scripSymbol)
        print(strike)
        print(expiry)

        #NOTE : Symbol has to be in the same format as specified in the example below.
        req_list_=[{"Exch":"N","ExchType":"D","Symbol":scripSymbol,"Expiry":expiry,"StrikePrice":str(strike),"OptionType":"CE"}]
        print(req_list_)
        print(self.client.fetch_market_feed(req_list_))


