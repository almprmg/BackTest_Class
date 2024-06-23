
import pandas as pd
import pandas_ta as ta
import numpy as np
import matplotlib.pyplot as plt
from numba import jit , prange
 
@jit()

def runa(name):
    
        
    df= pd.read_csv(name)
    df['Date'] = pd.to_datetime(df["Date"])
    df =df.set_index('Date')
    
    df
    
    def sum1(source, length):
        series = pd.Series(source)
        return series.rolling(length).sum().values
    
    # Parameters
    overbought = 70
    oversold = 30
    rsi_period = 14
    min_duration = 4
    max_duration = 100
    close = df.Close
    # Calculate RSI
    
    
    rsi = ta.rsi(pd.Series(close) , rsi_period)
    sma = ta.sma(close , 200)
    # Check if RSI is overbought or oversold for the specified duration
    longOverbought = np.sum(np.where(rsi[max_duration:] > overbought, 1, 0), axis=0, initial=0) >= min_duration
    
    #longOversold = sum(np.where(rsi < oversold, 1, 0),max_duration) >= min_duration and (close > df.Open)
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
    def SIGNAL():
      return buySignal
    
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
    
    from backtesting import Strategy
    from backtesting import Backtest
    #from backtesting.lib import TrailingStrategy
    Le = 8640
    class TrailingStrategy(Strategy):
        """
        A strategy with automatic trailing stop-loss, trailing the current
        price at distance of some multiple of average true range (ATR). Call
        `TrailingStrategy.set_trailing_sl()` to set said multiple
        (`6` by default). See [tutorials] for usage examples.
        [tutorials]: index.html#tutorials
        Remember to call `super().init()` and `super().next()` in your
        overridden methods.
        """
        __n_sl = 2.
    
    
        def init(self):
            super().init()
    
    
    
        def set_trailing_sl(self, __n_sl : float = 1):
          self.__n_sl = __n_sl
    
        def next(self):
            super().next()
            # Can't use index=-1 because self.__atr is not an Indicator type
            index = len(self.data)-1
            for trade in self.trades:
                if trade.is_long:
                    trade.sl = max(trade.sl or -np.inf, self.data.Close[index] - (self.__n_sl * 0.01) * self.data.Close[index])
                else:
                   trade.sl = min(trade.sl or np.inf,
                                   self.data.Close[index] + (self.__n_sl * 0.01 / 2 )*self.data.Close[index] )
    
    
    
    class MyStrat(TrailingStrategy):
        initsize = 0.99
        mysize = initsize
        Sr = 1
        Tr = 4
        t = 1
        le = 8640
    
        def init(self):
            super().init()
            self.signal1 = self.I(SIGNAL)
            self.sma = self.I(ta.sma,self.data.Close.s,200)
            super().set_trailing_sl(self.Tr)
    
        def next(self):
            super().next()
    
            slatr =  (self.Sr * 0.01 )*self.data.Close[-1]
            TPSLRatio = (self.t * 0.01) *self.data.Close[-1]
            if (self.signal1==1 and self.data.Close[-1] > self.sma[-1]) and len(self.trades)==0:
            #if (self.signal1==1) and len(self.trades)==0:
                sl1 = self.data.Close[-1] - slatr
                tp1 = self.data.Close[-1] + TPSLRatio
                self.buy(sl=sl1, tp=tp1 ,size= self.mysize)
    
    bt = Backtest(df, MyStrat, cash=100000, commission=0.001)
    stat = bt.run()
    #bt.plot()
    #stat
    
    stat._trades
    
    
    stats = bt.optimize(Sr= range(1,11,1),Tr= range(1,20,1) ,t= range(1,20,1) , maximize='Equity Final [$]',constraint=lambda param: param.Sr < param.t)
    
    
    # print(stats)
    # print(stats._strategy)
    return stats
