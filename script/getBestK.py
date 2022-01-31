import pybithumb
import datetime
import numpy as np
import pandas

pandas.set_option('display.max_columns', None)

def get_ror(k=0.5, days=30):
    df = pybithumb.get_ohlcv("BTC")
    df = df.tail(days)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

ror = float()
k = float()
days = int()
for k in np.arange(0.1, 1.0, 0.1):
    for days in np.arange(2, 60, 1):
        new_ror = get_ror(k, days)
        if ror < new_ror:
            ror = round(new_ror, 6)
            k = round(k, 1)
            days = days

print('%f %d %f' % (k, days, ror))