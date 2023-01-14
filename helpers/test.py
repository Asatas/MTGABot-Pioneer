import random
import cv2
import time
from pynput import mouse, keyboard

from src.output_fxns import get_window_info, get_full_screen, get_hand_region, locate_leftmost_playable_card
mouse = mouse.Controller()
kboard = keyboard.Controller()

if __name__ == "__main__":
    time.sleep(2)
    window_info = get_window_info()
    isPlayableCard, leftmost_pt_full_image = locate_leftmost_playable_card(
        window_info)
    print(isPlayableCard, leftmost_pt_full_image)

    for x in range(20):
        mouse.position = 500, 500
        time.sleep(0.2)
        x1 = leftmost_pt_full_image[0]
        y1 = leftmost_pt_full_image[1]
        if x1 > 500:
            x1 += random.randint(70, 150)
        elif x1 < 500:
            x1 += random.randint(40, 100)
            y1 += random.randint(10, 50)

        mouse.position = x1, y1
        time.sleep(0.3)
