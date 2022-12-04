import cv2
import pickle

width, height = 142,220

try:
    with open("Spark", "rb") as f:
        posList=pickle.load(f)
except:
    posList=[]

def mouseClick(events,x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events == cv2.EVENT_LBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1=pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(1)
    with open("Spark","wb") as f:
        pickle.dump(posList,f)


while True:
    img = cv2.imread("parker.png")
    for pos in posList:
        cv2.rectangle(img,pos,(pos[0] + width,pos[1] + height),(0,255,0),2)

    cv2.imshow("Image",img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)