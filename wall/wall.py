#!/SYSTEM/Python/3.6.3/bin/python3
#!/SYSTEM/FDS/FDS6/bin/fds

import re
import getopt
import sys, os
import subprocess

try:
      opts, args = getopt.getopt(sys.argv[1:],"i:a:b:c:d:e:f:" ,["inp=","surf_1=","surf_2=","surf_3=","surf_4=","surf_5=","surf_6="])
except getopt.GetoptError as err:
      print(str(err))
      sys.exit(1)

surf_1_if = False
surf_2_if = False
surf_3_if = False
surf_4_if = False
surf_5_if = False
surf_6_if = False

for opt,arg in opts:
      if  opt in ("-i", "--inp"):
            f_inputdeck = open(arg, "r")
      elif opt in ("-a", "--surf_1"):
            f_input_surf_1 = open(arg, "r")
            input_surf_lines_1 = f_input_surf_1.readlines()
            f_input_surf_1.close()
            surf_1_if = True
      elif opt in ("-b", "--surf_2"):
            f_input_surf_2 = open(arg, "r")
            input_surf_lines_2 = f_input_surf_2.readlines()
            f_input_surf_2.close()
            surf_2_if = True
      elif opt in ("-c", "--surf_3"):
            f_input_surf_3 = open(arg, "r")
            input_surf_lines_3 = f_input_surf_3.readlines()
            f_input_surf_3.close()
            surf_3_if = True
      elif opt in ("-d", "--surf_4"):
            f_input_surf_4 = open(arg, "r")
            input_surf_lines_4 = f_input_surf_4.readlines()
            f_input_surf_4.close()
            surf_4_if = True
      elif opt in ("-e", "--surf_5"):
            f_input_surf_5 = open(arg, "r")
            input_surf_lines_5 = f_input_surf_5.readlines()
            f_input_surf_5.close()
            surf_5_if = True
      elif opt in ("-f", "--surf_6"):
            f_input_surf_6 = open(arg, "r")
            input_surf_lines_6 = f_input_surf_6.readlines()
            f_input_surf_6.close()
            surf_6_if = True

inputdeck_lines = f_inputdeck.readlines()
f_inputdeck.close()



''' Make Obst Data '''

obst = ""
wall_door_num = 0
wall_window_num = 0
_x = 0
_y = 0
_w = 0
_l = 0
_z = 0
_h = 0

for line in inputdeck_lines:
      opt  = line.split(' = ')[0]
      if opt in "number_of_walls":
            number_of_walls = int(line.split(' = ')[1].rstrip('\n'))

for each in range(number_of_walls):
      for line in inputdeck_lines[1:]:
            opt  = line.split(' = ')[0]
            char = ord('a')

            # wall position, width, length
            if opt in "wall_%s_pos"%(chr(char + each)):
                  wall_pos=line.split(' = ')[1].rstrip('\n')[1:-1]
                  _x, _y, _w, _l = (float(s) for s in wall_pos.split(',')) 
                  pos = "{}, {}, {}, {}".format(_x, _x+_w, _y, _y+_l)
                  obst += "&OBST XB      = {}, ".format(pos)
            # if the wall has option, if not the height is 3
            if opt in "wall_%s_advance_opt"%(chr(char + each)):
                  wall_advance_opt = line.split(' = ')[1].rstrip('\n')
                  if wall_advance_opt is "0":
                        wall_advance_opt = False
                        obst += "0, 3/\n"
                  else:
                        wall_advance_opt = True
            # wall height
            if opt in "wall_%s_high"%(chr(char + each)):
                  if wall_advance_opt is True:
                        wall_high  = line.split(' = ')[1].rstrip('\n')[1:-1]
                        _z, _h = (float(s) for s in wall_high.split(','))
                        high = "{}, {}".format(_z, _z+_h)
                        obst += high + '\n'
            # material assign
            if opt in "wall_%s_surf"%(chr(char + each)):
                  if wall_advance_opt is True:
                        wall_surf  = line.split(' = ')[1].rstrip('\n')
                        obst += "      SURF_ID = '{}'\n".format(wall_surf)
            # color
            if opt in "wall_%s_rgb"%(chr(char + each)):
                  if wall_advance_opt is True:
                        wall_rgb = str(line.split(' = ')[1].rstrip('\n'))[1:-1]
                        obst += "      RGB     = {}/\n".format(wall_rgb) 

            # if the wall has door, 0 is non, 1 is horizontal direction, 2 is vertical direction.
            if opt in "wall_%s_door_opt"%(chr(char + each)):
                  wall_door_opt = line.split(' = ')[1].rstrip('\n')
            # number of doors
            if opt in "wall_%s_door_num"%(chr(char + each)):
                  wall_door_num  = int(line.split(' = ')[1].rstrip('\n'))
            # make a hole with the number of doors.
            for door in range(wall_door_num+1):
                  if opt in "wall_{}_door_{}".format(chr(char + each), door+1):
                        wall_hole  = line.split(' = ')[1].rstrip('\n')[1:-1]
                        #  _hs is the distance that the left side of the obj to the point
                        #  _hw is the width of the door
                        #  _hh is the height of the door
                        _hs,_hw,_hh = (float(s) for s in wall_hole.split(',')) 
                        if wall_door_opt in "1":
                              hole_pos = "{},{},{},{},{},{}".format(_x-1,_x+_w+1,_y+_hs,_y+_hs+_hw,_z-1,_z+_hh)
                              obst += "&HOLE XB      = {}/\n".format(hole_pos)
                        elif wall_door_opt in "2":
                              hole_pos = "{},{},{},{},{},{}".format(_x+_hs,_x+_hs+_hw,_y-1,_y+_l+1,_z-1, _z+_hh)
                              obst += "&HOLE XB      = {}/\n".format(hole_pos)

            # if the wall has window, 0 is non, 1 is horizontal direction, 2 is vertical direction.
            if opt in "wall_%s_window_opt"%(chr(char + each)):
                  wall_window_opt = line.split(' = ')[1].rstrip('\n')
            # number of window
            if opt in "wall_%s_window_num"%(chr(char + each)):
                  wall_window_num  = int(line.split(' = ')[1].rstrip('\n'))
            # make a hole with the number of window.
            for window in range(wall_window_num+1):
                  if opt in "wall_%s_window_%d" % (chr(char + each), window+1):
                        wall_hole  = line.split(' = ')[1].rstrip('\n')[1:-1]
                        _hs,_hw,_hz,_hh = (float(s) for s in wall_hole.split(','))
                        if wall_window_opt in "1":
                              hole_pos = "{},{},{},{},{},{}".format(_x-1,_x+_w+1,_y+_hs,_y+_hs+_hw,_z+_hz,_z+_hz+_hh)
                              obst += "&HOLE XB      = {}/\n".format(hole_pos)
                        elif wall_window_opt in "2":
                              hole_pos = "{},{},{},{},{},{}".format(_x+_hs,_x+_hs+_hw,_y-1,_y+_l+1,_z+_hz, _z+_hz+_hh)
                              obst += "&HOLE XB      = {}/\n".format(hole_pos)



''' Add Surf and Matl Data to the Obst '''

def append_matl(this_surf_line):
      this_matl = ""
      s_point = False
      for this_line in this_surf_line:
            if this_line[:5] == "&MATL":
                  s_point = True
            if s_point is True:
                  this_matl += this_line
            if this_line[-1] == "/" or this_line[-2] == "/":
                  s_point = False
                  this_matl += "\nhaha"
      this_list = this_matl.split('haha')[1:-1]
      return this_list

def append_surf(this_surf_line):
      this_surf = ""
      s_point = False
      for this_line in this_surf_line:
            if this_line[:5] == "&SURF":
                  s_point = True
            if s_point is True:
                  this_surf += this_line
            if this_line[-1] == "/" or this_line[-2] == "/":
                  s_point = False
      return this_surf

surf = ""
matl = ""
matl_list = []
if surf_1_if is True:
      surf += append_surf(input_surf_lines_1)
      matl_list += append_matl(input_surf_lines_1)
if surf_2_if is True:
      surf += append_surf(input_surf_lines_2)
      matl_list += append_matl(input_surf_lines_2)
if surf_3_if is True:
      surf += append_surf(input_surf_lines_3)
      matl_list += append_matl(input_surf_lines_3)
if surf_4_if is True:
      surf += append_surf(input_surf_lines_4)
      matl_list += append_matl(input_surf_lines_4)
if surf_5_if is True:
      surf += append_surf(input_surf_lines_5)
      matl_list += append_matl(input_surf_lines_5)
if surf_6_if is True:
      surf += append_surf(input_surf_lines_6)
      matl_list += append_matl(input_surf_lines_6)
for i in list(set(matl_list)):
    matl += i
obst += surf
obst += matl



''' Calculate Mesh XB and IJK '''

x_axis = []
y_axis = []
z_axis = []
resolution = 0.5

for line in obst.splitlines():
    if line[:5] == "&OBST":
        _x,_y,_w,_l,_z,_h = line.split(' = ')[1].rstrip('/').split(',')
        x_axis.append(float(_x))
        x_axis.append(float(_x)+float(_w))
        y_axis.append(float(_y))
        y_axis.append(float(_y)+float(_l))
        z_axis.append(float(_z))
        z_axis.append(float(_z)+float(_h))
x_min = min(x_axis)-5
x_max = max(x_axis)+5
y_min = min(y_axis)-5
y_max = max(y_axis)+5
z_min = min(z_axis)
z_max = max(z_axis)+5
_i = (x_max - x_min)/resolution
_j = (y_max - y_min)/resolution
_k = (z_max - z_min)/resolution



''' Body Data '''

head = "&HEAD CHID = 'sample', TITLE = 'Wall Format' /\n"
mesh = "&MESH IJK  = {},{},{}\n" \
       "      XB   = {},{},{},{},{},{}/\n".format(_i, _j, _k, x_min, x_max, y_min, y_max, z_min, z_max)
time = "&TIME T_END=5.0 /\n"
misc = "&MISC TMPA=20. /\n"
reac = "&REAC SOOT_YIELD=0.01,FUEL='PROPANE'/\n"
fire_surf = "&SURF ID        = 'FIRE'\n" \
            "      HRRPUA    = 1000.0\n" \
            "      COLOR     = 'RED' /\n"
fire = "&VENT XB             = 0.0, 0.1, 0.0, 0.1, 0.0, 0.0\n" \
       "      SURF_ID        = 'FIRE' /\n"
top_open = "&VENT MB         = 'ZMAX'\n" \
           "      SURF_ID    = 'OPEN' /\n" \
           "&VENT MB         = 'XMAX'\n" \
           "      SURF_ID    = 'OPEN' /\n" \
           "&VENT MB         = 'XMIN'\n" \
           "      SURF_ID    = 'OPEN' /\n" \
           "&VENT MB         = 'YMAX'\n" \
           "      SURF_ID    = 'OPEN' /\n" \
           "&VENT MB         = 'YMIN'\n" \
           "      SURF_ID    = 'OPEN' /\n"
tail = "&TAIL /"

sample = head + mesh + time + misc + reac + fire_surf + obst + top_open + fire + tail

print(sample)

os.system("rm -rf result")
os.system("mkdir result")
sample_out = open("result/sample.fds","w")
sample_out.write(sample)
sample_out.close()
surf_out = open("result/wall.obst", "w")
surf_out.write(obst)
surf_out.close()

''' run fds '''
def create_ssf(chid):
    buf = "RENDERDIR\n .\n"
    buf += "LOADFILE\n {}_01.s3d\n".format(chid)
    buf += "LOADFILE\n {}_02.s3d\n".format(chid)
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