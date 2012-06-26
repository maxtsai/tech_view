#!/usr/bin/python
#coding=utf-8


import wx
import string
import datetime
import sys
import  wx.lib.fancytext as fancytext
from yahoo import *
from wave import *

class LineChart(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		self.SetBackgroundColour('WHITE')
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Size = (600, 480)
		self.Title = "Line Chart"
		self.Axis = [[0, 600], [0, 100]]
		self.Margin = (30, 30, 50, 200) # LEFT, TOP, RIGHT, BOTTOM
		self.AData = []
		self.Data = []
		self.Volumn = []
		self.Bind(wx.EVT_MOTION, self.onMouseOver)
		self.SubShow = False
		self.MPosition = (0, 0)

	def onMouseOver(self, event):
		x = event.GetX()
		y = event.GetY()
		if y < self.Margin[1] or y > self.Size[1]-self.Margin[3] or x < self.Margin[0] or x > self.Size[0]-self.Margin[2]:
			self.SubShow = False
			event.Skip()
			self.Refresh()
		else:
			self.SubShow = True
			self.MPosition = (x, y)
			event.Skip()
			self.Refresh()
			#print "x, y = %d, %d" % (x, y)

	def SetSize(self, Size):
		self.Size = Size
		self.Axis[0][0] = self.Margin[0]
		self.Axis[0][1] = self.Size[0] - self.Margin[2]
		self.Axis[1][0] = self.Margin[3]
		self.Axis[1][1] = self.Size[1] - self.Margin[1]
		#print "%d, %d, %d, %d" % (self.Axis[0][0], self.Axis[0][1], self.Axis[1][0], self.Axis[1][1])
	def SetTitle(self, Title):
		self.Title = Title
	def SetAllData(self, Data):
		self.AData = Data
	def SetData(self, Data):
		self.Data = Data
		self.Data.sort()
	def SetVolumnData(self, Data):
		self.Volumn = Data
		self.Volumn.sort()

	def OnPaint(self, event):
		self.SetSize(self.GetSize())
		dc = wx.PaintDC(self)
		dc.Clear()
		dc.SetDeviceOrigin(self.Margin[0], self.Size[1])
		dc.SetAxisOrientation(True, True)
		dc.SetPen(wx.Pen('WHITE', 1))
		dc.DrawRectangle(1, 1, self.Size[0], self.Size[1])
		self.DrawAxis(dc)
		self.DrawTitle(dc)
		self.DrawData(dc)
		self.DrawVolumn(dc)
		dc.SetPen(wx.Pen('WHITE', 1))

		if self.SubShow == True:
			self.AData.sort(key=lambda x:x['Date'], reverse=False)
			x_axis = (self.Axis[0][1] - self.Axis[0][0]) / len(self.Data)
			if x_axis == 0:
				x_axis = int(len(self.Data)/(self.Axis[0][1] - self.Axis[0][0]))
				print "## axis = " + str(x_axis)
			else:
				if int((self.MPosition[0]-self.Axis[0][0])/x_axis) > len(self.AData):
					return
			show_keys = self.AData[int((self.MPosition[0]-self.Axis[0][0])/x_axis)].keys()
			show_str = []
			w = []
			h = []
			h_total = 0
			for show_key in show_keys:
				#input_str = ('<font style="italic" family="swiss" color="blue" weight="bold" > <sub> %s = %s </sub> </font>' %
				if self.AData[int((self.MPosition[0]-self.Axis[0][0])/x_axis)]['Close'] > self.AData[int((self.MPosition[0]-self.Axis[0][0])/x_axis)]['Open']:
					input_str = ('<font style="normal" color="red" weight="bold" size="10" > <sub> %s = %s </sub> </font>' %
							(show_key, self.AData[int((self.MPosition[0]-self.Axis[0][0])/x_axis)][show_key]))
				elif self.AData[int((self.MPosition[0]-self.Axis[0][0])/x_axis)]['Close'] < self.AData[int((self.MPosition[0]-self.Axis[0][0])/x_axis)]['Open']:
					input_str = ('<font style="normal" color="dark green" weight="bold" size="10" > <sub> %s = %s </sub> </font>' %
							(show_key, self.AData[int((self.MPosition[0]-self.Axis[0][0])/x_axis)][show_key]))
				else:
					input_str = ('<font style="normal" color="black" weight="bold" size="10" > <sub> %s = %s </sub> </font>' %
							(show_key, self.AData[int((self.MPosition[0]-self.Axis[0][0])/x_axis)][show_key]))
				show_str.append(input_str)
				ww, hh = fancytext.GetExtent(input_str, dc)
				w.append(ww)
				hh = hh/3*2
				h.append(hh)
				h_total += hh
			w_max = 0
			for i in w:
				if w_max < i:
					w_max = i

			if self.MPosition[0] > self.Size[0]/2:
				dc.DrawRectangle(self.MPosition[0]-w_max-9, self.Size[1]-self.MPosition[1], w_max+10, h_total)
			else:
				dc.DrawRectangle(self.MPosition[0], self.Size[1]-self.MPosition[1], w_max+10, h_total)

			ii = 0
			for i in show_str:
				h_ = 0
				for j in range(0, ii):
					h_ += h[j]
				if self.MPosition[0] > self.Size[0]/2:
					fancytext.RenderToDC(i, dc, self.MPosition[0]-w_max-5, self.Size[1]-self.MPosition[1]+h_)
				else:
					fancytext.RenderToDC(i, dc, self.MPosition[0]+5, self.Size[1]-self.MPosition[1]+h_)
				ii += 1

			dc.SetPen(wx.Pen('GREEN', 1))
			dc.DrawLine(self.MPosition[0], self.Axis[1][0], self.MPosition[0], self.Axis[1][1])
			dc.SetPen(wx.Pen('BLUE', 1))


	def DrawAxis(self, dc):
		dc.SetPen(wx.Pen('BLACK'))
		font =  dc.GetFont()
		font.SetPointSize(8)
		dc.SetFont(font)
		dc.DrawLine(self.Axis[0][0], self.Axis[1][0], self.Axis[0][1], self.Axis[1][0])
		dc.DrawLine(self.Axis[0][0], self.Axis[1][0], self.Axis[0][0], self.Axis[1][1])

		y_min = 1000
		y_max = 0
		for i in self.Data:
			if y_min > i[1]:
				y_min = i[1]
			if y_max < i[1]:
				y_max = i[1]
		y_axis = (self.Axis[1][1] - self.Axis[1][0]) / (y_max-y_min)
		y_axis = int(y_axis)
		x_axis = (self.Axis[0][1] - self.Axis[0][0]) / len(self.Data)

		dc.SetPen(wx.Pen('GREY'))
		ii = 0
		#print "(%d - %d) / %d = %d" % (self.Axis[1][1], self.Axis[1][0], y_max-y_min, y_axis)
		if y_axis == 0:
			y_axis = int((y_max-y_min)/(self.Axis[1][1] - self.Axis[1][0]))
			#print y_axis
		for i in range(self.Axis[1][0], self.Axis[1][1], y_axis):
			dc.DrawLine(self.Axis[0][0], i, self.Axis[0][1], i)
			dc.DrawText(str(int(y_min+ii)), self.Axis[0][0] - 30, i)
			ii += 1
		if x_axis == 0:
			x_axis = int(len(self.Data)/(self.Axis[0][1] - self.Axis[0][0]))
			print "axis = " + str(x_axis)

		for i in range(self.Axis[0][0], self.Axis[0][1], x_axis):
			dc.DrawLine(i, self.Axis[1][0], i, self.Axis[1][1])
		ii = 0
		for i in self.Data:
			r = [ii*x_axis+self.Axis[0][0], (i[1]-y_min)*y_axis+self.Axis[1][0]]
			ii += 1
			if (ii%2 == 0):
				dc.DrawText(datetime.datetime.strptime(i[0], "%Y-%m-%d").strftime("%m/%d"), r[0]-12, self.Axis[1][0] - 10)
			else:
				dc.DrawText(datetime.datetime.strptime(i[0], "%Y-%m-%d").strftime("%m/%d"), r[0]-12, self.Axis[1][0])

	def DrawTitle(self, dc):
		font =  dc.GetFont()
		font.SetPointSize(14)
		font.SetWeight(wx.FONTWEIGHT_BOLD)
		dc.SetFont(font)
		dc.DrawText(self.Title, self.Size[0]/2-100-4*len(self.Title), self.Size[1])
		ii = 0

	def DrawData(self, dc):
		font =  dc.GetFont()
		font.SetPointSize(8)
		font.SetWeight(wx.FONTWEIGHT_NORMAL)
		dc.SetFont(font)
		dc.SetPen(wx.Pen('BLUE'))
		pixel = []
		y_min = 1000
		y_max = 0
		for i in self.Data:
			if y_min > i[1]:
				y_min = i[1]
			if y_max < i[1]:
				y_max = i[1]
		y_axis = (self.Axis[1][1] - self.Axis[1][0]) / (y_max-y_min)
		y_axis = int(y_axis)
		x_axis = (self.Axis[0][1] - self.Axis[0][0]) / len(self.Data)
		if y_axis == 0:
			y_axis = int((y_max-y_min)/(self.Axis[1][1] - self.Axis[1][0]))
		if x_axis == 0:
			x_axis = int(len(self.Data)/(self.Axis[0][1] - self.Axis[0][0]))
		ii = 0
		for i in self.Data:
			r = [ii*x_axis+self.Axis[0][0], (i[1]-y_min)*y_axis+self.Axis[1][0]]
			pixel.append(r)
			ii += 1
		dc.DrawSpline(pixel)

	def DrawVolumn(self, dc):
		max_volumn = float(0)
		for i in self.Volumn:
			if max_volumn < i[1]:
				max_volumn = i[1]
		Axis = [self.Axis[0], [50, self.Axis[1][0]-50]]
		dc.SetPen(wx.Pen('BLACK'))
		font =  dc.GetFont()
		font.SetPointSize(8)
		dc.SetFont(font)
		dc.DrawLine(Axis[0][0], Axis[1][0], Axis[0][1], Axis[1][0])
		dc.DrawLine(Axis[0][0], Axis[1][0], Axis[0][0], Axis[1][1])

		y_axis = float((Axis[1][1] - Axis[1][0])) / float(max_volumn)
		x_axis = (Axis[0][1] - Axis[0][0]) / len(self.Volumn)
		dc.SetPen(wx.Pen('GREY', 1))
		ii = 0
		for i in range(Axis[1][0], Axis[1][1], int((Axis[1][1] - Axis[1][0])/5)):
			dc.DrawLine(Axis[0][0], i, Axis[0][1], i)
			dc.DrawText(str(int(max_volumn/5*ii)), Axis[0][0]-50, i)
			ii += 1
			
		dc.SetPen(wx.Pen('DARKGREEN', 10))

		ii = 0
		for i in self.Volumn:
			volumn = i[1]
			dc.DrawLine(ii*x_axis+Axis[0][0], Axis[1][0], ii*x_axis+Axis[0][0], int(volumn*y_axis)+Axis[1][0])
			ii += 1


class LineChartExample(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, size=(800, 600))

		#records = wave(sys.argv[1], "2011/6/25", "2012/6/25", 5)
		y = yahoo()
		records = y.ma(sys.argv[1], "2011/5/25", "2012/6/25", 5)
		dat = []
		vdat = []
		for i in records:
			dat.append([i['Date'], i['Close']])
			vdat.append([i['Date'], i['Volumn']])

		self.panel = wx.Panel(self, -1)
		self.panel.SetBackgroundColour('WHITE')

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		linechart = LineChart(self.panel)
		linechart.SetSize((800, 600))
		linechart.SetTitle("Max's testing. line chart.")
		linechart.SetData(dat)
		linechart.SetAllData(records)
		linechart.SetVolumnData(vdat)

		hbox.Add(linechart, 1, wx.EXPAND | wx.ALL, 15)
		self.panel.SetSizer(hbox)

		self.Centre()
		self.Show(True)


if __name__ == '__main__':
	app = wx.App()
	LineChartExample(None, -1, 'A line chart')
	app.MainLoop()

