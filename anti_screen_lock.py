
import win32api
import time
from pynput.keyboard import Key, Controller


MAX_COUNT = 55
count = 0
prev_last_input_info = 0

keyboard = Controller()

def blink_caps_lock():
    keyboard.press(Key.caps_lock)
    keyboard.release(Key.caps_lock)
    # time.sleep(0.2)
    keyboard.press(Key.caps_lock)
    keyboard.release(Key.caps_lock)


while True:
    last_input_info = win32api.GetLastInputInfo()

    if last_input_info == prev_last_input_info:
        count += 1
        if count == MAX_COUNT:
            # print("lock screen time!")
            blink_caps_lock()
    else:
        count = 0

    prev_last_input_info = last_input_info
    time.sleep(1)
