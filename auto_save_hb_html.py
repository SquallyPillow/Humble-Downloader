import pyautogui
import time


def save_active_window(file_name):
    pyautogui.hotkey('CTRL', 's')
    time.sleep(1)
    pyautogui.typewrite(file_name)
    pyautogui.press('enter')
