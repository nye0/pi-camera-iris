#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
import sys
sys.path.append('.')
from flask import Flask, render_template, Response, request, send_from_directory
from utils.camera import VideoCamera
from utils.LED_control import light_control
from utils.iris_recognition import iris_recon_img
from time import sleep
import os

lc = light_control(IR_dim=False, LED_dim=False, 
                   LED_duration=1, LED_intervention=3,
                   repeat_n=3)

pi_camera = VideoCamera(flip=True, led_controler=lc, mask_fun=iris_recon_img)

# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Take a photo when pressing camera button
@app.route('/picture')
def take_picture():
    pi_camera.take_picture_record()
    exit()
    return "None"

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)
