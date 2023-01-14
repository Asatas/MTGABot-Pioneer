import cv2
import time
import numpy as np


from src.output_fxns import get_window_info, get_full_screen


VIEW_LOCATION_DICT = {
    'TEST_IMAGE_C1': (978, 141),
    'TEST_IMAGE_C2': (1015, 208),
    'HOME_MENU_C1': (71, 0),
    'HOME_MENU_C2': (318, 100),
    'KEEP_HAND_C1': (1008, 834),
    'KEEP_HAND_C2': (1265, 922),
    'PASS_BUTTON_C1': (1672, 923),
    'PASS_BUTTON_C2': (1722, 978),
    'BLOCK_BUTTON_C1': (1672, 923),
    'BLOCK_BUTTON_C2': (1722, 978),
    'VIEW_BATTLEFIELD_C1': (1672, 23),
    'VIEW_BATTLEFIELD_C2': (1722, 78),
    'BLACK_BAR_C1': (0, 23),
    'BLACK_BAR_C2': (1920, 78),
    'DIALOG_DONE_BUTTON_C1': (830, 850),
    'DIALOG_DONE_BUTTON_C2': (1090, 900),
    'DEFEAT_C1': (880, 517),
    'DEFEAT_C2': (1034, 579),
}

REF_IMG_DICT = {
    'TEST_IMAGE': cv2.imread('./ref_images/test_image_1.png'),
    'BLOCK_BUTTON': cv2.imread('./ref_images/BLOCK_BUTTON.png'),
    'corner_mask_0': cv2.imread('./ref_images/corner_mask_0.png'),
    'corner_mask_1': cv2.imread('./ref_images/corner_mask_1.png'),
    'corner_mask': cv2.imread('./ref_images/corner_mask.png'),
    'HOME_MENU': cv2.imread('./ref_images/HOME_MENU.png'),
    'KEEP_HAND': cv2.imread('./ref_images/KEEP_HAND.png'),
    'PASS_BUTTON': cv2.imread('./ref_images/PASS_BUTTON.png'),
    'VIEW_BATTLEFIELD': cv2.imread('./ref_images/VIEW_BATTLEFIELD.png'),
    'BLACK_BAR': cv2.imread('./ref_images/BLACK_BAR.png'),
    'DIALOG_DONE_BUTTON': cv2.imread('./ref_images/blockers_done.png'),
    'DEFEAT': cv2.imread('./ref_images/DEFEAT.png'),
}


def onScreen(element_to_look_for, full_screen_img, cutoff=10000, save_img=False):
    (x1, y1) = VIEW_LOCATION_DICT[f'{element_to_look_for}_C1']
    (x2, y2) = VIEW_LOCATION_DICT[f'{element_to_look_for}_C2']
    img = full_screen_img[y1:y2, x1:x2]
    if save_img:
        print('saving example image:')
        cv2.imwrite(f'test_{element_to_look_for}.png', img)
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
    window_info = get_window_info()

    # make sure MTGA resolution is 1920x1080 and full screen
    window_info['width_fullscreen'] = 1920
    window_info['height_fullscreen'] = 1080

    counter = 0
    max_pixel_dist = 0
    for x in range(50):
        active, full_screen_img = get_full_screen(window_info)

        if (not active):
            print('INACTIVE SCREEN DETECTED')
        else:

            is_on_screen, pixel_dist = onScreen(
                'TEST_IMAGE', full_screen_img, cutoff=10000)

            print(
                is_on_screen,  pixel_dist
            )

            counter += 1
            if (pixel_dist > max_pixel_dist):
                max_pixel_dist = pixel_dist
            # time.sleep(0.2)
    print('max_pixel_dist: ', max_pixel_dist)
