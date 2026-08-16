import cv2
import os
import time
import numpy as np

CAMERA_INDEX = 1
FACE_FILE = "sangeeth_face.jpg"

def capture_image():
    cam = cv2.VideoCapture(CAMERA_INDEX)

    if not cam.isOpened():
        return None

    time.sleep(1)

    ret, frame = cam.read()
    cam.release()

    if not ret:
        return None

    return frame

def register_face():
    frame = capture_image()

    if frame is None:
        return False, "Could not access camera."

    cv2.imwrite(FACE_FILE, frame)

    return True, "Face registered successfully."

def compare_images(image1, image2):
    image1 = cv2.resize(image1, (300, 300))
    image2 = cv2.resize(image2, (300, 300))

    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    difference = cv2.absdiff(gray1, gray2)
    score = np.mean(difference)

    return score

def verify_face():
    if not os.path.exists(FACE_FILE):
        return False, "No registered face found. Please register your face first."

    saved_face = cv2.imread(FACE_FILE)

    if saved_face is None:
        return False, "Saved face image is not readable."

    live_face = capture_image()

    if live_face is None:
        return False, "Could not access camera."

    score = compare_images(saved_face, live_face)

    print("Face match score:", score)

    if score < 90:
        return True, "Face verified successfully."
    else:
        return False, "Access denied. Face does not match."