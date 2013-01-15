# -*- mode: python -*-


#PyInstaller can be downloaded at:
#wget http://sourceforge.net/projects/pyinstaller/files/2.0/pyinstaller-2.0.tar.bz2/download
#unzip pyinstaller-2.0.zip
#Check for new versions before downloading.
#Update this file if needed.
#
#On windows:
#    python pyinstaller.py --onedir main\main.spec
#On linux:
#    ./pyinstaller.py --onedir main/main.spec


import os


def osNormalizePath(path):
    """ this function only works for relative paths """
    parts = path.split('/')
    return os.path.abspath(os.path.join(*parts))


def create_datafile(path, strip_path=True):
    name = path
    if strip_path:
        name = os.path.basename(path)
    return name, path, 'DATA'


mainscriptPath = osNormalizePath('../main.py')


if os.name == "posix":
    execPath = os.path.join('build/pyi.linux2/main',
                            'trader-calculator')
elif os.name == "nt":
    execPath = os.path.join('build\\pyi.win32\\main', 
                            'trader-calculator.exe')


dfiles = ["../AUTHORS","../README.md","../COPYING"]
dfiles = TOC([create_datafile(osNormalizePath(dfile))
              for dfile in dfiles])


print " os.name:", os.name
print "mainPath:", mainscriptPath
print "execPath:", execPath
if dfiles:
    print "datafiles:"
    for dfile in dfiles:
        print "   ", dfile

a = Analysis([mainscriptPath])
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, exclude_binaries=1,
          debug=False, strip=None, upx=True, console=False, 
          icon="../lib/resources/icon/trader-calculator_512x512x32.png", 
          name=execPath)
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, dfiles, strip=None,
               upx=True, name=os.path.join('dist', 'main'))
