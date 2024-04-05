import pandas as pd
import pandas_ta as ta 
from Treding_live_model.strategy import myStratygy as st
import numpy as np
from maxdown import maxDown
from falter_result import reding,Seving
from datetime import timedelta



class BACKTESTING():
    def  __init__(self,data,treling: int = 1 ,symbol: str='CASH'):
        self.df = data
        self.__n_sl = treling
        self.symbol =symbol
        self.in_postion = [False,False,False]
        self.tp1 =False
        self.Enter_D ,self.Exit_D, self.Enter ,self.T1,self.T2,self.Sl,self.TRD = {},{},{},{},{},{},{}
        self.tp2= [0,0,0,0,0,0,0]
        self.tR = 0
        self.trel = [0,0,0]
        self.tp = [0,0,0,0]
        self.Slose = [0,0,0]
        self.buyprice = [0,0,0,0]
        
        self.Result = []
        self.Cash ,self.CTraed = [100],[]        
    def MTread(self,index,row,SL,T1,TR):# Asign = اعزيز
      
        
      
        if not self.in_postion[0] and ((self.df.loc[index-1,"Close"] < row.S1 and row.Close >row.S1) or  (row.Open <row.S1 and row.Close > row.S1) ) : 
            
            #self.tp2 = [row["S1"],row["S2"],row["S3"]]

            self.buy(index,row,1,SL)
        
            
                 
        elif not self.in_postion[1] and ((self.df.loc[index-1,"Close"] < row.S2 and row.Close >row.S2) or (row.Open <row.S2 and row.Close > row.S2)) :    
            self.buy(index,row,2,SL)
        
        elif not self.in_postion[2] and ((self.df.loc[index-1,"Close"] < row.S3 and row.Close > row.S3) or  (row.Open < row.S3 and row.Close > row.S3)) :
            self.buy(index,row,3,SL)
            
    
        elif TR :
            for i in range(1,3):
                self.treling(index,row,i)          
                self.sell(index,row,i)
        else:
            _=0
    def sell(self,index,row,livel,tp1: bool=True):
        if (row.Close <= self.Slose[livel-1] or row.Low <= self.Slose[livel-1]) and self.in_postion[livel-1]: 
            self.tp1 =tp1 # IF you want ues 2 target when  teak profet 1 mack tp1 = True and teak profet 1 mack tp1 = flase 
            self.in_postion[livel-1]=False
            if   f"S{livel}" not in  self.Exit_D.keys():
                
                self.TRD[f"S{livel}"] =[]
                self.Exit_D[f"S{livel}"] =[]

            self.TRD[f"S{livel}"].append(self.Slose[livel-1])
            self.Exit_D[f"S{livel}"].append(index)         
        elif self.in_postion[livel-1] and  False and((row.Close >= self.tp[livel-1])  or row.High >= self.tp[livel-1]) :
            
            self.in_postion[livel-1]=False
            if   f"S{livel}" not in  self.Exit_D.keys():
                
                self.TRD[f"S{livel}"] =[]
                self.Exit_D[f"S{livel}"] =[]

            self.TRD[f"S{livel}"].append(self.tp[livel-1])
            self.Exit_D[f"S{livel}"].append(index)   


    def buy(self,index,row,livel,SL,TR: bool=True):
        self.in_postion[livel-1]=True
        self.buyprice[livel-1] =  row.Close
        
        self.tp[livel-1]  = (row[f"S{livel}"] - (row[f"S{livel}"] *SL)  )#  row[f"R{livel}"]
        self.Slose[livel-1]  = (row[f"S{livel}"] - (row[f"S{livel}"] *SL))
        
        if  f"S{livel}" not in self.Enter_D.keys(): 
            self.Enter_D[f"S{livel}"] = [] 
            self.Enter[f"S{livel}"]= []
            self.T1[f"S{livel}"]= [ ]
            self.T2[f"S{livel}"]= [ ]
            self.Sl[f"S{livel}"]= []
        
        self.Enter_D[f"S{livel}"].append(index) 
        self.Enter[f"S{livel}"].append(self.buyprice[livel-1])
        self.T1[f"S{livel}"].append(self.tp[livel-1])
        self.T2[f"S{livel}"].append(0 if TR else self.tp+((self.tp * self.tp1))) #الكود لم يكتمل 
        self.Sl[f"S{livel}"].append(self.Slose[livel-1])
    def treling(self,index,row , livel):
        
        if self.in_postion[livel-1] :
                
                #self.Slose[livel-1] = min( self.Slose[livel-1],row.Close + (self.__n_sl * 0.03  )*row.Close )
                self.Slose[livel-1]=max(self.Slose[livel-1] , row.Close - (self.__n_sl * 0.02) * row.Close)
        #else:
               
         
                

        
        #elif (row.Close >= self.tp2[2] or row.High>= self.tp2[2] ) and (self.in_postion[livel-1] and self.in_postion[2]) : 
        #        #self.tp[livel-1]   =self.tp[livel-1] +(self.tp2[1] - self.tp2[0]) 
        #        self.Slose[livel-1]= self.tp2[0] #self.Slose[livel-1] + (self.tp2[1] - self.tp2[0]) 



    def start(self,T1,SL,TR: bool=False):
        for index , row in self.df.iterrows():
            if index < 2 :
                continue
            self.MTread(index,row,SL,T1,TR)           
        for keys in self.Enter.keys():
            if   keys not in  self.TRD.keys():
                self.TRD[keys] = [0]
                self.Exit_D[keys]= [0]
            if len(self.Enter[keys]) !=len(self.TRD[keys]):
                self.TRD[keys].append(0)
                self.Exit_D[keys].append(0)
        self.Seving()  
    
    def Seving(self):
        #keys = []
        #dectionary_df = {}
        for key in  self.Enter_D.keys():
            
            df1= pd.DataFrame(None,columns=[f'ENTER_D_{key}'])
            df1[f'ENTER_D_{key}']   ,df1[f'Exit_D_{key}']            =self.Enter_D[key],self.Exit_D[key]
            df1[f'Enter_{key}']     ,df1[f'T1_{key}'],df1[f'T2_{key}'] =self.Enter[key],self.T1[key],self.T2[key]
            df1[f'SL_{key}']        ,df1[f'TRD_{key}']                 =self.Sl[key],self.TRD[key] 
            #dectionary_df[key] =df1
            
            df1.to_csv(f'result/T{self.symbol}_{key}.csv')
        self.TCalculatoin()
    def Calculation(self,Enter,TRD,retail: int = 5):      
        amount = round(int(self.Cash[-1]) / retail,3)
        if amount >2:
            qty = amount / Enter
            CTrae=TRD * qty
            Cass= self.Cash[-1]+(CTrae - amount)
            self.Cash.append(Cass -(amount*0.002) ) 
        return CTrae , Cass
    def TCalculatoin(self):
        
      
        for key in self.Enter_D.keys():    
            df= pd.read_csv(f'result/T{self.symbol}_{key}.csv')
            if df[f"TRD_{key}"].tail(1).values == 0.:
                df = df[:-2]   
            Cas =  list(map(self.Calculation,df[f"Enter_{key}"],df[f"TRD_{key}"])) 

            df[f'CTraed{key}'],df[f'Cash{key}'] =[i[0] for i in Cas],[i[1] for i in Cas]
            df.to_csv(f'result/T{self.symbol}_{key}.csv',index=False)
            
            self.Result =df
            maxdC=maxDown(self.Result[f"Cash{key}"])
            print(self.Result[f"Cash{key}"].tail(1))
import os
import time
fi = os.listdir('data/1d')
fi = [i[:-4] for i in fi]


li = []
cast = []
tiker = []
fi = fi[0:]


if __name__ == '__main__':
    
    #resul = reding('ALL_RESULT.csv')
    
    for symbol in fi:
        #tp=0.05
        AinG = 2


     
        
        start = time.perf_counter() 
        
        
        tp =AinG * 0.02    
        sl = AinG*0.01
        
        
        
        df=pd.read_csv(f"C:\\Users\\dell\\Desktop\\مجلد جديد\\data\\5m\\{symbol}.csv",index_col=0)
        #hourly_data=pd.read_csv(f"C:\\Users\\dell\\Desktop\\مجلد جديد\\data\\1H\\{symbol}.csv",index_col=0)

        
        box = 1000
        df1 = df
        yp=[]
        levels  = st().support_resistance_levels_volumeP(data=df1,lookback= box, first_w=1.0, atr_mult=3.0)

        

        for i in range(box,len(levels),1000):   
            if i >len(levels)-1:
                continue
            matrix = [[0]*5]*len(levels)    
            LE = yp.append([df.Date[i],levels[i][0],levels[i][1],levels[i][2],levels[i][3]]) if len(levels[i]) >= 4 else yp.append([df.Date[i],levels[i][0],levels[i][1],levels[i][2],None]) if  len(levels[i]) ==3 else yp.append([df.Date[i],levels[i][0],levels[i][1],None,None])  if len(levels[i]) ==2 else yp.append([df.Date[i],levels[i][0],None,None,None])    

        cdf = pd.DataFrame(yp,columns=["Date","S1","S2","S3","S4"])
        df1 = df    
        cdf.replace(0, np.nan)
        cdf1 =cdf
        df1["Date"] = pd.to_datetime(df1["Date"], unit= "ms")
        df1 = df1.set_index("Date")
        cdf1["Date"] = pd.to_datetime(cdf1["Date"], unit= "ms")
        cdf1= cdf1.set_index("Date")
        df =pd.merge_asof(df1,cdf1, left_index=True , right_index=True)
        
        df["num"] = [i for i in range(len(df))]
        df = df.set_index("num")
        #df1 = df1[:7]
        #hourly_data[:500]
        #Siganl.append(0)
        #ITS.append(0)
        #df1['siganl'] = Siganl
        #df1['ITS'] = ITS
        df1.dropna(inplace=True) 
        back = BACKTESTING(data=df,treling=AinG,symbol=symbol)        
        back.start(T1=tp,SL=sl,TR=True)
          
        
        
        
        #maxdC=maxDown(back.Result.Cash)
        #winCH = back.Result.tail(1).Cash.values[-1]
        #
        #valuse = [symbol,tp,sl ,maxdC[0],maxdC[1],winCH]
        #df_ = reding('FINAL_RESULT1.csv')
        ##df_ = pd.DataFrame(None,columns=)
        #df_.append(valuse)
        #Seving('FINAL_RESULT1.csv',df_,columns=['symbol','TP','SL','%maxDown','$maxDown','%win'])
        #end =start = time.perf_counter()
        #print(f'finshed in {end -start}')