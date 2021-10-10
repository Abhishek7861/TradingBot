
dateDict = {"JAN":'01',"FEB":'02',"MAR":'03',"APR":'04',"MAY":'05',"JUN":'06',
                    "JUL":'07',"AUG":'08',"SEP":'09',"OCT":'10',"NOV":'11',"DEC":'12'}

def charToNum(temp):
    date = temp.split("-")
    return date[2]+dateDict[date[1].upper()]+date[0]

def dateWithSpace(temp):
    date = temp.split("-")
    return date[0]+' '+date[1].upper()+' '+date[2]

# print(dateWithSpace('21-Oct-2021'))
# print(charToNum('21-Oct-2021'))