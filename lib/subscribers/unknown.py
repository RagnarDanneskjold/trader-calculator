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
        __t.SetBackgroundColour(wx.NullColour)
    except:
        __t.SetBackgroundColour("#EC9797")
    __t.Refresh()


def OnFocusUnknown(self, evt):
    self.view[self.model.lastfocus].SetFocus()


def OnSetUnknown(self, old, new):
    tb = self.view[old]
    tb.SetFocus()
    tb.SetForegroundColour(wx.NullColor)
    ValidateTB(old, parseStake if old[-1]=="s" else parseOdd, self.view)
    if new:
        self.OnGuessUnknown(new)
    tb.SetValue(tb.GetValue())


def OnGuessUnknown(self, new):
    tb = self.view[new]
    tb.ChangeValue("")
    tb.SetForegroundColour("#0000FF")
    tb.SetBackgroundColour(wx.NullColour)
    tb.Refresh()
    
    titles = {"bo":_("Back Odd"), "bs":_("Back Stake"),
              "lo":_("Lay Odd"), "ls":_("Lay Stake")}
    title = "%s - %s"%(titles[new], _("Trader Calculator"))
    self.view["mainFrame"].SetTitle(title)
    self.view["mainFrame"].Refresh()


def init(ctrlr):
    frame = ctrlr.view["mainFrame"]
    
    ctrlr.OnGuessUnknown = MethodType(OnGuessUnknown, ctrlr)
    ctrlr.OnSetUnknown = MethodType(OnSetUnknown, ctrlr)
    ctrlr.OnFocusUnknown = MethodType(OnFocusUnknown, ctrlr)
    
    ctrlr.model.subscribe(ctrlr.OnGuessUnknown, "guess unknown")
    ctrlr.model.subscribe(ctrlr.OnSetUnknown, "set unknown")
