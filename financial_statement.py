#!/usr/bin/env python

#import urllib.request
import urllib
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
	return ''.join(self.fed)


parms = {}
parms['encodeURIComponent'] = 1
parms['step'] = 1
parms['firstin'] = 1
parms['off'] = 1
parms['keybord4'] = ''
parms['code1'] = ''
parms['TYPEK2'] = ''
parms['checkbtn'] = ''
parms['queryName'] = 'co_id'
parms['TYPEK'] = 'all'
parms['isnew'] = 'true'
parms['co_id'] = '2454'
parms['year'] = ''
parms['season'] = ''
parm = urllib.urlencode(parms)
#print parm
text = urllib.urlopen("http://mops.twse.com.tw/mops/web/t05st20", parm).read()
s = MLStripper()
s.feed(text)
print s.get_data()
