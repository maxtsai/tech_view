#! /usr/bin/env python

import string
import sys

f = open(sys.argv[1], "r")

for line in f.readlines():
	stock = line.split("\t")
	if len(stock) < 5:
		continue
	'''
	if string.atof(stock[2].split(" ")[2]) > 400:
		continue
	'''
	if string.atof(stock[2].split(" ")[2]) < 5:
		continue
	if (string.atof(stock[7].split(" ")[1].strip("\n")) > string.atof(sys.argv[2])):
		print line.strip("\n")

f.close()
