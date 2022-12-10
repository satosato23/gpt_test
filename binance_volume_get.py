from binance.client import Client
import os
import time

api_key = os.environ["BINANCE_API"]
api_secret = os.environ["BINANCE_SECRET"]
client = Client(api_key, api_secret)


all_tickers = client.get_all_tickers()

for ticker in all_tickers:
    try:
        pair=client.get_ticker(symbol=ticker["symbol"])
        symbol=pair["symbol"]
        klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "1 hour ago UTC")
        one_hour_volume=float(pair["volume"])/24
        for kline in klines:
            ago_volume=kline[5]
        if one_hour_volume/float(ago_volume) *100 >50:
            print(symbol+" 24時間の出来高"+pair["volume"]+"１時間の出来高"+str(one_hour_volume),"1時間前の出来高"+str(ago_volume))
            
       
    except ZeroDivisionError:
        continue

