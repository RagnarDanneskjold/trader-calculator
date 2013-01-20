#!/usr/bin/env python
#-*- coding:utf-8 -*-


#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.


import matplotlib as mpl
mpl.use('WX')
from matplotlib.backends.backend_wx import FigureCanvasWx as FigCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
import wx
from wx import xrc
from types import MethodType


class CanvasFrame(wx.Frame):
    
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, wx.ID_ANY,_("Trader Calculator"
                          " - Back-Lay Proportion Rule"))
        
        __f = mpl.figure.Figure(figsize=(1,1),facecolor="white")
        __a = __f.add_subplot(111)
        __a.spines['left'].set_smart_bounds(True)
        __a.spines['bottom'].set_smart_bounds(True)
        __a.xaxis.set_ticks_position('bottom')
        __a.yaxis.set_ticks_position('left')
        __a.spines['left'].set_position('zero')
        __a.spines['bottom'].set_position('zero')
        __a.spines['right'].set_color('none')
        __a.spines['top'].set_color('none')
        __a.annotate(_("Bias"), xy=(1,0), xycoords="figure fraction",
                     xytext=(.93,.1), textcoords="figure fraction",
                     horizontalalignment="center",
                     verticalalignment="center")
        __a.annotate(_("Bias"), xy=(1,0), xycoords="figure fraction",
                     xytext=(.07,.1), textcoords="figure fraction",
                     horizontalalignment="center",
                     verticalalignment="center")
        __a.annotate(_("Amount"), xy=(1,0), xycoords="figure fraction",
                     xytext=(.5,.93), textcoords="figure fraction",
                     horizontalalignment="center",
                     verticalalignment="center")
        __a.set_xlim((-1.1,1.1))
        __a.set_ylim((-1.,10.))
        __a.grid(True)
        
        self.canvas = FigCanvas(self, wx.ID_ANY, __f)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.canvas.draw()
        self.Fit()
        self.SetSize((500,300))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
    
    def Clear(self):
        ax = self.canvas.figure.axes[0]
        while ax.lines: del(ax.lines[0])
        ax.set_xlim((-1.1,1.1))
        ax.set_ylim((-1.,10.))
        ax.set_visible(False)
        self.canvas.draw()
        self.Refresh()
    
    def Plot(self, *args, **kargs):
        ax = self.canvas.figure.axes[0]
        for idx in range(len(ax.lines)):
            if ax.lines[idx].get_label() == kargs["label"]:
                del(ax.lines[idx])
                break
        ax.plot(*args, **kargs)
        ax.set_visible(True)
    
    def Mark(self, bias, amount):
        ax = self.canvas.figure.axes[0]
        if len(ax.texts)>3: del(ax.texts[-1])
        ax.annotate("", xy=(bias,amount), xycoords='data',
                    xytext=(6,24), textcoords='offset points',
                    arrowprops=dict(arrowstyle="->", lw=2, 
                                    connectionstyle="arc3"))
    
    def Autoscale(self):
        ax = self.canvas.figure.axes[0]
        ymin = min([line.get_data()[1].min() for line in ax.lines])
        ymin = (1.1 if ymin<0.0 else .9)*ymin
        ymax = max([line.get_data()[1].max() for line in ax.lines])
        ymax = (1.1 if ymin>0.0 else .9)*ymax
        ax.set_ylim((ymin,ymax))
        self.canvas.draw()
        self.Refresh()
    
    def OnClose(self, evt):
        mbar = self.GetParent().GetMenuBar()
        menu = mbar.GetMenu(1)
        idx = menu.FindItem("Show Plot")
        menu.Check(idx, False)
        self.Show(False)


def OnShowPlot(self, evt):
    self.view["plot"].Show(not self.view["plot"].IsShown())
    self.view["mainFrame"].Raise()


def init(ctrlr):
    frame = ctrlr.view["mainFrame"]
    ctrlr.view["plot"] = CanvasFrame(frame)
    ctrlr.view["plot"].Hide()
    
    ctrlr.OnShowPlot = MethodType(OnShowPlot, ctrlr)
    
    frame.Bind(wx.EVT_MENU, ctrlr.OnShowPlot,
               id=xrc.XRCID("menuShowPlot"))
