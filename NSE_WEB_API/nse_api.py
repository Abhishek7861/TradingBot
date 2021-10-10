import requests
import json

def getScripStrike(name):
    name = name.upper()
    if name == "NIFTY" or name == "BANKNIFTY" or name == "NIFTYIT":
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol="+name
    else:
        url = f"https://www.nseindia.com/api/option-chain-equities?symbol="+name
    baseurl = "https://www.nseindia.com/"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                            'like Gecko) '
                            'Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
    session = requests.Session()
    request = session.get(baseurl, headers=headers, timeout=5)
    cookies = dict(request.cookies)
    response = session.get(url, headers=headers, timeout=5, cookies=cookies)
    data = response.json()
    return data['records']['strikePrices']

def getScripExpiry(name):
    name = name.upper()
    if name == "NIFTY" or name == "BANKNIFTY" or name == "NIFTYIT":
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol="+name
    else:
        url = f"https://www.nseindia.com/api/option-chain-equities?symbol="+name
    baseurl = "https://www.nseindia.com/"    
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                            'like Gecko) '
                            'Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
    session = requests.Session()
    request = session.get(baseurl, headers=headers, timeout=5)
    cookies = dict(request.cookies)
    response = session.get(url, headers=headers, timeout=5, cookies=cookies)
    data = response.json()
    return data['records']['expiryDates']