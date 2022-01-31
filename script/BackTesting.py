import pybithumb
import numpy as np

df = pybithumb.get_ohlcv("ETC")
df = df.tail(n=365)

df['ma15'] = df['close'].rolling(window=15).mean().shift(1)
df['range'] = (df['high'] - df['low']) * 0.7
df['target'] = df['open'] + df['range'].shift(1)
df['bull'] = df['open'] > df['ma15']

fee = 0.0032
df['ror'] = np.where((df['high'] > df['target']) & df['bull'],
                      df['close'] / df['target'] - fee,
                      1)

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD: ", df['dd'].max())
print("HPR: ", df['hpr'][-2])
df.to_excel("../data/larry_ma.xlsx")