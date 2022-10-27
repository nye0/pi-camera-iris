#!/usr/bin/python3
import picamera
import sys
file_path = sys.argv[1] + '.h264'
r_length = int(round(float(sys.argv[2])))

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
# black and white
camera.color_effects = (128,128)
camera.vflip = True
#server_socket = socket.socket()
#server_socket.bind(('0.0.0.0', 8000))
#server_socket.listen(0)
# Accept a single connection and make a file-like
# object out of it
#connection = server_socket.accept()[0].makefile('wb')

camera.start_recording(file_path, format='h264')
camera.wait_recording(r_length)
camera.stop_recording()
print('record finished!')
exit()
