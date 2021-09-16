# -*- coding: utf-8 -*-


# Commented out IPython magic to ensure Python compatibility.
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

#https://stackoverflow.com/questions/51143458/difference-in-output-with-waitkey0-and-waitkey1/51143586 problem: it does not show as continuous feed
#1) highlight the three points
#2) graphics to visually show angle
#3) funzione dove input=parte del corpo, output=highlight landmarks su parte del corpo desiderata
#save params to run only plots and not everything
#in teoria, sia da webcam che da video esterno dovrei avere la sequenza di immagini. Perché con yolov4 file no? non è solo cv_imshow il problema. Sembra quasi che 
#con delle funzioni di supporto javascript riesco ad avere un continuous flow
#se aggiro il problema cv_imshow mantenendo le funzioni javascript, cambierebbe qualcosa almeno per l'input da webcam? /edit, stesso problema anche con video 
#senza pose tracker
#per webcam: funziona usare qualcos'altro invece che cv2_show? tipo PIL?
#per video salvato: funziona creare un'impalcatura html-js che "aggiri" il ciclo while con dentro cv2_imshow?
#se faccio cv2_imshow senza fare img=cv2.circle... a cosa è uguale img? resta invariata?
"""
le due cose che portano via più tempo: dover aggiornare i salvataggi ed il fatto di non avere continuous stream
inoltre, sarebbe bello poter modificare il codice mentre l'applicazione gira e poterne vedere gli effetti in real-time, senza dover ri-runnare tutto (a costo di farla inceppare per un comando errato)
esempio potrei scrivere codice commentato mentre l'applicazione gira, e poi scommentarlo quando sono certo che non dà errori, oppure se devo modificare
solo una cosa lo posso fare al volo senza conseguenze
"""
#"""
# video_path = "1500_doha.mp4"

# mp4 = open(video_path, "rb").read()
# data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
# HTML(f"""
# <video width=400 controls>
#       <source src="{data_url}" type="video/mp4">
# </video>
# """)

#conversion function from body part to number

###

#disegna funzione che sostituisce arto cercato con arto che lo sovrappone (altrimenti, se i punti cercati sono unici, va bene cosi)
#detect occluded angles
#issue: if wait until end of video findangle has trubles; maybe is only a particular config wich cause it, and not the ending point
#averaginf function for plots, display seconds, milliseconds 
#the sequence of try except allows to run this code from command line or opening an editor. Alternatively, you can replace
#the try-excepts statements with if-else to handle None arguments from the argparser
def main(args):
    
    # filename=args.video
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
    
    #positioning of text and dimensions
    h_angle=50
    w_angle=100
    h_j=65
    w_j=w_angle
    fontScale=2
    thickness=2
    
    #to save the video
    width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer= cv2.VideoWriter('runpose.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))
    try:
        duration=args.max_len
        if duration is None:
            duration=25
    except:
        duration=40
        
        
    while cap.isOpened():

        success, img = cap.read()
        if success is False or img is None:
            break
        print(success)
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
        
        
        writer.write(img)
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
    # with open("angle.pickle1", "wb") as f:
    #     pickle.dump(angles, f)
        
    target2=target
    # Bt.plot(lmList, target2, width, height)
    # an=[]
    # with open("angle.pickle1", "rb") as f:
    #     an1=pickle.load(f)
    # with open("angle.pickle2", "rb") as f:
    #     an2=pickle.load(f)
    # with open("angle.pickle3", "rb") as f:
    #     an3=pickle.load(f)
    # an.append(an1)
    # an.append(an2)
    # an.append(an3)
    # an=np.array(an)
    # print(an)
    # angles=[statistics.mean(an[:][i]) for i in range(0, an.shape[1]-1)]
    
    # target_angles=[20, 40, 80, 120, 140, 160]
    # frequencies=np.zeros(range(len(target_angles)-1))
    # for ang in angles:
    #     for i in range(len(target_angles)-1):
    #         angle=ang[0]
    #         print("angle: ", angle)
    #         if angle>target_angles[i] and angle<target_angles[i+1]:
    #             frequencies[i]+=1
               
    x=range(len(angles)) #frames
    # x2=range(int(len(x)/fps))
    # x3=[]
    # for val in x:
    #     if (val/fps)==x2[int(val/fps)]:
    #         x3.append(x2[int(val/fps)])
    #     else:
    #         x3.append(0)
    plt.plot(x, angles, linestyle="-", color="blue")
    # plt.locator_params(axis='x', nbins=len(x2))
    plt.xlabel("frames") #frames change
    plt.ylabel("angle values")
    # plt.xticks(x, x2)
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