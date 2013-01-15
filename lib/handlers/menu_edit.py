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


from lib.langs import GetLanguages


def ClearTB(self, evt):
    self.view["mainFrame"].FindFocus().SetValue("")


def ResetTBs(self, evt):
    self.model.clear()
    for key in ["bs","bo","ls","lo"]:
        self.view[key].ChangeValue("")
    self.view["bo"].SetValue("")
    self.view["bo"].SetFocus()


def SetUnknown(self, evt):
    unk = self.view["mainFrame"].FindFocus().GetName()
    self.model.setUnknown(unk)


def init(ctrlr):
    frame = ctrlr.view["mainFrame"]
    
    handlers = [("ClearTB", ClearTB, "menuClearTextbox"),
                ("ResetTBs", ResetTBs, "menuClearValues"),
                ("SetUnknown", SetUnknown, "menuSetUnknown")]
    for nm,foo,lbl in handlers:
        setattr(ctrlr, nm, MethodType(foo, ctrlr))
        frame.Bind(wx.EVT_MENU, getattr(ctrlr, nm), id=xrc.XRCID(lbl))
