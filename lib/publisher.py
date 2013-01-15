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


class Publisher:
    
    def __init__(self):
        self.connections = {}
    
    def unsubscribe(self, handler, signal):
        handlers = self.connections.get(signal)
        if not handlers:
            return
        if handlers.get(id(handler)):
            del handlers[id(handler)]
        if handlers:
            self.connections[signal] = handlers
        else:
            del self.connections[signal]
    
    def subscribe(self, handler, signal):
        handlers = self.connections.get(signal, {})
        handlers[id(handler)] = handler
        self.connections[signal] = handlers
    
    def publish(self, signal, *args):
        for handler in self.connections.get(signal,{}).itervalues():
            handler(*args)
