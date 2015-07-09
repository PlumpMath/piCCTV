from os import system
from sys import argv

if not 2 <= len(argv)<= 3:
  print('example: {} 192.168.0.15 "2015\ 05\ 18-22*"'.format(argv[0]))
  exit(0)

ip = argv[1]

files = argv[2] if len(argv)>2 else '*.h264'

system('scp "pi@{}:~/cctv_capture/{}" .'.format(ip, files))