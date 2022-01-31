import pybithumb
import time
import datetime

with open("../secret/bithumb.txt") as f:
    lines = f.readlines()
    key = lines[0].strip()
    secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(key, secret)

def buy_crypto_currency(ticker, krw):
    orderbook = pybithumb.get_orderbook(ticker)
    print('orderbook: ', orderbook)
    sell_price = orderbook['asks'][0]['price']
    print('sell_price: ', sell_price)
    unit = krw/float(sell_price)
    print('unit: ', unit)

print(buy_crypto_currency("ETH", 5000))