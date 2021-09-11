#python -m pip install opencv-python 필요
import cv2
import time
import datetime

video = cv2.VideoCapture(0)  # WebCam의 경우 0 또는 1
# 비디오 파일의 경우 '경로/파일명.확장자'

prev_time = 1
FPS = 144

while True:

    ret, frame = video.read()
    frame = cv2.flip(frame, 1)

    current_time = time.time() - prev_time

    if (ret is True) and (current_time > 1. / FPS):

        prev_time = time.time()

        cv2.imshow('VideoCapture', frame)

        cv2.waitKey(1)
        now = datetime.datetime.now().strftime("%m월/%d일_%H-%M-%S")
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        elif k == 26:
            print("캡쳐")
            cv2.imwrite("/Users/jiminkim/Desktop/C/" + str(now) + ".png", frame)
