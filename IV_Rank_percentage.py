################################################
#################################################
################################################
#####################################################
# find IV Rank
################################################
#################################################
################################################
#####################################################



from datetime import date
import math
import numpy as np
import pandas as pd

Stdv_count=52

Script_list=os.listdir(r"C:\Users\DELL\Desktop\Market Analysis\Old\NSEData")

record_name=[]
ivRank_rec=[]

for script_name in Script_list:
    stockPrices=pd.read_csv(r"C:\Users\DELL\Desktop\Market Analysis\Old\NSEData\\" +  script_name)

    no_days=len(stockPrices)
    slicer_count=no_days-52

    filtered_stockPrices=stockPrices[['Close']]
    filtered_stockPrices['Close T-1']=stockPrices['Close'].shift(1)
    filtered_stockPrices['returns']=(filtered_stockPrices['Close']-filtered_stockPrices['Close T-1'])/filtered_stockPrices['Close T-1']
    filtered_stockPrices['stdv']=filtered_stockPrices['returns'].rolling(Stdv_count).std()
    Slice_data=filtered_stockPrices[slicer_count:]
    Slice_data
    latest_stdv=Slice_data['stdv'].tail(1)
    high=np.max(Slice_data['stdv'])
    low=np.min(Slice_data['stdv'])
    IV_Rank=float(100*(latest_stdv-low)/(high-low))
    record_name.append(script_name)
    ivRank_rec.append(IV_Rank)
    Get_allRanks=pd.DataFrame({"Script Name": record_name, "IV Rank Percentage":ivRank_rec})
Get_allRanks
    