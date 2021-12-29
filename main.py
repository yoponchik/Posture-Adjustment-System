#https://www.youtube.com/watch?v=VWUgkcX_KoY
import cv2
import numpy as np
import dlib
from win32api import GetSystemMetrics
from serial import Serial
import time


ser = Serial('com6', 9600)
ser.timeout = 1

##screen size
# print("Screen Size = ", GetSystemMetrics(0), "x", GetSystemMetrics(1))
# height, width = GetSystemMetrics(0), GetSystemMetrics(1)
x1, y1 = 0, 120
x2, y2 = 900, 120
# image = np.ones((height, width)) * 255




cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()

def eye_detection(eyepoints, landmarks):
    eye_region = np.array([(landmarks.part(eyepoints[0]).x, landmarks.part(eyepoints[0]).y),
                           (landmarks.part(eyepoints[1]).x, landmarks.part(eyepoints[1]).y),
                           (landmarks.part(eyepoints[2]).x, landmarks.part(eyepoints[2]).y),
                           (landmarks.part(eyepoints[3]).x, landmarks.part(eyepoints[3]).y),
                           (landmarks.part(eyepoints[4]).x, landmarks.part(eyepoints[4]).y),
                           (landmarks.part(eyepoints[5]).x, landmarks.part(eyepoints[5]).y)], np.int32)

    rectangle = np.array([np.min(eye_region[:, 0]), # takes the first column of the arrays
                          np.max(eye_region[:, 0]), #takes the second column of the arrays
                          np.min(eye_region[:, 1]),
                          np.max(eye_region[:, 1]),
                          np.int32])
    return rectangle



while True:
    _, capture = cap.read()
    #gray_face = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
    predictor = dlib.shape_predictor("face_landmarks.dat")



    faces = detector(capture)
    for face in faces:

        landmarks = predictor(capture, face)
        #cv2.polylines(capture, [left_eye_region], True, (0, 0, 255), 2)   #image, points, close polygon?, color, thickness

        eye_region = eye_detection([36, 37, 38, 44, 45, 46], landmarks)
        # eye_region = capture[eye_region[2]-5 : eye_region[3]+5, eye_region[0]-5: eye_region[1]+5]
        # eye_rectangle = cv2.resize(eye_region, None, fx=5, fy=5)   #resize eye
        # cv2.imshow("Eye Region", eye_rectangle)

        if (eye_region[2] > y1) and  (eye_region[3] > y2):
            print("1") #eyes under the lines
            ser.write("1".encode())
        else:
            print("0") #eyes over the lines
            ser.write("0".encode())

    #cv2.polylines(capture, ) don't need this because we're not making a polygon
    cv2.line(capture, (x1, y1), (x2, y2), (0,255,0), 1)
    cv2.imshow("Frame", capture)

    ##send to Arduino the data
    # val = input('Enter value').strip() #strip gets rid of unneeded spaces
    # ser.write(val.encode())



    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()