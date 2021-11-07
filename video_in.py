import sys
import numpy as np
import cv2


# 비디오 파일 열기
cap = cv2.VideoCapture('C:/HH/output3.avi')

if not cap.isOpened():
    print("Video open failed!")
    sys.exit()

fps = cap.get(cv2.CAP_PROP_FPS)
delay = round(1000 / fps)
list=[]

# 비디오 매 프레임 처리
while True:
    ret1, src1 = cap.read()
    ret2, src2 = cap.read()
    if not ret1 or not ret2:
        break

    if cv2.waitKey(delay) == 27:
        break

    gray1 = cv2.cvtColor(src1, cv2.COLOR_BGR2GRAY)

    pt1 = cv2.goodFeaturesToTrack(gray1, 50, 0.01, 10)
    pt2, status, err = cv2.calcOpticalFlowPyrLK(src1, src2, pt1, None)

    dst = cv2.addWeighted(src1, 0.5, src2, 0.5, 0)
    array = []
    max = 0

    for i in range(pt2.shape[0]):
        if status[i, 0] == 0:
            continue

        cv2.circle(dst, tuple(pt1[i, 0].astype(int)),
                4, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.circle(dst, tuple(pt2[i, 0].astype(int)),
                4, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.arrowedLine(dst, tuple(pt1[i, 0].astype(int)), tuple(
            pt2[i, 0].astype(int)), (0, 255, 0), 2)
        ar = pt2[i, 0].astype(int) - pt1[i, 0].astype(int)
        # print(abs(ar))
        ar = abs(ar)
        a = ar[:1]
        b = ar[1:]
        # print(a,' ' ,b)
        if max < (a+b):
            max = a+b
    list.append(max)
    cv2.imshow('dst', dst)

# print(list)
for i in list:
    print(int(i))

cv2.waitKey()
cap.release()
cv2.destroyAllWindows()
