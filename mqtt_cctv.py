import io, time, picamera
import picamera.array
import numpy as np
# import cv2

from mqtt import Mqtt
if __name__ == '__main__':
  from sys import argv

  def msg(msg):
    if msg == 'record':
      detected = True

  mqtt = Mqtt(*([msg, 'CCTV'] + argv[1:]))

  detected = False
  class DetectMotion(picamera.array.PiMotionAnalysis):
    def analyse(self, a):
      global detected
      a = np.sqrt(
        np.square(a['x'].astype(np.float)) +
        np.square(a['y'].astype(np.float))
      ).clip(0, 255).astype(np.uint8)
      # If there're more than 15 vectors with a magnitude greater
      # than 80, then say we've detected motion
      if (a > 80).sum() > 15:
        detected = True

  stream = None
  outfile = None
  last_pos = 0
  from os import chdir, listdir, remove, curdir
  from os.path import getsize
  chdir('/home/pi/cctv_capture')

  def write_video():
    global outfile, last_pos, stream
    if outfile is None or outfile.closed:
      files = listdir(curdir) #not checking directories under 'capture'
      max = 1024**3
      s = sum(getsize(f) for f in files)
      if s > max: #larger then 1GB
        i = 0
        while s > max:
          s -= getsize(files[i])
          remove(files[i])
          i += 1
      outfile = io.open(time.strftime('%Y %m %d-%H %M %S') +'.h264', 'wb')
      with stream.lock:
        for frame in stream.frames:
          if frame.frame_type == picamera.PiVideoFrameType.sps_header:
            stream.seek(frame.position)
            break
      mqtt.send('Started recording:'+outfile.name)
    else:
      stream.seek(0)
    mqtt.send('Resuming record on:'+outfile.name)
    # print('writing video :', outfile.name)
    # while True:
    #     byte = stream.read1()
    #     if not byte : break
    #     outfile.write(byte)
    outfile.write(stream.read())
    stream.seek(0)
    stream.truncate() #wipe circular buffer
    #last_pos = stream.frames[-1].position

  with picamera.PiCamera() as cam:
    cam.resolution = (1920//2, 1080//2) # pi is not powerful enough for full HD record
    stream = picamera.PiCameraCircularIO(cam, seconds=5)
    with DetectMotion(cam) as motion:
      try:
        cam.start_recording(stream, format='h264', motion_output=motion)
        time.sleep(2)
        while True:
          cam.wait_recording(2)
          if detected:
            # cam.split_recording(outfile)
            cam.wait_recording(3)
            write_video()
            detected = False
          elif outfile is not None and not outfile.closed:
            mqtt.send('Done recording:'+outfile.name)
            outfile.close()
      finally:
        cam.stop_recording()