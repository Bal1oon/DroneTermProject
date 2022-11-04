import cv2
import pickle
import cvzone
import datetime
import time
import numpy as np

videos = ['carPark.mp4',
         #'carPark2.mp4',
         'carOut.mp4']

positions = ['carParkPos_carPark',
          # 'carParkPos_carPark2',
           'carParkPos_carOut']

wh = {'carPark.mp4': (107, 48),
      #'carPark2.mp4': (110, 60),
      'carOut.mp4': (600, 250)}

weights = [900,
           #900,
           3000]
idx = 0

# Video feed
cap = cv2.VideoCapture(videos[idx])

with open(positions[idx], 'rb') as f:
    posList = pickle.load(f)

width, height = wh[videos[idx]]

root = time.time()

root = time.time()


def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        #cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)

        if count < weights[idx]:
            color = (255, 0, 0)
            thickness = 2
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=1, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Vacant space: {spaceCounter}/{len(posList)}', (230, 50), scale=3,
                       thickness=2, offset=20, colorR=(0, 0, 0))
    return spaceCounter

while True:
    curTime = time.time()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    spaceCounter = checkParkingSpace(imgDilate)
    if spaceCounter > 11 and spaceCounter <= 12 and curTime - root > 1:
        print("Space is 12")
        now = datetime.datetime.now()
        print(now)
        root = curTime
    if spaceCounter > 12 and spaceCounter <= 13 and curTime - root > 1:
        print("Space is 13")
        now = datetime.datetime.now()
        print(now)
        root = curTime
    if spaceCounter > 13 and spaceCounter <= 14 and curTime - root > 1:
        print("Space is 14")
        now = datetime.datetime.now()
        print(now)
        root = curTime
    if spaceCounter > 14 and spaceCounter <= 15 and curTime - root > 1:
        print("Space is 15")
        now = datetime.datetime.now()
        print(now)
        root = curTime
    cv2.imshow("Image", img)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThres", imgMedian)
    cv2.waitKey(10)