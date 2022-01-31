import time
import pybithumb
import datetime
import requests

TICKER = "ETC"
MIN_KRW = 1000
MIN_UNIT = 0.033
FEE = 0.9975
K = 0.7

with open("../secret/bithumb.txt") as f:
    lines = f.readlines()
    key = lines[0].strip()
    secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(key, secret)

def get_target_price(ticker, k):
    """변동성 돌파 전략 - 매수 목표가 조회"""

    df = pybithumb.get_ohlcv(ticker)
    df = df.tail(2)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * k
    return target

def get_yesterday_ma15(ticker):
    """15일 이동 평균선 조회"""

    df = pybithumb.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(15).mean()
    return ma[-2]

def get_current_price(ticker):
    """현재가 조회"""
    return bithumb.get_current_price(ticker)

def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2]*FEE
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    unit = krw/float(sell_price)
    bithumb.buy_market_order(ticker, unit)

def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]*FEE
    bithumb.sell_market_order(ticker, unit)

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
ma15 = get_yesterday_ma15(TICKER)
target_price = get_target_price(TICKER, k=K)

while True:
    try:
        now = datetime.datetime.now()

        if mid < now < mid + datetime.timedelta(seconds=10):
            target_price = get_target_price(TICKER, k=K)
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            ma15 = get_yesterday_ma15(TICKER)
            unit = bithumb.get_balance(TICKER)[2]
            if unit > MIN_UNIT:
                sell_crypto_currency(TICKER)

        current_price = pybithumb.get_current_price(TICKER)
        if (current_price > target_price) and (current_price > ma15):
            krw = bithumb.get_balance(TICKER)[2]
            if krw > MIN_KRW:
                buy_crypto_currency(TICKER)
    except:
        print("에러 발생")
    time.sleep(1)