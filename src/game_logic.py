import win32gui
from PIL import ImageGrab
import numpy as np
import cv2
from scipy import ndimage
from util.lprint import *
from windows_api_fxns import *
from screen.screen import *
from screen.input import *


def get_game_state():
    failsafe()
    img = get_full_screen()
    if isRewardScreen(img):
        return "REWARDS", img
    elif isPay0(img):
        return "PAY0", img
    elif onHomeMenu(img):
        return "HOMESCREEN", img
    elif isLoadingScreen(img):
        return "LOADSCREEN", img
    elif onKeepHand(img):
        return "MULLIGAN", img
    elif hasPriority(img):
        return "PRIORITY", img
    elif isDialog(img):
        return "DIALOG", img
    elif isGameOver(img):
        return "ENDOFGAME", img
    elif isDiscard(img):
        return "DISCARD", img
    #elif hasBlockingPriority(img):
    #    return "BLOCKING", img
    else:
        return None, img


def handle_unkown_game_outcome(img):
    lprint("UKNOWN GAME OUTCOME - SAVING SCREENSHOT")
    write_img(img, "UNKOWN_GAME_OUTCOME")
    click_on("RIGHT_EDGE")
    time.sleep(15)
    img = get_full_screen()
    if isRewardScreen(img):
        handle_rewards(img)


def handle_win():
    lprint("ebot WON game")
    click_on("RIGHT_EDGE")
    time.sleep(15)
    img = get_full_screen()
    if isRewardScreen(img):
        handle_rewards(img)


def handle_loss():
    lprint("ebot LOST game")
    click_on("RIGHT_EDGE")
    time.sleep(15)
    img = get_full_screen()
    if isRewardScreen(img):
        handle_rewards(img)

def concede_game():
    lprint("ebot CONCEDED game")
    click_on("GEAR")
    time.sleep(1)
    click_on("CONCEDE")
    time.sleep(1)
    click_on("RIGHT_EDGE")


def get_deck_to_play():

    return "main"



def handle_rewards(initial_img):
    reward_count = 0
    img = initial_img
    while isRewardScreen(img) and reward_count < 3:
        lprint("Capturing rewards")
        write_img(img, "REWARD")
        click_on("RIGHT_EDGE")
        time.sleep(5)
        reward_count += 1
        img = get_full_screen()



def handle_start_game(img):
    #deck = get_deck_to_play()
    #lprint("Getting current deck to start game: " + deck)
    # TO-DO Verify clicking the right button here
    click_on("PLAY_GAME")
    time.sleep(2)
    click_on("PLAY_GAME")

