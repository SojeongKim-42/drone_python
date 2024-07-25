#!/opt/local/bin/python
# -*- coding: utf-8 -*-
from time import sleep

import cv2
CAM_ID = 0

#Open the CAM
cap = cv2.VideoCapture(CAM_ID) #카메라 생성


#create the window & change the window size
#윈도우 생성 및 사이즈 변경
cv2.namedWindow('Face')

face_cascade = cv2.CascadeClassifier()
#face_cascade.load(r'C:\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
face_cascade.load(r'C:\Users\gs00\AppData\Local\Programs\Python\Python312\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
#C:\Users\ohyong\AppData\Local\Programs\Python\Python310\Lib\site-packages\cv2\data


while(True):
    #read the camera image
    #카메라에서 이미지 얻기
    
    ret, frame = cap.read()

    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayframe = cv2.equalizeHist(grayframe)

    faces = face_cascade.detectMultiScale(grayframe, 1.1, 3, 0, (30, 30))

    if faces is():

        print("0")
    else:

        print("1")

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3, 4, 0)
        

    cv2.imshow('Face',frame)



    #10ms 동안 키입력 대기
    if cv2.waitKey(10) >= 0:

        break;


#close the window
#윈도우 종료
cap.release()
cv2.destroyWindow('Face')
