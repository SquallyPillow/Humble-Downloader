import pyautogui
import time
import os


def save_active_window(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    dir_path = os.path.join(dir_path, file_name)

    input('Will now save the HTML, hit enter and then you have 5 seconds to click on the window with the bundle.')
    for i in range(5):
        print('{}{}'.format(5 - i, '...'), end='')
        time.sleep(1)
    print()
    print()

    pyautogui.hotkey('CTRL', 's')
    time.sleep(1)
    pyautogui.typewrite(dir_path)
    pyautogui.press('enter')
