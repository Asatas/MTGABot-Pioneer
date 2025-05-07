import win32gui
from windows_api_fxns import *
from scipy import ndimage
import cv2
import numpy as np
from PIL import ImageGrab
from screen.locations import *


def isLoadingScreen(full_screen_img):
    return onScreen("BLACK_BAR", full_screen_img, cutoff=1000)


def onKeepHand(full_screen_img):
    return onScreen("KEEP_HAND", full_screen_img)


def onHomeMenu(full_screen_img):
    return onScreen("HOME_MENU", full_screen_img)


def hasPriority(full_screen_img):
    return onScreen("PASS_BUTTON", full_screen_img, cutoff=6000)


def hasBlockingPriority(full_screen_img):
    return onScreen("BLOCK_BUTTON", full_screen_img, cutoff=7500)


def isDialog(full_screen_img):
    return onScreen("DIALOG_DONE_BUTTON", full_screen_img)


def isGameOver(full_screen_img):
    return onScreen("VIEW_BATTLEFIELD", full_screen_img, cutoff=5000)


def isDefeat(full_screen_img):
    return onScreen("DEFEAT", full_screen_img, cutoff=10000)


def isWin(full_screen_img):
    return onScreen("WIN", full_screen_img, cutoff=8000)


def isDeckExpanded(full_screen_img):
    return onScreen("DECK_EXPANDED", full_screen_img, cutoff=2000)


def isDeckCollapsed(full_screen_img):
    return onScreen("DECK_COLLAPSED", full_screen_img, cutoff=2000)


def isWinScreenTop(full_screen_img):
    return onScreen("WIN_SCREEN_TOP", full_screen_img, cutoff=10000)


def isDefeatScreenTop(full_screen_img):
    return onScreen("DEFEAT_SCREEN_TOP", full_screen_img, cutoff=8000)


def isRewardScreen(full_screen_img):
    return onScreen("REWARD_SCREEN", full_screen_img, cutoff=2000)


def isDiscard(full_screen_img):
    return onScreen("DISCARD", full_screen_img, cutoff=2000)


def isSelectDecks(full_screen_img):
    select_decks_one = onScreen(
        "SELECT_DECK_EVENT_SELECTED", full_screen_img, cutoff=2000
    )
    select_decks_two = onScreen(
        "SELECT_DECK_EVENT_NOT_SELECTED", full_screen_img, cutoff=2000
    )
    return select_decks_one or select_decks_two


def isFindMatch(full_screen_img):
    select_decks_one = onScreen("DECK_EXPANDED", full_screen_img, cutoff=2000)
    select_decks_two = onScreen("DECK_COLLAPSED", full_screen_img, cutoff=2000)
    return select_decks_one or select_decks_two


def onScreen(element_to_look_for, full_screen_img, cutoff=10000, save_img=False):
    (x1, y1) = VIEW_LOCATION_DICT[f"{element_to_look_for}_C1"]
    (x2, y2) = VIEW_LOCATION_DICT[f"{element_to_look_for}_C2"]
    img = full_screen_img[y1:y2, x1:x2]
    if save_img:
        print("saving example image:")
        cv2.imwrite(f"test_{element_to_look_for}.png", img)
    ref_img = REF_IMG_DICT[element_to_look_for]
    return areImgsSimilar(img, ref_img, cutoff=cutoff)


def get_hand_region():
    x1 = 0
    x2 = 1920
    y1 = 1080 - 200
    y2 = 1080
    return get_screenshot(x1, y1, x2, y2)


def get_full_screen():
    x1 = 0
    x2 = 1920
    y1 = 0
    y2 = 1080
    return get_screenshot(x1, y1, x2, y2)


def get_screenshot(x1, y1, x2, y2):
    # win32gui.SetForegroundWindow(window_info['hwnd'])
    ret = is_mtga_window_foreground()
    if not ret:
        # set_mtga_window_foreground()
        # time.sleep(0.5)
        # ret = is_mtga_window_foreground()
        exit_and_report("Window not in foreground", get_system_screenshot())
    if ret:
        box = (x1, y1, x2, y2)
        screen = ImageGrab.grab(box)
        img = np.array(screen.getdata(), dtype="float32").reshape(
            (screen.size[1], screen.size[0], 3)
        )
        img_reversed = img.copy()
        img_reversed[:, :, 0] = img[:, :, 2]
        img_reversed[:, :, 2] = img[:, :, 0]
    else:
        exit_and_report("Window not in foreground after retry",
                        get_system_screenshot())
        """img_reversed = np.zeros(
            (1080, 1920, 3))"""
    return img_reversed


def get_system_screenshot():
    x1 = 0
    x2 = 1920
    y1 = 0
    y2 = 1080
    box = (x1, y1, x2, y2)
    screen = ImageGrab.grab(box)

    img = np.array(screen.getdata(), dtype="float32").reshape(
        (screen.size[1], screen.size[0], 3)
    )
    img_reversed = img.copy()
    img_reversed[:, :, 0] = img[:, :, 2]
    img_reversed[:, :, 2] = img[:, :, 0]
    return img_reversed


def locate_leftmost_playable_card():
    # Define the lower and upper bounds for the blue tint in HSV
    lower_bound = np.array([95, 100, 150])  # Adjusted for blue tint
    upper_bound = np.array([135, 255, 255])  # Adjusted for blue tint

    # Get the hand region
    hand_img = get_hand_region()

    # Convert the hand region to HSV color space
    hand_img_hsv = cv2.cvtColor(hand_img.astype(np.uint8), cv2.COLOR_BGR2HSV)

    # Create a mask for the blue-tinted areas
    mask = cv2.inRange(hand_img_hsv, lower_bound, upper_bound)

    # Save the mask for debugging
    cv2.imwrite('./mask.png', mask)

    # Load the template and convert it to grayscale
    template = REF_IMG_DICT["corner_mask_1"]
    template = cv2.cvtColor(template.astype(np.float32), cv2.COLOR_BGR2GRAY)
    w, h = template.shape

    leftmost_pt = (mask.shape[1], 0)
    isPlayableCard = False

    # Perform template matching with rotations
    for theta in [0, -10, 10]:
        # Rotate the template
        template_rotated = ndimage.rotate(template, theta)

        # Ensure the rotated template is of type uint8
        template_rotated = template_rotated.astype(np.uint8)

        # Perform template matching
        res = cv2.matchTemplate(mask, template_rotated, cv2.TM_CCOEFF_NORMED)
        threshold = 0.55
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            if pt[0] < leftmost_pt[0]:
                leftmost_pt = pt

    # Check if a playable card was found
    if leftmost_pt[0] < mask.shape[1]:
        isPlayableCard = True
    leftmost_pt_full_image = [leftmost_pt[0], leftmost_pt[1] + 1080 - 150]
    return isPlayableCard, leftmost_pt_full_image


def areImgsSimilar(img1, img2, cutoff=10000):

    pixel_distance = np.sqrt(sum(np.square(img1.ravel() - img2.ravel())))

    # print(pixel_distance)

    if pixel_distance < cutoff:
        return True
    else:
        return False
