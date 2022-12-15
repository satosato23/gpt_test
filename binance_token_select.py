from binance.client import Client
import os
import time
import json
import math
import slackweb

from dotenv import load_dotenv
from os.path import join, dirname

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


slack_url=os.environ["SLACK_URL"]
api_key = os.environ.get("BINANCE_API")
api_secret = os.environ.get("BINANCE_SECRET")
client = Client(api_key, api_secret)

all_tickers = client.get_all_tickers()

def btc_and_eth(symbol):
    day_ago_klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY,"2 day ago UTC","1 day ago UTC")
    #week_klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, "1 week ago UTC")
    pair=client.get_ticker(symbol=symbol)
    for kline in day_ago_klines:
        ago_volume=kline[5]
       
    volume_persent=float(pair["volume"])/float(ago_volume) *100
    volume_persent=round(volume_persent,2)
    ago_volume=round(float(ago_volume),2)
    volume=round(float(pair["volume"]),2)
    #print(float(pair["volume"]),float(ago_volume),volume_persent)
    klines_14 = client.get_klines(
                    symbol=symbol,
                    interval=Client.KLINE_INTERVAL_1HOUR,
                    limit=25
                )

                # Calculate the RSI
    gain_sum = 0
    loss_sum = 0
    for i in range(1, len(klines_14)):
        change = float(klines_14[i][4]) - float(klines_14[i-1][4])
        if change > 0:
            gain_sum += change
        else:
            loss_sum += abs(change)

    RS = gain_sum / loss_sum
    RSI = 100 - (100 / (1 + RS))
    
    attachments = [
                    {
                        "color": "#ff0000",
                        "text":"symbol: "+symbol+"\n"
                        +"RSI (20 or 80 periods): "+ str(math.floor(RSI))+"\n"
                        +"24h volume: "+str(volume)+"\n"
                        +"1day Ago:"+str(ago_volume)+"\n"
                        +"volume%:"+str(volume_persent)
                    }
                    ]
    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
    slack.notify(

        username="volumeBot",

        attachments=attachments)
    
    
    
def main():
    btc_and_eth("BTCUSDT")
    for ticker in all_tickers:

        try:
            pair=client.get_ticker(symbol=ticker["symbol"])
            symbol=pair["symbol"]
            
            day_ago_klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY,"2 day ago UTC","1 day ago UTC")
            
            
            for kline in day_ago_klines:
                ago_volume=kline[5]
            
            volume_persent=float(pair["volume"])/float(ago_volume) *100
            volume_persent=round(volume_persent,2)
            ago_volume=round(float(ago_volume),2)
            volume=round(float(pair["volume"]),2)
            #print(float(pair["volume"]),float(ago_volume),volume_persent)
            time.sleep(0.3)
            
            if volume_persent >110:
                
                klines_14 = client.get_klines(
                    symbol=symbol,
                    interval=Client.KLINE_INTERVAL_1HOUR,
                    limit=25
                )

                # Calculate the RSI
                gain_sum = 0
                loss_sum = 0
                for i in range(1, len(klines_14)):
                    change = float(klines_14[i][4]) - float(klines_14[i-1][4])
                    if change > 0:
                        gain_sum += change
                    else:
                        loss_sum += abs(change)

                RS = gain_sum / loss_sum
                RSI = 100 - (100 / (1 + RS))

                # Print the RSI
                if 20 >RSI or RSI>80:
                    
                    attachments = [
                    {
                        "color": "#000080",
                        "text":"symbol: "+symbol+"\n"
                        +"RSI (20 or 80 periods): "+ str(math.floor(RSI))+"\n"
                        +"24h volume: "+str(volume)+"\n"
                        +"1day Ago:"+str(ago_volume)+"\n"
                        +"volume%:"+str(volume_persent)
                    }
                    ]
                    slack = slackweb.Slack(url=slack_url)
                    slack.notify(

                        username="volumeBot",

                        attachments=attachments)
                    
            
        except ZeroDivisionError:
            continue
            

main()