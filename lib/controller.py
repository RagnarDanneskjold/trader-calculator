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


import wxversion
wxversion.ensureMinimal('2.8')
import wx
import logging as log


from lib.langs import SetI18N
from lib.model import Model
# Note: Any method that is intended to subscribe the Model events, 
#       should use the following construct:
#           self.model.subscribe(receiver, signal)


class Controller(wx.App):
    
    def __init__(self, version):
        self.view = {}
        self.model = Model(version)
        wx.App.__init__(self, False)
    
    def OnInit(self):
        """
        Bind/Subscribe View/Model events to methods (handlers and
        subscribers, respectively).
        """
        
        # In order to minimize the number of lines in this file and
        # also to prevent the existence of an !infinite! list of
        # entangled unrelated methods, the definition of handlers and 
        # subscribers is made separetly inside the module 'lib.events'.
        #
        # Each script in the module is imported from here and the 
        # appropriate methods are can be attached to this instance of 
        # the class Controller in the following way:
        #     from types import MethodType
        #     self.handlerX = types.MethodType(handlerX, self)
        
        log.debug("setting i18n")
        self.i18n = SetI18N(self.model.conf["settings"]["language"],
                            self.model.conf["basedir"])
        
        # TODO: use importlib inside a loop
        
        log.info("loading handlers...")
        
        log.debug("setting up 'lib.handlers.frame'")
        from lib.handlers.frame import init
        init(self)
        
        log.debug("setting up 'lib.handlers.menu_calculator'")
        from lib.handlers.menu_calculator import init
        init(self)
        
        log.debug("setting up 'lib.handlers.menu_edit'")
        from lib.handlers.menu_edit import init
        init(self)
        
        log.debug("setting up 'lib.handlers.menu_plot'")
        from lib.handlers.menu_plot import init
        init(self)
        
        log.debug("setting up 'lib.handlers.menu_help'")
        from lib.handlers.menu_help import init
        init(self)
        
        log.debug("setting up 'lib.handlers.menu_updates'")
        from lib.handlers.menu_updates import init
        init(self)
        
        log.debug("setting up 'lib.handlers.textboxes_profits'")
        from lib.handlers.textboxes_profits import init
        init(self)
        
        log.debug("setting up 'lib.handlers.textboxes_parameters'")
        from lib.handlers.textboxes_parameters import init
        init(self)
        
        log.debug("setting up 'lib.handlers.textboxes_values'")
        from lib.handlers.textboxes_values import init
        init(self)
        
        log.debug("setting up 'lib.handlers.textboxes_evtchar'")
        from lib.handlers.textboxes_evtchar import init
        init(self)
        
        log.info("loading subscribers...")
        
        log.debug("setting up 'lib.subscribers.values'")
        from lib.subscribers.values import init
        init(self)
        
        log.debug("setting up 'lib.subscribers.profits'")
        from lib.subscribers.profits import init
        init(self)
        
        log.debug("setting up 'lib.subscribers.unknown'")
        from lib.subscribers.unknown import init
        init(self)
        
        log.debug("setting up 'lib.subscribers.plot'")
        from lib.subscribers.plot import init
        init(self)
        
        return True
    
    def OnExit(self):
        self.model.shutdown()
    
    def Reboot(self):
        self.isRebooting = True
        self.view["mainFrame"].Close()
