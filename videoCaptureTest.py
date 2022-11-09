import cv2

#비디오 캡쳐 py 파일
video = cv2.VideoCapture(0)

ret = False
scale = 2

i=0

while True:
    ret, frame = video.read()
    if (ret):
        # Our operations on the frame come here
        height, width, layers = frame.shape
        new_h = int(height / scale)
        new_w = int(width / scale)
        resize = cv2.resize(frame, (new_w, new_h))  # <- resize for improved performance
        # Display the resulting frame
        cv2.imshow('Tello', resize)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(f"captures/test{i}.jpg", resize)  # writes image test.bmp to disk
        print("Take Picture")
        i+=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()