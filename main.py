import time

import cv2
import mss
import numpy as np


with mss.mss() as sct:
    # Capture a bbox using percent values
    monitor = sct.monitors[1]
    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img_rgb = np.array(sct.grab(monitor))

        # Display the picture
        cv2.imshow("OpenCV/Numpy normal", img_rgb)

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

        # img_rgb = cv2.imread('larger.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('smaller.png', 0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        print(loc)
        if len(loc[0]) > 0:
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

            cv2.imwrite('res.png', img_rgb)

