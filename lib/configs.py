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


import sys
import os
import json
import logging as log
from pprint import pformat


from lib.cli import parseCLI


UPDATES_LINK = "http://ffunenga.github.com/trader-calculator/updates"
if getattr(sys, 'frozen', None): #compatible with pyinstaller
    BASEPATH = sys._MEIPASS
    DOCS_PATH = BASEPATH
else:
    BASEPATH = os.path.dirname(__file__)
    DOCS_PATH = os.path.abspath(os.path.join(BASEPATH,".."))
CONFIGFILE_PATH = os.path.join(BASEPATH, "configuration.json")


DEFAULT_CONFIG = {
    "basedir": BASEPATH,
    "docsdir": DOCS_PATH,
    "updates": UPDATES_LINK,
    "settings": {
        "size": (285,195),
        "verbose": 0,
        "language": "en"
    },
    "parameters": {
        "bias": 0.00,
        "commission": 0.05
    }
}


# self.conf is a dictionary that holds all the aplication
# settings that are saved/retrieve to/from a file between
# application utilizations.
class Configuration(dict):
    
    def __init__(self, version):
        self["version"] = version
        args = parseCLI()
        self.update(DEFAULT_CONFIG)
        try:
            self.__parseFile(args)
        except Exception as e:
            log.debug(e)
            log.warning("configuration file error, using defaults.")
            self.write()
        
        lvl = int(self["settings"]["verbose"])
        lvl = lvl if lvl in [0,1,2] else 0
        root = log.getLogger()
        root.setLevel([log.WARNING,log.INFO,log.DEBUG][lvl])
    
    def parse(self, section, label, val):
        if self.get(section) is None:
            log.critical("unrecognized section '%s'", section)
            raise Exception("unrecognized section '%s'"%section)
        
        if label not in self[section]:
            log.critical("unrecognized label '%s.%s'", section, label)
            raise Exception("unrecognized label '%s'"%label)
        
        if section == "settings":
            if label == "size":
                val = tuple(val)
            elif label == "verbose":
                val = str(val)
                val = int(0 if val == "" else val)
                assert val in [0,1,2]
            elif label == "language":
                assert type(val) is str and val in ["en", "pt"]
            else:
                log.warning("'%s.%s' not parsed", section, label)
        elif section == "parameters":
            val = str(val)
            if label == "bias":
                val = float(val)
                assert val > -1.0 and val < 1.0
            elif label == "commission":
                val = float(val)
                assert val >= 0.0 and val <= 1.0
            else:
                log.warning("'%s.%s' not parsed", section, label)
        else:
            log.warning("'%s.%s=%s' not parsed", section, label,
                                                 str(param))
        return val
    
    def __parseFile(self, args):
        if args["settings_verbose"]:
            log.info("parsing configuration file...")
        
        # The configuration file is a json formated textfile where every
        # valued item exists at depth 2 of nested dictionaries. This 
        # restriction entails that every item in depth 1 (a "section")
        # is a dict object.
        
        with open(CONFIGFILE_PATH) as f:
            conf = json.load(f)
        
        for sec,items in conf.iteritems():
            if self.get(sec) is None:
                self.warning("config item '%s' not recognized", sec)
            if type(items) is not dict:
                self.error("config item '%s' is not dict.", sec)
                continue
            for item,value in items.iteritems():
                self[sec][item] = value
        
        for k,v in args.iteritems():
            k = k.split("_")
            if len(k) is 1 and v is not None:
                config[k[0]] = v
            elif v is not None:
                self[k[0]][k[1]] = v
    
    def write(self):
        log.info("saving configfile")
        try:
            __t = {s:i for s,i in self.iteritems() if type(i) is dict}
            with open(CONFIGFILE_PATH, "w") as fp:
                json.dump(__t, fp, indent=4, sort_keys=True)
        except Exception as e:
            log.debug(str(e))
            log.error("configuration file error, not saved.")
