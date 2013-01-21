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


def OnMenuPreferences(self, evt):
    dialog = self.view["xrc"].LoadDialog(self.view["mainFrame"], 
                                         "preferencesDialog")
    if dialog is None:
        __msg = "unable to open preferences dialog"
        log.critical(__msg)
        self.view["mainFrame"].SetStatus(__msg)
        evt.Skip()
        return
    
    elems = {}
    l,i = GetLanguages()
    __l = xrc.XRCCTRL(dialog, "language")
    __l.AppendItems(i)
    __l.SetSelection(l.index(self.model.conf["settings"]["language"]))
    elems["language"] = lambda: l[__l.GetSelection()]
    __v = xrc.XRCCTRL(dialog, "verbose")
    __v.SetSelection(self.model.conf["settings"]["verbose"])
    elems["verbose"] = lambda: __v.GetSelection()
    __p = xrc.XRCCTRL(dialog, "plotdelay")
    __p.SetSelection([.1,.2,.5,.7,1.,1.5,2.3].index(
        self.model.conf["settings"]["plotdelay"]))
    elems["plotdelay"] = lambda: [.1,.2,.5,.7,1.,1.5,2.3][
            __p.GetSelection()]
    __c = xrc.XRCCTRL(dialog, "cancel")
    __c.SetId(wx.ID_CANCEL)
    __o = xrc.XRCCTRL(dialog, "ok")
    __o.SetId(wx.ID_OK)
    __o.SetFocus()
    
    __t = lambda *args: dialog.Close()
    dialog.Bind(wx.EVT_BUTTON, __t, id=xrc.XRCID("cancel"))
    dialog.Bind(wx.EVT_BUTTON, __t, id=xrc.XRCID("ok"))
    
    ans = dialog.ShowModal()
    dialog.Destroy()
    if ans == wx.ID_OK:
        requiresReboot = ["language"]
        for key in ["verbose", "language", "plotdelay"]:
            __t = self.model.set("settings", key, elems[key]())
            if __t and key in requiresReboot:
                wx.CallAfter(self.Reboot)


def init(ctrlr):
    frame = ctrlr.view["mainFrame"]
    
    ctrlr.OnMenuPreferences = MethodType(OnMenuPreferences, ctrlr)
    
    for handler,name in [(ctrlr.OnMenuPreferences, "menuPreferences"),
                         (lambda *args: frame.Close(), "menuQuit")]:
        frame.Bind(wx.EVT_MENU, handler, id=xrc.XRCID(name))
