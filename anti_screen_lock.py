
import os
import win32api
import time
from pynput.keyboard import Key, Controller
import configparser


CONFIG_FILE = "anti_screen_lock.ini"
DEFAULT_CONFIG = {
    # 30 x 6 = 180 seconds = 3 min
    "main_cycle_delay": 30,
    "max_count": 6,
    "blink_caps_lock_delay": 0.0,
    "debug_print": True,
}
config = {}

def load_config():
    global config

    def load_key(parser, key, type="str"):
        try:
            if type == "str":
                value = parser["DEFAULT"][key]
            elif type == "int":
                value = int(parser["DEFAULT"][key])
            elif type == "float":
                value = float(parser["DEFAULT"][key])
            elif type == "bool":
                value = bool(int(parser["DEFAULT"][key]))
        except KeyError:
            print(f"No key '{key}' in config file! Loaded from DEFAULT_CONFIG")
            value = DEFAULT_CONFIG[key]    

        return value


    if not os.path.exists(CONFIG_FILE):
        print("Config file not found! Loaded DEFAULT_CONFIG")
        config = DEFAULT_CONFIG
        return

    parser = configparser.ConfigParser()
    parser.read(CONFIG_FILE, encoding="utf-8")

    config["main_cycle_delay"] = load_key(parser, "main_cycle_delay", "int")
    config["max_count"] = load_key(parser, "max_count", "int")
    config["blink_caps_lock_delay"] = load_key(parser, "blink_caps_lock_delay", "float")
    config["debug_print"] = load_key(parser, "debug_print", "bool")

keyboard = None

def blink_caps_lock():
    keyboard.press(Key.caps_lock)
    keyboard.release(Key.caps_lock)
    if config["blink_caps_lock_delay"] > 0:
        time.sleep(config["blink_caps_lock_delay"])
    keyboard.press(Key.caps_lock)
    keyboard.release(Key.caps_lock)


def main():
    load_config()
    print(config)
    update_interval = config["main_cycle_delay"] * config["max_count"]
    print(f"Update interval: {update_interval} second(s)")

    global keyboard
    keyboard = Controller()

    count = 0
    prev_last_input_info = 0

    while True:
        last_input_info = win32api.GetLastInputInfo()

        if last_input_info == prev_last_input_info:
            count += 1
            if count == config["max_count"]:
                if config["debug_print"]:
                    print("Update time!")
                blink_caps_lock()
        else:
            count = 0

        prev_last_input_info = last_input_info
        time.sleep(config["main_cycle_delay"])


if __name__ == "__main__":
    main()