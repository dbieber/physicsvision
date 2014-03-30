import sys
import cv
import cv2
import numpy as np
import math
import random
import time

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


#demo = VideoDemo()
p = .08
"""
demo.run()

p = .08
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
"""
image = cv2.imread('test.png')

blur = cv2.blur(image, ksize=(4,4))
#gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
#retval, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
canny = cv2.Canny(blur, 404*p, 156*p, apertureSize=3)
#canny = thresh

cv2.imshow('win', canny)
key = cv2.waitKey(0)

cannycopy = canny.copy()

hold = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
contours, hierarchy = cv2.findContours(canny, cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_SIMPLE)
circleList = []

houghcirlces = cv2.HoughCircles(canny, cv.CV_HOUGH_GRADIENT, 2, 100)
#print 'hough', houghcirlces

circles = image.copy()
for circ in houghcirlces[0]:
    print circ
    cv2.circle(circles, (int(circ[0]), int(circ[1])), int(circ[2]), (1, 0, 0))

cv2.imshow('win', circles)
key = cv2.waitKey(0)

def slidingWindow(canny):
    width, height = canny.shape
    step = 50
    for windowSize in [25, 50, 100]:
        for x in range(windowSize, width-windowSize, step):
            for y in range(windowSize, height-windowSize, step):
                
                #cv2.imshow('win', window)
                #key = cv2.waitKey(0)
                center = np.array([0, 0])
                num = 0.0
                for i in range(-windowSize, windowSize):
                    for j in range(-windowSize, windowSize):
                        if canny[x+i, y+j] > 0:
                            center += np.array([i, j])
                            num += 1.0
                if num == 0.0:
                    continue
                center = center / num

                avgRadius = 0
                radii = []
                for i in range(-windowSize, windowSize):
                    for j in range(-windowSize, windowSize):
                        if canny[x+i, y+j] > 0:
                            radius = np.linalg.norm(np.array([i, j]) - center)
                            radii.append(radius)
                            avgRadius += radius

                avgRadius = avgRadius / len(radii)
                
                counter = 0
                for r in radii:
                    dist = r / avgRadius
                    if .6 < dist < 1.4:
                        counter += 1
                
                if counter/num > .5:
                    #circleList.append((center[0], center[1], avgDist))
                    print 'PICK THIS ONE'
                    window = canny[x-windowSize:x+windowSize, y-windowSize:y+windowSize]
                #cv2.drawContours(hold, [contour], 0, (0, 0, 200))
                    cv2.imshow('win', window)
                    key = cv2.waitKey(0)

def slidingWindow2(contours):
    for contour in contours:
        #perimeter = cv2.arcLength(contour, True)
        #newContour = cv2.approxPolyDP(contour, 0.005*perimeter, True)
        #newContour = cv2.convexHull(newContour)
        if cv2.contourArea(contour) < 100:
            continue
        newContour = contour
        newContour = newContour.reshape(len(newContour),2)

        minX = sys.maxint
        maxX = sys.minint
        minY = sys.maxint
        maxY = sys.minint

        for p in newContour:
            if minX > p[0]:
                minX = p[0]
            if maxX < p[0]:
                maxX = p[0]
            if minY > p[1]:
                minY = p[1]
            if maxY < p[1]:
                maxY = p[1]
        width, height = canny.shape
        step = 50
        for windowSize in [25, 50, 100]:
            for x in range(windowSize, width-windowSize, step):
                for y in range(windowSize, height-windowSize, step):
                    
                    #cv2.imshow('win', window)
                    #key = cv2.waitKey(0)
                    center = np.array([0, 0])
                    num = 0.0
                    for i in range(-windowSize, windowSize):
                        for j in range(-windowSize, windowSize):
                            if canny[x+i, y+j] > 0:
                                center += np.array([i, j])
                                num += 1.0
                    if num == 0.0:
                        continue
                    center = center / num

                    avgRadius = 0
                    radii = []
                    for i in range(-windowSize, windowSize):
                        for j in range(-windowSize, windowSize):
                            if canny[x+i, y+j] > 0:
                                radius = np.linalg.norm(np.array([i, j]) - center)
                                radii.append(radius)
                                avgRadius += radius

                    avgRadius = avgRadius / len(radii)
                    
                    counter = 0
                    for r in radii:
                        dist = r / avgRadius
                        if .6 < dist < 1.4:
                            counter += 1
                    
                    if counter/num > .5:
                        #circleList.append((center[0], center[1], avgDist))
                        print 'PICK THIS ONE'
                        window = canny[x-windowSize:x+windowSize, y-windowSize:y+windowSize]
                    #cv2.drawContours(hold, [contour], 0, (0, 0, 200))
                        cv2.imshow('win', window)
                        key = cv2.waitKey(0)

slidingWindow2(contours)

for contour in contours:
    #perimeter = cv2.arcLength(contour, True)
    #newContour = cv2.approxPolyDP(contour, 0.005*perimeter, True)
    #newContour = cv2.convexHull(newContour)
    if cv2.contourArea(contour) < 100:
        continue
    newContour = contour
    newContour = newContour.reshape(len(newContour),2)

    center = np.average(newContour, axis=0)
    avgDist = 0.0
    numPoints = 0
    for c in newContour:
        dist = np.linalg.norm(c - center)
        print dist
        avgDist += dist
        numPoints += 1

    avgDist = avgDist / numPoints
    print avgDist
    
    counter = 0
    for c in newContour:
        dist = np.linalg.norm(c - center) / avgDist
        print 'dist', dist
        if .8 < dist < 1.2:
            counter += 1
    print counter
    if counter/numPoints > .8:
        circleList.append((center[0], center[1], avgDist))
        print 'PICK THIS ONE'
    
    cv2.drawContours(hold, [contour], 0, (0, 0, 200))
    cv2.imshow('win', hold)
    key = cv2.waitKey(0)

circles = image
for circ in circleList:
    print circ
    cv2.circle(circles, (int(circ[0]), int(circ[1])), int(circ[2]), (1, 0, 0))

cv2.imshow('win', circles)
key = cv2.waitKey(0)

cv2.destroyWindow('win')
# cv2.namedWindow('win', cv2.CV_WINDOW_AUTOSIZE)
# cv2.imshow('win', canny)

print "here2"
raw_input()
