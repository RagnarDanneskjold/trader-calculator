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


def __GetTextboxesValues(keysANDparsers, view, model=None):
    values = {}
    for key,parser in keysANDparsers:
        __t = view[key]
        try:
            param = __t.GetValue()
            if model: model.set("parameters", key, param)
            values[key] = parser(param)
            __t.SetBackgroundColour(wx.NullColour)
        except:
            __t.SetBackgroundColour("#EC9797")
        __t.Update()
        __t.Refresh()
    return values


def OnText(self, evt):
    __b = lambda v: self.model.conf.parse("parameters","bias",v)
    __c = lambda v: self.model.conf.parse("parameters","commission",v)
    __t = [("bias", __b), ("commission", __c)]
    params = __GetTextboxesValues(__t, self.view, self.model)
    flagParams = len(params) != len(__t)
    
    __t = [("bs", parseStake), ("bo", parseOdd),
           ("ls", parseStake), ("lo", parseOdd)]
    __t = [p for p in [("bs", parseStake), ("bo", parseOdd),
                       ("ls", parseStake), ("lo", parseOdd)]
             if not self.model.isUnknown(p[0])]
    vals = __GetTextboxesValues(__t, self.view)
    
    tbLabel = evt.GetEventObject().GetName()
    
    if len(vals)==3 and self.model.unknown is None:
        self.model.guessUnknown(vals)
    
    unklbl = self.model.unknown[0] if self.model.unknown else None
    vkeys = list(vals.iterkeys())
    flagVals = (len(vals)==4 or (len(vals)==3 and unklbl not in vkeys))
    if flagVals and not flagParams and self.model.unknown is not None:
        self.model.calculate(tbLabel, params, vals)
    else:
        unklst = [self.model.unknown[0]] if self.model.unknown else []
        for key in ["bp", "lp"] + unklst:
            self.view[key].ChangeValue("")
            self.view[key].Refresh()
        self.view["plot"].Clear()


def init(ctrlr):
    frame = ctrlr.view["mainFrame"]
    
    ctrlr.OnText = MethodType(OnText, ctrlr)
    for key in ["bs", "bo", "ls", "lo", "bias", "commission"]:
        elem = ctrlr.view[key]
        elem.Bind(wx.EVT_TEXT, ctrlr.OnText)
    
    ctrlr.view["bo"].SetFocus()
    ctrlr.view["bo"].SetValue("")
