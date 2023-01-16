import random
import time
import win32gui
from scipy import ndimage
import cv2
import numpy as np
from PIL import ImageGrab
from pynput import mouse

from screen.screen import locate_leftmost_playable_card
mouse = mouse.Controller()


if __name__ == "__main__":
    time.sleep(2)
    isPlayableCard, leftmost_pt_full_image = locate_leftmost_playable_card()
    print(isPlayableCard, leftmost_pt_full_image)
    mouse.position = leftmost_pt_full_image
    time.sleep(1)
    if isPlayableCard:
        for x in range(20):
            x1 = leftmost_pt_full_image[0]
            y1 = leftmost_pt_full_image[1]

            if x1 <= 450:
                x1 += random.randint(50, 100)
            else:
                x1 += random.randint(50, 100)
                y1 += random.randint(20, 30)

            mouse.position = (x1, y1)
            print('New values X: ', x1, ' Y: ', y1)
            time.sleep(0.5)
