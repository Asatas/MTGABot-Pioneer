import cv2
import time
import numpy as np
from PIL import ImageGrab


VIEW_LOCATION_DICT = {
    "TEST_IMAGE_C1": (903, 497),
    "TEST_IMAGE_C2": (967, 580),
}

REF_IMG_DICT = {
    "TEST_IMAGE": cv2.imread("./test_images/test_image_1.png"),
}


def get_screenshot(x1, y1, x2, y2):
    # win32gui.SetForegroundWindow(window_info['hwnd'])

    box = (x1, y1, x2, y2)
    screen = ImageGrab.grab(box)
    img = np.array(screen.getdata(), dtype=float).reshape(
        (screen.size[1], screen.size[0], 3)
    )
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


def onScreen(element_to_look_for, full_screen_img, cutoff=10000, save_img=False):
    (x1, y1) = VIEW_LOCATION_DICT[f"{element_to_look_for}_C1"]
    (x2, y2) = VIEW_LOCATION_DICT[f"{element_to_look_for}_C2"]
    img = full_screen_img[y1:y2, x1:x2]
    if save_img:
        print("saving example image:")
        cv2.imwrite(f"test_{element_to_look_for}.png", img)
    ref_img = REF_IMG_DICT[element_to_look_for]
    return areImgsSimilar(img, ref_img, cutoff=cutoff)


def areImgsSimilar(img1, img2, cutoff=10000):

    pixel_distance = np.sqrt(sum(np.square(img1.ravel() - img2.ravel())))

    if pixel_distance < cutoff:
        return True, pixel_distance
    else:
        return False, pixel_distance


if __name__ == "__main__":
    time.sleep(1)

    counter = 0
    max_pixel_dist = 0
    for x in range(50):
        full_screen_img = get_full_screen()

        is_on_screen, pixel_dist = onScreen(
            "TEST_IMAGE", full_screen_img, cutoff=10000)

        print(is_on_screen, pixel_dist)

        counter += 1
        if pixel_dist > max_pixel_dist:
            max_pixel_dist = pixel_dist
        # time.sleep(0.2)
    print("max_pixel_dist: ", max_pixel_dist)
