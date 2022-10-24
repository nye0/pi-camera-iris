#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This scrtipt script..

import cv2 as cv
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
from datetime import datetime
import numpy as np
import os


class VideoCamera(object):
    def __init__(self, flip = True, 
                 output_loc='./',
                 img_type  = ".jpg", 
                 photo_string= "stream_photo",
                 mask_fun=None):
        # self.vs = PiVideoStream(resolution=(1920, 1080), framerate=30).start()
        self.width = 640 
        self.height = 480
        self.framerate = 20
        self.video_type = 'mp4'
        self.video_encoder = 'mp4v'
        self.output_loc = output_loc
        self.video_stop = False
        self.mask_fun = mask_fun
        self.save_mask_loc = False
        if not os.path.exist(output_loc):
            os.makedirs(output_loc)
        self.vs = PiVideoStream((self.width, self.height), framerate=20).start()
        self.flip = flip # Flip frame vertically
        self.file_type = file_type # image type i.e. .jpg
        self.photo_string = photo_string # Name to save the photo
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()
        self.video_stop = True

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame
    
    def add_mask(self, frame):
        if self.mask_fun not is None:
            return mask_fun(frame, self.save_mask_loc)
        return frame
    
    def get_frame(self):
        frame = self.add_mask(self.flip_if_needed(self.vs.read()))
        ret, jpeg = cv.imencode(self.img_type, frame)
        self.previous_frame = jpeg
        return jpeg.tobytes()

    # Take a photo, called by camera button
    def take_picture(self):
        frame = self.flip_if_needed(self.vs.read())
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S") # get current time
        file_name = str(self.photo_string + "_" + today_date + self.img_type)
        cv.imwrite(os.path.join(self.output_loc, file_name), frame)    
        with open(os.path.join(self.output_loc, file_name)+'.txt', 'w') as f:
            f.write('\n'.join([str(i) for i in mask_fun(frame, True)]))
            
            
    def record_video(self):
        fourcc_mp4 = cv2.VideoWriter_fourcc(*'%s' % self.video_encoder)
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S")
        file_result = os.path.join(self.output_loc, self.photo_string + "_" + today_date + self.video_type)
        out_mp4 = cv2.VideoWriter(file_result, fourcc_mp4, self.framerate, 
                                  (self.width, self.height),isColor = False)
        while True:
            frame = self.flip_if_needed(self.vs.read())
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            out_mp4.write(gray)
            if self.video_stop:
                break
        out_mp4.release()
        
        
        
