import requests
from binance.client import Client
import os
# Set the API key and secret
api_key = os.environ["BINANCE_API"]
api_secret = os.environ["BINANCE_SECRET"]

# Initialize the Binance client
client = Client(api_key, api_secret)

# Set the symbol and the interval
symbol = "BTCUSDT"
interval = "1h"

# Get the current funding rate
funding_rate = client.futures_funding_rate(symbol=symbol, interval=interval)
print(funding_rate)
# Set the thresholds for buying and selling
buy_threshold = 0.001
sell_threshold = -0.001

# Check if the funding rate is above the buy threshold
if funding_rate > buy_threshold:
  # Calculate the quantity to buy
  # You can set this to a fixed amount or use a
  # formula to calculate the amount based on your
  # available balance and the current price
  quantity = ...

  # Send a buy order
  buy_order = client.order_market_buy(
    symbol=symbol,
    quantity=quantity
  )

# Check if the funding rate is below the sell threshold
if funding_rate < sell_threshold:
  # Calculate the quantity to sell
  # You can set this to a fixed amount or use a
  # formula to calculate the amount based on your
  # available balance and the current price
  quantity = ...

  # Send a sell order
  sell_order = client.order_market_sell(
    symbol=symbol,
    quantity=quantity
  )
