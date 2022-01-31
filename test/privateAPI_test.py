import pybithumb

with open("../secret/bithumb.txt") as f:
    lines = f.readlines()
    key = lines[0].strip()
    secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(key, secret)

krw = bithumb.get_balance("BTC")[2]
orderbook = pybithumb.get_orderbook("BTC")

asks = orderbook['asks']
sell_price = asks[0]['price']
unit = krw/sell_price

# order = bithumb.buy_market_order("BTC", unit)

order = bithumb.buy_limit_order("BTC", 3000, 0.001)
print(order)

