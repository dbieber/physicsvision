import sys
import cv
import cv2
import numpy as np
import math
import random
import time

import simulations

ESC = 27

class VideoDemo():
    def __init__(self):
        self.vc = cv2.VideoCapture(0)
        self.frame = None
        cv2.namedWindow('win', cv2.CV_WINDOW_AUTOSIZE)

        if self.vc.isOpened(): # try to get the first frame
            self.vc.read()

    def run(self):
        while True:
            rval, frame = self.vc.read()
            key = cv2.waitKey(10)
            time.sleep(.16)
            if frame is None:
                continue
            else:
                framecopy = frame.copy()
                framecopy = cv2.resize(framecopy, (framecopy.shape[1]/2, framecopy.shape[0]/2))
                self.frame = framecopy
                cv2.imshow('win', framecopy)

            if key == ESC: # exit on ESC
                sys.exit(0)

            if key == ord(' '):
                self.vc.release()
                return


demo = VideoDemo()
demo.run()

p = .4
cv2.destroyWindow('win')
cv2.namedWindow('win', cv2.CV_WINDOW_AUTOSIZE)
while True:
    key = cv2.waitKey(10)
    time.sleep(.16)

    blur = cv2.blur(demo.frame, ksize=(4,4))
    canny = cv2.Canny(blur, 404*p, 156*p, apertureSize=3)

    cv2.imshow('win', canny)

    if key == ESC:
        sys.exit()

    if key == ord('='):  # +
        p += .02; print p
    elif key == ord('-'):
        p -= .02; print p

    if key == ord(' '):
        break

simulation = simulations.SimulationDemo()
contours, hierarchy = cv2.findContours(canny, cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_SIMPLE)
for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    newContour = cv2.approxPolyDP(contour, 0.005*perimeter, True)
    newContour = cv2.convexHull(newContour)
    newContour = newContour.reshape(len(newContour),2)
    simulation.add_contour(newContour)

cv2.destroyWindow('win')
# cv2.namedWindow('win', cv2.CV_WINDOW_AUTOSIZE)
# cv2.imshow('win', canny)

simulation.run()

print "here2"
raw_input()
