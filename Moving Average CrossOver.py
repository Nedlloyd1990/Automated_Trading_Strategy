from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import pandas as pd
import datetime as dt
import os 
from datetime import datetime
from datetime import date
import logging
import time
import xlwings as xw


long_pos=0
short_pos=0



dir_path=os.path.normpath(os.getcwd() + os.sep + os.pardir)
dir_path2=os.path.dirname(os.path.realpath(__file__))



api_key=open(dir_path2 +"\\Access Details\\" +"api_key.txt","r").read()
access_token=open(dir_path2 +"\\Access Details\\" +"access_token.txt","r").read()
kite=KiteConnect(api_key=api_key)
kite.set_access_token(access_token)




data_Extract = pd.DataFrame(kite.historical_data(5633,dt.date.today()-dt.timedelta(3), dt.datetime.now(),"minute"))
# data_Extract1= data_Extract.set_index('date')
Current_MA5=sum(data_Extract['close'][-6:-1])/5
Current_MA50=sum(data_Extract['close'][-51:-1])/50



if long_pos==0 and short_pos==0:
	if Current_MA5>Current_MA50:
		bookbuy_order(tk_name)
		print(str(tk_name)  + " | " + "Open Long Position" + " | " +  "Current price- " +  str(data_Extract1['close'][-1]))
		long_pos=1

	if Current_MA5<Current_MA50:
		booksell_order(tk_name)
		print(str(tk_name)  + " | " + "Open Short Position" + " | " +  "Current price- " +  str(data_Extract1['close'][-1]))
		short_pos=1

else:
	if Current_MA5>Current_MA50 and long_pos==0 and short_pos==1:
		short_pos=0
		bookbuy_order(tk_name)
		print(str(tk_name)  + " | " + "Close Short Position" + " | " +  "Current price- " +  str(data_Extract1['close'][-1]))
		long_pos=1
		bookbuy_order(tk_name)
		print(str(tk_name)  + " | " + "Open Long Position" + " | " +  "Current price- " +  str(data_Extract1['close'][-1]))



	elif Current_MA5<Current_MA50 and long_pos==1 and short_pos==0:
		long_pos=0
		booksell_order(tk_name)
		print(str(tk_name)  + " | " + "Close Long Position" + " | " +  "Current price- " +  str(data_Extract1['close'][-1]))		
		short_pos=1
		booksell_order(tk_name)
		print(str(tk_name)  + " | " + "Open Short Position" + " | " +  "Current price- " +  str(data_Extract1['close'][-1]))				