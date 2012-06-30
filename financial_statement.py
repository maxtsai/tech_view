#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from string import atoi, atof
import lxml.html as L
import sys

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

		'''
		self.items[u'短期借款'] = 0
		self.items[u'一年內到期的長期負債'] = 0
		self.items[u'長期借款'] = 0
		self.items[u'應付債券'] = 0
		self.items[u'長期應付款'] = 0
		self.items[u'速動資產'] = 0
		self.items[u'所得稅及利息費用前純益'] = 0
		self.items[u'銀行利息費用支出'] = 0
		self.items[u'預付款項'] = 0
		self.items[u'本期利息支出'] = 0
		'''

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
		'''
		for key_name in self.items.keys():
			print "%s = %s" % (key_name, self.items[key_name])
		'''

	def fetch(self):
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
	def report(self):
		data = self.fetch()
		result = {}
		result[u'股東權益比率'] = self.items[u'股東權益總計'] / self.items[u'資產總計']
		result[u'資本負債比率'] = self.items[u'負債總計'] / self.items[u'資產總計'] 
		result[u'流動負債佔總負債比率'] = self.items[u'流動負債'] / self.items[u'負債總計']
		result[u'流動比率'] = self.items[u'流動資產'] / self.items[u'流動負債']
		result[u'存貨週轉率'] = self.items[u'營業費用合計'] / self.items[u'存貨']
		result[u'股東權益報酬率'] = self.items[u'營業淨利(淨損)'] / self.items[u'股東權益總計']
		result[u'資產報酬率'] = self.items[u'營業淨利(淨損)'] / self.items[u'資產總計']
		result[u'財務槓桿指數'] = result[u'股東權益報酬率'] / result[u'資產報酬率']

		return result


	def _test(self):
		parm = urllib.urlencode(self.parms)
		fd = urllib.urlopen("http://mops.twse.com.tw/mops/web/t05st32", parm)
		page = fd.read()
		fd.close()

		dom = L.fromstring(page)

		'''
		Firebug & Firepath are great tools. Firebug can show request content, 
		and Firepath can locate tag.
		ps: Firepath adds 'tbody' tag, remove it.
		'''
		r = dom.xpath(".//*[@id='table01']/center/table[2]/tr[19]/td[1]")
		print r[0].text


if __name__ == "__main__":
	mops = MOPS_fetch(sys.argv[1])
	result = mops.report()

	for key in result.keys():
		print "%s = %f" % (key, result[key])


