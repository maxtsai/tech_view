#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib
import string
import os
import datetime
import sys


PATH = "data/"

class yahoo:
	def __init__(self):
		self.quates_url = "http://finance.yahoo.com/d/quotes.csv?s="
		self.history_quates_url = "http://ichart.yahoo.com/table.csv?s="
		self.chart_url = "http://chart.finance.yahoo.com/z?"
		self.sector_url = "http://biz.yahoo.com/p/csv/"
		self.DATE = 'Date'
		self.OPEN = 'Open'
		self.HIGH = 'High'
		self.LOW = 'Low'
		self.CLOSE = 'Close'
		self.VOLUME = 'Volumn'
		self.ADJCLOSE = 'Adj Close'
		self.HISTORY_RECORD_NUM = 7
	def __check_time_format(self, day):
		d = day.split("/")
		if d.__len__() != 3: ## expect format like "2012/6/6" or "2012-6-6"
			d = day.split("-")
			if d.__len__() != 3:
				print "unacceptable time format: '" + day + "'"
				return ""
		return d
	def __format_record(self, r):
		data = {}
		data[self.DATE] = r[0]
		data[self.OPEN] = string.atof(r[1])
		data[self.HIGH] = string.atof(r[2])
		data[self.LOW] = string.atof(r[3])
		data[self.CLOSE] = string.atof(r[4])
		data[self.VOLUME] = string.atoi(r[5])/1000
		data[self.ADJCLOSE] = string.atof(r[6])
		return data
	def __request_history(self, symbol, s, e):
		s = self.__check_time_format(s)
		e = self.__check_time_format(e)
		url = self.history_quates_url + symbol + "&a=" + str(string.atoi(s[1])-1) + "&b=" + s[2] + "&c=" + s[0] + "&d=" + str(string.atoi(e[1])-1) + "&e=" + e[2] + "&f=" + e[0] + "&g=d"
		fh = urllib.urlopen(url)
		a = []
		for line in fh.readlines():
			r = line.strip().split(",")
			if len(r) != self.HISTORY_RECORD_NUM:
				return ""
			if r[0] == 'Date':
				continue
			a.append(self.__format_record(r))
		fh.close()
		#a.pop(0) ## remove column name
		if a[0][self.DATE].find("404 Not Found") != -1:
			return ""
		return a

	def __request_history_from_cache(self, symbol, s, e):
		hh = []
		if not os.path.exists(os.path.realpath(os.path.dirname(sys.argv[0])) + "/" + PATH + symbol):
			return ""
		f = open(os.path.realpath(os.path.dirname(sys.argv[0])) + "/" + PATH + symbol, "r")
		for line in f.readlines():
			ret = line.split(",")
			ret[6] = ret[6].strip("\n")
			hh.append(self.__format_record(ret))
		f.close()

		if len(hh) == 0:
			return "";
		hh.sort(key=lambda x:x[self.DATE], reverse=True)
		h = []
		for i in hh:
			if ((datetime.datetime.strptime(s, "%Y/%m/%d") - datetime.datetime.strptime(i[self.DATE], "%Y-%m-%d")).days <= 0) and (datetime.datetime.strptime(e, "%Y/%m/%d") - datetime.datetime.strptime(i[self.DATE], "%Y-%m-%d")).days >= 0:
				h.append(i)
		if len(h) == 0:
			return ""
		h.sort(key=lambda x:x[self.DATE], reverse=True)
		return h

	def update_history(self, symbol, from_day):
		record = []
		rfrom_day = ""
		today = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d")
		if not os.path.exists(PATH + symbol):
			f = open(PATH + symbol, "w")
		else:
			f = open(PATH + symbol, "r")
			err_num = 0
			for line in f.readlines():
				ret = line.split(",")
				if ret.__len__() < 7:
					err_num += 1
				else:
					record.append(self.__format_record(ret))
		f.close()
		if record.__len__() <  (datetime.datetime.now() - datetime.datetime.strptime(from_day, "%Y/%m/%d")).days/2:
			record = []
			rfrom_day = from_day
		else:
			record.sort(key=lambda x:x[self.DATE], reverse=True)
			if (datetime.datetime.strptime(record[0][self.DATE], "%Y-%m-%d") - datetime.datetime.strptime(from_day, "%Y/%m/%d")).days > 30:
				rfrom_day = record[0][self.DATE]
			else:
				rfrom_day = from_day
			if rfrom_day == today:
				print symbol + " already up-to-day"
				return

		h = self.__request_history(symbol, rfrom_day, today)
		if h == "":
			#os.remove(PATH + symbol)
			print symbol + " no data."
			return "ignore"
		record += h
		record.sort(key=lambda x:x[self.DATE], reverse=True)
		record1 = []
		'''
		for i in range(len(record)):
			record[i][self.ADJCLOSE] = record[i][self.ADJCLOSE].split("\n")[0]
		'''

		for i in record:
			if not i in record1:
				record1.append(i)
		record1.sort(key=lambda x:x[self.DATE], reverse=True)
		if record1.__len__() > 0:
			f = open(PATH + symbol, "w")
			for line in record1:
				if len(line) > 0:
					#f.write(','.join(line).split("\n")[0] + "\n")
					f.write(str(line[self.DATE]) + "," + str(line[self.OPEN]) + "," + str(line[self.HIGH]) + "," + str(line[self.LOW]) + ",")
					f.write(str(line[self.CLOSE]) + "," + str(line[self.VOLUME]) + "," + str(line[self.ADJCLOSE]) + "\n")
			f.close()
			print symbol + " updates from " + rfrom_day + " to " + today + " done."
			return "done"
		else:
			print symbol + " no data."
			return "ignore"

	def update_all_history(self, list_filename, from_day):
		stock_list = []
		if not os.path.exists(PATH):
			os.makedirs(PATH)
		f = open(list_filename, "r")
		for stock in f.readlines():
			stock = stock.strip("\n") + ".TW"
			stock_list.append(stock)
		f.close()	

		stock_num = 0

		for stock in stock_list:
			ret = self.update_history(stock, from_day)
			if ret == "done":
				stock_num += 1
		print "Update " + str(stock_num) + " stocks"

	def ma(self, symbol, start_day, end_day, ma):
		h = self.__request_history_from_cache(symbol, start_day, end_day)
		if h.__len__() < ma:
			print str(h.__len__()) + " records are not enough!"
			return "";
		h.sort(key=lambda x:x[self.DATE], reverse=True)
		for i in range(h.__len__()):
			ret = 0
			for j in range(ma, 0, -1):
				if (i + j) >= h.__len__():
					break
				ret += string.atof(h[i+j][self.ADJCLOSE])
			ret /= ma
			h[i]['MA' + str(ma)] = ret
		return h
	def get_quote(self, symbol, parm):
		url = self.quates_url + symbol + "&f=" + parm
		fh = urllib.urlopen(url)
		a = []
		for line in fh.readlines():
			a.append(line.strip().split(","))
		fh.close()
		if a[0][0].find("404 Not Found") != -1:
			return ""
		#print a
		return a
	def oscillators(self, stock, from_day, end_day, ma):
		h = self.ma(stock, from_day, end_day, ma)
		for i in h:
			if string.atof(i[7]) != 0:
				print str(i[0]) + "\t" + str(string.atof(i[6])/string.atof(i[7]))



if __name__ == '__main__':
	ya = yahoo()
	ya.update_all_history("stock_list.txt", "2011/1/1")
