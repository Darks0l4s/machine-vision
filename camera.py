import cv2
import time

video = cv2.VideoCapture(1)

prevTime = 0
nowTime = 0
pos =100
while True:
    good, img = video.read()
    
    nowTime = time.time()
    fps = 1/(nowTime-prevTime)
    prevTime=nowTime
    key= cv2.waitKey(30)

    if key == ord("a"):
        pos-=5
    if key == ord('d'):
        pos+=5
    if key == ord('q'):
        break
    cv2.putText(img, str(fps), (pos, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (150, 0, 0), 2)
    cv2.imshow("myVideo", img)