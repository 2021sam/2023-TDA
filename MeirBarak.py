import datetime
import requests
from Class.Gap import Gap
gap = Gap()

print( 'Meir Barak')
print ( gap.movers )

from Class.Quote import Quote


stock = {}
stock = { 'open': 0, 'low': 0, 'high': 0, 'close': 0 }

		# for i in movers:
		# 	close = i['last'] / ( 1 + i['change'] )     #   Change is a negative
		# 	# print( i['symbol'], close, i['last'], i['change'] )
		# 	print( '{:4} {:6} {:6} {:.1f}%'.format( i['symbol'], close, i['last'], i['change'] * 100 ))


# symbol	= gap.movers[0]['symbol']

# quote = Quote( symbol )
# print( 'Test' )
# print( quote.quote )

# low_price	= quote.quote['lowPrice']
# high_price	= quote.quote['highPrice']
# totalVolume = quote.quote['totalVolume']

# print( low_price, high_price, totalVolume )





	week = ['Monday', 'Teusday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	d = datetime.datetime.today().weekday()
	h = datetime.datetime.now().hour
	m = datetime.datetime.now().minute
	s = datetime.datetime.now().second
			# print( 'd = {}'.format( d ) )
	hm	= [h, m]
	hms = [h, m, s]
			# print('hm {}'.format(hm))

	start_time = [6,30]
	if start_time == hm:
		if stock['open'] == 0:
			stock['open'] = 



		if time_revised:
			alarm_set = False

def toDecimalTime( time ):
	h, m = map(int, time.split(':'))
	return ( h, h + float(m) / 60 )[ bool( m )  ]


def toListTime( time ):
	h, m = map(int, time.split(':'))
	return [h, m]

















while True:
	for i in gap.movers[:5]:
		symbol	= i['symbol']
		quote = Quote( symbol )
		# print( quote.quote )
		low_price	= quote.quote['lowPrice']
		high_price	= quote.quote['highPrice']
		totalVolume = quote.quote['totalVolume']
		print( low_price, high_price, totalVolume )


		# gap		=	yesterday_close - open_price
		up		=	high_price - open_price
		down	=	open_price - low_price


		# up%		=	up / gap
		# down%	=	down / gap

		# if down / up < 5%:
		# 	print( 'down / up < 5%' )

		# if up% > 5%:
		# 	print( 'up% / gap% > 5%')





