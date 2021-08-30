#!/SYSTEM/Python/3.6.3/bin/python3
#!/SYSTEM/FDS/FDS6/bin/fds

import re
import getopt
import sys, os
import subprocess


try:
      opts, args = getopt.getopt(sys.argv[1:],"i:" ,["inp="])
except getopt.GetoptError as err:
      print(str(err))
      sys.exit(1)

for opt,arg in opts:
      if  opt in ("-i", "--inp"):
            f_inputdeck = open(arg, "r")
inputdeck_lines = f_inputdeck.readlines()
f_inputdeck.close()

matl = "&MATL "
for line in inputdeck_lines:
      opt  = line.split(' = ')[0]
      if opt in "material_name":
            material_name = line.split(' = ')[1].rstrip('\n')
            matl += "ID                    = '{}'\n".format(material_name)
      elif opt in "conductivity":
            conductivity = line.split(' = ')[1].rstrip('\n')
            matl += "      CONDUCTIVITY          = {}\n".format(conductivity)
      elif opt in "density":
            density = line.split(' = ')[1].rstrip('\n')
            matl += "      DENSITY               = {}\n".format(density)
      elif opt in "specific_heat":
            specific_heat = line.split(' = ')[1].rstrip('\n')
            matl += "      SPECIFIC_HEAT         = {}\n".format(specific_heat)
      else:
            print("error")
            sys.exit(1)
matl = matl.rstrip('\n')+"/\n"

head = "&HEAD CHID='sample', TITLE='Material Format' /\n"
mesh = "&MESH IJK=20,20,40, XB=0.0,1.0,0.0,1.0,0.0,2.0 /\n"
time = "&TIME T_END=10. /\n"
misc = "&MISC TMPA=20. /\n"
reac = "&REAC SOOT_YIELD=0.01,FUEL='PROPANE'/\n"
surf = "&SURF ID             = 'TEST_SURF'\n" \
       "      COLOR          = 'PURPLE'\n" \
       "      BURN_AWAY      = .TRUE.\n" \
       "      MATL_ID        = '{}'\n" \
       "      THICKNESS      = 0.02  /\n".format(material_name)
fire_surf = "&SURF ID        = 'FIRE'\n" \
            "      HRRPUA    = 1000.0\n" \
            "      COLOR     = 'RED' /\n"
obst = "&OBST XB             = 0.4, 0.6, 0.4, 0.6, 0.1, 0.3\n" \
       "      SURF_ID        = 'TEST_SURF'/\n"
top_open = "&VENT MB         = 'ZMAX'\n" \
           "      SURF_ID    = 'OPEN' /\n"
fire = "&VENT XB             = 0.4, 0.6, 0.4, 0.6, 0.0, 0.0\n" \
       "      SURF_ID        = 'FIRE' /\n"
bndf = "&BNDF QUANTITY='RADIATIVE HEAT FLUX' /\n" \
       "&BNDF QUANTITY='CONVECTIVE HEAT FLUX' /\n" \
       "&BNDF QUANTITY='NET HEAT FLUX' /\n" \
       "&BNDF QUANTITY='WALL TEMPERATURE' /\n" \
       "&BNDF QUANTITY='BURNING RATE' /\n"
slcf = "&SLCF PBX=0.5, QUANTITY='TEMPERATURE',VECTOR=.TRUE., CELL_CENTERED=.TRUE. /\n" \
       "&SLCF PBX=0.5, QUANTITY='HRRPUV', CELL_CENTERED=.TRUE. /\n" \
       "&SLCF PBX=0.5, QUANTITY='RADIATION LOSS', CELL_CENTERED=.TRUE. /\n" \
       "&SLCF PBY=0.5, QUANTITY='TEMPERATURE',VECTOR=.TRUE., CELL_CENTERED=.TRUE. /\n" \
       "&SLCF PBY=0.5, QUANTITY='HRRPUV', CELL_CENTERED=.TRUE. /\n" \
       "&SLCF PBY=0.5, QUANTITY='RADIATION LOSS', CELL_CENTERED=.TRUE. /\n"
tail = "&TAIL /"

sample = head + mesh + time + misc + reac + matl + surf + fire_surf + obst + top_open + fire + bndf + slcf + tail

os.system("rm -rf result")
os.system("mkdir result")
sample_out = open("result/sample.fds","w")
sample_out.write(sample)
sample_out.close()
matl_out = open("result/material.matl", "w")
matl_out.write(matl)
matl_out.close()

''' run fds '''
def create_ssf(chid):
    buf = "RENDERDIR\n .\n"
    buf += "LOADFILE\n {}_01.s3d\n".format(chid)
    buf += "LOADFILE\n {}_02.s3d\n".format(chid)
    buf += "LOADFILE\n {}_01.bf\n".format(chid)
    buf += "RENDERALL\n 1\n\n"
    
    f = open("result/{}.ssf".format(chid), 'w')
    f.write(buf)
    f.close()


def create_ini(fds, chid):
    fr = open("temp.ini", 'r')
    fw = open("result/{}.ini".format(chid), 'w')
    data = fr.read()
    data = data.replace('sample_fds', fds)
    data = data.replace('sample_script', chid)
    fw.write(data)
    fw.close()
    fr.close()


subprocess.call('fds sample.fds', shell=True, cwd='result/')

fdsname = "sample"
chid = "sample"
create_ini(fdsname, chid)
create_ssf(chid)

subprocess.call('xvfb-run --server-args "-screen 0 1280x800x16" smokeview -runscript {}'.format(chid), shell=True, cwd='result/')
subprocess.call('ffmpeg -r 20 -s 1280x800 -i {}_%04d.png -vcodec mpeg4 -y {}.mp4'.format(chid, chid), shell=True, cwd='result/')
subprocess.call('rm *.png', shell=True, cwd='result/')
