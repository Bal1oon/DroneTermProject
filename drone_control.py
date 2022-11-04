from utils import *
import time
import cv2
from threading import Thread

keepRecording = True
recorder = 0

def videoRecorder():
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()

if __name__ == "__main__":
    myDrone = initTello()
    myDrone.takeoff()
    time.sleep(1)
    myDrone.streamon()
    cv2.namedWindow("drone")
    frame_read = myDrone.get_frame_read()
    time.sleep(2)

    while True:
        img = frame_read.frame
        cv2.imshow("drone", img)
        if recorder == 0:
            recorder = Thread(target=videoRecorder)
            recorder.start()

        keyboard = cv2.waitKey(1)
        if keyboard & 0xFF == ord('q'):
            myDrone.land()
            frame_read.stop()
            myDrone.streamoff()
            keepRecording = False
            recorder.join()
            exit(0)
            break
        if keyboard == ord('w'):
            myDrone.move_forward(20)
        if keyboard == ord('s'):
            myDrone.move_back(20)
        if keyboard == ord('a'):
            myDrone.move_left(20)
        if keyboard == ord('d'):
            myDrone.move_right(20)
        if keyboard == ord('u'):
            myDrone.move_up(20)
        if keyboard == ord('p'):
            myDrone.move_down(20)
        if keyboard == ord('c'):
            myDrone.rotate_clockwise(30)
        if keyboard == ord('v'):
            myDrone.rotate_counter_clockwise(30)