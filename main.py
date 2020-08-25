import time

import cv2
import mss
import numpy as np
import pyautogui
import subprocess

pyautogui.FAILSAFE = False
move_process = False
onmount = False
login = True
is_hunting_place = True

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

def character_move(command, steps):
    print("CMD: %s, steps: %s" % (command, steps))
    while steps:
        print(command)
        pyautogui.press([command])
        time.sleep(0.3)
        steps -= 1

def start_to_move():
    global move_process
    if not move_process or move_process.poll() == 1:
        move_process = subprocess.Popen(['C:\\Users\\Duong Long\\Desktop\\autopro\\venv\\Scripts\\python.exe',
                          "C:\\Users\\Duong Long\\Desktop\\autopro\\move.py"],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
start_to_move()

with mss.mss() as sct:
    # Capture a bbox using percent values
    monitor = sct.monitors[1]
    while "Screen capturing":
        last_time = time.time()
        # Get raw pixels from the screen, save it to a Numpy array
        img_rgb = np.array(sct.grab(monitor))
        found_login = detect_object("login")
        found_loading = detect_object("loading")
        if found_login:
            move_process.kill()
            move_process.terminate()
            login = False
            onmount = False
            pyautogui.moveTo(found_login[0] - 30, found_login[1] - 10, 0)
            pyautogui.click()
        elif not found_loading:
            login = True
            found_guard = detect_object("guard")
            if found_guard:
                is_hunting_place = False
            else:
                if is_hunting_place:
                    start_to_move()
        # Display the picture
        # cv2.imshow("OpenCV/Numpy normal", img_rgb)
        if not is_hunting_place:
            if found_guard:
                pyautogui.press(["left"])
                time.sleep(0.2)
                pyautogui.press(["right"])
                character_move("s", 5)
                time.sleep(3)
            found_mail_box = detect_object("mailbox")
            if found_mail_box:
                print("Moving")
                character_move("right", 5)
                character_move("up", 12)
                character_move("right", 3)
            found_npc = detect_object("npc")
            if found_npc:
                is_hunting_place = True
                character_move("right", 3)
                character_move("up", 2)

            # found_at_hunting_place = detect_object("at_hunting_place")
            # if found_at_hunting_place:
            #     is_hunting_place = True

        if login and is_hunting_place:
            if not onmount:
                found_mount = detect_object("mount_icon")
                print("going to mount")
                if found_mount:
                    pyautogui.moveTo(found_mount[0] - 10, found_mount[1] - 10, 0)
                    pyautogui.click()
                    print("click on mount")
                    onmount = True
            to_catch = [
                # "machop_day",
                # "machop_night",
                "bulba_night",
                "bulba_day",
                "charmander",
                "bagon_day",
                "bagon_night",
                "mediate",
                "scyther",
                "scyther_day",
                "swablu_day",
            ]
            found_poke = False
            for poke in to_catch:
                found_poke = detect_object(poke)
                if found_poke:
                    print("Found %s !!!" % poke)
                    found_chansey_battle = detect_object("chansey_battle_day")
                    if not found_chansey_battle:
                        found_chansey_battle = detect_object("chansey_battle_night")
                    if not found_chansey_battle:
                        pyautogui.press(["2"])
                        pyautogui.press(["2"])
                        print("Changed to chansey")
                        time.sleep(2)
                    found_bag = detect_object("bag")
                    if found_bag:
                        pyautogui.moveTo(found_bag[0] - 50, found_bag[1] - 30, 0)
                        pyautogui.click()
                        found_greatball = detect_object("greatball")
                        print("catching poke")
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

            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
