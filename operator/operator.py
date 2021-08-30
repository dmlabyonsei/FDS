#!/SYSTEM/Python/3.6.3/bin/python3
#!/SYSTEM/FDS/FDS6/bin/fds

import re
import getopt
import sys, os
import subprocess

try:
      opts, args = getopt.getopt(sys.argv[1:],"i:a:b:c:d:e:f:" ,["inp=","obst_1=","obst_2=","obst_3=","obst_4=","obst_5=","obst_6="])
except getopt.GetoptError as err:
      print(str(err))
      sys.exit(1)

obst_1_if = False
obst_2_if = False
obst_3_if = False
obst_4_if = False
obst_5_if = False
obst_6_if = False

for opt,arg in opts:
      if  opt in ("-i", "--inp"):
            f_inputdeck = open(arg, "r")
            inputdeck_lines = f_inputdeck.readlines()
            f_inputdeck.close()
      elif opt in ("-a", "--obst_1"):
            f_input_obst_1 = open(arg, "r")
            input_obst_lines_1 = f_input_obst_1.readlines()
            f_input_obst_1.close()
            obst_1_if = True
      elif opt in ("-b", "--obst_2"):
            f_input_obst_2 = open(arg, "r")
            input_obst_lines_2 = f_input_obst_2.readlines()
            f_input_obst_2.close()
            obst_2_if = True
      elif opt in ("-c", "--obst_3"):
            f_input_obst_3 = open(arg, "r")
            input_obst_lines_3 = f_input_obst_3.readlines()
            f_input_obst_3.close()
            obst_3_if = True
      elif opt in ("-d", "--obst_4"):
            f_input_obst_4 = open(arg, "r")
            input_obst_lines_4 = f_input_obst_4.readlines()
            f_input_obst_4.close()
            obst_4_if = True
      elif opt in ("-e", "--obst_5"):
            f_input_obst_5 = open(arg, "r")
            input_obst_lines_5 = f_input_obst_5.readlines()
            f_input_obst_5.close()
            obst_5_if = True
      elif opt in ("-f", "--obst_6"):
            f_input_obst_6 = open(arg, "r")
            input_obst_lines_6 = f_input_obst_6.readlines()
            f_input_obst_6.close()
            obst_6_if = True


''' Operator Input Data '''
for line in inputdeck_lines:
      opt  = line.split(' = ')[0]
      if opt in "title":
            title = line.split(' = ')[1].rstrip('\n')
      elif opt in "resolution":
            resolution = float(line.split(' = ')[1].rstrip('\n'))
      elif opt in "fds_time":
            fds_time = float(line.split(' = ')[1].rstrip('\n'))
      elif opt in "fire_pos":
            fire_pos = line.split(' = ')[1].rstrip('\n')[1:-1]
            fx,fy,fw,fl = (float(s) for s in fire_pos.split(','))
      elif opt in "fire_height":
            fire_height = line.split(' = ')[1].rstrip('\n')[1:-1]
            fz,fh = (float(s) for s in fire_height.split(',')) 
      elif opt in "hrrpua":
            hrrpua = float(line.split(' = ')[1].rstrip('\n'))
      else:
            print("error")
            sys.exit(1)
''' End of Operator Input Data '''


''' Add Surf and Matl Data to the Obst '''
def append_matl(this_obst_line):
      this_matl = ""
      s_point = False
      for this_line in this_obst_line:
            if this_line[:5] == "&MATL":
                  s_point = True
            if s_point is True:
                  this_matl += this_line
            if this_line == "\n" or this_line == "":
                  continue
            else:
                  if this_line[-1]=="/" or this_line[-2]=="/":
                        s_point = False
                        this_matl = this_matl.rstrip('\n')
                        this_matl += "\nhaha"
      this_list = this_matl.split('haha')[1:-1]
      return this_list

def append_surf(this_obst_line):
      this_surf = ""
      s_point = False
      for this_line in this_obst_line:
            if this_line[:5] == "&SURF":
                  s_point = True
            if s_point is True:
                  this_surf += this_line
            if this_line == "\n" or this_line == "":
                  continue
            else:
                  if this_line[-1]=="/" or this_line[-2]=="/":
                        s_point = False
                        this_surf = this_surf.rstrip('\n')
                        this_surf += "\nhaha"
      this_list = this_surf.split('haha')[1:-1]
      return this_list

def append_obst(this_obst_line):
      this_obst = ""
      s_point = False
      for i, this_line in enumerate(this_obst_line):
            if this_line[:5] == "&OBST":
                  s_point = True
            if s_point is True:
                  this_obst += this_line
            if this_line is not this_obst_line[-1]:
                  if this_obst_line[i+1][:5] != "&HOLE":
                        if this_line == "\n" or this_line == "":
                              continue
                        else:
                              if this_line[-1]=="/" or this_line[-2]=="/":
                                    s_point = False
      return this_obst

obst = ""
surf = ""
matl = ""
surf_list = []
matl_list = []
if obst_1_if is True:
      obst += append_obst(input_obst_lines_1)
      surf_list += append_surf(input_obst_lines_1)
      matl_list += append_matl(input_obst_lines_1)
if obst_2_if is True:
      obst += append_obst(input_obst_lines_2)
      surf_list += append_surf(input_obst_lines_2)
      matl_list += append_matl(input_obst_lines_2)
if obst_3_if is True:
      obst += append_obst(input_obst_lines_3)
      surf_list += append_surf(input_obst_lines_3)
      matl_list += append_matl(input_obst_lines_3)
if obst_4_if is True:
      obst += append_obst(input_obst_lines_4)
      surf_list += append_surf(input_obst_lines_4)
      matl_list += append_matl(input_obst_lines_4)
if obst_5_if is True:
      obst += append_obst(input_obst_lines_5)
      surf_list += append_surf(input_obst_lines_5)
      matl_list += append_matl(input_obst_lines_5)
if obst_6_if is True:
      obst += append_obst(input_obst_lines_6)
      surf_list += append_surf(input_obst_lines_6)
      matl_list += append_matl(input_obst_lines_6)

matl_list = list(set(matl_list))
for i in matl_list:
      if i=="" or i=="\n":
            continue
      else:
            matl += i

surf_list = list(set(surf_list))
for i in surf_list:
      if i=="" or i=="\n":
            continue
      else:
            surf += i
obst += surf
obst += matl
''' End of Add Surf and Matl Data to the Obst '''


''' Calculate Mesh XB and IJK '''
x_axis = []
y_axis = []
z_axis = []
margine = 5
for line in obst.splitlines():
    if line[:5] == "&OBST":
        _x1,_x2,_y1,_y2,_z1,_z2 = line.split(' = ')[1].rstrip('/').split(',')
        x_axis.append(float(_x1))
        x_axis.append(float(_x2))
        y_axis.append(float(_y1))
        y_axis.append(float(_y2))
        z_axis.append(float(_z1))
        z_axis.append(float(_z2))
x_min = min(x_axis)-margine
x_max = max(x_axis)+margine
y_min = min(y_axis)-margine
y_max = max(y_axis)+margine
z_min = min(z_axis)
z_max = max(z_axis)
_i = (x_max - x_min)/resolution
_j = (y_max - y_min)/resolution
_k = (z_max - z_min)/resolution
''' End of Calculate Mesh XB and IJK '''


''' Change Negative Number to Positive Number '''
new_obst = ""
if x_min<0 and y_min<0:
      mesh_x_min = x_min + abs(x_min)
      mesh_x_max = x_max + abs(x_min)
      mesh_y_min = y_min + abs(y_min)
      mesh_y_max = y_max + abs(y_min)
      for line in obst.splitlines():
            if line[:5]=="&OBST":
                  _x1,_x2,_y1,_y2,_z1,_z2 = line.split(' = ')[1].rstrip('/').split(',')
                  _nx1 = float(_x1) + abs(x_min)
                  _nx2 = float(_x2) + abs(x_min)
                  _ny1 = float(_y1) + abs(y_min)
                  _ny2 = float(_y2) + abs(y_min)
                  _nz1 = float(_z1)
                  _nz2 = float(_z2)
                  new_obst = new_obst + "&OBST XB                        = {}, {}, {}, {}, {}, {}\n".format(_nx1,_nx2,_ny1,_ny2,_nz1,_nz2)
            elif line[:5]=="&HOLE":
                  _x1,_x2,_y1,_y2,_z1,_z2 = line.split(' = ')[1].rstrip('/').split(',')
                  _nx1 = float(_x1) + abs(x_min)
                  _nx2 = float(_x2) + abs(x_min)
                  _ny1 = float(_y1) + abs(y_min)
                  _ny2 = float(_y2) + abs(y_max)
                  _nz1 = float(_z1)
                  _nz2 = float(_z2)
                  new_obst = new_obst + "&HOLE XB                        = {}, {}, {}, {}, {}, {}/\n".format(_nx1,_nx2,_ny1,_ny2,_nz1,_nz2)
            else:
                  new_obst = new_obst + line + '\n'
      fire = "&OBST XB             = {}, {}, {}, {}, {}, {}\n" \
             "      SURF_ID        = 'FIRE' /\n".format(fx+abs(x_min),fx+fw+abs(x_min),fy+abs(y_min),fy+fl+abs(y_min),fz,fz+fh)
elif x_min<0 and y_min>0:
      mesh_x_min = x_min + abs(x_min)
      mesh_x_max = x_max + abs(x_min)
      mesh_y_min = y_min
      mesh_y_max = y_max
      for line in obst.splitlines():
            if line[:5]=="&OBST":
                  _x1,_x2,_y1,_y2,_z1,_z2 = line.split(' = ')[1].rstrip('/').split(',')
                  _nx1 = float(_x1) + abs(x_min)
                  _nx2 = float(_x2) + abs(x_min)
                  _ny1 = float(_y1)
                  _ny2 = float(_y2)
                  _nz1 = float(_z1)
                  _nz2 = float(_z2)
                  new_obst = new_obst + "&OBST XB                        = {}, {}, {}, {}, {}, {}\n".format(_nx1,_nx2,_ny1,_ny2,_nz1,_nz2)
            elif line[:5]=="&HOLE":
                  _x1,_x2,_y1,_y2,_z1,_z2 = line.split(' = ')[1].rstrip('/').split(',')
                  _nx1 = float(_x1) + abs(x_min)
                  _nx2 = float(_x2) + abs(x_min)
                  _ny1 = float(_y1)
                  _ny2 = float(_y2)
                  _nz1 = float(_z1)
                  _nz2 = float(_z2)
                  new_obst = new_obst + "&HOLE XB                        = {}, {}, {}, {}, {}, {}/\n".format(_nx1,_nx2,_ny1,_ny2,_nz1,_nz2)
            else:
                  new_obst = new_obst + line + '\n'
      fire = "&OBST XB             = {}, {}, {}, {}, {}, {}\n" \
             "      SURF_ID        = 'FIRE' /\n".format(fx+abs(x_min),fx+fw+abs(x_min),fy,fy+fl,fz,fz+fh)
elif x_min>0 and y_min<0:
      mesh_x_min = x_min
      mesh_x_max = x_max
      mesh_y_min = y_min + abs(y_min)
      mesh_y_max = y_max + abs(y_min)
      for line in obst.splitlines():
            if line[:5]=="&OBST":
                  _x1,_x2,_y1,_y2,_z1,_z2 = line.split(' = ')[1].rstrip('/').split(',')
                  _ny1 = float(_y1)
                  _ny2 = float(_y2)
                  _ny1 = float(_y1) + abs(y_min)
                  _ny2 = float(_y2) + abs(y_min)
                  _nz1 = float(_z1)
                  _nz2 = float(_z2)
                  new_obst = new_obst + "&OBST XB                        = {}, {}, {}, {}, {}, {}\n".format(_nx1,_nx2,_ny1,_ny2,_nz1,_nz2)
            elif line[:5]=="&HOLE":
                  _x1,_x2,_y1,_y2,_z1,_z2 = line.split(' = ')[1].rstrip('/').split(',')
                  _nx1 = float(_x1)
                  _nx2 = float(_x2)
                  _ny1 = float(_y1) + abs(y_min)
                  _ny2 = float(_y2) + abs(y_max)
                  _nz1 = float(_z1)
                  _nz2 = float(_z2)
                  new_obst = new_obst + "&HOLE XB                        = {}, {}, {}, {}, {}, {}/\n".format(_nx1,_nx2,_ny1,_ny2,_nz1,_nz2)
            else:
                  new_obst = new_obst + line + '\n'
      fire = "&OBST XB             = {}, {}, {}, {}, {}, {}\n" \
             "      SURF_ID        = 'FIRE' /\n".format(fx,fx+fw,fy+abs(y_min),fy+fl+abs(y_min),fz,fz+fh)
else: 
      mesh_x_min = x_min
      mesh_x_max = x_max
      mesh_y_min = y_min
      mesh_y_max = y_max
      new_obst = obst
''' End of Change Negative Number to Positive Number '''


''' Body Data '''
head = "&HEAD CHID = 'sample', TITLE = '{}' /\n".format(title)
mesh = "&MESH IJK  = {},{},{}\n" \
       "      XB   = {},{},{},{},{},{}/\n".format(_i, _j, _k, mesh_x_min, mesh_x_max, mesh_y_min, mesh_y_max, z_min, z_max)
time = "&TIME T_END={} /\n".format(fds_time)
misc = "&MISC TMPA=20. /\n"
reac = "&REAC SOOT_YIELD=0.01, FUEL='PROPANE'/\n"
fire_surf = "&SURF ID        = 'FIRE'\n" \
            "      HRRPUA    = {}\n" \
            "      COLOR     = 'RED' /\n".format(hrrpua)
# top_open = "&VENT MB         = 'ZMAX'\n" \
#            "      SURF_ID    = 'OPEN' /\n" \
#            "&VENT MB         = 'XMAX'\n" \
#            "      SURF_ID    = 'OPEN' /\n" \
#            "&VENT MB         = 'XMIN'\n" \
#            "      SURF_ID    = 'OPEN' /\n" \
#            "&VENT MB         = 'YMAX'\n" \
#            "      SURF_ID    = 'OPEN' /\n" \
#            "&VENT MB         = 'YMIN'\n" \
#            "      SURF_ID    = 'OPEN' /\n"
slcf = "&SLCF PBZ=1.5, QUANTITY='TEMPERATURE',VECTOR=.TRUE., CELL_CENTERED=.TRUE. /\n" \
       "&SLCF PBZ=1.5, QUANTITY='HRRPUV', CELL_CENTERED=.TRUE. /\n" \
       "&SLCF PBZ=1.5, QUANTITY='RADIATION LOSS', CELL_CENTERED=.TRUE. /\n"
tail = "&TAIL /"
sample = head+mesh+time+misc+reac+fire_surf+new_obst+fire+slcf+tail
print(sample)


''' Save FDS Data '''
os.system("rm -rf result")
os.system("mkdir result")
sample_out = open("result/sample.fds","w")
sample_out.write(sample)
sample_out.close()
''' End of Save FDS Data '''


''' Run FDS '''
def create_ssf(chid):
    buf = "RENDERDIR\n .\n"
    buf += "LOADFILE\n {}_01.s3d\n".format(chid)
    buf += "LOADFILE\n {}_02.s3d\n".format(chid)
    buf += "LOADFILE\n {}_05.sf\n".format(chid)
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

subprocess.call('xvfb-run -s "-screen 0 1280x800x24" smokeview -runscript sample', shell=True, cwd='result/')
subprocess.call('ffmpeg -r 20 -s 1280x800 -i sample_%04d.png -vcodec mpeg4 -y sample.mp4', shell=True, cwd='result/')
subprocess.call('rm *.png', shell=True, cwd='result/')
''' End of Run FDS '''