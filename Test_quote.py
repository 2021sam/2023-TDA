from Class.Quote import Quote

quote = Quote('SPY')
print( 'Test' )
print( quote.quote )

low_price	= quote.quote['lowPrice']
high_price	= quote.quote['highPrice']
totalVolume = quote.quote['totalVolume']

print( low_price, high_price, totalVolume )