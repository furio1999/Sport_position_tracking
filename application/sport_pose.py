# -*- coding: utf-8 -*-


# import dependencies
import cv2
import numpy as np
import PIL
import io
import html
import time
import imageio
import matplotlib.pyplot as plt
import BodyTracker as Bt
from utils import *
# %matplotlib inline

def main(args):
    
    filename="1500_doha.mp4"
    if(args.camera):
        cap = cv2.VideoCapture(0)
    else:
        if(args.video is not None):
            cap=cv2.VideoCapture(args.video)
        else:
          print("hello")
          cap = cv2.VideoCapture(filename)
    time.sleep(2.0)  #let time to the video to start
    pTime = 0
    detector = Bt.poseDetector()
    lmList=[]
    
    #selected body parts
    try:
     points=detector.joint_mapping(args.body_part)
     if points is None:
        points=[12, 14, 16] 
    except:
      points=[12, 14, 16]
    p=points
    maxim=max(points)
    angle=0
    img=""
    inf=60
    sup=140
    try:
        target=argparse.joint
        if target is None:
            target=21
    except:
       target=21 #left wirst, to be traced
       
    #keep trace of some key variables   
    nframes=30 # is the number of saved frames for the function live_tracker
    iterator=0
    angles=[]
    refTime=time.time()
    tracker=live_tracker(nframes)
    
    #to save the video
    width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer= cv2.VideoWriter('runpose.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))
    try:
        duration=args.max_len
        if duration is None:
            duration=25
    except:
        duration=25
        
        
    while cap.isOpened():

        success, img = cap.read()
        if success is False or img is None:
            break
        print(success)
        writer.write(img)
        width,height, c=img.shape
        size=(width, height)
        img = detector.findPose(img)
        lmList2 = detector.findPosition(img)
        #print(lmList2)
        
        #draw angle and perform evaluation
        if(maxim>len(lmList2)):
            draw=False
        if(search(lmList2, p[0])  and search(lmList2, p[1] ) ) and ( search(lmList2, p[2]) ):
            draw=True
        angle=detector.findAngle(img, p[0], p[1], p[2]), #attenzione, cambia braccio ogni tanto!!
        angles.append(angle)
        if(args.running_evaluation):
           judge(img, angle, inf, sup)
           
           
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        lmList.append(lmList2)
        
        #trajectory tracker
        text=cv2.putText(img, str(int(fps)), (30, 30), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        if(iterator>0) and args.trajectory_tracking:
            tracker.live_track(img, lmList2[target])
        cv2.imshow(" Capture ", img)
        iterator+=1
        
        #save and ending code
        result = cv2.VideoWriter('runpose.mp4', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)
        
        key=cv2.waitKey(10)
        if key == ord('q'):
          break
        if (cTime-refTime)>duration:
            print("end ")
            break
     
    cap.release()
    cv2.destroyAllWindows()
    
    import pickle
    import statistics
        
    target2=target
               
    x=range(len(angles)) #frames

    plt.plot(x, angles, linestyle="-", color="blue")
    plt.xlabel("frames") #frames change
    plt.ylabel("angle values")
    plt.show()
    plt.savefig("angle_graph")
    # plt.bar(target_angles, frequencies)
    # plt.savefig("angle_hist")
    
if __name__ == "__main__":
     #action default false
    
      parser=argparse.ArgumentParser()
      
      parser.add_argument("--running_evaluation", action="store_true", help="perform AI running trainer on video, actually only for upper arms")
      
      parser.add_argument("--trajectory_tracking", action="store_true")
      
      parser.add_argument("--joint", type=int)
      
      parser.add_argument("--video", type=str, help="type the name of the desired video to load")
      
      parser.add_argument("--camera", action="store_true")
      
      parser.add_argument("--out_directory", type=str)
      
      parser.add_argument("--duration", type=int, help="max desired duration of video application")
      
      parser.add_argument("--body_part", type=str, help="possible options: right_leg, left_leg, right_arm, left_arm, right_ankle, left_ankle")
      
      args=parser.parse_args()
      main(args)
#argpaser for: type of sport; seconds of length; target part of body; color; activate different tracker;
