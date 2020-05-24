from nsepy import get_history
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

stockPrices=get_history(symbol="NIFTY", start=date(2015,1,1), end=date(2019,11,11),index=True)



records=len(stockPrices['Close'])

Open_longPos=0
Open_ShortPos=0

Price_record=[]
Position_Record=[]
Profit_Loss_Record=[]
sum_pl=[]


for i1 in range(1,records):
    if stockPrices['Close'][i1]>stockPrices['Close'][i1-1] and Open_longPos==0 and Open_ShortPos==0:
        Price_record.append(stockPrices['Close'][i1])
        Position_Record.append("Open_Long_Position")
        Profit_Loss_Record.append(0)
        sum_pl.append(sum(Profit_Loss_Record))
        Open_longPos=1
        
    elif stockPrices['Close'][i1]>=stockPrices['Close'][i1-1] and Open_longPos==1 and Open_ShortPos==0:
        Price_record.append(stockPrices['Close'][i1])
        Position_Record.append("Hold_Long_Position")
        pl_rec=stockPrices['Close'][i1]-stockPrices['Close'][i1-1]
        Profit_Loss_Record.append(pl_rec)
        sum_pl.append(sum(Profit_Loss_Record))
        Open_longPos=1        
        
        
    elif stockPrices['Close'][i1]<stockPrices['Close'][i1-1] and Open_longPos==1 and Open_ShortPos==0:
        Price_record.append(stockPrices['Close'][i1])
        Position_Record.append("Close_Long_Position")
        pl_rec=stockPrices['Close'][i1]-stockPrices['Close'][i1-1]
        Profit_Loss_Record.append(pl_rec)
        sum_pl.append(sum(Profit_Loss_Record))
        Open_longPos=0  
        
    
    elif stockPrices['Close'][i1]<stockPrices['Close'][i1-1] and Open_longPos==0 and Open_ShortPos==0 :
        Price_record.append(stockPrices['Close'][i1])
        Position_Record.append("Open_Short_Position")
        Profit_Loss_Record.append(0)
        sum_pl.append(sum(Profit_Loss_Record))
        Open_ShortPos=1
        
        
    elif stockPrices['Close'][i1]<=stockPrices['Close'][i1-1] and Open_longPos==0 and Open_ShortPos==1:
        Price_record.append(stockPrices['Close'][i1])
        Position_Record.append("Hold_Short_Position")
        pl_rec=stockPrices['Close'][i1-1]-stockPrices['Close'][i1]
        Profit_Loss_Record.append(pl_rec)
        sum_pl.append(sum(Profit_Loss_Record))
        Open_ShortPos=1  
        
    elif stockPrices['Close'][i1]>stockPrices['Close'][i1-1] and Open_longPos==0 and Open_ShortPos==1:
        Price_record.append(stockPrices['Close'][i1])
        Position_Record.append("Close_Short_Position")
        pl_rec=stockPrices['Close'][i1-1]-stockPrices['Close'][i1]
        Profit_Loss_Record.append(pl_rec)
        sum_pl.append(sum(Profit_Loss_Record))
        Open_ShortPos=0
        

df=pd.DataFrame({'Price_record':Price_record,'Position_Record':Position_Record,'Profit_Loss_Record':Profit_Loss_Record,"sum_pl":sum_pl})
plt.plot(sum_pl)
plt.show()
