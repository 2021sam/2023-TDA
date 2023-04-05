import requests
from credentials import client_id, username, password, redirect_uri
from OAuth import OAuth

auth = OAuth()

# Get Quote
# <Response [200]> → Success
endpoint = 'https://api.tdameritrade.com/v1/marketdata/SPY/pricehistory'
headers = {'Authorization':'Bearer {}'.format(auth.tokens['access_token'])}
params = {
			'apikey': client_id,
			'periodType': 'month',
			'period': 1,
			'frequencyType': 'daily',
			'frequency': 1			
}
content = requests.get( url = endpoint, params = params, headers = headers )
quote	= content.json()

print( quote['candles'] )
d = quote['candles']

for i in d:
	print( f'{i}' )

yesterday_close = d[-1]['close']
print( yesterday_close )



# [{'open': 339.76, 'high': 340.12, 'low': 337.99, 'close': 338.22, 'volume': 65994108, 'datetime': 1603774800000}, {'open': 332.1, 'high': 338.2483, 'low': 326.13, 'close': 326.66, 'volume': 127094307, 'datetime': 1603861200000}, {'open': 326.91, 'high': 333.395, 'low': 325.09, 'close': 329.98, 'volume': 90597689, 'datetime': 1603947600000}, {'open': 328.28, 'high': 329.69, 'low': 322.6, 'close': 326.54, 'volume': 120448685, 'datetime': 1604034000000}, {'open': 330.2, 'high': 332.36, 'low': 327.24, 'close': 330.2, 'volume': 86068299, 'datetime': 1604296800000}, {'open': 333.69, 'high': 338.25, 'low': 330.2935, 'close': 336.03, 'volume': 93294192, 'datetime': 1604383200000}, {'open': 340.86, 'high': 347.94, 'low': 339.59, 'close': 343.54, 'volume': 126959700, 'datetime': 1604469600000}, {'open': 349.24, 'high': 352.19, 'low': 348.86, 'close': 350.24, 'volume': 82039749, 'datetime': 1604556000000}, {'open': 349.93, 'high': 351.51, 'low': 347.65, 'close': 350.16, 'volume': 74972973, 'datetime': 1604642400000}, {'open': 363.97, 'high': 364.38, 'low': 354.06, 'close': 354.56, 'volume': 172304203, 'datetime': 
# 1604901600000}, {'open': 353.49, 'high': 355.18, 'low': 350.51, 'close': 354.04, 'volume': 85552022, 'datetime': 1604988000000}, {'open': 356.4, 'high': 357.56, 'low': 355.06, 'close': 356.67, 'volume': 58649048, 'datetime': 1605074400000}, {'open': 355.58, 'high': 356.7182, 'low': 351.26, 'close': 353.21, 'volume': 68118563, 'datetime': 1605160800000}, {'open': 355.27, 'high': 358.9, 'low': 354.71, 'close': 358.1, 'volume': 62959429, 'datetime': 1605247200000}, {'open': 360.98, 'high': 362.78, 'low': 359.59, 'close': 362.57, 'volume': 74541138, 'datetime': 1605506400000}, {'open': 359.97, 'high': 361.92, 'low': 358.34, 'close': 360.62, 'volume': 66111009, 'datetime': 1605592800000}, {'open': 360.91, 'high': 361.5, 'low': 356.24, 'close': 356.28, 'volume': 70591299, 'datetime': 1605679200000}, {'open': 355.6, 'high': 358.18, 'low': 354.15, 'close': 357.78, 'volume': 59940947, 'datetime': 1605765600000}, {'open': 357.5, 'high': 357.72, 'low': 355.25, 'close': 355.33, 'volume': 70411890, 'datetime': 1605852000000}, {'open': 357.28, 'high': 358.82, 'low': 354.865, 'close': 357.46, 'volume': 63230608, 'datetime': 1606111200000}, {'open': 360.21, 'high': 363.81, 'low': 359.29, 'close': 363.22, 'volume': 62415877, 'datetime': 1606197600000}, {'open': 363.13, 'high': 363.16, 'low': 361.48, 'close': 362.66, 'volume': 45330890, 'datetime': 1606284000000}, {'open': 363.84, 'high': 364.18, 'low': 362.58, 'close': 363.67, 'volume': 28514072, 'datetime': 1606456800000}]
# {'open': 339.76, 'high': 340.12, 'low': 337.99, 'close': 338.22, 'volume': 65994108, 'datetime': 1603774800000}
# {'open': 332.1, 'high': 338.2483, 'low': 326.13, 'close': 326.66, 'volume': 127094307, 'datetime': 1603861200000}
# {'open': 326.91, 'high': 333.395, 'low': 325.09, 'close': 329.98, 'volume': 90597689, 'datetime': 1603947600000}
# {'open': 328.28, 'high': 329.69, 'low': 322.6, 'close': 326.54, 'volume': 120448685, 'datetime': 1604034000000}
# {'open': 330.2, 'high': 332.36, 'low': 327.24, 'close': 330.2, 'volume': 86068299, 'datetime': 1604296800000}
# {'open': 333.69, 'high': 338.25, 'low': 330.2935, 'close': 336.03, 'volume': 93294192, 'datetime': 1604383200000}
# {'open': 340.86, 'high': 347.94, 'low': 339.59, 'close': 343.54, 'volume': 126959700, 'datetime': 1604469600000}
# {'open': 349.24, 'high': 352.19, 'low': 348.86, 'close': 350.24, 'volume': 82039749, 'datetime': 1604556000000}
# {'open': 349.93, 'high': 351.51, 'low': 347.65, 'close': 350.16, 'volume': 74972973, 'datetime': 1604642400000}
# {'open': 363.97, 'high': 364.38, 'low': 354.06, 'close': 354.56, 'volume': 172304203, 'datetime': 1604901600000}
# {'open': 353.49, 'high': 355.18, 'low': 350.51, 'close': 354.04, 'volume': 85552022, 'datetime': 1604988000000}
# {'open': 356.4, 'high': 357.56, 'low': 355.06, 'close': 356.67, 'volume': 58649048, 'datetime': 1605074400000}
# {'open': 355.58, 'high': 356.7182, 'low': 351.26, 'close': 353.21, 'volume': 68118563, 'datetime': 1605160800000}
# {'open': 355.27, 'high': 358.9, 'low': 354.71, 'close': 358.1, 'volume': 62959429, 'datetime': 1605247200000}
# {'open': 360.98, 'high': 362.78, 'low': 359.59, 'close': 362.57, 'volume': 74541138, 'datetime': 1605506400000}
# {'open': 359.97, 'high': 361.92, 'low': 358.34, 'close': 360.62, 'volume': 66111009, 'datetime': 1605592800000}
# {'open': 360.91, 'high': 361.5, 'low': 356.24, 'close': 356.28, 'volume': 70591299, 'datetime': 1605679200000}
# {'open': 355.6, 'high': 358.18, 'low': 354.15, 'close': 357.78, 'volume': 59940947, 'datetime': 1605765600000}
# {'open': 357.5, 'high': 357.72, 'low': 355.25, 'close': 355.33, 'volume': 70411890, 'datetime': 1605852000000}
# {'open': 357.28, 'high': 358.82, 'low': 354.865, 'close': 357.46, 'volume': 63230608, 'datetime': 1606111200000}
# {'open': 360.21, 'high': 363.81, 'low': 359.29, 'close': 363.22, 'volume': 62415877, 'datetime': 1606197600000}
# {'open': 363.13, 'high': 363.16, 'low': 361.48, 'close': 362.66, 'volume': 45330890, 'datetime': 1606284000000}
# {'open': 363.84, 'high': 364.18, 'low': 362.58, 'close': 363.67, 'volume': 28514072, 'datetime': 1606456800000}
# 363.67

# (base) C:\Z\Python\TDA\OAuth>