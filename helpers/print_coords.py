
from src.output_fxns import VIEW_LOCATION_DICT, get_window_info, get_full_screen
from pynput import mouse, keyboard

import time
from numpy import random
from src.input_fxns import print_coord

mouse = mouse.Controller()
kboard = keyboard.Controller()


if __name__ == "__main__":

    window_info = get_window_info()
    while True:
        time.sleep(3)
        print_coord()
