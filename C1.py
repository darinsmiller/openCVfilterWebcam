import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation

def clp(a):
    pass

def getTrackbarsVals():
    return cv2.getTrackbarPos("Threshold", "TrackBars")/100

cv2.namedWindow("TrackBars")
#cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Threshold", "TrackBars", 0, 100, clp)
cams = 1

####  Cammera ####
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

if cams == 2:
    cap2 = cv2.VideoCapture(4)
    cap2.set(3,640)
    cap2.set(4,480)
#cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
cap.set(cv2.CAP_PROP_FPS, 30)

segmentor = SelfiSegmentation()
fpsReader = cvzone.FPS()

while True:
    success, img = cap.read()
    imgOut = segmentor.removeBG(img,(255,255,0), threshold=getTrackbarsVals()) #0.8
    if cams == 2:
        success, img2 = cap2.read()
        imgOut2 = segmentor.removeBG(img,(255,255,0), threshold=getTrackbarsVals()) #0.8
        imgStacked = cvzone.stackImages([img, imgOut, img2, imgOut2],4,1)
    else:
        imgStacked = cvzone.stackImages([img, imgOut],2,1)

    fps, imgStacked = fpsReader.update(imgStacked, color=(0,0,244))
    cv2.imshow("Image",imgStacked)

    if cv2.waitKey(1) != -1:
        cv2.destroyAllWindows()
        break
