import datetime
import time
import math
import pandas as pd
from time import gmtime, strftime
from tkinter import *

class Plot():
    wh = 600
    ww = 800
    screen_width = ww + 600
    m = 30                      # margin
    x_axis = 10
    y_axis = 75
    volume_height = 200
    win = Tk()
    canvas = None
    showCandles = 120


    def __init__(self):
        self.candles = {'timestamp': [], 'Date':[], 'Hour':[], 'Minute':[], 'Symbol': [], 'Open':[], 'High':[], 'Low':[], 'Close':[], 'Volume':[]}
        self.minute_last = 0
        self.quarter_last = 5           # Any number other than 0,1,2,3
        self.volume_last = 0
        self.df = {}
        self.minp  = 0
        self.maxp  = 0
        self.price_range = 0
        self.minp_axis = 0
        self.maxp_axis = 0
        self.minv =  0
        self.maxv =  1000   # Avoid division by zero
        Plot.canvas = Canvas(Plot.win, width = Plot.ww + self.wh, height = Plot.wh + 300, bg = 'white')


    def updateExtremes(self, plot):
        self.df = pd.DataFrame(data=plot.candles)

        # Ranges in $1 increments
#         self.minp  = math.floor(  min( self.df['Low'] ) )
#         self.maxp  = math.ceil(   max( self.df['High'] ) )


        # Ranges in 10 cent increments
        self.minp  = math.floor(  min( self.df['Low'] ) * 10 ) / 10 - .1
        self.maxp  = math.ceil(   max( self.df['High'] ) * 10 ) / 10 + .1
       
        self.price_range = self.maxp - self.minp
        self.maxv =  max( self.df['Volume'][:])
        assert self.maxv != 0

        if self.maxv > 10000:
            i = math.ceil( self.maxv / 50000 )
            self.maxv = 50000 * i


    def setupAxis(self):
        Plot.canvas.delete("all")
        Plot.canvas.create_line( Plot.y_axis, Plot.wh, Plot.y_axis, Plot.m,  fill="#476042")
        Plot.canvas.create_line( Plot.y_axis, Plot.wh, self.screen_width, Plot.wh, fill="green")

        #p = int( math.floor( self.minp ) )   # Previous
        p = self.minp
        #self.minp_axis = p    # Not being used
        pricei = self.price_range / 10

        for i in range(10):
            Plot.canvas.create_text(5, self.plot(p), anchor=W, font="Purisa", fill='blue', text = str(round(p, 2)) )    # Price levels
            Plot.canvas.create_line( Plot.y_axis - 5, self.plot(p), Plot.y_axis + 5, self.plot(p), fill="green")                    # Tick marks
            Plot.canvas.pack(fill=BOTH, expand=1)
            p += pricei

        pricei = int ( self.maxv / 4 )   # Dividing by 4 → volume less than minv
        p = pricei
        for i in range(4):
            Plot.canvas.create_text(5, self.plotv(p), anchor=W, font="Purisa", fill='blue', text = "{0:>6}".format(p) ) # Volume levels
            Plot.canvas.create_line( Plot.y_axis - 5, self.plotv(p), Plot.y_axis + 5, self.plotv(p), fill="green")                    # Tick marks
            Plot.canvas.pack(fill=BOTH, expand=1)
            p += pricei


    def refresh(self, plot ):
        if len( plot.candles['timestamp'] ) > Plot.showCandles:
            self.candles['timestamp'].pop( 0 )
            self.candles['Date'].pop( 0 )
            self.candles['Hour'].pop( 0 )
            self.candles['Minute'].pop( 0 )
            self.candles['Symbol'].pop( 0 )
            self.candles['Open'].pop( 0 )
            self.candles['Low'].pop( 0 )
            self.candles['High'].pop( 0 )
            self.candles['Close'].pop( 0 )
            self.candles['Volume'].pop( 0 )

        df = pd.DataFrame( data=plot.candles )
        barw = 10

        for i in range( len( df ) ):
            j = len( df ) - i - 1
            space_between_bars = 1
            x = Plot.y_axis + ( barw + space_between_bars ) * ( Plot.showCandles - i - 1)
            hour, minute, seconds = self.epochToTime( df['timestamp'][j] )

            if seconds < 10:
                Plot.canvas.create_text(x, Plot.wh + 30, anchor=W, font="Purisa", fill='blue', text=hour - 8)
                Plot.canvas.create_text(x, Plot.wh + 50, anchor=W, font="Purisa", fill='blue', text=minute )

            Plot.canvas.pack(fill=BOTH, expand=1)

            color = 'green'
            if df['Close'][j] < df['Open'][j]:
                color = 'red'

            Plot.canvas.create_rectangle(x + ( barw / 2) - 1, self.plot( df['Low'][j] ), x + ( barw /  2 ) + 1, self.plot( df['High'][j] ), fill=color)
            Plot.canvas.create_rectangle(x, self.plot( df['Open'][j] ), x + barw, self.plot( df['Close'][j] ), fill=color)
            Plot.canvas.create_rectangle(x, self.plotv(0), x + barw, self.plotv( df['Volume'][j] ), fill=color)
            Plot.canvas.update()

        x = Plot.y_axis + 15 * ( Plot.showCandles)
        # p = df['Close'][-1]
        p = df['Close'][ len( df ) - 1 ]
        Plot.canvas.create_text(5, self.plot(p), anchor=W, font="Purisa", fill='blue', text = str(round(p, 2)) ) # Price levels

    def normalize(self, x ):
        return (x - self.minp) / (self.maxp - self.minp)

    def plot(self, p ):
        return Plot.wh - (Plot.wh * self.normalize(p))

    def normalizev(self, x ):
        y = (x - self.minv) / (self.maxv - self.minv)
        if y > 1:
            y = 1
        assert y >= 0
        return y

    def plotv(self, p ):
        return int( Plot.wh + Plot.volume_height + 50 - (Plot.volume_height * self.normalizev(p)) )


    def insertPricePoint(self, timestamp, hour, minute, seconds, symbol, price, volume):
            lastPrice = price
            # Address case for 6:00 am where minute is 00.  May need to use hour
            #Get quarter:
            quarter = int(seconds / 15)

            #if minute != minute_last:
            if quarter != self.quarter_last:
                if self.candles['Volume']:
                    v = volume - self.volume_last
                    self.candles['Volume'][-1] = v  # To be more accurate with volume would require posting all posts & this post
                    self.volume_last = volume
                else:
                    self.volume_last = volume    # Lose volume for first instance.

                self.quarter_last = quarter

                t = int( timestamp / 1000 )
                date = datetime.datetime.fromtimestamp( t )

                self.candles['timestamp'].append( timestamp )        
                self.candles['Date'].append( date )
                self.candles['Hour'].append( hour )
                self.candles['Minute'].append( minute )
                self.candles['Symbol'].append( symbol )
                self.candles['Open'].append( lastPrice )
                self.candles['Low'].append( lastPrice )
                self.candles['High'].append( lastPrice )
                self.candles['Close'].append( lastPrice )
                self.candles['Volume'].append( 100 )  # Appending 0 → division by zero
            else:
                # In same candle
                if self.candles['Low'][-1] > lastPrice:
                    self.candles['Low'][-1] = lastPrice

                if self.candles['High'][-1] < lastPrice:
                    self.candles['High'][-1] = lastPrice

                self.candles['Close'][-1]    = lastPrice
                self.candles['Volume'][-1]  = volume - self.volume_last

    def epochToTime(self, epoch):
        epoch /= 1000                               # Convert to seconds
        hours            = epoch % 86400            # Modding by seconds in a day  → Seconds since midnight 
        minutes          = hours % (60 * 60)        # Modding by seconds in a hour → Seconds since last hour
        seconds          = int( minutes % 60 )             # Modding by seconds in a minute → Seconds since last minute 
        hour             = int( hours / 3600 )
        minute           = int( minutes / 60 )
        #print ( '{}:{}:{}'.format( hour, minute, seconds ) )   
        return hour, minute, seconds
