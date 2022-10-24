# modified based on: https://github.com/lxy764139720/IrisRecognition
# Thanks lxy764139720!

import numpy as np
import cv2


def inner_circle(img):
    """
    内圆检测
    :param img: cv2.imread() numpy.ndarrdy
    :return: 瞳孔霍夫圆参数 numpy.ndarray [x, y, r], left and right
    """

    img = cv2.medianBlur(img, 11)
    ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2, 800,
                               param1=110, param2=20, minRadius=10, maxRadius=100)
    circles = np.int16(np.around(circles))
    circles[0, :, 2] += 3
    return circles[0][0], circles[0][1]

def add_circle(img, inner_x, inner_y, inner_r):
    cv2.circle(img, (inner_x, inner_y), inner_r, (0, 255, 0), 1)
    cv2.circle(img, (inner_x, inner_y), 2, (0, 0, 255), 3)
    return img

def iris_recon_img(img):
    right_iris, left_iris = inner_circle(img)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cimg = displayCircle(cimg, right_iris[0], right_iris[1], right_iris[2])
    cimg = displayCircle(cimg, left_iris[0], left_iris[1], left_iris[2])
    return cimg, right_iris[2], left_iris[2]

    
    
