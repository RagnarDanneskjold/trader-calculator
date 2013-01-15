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


def parseOdd(val):
    val = float(val)
    assert val >= 1.0
    return val


def parseStake(val):
    val = float(val)
    assert val >= 0.0
    return val


def ValidateTB(key, parser, view):
    __t = view[key]
    try:
        parser(__t.GetValue())
        __t.SetBackgroundColour(wx.NullColor)
    except:
        __t.SetBackgroundColour("#EC9797")
    __t.Refresh()


def OnLS(self, v):
    self.view["ls"].ChangeValue("%.02f"%v if type(v) is float else v)
    ValidateTB("ls", parseStake, self.view)


def OnLO(self, v):
    self.view["lo"].ChangeValue("%.02f"%v if type(v) is float else v)
    ValidateTB("lo", parseOdd, self.view)


def OnBS(self, v):
    self.view["bs"].ChangeValue("%.02f"%v if type(v) is float else v)
    ValidateTB("bs", parseStake, self.view)


def OnBO(self, v):
    self.view["bo"].ChangeValue("%.02f"%v if type(v) is float else v)
    ValidateTB("bo", parseOdd, self.view)


def init(ctrlr):
    frame = ctrlr.view["mainFrame"]
    
    subscribes = [("OnLS", OnLS, "ls"), ("OnLO", OnLO, "lo"),
                  ("OnBS", OnBS, "bs"), ("OnBO", OnBO, "bo")]
    for lbl,mtd,sig in subscribes:
        setattr(ctrlr, lbl, MethodType(mtd, ctrlr))
        ctrlr.model.subscribe(getattr(ctrlr,lbl), sig)
