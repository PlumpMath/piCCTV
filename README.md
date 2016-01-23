# piCCTV
Turn Raspberry pi into a CCTV

## Features
1. Start recording on capture of movement.
2. It uses ring buffer to include recordings
3. Automatically merge records into 1 file on capture of continuous movements.
4. Keep its recording folder(/home/pi/cctv_capture) under 1GB by removing oldest files.

## Prerequisites
1. Raspberry compatible camera connected to its camera connector. Other interfaces like GPIO is not tested but may possible somehow...
2. `sudo pip install numpy`
3. `sudo apt-get install python-picamera` [details](http://picamera.readthedocs.org/en/release-1.10/install2.html)
4. `sudo raspi-config` and enable camera.
5. Git installed system that you'll use as a surveillance monitor. On Windows, git bin folder needs to be registered in environmental variable path. The getall script uses the scp.exe in it.

## How to use
1. `git clone https://github.com/chidea/piCCTV.git && cd piCCTV`
2. `sudo python cctv.py for one-time run`
3. `sudo sh install.sh` to install it as system service. In this way, you can stop, start, restart the service with `sudo service cctv [restart/start/stop]` later.
4. On your monitoring machine, do the same on line number 1 and `python getall.py <address of your raspberry pi> [file name or filter]`
  If you're using Windows for it and do not want python to be installed, use `getall <address of your raspberry pi> [file name or filter]` instead (utilizing getall.bat).  

### File name filter example for getall.bat or scp
- Simply leave it blank or `*` to get all videos.
- `"2015\ 05\ 18*"` to get all videos captured on May 18th, 2015.

### How to play recorded .264 videos
[ffplay](https://ffmpeg.org/ffplay.html) can be used to play it directly or convert it with [ffmpeg](https://trac.ffmpeg.org/wiki/Encode/H.264).

### MQTT version
You can be noticed for CCTV status messages by MQTT.
It's utilizing [paho python client](http://www.eclipse.org/paho/clients/python/).
```
sudo pip install paho-mqtt
sudo python mqtt_cctv.py <topic> [broker address] [id] [pw]
```
Sending a message `record` to topic `/control/<topic>` will record for several seconds as same as capturing a motion.
 
If you want to install this version as service, after installing the service as instruction above, overwrite the file /home/pi/cctv.py with it and restart the service.
```
mv mqtt_cctv.py /home/pi/cctv.py && sudo service cctv restart
```

> Feel free to take a look at cctv.py and apply the CV on it. 
