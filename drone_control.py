import face_recognition
import cv2
import numpy as np
from utils import *
import time
from threading import Thread
import datetime

keepRecording = True
recorder = 0


def videoRecorder():
    height, width, _ = frame_read.frame.shape
    now = datetime.datetime.now()
    video = cv2.VideoWriter(f'record/video {now}.mp4', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()

myDrone = initTello()
myDrone.takeoff()
time.sleep(1)
myDrone.streamon()
frame_read = myDrone.get_frame_read()
time.sleep(2)

# # Load a sample picture and learn how to recognize it.
# obama_image = face_recognition.load_image_file("obama.jpg")
# obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# # Load a second sample picture and learn how to recognize it.
# biden_image = face_recognition.load_image_file("biden.jpg")
# biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Load a picture and learn how to recognize it
shin_image = face_recognition.load_image_file("face/Shin.jpeg")
shin_face_encoding = face_recognition.face_encodings(shin_image)[0]
lee_image = face_recognition.load_image_file("face/Lee.jpg")
lee_face_encoding = face_recognition.face_encodings(lee_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
#    obama_face_encoding,
#    biden_face_encoding,
    shin_face_encoding,
    lee_face_encoding
]
known_face_names = [
#    "Barack Obama",
#    "Joe Biden",
    "Junyoung Shin",
    "Wooseok Lee"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

administrators = known_face_names.copy()
control = True
adminOK = False
num = 0

while True:
    # Grab a single frame of video
    frame = frame_read.frame

    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            min_value = min(distances)

            # tolerance: How much distance between faces to consider it a match. Lower is more strict.
            # 0.6 is typical best performance.
            name = "Unknown"
            if min_value < 0.4:
                index = np.argmin(distances)
                name = known_face_names[index]

            face_names.append(name)

        # Once administrator is passed, if-statement does not work
        if not adminOK:
            for name in face_names:
                if adminOK: break
                for administrator in administrators:
                    if name == administrator:
                        adminOK = True
                        print("Administrator Pass. Keep Controlling")
                        break
                    if name == "Unknown":
                        control = False
                        print("Detect unknown. Landing")

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Terminate the program if not administer
    if not control:
        myDrone.land()
        break

    # Start recording
    if recorder == 0:
        recorder = Thread(target=videoRecorder)
        recorder.start()

    # Control the drone with keyboard
    keyboard = cv2.waitKey(1)
    if keyboard & 0xFF == ord('q'):
        myDrone.land()
        break
    if keyboard == ord('t'):
        frame = frame_read.frame
        height, width, layers = frame.shape
        new_h = int(height / 2)
        new_w = int(width / 2)
        resize = cv2.resize(frame, (new_w, new_h))
        cv2.imwrite(f"captures/capture{num}.jpg", resize)
        print("Take Picture")
        num+=1
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

frame_read.stop()
myDrone.streamoff()
keepRecording = False
recorder.join()
cv2.destroyAllWindows()
