import pyautogui
import time

def move_around():
    while 1:
        pyautogui.keyDown("right")
        time.sleep(0.5)
        pyautogui.keyDown("left")
        time.sleep(0.5)
        pyautogui.keyUp("right")
        pyautogui.keyUp("left")

time.sleep(1)
move_around()