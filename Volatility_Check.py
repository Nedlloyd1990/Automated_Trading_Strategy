from nsepy import get_history
from datetime import date
import math
import numpy as np
import pandas as pd

Script_list=['ZEEL','YESBANK','WIPRO','VEDL','UPL','ULTRACEMCO','TITAN','TECHM','TCS','TATASTEEL','TATAMOTORS','SUNPHARMA','SBIN','RELIANCE','POWERGRID','ONGC','NTPC','NESTLEIND','MARUTI','M&M','LT','KOTAKBANK','JSWSTEEL','ITC','IOC','INFY','INFRATEL','INDUSINDBK','ICICIBANK','HINDUNILVR','HINDALCO','HEROMOTOCO','HDFCBANK','HCLTECH','GRASIM','GAIL','EICHERMOT','DRREDDY','COALINDIA','CIPLA','BRITANNIA','BPCL','BHARTIARTL','BAJFINANCE','BAJAJFINSV','BAJAJ-AUTO','AXISBANK','ASIANPAINT','ADANIPORTS']

record=[]
for script_name in Script_list:
    stockPrices=get_history(symbol=script_name, start=date(2019,1,1), end=date(2019,11,11))
    no_days=len(stockPrices)
    filtered_stockPrices=stockPrices[['Open','High','Low','Close']]
    filtered_stockPrices['Close T-1']=stockPrices['Close'].shift(1)
    filtered_stockPrices['returns']=(filtered_stockPrices['Close']-filtered_stockPrices['Close T-1'])/filtered_stockPrices['Close T-1']
    filtered_stockPrices.dropna()

    annual_volatility=(np.std(filtered_stockPrices['returns']))* math.sqrt(no_days)
    convt_toPer=(script_name + " :  "  +"{:.3%}".format(annual_volatility))
    #print(convt_toPer)
    record.append(convt_toPer)
    format_record=pd.DataFrame({"List":record})
    