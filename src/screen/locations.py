import cv2
import os


DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))))
VIEW_LOCATION_DICT = {
    "HOME_MENU_C1": (71, 0),
    "HOME_MENU_C2": (318, 100),
    "KEEP_HAND_C1": (1008, 834),
    "KEEP_HAND_C2": (1265, 922),
    "PASS_BUTTON_C1": (1672, 923),
    "PASS_BUTTON_C2": (1722, 978),
    "VIEW_BATTLEFIELD_C1": (1672, 23),
    "VIEW_BATTLEFIELD_C2": (1722, 78),
    "BLACK_BAR_C1": (0, 23),
    "BLACK_BAR_C2": (1920, 78),
    "DIALOG_DONE_BUTTON_C1": (830, 850),
    "DIALOG_DONE_BUTTON_C2": (1090, 900),
    "DEFEAT_C1": (880, 517),
    "DEFEAT_C2": (1034, 579),
    "WIN_C1": (903, 497),
    "WIN_C2": (967, 580),
    "SELECT_DECK_EVENT_SELECTED_C1": (1581, 85),
    "SELECT_DECK_EVENT_SELECTED_C2": (1641, 204),
    "SELECT_DECK_EVENT_NOT_SELECTED_C1": (1581, 85),
    "SELECT_DECK_EVENT_NOT_SELECTED_C2": (1641, 204),
    "DECK_COLLAPSED_C1": (88, 338),
    "DECK_COLLAPSED_C2": (108, 369),
    "DECK_EXPANDED_C1": (88, 338),
    "DECK_EXPANDED_C2": (108, 369),
    "WIN_SCREEN_TOP_C1": (722, 140),
    "WIN_SCREEN_TOP_C2": (1188, 209),
    "REWARD_SCREEN_C1": (858, 90),
    "REWARD_SCREEN_C2": (1059, 137),
    "DEFEAT_SCREEN_TOP_C1": (978, 141),
    "DEFEAT_SCREEN_TOP_C2": (1015, 208),
    "DISCARD_C1": (867, 445),
    "DISCARD_C2": (1044, 467),
    "PAY0_C1": (1685, 750),
    "PAY0_C2": (1740, 792),
    "BLOCK_BUTTON_C1": (1672, 923),
    "BLOCK_BUTTON_C2": (1722, 978)
}

REF_IMG_DICT = {
    "BLOCK_BUTTON": cv2.imread(DIR + "/ref_images/BLOCK_BUTTON.png"),
    "corner_mask_0": cv2.imread(DIR + "/ref_images/corner_mask_0.png"),
    "corner_mask_1": cv2.imread(DIR + "/ref_images/corner_mask_1.png"),
    "corner_mask": cv2.imread(DIR + "/ref_images/corner_mask.png"),
    "HOME_MENU": cv2.imread(DIR + "/ref_images/HOME_MENU.png"),
    "KEEP_HAND": cv2.imread(DIR + "/ref_images/KEEP_HAND.png"),
    "PASS_BUTTON": cv2.imread(DIR + "/ref_images/PASS_BUTTON.png"),
    "VIEW_BATTLEFIELD": cv2.imread("./ref_images/VIEW_BATTLEFIELD.png"),
    "BLACK_BAR": cv2.imread(DIR + "/ref_images/BLACK_BAR.png"),
    "DIALOG_DONE_BUTTON": cv2.imread("./ref_images/blockers_done.png"),
    "DEFEAT": cv2.imread(DIR + "/ref_images/DEFEAT.png"),
    "WIN": cv2.imread(DIR + "/ref_images/WIN.png"),
    "SELECT_DECK_EVENT_SELECTED": cv2.imread(
        DIR + "/ref_images/SELECT_DECK_EVENT_SELECTED.png"
    ),
    "SELECT_DECK_EVENT_NOT_SELECTED": cv2.imread(
        DIR + "/ref_images/SELECT_DECK_EVENT_NOT_SELECTED.png"
    ),
    "DECK_COLLAPSED": cv2.imread(DIR + "/ref_images/DECK_COLLAPSED.png"),
    "DECK_EXPANDED": cv2.imread(DIR + "/ref_images/DECK_EXPANDED.png"),
    "WIN_SCREEN_TOP": cv2.imread(DIR + "/ref_images/WIN_SCREEN_TOP.png"),
    "REWARD_SCREEN": cv2.imread(DIR + "/ref_images/REWARD_SCREEN.png"),
    "DEFEAT_SCREEN_TOP": cv2.imread(DIR + "/ref_images/DEFEAT_SCREEN_TOP.png"),
    "DISCARD": cv2.imread(DIR + "/ref_images/DISCARD.png"),
    "PAY0": cv2.imread("./ref_images/pay0button.png"),
}

CLICK_LOCATION_DICT = {
    "PLAY_GAME": (1738, 1010),
    "KEEP_HAND": (1125, 879),
    "LEFTMOST_HAND": (347, 1079),
    "DECK": (460, 572),
    "PASS": (1773, 948),
    "OPPONENT": (954, 117),
    "CENTER": (965, 624),
    "RIGHT_EDGE": (1915, 511),
    "DIALOG_DONE": (960, 874),
    "___NOT_EDITED___": (0, 0),
    "PLAY_FIRST": (888, 502),
    "___": (0, 0),
    "FIND_MATCH": (1732, 119),
    "RANKED_MATCH": (1614, 270),
    "CASUAL_MATCH": (1732, 278),
    "HISTORIC_RANKED": (1593, 582),
    "EXPAND_DECK": (102, 356),
    "SELECT_FIRST_DECK": (456, 573),
    "SELECT_SECOND_DECK": (749, 561),
    "DISCARD": (938, 1020),
    "PAY0": (1720,780),
    "CONFIRM0": (1780,950),
    "GEAR": (1885, 35),
    "CONCEDE": (960, 635)
}
