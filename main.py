import time

import cv2
import mss
import numpy as np
import pyautogui

def detect_object(pokename):
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("%s.png" % pokename, 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    if len(loc[0]) > 0:
        for pt in zip(*loc[::-1]):
            return (pt[0] + w, pt[1] + h)
            # pyautogui.moveTo(pt[0] + w - 50, pt[1] + h - 30, 0)
            # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        # cv2.imwrite('res.png', img_rgb)
        return loc
    return []

command = "left"
pyautogui.FAILSAFE = False

def toggle_command():
    global command
    if command == "left":
        command = "right"
    else:
        command = "left"

with mss.mss() as sct:
    # Capture a bbox using percent values
    monitor = sct.monitors[1]
    while "Screen capturing":
        last_time = time.time()
        # Get raw pixels from the screen, save it to a Numpy array
        img_rgb = np.array(sct.grab(monitor))

        # Display the picture
        # cv2.imshow("OpenCV/Numpy normal", img_rgb)

        found_char = detect_object("charmander")
        if found_char:
            print("Found Charmander !!!")
            found_bag = detect_object("bag")
            if found_bag:
                pyautogui.moveTo(found_bag[0] - 50, found_bag[1] - 30, 0)
                pyautogui.click()
                found_greatball = detect_object("greatball")
                if found_greatball:
                    pyautogui.moveTo(found_greatball[0] - 30, found_greatball[1] - 15 , 0)
                    pyautogui.click()
                else:
                    found_pokeball = detect_object("pokeball")
                    if found_pokeball:
                        pyautogui.moveTo(found_pokeball[0], found_pokeball[1], 0)
                        pyautogui.click()

        found_sync = detect_object("kadabra")
        if not found_sync:
            found_sync = detect_object("xatu")

        if found_sync and not found_char:
            pyautogui.press(["4"])

        found_sync_icon = detect_object("kadabra_icon")
        if not found_sync_icon:
            found_sync_icon = detect_object("xatu_icon")
        if not found_char and not found_sync and found_sync_icon:
            pyautogui.keyDown(command)
            pyautogui.keyDown(command)
            pyautogui.keyDown(command)
            pyautogui.keyUp(command)
            pyautogui.keyDown("right")
            pyautogui.keyDown("right")
            pyautogui.keyDown("right")
            pyautogui.keyUp("right")
            # toggle_command()

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break