#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
from financial_statement import *
from yahoo import *

candidates = []

mops = MOPS_fetch()
f = open("stock_list.txt", "r")
for sym in f.readlines():
	sym = sym.strip('\n')
	result = mops.report(sym)
	if result != "no data":
		if result['ROE'] > 0.02:
			if result['Current Ratio'] >= 1.2:
				if result['Real Debt Ratio'] < 0.01:
					candidates.append(sym)
f.close()

y = yahoo()
for i in candidates:
	records = y.ma(str(i) + ".TW", "2012/1/1", "2012/7/1", 5)
	if len(records) < 10:
		continue
	avg_vol = 0
	avg_count = 0
	for j in records:
		avg_vol += j['Volumn']/1000
		avg_count += 1
	avg_vol = avg_vol / avg_count
	if avg_vol > 1000 and records[0]['Close'] < 50 and records[0]['Close'] > 10:
		print "found " + str(i)
