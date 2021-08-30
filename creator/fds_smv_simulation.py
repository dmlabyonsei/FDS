#!/SYSTEM/Python/3.6.3/bin/python3
#!/SYSTEM/FDS/FDS6/bin fds

import sys, os
import getopt
import subprocess
import read_fds

subprocess.call('rm -r result', shell=True)
subprocess.call('mkdir result', shell=True)

try:
      opts, args = getopt.getopt(sys.argv[1:],"i:" ,["inp="])
except getopt.GetoptError as err:
      f.write(str(err))
      print(str(err))
      sys.exit(1)

fds = ''
for opt,arg in opts:
      if  opt in ("-i", "--inp"):
            fds = arg

subprocess.call('fds {}'.format(fds), shell=True)

fdsname = read_fds.get_fds_name(fds)
chid = read_fds.get_chid(fdsname)
read_fds.create_ssf_with_evac(chid)
read_fds.create_ini(fdsname, chid)

subprocess.call('xvfb-run --server-args "-screen 0 1280x800x16" smokeview -runscript {}'.format(chid), shell=True)
subprocess.call('ffmpeg -r 20 -s 1280x800 -i {}_%04d.png -vcodec mpeg4 -y {}.mp4'.format(chid, chid), shell=True)

subprocess.call('rm *.png', shell=True)
subprocess.call('mv *.mp4 result', shell=True)

