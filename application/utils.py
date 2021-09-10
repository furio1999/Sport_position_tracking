#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 21:44:45 2021

@author: fulvio
"""
import time
from absl import app, logging
import cv2
import numpy as np
from flask import Flask, request, Response, jsonify, send_from_directory, abort
import os
import sys
from sys import platform
import argparse
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def fit_func(x, a, b, c):
    return a*(x ** 2) + b * x + c


# megio per saltatori. Per i runners semplice traccio linea, forse meglio con velocita relativa pario a 0. Per i ruuners, stride
#+ foot angle + leg angle + elbow angle
#https://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06.15-Quiver-and-Stream-Plots/
def trajectory_fit(x, y, height, width, runJudgement, fig):
    #DONOT PASS figure as a kwarg
    # x = [joint for joint in joints[0]]
    # y = [height - joint for joint in joints[1]]
    print("x: ", x)
    print("y: ", y)

    try:
        params = curve_fit(fit_func, x, y)
        [a, b, c] = params[0]   
    except:
        print("fitting error")
        a = 0
        b = 0
        c = 0
    x_pos = np.arange(0, width, 1) #0, len(x), 0.1 (es. fino a 10 cm)
    y_pos = [(a * (x_val ** 2)) + (b * x_val) + c for x_val in x_pos]
    X, Y=np.meshgrid(x, y)
    U=np.cos(X)
    V=np.sin(Y)
    sp=fig.add_subplot(111)

    if(runJudgement == "WRONG"):
        # sp.plot(x, y, 'ro', linestyle='-', color='red',figure=fig)
        # sp.plot(x_pos, y_pos, linestyle='-', color='red',
        #          alpha=0.4, linewidth=5, figure=fig)
        sp.quiver(x,y,U,V)
    else:
        sp.plot(x, y, 'go', figure=fig)
        sp.plot(x_pos, y_pos, linestyle='-', color='green',
                 alpha=0.4, linewidth=5, figure=fig)

def distance(x, y):
    return ((y[0] - x[0]) ** 2 + (y[1] - x[1]) ** 2) ** (1/2)
    
def judge(img, angle, low, upper):
    #non funziona neanche passare angle come int da findangle
    w,h,c=img.shape
    angle=angle[0]
    judgement="RIGHT MOTION"
    if angle>low and angle<upper:
        judgment="RIGHT MOTION"  #non la prende questa opzione
    else:
        judgement="WRONG MOTION"
        
    cv2.putText(img, judgement, (w+100, 65), cv2.FONT_HERSHEY_PLAIN, 1,
                    (0, 255, 0), 2)
    return judgement

def search(lista, searched):
    for i in range(len(lista)):
        if lista[i][0] == searched:
            return True
    return False


# import the necessary packages
from collections import deque
import imutils
from imutils.video import VideoStream

# construct the argument parse and parse the arguments
class live_tracker():
    
 def __init__(self, buffer):
     self.buffer=buffer
     self.pts=deque(maxlen=buffer)
#  ap = argparse.ArgumentParser()
#  ap.add_argument("-v", "--video",
# 	help="path to the (optional) video file")
#  ap.add_argument("-b", "--buffer", type=int, default=64,
# 	help="max buffer size")
#  args = vars(ap.parse_args())
 
# # if a video path was not supplied, grab the reference
# # to the webcam
#  if not args.get("video", False):
#   vs=VideoStream(src=0).start()
 
# # otherwise, grab a reference to the video file
#  else:
#   vs = cv2.VideoCapture(args["video"])

 def live_track(self, frame, lista):
  buffer=self.buffer
 
  id, xc, yc=lista
  center=(xc,yc)
		# only proceed if the radius meets a minimum size, 10 default
  # if frame is None:
  #         return
     

  cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
	# update the points queue
  self.pts.appendleft(center)
  pts=self.pts


	# loop over the set of tracked points
  for i in range(1, len(pts)):
	  	# if either of the tracked points are None, ignore
	 	# them
	 	if pts[i - 1] is None or pts[i] is None:
	 		continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
	 	thickness = int(np.sqrt(buffer/ float(i + 1)) * 2.5)
	 	cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)


