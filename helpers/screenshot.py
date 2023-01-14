import cv2
import time


from src.output_fxns import get_window_info, get_full_screen, isDefeat

if __name__ == "__main__":
    #
    window_info = get_window_info()
    time.sleep(2)

    # make sure MTGA resolution is 1920x1080 and full screen
    window_info['width_fullscreen'] = 1920
    window_info['height_fullscreen'] = 1080

    shit, full_screen_img = get_full_screen(window_info)
    (x1, y1) = (722, 140)
    (x2, y2) = (1188, 209)
    img = full_screen_img[y1:y2, x1:x2]

    cv2.imwrite('./test.png', img)
    print('done')
