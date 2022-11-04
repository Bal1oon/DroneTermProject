from djitellopy import Tello
import cv2
import time

def initTello():
    myDrone = Tello()
    myDrone.connect()

    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0

    # myDrone.streamoff()

    return myDrone
