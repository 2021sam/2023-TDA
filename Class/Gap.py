import requests
# from OAuth import OAuth
from Class.OAuth import OAuth
auth = OAuth()

class Gap:
	def __init__(self):
		# Get NASDAQ Movers
		endpoint = 'https://api.tdameritrade.com/v1/marketdata/$COMPX/movers'
		headers = {'Authorization':'Bearer {}'.format(auth.tokens['access_token'])}
		params = {'direction': 'down', 'change': 'percent'}
		content = requests.get( url = endpoint, params = params, headers = headers )
		movers_COMPX = content.json()

		# Get DJI Movers
		endpoint = 'https://api.tdameritrade.com/v1/marketdata/$DJI/movers'
		headers = {'Authorization':'Bearer {}'.format(auth.tokens['access_token'])}
		params = {'direction': 'down', 'change': 'percent'}
		content = requests.get( url = endpoint, params = params, headers = headers )
		movers_DJI = content.json()

		# Get SPX Movers
		endpoint = 'https://api.tdameritrade.com/v1/marketdata/$SPX.X/movers'
		headers = {'Authorization':'Bearer {}'.format(auth.tokens['access_token'])}
		params = {'direction': 'down', 'change': 'percent'}
		content = requests.get( url = endpoint, params = params, headers = headers )
		movers_SPX = content.json()
		print('COMPX')
		print( movers_COMPX )
		print('')

		print('DJI')
		print( movers_DJI )
		print('')

		print('SPX')
		print( movers_SPX )
		print('')

		movers = movers_COMPX + movers_DJI + movers_SPX
		# movers.extend( movers_DJI )
		# movers.extend( movers_SPX )
		print( 'movers')
		print( movers )
		print('')

		sorted(movers, key = lambda i: movers[0]['change'])
		print( 'movers' )
		for i in movers:
			print( i )


		print( '\nmovers' )
		for i in movers:
			close = i['last'] / ( 1 + i['change'] )     #   Change is a negative
			# print( i['symbol'], close, i['last'], i['change'] )
			print( '{:4} {:6} {:6} {:.1f}%'.format( i['symbol'], close, i['last'], i['change'] * 100 ))

		self.movers = movers