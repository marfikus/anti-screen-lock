
import win32api
import time
# from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller


MAX_COUNT = 55
count = 0
prev_last_input_info = 0

# mouse = Controller()
keyboard = Controller()

def blink_caps_lock():
    keyboard.press(Key.caps_lock)
    keyboard.release(Key.caps_lock)
    # time.sleep(0.2)
    keyboard.press(Key.caps_lock)
    keyboard.release(Key.caps_lock)


# def move_mouse(back):
#     if back:
#         mouse.move(-100, 0)
#     else:
#         mouse.move(100, 0)

# mouse_moved = False

while True:
    last_input_info = win32api.GetLastInputInfo()
    # print(last_input_info)

    # if mouse_moved:
    #     move_mouse(back=True)
    #     mouse_moved = False

    if last_input_info == prev_last_input_info:
        count += 1
        if count == MAX_COUNT:
            print("lock screen time!")
            # move_mouse(back=False)
            # mouse_moved = True
            # count = 0
            blink_caps_lock()

    else:
        count = 0

    prev_last_input_info = last_input_info


    time.sleep(1)