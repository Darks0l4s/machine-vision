import cv2
import numpy as np
import re


def get_face_embedding(img):
    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    if len(faces) == 0:
        return None
    x, y, w, h = faces[0]
    face = img[y:y+h, x:x+w]
    face = cv2.resize(face, (64, 64))
    gx = cv2.Sobel(face, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(face, cv2.CV_32F, 0, 1, ksize=3)
    mag, ang = cv2.cartToPolar(gx, gy)
    hist = cv2.calcHist([face], [0], None, [32], [0, 256])
    return hist.flatten() / np.linalg.norm(hist)

video = cv2.VideoCapture(1)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

with open("encod.txt", 'r', encoding='utf-8') as f:
    content = f.read()
pattern = r'([^:]+):\[(.*?)\]'
matches = re.findall(pattern, content, re.DOTALL)

while True:
    good, img = video.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(img_gray, 1.3, 2)

    for x, y, w, h in faces:

        face_roi = img_gray[y:y+h, x:x+w]
        
        emb = get_face_embedding(face_roi)
        for i, (image_name, numbers_str) in enumerate(matches, 1):
            embedding = [float(x) for x in numbers_str.split()]
            
            if emb is not None and embedding is not None:
                distance = np.linalg.norm(emb - embedding)
                if distance < 1:
                    cv2.putText(img, image_name.strip()[:-6], (x,y-10), cv2.FONT_HERSHEY_COMPLEX, 1, (200, 0, 0), 2)
                    cv2.rectangle(img, (x,y), (x+w, y+h), (0, 150, 0), 3)
                    break
                else:
                    cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 150), 3)

    key= cv2.waitKey(30)
    if key == ord('q'):
        break
    cv2.imshow("myVideo", img)