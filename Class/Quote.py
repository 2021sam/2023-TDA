import requests
from credentials import client_id, username, password, redirect_uri

class Quote:
	def __init__(self, symbol):
		endpoint = 'https://api.tdameritrade.com/v1/marketdata/' + symbol + '/quotes'
		# headers = {'Authorization':'Bearer {}'.format(auth.tokens['access_token'])}
		params = {'apikey': client_id}
		# content = requests.get( url = endpoint, params = params, headers = headers )
		content = requests.get( url = endpoint, params = params )
		quote = content.json()

		# print( quote[symbol] )
		# for i in quote[symbol]:
		# 	print( f'{i}: { quote[symbol][i] }' )

		self.quote = quote[symbol]
		# print( quote['SPY']['closePrice'] )
		# low_price = quote['SPY']['lowPrice']
		# high_price = quote['SPY']['highPrice']
		# print( quote['SPY']['totalVolume'])
