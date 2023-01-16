import cv2
import time
from PIL import ImageGrab
import numpy as np


def get_screenshot(x1, y1, x2, y2):
    # win32gui.SetForegroundWindow(window_info['hwnd'])

    box = (x1, y1, x2, y2)
    screen = ImageGrab.grab(box)
    img = np.array(screen.getdata(), dtype=float).reshape(
        (screen.size[1], screen.size[0], 3))
    img_reversed = img.copy()
    img_reversed[:, :, 0] = img[:, :, 2]
    img_reversed[:, :, 2] = img[:, :, 0]

    return img_reversed


def get_full_screen():
    x1 = 0
    x2 = 1920
    y1 = 0
    y2 = 1080
    return get_screenshot(x1, y1, x2, y2)


if __name__ == "__main__":
    #
    time.sleep(2)

    # make sure MTGA resolution is 1920x1080 and full screen

    full_screen_img = get_full_screen()
    # (x1, y1) = (722, 140)
    # (x2, y2) = (1188, 209)
    # img = full_screen_img[y1:y2, x1:x2]

    cv2.imwrite('./test.png', full_screen_img)
    print('done')
