	week = ['Monday', 'Teusday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	d = datetime.datetime.today().weekday()
	h = datetime.datetime.now().hour
	m = datetime.datetime.now().minute
	s = datetime.datetime.now().second
			# print( 'd = {}'.format( d ) )
	hm = [h, m]
			# print('hm {}'.format(hm))


	if start_time <= hm and end_time > hm:
		if time_revised:
			alarm_set = False

def toDecimalTime( time ):
	h, m = map(int, time.split(':'))
	return ( h, h + float(m) / 60 )[ bool( m )  ]


def toListTime( time ):
	h, m = map(int, time.split(':'))
	return [h, m]


