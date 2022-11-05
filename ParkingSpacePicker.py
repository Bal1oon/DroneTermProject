import cv2
# 모든 주차 공간들을 저장한 후 main.py에 전송
import pickle

images = ['images/carParkImg.png',
         #'images/carPark2Img.png',
         'images/carOutImg.png']

positions = ['pos/carParkPos_carPark',
          # 'pos/carParkPos_carPark2',
           'pos/carParkPos_carOut']

wh = {'images/carParkImg.png': (107, 48),
      #'images/carPark2Img.png': (107, 48),
      'images/carOutImg.png': (600, 250)}

idx = 0
#이미지에서 주차 공간 한 칸의 길이와 높이
width, height = wh[images[idx]]

try:
    with open(positions[idx], 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    #왼쪽 클릭을 했을 때 원하는 주차공간에 대한 설정이 가능하게 한다.
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    # 오른쪽 클릭을 했을 때 잘못된 position에 대한 주차 공간을 삭제할 수 있다.
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open(positions[idx], 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread(images[idx])
    # 주차 공간 하나의 크기를 정하는 for loop
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 255, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#test1