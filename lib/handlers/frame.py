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


import os
from types import MethodType
import wx
from wx import xrc


def OnSize(self, evt):
    self.model.set("settings", "size", evt.Size)
    evt.Skip()


def parseXRC(ctrlr):
    __t = [ctrlr.model.conf["basedir"], "resources", "view",
           "mainFrame.xrc"]
    xrcres = __t = xrc.XmlResource(os.path.join(*__t))
    mainfr = __t.LoadFrame(None, "mainFrame")
    if mainfr is None:
        import logging as log
        log.critical("unable to parse 'lib/view/mainFrame.xrc'")
        exit(1)
    return xrcres, mainfr


def init(ctrlr):
    ctrlr.view["xrc"],ctrlr.view["mainFrame"] = parseXRC(ctrlr)
    
    frame = ctrlr.view["mainFrame"]
    ctrlr.SetTopWindow(frame)
    iconpath = os.path.join(*[ctrlr.model.conf["basedir"], "resources",
                              "icon", "trader-calculator.ico"])
    frame.SetIcon(wx.Icon(iconpath, wx.BITMAP_TYPE_ICO))
    frame.SetSize(tuple(ctrlr.model.conf["settings"]["size"]))
    frame.Show()
    
    ctrlr.OnSize = MethodType(OnSize, ctrlr)
    
    frame.Bind(wx.EVT_SIZE, ctrlr.OnSize)
