import pandas as pd
import pandas_ta as ta 
from Treding_live_model.strategy import myStratygy as strR
import time
#import numpy as np
from maxdown import maxDown
from falter_result import reding,Seving
class BACKTESTING():
    def  __init__(self,data,TP,SL,ST_Asign: bool=False,Asign: float= 0.5,symbol: str='CASH'):
        self.df = data
        self.symbol =symbol
        self.in_postion = False
        self.SL,self.TP= SL,TP
        self.tp1 =False
        self.tp_A =True
        self.Enter_D ,self.Exit_D, self.Enter ,self.T1,self.T2,self.Sl,self.TRD,self.Enter_A,self.TS_A=[],[],[],[],[],[],[],[],[]
        self.num=0
        self.tR = 0
        self.tp = 0
        self.Slose = 0
        self.buyprice = 0
        self.ST_Asign =ST_Asign
        self.PAsign = 0 
        self.Asign = Asign
        self.Result = []
        self.Cash ,self.CTraed = [100],[]        
    def MTread(self,row,TR,Asign : bool = False):# Asign = اعزيز
        
        if not self.in_postion and row.siganl == 1 : 
            self.ST_Asign = Asign
            self.in_postion=True
            self.num=0
            self.buyprice = row.Close
            self.PAsign =  self.buyprice -(self.buyprice * (0.01*self.Asign))
            self.tr = 2 * 0#row.ATR
            self.tp = self.buyprice  + ((self.buyprice * self.TP)+self.tr)
            self.Slose  = self.buyprice  -  ((self.buyprice * self.SL)+self.tr)
            self.Enter_D.append(row.Date)
            self.Enter_A.append(self.PAsign)
            self.Enter.append(self.buyprice)
            self.T1.append(self.tp)
            self.T2.append(0 if TR else self.tp+((self.tp * self.TP)))
            #T2.append(tp+((buyprice * 0.02)+tr))
            self.Sl.append(self.Slose)       

        elif (row.Close >= self.tp or row.High>= self.tp ) and self.in_postion :
                if TR:
                    self.tp =self.tp + (self.tp * self.TP)
                    self.Slose=self.Slose  + (self.Slose * self.SL)
                elif not self.tp1:
                    self.tp =self.T2[-1]
                    self.Slose=self.Slose  + (self.Slose * self.SL)
                    self.tp1 =True
                    if not self.tp_A and self.num ==1 :
                        self.num +=1
                        self.TS_A.append(self.T1[-1])
                        self.tp_A = True
                    else:
                        self.TS_A.append(0)
                        
                else:
                    if len(self.Enter_A) != len(self.TS_A):
                        self.TS_A.append(0)       
                    self.Exit_D.append(row.Date)
                    self.TRD.append((self.tp + self.T1[-1])/2)
                    self.in_postion=False
                    self.tp1 =False
        elif (row.Close <= self.Slose or row.Low<= self.Slose) and self.in_postion : 
                self.tp1 =False
                self.in_postion=False
                if len(self.TS_A) != len(self.Enter_A) and not self.tp_A:
                        self.TS_A.append(self.Slose)
                self.TRD.append(self.Slose)
                self.Exit_D.append(row.Date)         
        if self.ST_Asign and self.in_postion :
            if self.tp_A and self.num==0 and (row.Close <= self.PAsign or row.Low<= self.PAsign) :
                self.num +=1
                self.tp_A = False

    def start(self,TR: bool=False,Asign: bool= False):
        for _ , row in self.df.iterrows():
            self.MTread(row,TR,Asign)           
        if len(self.Enter) !=len(self.TS_A):
            self.TS_A.append(0)
        if len(self.Enter) !=len(self.TRD):
            self.TRD.append(0)
            self.Exit_D.append(0)
            
        if len(self.Enter)-len(self.TS_A) > 0:
            df1= pd.DataFrame(self.Enter_D,columns=['ENTER_D'])        
            df1['Exit_D'],df1['Enter'],df1['T1'],df1['T2'],df1['SL'],df1['TRD']=self.Exit_D,self.Enter,self.T1,self.T2,self.Sl,self.TRD
            #print(i)
        #print(len(Enter),len(T1),len(Sl),len(TRD))
        else:
            df1= pd.DataFrame(self.Enter_D,columns=['ENTER_D'])        
            df1['Exit_D'],df1['Enter'],df1['T1'],df1['T2'],df1['SL'],df1['TRD'],df1['ENTER_A'],df1['TS_A'] =self.Exit_D,self.Enter,self.T1,self.T2,self.Sl,self.TRD,self.Enter_A,self.TS_A
            #df['Def'] = df.Enter -  df.TRD
        df1.to_csv(f'result/T{self.symbol}_{self.SL}_{self.TP}_{self.Asign}.csv',index=False)
        self.TCalculatoin()
        
    def Calculation(self,Enter,TRD,retail: int = 5):      
        amount = round(int(self.Cash[-1]) / retail,3)
        if amount >2:
            qty = amount / Enter
            CTrae = TRD * qty
            Cass= self.Cash[-1]+(CTrae - amount) if TRD >0 else self.Cash[-1]
            self.Cash.append(Cass)
            return CTrae , Cass
    def TCalculatoin(self):
        df= pd.read_csv(f'result/T{self.symbol}_{self.SL}_{self.TP}_{self.Asign}.csv',index_col=0)
        if df.TRD.tail(1).values == 0.:
            df = df[:-2]    
            
        Cas =  list(map(self.Calculation,df.Enter,df.TRD)) 
        if len(self.Enter)-len(self.TS_A) > 0:
            df['CTraed'],df['Cash']=[i[0] for i in Cas],[i[1] for i in Cas]
        else:
            self.Cash.pop()
            self.Cash.append(100)
            Aing =  map(self.Calculation,df.ENTER_A,df.TS_A)
            df['CTraed'],df['Cash'],df['Cash_A'] =[i[0] for i in Cas],[i[1] for i in Cas],[i[1] for i in list(Aing)] 
        df.to_csv(f'result/T{self.symbol}_{self.SL}_{self.TP}_{self.Asign}.csv',index=False)
        self.Result =df
import os
fi = os.listdir('data/5m')
fi = [i[:-4] for i in fi]


li = []
cast = []
tiker = []
fi = fi[0:]
a=0
if __name__ == '__main__':
    resul = reding('ALL_RESULT.csv')
    
    for x in resul[0:]:
        #tp=0.05
        AinG = 1
        num=1
        print(a)
        for i in range(2,len(x),2):
            start = time.perf_counter() 
            AinG+=1
            #print(f'chash : {x[i-1]}',f'chash_a : {x[i]}')
            if AinG ==10 and num!=2:
               #tp=0.
               AinG = 1
               num+=1
              
            #print('sl',sl,'tp',tp)
            
                
            symbol = x[0]
            
            
            tp =AinG * 0.01    
            sl = AinG*0.01
            ain = AinG-1
            
            
            df=pd.read_csv(f"C:\\Users\\dell\\Desktop\\مجلد جديد\\data\\5m\\{symbol}.csv")
            df1 = df
            Siganl = strR().macd_str(df1)
            Siganl.append(0)
            df1.dropna(inplace=True) 
            df1['siganl'] = Siganl
            df1['ATR'] = ta.atr(df1.High, df1.Low, df1.Close, length=14)
            df1['sma'] = ta.sma(df.Close,100) 
            back = BACKTESTING(data=df1,Asign=ain,TP=tp,SL=sl,symbol=symbol)        
            back.start(TR=True,Asign=True)
              
            
            
            if (x[i] >0 and x[i] != None) and (x[i-1] >0 and x[i-1] != None):
                try:
                    maxdC=maxDown(back.Result.Cash)        
                    maxd=maxDown(back.Result.Cash_A)
                    winCH = back.Result.tail(1).Cash.values[-1]
                    winA = back.Result.tail(1).Cash_A.values[-1]
                    valuse = [symbol,tp,sl ,ain ,maxd[0],maxd[1],maxdC[0],maxdC[1],winCH,winA]
                except AttributeError:
                    pass

            else:
                maxdC=maxDown(back.Result.Cash)
                winCH = back.Result.tail(1).Cash.values[-1]
                maxd = ['0','0']
                winA = '0'
                valuse = [symbol,tp,sl ,ain ,maxd[0],maxd[1],maxdC[0],maxdC[1],winCH,winA]
            df_ = reding('FINAL_RESULT.csv')
            #df_ = pd.DataFrame(None,columns=)
            df_.append(valuse)
            Seving('FINAL_RESULT.csv',df_,columns=['symbol','TP','SL','Aingn','%maxDownCH','$maxDownCH','%maxDownA','$maxDownA','%winCH','%winA'])
            end =start = time.perf_counter()
            print(f'finshed in {end -start}')