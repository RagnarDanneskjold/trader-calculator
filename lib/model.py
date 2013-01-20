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


import logging as log
#from wx import CallAfter
# Note: In a multi-threaded application, the following construct should
#       be used when publishing some event:
#           CallAfter(self.publish, signal, args)
#       This allows the Model to launch threads for long running tasks
#       while the View/Controller keeps handling user events.


from lib.configs import Configuration
from lib.publisher import Publisher


class Model(Publisher):
    
    def __init__(self, version):
        Publisher.__init__(self)
        
        self.conf = Configuration(version)
        self.lastfocus = None
        self.unknown = None
        self.nav = {"bo":"bs", "bs":"lo", "lo":"ls", "ls":"bo"}
        self.index3 = {(True,True,True,False): ("ls", self.__calcLS),
                       (True,True,False,True): ("lo", self.__calcLO),
                       (True,False,True,True): ("bs", self.__calcBS),
                       (False,True,True,True): ("bo", self.__calcBO)}
    
    def shutdown(self):
        self.conf.write()
    
    def set(self, section, label, sett):
        sett = self.conf.parse(section, label, sett)
        if self.conf[section][label] != sett:
            log.debug("set %s.%s=%s",section, label, str(sett))
            self.conf[section][label] = sett
            return True
        return False
    
    def isUnknown(self, name):
        return self.unknown and name == self.unknown[0]
    
    def guessUnknown(self, vals):
        flags = (vals.get("bo",-1)>0,vals.get("bs",-1)>0,
                 vals.get("lo",-1)>0,vals.get("ls",-1)>0)
        self.unknown = self.index3[flags]
        self.publish("guess unknown", self.unknown[0])
        log.debug("unknown was guessed to '%s'", self.unknown[0])
    
    def calculate(self, tbFrom, params, vals):
        if self.unknown is None: return
        beta = (1.0+params["bias"])/(1.0-params["bias"])
        val = self.unknown[-1](vals, beta)
        log.debug("unknown was updated to %.02f", val)
    
    def __calcLS(self, vals, beta):
        ob,sb,ol = vals["bo"],vals["bs"],vals["lo"]
        sl = sb*(ob+beta-1)/(ol+beta-1)
        self.publish("ls", sl)
        return sl
    
    def __calcLO(self, vals, beta):
        ob,sb,sl = vals["bo"],vals["bs"],vals["ls"]
        ol = ((sb/sl)*(ob+beta-1))-(beta-1) if sl!=0.0 else "inf"
        self.publish("lo", ol)
        return ol
    
    def __calcBS(self, vals, beta):
        ob,sl,ol = vals["bo"],vals["ls"],vals["lo"]
        sb = sl*(ol+beta-1)/(ob+beta-1)
        self.publish("bs", sb)
        return sb
    
    def __calcBO(self, vals, beta):
        sb,ol,sl = vals["bs"],vals["lo"],vals["ls"]
        ob = ((sl/sb)*(ol+beta-1))-(beta-1) if sb!=0.0 else "inf"
        self.publish("bo", ob)
        return ob
    
    def setUnknown(self, new):
        new = [nm for nm in self.index3.itervalues() if nm[0] == new][0]
        old = self.unknown[0] if self.unknown else self.nav[new[0]]
        self.unknown = new
        self.publish("set unknown", old, new[0])
        log.debug("unknown was setted to '%s'", self.unknown[0])
    
    def clear(self):
        if self.unknown:
            self.publish("set unknown", self.unknown[0], None)
        self.lastfocus = None
        self.unknown = None
