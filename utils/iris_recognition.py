# modified based on: https://github.com/lxy764139720/IrisRecognition
# Thanks lxy764139720!

import numpy as np
import cv2


def inner_circle(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img = cv2.medianBlur(img, 11)
    ret, img = cv2.threshold(img, 25, 60, cv2.THRESH_BINARY)
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2, 100,
                               param1=110, param2=20, minRadius=10, maxRadius=30)
    circles = np.int16(np.around(circles))
    circles[0, :, 2] += 3
    return circles[0][0], circles[0][1]

def add_circle(img, inner_x, inner_y, inner_r):
    cv2.circle(img, (inner_x, inner_y), inner_r, (0, 255, 0), 1)
    cv2.circle(img, (inner_x, inner_y), 2, (0, 0, 255), 3)
    return img

def iris_recon_img(img, save_mask_loc):
    right_iris = left_iris = [0, 0, 0]
    try:
        right_iris, left_iris = inner_circle(img)
    except:
        pass
    img = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    img = add_circle(img, right_iris[0], right_iris[1], right_iris[2])
    img = add_circle(img, left_iris[0], left_iris[1], left_iris[2])
    if right_iris[2] != 0 or left_iris[2] != 0:
        print(right_iris[2], left_iris[2])
    
    if save_mask_loc:
        return right_iris, left_iris
    else:
        return img

    
    
