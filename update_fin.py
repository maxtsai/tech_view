#!/usr/bin/env python

import commands


f = open("stock_list.txt", "r")
for sym in f.readlines():
	cmd = "./financial_statement.py %s" % sym.strip('\n')
	stat, ret = commands.getstatusoutput(cmd)
	print ret
f.close()
