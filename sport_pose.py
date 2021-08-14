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

#!git clone https://github.com/google/mediapipe.git
# %cd mediapipe
# !pip list -v mediapipe







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

#punta piede verso il basso: poco accurato

## Detect poses on a test video

We are going to detect poses on the following youtube video:
"""

#https://stackoverflow.com/questions/51143458/difference-in-output-with-waitkey0-and-waitkey1/51143586 problem: it does not show as continuous feed
#1) highlight the three points
#2) graphics to visually show angle
#3) funzione dove input=parte del corpo, output=highlight landmarks su parte del corpo desiderata
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