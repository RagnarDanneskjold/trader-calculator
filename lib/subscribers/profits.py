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


def UpdateProfits(self, val):
    try:
        tctrls = [self.view[k] for k in ["bs","bo","ls","lo"]]
        sb,ob,sl,ol = (float(tc.GetValue()) for tc in tctrls)
        
        comm = self.model.conf["parameters"]["commission"]
        HouseFunction = lambda h,x: x if x<0 else x*(1.-h)
        pTrue = HouseFunction(comm,((ob-1.)*sb) + ((1.-ol)*sl))
        pFalse = HouseFunction(comm,(sl-sb))
        for key,p in [("bp", pTrue), ("lp", pFalse)]:
            self.view[key].ChangeValue("%.02f"%p)
            clr = "#0B8600" if p>=0 else "red"
            self.view[key].SetForegroundColour(clr)
            self.view[key].Refresh()
    except:
        for key in ["bp","lp"]:
            self.view[key].ChangeValue("")
            self.view[key].Refresh()


def init(ctrlr):
    frame = ctrlr.view["mainFrame"]
    
    ctrlr.UpdateProfits = MethodType(UpdateProfits, ctrlr)
    
    for sig in ["ls", "lo", "bs", "bo"]:
        ctrlr.model.subscribe(ctrlr.UpdateProfits, sig)
