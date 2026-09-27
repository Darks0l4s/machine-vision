import cv2

video = cv2.VideoCapture("face/cat.mp4")

while True:
    good, img = video.read()
    
    # img = cv2.resize(img, (120, 120))
    # imgCropped = img[10:390, 500:700]
    # cv2.imshow("Cropped", imgCropped)
    cv2.rectangle(img, (0,0), (570, 390), (0, 150, 0), 50)
    cv2.putText(img, "SOS", (500, 500), cv2.FONT_HERSHEY_COMPLEX, 1, (150, 0, 0), 2)
    cv2.imshow("myVideo", img)
    if cv2.waitKey(30) == ord('q'):
        break
    
# img = cv2.imread("face/robbi1.jpeg")
# cv2.imshow("myImage", img)
# cv2.waitKey(2000)