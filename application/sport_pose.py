# -*- coding: utf-8 -*-


# Commented out IPython magic to ensure Python compatibility.
# import dependencies
import cv2
import numpy as np
import PIL
import io
import html
import time
import matplotlib.pyplot as plt
import HandTracker as Ht
# %matplotlib inline








"""dataset=curr + "Dataset_photo_random/"
os.chdir(dataset)
def pose_photo(img):
        detector = poseDetector()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=True)
        angle=detector.findAngle(img, 11, 13, 15) #attenzione, cambia braccio ogni tanto!!
        # if len(lmList) != 0:
        #     print(lmList[14])
        #     cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)
        cv2_imshow(img)
        return lmList

img=cv2.imread("running_lat_3.png")
lmList=pose_photo(img)
width, height, c=img.shape
plot(lmList, width, height)

# video_path = "1500_doha.mp4"

def search(list, platform):
    for i in range(len(list)):
        if list[i][0] == platform:
            return True
    return False

def main():

    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = Ht.poseDetector()
    lmList=[]
    points=[11, 13, 15]
    p=points
    maxim=max(points)
    draw=True
    angle=0
    img=""
    refTime=time.time()
    while cap.isOpened():

        success, img = cap.read()
        width,height, c=img.shape
        img = detector.findPose(img)
        lmList2 = detector.findPosition(img, draw=False)
        if(maxim>len(lmList2)):
            draw=False
        if(search(lmList2, p[0])  and search(lmList2, p[1] ) ) and ( search(lmList2, p[2]) ):
            draw=True
        angle=detector.findAngle(img, p[0], p[1], p[2], draw=draw), #attenzione, cambia braccio ogni tanto!!
        # if len(lmList2) != 0:
        #     print(lmList2[14])
        #     cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        lmList.append(lmList2)
        text=cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        cv2.imshow(" Capture ", img)
        cv2.waitKey(1)

        if cv2.waitKey(10) & 0xFF == ord('q'):
          break
        if (cTime-refTime)>4:
            print("end ")
            break
     
    cap.release()
    cv2.destroyAllWindows()
    print(lmList[1])
    width, height, c=img.shape
    joint=11
    Ht.plot(lmList, joint, width, height)
    
if __name__ == "__main__":
    main()
#"""

# Commented out IPython magic to ensure Python compatibility.
# %%script bash --bg
# python3 -m http.server 8000

# Commented out IPython magic to ensure Python compatibility.
# %%html
# <video controls autoplay><source src="http://localhost:8000/1500_doha.mp4" type="video/mp4"></video>
