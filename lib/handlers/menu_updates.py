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
from wx import CallAfter
import logging as log
import urllib
from threading import Thread


class DownloadLinks:
    def __init__(self, dialog, url, version):
        self.dia = dialog
        self.gau = xrc.XRCCTRL(dialog, "gauge")
        self.chk = xrc.XRCCTRL(dialog, "check")
        self.ins = xrc.XRCCTRL(dialog, "download")
        self.sta = xrc.XRCCTRL(dialog, "status")
        self.url = xrc.XRCCTRL(dialog, "url")
        self.url.SetValue(url)
        self.version = version
        self.download = None
        
        self.stop = False
        
        dialog.Bind(wx.EVT_BUTTON, self.OnCheck, id=xrc.XRCID("check"))
        dialog.Bind(wx.EVT_BUTTON, self.OnDownload,
                    id=xrc.XRCID("download"))
    
    def OnCheck(self, evt):
        self.url.Enable(False)
        self.chk.Enable(False)
        self.ins.Enable(False)
        t = Thread(target=self.CheckUpdates)
        t.daemon = True
        t.start()
    
    def EnableSomeElements(self, msg):
        self.sta.SetLabel(msg)
        self.gau.SetValue(0)
        self.url.Enable(True)
        self.chk.Enable(True)
        self.dia.Layout()
    
    def CheckUpdates(self):
        f = urllib.urlopen(self.url.GetValue())
        if self.stop: return
        CallAfter(self.gau.SetValue, 33)
        CallAfter(self.dia.Refresh)
        
        links = f.read()
        if self.stop: return
        CallAfter(self.gau.SetValue, 66)
        CallAfter(self.dia.Refresh)
        
        try:
            links = eval(links)
            if self.stop: return
            CallAfter(self.gau.SetValue, 99)
            CallAfter(self.dia.Refresh)
        except:
            if self.stop: return
            CallAfter(self.EnableSomeElements,
                      _("(Manifest not found!)"))
            CallAfter(self.dia.Layout)
            return
        
        for ver,os,arch,url in links:
            if (os,arch) == self.version[1:]:
                if float(ver)>float(self.version[0]):
                    self.download = url
                    if self.stop: return
                    CallAfter(self.ins.Enable, True)
                    CallAfter(self.EnableSomeElements,
                              _("(Update available!)"))
                    CallAfter(self.dia.Layout)
                    return
        
        if self.stop: return
        CallAfter(self.EnableSomeElements,
                  _("(At the lastest version. Nice!)"))
        CallAfter(self.dia.Layout)
    
    def OnDownload(self, evt):
        wx.LaunchDefaultBrowser(self.download)
        self.dia.Close()


def OnMenuUpdates(self, evt):
    dia = self.view["xrc"].LoadDialog(
            self.view["mainFrame"], "updateDialog")
    down = DownloadLinks(dia, self.model.conf["updates"],
                         self.model.conf["version"])
    dia.ShowModal()
    down.stop = True
    dia.Destroy()


def init(ctrlr):
    frame = ctrlr.view["mainFrame"]
    
    ctrlr.OnMenuUpdates = MethodType(OnMenuUpdates, ctrlr)
    
    frame.Bind(wx.EVT_MENU, ctrlr.OnMenuUpdates,
               id=xrc.XRCID("menuCheckUpdate"))
