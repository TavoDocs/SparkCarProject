import cv2
import pickle
import cvzone
import numpy as np
import requests

cap=cv2.VideoCapture(0)

with open("Spark", "rb") as f:
    posList = pickle.load(f)
width, height = 142,220
matripark=[0,0,0,0,0,0,0,0]

def chequeo(imgPro,matripark):
    space=0
    for pos in posList:
        i=posList.index(pos)
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        count=cv2.countNonZero(imgCrop)


        if count < 500:
            color=(0,255,0)
            thickness=6
            space+=1
            matripark[i]=1
        else:
            color=(0,0,255)
            thickness=2
            matripark[i]=0
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height),color ,thickness)
        r = requests.post(url="http://44.210.138.139/update_spaceB"+str(i+1)+".php?space=" + str(matripark[i]), data=0)
        cvzone.putTextRect(img, str(i), (x+100, y + height - 4), scale=3, thickness=1, offset=0)
        cvzone.putTextRect(img, str(count), (x, y + height - 4), scale=1.5, thickness=1, offset=0)
    cvzone.putTextRect(img, f'Espacios libres: {space}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20)


while True:

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    chequeo(imgDilate,matripark)

    cv2.imshow("Image",img)
    cv2.waitKey(1)
