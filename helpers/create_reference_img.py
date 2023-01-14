import cv2
import time

from waiting import wait

from src.output_fxns import VIEW_LOCATION_DICT, get_window_info, get_full_screen

if __name__ == "__main__":

    window_info = get_window_info()

    # make sure MTGA resolution is 1920x1080 and full screen
    window_info['width_fullscreen'] = 1920
    window_info['height_fullscreen'] = 1080
    print('sleeping')
    time.sleep(1)
    print(
        'go'
    )

    active, full_screen_img = get_full_screen(window_info)

    element_to_look_for = 'HOME_MENU'
    (x1, y1) = VIEW_LOCATION_DICT[f'{element_to_look_for}_C1']
    (x2, y2) = VIEW_LOCATION_DICT[f'{element_to_look_for}_C2']
    img = full_screen_img[y1:y2, x1:x2]

    print(img)

    cv2.imwrite('./test.png', img)
