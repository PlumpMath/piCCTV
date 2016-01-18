#!/usr/bin/env bash

mv cctv.py /home/pi/
chmod 755 cctv
mv cctv /etc/init.d/
update-rc.d cctv defaults
service cctv start
