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


NAV = {"commission":"bias", "bias":"commission"}


def OnKeyDown(self, evt):
    key = evt.GetKeyCode()
    __t = evt.GetEventObject()
    if key in [wx.WXK_TAB, wx.WXK_RETURN]:
        if evt.ControlDown() and key in [wx.WXK_TAB]:
            self.view["bo"].SetFocus()
        else:
            nm = __t.GetName()
            self.view[NAV[nm]].SetFocus()
    elif key in [wx.WXK_UP,wx.WXK_DOWN]:
        v = __t.GetValue()
        if v == "":
            __t.SetValue("0.00")
        else:
            v = float(v)
            __t.SetValue("%.02f"%(
                    v+(0.01 if key == wx.WXK_UP else -0.01)))
        __t.SetSelection(0,-1)
    else:
        evt.Skip()


def OnSetFocus(self, evt):
    textCtrl = evt.GetEventObject()
    textCtrl.SetSelection(0,-1)
    self.model.lastfocus = textCtrl.GetName()
    
    mb = self.view["mainFrame"].GetMenuBar()
    mb.FindItemById(xrc.XRCID("menuSetUnknown")).Enable(False)


def init(ctrlr):
    frame = ctrlr.view["mainFrame"]
    
    ctrlr.OnKeyDown = MethodType(OnKeyDown, ctrlr)
    ctrlr.OnSetFocus = MethodType(OnSetFocus, ctrlr)
    
    for key in ["commission", "bias"]:
        ctrlr.view[key] = elem = xrc.XRCCTRL(frame, key)
        elem.Bind(wx.EVT_KEY_DOWN, ctrlr.OnKeyDown)
        elem.Bind(wx.EVT_SET_FOCUS, ctrlr.OnSetFocus)
        elem.ChangeValue("%.02f"%ctrlr.model.conf["parameters"][key])
