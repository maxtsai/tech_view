#! /usr/bin/env python


import sys
import string
import datetime
from yahoo import *


COST_RATE = 0.002
FAX_RATE = 0.003
READY_BUY = 3
READY_SELL = 2
ACCEPT_LOSS = 0.2

def ma_normal_rule(stock, start_day, end_day, ma):
	print stock
	ma_key = "MA" + str(ma)
	signal_key = "signal"
	operation_key = "operation"
	yf = yahoo()
	result = yf.ma(stock, start_day, end_day, ma)
	if result == "":
		#print stock + " NORMAL: No data"
		return

	result.sort(key=lambda x:x[yf.DATE], reverse=False)
	bought = False
	buy_stop = READY_BUY
	sell_stop = READY_SELL

	price = 0.0
	for line in result:
		if (line[ma_key] != 0) and (string.atof(line[yf.ADJCLOSE]) > line[ma_key]) and (bought == False):
			buy_stop = buy_stop -1 
			if buy_stop == 0:
				line[signal_key] = "buy"
				bought = True
				price = string.atof(line[yf.HIGH])
				sell_stop = READY_SELL
			else:
				if bought == True:
					line[signal_key] = "keep"
				else:
					line[signal_key] = "none"
		elif (line[ma_key] != 0) and (string.atof(line[yf.ADJCLOSE]) < line[ma_key]) and (bought == True):
			sell_stop = sell_stop -1 
			if sell_stop == 0:
				line[signal_key] = "sell"
				bought = False
				buy_stop = READY_BUY
			else:
				if bought == True:
					line[signal_key] = "keep"
				else:
					line[signal_key] = "none"
		elif (bought == True) and ((string.atof(line[yf.CLOSE])-price) < 0 and (price - string.atof(line[yf.CLOSE])) > price*ACCEPT_LOSS):
			line[signal_key] = "sell"
			bought = False
		else:
			if bought == True:
				line[signal_key] = "keep"
			else:
				line[signal_key] = "none"

	bought = False
	profit = 0.0
	cost = 0.0
	price = 0.0
	count = 0

	# only can order off day	
	result[0][operation_key] = "none"
	for i in range(result.__len__()):
		if (i+1) >= result.__len__():
			break
		if (bought == False) and (result[i][signal_key] == "buy"):
			result[i+1][operation_key] = "buy"
			bought = True
			price = string.atof(result[i+1][yf.HIGH])
			count += 1 
			cost += string.atof(result[i+1][yf.HIGH]) * 1000 * COST_RATE
		elif (bought == True) and (result[i][signal_key] == "sell"):
			result[i+1][operation_key] = "sell"
			bought = False
			profit += (string.atof(result[i+1][yf.HIGH]) - price) * 1000
			cost += string.atof(result[i+1][yf.HIGH]) * 1000 * (COST_RATE + FAX_RATE)
		else:
			if bought == True:
				result[i+1][operation_key] = "keep"
			else:
				result[i+1][operation_key] = "none"



	result.sort(key=lambda x:x[yf.DATE], reverse=True)

	#f = open("data/." + stock + "." + str(ma) + ".normal", "w")
	f = open(".normal", "w")
	f.write("DATE\t\tOPEN\tCLOSE\tHIGH\tLOW\tVOLUME\t" + ma_key + "\tSIGNAL\tOPERATION\n")
	for line in result:
		f.write(str(line[yf.DATE]))
		f.write("\t")
		f.write(str(line[yf.OPEN]))
		f.write("\t")
		f.write(str(line[yf.CLOSE]))
		f.write("\t")
		f.write(str(line[yf.HIGH]))
		f.write("\t")
		f.write(str(line[yf.LOW]))
		f.write("\t")
		f.write(str(line[yf.VOLUME]/1000))
		f.write("\t")
		f.write(str(line[ma_key]))
		f.write("\t")
		f.write(str(line[signal_key]))
		f.write("\t")
		f.write(str(line[operation_key]))
		f.write("\n")
	f.close()

	if bought == True:
		print stock + " kept,\tNORMAL:\tprice = " + str(result[0][yf.HIGH]) + " (" + result[0][yf.DATE] + "),\tresult = " + str(profit - cost) + ",\tprofit = " + str(profit) + ",\tcost = " + str(cost) + ",\tcount = " + str(count) + ",\tROI= " + str((profit-cost)/string.atof(result[0][yf.HIGH]))
	else:
		print stock + " empty,\tNORMAL:\tprice = " + str(result[0][yf.HIGH]) + " (" + result[0][yf.DATE] + "),\tresult = " + str(profit - cost) + ",\tprofit = " + str(profit) + ",\tcost = " + str(cost) + ",\tcount = " + str(count) + ",\tROI= " + str((profit-cost)/string.atof(result[0][yf.HIGH]))



def ma_short_sell_rule(stock, start_day, end_day, ma):
	ma_key = "MA" + str(ma)
	signal_key = "signal"
	operation_key = "operation"
	yf = yahoo()
	result = yf.ma(stock, start_day, end_day, ma)
	if result == "":
		#print stock + " SHORT: No data"
		return

	result.sort(key=lambda x:x[yf.DATE], reverse=False)
	bought = False
	buy_stop = READY_BUY
	sell_stop = READY_SELL

	price = 0.0
	for line in result:
		if (line[ma_key] != 0) and (string.atof(line[yf.ADJCLOSE]) > line[ma_key]) and (bought == True):
			buy_stop = buy_stop -1
			if buy_stop == 0:
				line[signal_key] = "short-cover"
				bought = False
				sell_stop = READY_SELL
			else:
				if bought == True:
					line[signal_key] = "keep"
				else:
					line[signal_key] = "none"
		elif (line[ma_key] != 0) and (string.atof(line[yf.ADJCLOSE]) < line[ma_key]) and (bought == False):
			sell_stop = sell_stop -1
			if sell_stop == 0:
				line[signal_key] = "short-sell"
				bought = True
				price = string.atof(line[yf.LOW])
				buy_stop = READY_BUY
			else:
				if bought == True:
					line[signal_key] = "keep"
				else:
					line[signal_key] = "none"
		elif (bought == True) and ((string.atof(line[yf.ADJCLOSE]) - price) > 0 and (string.atof(line[yf.ADJCLOSE]) - price) > price * ACCEPT_LOSS):
			bought = False
			line[signal_key] = "short-cover"
		else:
			if bought == True:
				line[signal_key] = "keep"
			else:
				line[signal_key] = "none"

	bought = False
	profit = 0.0
	cost = 0.0
	price = 0.0
	count = 0

	result[0][operation_key] = "none"

	for i in range(result.__len__()):
		if (i+1) >= result.__len__():
			break
		if (bought == False) and (result[i][signal_key] == "short-sell"):
			result[i+1][operation_key] = "short-sell"
			bought = True
			price = string.atof(result[i+1][yf.LOW])
			count += 1 
			cost += string.atof(result[i+1][yf.LOW]) * 1000 * COST_RATE
		elif (bought == True) and (result[i][signal_key] == "short-cover"):
			result[i+1][operation_key] = "short-cover"
			bought = False
			profit += (price - string.atof(result[i+1][yf.LOW])) * 1000
			cost += string.atof(result[i+1][yf.LOW]) * 1000 * (COST_RATE + FAX_RATE)
		else:
			if bought == True:
				result[i+1][operation_key] = "keep"
			else:
				result[i+1][operation_key] = "none"

	result.sort(key=lambda x:x[yf.DATE], reverse=True)

	#f = open("data/." + stock + "." + str(ma) + ".short", "w")
	f = open(".short", "w")
	f.write("DATE\t\tOPEN\tCLOSE\tHIGH\tLOW\tVOLUME\t" + ma_key + "\tSIGNAL\t\tOPERATION\n")
	for line in result:
		f.write(str(line[yf.DATE]))
		f.write("\t")
		f.write(str(line[yf.OPEN]))
		f.write("\t")
		f.write(str(line[yf.CLOSE]))
		f.write("\t")
		f.write(str(line[yf.HIGH]))
		f.write("\t")
		f.write(str(line[yf.LOW]))
		f.write("\t")
		f.write(str(line[yf.VOLUME]/1000))
		f.write("\t")
		f.write(str(line[ma_key]))
		f.write("\t")
		f.write(str(line[signal_key]))
		f.write("\t\t")
		f.write(str(line[operation_key]))
		f.write("\n")
	f.close()

	if bought == True:
		print stock + " kept,\tSHORT:\tprice = " + str(result[0][yf.LOW]) + " (" + result[0][yf.DATE] + "),\tresult = " + str(profit - cost) + ",\tprofit = " + str(profit) + ",\tcost = " + str(cost) + ",\tcount = " + str(count) + ",\tROI= " + str((profit-cost)/string.atof(result[0][yf.LOW]))
	else:
		print stock + " empty,\tSHORT:\tprice = " + str(result[0][yf.LOW]) + " (" + result[0][yf.DATE] + "),\tresult = " + str(profit - cost) + ",\tprofit = " + str(profit) + ",\tcost = " + str(cost) + ",\tcount = " + str(count) + ",\tROI= " + str((profit-cost)/string.atof(result[0][yf.LOW]))



if len(sys.argv) == 1:
	f = open("stock_list.txt", "r")
	for stock in f.readlines():
		stock = stock.strip("\n") + ".TW"
		# within 30 days
		from_day = datetime.datetime.now() - datetime.timedelta(30)
		ma_normal_rule(stock, datetime.datetime.strftime(from_day, "%Y/%m/%d"), datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d"), 5)
		ma_short_sell_rule(stock, datetime.datetime.strftime(from_day, "%Y/%m/%d"), datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d"), 5)
	f.close()
elif len(sys.argv) != 5:
	print "Usage:"
	print "(1)\t" + sys.argv[0]
	print "(2)\t" + sys.argv[0] + " stock from_day end_day ma"

else:
	ma_normal_rule(sys.argv[1] + ".TW", sys.argv[2], sys.argv[3], string.atoi(sys.argv[4]))
	ma_short_sell_rule(sys.argv[1] + ".TW", sys.argv[2], sys.argv[3], string.atoi(sys.argv[4]))


