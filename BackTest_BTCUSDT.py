
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv("BTCUSDT.csv")
#df =df.set_index('Date')

df = df[190000:]

import pandas_ta as ta
import numpy as np

# Parameters
overbought = 70
oversold = 30
rsi_period = 14
min_duration = 4
max_duration = 100
close = df.Close
# Calculate RSI


rsi = ta.rsi(pd.Series(close) , rsi_period)

# Check if RSI is overbought or oversold for the specified duration
longOverbought = np.sum(np.where(rsi[max_duration:] > overbought, 1, 0), axis=0, initial=0) >= min_duration
longOversold = np.sum(np.where(rsi[max_duration:] < oversold, 1, 0), axis=0, initial=0) >= min_duration and (close > df.Open)

# Generate signals
buySignal = np.logical_and(np.diff(np.where(rsi < oversold, 1, 0)) > 0, longOversold[:-1])
sellSignal = np.logical_and(np.diff(np.where(rsi > overbought, 1, 0)) > 0, longOverbought)

# Calculate RSI divergence
priceDelta = np.array(close[:-1]) - np.array(close[1:])
rsiDelta = np.array(rsi[:-1]) - np.array(rsi[1:])
divergence = priceDelta * rsiDelta < 0

strongBuySignal = np.logical_and(buySignal[:-1], divergence[:-1])
strongSellSignal = np.logical_and(sellSignal[:-1], divergence[:-1])
df = df[:-1]

#buySignal = list(buySignal)

ran =len(df)

import plotly.graph_objects as go
fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
'''fig.add_scatter(x=df.index[strongBuySignal], y=df['Close'][strongBuySignal], mode="markers",
                marker=dict(size=5, color="green"),
                name="Signal")'''


fig.add_scatter(x=df.index[buySignal], y=df['Close'][buySignal]-100, mode="markers",
                marker= dict(size=10, color="MediumPurple"),
                name="Signal")

fig.show()



df

df['ATR'] =ta.atr(df.High, df.Low, df.Close, length=7)
from backtesting import Strategy
from backtesting import Backtest

class MyStrat(Strategy):
    overbought = 70
    oversold = 30
    rsi_period = 14
    min_duration = 4
    max_duration = 100
    def init(self):
        super().init()
        self.rsi = self.I(ta.rsi ,self.data.Close.s , rsi_period)


    def next(self):
        super().next()
        slatr = 0.02 * self.data.Close[-1]
        TPSLRatio = 0.06 * self.data.Close[-1]


        if np.sum(np.where(self.rsi[:] < oversold, 1, 0), axis=0, initial=0) >= min_duration and (self.data.Close[-1] > self.data.Open[-1]) and len(self.trades)==0:
            sl1 = self.data.Close[-1] - slatr
            tp1 = self.data.Close[-1] + TPSLRatio
            self.buy(sl=sl1, tp=tp1)

bt = Backtest(df, MyStrat, cash=1000000, commission=0.02)
stat = bt.run()
bt.plot()
stat

stat._trades

