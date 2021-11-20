import cv2, sys
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt


video = cv2.VideoCapture(0)
prev_time = 1
FPS = 144
prev_time = 1 #카매라
FPS = 144
a = 0

while True:

    ret, frame = video.read()
    current_time = time.time() - prev_time
    now = datetime.datetime.now().strftime("_%H-%M-%S")#현재 시간변수
    cv2.imshow("images", frame)
        if (ret is True) and (current_time > 1. / FPS):
        if cv2.waitKey(1) & 0xFF == ord(" "):
            break
        elif cv2.waitKey(1) & 0xFF == ord("s"):
            print("캡쳐")
            a = str(now)
            cv2.imwrite("/Users/jiminkim/Desktop/Capture/" + str(now) + ".png", frame)
        elif cv2.waitKey(1) & 0xFF == ord("z"):
            print("이미지 테두리 분석")
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            img = cv2.imread("/Users/jiminkim/Desktop/Capture/" + a + ".png")
            img_copy = img.copy()
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)

            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(img, contours, -1, (0, 255, 255), 2)

            c0 = contours[0]
            M = cv2.moments(c0)
            print(M.items())

            plt.title('contour')
            plt.imshow(img)
            plt.axis('off')


            img_copy = img.copy()
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(img_copy, (cx, cy), 15, (255, 0, 0), -1)

            plt.imshow(img_copy)
            plt.title("Contour Center")
            plt.axis("off")
            plt.show()


            leftmost = tuple(c0[c0[:, :, 0].argmin()][0])
            rightmost = tuple(c0[c0[:, :, 0].argmax()][0])
            topmost = tuple(c0[c0[:, :, 1].argmin()][0])
            bottommost = tuple(c0[c0[:, :, 1].argmax()][0])

            cv2.circle(img_copy, (leftmost[0], leftmost[1]), 10, (0, 0, 255), -1)
            cv2.circle(img_copy, (rightmost[0], rightmost[1]), 10, (0, 0, 255), -1)
            cv2.circle(img_copy, (bottommost[0], bottommost[1]), 10, (0, 0, 255), -1)
            cv2.circle(img_copy, (topmost[0], topmost[1]), 10, (0, 0, 255), -1)

            plt.imshow(img_copy)
            plt.title("Extream Point")
            plt.axis("off")
            plt.show()

