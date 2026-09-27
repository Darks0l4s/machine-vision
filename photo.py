import cv2
# import os
import sys

if len(sys.argv) > 1:
    text = sys.argv[1]
    print(f"Получен текст: {text}")
else:
    print("Текст не передан")
# name = input("Введите имя нового пользователя\n")
dir = "faces/"+text+"#"
video = cv2.VideoCapture(0)
for i in range(10):
    good, img = video.read()
    cv2.waitKey(200)
    cv2.imwrite(str(dir+str(i)+'.jpg'), img)
    cv2.imshow("myVideo", img)
