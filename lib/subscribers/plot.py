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


from types import MethodType
import wx
import numpy as np
from threading import Timer, Lock


class TaskBuffer:
    def __init__(self, delay):
        self.delay = delay
        self.timer = None
        self.lock = Lock()
        self.task = None
    
    def Post(self, func, *args, **kargs):
        try:
            self.timer.cancel()
            del self.timer
        except: pass
        with self.lock:
            self.task = (func, args, kargs)
            self.timer = Timer(float(self.delay["plotdelay"]),
                               self.Dispatch)
            self.timer.start()
    
    def Dispatch(self):
        with self.lock:
            func, args, kargs = self.task
            self.timer = self.task = None
            wx.CallAfter(func, *args, **kargs)


BIAS = np.arange(-.99, .99, 0.01)
BETA = (1.+BIAS)/(1.-BIAS)


def HouseFunction(h,x):
    if type(x) is float:
        return (np.zeros(len(BIAS)))+(x if x<0 else x*(1.-h))
    return np.array([(xi if xi<0 else xi*(1.-h)) for xi in x])


def UpdatePlot(self,bias,am,sb,ob,sl,ol,key):
    comm = self.model.conf["parameters"]["commission"]
    ptrue = HouseFunction(comm,((ob-1.)*sb) + ((1.-ol)*sl))
    pfalse = HouseFunction(comm,(sl-sb))
    
    lw = {"__WXGTK__":2, "__WXMSW__":10, "__WXMAC__":2}[wx.Platform]
    
    self.view["plot"].Plot(BIAS, {"sb":sb,"ob":ob,"sl":sl,"ol":ol}[key],
                           "g", linewidth=lw, ls="-", label="Amount")
    self.view["plot"].Plot(BIAS, ptrue, "b", linewidth=lw, ls="-",
                           label="BackProfits")
    self.view["plot"].Plot(BIAS, pfalse, "r", linewidth=lw, ls="-",
                           label="LayProfits")
    self.view["plot"].Mark(bias, am)
    self.view["plot"].Autoscale()


def OnLS(self, v):
    tctrls = [self.view[k] for k in ["bs","bo","lo"]]
    sb,ob,ol = (float(tc.GetValue()) for tc in tctrls)
    sl = sb*(ob+BETA-1)/(ol+BETA-1)
    bias = self.model.conf["parameters"]["bias"]
    beta = (1.+bias)/(1.-bias)
    am = sb*(ob+beta-1)/(ol+beta-1)
    self.view["plot"].taskdelayer.Post(self.UpdatePlot, bias, am,
                                       sb, ob, sl, ol, "sl")


def OnLO(self, v):
    tctrls = [self.view[k] for k in ["bs","bo","ls"]]
    sb,ob,sl= (float(tc.GetValue()) for tc in tctrls)
    ol = BETA*((sb/sl)-1.) + ((sb/sl)*(ob-1.)+1.)
    bias = self.model.conf["parameters"]["bias"]
    beta = (1.+bias)/(1.-bias)
    am = beta*((sb/sl)-1.) + ((sb/sl)*(ob-1.)+1.)
    self.view["plot"].taskdelayer.Post(self.UpdatePlot, bias, am,
                                       sb, ob, sl, ol, "ol")


def OnBS(self, v):
    tctrls = [self.view[k] for k in ["bo","ls","lo"]]
    ob,sl,ol = (float(tc.GetValue()) for tc in tctrls)
    sb = sl*(ol+BETA-1)/(ob+BETA-1)
    bias = self.model.conf["parameters"]["bias"]
    beta = (1.+bias)/(1.-bias)
    am = sl*(ol+beta-1)/(ob+beta-1)
    self.view["plot"].taskdelayer.Post(self.UpdatePlot, bias, am,
                                       sb, ob, sl, ol, "sb")


def OnBO(self, v):
    tctrls = [self.view[k] for k in ["bs","ls","lo"]]
    sb,sl,ol= (float(tc.GetValue()) for tc in tctrls)
    ob = BETA*((sl/sb)-1.) + ((sl/sb)*(ol-1.)+1.)
    bias = self.model.conf["parameters"]["bias"]
    beta = (1.+bias)/(1.-bias)
    am = beta*((sl/sb)-1.) + ((sl/sb)*(ol-1.)+1.)
    self.view["plot"].taskdelayer.Post(self.UpdatePlot, bias, am,
                                       sb, ob, sl, ol, "ob")


def OnSU(self, old, new):
    if new is None:
        self.view["plot"].Clear()


def init(ctrlr):
    subscribes = [("OnLS", OnLS, "ls"), ("OnLO", OnLO, "lo"),
                  ("OnBS", OnBS, "bs"), ("OnBO", OnBO, "bo"),
                  ("OnSU", OnSU, "set unknown")]
    for lbl,mtd,sig in subscribes:
        setattr(ctrlr, lbl, MethodType(mtd, ctrlr))
        ctrlr.model.subscribe(getattr(ctrlr,lbl), sig)
    
    ctrlr.UpdatePlot = MethodType(UpdatePlot, ctrlr)
    
    ctrlr.view["plot"].taskdelayer = TaskBuffer(
            ctrlr.model.conf["settings"])
