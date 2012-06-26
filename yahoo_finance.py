#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib
import string
import os
import datetime
import sys

class yahoo_finance:
	def __init__(self):
		self.chart_url = "http://chart.finance.yahoo.com/z?"
		self.quates_url = "http://finance.yahoo.com/d/quotes.csv?s="
		self.history_quates_url = "http://ichart.yahoo.com/table.csv?s="
		self.sector_url = "http://biz.yahoo.com/p/csv/"

	def __check_time_format(self, day):
		d = day.split("/")
		if d.__len__() != 3: ## expect format like "2012/6/6" or "2012-6-6"
			d = day.split("-")
			if d.__len__() != 3:
				print "unacceptable time format: '" + day + "'"
				return ""
		return d

	def get_quote(self, stock, parm):
		url = self.quates_url + stock + "&f=" + parm
		fh = urllib.urlopen(url)
		a = []
		for line in fh.readlines():
			a.append(line.strip().split(","))
		fh.close()
		if a[0][0].find("404 Not Found") != -1:
			return ""
		print a
		return a

	def get_history(self, stock, start_day, end_day):
		## ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
		s = self.__check_time_format(start_day)
		e = self.__check_time_format(end_day)
		if s == "" or e == "":
			return ""
		url = self.history_quates_url + stock + "&a=" + str(string.atoi(s[1])-1) + "&b=" + s[2] + "&c=" + s[0] + "&d=" + str(string.atoi(e[1])-1) + "&e=" + e[2] + "&f=" + e[0] + "&g=d"
		#print url
		fh = urllib.urlopen(url)
		a = []
		for line in fh.readlines():
			a.append(line.strip().split(","))
		fh.close()
		a.pop(0) ## remove column name
		if a[0][0].find("404 Not Found") != -1:
			return ""
		return a

	def get_history_from_cache(self, stock, start_day, end_day):
		hh = []
		if not os.path.exists("data/" + stock):
			return ""
		f = open("data/" + stock, "r")
		for line in f.readlines():
			ret = line.split(",")
			ret[6] = ret[6].strip("\n")
			hh.append(ret)
		f.close()

		if hh == "":
			return "";

		hh.sort()
		h = []
		for i in hh:
			if ((datetime.datetime.strptime(start_day, "%Y/%m/%d") - datetime.datetime.strptime(i[0], "%Y-%m-%d")).days <= 0) and (datetime.datetime.strptime(end_day, "%Y/%m/%d") - datetime.datetime.strptime(i[0], "%Y-%m-%d")).days >= 0:
				h.append(i)
		h.sort(None, None, True)
		return h

	def ma(self, stock, start_day, end_day, ma):
		h = self.get_history_from_cache(stock, start_day, end_day)

		if h.__len__() < ma:
			print str(h.__len__()) + " records are not enough!"
			return "";
		h.sort(None, None, True)
		#print h
		for i in range(h.__len__()):
			ret = 0
			for j in range(ma, 0, -1):
				if (i + j) >= h.__len__():
					break
				ret += string.atof(h[i+j][6])
			ret /= ma
			h[i].append(ret)
		return h


	def update_history(self, stock, from_day):
		record = []
		rfrom_day = ""
		today = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d")
		if not os.path.exists("data/" + stock):
			return ""

		f = open("data/" + stock, "r")
		err_num = 0
		for line in f.readlines():
			ret = line.split(",")
			if ret.__len__() < 7:
				err_num += 1
			else:
				record.append(ret)
		f.close()
		if record.__len__() <  (datetime.datetime.now() - datetime.datetime.strptime(from_day, "%Y/%m/%d")).days/2:
			record = []
			rfrom_day = from_day
		else:
			record.sort(None, None, True)
			if (datetime.datetime.strptime(record[0][0], "%Y-%m-%d") - datetime.datetime.strptime(from_day, "%Y/%m/%d")).days > 30:
				rfrom_day = record[0][0]
			else:
				rfrom_day = from_day
			if rfrom_day == today:
				print stock + " already up-to-day"
				return

		#print rfrom_day + " <=> " + today
		h = self.get_history(stock, rfrom_day, today)
		record += h
		record.sort(None, None, True)
		record1 = []
		for i in range(len(record)):
			record[i][6] = record[i][6].split("\n")[0]

		for i in record:
			if not i in record1:
				record1.append(i)
		record1.sort(None, None, True)

		if record1.__len__() > 0:
			f = open("data/" + stock, "w")
			for line in record1:
				if len(line) > 0:
					f.write(','.join(line).split("\n")[0] + "\n")
			f.close()
			print stock + " update done."
			return "done"
		else:
			print stock + " no data."
			return "ignore"

	def update_all_history(self, list_filename, from_day):
		stock_list = []
		if not os.path.exists("data"):
			os.makedirs("data")
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

	def oscillators(self, stock, from_day, end_day, ma):
		h = self.ma(stock, from_day, end_day, ma)
		for i in h:
			if string.atof(i[7]) != 0:
				print str(i[0]) + "\t" + str(string.atof(i[6])/string.atof(i[7]))


if __name__ == "__main__":
	yf = yahoo_finance()
	yf.update_all_history(sys.argv[1], sys.argv[2])
