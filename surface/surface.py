#!/SYSTEM/Python/3.6.3/bin/python3
#!/SYSTEM/FDS/FDS6/bin/fds

import re
import getopt
import sys, os
import subprocess


try:
      opts, args = getopt.getopt(sys.argv[1:],"i:a:b:c:d:e:f" ,["inp=","matl_1=","matl_2=","matl_3=","matl_4=","matl_5=","matl_6="])
except getopt.GetoptError as err:
      print(str(err))
      sys.exit(1)

matl_1_if = False
matl_2_if = False
matl_3_if = False
matl_4_if = False
matl_5_if = False
matl_6_if = False

for opt,arg in opts:
      if  opt in ("-i", "--inp"):
            f_inputdeck = open(arg, "r")
      elif opt in ("-a", "--matl_1"):
            f_input_matl_1 = open(arg, "r")
            input_matl_lines_1 = f_input_matl_1.readlines()
            f_input_matl_1.close()
            matl_1_if = True
      elif opt in ("-b", "--matl_2"):
            f_input_matl_2 = open(arg, "r")
            input_matl_lines_2 = f_input_matl_2.readlines()
            f_input_matl_2.close()
            matl_2_if = True
      elif opt in ("-c", "--matl_3"):
            f_input_matl_3 = open(arg, "r")
            input_matl_lines_3 = f_input_matl_3.readlines()
            f_input_matl_3.close()
            matl_3_if = True
      elif opt in ("-d", "--matl_4"):
            f_input_matl_4 = open(arg, "r")
            input_matl_lines_4 = f_input_matl_4.readlines()
            f_input_matl_4.close()
            matl_4_if = True
      elif opt in ("-e", "--matl_5"):
            f_input_matl_5 = open(arg, "r")
            input_matl_lines_5 = f_input_matl_5.readlines()
            f_input_matl_5.close()
            matl_5_if = True
      elif opt in ("-f", "--matl_6"):
            f_input_matl_6 = open(arg, "r")
            input_matl_lines_6 = f_input_matl_6.readlines()
            f_input_matl_6.close()
            matl_6_if = True

inputdeck_lines = f_inputdeck.readlines()
f_inputdeck.close()

surf = "&SURF "
for line in inputdeck_lines:
      opt  = line.split(' = ')[0]
      if opt in "surface_name":
            surface_name = line.split(' = ')[1].rstrip('\n')
            surf += "ID                        = '{}'\n".format(surface_name)
      elif opt in "number_of_layers": 
            number_of_layers = int(line.split(' = ')[1].rstrip('\n'))
      # Layer 1
      elif opt in "layer_one_type": 
            layer_one_type = int(line.split(' = ')[1].rstrip('\n'))
      elif opt in "layer_one_material": 
            layer_one_material = line.split(' = ')[1].rstrip('\n')
            surf += "      MATL_ID(1,1)              = '{}'\n".format(layer_one_material)
      elif opt in "layer_one_material_A":
            layer_one_material_A = line.split(' = ')[1].rstrip('\n')
            surf += "      MATL_ID(1,1:2)            = '{}', ".format(layer_one_material_A)
      elif opt in "layer_one_material_B":
            layer_one_material_B = line.split(' = ')[1].rstrip('\n')
            surf += "'{}'\n".format(layer_one_material_B)
      elif opt in "layer_one_fraction":
            layer_one_fraction = float(line.split(' = ')[1].rstrip('\n'))
            surf += "      MATL_MASS_FRACTION(1,1:2) = {}, {}\n".format(layer_one_fraction, 1-layer_one_fraction)
      elif opt in "layer_one_thickness": 
            layer_one_thickness = float(line.split(' = ')[1].rstrip('\n'))
            surf += "      THICKNESS(1)              = {}\n".format(layer_one_thickness)
      # Layer 2 
      elif opt in "layer_two_type": 
            layer_two_type = int(line.split(' = ')[1].rstrip('\n'))
      elif opt in "layer_two_material":
            layer_two_material = line.split(' = ')[1].rstrip('\n')
            surf += "      MATL_ID(2,1)              = '{}'\n".format(layer_two_material)
      elif opt in "layer_two_material_A":
            layer_two_material_A = line.split(' = ')[1].rstrip('\n')
            surf += "      MATL_ID(2,1:2)            = '{}',".format(layer_two_material_A)
      elif opt in "layer_two_material_B":
            layer_two_material_B = line.split(' = ')[1].rstrip('\n')
            surf += "'{}'\n".format(layer_two_material_B)
      elif opt in "layer_two_fraction":
            layer_two_fraction = float(line.split(' = ')[1].rstrip('\n'))
            surf += "      MATL_MASS_FRACTION(2,1:2) = {}, {}\n".format(layer_two_fraction, 1-layer_two_fraction)
      elif opt in "layer_two_thickness":
            layer_two_thickness = float(line.split(' = ')[1].rstrip('\n'))
            surf += "      THICKNESS(2)              = {}\n".format(layer_two_thickness)
      # Layer 3 
      elif opt in "layer_three_type":
            layer_three_type = int(line.split(' = ')[1].rstrip('\n'))
      elif opt in "layer_three_material":
            layer_three_material = line.split(' = ')[1].rstrip('\n')
            surf += "      MATL_ID(3,1)              = '{}'\n".format(layer_three_material)
      elif opt in "layer_three_material_A":
            layer_three_material_A = line.split(' = ')[1].rstrip('\n')
            surf += "      MATL_ID(3,1:2)            = '{}', ".format(layer_three_material_A)
      elif opt in "layer_three_material_B":
            layer_three_material_B = line.split(' = ')[1].rstrip('\n')
            surf += "'{}'\n".format(layer_three_material_B)
      elif opt in "layer_three_fraction":
            layer_three_fraction = float(line.split(' = ')[1].rstrip('\n'))
            surf += "      MATL_MASS_FRACTION(3,1:2) = {}, {}\n".format(layer_three_fraction, 1-layer_three_fraction)
      elif opt in "layer_three_thickness": 
            layer_three_thickness = float(line.split(' = ')[1].rstrip('\n'))
            surf += "      THICKNESS(3)              = {}\n".format(layer_three_thickness)
      else:
            print("error")
            sys.exit(1)
surf = surf.rstrip('\n')+"/\n"

matl = ""
if matl_1_if is True:
      for line in input_matl_lines_1:
            matl += line
if matl_2_if is True:
      for line in input_matl_lines_2:
            matl += line
if matl_3_if is True:
      for line in input_matl_lines_3:
            matl += line
if matl_4_if is True:
      for line in input_matl_lines_4:
            matl += line
if matl_5_if is True:
      for line in input_matl_lines_5:
            matl += line
if matl_6_if is True:
      for line in input_matl_lines_6:
            matl += line

surf += matl

head = "&HEAD CHID='sample', TITLE='Surface Format' /\n"
mesh = "&MESH IJK=20,20,40, XB=0.0,1.0,0.0,1.0,0.0,2.0 /\n"
time = "&TIME T_END=10. /\n"
misc = "&MISC TMPA=20. /\n"
reac = "&REAC SOOT_YIELD=0.01,FUEL='PROPANE'/\n"
fire_surf = "&SURF ID        = 'FIRE'\n" \
            "      HRRPUA    = 1000.0\n" \
            "      COLOR     = 'RED' /\n"
obst = "&OBST XB             = 0.4, 0.6, 0.4, 0.6, 0.1, 0.3\n" \
       "      SURF_ID        = '{}'/\n".format(surface_name)
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

sample = head + mesh + time + misc + reac + surf + fire_surf + obst + top_open + fire + bndf + slcf + tail
print(sample)


os.system("rm -rf result")
os.system("mkdir result")
sample_out = open("result/sample.fds","w")
sample_out.write(sample)
sample_out.close()
surf_out = open("result/surface.surf", "w")
surf_out.write(surf)
surf_out.close()

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