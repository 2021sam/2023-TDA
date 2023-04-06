import requests
from private.credentials import client_id, username, password, redirect_uri
# from OAuth import OAuth

# auth = OAuth()

# Get Quote
# <Response [200]> → Success
endpoint = 'https://api.tdameritrade.com/v1/marketdata/SPY/quotes'
# headers = {'Authorization':'Bearer {}'.format(auth.tokens['access_token'])}
params = {'apikey': client_id}
# content = requests.get( url = endpoint, params = params, headers = headers )
content = requests.get( url = endpoint, params = params )
# content
quote = content.json()

print( quote['SPY'] )
for i in quote['SPY']:
	print( f'{i}: { quote["SPY"][i] }' )

print( quote['SPY']['closePrice'] )
low_price = quote['SPY']['lowPrice']
high_price = quote['SPY']['highPrice']
print( quote['SPY']['totalVolume'])


# gap		=	yesterday_close - open_price
# up		=	high_price - open_price
# down	=	open_price - low_price


# up%		=	up / gap
# down%	=	down / gap

# if down / up < 5%:
# 	print( 'down / up < 5%' )

# if up% > 5%:
# 	print( 'up% / gap% > 5%')




# {'assetType': 'EQUITY', 'assetMainType': 'EQUITY', 'cusip': '16936R105', 'symbol': 'CAAS', 'description': 'China Automotive Systems, Inc. - 
# Common Stock', 'bidPrice': 8.37, 'bidSize': 800, 'bidId': 'Q', 'askPrice': 8.4, 'askSize': 400, 'askId': 'P', 'lastPrice': 8.37, 'lastSize': 0, 'lastId': 'Q', 'openPrice': 12.51, 'highPrice': 13.6938, 'lowPrice': 8.22, 'bidTick': ' ', 'closePrice': 10.5, 'netChange': -2.13, 'totalVolume': 45621895, 'quoteTimeInLong': 1606870771527, 'tradeTimeInLong': 1606870796698, 'mark': 8.68, 'exchange': 'q', 'exchangeName': 'NASD', 'marginable': True, 'shortable': True, 'volatility': 0.1437, 'digits': 4, '52WkHigh': 13.6938, '52WkLow': 1.425, 'nAV': 0.0, 'peRatio': 0.0, 'divAmount': 0.0, 'divYield': 0.0, 'divDate': '', 'securityStatus': 'Normal', 'regularMarketLastPrice': 8.68, 'regularMarketLastSize': 270, 'regularMarketNetChange': -1.82, 'regularMarketTradeTimeInLong': 1606856400783, 'netPercentChangeInDouble': -20.2857, 'markChangeInDouble': -1.82, 'markPercentChangeInDouble': -17.3333, 'regularMarketPercentChangeInDouble': -17.3333, 'delayed': True}
