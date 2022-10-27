#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This scrtipt script..

import cv2
from imutils.video.pivideostream import PiVideoStream
import time
from datetime import datetime
import numpy as np
import os
from subprocess import call

class VideoCamera(object):
    def __init__(self, led_controler=None,
                 flip = True, 
                 output_loc='./',
                 img_type  = ".jpg", 
                 photo_string= "stream_photo",
                 mask_fun=None):
        #self.vs = PiVideoStream(resolution=(1920, 1080), framerate=30).start()
        self.width = 640 
        self.height = 480
        self.framerate = 30
        self.output_loc = output_loc
        self.video_stop = False
        self.mask_fun = mask_fun
        self.save_mask_loc = False
        self.led_controler = led_controler
        if not os.path.exists(output_loc):
            os.makedirs(output_loc)
        self.vs = PiVideoStream((self.width, self.height), framerate=self.framerate).start()
        self.flip = flip # Flip frame vertically
        self.img_type = img_type # image type i.e. .jpg
        self.photo_string = photo_string # Name to save the photo
        self.led_c = False
        if self.led_controler is not None:
            self.led_controler.IR_open()
            self.led_c = True
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()
        self.video_stop = True

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame
    
    def add_mask(self, frame):
        if self.mask_fun is not None:
            return self.mask_fun(frame, self.save_mask_loc)
        return frame
    
    def get_frame(self):
        frame = self.add_mask(self.flip_if_needed(self.vs.read()))
        ret, jpeg = cv2.imencode(self.img_type, frame)
        return jpeg.tobytes()

    # Take a photo, called by camera button
    def take_picture_record(self):
        frame = self.flip_if_needed(self.vs.read())
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S") # get current time
        file_name = str(self.photo_string + "_" + today_date)
        file_path_main =os.path.join(self.output_loc, file_name) 
        cv2.imwrite(file_path_main + self.img_type, frame)
        if self.mask_fun is None:
            pass
        else:
            with open(os.path.join(self.output_loc, file_name)+'.txt', 'w') as f:
                f.write('\n'.join([str(i) for i in self.mask_fun(frame, True)]))
        if self.led_c: 
            self.vs.stop()
            sleep(2)
            script = './utils/LED_and_Record.sh'
            call([script, str(self.led_controler.LED_duration), 
                str(self.led_controler.LED_intervention), 
                str(self.led_controler.repeat_n), file_path_main])
