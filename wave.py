#! /usr/bin/env python

import sys
import string
import datetime
from linechart import *
from yahoo import *

def wave(stock, start_day, end_day, ma):
	ma_key = "MA" + str(ma)
	profit_key = "Profit"
	wave_key = "Wave"
	wave_peak_key = "WavePeak"

	y = yahoo()

	result = y.ma(stock, start_day, end_day, ma)
	if result == "":
		return ""

	for i in result:
		if string.atof(i[y.CLOSE]) < i[ma_key]:
			i[profit_key] = "-" 
		else:
			i[profit_key] = "+"

	result.sort(key=lambda x:x[y.DATE], reverse=False)
	sign = result[0][profit_key]

	for i in result:
		i[wave_peak_key] = ""
	si = 0
	ei = 0
	index = 0
	peak_id = 0
	for i in result:
		i[wave_key] = 0
		if sign != i[profit_key]:
			ei = index
		if sign != i[profit_key] and sign == "-":
			low = 10000
			for ii in range(si, ei):
				if string.atof(result[ii][y.LOW]) < low:
					low = string.atof(result[ii][y.LOW])
					peak_id = ii
			result[peak_id][wave_key] = string.atof(result[peak_id][y.LOW])
			result[peak_id][wave_peak_key] = "+"
			#print("peak_index = %d, price = %s" % (peak_id, result[peak_id][y.LOW]))
		elif sign != i[profit_key] and sign == "+":
			high = 0
			for ii in range(si, ei):
				if string.atof(result[ii][y.HIGH]) > high:
					high = string.atof(result[ii][y.HIGH])
					peak_id = ii
			result[peak_id][wave_key] = string.atof(result[peak_id][y.HIGH])
			result[peak_id][wave_peak_key] = "-"
			#print("peak_index = %d, price = %s" % (peak_id, result[peak_id][y.HIGH]))

		if sign != i[profit_key]:
			sign = i[profit_key]
			si = index
		index += 1

	ii = 0
	for i in result:
		if i[wave_key] != 0:
			break
		ii += 1

	rr = result
	result = []
	for i in range(ii, len(rr)):
		result.append(rr[i])


	count = 0
	ii = 0
	for i in result:
		i.pop(profit_key)
		if i[wave_key] == 0:
			count += 1
		elif i[wave_key] > 0 and count > 0:
			j = ii - count
			for r in range(j, ii):
				result[r][wave_key] = (result[ii][wave_key] - result[j-1][wave_key]) / (count+1) * (r - j + 1) + result[j-1][wave_key]
				#print "[" + str(r) + "]\t" + str(result[r][wave_key])
			count = 0
		ii += 1
	
	'''
	ii = 0
	for i in result:
		if i[wave_key] == 0:
			if ii-2 > 0:
				i[wave_key] = (result[ii-1][wave_key] - result[ii-2][wave_key]) + result[ii-1][wave_key]
			else:
				i[wave_key] = i[y.CLOSE]
		ii += 1
	'''
	rr = result
	result = []
	for i in rr:
		if i[wave_key] != 0:
			result.append(i)
	'''
	ii = 0
	for i in result:
		print str(ii) + "\t" + i[y.DATE] + "\t" + str(i[y.LOW]) + "\t" + str(i[y.HIGH]) + "\t" + str(i[y.CLOSE]) + "\t" + str(i[ma_key]) + "\t" + str(i[wave_key]) + "\t" + i[wave_peak_key]
		ii += 1
	'''
	return result

if __name__ == "__main__":
	#wave(sys.argv[1], sys.argv[2], sys.argv[3], string.atoi(sys.argv[4]))
	wave("2002.TW", "2011/6/25", "2012/6/25", 5)
