#! /usr/bin/env python

from yahoo import *

yf = yahoo()
yf.get_quote("2002.TW", "b4")
#yf.oscillators("2002.TW", "2012/4/1", "2012/6/14", 5)

