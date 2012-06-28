#!/usr/bin/env python

#import urllib.request
import urllib
import lxml.html as L
import lxml.html.soupparser as S

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

		self.accounts = []
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
	mops._test()
