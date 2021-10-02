import cv2
import time
import datetime
import numpy as np

video = cv2.VideoCapture(0)
# 비디오 파일의 경우 '경로/파일명.확장자'

prev_time = 1
FPS = 144
a = 0

while True:

    ret, frame = video.read()
    frame = cv2.flip(frame, 1)

    current_time = time.time() - prev_time

    if (ret is True) and (current_time > 1. / FPS):

        prev_time = time.time()

        cv2.imshow('VideoCapture', frame)

        now = datetime.datetime.now().strftime("_%H-%M-%S")
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
        elif k == 26:
            print("캡쳐")
            a = str(now)
            cv2.imwrite("/Users/jiminkim/Desktop/Capture/" + str(now) + ".png", frame)
        elif k == 24:
            print("최근 파일 색상 검출")
            img_color = cv2.imread('/Users/jiminkim/Desktop/Capture/' + a + '.png')
            print('shape: ', img_color.shape)
            height, width = img_color.shape[:2]
            img_hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)

            lower_blue = (120-10, 30, 30)#R:140 G:120 B:100
            upper_blue = (120+10, 255, 255)#R:220 G:200 B:170
            img_mask = cv2.inRange(img_hsv, lower_blue, upper_blue)

            img_result = cv2.bitwise_and(img_color, img_color, mask=img_mask)
            cv2.imshow('img_origin', img_color)
            cv2.imshow('img_mask', img_mask)
            cv2.imshow('img_color', img_result)
        elif k == 3:
            print("최근 파일 모서리 검출")
            img = cv2.imread('/Users/jiminkim/Desktop/Capture/' + a + '.png', cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #모서리 검출
            corner = cv2.cornerHarris(gray, 2, 3, 0.16)
            #10% 지표구하기
            coord = np.where(corner > 0.05 * corner.max())
            coord = np.stack((coord[1], coord[0]), axis=-1)

            for x, y in coord:
                cv2.circle(img, (x, y), 5, (0, 0, 255), 1, cv2.LINE_AA)

            corner_norm = cv2.normalize(corner, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

            corner_norm = cv2.cvtColor(corner_norm, cv2.COLOR_GRAY2BGR)
            merged = np.hstack((corner_norm, img))
            cv2.imshow('Harris Corner', merged)
            cv2.waitKey()
            cv2.destroyAllWindows()



#img_color = cv2.imread(str(now) + '.png')  # 이미지 파일을 컬러로 불러옴
#print('shape: ', img_color.shape)
# 색 추출 -> 형태인식 -> 꼭직점 인식 -> 비율 비교 -> 출력
