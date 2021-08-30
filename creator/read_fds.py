# -*- coding: utf-8 -*-
import re

def get_fds_name(filename):
    return filename.replace(".fds", "")

def get_chid(fds):
    f = open("{}.fds".format(fds), 'r')
    data = f.read().replace(' ', '')
    f.close()
    
    try:
        return re.search("&HEADCHID='([a-zA-Z0-9]*)'", data).group(1)
    except ValueError:
        return ""

def create_ssf(chid):
    buf = "RENDERDIR\n .\n"
    buf += "LOADFILE\n {}_01.s3d\n".format(chid)
    buf += "LOADFILE\n {}_02.s3d\n".format(chid)
    buf += "RENDERALL\n 1\n\n"
    
    f = open("{}.ssf".format(chid), 'w')
    f.write(buf)
    f.close()

def create_ssf_with_evac(chid):
    buf = "RENDERDIR\n .\n"
    buf += "LOADFILE\n {}_01.s3d\n".format(chid)
    buf += "LOADFILE\n {}_02.s3d\n".format(chid)
    buf += "LOADFILE\n {}_0001.prt5\n".format(chid)
    buf += "RENDERALL\n 1\n\n"
    
    f = open("{}.ssf".format(chid), 'w')
    f.write(buf)
    f.close()

def create_ini(fds, chid):
    fr = open("sample.ini", 'r')
    fw = open("{}.ini".format(chid), 'w')
    
    data = fr.read()
    data = data.replace('sample_fds', fds)
    data = data.replace('sample_script', chid)
    
    fw.write(data)
    fw.close()
    fr.close()
    
def create_ssf_and_ini(filename):
    fdsname = get_fds_name(filename)
    chid = get_chid(fdsname)
    create_ssf(chid)
    create_ini(fdsname, chid)

