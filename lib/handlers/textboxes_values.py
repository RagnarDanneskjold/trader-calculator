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


NAVFORW = {"bo":"bs","bs":"lo","lo":"ls","ls":"bo"}
NAVBACK = {"bo":"ls","bs":"bo","lo":"bs","ls":"lo"}
NAVKEYS = {(wx.WXK_TAB, True):NAVBACK, (wx.WXK_TAB, False):NAVFORW,
           (wx.WXK_RETURN, True):NAVBACK,(wx.WXK_RETURN, False):NAVFORW,
           (wx.WXK_UP, True):NAVBACK, (wx.WXK_UP, False):NAVBACK,
           (wx.WXK_DOWN, True):NAVFORW, (wx.WXK_DOWN, False):NAVFORW}


def KeyDown(self, evt):
    key = evt.GetKeyCode()
    __t = evt.GetEventObject()
    if key in [wx.WXK_UP,wx.WXK_DOWN]:
        v = __t.GetValue()
        if v == "":
            __t.SetValue("1.00")
        else:
            v = float(v)
            __t.SetValue("%.02f"%(
                    v+(0.01 if key == wx.WXK_UP else -0.01)))
        __t.SetSelection(0,-1)
    else:
        if evt.ControlDown() and key in [wx.WXK_TAB]:
            self.view["commission"].SetFocus()
        else:
            nm = __t.GetName()
            nav = NAVKEYS.get((key,evt.ShiftDown()))
            if nav:
                newfocus = nav[nm]
                if (self.model.isUnknown(newfocus) or
                    not self.view[newfocus].IsEnabled()):
                    newfocus = nav[newfocus]
                elem = self.view[newfocus]
                elem.SetFocus()
            else:
                evt.Skip()


def SetFocus(self, evt):
    tb = evt.GetEventObject()
    if self.model.isUnknown(tb.GetName()):
        self.view[self.model.lastfocus].SetFocus()
    else:
        tb.SetSelection(0,-1)
        self.model.lastfocus = tb.GetName()
        mb = self.view["mainFrame"].GetMenuBar()
        mb.FindItemById(xrc.XRCID("menuSetUnknown")).Enable(True)


def init(ctrlr):
    frame = ctrlr.view["mainFrame"]
    
    handlers = [("OnKeyDown", KeyDown, wx.EVT_KEY_DOWN),
                ("OnSetFocus", SetFocus, wx.EVT_SET_FOCUS)]
    for nm,foo,evt in handlers:
        setattr(ctrlr, nm, MethodType(foo, ctrlr))
        for key in ["bs", "bo", "ls", "lo"]:
            ctrlr.view[key] = elem = xrc.XRCCTRL(frame, key)
            elem.Bind(evt, getattr(ctrlr, nm))
