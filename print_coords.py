
from output_fxns import VIEW_LOCATION_DICT, get_window_info, get_full_screen
from pynput import mouse, keyboard

import time
from numpy import random
from input_fxns import CLICK_LOCATION_DICT

mouse = mouse.Controller()
kboard = keyboard.Controller()


if __name__ == "__main__":

    window_info = get_window_info()

    item = 'PLAY_GAME'
    (x, y) = CLICK_LOCATION_DICT[item]
    mouse.position = (x, y)
