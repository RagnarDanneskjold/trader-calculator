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


def OnMenuAbout(self, evt):
    description = (_("""\
Trader Calculator is an eficient tool for the 
betting exchange users. 

Features include optimized keyboard 
navigation, updated results on every 
keypress, setting of bias between back/lay 
profits and more.""")).decode("utf-8")
    
    licence = """\
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA."""
    
    info = wx.AboutDialogInfo()
    
    iconpath = os.path.join(*[self.model.conf["basedir"], "resources",
                              "icon", "trader-calculator.ico"])
    info.SetIcon(wx.Icon(iconpath, wx.BITMAP_TYPE_ICO))
    info.SetName(_("Trader Calculator"))
    info.SetVersion("0.1")
    info.SetDescription(description)
    info.SetCopyright("(C) 2012 Filipe Funenga")
    info.SetWebSite("http://ffunenga.github.com/traderCalculator")
    info.SetLicence(licence)
    info.AddDeveloper("Filipe Funenga <filipe.funenga@ist.utl.pt>")
    info.AddDeveloper("Miguel Veríssimo <miguel.verissimo@ist.utl.pt>")
    info.AddDocWriter('Filipe Funenga <filipe.funenga@ist.utl.pt>')
    info.AddArtist('The Tango Team <http://tango.freedesktop.org/>')
    info.AddTranslator("Filipe Funenga <filipe.funenga@ist.utl.pt>")
    
    wx.AboutBox(info)


def SetEmptyStatus(frame):
    try: CallAfter(frame.SetStatusText, "")
    except: pass


def OnMenuDocumentation(self, evt):
    from urllib import pathname2url
    from threading import Timer
    
    frame = self.view["mainFrame"]
    lang = self.model.conf["settings"]["language"]
    docspath = os.path.abspath(os.path.join(*[
            self.model.conf["docsdir"], "docs", lang, "index.html"]))
    try:
        with open(docspath, "r") as f:
            frame.SetStatusText("Opening webbrowser...")
            Timer(1.0, SetEmptyStatus, args=[frame]).start()
            wx.LaunchDefaultBrowser("file:"+pathname2url(docspath))
    except Exception as e:
        log.error("can't open the documentation: " + str(e))
        frame.SetStatusText("Can't open the documentation: " + str(e))


# TODO: as distribuições têm que ser publicadas com o tuplo 
#       (versão, os, arch) embutido no código.

#{('0.1', 'win7', 'x86'): 'https://www.box.com/s/3fakm7x292dpmdv4q200',
# ('0.1', 'linux', 'x64'): 'https://www.box.com/s/qc0qqh6nymvkfvmv8cg5'}
def OnMenuUpdates(self, evt):
    wx.MessageBox("Not implemented yet!",
                  style=wx.OK|wx.ICON_EXCLAMATION)


def init(ctrlr):
    frame = ctrlr.view["mainFrame"]
    
    ctrlr.OnMenuAbout = MethodType(OnMenuAbout, ctrlr)
    ctrlr.OnMenuDocumentation = MethodType(OnMenuDocumentation, ctrlr)
    ctrlr.OnMenuUpdates = MethodType(OnMenuUpdates, ctrlr)
    
    frame.Bind(wx.EVT_MENU, ctrlr.OnMenuAbout,
               id=xrc.XRCID("menuAbout"))
    frame.Bind(wx.EVT_MENU, ctrlr.OnMenuDocumentation,
               id=xrc.XRCID("menuDocumentation"))
    frame.Bind(wx.EVT_MENU, ctrlr.OnMenuUpdates,
               id=xrc.XRCID("menuCheckUpdate"))
