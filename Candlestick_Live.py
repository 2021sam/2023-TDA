import time
from Class.ReadSQL import ReadSQL
client = ReadSQL()
client.database_connect()
from Class.Plot import Plot
plot = Plot()
symbol = 'SPY'

def epochToTime(epoch):
    epoch /= 1000                               # Convert to seconds
    hours            = epoch % 86400            # Modding by seconds in a day  → Seconds since midnight 
    minutes          = hours % (60 * 60)        # Modding by seconds in a hour → Seconds since last hour
    seconds          = int( minutes % 60 )      # Modding by seconds in a minute → Seconds since last minute 
    hour             = int( hours / 3600 )
    minute           = int( minutes / 60 )
    #print ( '{}:{}:{}'.format( hour, minute, seconds ) )   
    return hour, minute, seconds


id = 0
while True:
	top = client.database_live()
    if row['id'] == id:
        continue

    # print( '{} [{}]'.format( id, row['Symbol']) )
    id = row['id']

    if symbol in row['Symbol']:
        # print('.', end='')
        hour_GMT, minute, second = epochToTime(row['timestamp'])
        hour = hour_GMT - 8 # PST
        print( row['timestamp'], row['Symbol'], hour_GMT, hour, minute, second )

        if hour < 6:
            continue

        if hour == 6 and minute < 30:
            continue

        time.sleep(.1)

        if hour > 12:
            continue

        plot.insertPricePoint( row['timestamp'], hour, minute, second, row['Symbol'], row['LastPrice'], row['TotalVolume'] )
        plot.updateExtremes( plot )
        plot.setupAxis()
        plot.refresh( plot )
        time.sleep(.5)


plot.win.mainloop()               # Canvas will crash with out this line.
print('Done !')