# camera_test.py

import cv2

for i in range(5):
    print(f"Testing camera {i}")

    cam = cv2.VideoCapture(i)

    if cam.isOpened():
        ret, frame = cam.read()

        if ret:
            cv2.imshow(f"Camera {i}", frame)
            print(f"Camera {i} works")

            cv2.waitKey(5000)
            cv2.destroyAllWindows()

        cam.release()