import pandas as pd
import pandas_ta as ta 
from Treding_live_model.strategy import myStratygy as str
import numpy as np
df=pd.read_csv("C:\\Users\\dell\\Desktop\\مجلد جديد\\data\\5m\\BTCUSDT.csv")

df1 = df

Siganl = str().macd_str(df1)
Siganl.append(0)
df1.dropna(inplace=True) 
df1['siganl'] = Siganl
df1['ATR'] = ta.atr(df1.High, df1.Low, df1.Close, length=14)
df1['sma'] = ta.sma(df.Close,100)
import time
start = time.perf_counter() 
in_postion = False
Enter_D ,Exit_D, Enter ,T1,T2,Sl,TRD = [],[],[],[],[],[],[]
tR = 0
t =0 
tp = 0
SL = 0
buyprice = 0

for index , row in df.iterrows():
    if not in_postion and row.siganl == 1 :
        buyprice = row.Close
        tr = 2 * row.ATR
        tp = buyprice  + ((buyprice * 0.01)+tr)
        SL  = buyprice  -  ((buyprice * 0.01)+tr)
        Enter_D.append(row.Date)
        Enter.append(buyprice)
        T1.append(tp)
        #T2.append(tp+((buyprice * 0.02)+tr))
        Sl.append(SL)
        in_postion=True 
    if (row.Close >= tp or row.High>= tp ) and in_postion :
        #in_postion=False 
        #t += 1
        #tr= f'TP{t}' 
        tp =tp + (tp * 0.01)
        SL=tp  - (tp * 0.01)
    elif (row.Close <= SL or row.Low<= SL) and in_postion :
        
        TRD.append(SL)
        Exit_D.append(row.Date)
        in_postion=False
if len(Enter) !=len(TRD):
    TRD.append(0)
    Exit_D.append(0)
print(len(Enter),len(T1),len(Sl),len(TRD))

df= pd.DataFrame(Enter_D,columns=['ENTER_D'])        
df['Exit_D'],df['Enter'],df['T1'],df['SL'],df['TRD'] =Exit_D,Enter,T1,Sl,TRD 
df['Def'] = df.Enter -  df.TRD
df1 = df
# buy qty = amount / float(close)
# sell = res[6] * qty  الكمية في الهدف 
Cash ,CTraed = [],[]
#Cash2 ,CTraed2 = [],[]
Cash.append(100)
#Cash2.append(100)

for _,row in df1.iterrows():

    amount = round(Cash[-1] / 5,3)
    if amount >15:
        
        qty = amount / row.Enter
        CTraed.append((row.TRD * qty))
        Cash.append(Cash[-1]+(CTraed[-1] - amount))
        #CTraed2.append(-(row.Def * qty))
        
        #Cash2.append(Cash[-1]+(CTraed[-1]))
        
        
Cash.pop(0)

df['CTraed'],df['Cash'] =CTraed,Cash
#df['CTraed2'],df['Cash2'] =CTraed2,Cash2

print(df)
end = time.perf_counter()

print(f'finshed in {end -start}')
print()