#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from string import atoi, atof
import lxml.html as L
import sys
from os import path
from datetime import *

class MOPS_fetch:
	def __init__(self, symbol):
		self.balance_sheet_url = "http://mops.twse.com.tw/mops/web/t05st31"
		self.income_statement_url = "http://mops.twse.com.tw/mops/web/t05st32"
		self.stock_holder_change_url = "http://mops.twse.com.tw/mops/web/t05st35"
		self.cash_change_url = "http://mops.twse.com.tw/mops/web/t05st36"
		self.parms = {}
		self.parms['encodeURIComponent'] = 1
		self.parms['step'] = 1
		self.parms['firstin'] = 1
		self.parms['off'] = 1
		self.parms['keybord4'] = ''
		self.parms['code1'] = ''
		self.parms['TYPEK2'] = ''
		self.parms['checkbtn'] = ''
		self.parms['queryName'] = 'co_id'
		self.parms['TYPEK'] = 'all'
		self.parms['isnew'] = 'true'
		self.parms['co_id'] = symbol
		self.parms['year'] = ''
		self.parms['season'] = ''

		self.items = {}
		self.items[u'資產總計'] = 0
		self.items[u'負債總計'] = 0
		self.items[u'固定資產淨額'] = 0
		self.items[u'流動資產'] = 0
		self.items[u'流動負債'] = 0
		self.items[u'長期負債'] = 0
		self.items[u'股東權益總計'] = 0
		self.items[u'存貨'] = 0
		self.items[u'應收帳款淨額'] = 0
		self.items[u'應付帳款'] = 0
		self.items[u'營業費用合計'] = 0

		self.items[u'營業淨利(淨損)'] = 0
		self.items[u'利息費用'] = 0
		self.items[u'營業外收入及利益'] = 0
		self.items[u'本期淨利(淨損)'] = 0
		self.items[u'繼續營業單位稅前淨利(淨損)'] = 0
		self.update_date = ""

		self.c2e = {} 
		self.c2e['A'] = u'資產總計'
		self.c2e['B'] = u'負債總計'
		self.c2e['C'] = u'固定資產淨額'
		self.c2e['D'] = u'流動資產'
		self.c2e['E'] = u'流動負債'
		self.c2e['F'] = u'長期負債'
		self.c2e['G'] = u'股東權益總計'
		self.c2e['H'] = u'存貨'
		self.c2e['I'] = u'應收帳款淨額'
		self.c2e['J'] = u'應付帳款'
		self.c2e['K'] = u'營業費用合計'
		self.c2e['L'] = u'營業淨利(淨損)'
		self.c2e['M'] = u'利息費用'
		self.c2e['N'] = u'營業外收入及利益'
		self.c2e['O'] = u'本期淨利(淨損)'
		self.c2e['P'] = u'繼續營業單位稅前淨利(淨損)'
		self.c2e['Z'] = 'UpdateDate'
		self.page_cache = ""

	def __fetch(self, url):
		parm = urllib.urlencode(self.parms)
		fd = urllib.urlopen(url, parm)
		self.page_cache = fd.read()
		fd.close()
		return self.page_cache
	def __fetch_stockholer_change(self):
		page = self.__fetch(self.stock_holder_change_url)
		dom = L.fromstring(page)
		locate_str = ".//*[@id='table01']/center/table[3]/tr/td/pre"
		r = dom.xpath(locate_str)
		#print r[0].text

	def __fetch_income_statement(self):
		page = self.__fetch(self.income_statement_url)
		dom = L.fromstring(page)
		locate_str = ".//*[@id='table01']/center/table[2]/tr[1]/td[1]"
		for i in range(1, 150):
			locate_str = locate_str.replace('tr[%d]'%(i-1), 'tr[%d]'%i)
			r = dom.xpath(locate_str)
			if len(r) > 0:
				target = r[0].text.replace(u'\xa0', '')
				for key_name in self.items.keys():
					#print "lookup " + key_name + " ,trg = " + target
					if key_name == target:
						locate_str1 = locate_str.replace('td[1]', 'td[2]')
						#print locate_str1
						rr = dom.xpath(locate_str1)
						if len(rr) > 0:
							self.items[key_name] = rr[0].text
							#print "\t" + rr[0].text
		'''
		for key_name in self.items.keys():
			print "%s = %s" % (key_name, self.items[key_name])
		'''

	def __fetch_balance(self):
		page = self.__fetch(self.balance_sheet_url)
		dom = L.fromstring(page)
		locate_str = ".//*[@id='table01']/center/table/tr[1]/td[1]"
		for i in range(1, 150):
			locate_str = locate_str.replace('tr[%d]'%(i-1), 'tr[%d]'%i)
			r = dom.xpath(locate_str)
			if len(r) > 0:
				target = r[0].text.replace(u'\xa0', '')
				target = target.replace(' ', '')
				for key_name in self.items.keys():
					#print "lookup " + key_name + " with " + target
					if key_name == target:
						locate_str1 = locate_str.replace('td[1]', 'td[2]')
						#print locate_str1
						rr = dom.xpath(locate_str1)
						if len(rr) > 0:
							self.items[key_name] = rr[0].text
		r = dom.xpath(".//*[@id='table01']/center/table/tr[4]/th[2]/b")
		r = r[0].text
		r = r.replace(u'年', '/')
		r = r.replace(u'月', '/')
		r = r.replace(u'日', '')
		self.update_date = r
		print "update %s" % self.update_date
		'''
		for key_name in self.items.keys():
			print "%s = %s" % (key_name, self.items[key_name])
		'''

	def _fetch(self):
		self.__fetch_balance()
		self.__fetch_income_statement()

		for key in self.items.keys():
			self.items[key] = self.items[key].replace(u'\xa0', '')
			#print self.items[key].split('\n')
			if self.items[key] == '':
				self.items[key] = float(0)
			else:
				#print self.items[key].replace(',', '')
				self.items[key] = atof(self.items[key].replace(',', ''))
		return self.items

	def fetch(self):
		if self.load_from_file(self.parms['co_id']) == "OK":
			r = self.update_date.split('/')
			r = "%d/%s/%s" % (atoi(r[0]) + 1911, r[1], r[2])
			if (datetime.now() - datetime.strptime(r, "%Y/%m/%d")).days < 100:
				print "load from cache"
				return self.items
		self.save_to_file(self.parms['co_id'])
		return self.items

	def save_to_file(self, symbol):
		self.items['co_id'] = symbol
		data = self._fetch()
		f = open("data/%s.fin" % symbol, "w")
		for key in data.keys():
			for key1 in self.c2e.keys():
				if self.c2e[key1] == key:
					f.write('%s,%f\n' % (key1, data[key]))
		f.write('Z,%s\n' % self.update_date)
		f.close()
	def load_from_file(self, symbol):
		if not path.exists("data/%s.fin" % symbol):
			return ""
		f = open("data/%s.fin" % symbol, "r")
		for line in f.readlines():
			r = line.strip('\n').split(',')
			if r[0] == 'Z':
				self.update_date = r[1]
			else:
				self.items[self.c2e[r[0]]] = atof(r[1])
		f.close()
		return "OK"

	def report(self):
		data = self.fetch()

		'''
		for key in data.keys():
			print "%s = %10.2f" % (key, data[key])
		'''

		result = {}
		# 股東權益比率
		result['Equity Ratio'] = self.items[u'股東權益總計'] / self.items[u'資產總計']
		# 資本負債比率
		result['Debt Ratio'] = self.items[u'負債總計'] / self.items[u'資產總計'] 
		# 流動負債佔總負債比率
		result['Current/Total Liabilities'] = self.items[u'流動負債'] / self.items[u'負債總計']
		# 流動比率
		result['Current Ratio'] = self.items[u'流動資產'] / self.items[u'流動負債']
		# 存貨週轉率
		result['Stock Turnover'] = self.items[u'營業費用合計'] / self.items[u'存貨']
		# 股東權益報酬率
		result['ROE'] = self.items[u'本期淨利(淨損)'] / self.items[u'股東權益總計']
		# 資產報酬率
		result['ROA'] = self.items[u'本期淨利(淨損)'] / self.items[u'資產總計']
		# 財務槓桿指數
		result['Financial leverage index'] = result['ROE'] / result['ROA']
		# 實質負債比
		result['Real Debt Ratio'] = self.items[u'長期負債'] / (self.items[u'資產總計'] - self.items[u'流動負債'])
		return result




if __name__ == "__main__":
	mops = MOPS_fetch(sys.argv[1])
	result = mops.report()
	for key in result.keys():
		print "%s = %f" % (key, result[key])
	#mops.save_to_file('2002')
	'''
	mops.load_from_file('2002')
	for key in mops.items.keys():
		print "%s = %f" % (key, mops.items[key])
	'''

