import cv2
import time
import numpy as np
from PIL import ImageGrab


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


NUM_IMAGES_TO_GET = 2
NUM_TESTS_PER_IMAGE = 10


VIEW_LOCATION_DICT = {
    'FIND_C1': (867, 445),
    'FIND_C2': (1044, 467),
}


def onScreen(ref_img, full_screen_img, cutoff=10000):
    (x1, y1) = VIEW_LOCATION_DICT[f'FIND_C1']
    (x2, y2) = VIEW_LOCATION_DICT[f'FIND_C2']
    img = full_screen_img[y1:y2, x1:x2]
    return areImgsSimilar(img, ref_img, cutoff=cutoff)


def areImgsSimilar(img1, img2, cutoff=10000):
    pixel_distance = np.sqrt(sum(np.square(img1.ravel() - img2.ravel())))

    if pixel_distance < cutoff:
        return True, pixel_distance
    else:
        return False, pixel_distance


if __name__ == "__main__":
    time.sleep(1)

    all_tests = {}
    test_counter = 0

    for x in range(NUM_IMAGES_TO_GET):

        full_screen_img = get_full_screen()
        test_counter += 1
        img_path_name = './test_images/test_image_' + \
            str(test_counter) + '.png'
        img_name = 'test_image_' + str(test_counter) + '.png'
        (x1, y1) = VIEW_LOCATION_DICT[f'FIND_C1']
        (x2, y2) = VIEW_LOCATION_DICT[f'FIND_C2']
        test_img = full_screen_img[y1:y2, x1:x2]
        cv2.imwrite(img_path_name, test_img)

        # testing image now
        counter = 0
        max_pixel_dist = 0
        for x in range(NUM_TESTS_PER_IMAGE):
            full_screen_img = get_full_screen()
            is_on_screen, pixel_dist = onScreen(
                cv2.imread(img_path_name), full_screen_img)
            # print(is_on_screen,  pixel_dist)
            counter += 1
            if (pixel_dist > max_pixel_dist):
                max_pixel_dist = pixel_dist
            print('Tested ', img_name, 'pixel_dist ', pixel_dist)

        # testing for image complete
        print('Testing complete for: ', img_name, ' tests ran: ',
              counter, 'max_pixel_distance: ', max_pixel_dist)
        all_tests[img_name] = (counter, max_pixel_dist)

    print('All test results: ', all_tests)

    best_pic_pixel_dist = 999999999999
    best_pic = ''
    for key in all_tests:
        (count, pix) = all_tests[key]
        if (count > 5 and pix < best_pic_pixel_dist):
            best_pic = key
            best_pic_pixel_dist = pix

    print('All testing complete, tests ran: ',
          test_counter, 'best_picture: ', best_pic)
