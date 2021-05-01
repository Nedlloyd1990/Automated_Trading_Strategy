from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import pandas as pd
import datetime as dt
import os 
from datetime import datetime
from datetime import date
import logging
import time


longpos_count=0
shortpos_count=0

dir_path2=os.path.dirname(os.path.realpath(__file__))



api_key=open(dir_path2 +"\\Access Details\\" +"api_key.txt","r").read()
access_token=open(dir_path2 +"\\Access Details\\" +"access_token.txt","r").read()
kite=KiteConnect(api_key=api_key)
kite.set_access_token(access_token)


while True:
	now = datetime.now()
	current_time = str(now.strftime("%H-%M-%S"))
	data_Extract_raw1 = pd.DataFrame(kite.historical_data(738561,dt.date.today()-dt.timedelta(200), dt.datetime.now(),"day"))
	data_Extract1= data_Extract_raw1.set_index('date')

	#data_Extract1.to_csv("bla.csv")


	priceBand1=[data_Extract1['close'][-counterprice] for counterprice in range(100,0,-1) ]


	ATR=[(sum([max(data_Extract1['high'][-count] - data_Extract1['low'][-count], \
		abs(data_Extract1['high'][-count] - data_Extract1['close'][-(count+1)]), \
		abs(data_Extract1['low'][-count] - data_Extract1['close'][-(count+1)])) \
		for count in range(counterprime,counterprime-7,-1)])/7) \
		for counterprime in range(100,6,-1)]



	upperBandATR= [(((data_Extract1['high'][-countup] + data_Extract1['low'][-countup])/2)+ (3 * ATR[-countup])) for countup in range(50,0,-1)]
	lowerBandATR= [(((data_Extract1['high'][-countdown] + data_Extract1['low'][-countdown])/2)- (3 * ATR[-countdown])) for countdown in range(50,0,-1)]

	priceBand2=priceBand1[-50:]
	ATR2=ATR[-50:]
	upperBandATR2=upperBandATR[-50:]
	lowerBandATR2=lowerBandATR[-50:]


	upperband=[0]
	for i1 in range(0,50):
		if upperBandATR[i1] < upperband[-1] or priceBand2[i1-1] > upperband[-1]:
			upperband.append(upperBandATR[i1])
		else:
			upperband.append(upperband[-1])


	lowerband=[0]
	for i2 in range(0,50):
		if lowerBandATR2[i2] > lowerband[-1] or priceBand2[i2-1] < lowerband[-1]:
			lowerband.append(lowerBandATR2[i2])
		else:
			lowerband.append(lowerband[-1])
			

	upperband2=upperband[-50:]	
	lowerband2=lowerband[-50:]	

	upperband2[0]=0
	lowerband2[0]=0

	supertrend=[0]
	for i3 in range(1,50):
		if (supertrend[-1]==upperband2[i3-1]) and (priceBand2[i3] <= upperband2[i3]):
			supertrend.append(upperband2[i3])
		elif (supertrend[-1]==upperband2[i3-1]) and (priceBand2[i3] >= upperband2[i3]):
			supertrend.append(lowerband2[i3])

		elif (supertrend[-1]==lowerband2[i3-1]) and (priceBand2[i3] >= lowerband2[i3]):
			supertrend.append(lowerband2[i3])
		elif (supertrend[-1]==upperband2[i3-1]) and (priceBand2[i3] <= lowerband2[i3]):
			supertrend.append(upperband2[i3])




	#df1=pd.DataFrame({'Price':priceBand2, 'ATR':ATR2, 'upperBandATR':upperBandATR2, 'lowerBandATR':lowerBandATR2, 'UpperBand':upperband2, 'LowerBand':lowerband2,'SuperTrend':supertrend })




	if ((data_Extract1['open'][-2]> supertrend[-2]) and (data_Extract1['open'][-3]< supertrend[-3]) and \
		(data_Extract1['close'][-3]> supertrend[-3]) and (data_Extract1['close'][-3] < supertrend[-3]) and\
		longpos_count ==0 and shortpos_count ==1):
		print(str(current_time) + " | " + "Close_Short" + " | " + "SuperTrend Value: " + str(supertrend[-1]))
		print(str(current_time) + " | " + "Open_Long" + " | " + "SuperTrend Value: " + str(supertrend[-1]))
		shortpos_count=0
		longpos_count=1

	elif ((data_Extract1['open'][-2]< supertrend[-2]) and (data_Extract1['open'][-3]> supertrend[-3]) and \
		(data_Extract1['close'][-3]< supertrend[-3]) and (data_Extract1['close'][-3] > supertrend[-3])and\
		longpos_count ==1 and shortpos_count ==0):
		print(str(current_time) + " | " + "Close_Long" + " | " + "SuperTrend Value: " + str(supertrend[-1]))
		print(str(current_time) + " | " + "Open_Short" + " | " + "SuperTrend Value: " + str(supertrend[-1]))
		shortpos_count=1
		longpos_count=0




	elif ((data_Extract1['open'][-2]> supertrend[-2]) and (data_Extract1['open'][-3]< supertrend[-3]) and \
		(data_Extract1['close'][-3]> supertrend[-3]) and (data_Extract1['close'][-3] < supertrend[-3]) and\
		longpos_count ==0 and shortpos_count ==0):
		print(str(current_time) + " | " + "Open_Long" + " | " + "SuperTrend Value: " + str(supertrend[-1]))
		shortpos_count=0
		longpos_count=1

	elif ((data_Extract1['open'][-2]< supertrend[-2]) and (data_Extract1['open'][-3]> supertrend[-3]) and \
		(data_Extract1['close'][-3]< supertrend[-3]) and (data_Extract1['close'][-3] > supertrend[-3])and\
		longpos_count ==0 and shortpos_count ==0):
		print(str(current_time) + " | " + "Open_Short" + " | " + "SuperTrend Value: " + str(supertrend[-1]))
		shortpos_count=1
		longpos_count=0


	else:
		print(str(current_time) + " | " + "no Trade" + " | " + "SuperTrend Value: " + str(supertrend[-1]))















