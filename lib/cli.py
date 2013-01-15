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


import argparse


DESCRIPTION = """\
MVC: Model-View-Controller
Cross platform attempt using python2.7 + wxpython + pyinstaller"""


EPILOG = """\
authors:
    Filipe Funenga <filipe.funenga@ist.utl.pt>"""


def parseCLI():
    
    parser = argparse.ArgumentParser(
            description=DESCRIPTION, epilog=EPILOG,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', '--settings-verbose', action='count',
                        help="define the minimum verbosity level: the "\
                             "default value is WARNING; '-v' is INFO; "\
                             "'-vv' is DEBUG. This value can be "\
                             "defined in the configuration file. "\
                             "All levels (sorted): [DEBUG, INFO, "\
                             "WARNING, ERROR, CRITICAL]")
    parser.add_argument("--settings-language-iso3", "-lang",
                        metavar="LANG",
                        help="define the language to be used in ISO3 "\
                             "country code. examples: -lang PRT, "\
                             "-lang GRB")
    return vars(parser.parse_args())

