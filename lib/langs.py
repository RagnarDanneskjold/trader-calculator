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


import gettext
import os
import wx


locales = {
    "en": (wx.LANGUAGE_ENGLISH, "en_US.UTF-8", "English"),
    "pt": (wx.LANGUAGE_PORTUGUESE, "pt_PT.UTF-8", "Português")
}


def SetI18N(lang, basedir):
    langdir = os.path.join(basedir, "locale")
    
    # This allows the usage of gettext inside the application with the
    # function _("string to translate").
    transl = gettext.translation("trader_calculator", langdir, [lang])
    transl.install()
    
    # The following code will set the appropriate variables so that
    # the import of XRC code can be translated.
    wx.Locale.AddCatalogLookupPathPrefix(langdir)
    i18n = wx.Locale(locales[lang][0])
    i18n.AddCatalog("trader_calculator")
    
    # Do not forget to keep this object "alive". Example: keep it as an
    # attribute of the wx.App.
    return i18n


def GetLanguages():
    keys = [k for k,v in locales.iteritems()]
    lbls = [v[-1].decode("utf-8") for k,v in locales.iteritems()]
    return keys,lbls
