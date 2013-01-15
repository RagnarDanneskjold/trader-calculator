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
from wx import xrc


def OnFocusProfits(self, evt):
    self.view[self.model.lastfocus].SetFocus()


def init(ctrlr):
    frame = ctrlr.view["mainFrame"]
    
    ctrlr.OnFocusProfits = MethodType(OnFocusProfits, ctrlr)
    
    for key in ["bp","lp"]:
        ctrlr.view[key] = elem = xrc.XRCCTRL(frame, key)
        elem.Bind(wx.EVT_SET_FOCUS, ctrlr.OnFocusProfits)
