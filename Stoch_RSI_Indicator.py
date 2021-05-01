from kiteconnect import KiteConnect
import pandas as pd
import datetime as dt
from collections import deque
import os
from datetime import datetime
from datetime import date

today = date.today()

d1 = today.strftime("%d-%m-%Y")

dir_path = os.path.dirname(os.path.realpath(__file__))
now = datetime.now()
current_time = now.strftime("%H-%M-%S")






signals_list=[]
signals_name=[]


token_list=[2952193,857857,2977281,1346049,345089,5215745,4268801,784129,2953217,4598529,408065,
348929,225537,2889473,779521,2815745,415745,341249,177665,81153,897537,794369,519937,424961,
1850625,140033,4267265,3465729,738561,2939649,1270529,315393,7458561,1510401,975873,895745,
3834113,492033,340481,1207553,2714625,60417,969473,884737,633601,3001089,356865,232961,134657,3861249
]


Symbol_dict={975873:'ZEEL',2889473:'UPL',884737:'TATAMOTORS',794369:'SHREECEM',4598529:'NESTLEIND',
2939649:'LT',1346049:'INDUSINDBK',340481:'HDFC',341249:'HDFCBANK',232961:'EICHERMOT',140033:'BRITANNIA',
4268801:'BAJAJFINSV',1510401:'AXISBANK',2952193:'ULTRACEMCO',895745:'TATASTEEL',779521:'SBIN',
633601:'ONGC',519937:'M&M',408065:'INFY',1270529:'ICICIBANK',345089:'HEROMOTOCO',1207553:'GAIL',
177665:'CIPLA',134657:'BPCL',969473:'WIPRO',897537:'TITAN',2953217:'TCS',738561:'RELIANCE',2977281:'NTPC',
492033:'KOTAKBANK',415745:'IOC',356865:'HINDUNILVR',1850625:'HCLTECH',225537:'DRREDDY',7458561:'INFRATEL',
81153:'BAJFINANCE',60417:'ASIANPAINT',784129:'VEDL',3465729:'TECHM',857857:'SUNPHARMA',3834113:'POWERGRID',
2815745:'MARUTI',3001089:'JSWSTEEL',424961:'ITC',348929:'HINDALCO',315393:'GRASIM',5215745:'COALINDIA',
2714625:'BHARTIARTL',4267265:'BAJAJ-AUTO',3861249:'ADANIPORTS',256265:'NIFTY 50'

}




api_key=open(dir_path +"\\Access Details\\" +"api_key.txt","r").read()
access_token=open(dir_path +"\\Access Details\\" +"access_token.txt","r").read()
kite=KiteConnect(api_key=api_key)
kite.set_access_token(access_token)


######################
######################


######################
######################


for token in token_list:
	try:
		data_Extract = pd.DataFrame(kite.historical_data(token,dt.date.today()-dt.timedelta(50), dt.datetime.now(),"day"))
		data_Extract1= data_Extract.set_index('date')
		Price_Data=data_Extract1['close']
		timestamp1=data_Extract1.index[-1]
		Price_Data_ext=Price_Data

		price_list1=[ i1 for i1 in Price_Data_ext[-34:]]
		price_change1= [price_list1[count1]-price_list1[count1-1] for count1 in range(1,len(price_list1))]
		postiveChange1=[ priceChange_per1 if priceChange_per1>0 else 0 for priceChange_per1 in price_change1]
		negativeChange1=[abs(priceChange_per1) if priceChange_per1<0 else 0 for priceChange_per1 in price_change1]


		avg_pos_gain=[]
		avg_pos_gain.append(sum(postiveChange1[0:14])/len(postiveChange1[0:14]))
		for gain_i in postiveChange1[-19:]:
			avg_gain1= ((avg_pos_gain[-1] * 13) + gain_i )/14 
			avg_pos_gain.append(avg_gain1)
				
		avg_pos_loss=[]	
		avg_pos_loss.append(sum(negativeChange1[0:14])/len(negativeChange1[0:14]))
		for loss_i in negativeChange1[-19:]:
			avg_loss1= ((avg_pos_loss[-1] * 13) + loss_i )/14 
			avg_pos_loss.append(avg_loss1)

		RS=[(avg_pos_gain [counter_RS] / avg_pos_loss[counter_RS]) for counter_RS in range(0,len(avg_pos_loss))]	
		RSI=[ (100 if avg_pos_loss[counter_RSI] == 0 else 100-(100/(1 + RS[counter_RSI]))) for counter_RSI in range(0,len(RS))]

		stochrsi_list=[]

		prevDay_srsi=RSI[-15:-1]
		prev_maxRSI=max(prevDay_srsi)
		prev_minRSI=min(prevDay_srsi)
		prev_srsi= (((RSI[-2]-prev_minRSI)/(prev_maxRSI-prev_minRSI)))*100
		stochrsi_list.append(prev_srsi)


		currDay_srsi=RSI[-14:]
		curr_maxRSI=max(currDay_srsi)
		curr_minRSI=min(currDay_srsi)
		curr_srsi= (((RSI[-1]-curr_minRSI)/(curr_maxRSI-curr_minRSI)))*100
		stochrsi_list.append(curr_srsi)


		MA20=sum([ i2 for i2 in Price_Data_ext[-20:]])/20
		MA10=sum([ i3 for i3 in Price_Data_ext[-10:]])/10
		if stochrsi_list[1] < 80 and stochrsi_list[0] > 80:
			signals_list.append(Symbol_dict.get(token))
			signals_name.append("DownBreakout")

		elif stochrsi_list[1] > 20 and stochrsi_list[0] < 20 :
			signals_list.append(Symbol_dict.get(token))
			signals_name.append("UpBreakout")






		stochrsi_list.clear()

	except: Exception
	pass



dff=pd.DataFrame({"Script":signals_list, "Signal":signals_name})
print(dff)








