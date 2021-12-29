import cv2
import numpy as np
import dlib
import serial

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()

def eye_detection(eyepoints, landmarks):
    eye_region = np.array([(landmarks.part(eyepoints[0]).x, landmarks.part(eyepoints[0]).y),
                           (landmarks.part(eyepoints[1]).x, landmarks.part(eyepoints[1]).y),
                           (landmarks.part(eyepoints[2]).x, landmarks.part(eyepoints[2]).y),
                           (landmarks.part(eyepoints[3]).x, landmarks.part(eyepoints[3]).y),
                           (landmarks.part(eyepoints[4]).x, landmarks.part(eyepoints[4]).y),
                           (landmarks.part(eyepoints[5]).x, landmarks.part(eyepoints[5]).y)], np.int32)

    rectangle = np.array([np.min(eye_region[:, 0]),
                          np.max(eye_region[:, 0]),
                          np.min(eye_region[:, 1]),
                          np.max(eye_region[:, 1]),
                          np.int32])
    return rectangle

while True:
    _, frame = cap.read()
    screen = frame[0: 500, 0: 750] #size

    predictor = dlib.shape_predictor("face_landmarks.dat")
    faces = detector(frame)

    for face in faces:
        landmarks = predictor(frame, face)

        eye_region =
        left_eye_region = eye_detection([36, 37, 38, 39, 40, 41], landmarks)
        left_eye_region = frame[left_eye_region[2]-5 : left_eye_region[3]+5 , left_eye_region[0]-5: left_eye_region[1]+5 ]
        right_eye_region = eye_detection([42, 43, 44, 45, 46, 47], landmarks)
        right_eye_region = frame[right_eye_region[2] - 5: right_eye_region[3] + 5,
                          right_eye_region[0] - 5: right_eye_region[1] + 5]

        left_eye_rectangle = cv2.resize(left_eye_region, None, fx=5, fy=5)   #resize eye
        right_eye_rectangle = cv2.resize(right_eye_region, None, fx=5, fy=5)   #resize eye

        cv2.imshow("Left Eye", left_eye_rectangle)
        cv2.imshow("Right Eye", right_eye_rectangle)


    cv2.imshow("Frame", frame)



    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()