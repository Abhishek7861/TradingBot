from nsetools import Nse

class optionQuotes():
    def __init__(self):
        self.nse = Nse()
        self.LotSizeDict = self.nse.get_fno_lot_sizes()
        self.scripDict = dict()

    def getAllOptionSymbol(self):
        res = []
        for i in self.LotSizeDict:
            res.append(i)
        return res

    def getOptionSymbolLot(self,name):
        return self.LotSizeDict[name]



# obj = optionQuotes()
# print(obj.getAllOptionSymbol())
# print(obj.getOptionSymbolLot('NIFTY'))
