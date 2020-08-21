import time

import cv2
import mss
import numpy as np
import pyautogui
import subprocess

pyautogui.FAILSAFE = False


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

time.sleep(1)
move_process = subprocess.Popen(['C:\\Users\\Duong Long\\Desktop\\autopro\\venv\\Scripts\\python.exe',
                         "C:\\Users\\Duong Long\\Desktop\\autopro\\move.py"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
onmount = False
login = False
with mss.mss() as sct:
    # Capture a bbox using percent values
    monitor = sct.monitors[1]
    while "Screen capturing":
        last_time = time.time()
        # Get raw pixels from the screen, save it to a Numpy array
        img_rgb = np.array(sct.grab(monitor))
        found_login = detect_object("login")
        found_sync = detect_object("kadabra_r10")
        if found_login:
            login = False
            onmount = False
            pyautogui.moveTo(found_login[0] - 30, found_login[1] - 10, 0)
            pyautogui.click()

        elif found_sync:
            login = True
        # Display the picture
        # cv2.imshow("OpenCV/Numpy normal", img_rgb)4
        if not onmount:
            found_mount = detect_object("mount_icon")
            print("going to mount")
            if found_mount:
                pyautogui.moveTo(found_mount[0] - 10, found_mount[1] - 10, 0)
                pyautogui.click()
                print("click on mount")
                onmount = True
        to_catch = ["charmander", "bagon_day", "bagon_night", "mediate", "scyther", "scyther_day", "swablu_day"]
        found_poke = False
        for poke in to_catch:
            found_poke = detect_object(poke)
            if found_poke:
                print("Found %s !!!" % poke)
                found_bag = detect_object("bag")
                if found_bag:
                    pyautogui.moveTo(found_bag[0] - 50, found_bag[1] - 30, 0)
                    pyautogui.click()
                    found_greatball = detect_object("greatball")
                    if found_greatball:
                        pyautogui.moveTo(found_greatball[0] - 30, found_greatball[1] - 15, 0)
                        pyautogui.click()
                    else:
                        found_pokeball = detect_object("pokeball")
                        if found_pokeball:
                            pyautogui.moveTo(found_pokeball[0], found_pokeball[1], 0)
                            pyautogui.click()
                break
        found_sync = detect_object("kadabra_r10")
        if not found_sync:
            found_sync = detect_object("kadabra_r210_2")
        found_change_sync = detect_object("change_sync")
        if found_change_sync:
            pyautogui.moveTo(found_change_sync[0] - 10, found_change_sync[1] -10, 0)
            pyautogui.click()
        if found_sync and not found_poke:
            pyautogui.press(["4"])

        found_sync_icon = detect_object("kadabra_r10_icon")

        if not found_sync_icon:
            found_sync_icon = detect_object("mew_icon")
        if not found_poke and not found_sync and found_sync_icon:
            pass
            # pyautogui.keyDown(command)
            # pyautogui.keyDown(command)
            # pyautogui.keyDown(command)
            # pyautogui.keyUp(command)
            # pyautogui.keyDown("right")
            # pyautogui.keyDown("right")
            # pyautogui.keyDown("right")
            # pyautogui.keyUp("right")
            # toggle_command()

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
