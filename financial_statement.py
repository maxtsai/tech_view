#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import lxml.html as L

class MOPS_fetch:
	def __init__(self):
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
		self.parms['co_id'] = '2454'
		self.parms['year'] = ''
		self.parms['season'] = ''

		self.items = {}
		self.items[u'資產總計'] = 0
		self.items[u'負債總計'] = 0
		self.items[u'長期負債'] = 0
		self.items[u'短期借款'] = 0
		self.items[u'一年內到期的長期負債'] = 0
		self.items[u'長期借款'] = 0
		self.items[u'應付債券'] = 0
		self.items[u'長期應付款'] = 0
		self.items[u'流動資產'] = 0
		self.items[u'流動負債'] = 0
		self.items[u'速動資產'] = 0
		self.items[u'固定資產'] = 0
		self.items[u'應收帳款'] = 0
		self.items[u'所得稅及利息費用前純益'] = 0
		self.items[u'銀行利息費用支出'] = 0
		self.items[u'繼續營業單位稅前淨利(淨損)'] = 0
		self.items[u'利息費用'] = 0
		self.items[u'存貨'] = 0
		self.items[u'預付款項'] = 0
		self.items[u'本期利息支出'] = 0
		self.items[u'營運成本'] = 0
		self.items[u'營業淨利'] = 0
		self.items[u'營業外收入及利益'] = 0
		self.items[u'營業收入'] = 0
		self.items[u'本期淨利'] = 0
		self.items[u'股東權益'] = 0

		self.page_cache = ""

	def __fetch(self, url):
		parm = urllib.urlencode(self.parms)
		fd = urllib.urlopen(self.balance_sheet_url, parm)
		self.page_cache = fd.read()
		fd.close()
		return self.page_cache

	def __fetch_balance(self):
		page = self.__fetch(self.balance_sheet_url)
		dom = L.fromstring(page)
		locate_str = ".//*[@id='table01']/center/table/tr[1]/td[1]"
		for i in range(1, 150):
			locate_str = locate_str.replace('tr[%d]'%(i-1), 'tr[%d]'%i)
			r = dom.xpath(locate_str)
			if len(r) > 0:
				for key_name in self.items.keys():
					if key_name == r[0].text.replace(u'\xa0', ''):
						locate_str = locate_str.replace('td[1]', 'td[2]')
						print locate_str
						print dom.xpath(locate_str)[0].text

	def _test_1(self):
		self.__fetch_balance()

	def _test(self):
		parm = urllib.urlencode(self.parms)
		fd = urllib.urlopen("http://mops.twse.com.tw/mops/web/t05st31", parm)
		page = fd.read()
		fd.close()

		dom = L.fromstring(page)

		'''
		Firebug & Firepath are great tools. Firebug can show request content, 
		and Firepath can locate tag.
		ps: Firepath adds 'tbody' tag, remove it.
		'''
		r = dom.xpath(".//*[@id='table01']/center/table/tr[8]/td[2]")
		r1 = dom.xpath(".//*[@id='table01']/center/table/tr[4]/th[2]/b")
		print r[0].text
		print r1[0].text


if __name__ == "__main__":
	mops = MOPS_fetch()
	mops._test_1()
