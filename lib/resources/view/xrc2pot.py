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
from subprocess import check_output as xgettext
from xml.etree import ElementTree


def extractMsgs(filename):
    tree = ElementTree.parse(filename).getroot()
    tags = ['.//{http://www.wxwindows.org/wxxrc}label',
            './/{http://www.wxwindows.org/wxxrc}title',
            './/{http://www.wxwindows.org/wxxrc}help']
    r = []
    [r.append(e.text) for t in tags for e in tree.findall(t)
                                    if e not in r]
    return r


def main():
    viewpath = os.getcwd()
    librpath = os.path.abspath(os.path.join(viewpath, "..", ".."))
    
    # Collects translatable strings from the source code on parent
    # folders with depth-first search algorithm.
    args = ["xgettext", "-o", "-", "../../../main.py"]
    queue = [librpath]
    while queue:
        path = queue.pop(-1)
        for i in os.listdir(path):
            i = os.path.join(librpath, i)
            if (os.path.isdir(i) and
                os.path.relpath(i) not in [".", "../../locale"]):
                queue.append(i)
        args += [os.path.relpath(os.path.join(path, fn))
                  for fn in os.listdir(path) if fn[-3:]==".py"]
    
    try:
        output = xgettext(args)
    except:
        print "error: xgettext is not installed"
        exit(1)
    
    lines = [line for line in output.split("\n") if line[:1] != "#"]
    
    # Removes the first item (project header, etc)
    idx = 0
    for idx in range(len(lines)):
        if lines[idx] == '"Content-Transfer-Encoding: 8bit\\n"':
            break
    lines = lines[idx+2:]
    
    # Collects translatable strings from all the xrc files in the
    # same path of __file__.
    filenames = [fn for fn in os.listdir(viewpath) if fn[-4:] == ".xrc"]
    msgs = [line[7:-1] for line in lines if line[:7] == 'msgid "']
    for fn in filenames:
        for msg in extractMsgs(fn):
            if msg not in msgs:
                lines.append('msgid "%s"'%msg)
                lines.append('msgstr ""\n')
    
    # write output to the appropriate .pot file
    outfn = os.path.join(librpath, "locale", fn[:-4]+".pot")
    with open(outfn, "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
