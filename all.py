#! /usr/bin/env python

import urllib
import os, sys

def __request(symbol, stat):
	url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
	#print(url)
	return urllib.urlopen(url).read().strip().strip('"')


def get_all(symbol):
	values = __request(symbol, 'd1dd2aa2a5bb2b3b4cc1c2c3c6c8dd1d2ee1e7e8e9f6ghjkg1g3g4g5g6ii5j1j3j4j5j6k1k2k3k4k5ll1l2l3mm2m3m4m5m6m7m8nn4opp1p2p5p6qrr1r2r5r6r7ss1s7t1t8vv1v7ww1w4xy')
	return values

f = open(os.path.realpath(os.path.dirname(sys.argv[0])) + "/stock_list.txt", "r")
for line in f.readlines():
	stock = line.strip("\n") + ".TW"
	all_records = []
	if __request(stock , "p") != "N/A":
		result = get_all(stock)
		if os.path.exists(os.path.realpath(os.path.dirname(sys.argv[0])) + "/data/" + stock + ".quote"):
			save_f = open(os.path.realpath(os.path.dirname(sys.argv[0])) + "/data/" + stock + ".quote", "r")
			found = False
			for r in save_f.readlines():
				all_records.append(r)
				if result.split(",")[0] == r.split(",")[0]:
					found = True
					break
			save_f.close()
			all_records.append(result)
			if found == False:
				save_f = open(os.path.realpath(os.path.dirname(sys.argv[0])) + "/data/" + stock + ".quote", "w")
				for i in all_records:
					save_f.write(i)
					save_f.write("\n")
				save_f.close()
				print "update " + stock + " done."
			else:
				print stock + " was up-to-day"
		else:
			save_f = open(os.path.realpath(os.path.dirname(sys.argv[0])) + "/data/" + stock + ".quote", "w")
			save_f.write(result)
			save_f.write("\n")
			save_f.close()
f.close()
