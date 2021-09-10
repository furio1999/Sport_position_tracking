#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 14:11:46 2021

@author: fulvio
"""
import cv2
import numpy as np
import PIL
import io
import html
import time
import matplotlib.pyplot as plt
import BodyTracker as Bt
# %matplotlib inline
import mediapipe as mp
from utils import *   #in teoria se import * importo ancge gli import, o solo le classi e funzioni?
import math
class poseDetector():
    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,
                                     self.detectionCon, self.trackCon)
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS) #c'è in comando img=cv2.line in draw_landmarks?
        return img
    
    def joint_mapping(self, target):
        numbers=range(33)
        body=["right_leg", "left_leg", "right_arm", "left_arm", "right_ankle", "left_ankle"]
        if(target==body[0]):
            return [24,26,28]
        elif(target==body[1]):
           return [23,25,27]
        elif(target==body[2]):
           return [12,14,16]
        elif(target==body[3]):
            return [11,13,15]
        elif(target==body[4]):
            return 28
        elif(target==body[5]):
            return 27
        else:
            print("please type correctly the desired body part")
        
        
    #draw=True draw the searched landmark
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
            if draw:
              id, cx, cy=self.lmList[28]
              circle=cv2.circle(img, (cx, cy), 4, (255, 0, 0), cv2.FILLED)
              
              
        return self.lmList
    
    #occhio, angle>180!! perché? cosa lo fa "sballare"?
    #metti un if nel caso il joint sia nascosto
    def findAngle(self, img, p1, p2, p3, draw=True):
        # Get the landmarks
        angle=0
        w,h,c=img.shape
        if draw:
            x1, y1 = self.lmList[p1][1:]
            x2, y2 = self.lmList[p2][1:]
            x3, y3 = self.lmList[p3][1:]
            # Calculate the Angle
            angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
            if angle < 0:
              angle += 360
            if angle >180:
              angle-=180
        # print(angle)
        # Draw
            # cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            # cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            circle=cv2.circle(img, (x1, y1), 6, (255, 0, 0), cv2.FILLED) #4=standard for mediapipe keypoints
            circle=cv2.circle(img, (x2, y2), 6, (255, 0, 0), cv2.FILLED)
            circle=cv2.circle(img, (x3, y3), 6, (255, 0, 0), cv2.FILLED)
            #metti un if per regolare le coordinate della scritta in base a quale parte del corpo hai scelto (sx, dx)
            text="Angle: " + str(int(angle))
            text=cv2.putText(img, text, (w+100, 50),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        return angle
    

# Commented out IPython magic to ensure Python compatibility.
def subplot(axes, x, y, Xlabel, Ylabel, title=None): #dopo anche tipo di function, es, scatter o plot
     axes.set_title(title)
     axes.set(xlabel=Xlabel, ylabel=Ylabel)
     axes.scatter(x, y)
     
def plot(lmList, target, width, height):
     coord=[]
     coords=[]
     x=[]
     h=[]
     ##for##
     n=0
     for lista in lmList:
       #if target is in list
       id, xc, yc=lista[target]
       x.append(xc/width)
       h.append(yc/height)
     #coords=[coord.append([i,j]) for i in x for j in h]
     coord.append(x)
     coords.append(coord)
     n+=1
     coord=[]
     coord.append(h)
     coords.append(coord)
     #end for##
     
#      %cd ..
     # fig, axs=plt.subplots(1,3) #fai un terzo grafico per la velocità nella direzione x
     # fig.suptitle("different comparisons")
     # subplot(axs[0], coords[0], coords[1], "Xposition", "Yposition", title="joint x_y")
     # #plt.savefig("joint_position_x_y.png")
     
     # timestamps = [x/20 for x in range(len(coords[0]))]
     # subplot(axs[1], coords[0], coords[1], "time", "Xposition", title="joints in time")
     # #plt.savefig("joint_position_over_time.png")
     # plt.savefig("position graphs.png")

     # timestamps = [t/20 for t in range(len(coords[1]))]
     # subplot(axs[2], coords[0], coords[1], "time", "Yposition", title="joints in time")
     # #plt.savefig("joint_position_over_time.png")
     # plt.savefig("position graphs.png")
     
     ## occhio
     fig2=plt.figure(1)
     judgement="WRONG"
     trajectory_fit(x, h, height, width, judgement, fig2)