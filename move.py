import pyautogui
import time
import cv2

def move_around():
    while 1:
        pyautogui.keyDown("right")
        time.sleep(0.2)
        pyautogui.keyDown("left")
        time.sleep(0.2)
        pyautogui.keyUp("right")
        pyautogui.keyUp("left")
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

time.sleep(1)
move_around()