import cv2
import time
import numpy as np


from src.output_fxns import get_window_info, get_full_screen

NUM_IMAGES_TO_GET = 5
NUM_TESTS_PER_IMAGE = 10


VIEW_LOCATION_DICT = {
    'FIND_C1': (978, 141),
    'FIND_C2': (1015, 208),
}

REF_IMG_DICT = {
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


def onScreen(ref_img, full_screen_img, cutoff=10000, save_img=False):
    (x1, y1) = VIEW_LOCATION_DICT[f'FIND_C1']
    (x2, y2) = VIEW_LOCATION_DICT[f'FIND_C2']
    img = full_screen_img[y1:y2, x1:x2]
    if save_img:
        print('saving example image:')
        # cv2.imwrite(f'test_{element_to_look_for}.png', img)
    return areImgsSimilar(img, ref_img, cutoff=cutoff)


def areImgsSimilar(img1, img2, cutoff=10000):

    pixel_distance = np.sqrt(sum(np.square(img1.ravel() - img2.ravel())))

    if pixel_distance < cutoff:
        return True, pixel_distance
    else:
        return False, pixel_distance


if __name__ == "__main__":
    window_info = get_window_info()
    time.sleep(1)

    all_tests = {}
    test_counter = 0

    for x in range(NUM_IMAGES_TO_GET):

        active, full_screen_img = get_full_screen(window_info)
        if (active):
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
                active, full_screen_img = get_full_screen(window_info)
                if (not active):
                    print('INACTIVE SCREEN DETECTED DURING TEST')
                else:

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
        else:
            print('WINDOW NOT ACTIVE ERROR')
            window_info = get_window_info()
            time.sleep(1)
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
