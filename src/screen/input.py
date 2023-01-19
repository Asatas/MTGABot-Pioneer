
from pynput import mouse
import pyautogui
import time
from numpy import random
from screen.locations import CLICK_LOCATION_DICT
from util.lprint import lprint

mouse = mouse.Controller()


def click(x, y):
    time.sleep(abs(random.normal(0.1)))
    mouse.position = (x, y)
    time.sleep(abs(random.normal(0.15)))
    pyautogui.mouseDown()
    time.sleep(0.05)
    pyautogui.mouseUp()


def click_down(x, y):
    time.sleep(abs(random.normal(0.1)))
    mouse.position = (x, y)
    time.sleep(abs(random.normal(0.15)))
    pyautogui.mouseDown()


def click_up(x, y):
    time.sleep(abs(random.normal(0.1)))
    mouse.position = (x, y)
    time.sleep(abs(random.normal(0.15)))
    pyautogui.mouseUp()


def click_on(item):
    try:
        (x, y) = CLICK_LOCATION_DICT[item]
    except FileNotFoundError as e:
        print('unknown item', item)

    click(x, y)
    lprint(f'EBot: {item} clicked')


def move_card(x1, y1, x2, y2):
    # click_down(x1, y1)
    time.sleep(abs(random.normal(0.1)))
    mouse.position = (x1, y1)
    time.sleep(abs(random.normal(0.15)))
    time.sleep(0.2)
    pyautogui.mouseDown()
    time.sleep(0.2)
    # click_up(x2, y2)
    time.sleep(abs(random.normal(0.1)))
    mouse.position = (x2, y2)
    time.sleep(abs(random.normal(0.15)))
    time.sleep(0.5)
    pyautogui.mouseUp()

    print(
        f'EBot: moved card from ({int(x1)},{int(y1)}) -> ({int(x2)},{int(y2)})')


def print_coord():
    print(mouse.position)


def playCardAt(card_tl_corner):
    x1 = card_tl_corner[0]
    y1 = card_tl_corner[1]

    print('playcardat: ', x1, y1)
    if x1 <= 450:
        x1 += random.randint(50, 100)
    else:
        x1 += random.randint(50, 100)
        y1 += random.randint(20, 30)
    print('after transform: ', x1, y1)

    # if x1 > 500:
    #    x1 += random.randint(70, 150)
    # elif x1 < 500:
    #    x1 += random.randint(40, 100)
    #    y1 += random.randint(10, 50)

    # if x1 > 700:
    #    x1 -= random.randint(70, 150)
    # elif x1 < 500:
    #    x1 -= random.randint(40, 100)
    #    y1 -= random.randint(10, 50)

    x_center = 1920 / 2
    y_center = 1080 / 2

    move_card(x1, y1, x_center, y_center)
    time.sleep(1)
