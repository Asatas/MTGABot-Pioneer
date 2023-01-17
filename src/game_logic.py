import win32gui
from PIL import ImageGrab
import numpy as np
import cv2
from scipy import ndimage
from util.lprint import lprint
from windows_api_fxns import *
from screen.screen import *
from screen.input import *


def get_game_state():
    failsafe()
    img = get_full_screen()
    if isRewardScreen(img):
        return 'REWARDS', img
    elif onHomeMenu(img):
        return 'HOMESCREEN', img
    elif isLoadingScreen(img):
        return 'LOADSCREEN', img
    elif onKeepHand(img):
        return 'MULLIGAN', img
    elif hasPriority(img):
        return 'PRIORITY', img
    elif hasBlockingPriority(img):
        return 'BLOCKING', img
    elif isDialog(img):
        return 'DIALOG', img
    elif isGameOver(img):
        return 'ENDOFGAME', img
    elif isDiscard(img):
        return 'DISCARD', img
    else:
        return None, img


def handle_unkown_game_outcome(img):
    lprint('UKNOWN GAME OUTCOME - SAVING SCREENSHOT')
    update_score_db('UNKNOWN')
    write_img(img, 'UNKOWN_GAME_OUTCOME')
    click_on('RIGHT_EDGE')
    time.sleep(15)
    img = get_full_screen()
    if (isRewardScreen(img)):
        handle_rewards(img)


def handle_win():
    lprint('ebot WON game')
    update_score_db('WON')
    click_on('RIGHT_EDGE')
    time.sleep(15)
    img = get_full_screen()
    if (isRewardScreen(img)):
        handle_rewards(img)


def handle_loss():
    lprint('ebot LOST game')
    update_score_db('LOST')
    click_on('RIGHT_EDGE')
    time.sleep(15)
    img = get_full_screen()
    if (isRewardScreen(img)):
        handle_rewards(img)


def update_score_db(outcome):
    score_db = read_score_db('DAY')
    if outcome == 'WON':
        score_db['wins'] = score_db['wins'] + 1
        write_score_db('DAY', score_db)
    elif outcome == 'LOST':
        score_db['losses'] = score_db['losses'] + 1
        write_score_db('DAY', score_db)
    elif outcome == 'UNKNOWN':
        score_db['unknown'] = score_db['unknown'] + 1
        write_score_db('DAY', score_db)
    else:
        exit_and_report('Invalid outcome type for update_score_db', None)


def handle_rewards(initial_img):
    reward_count = 0
    img = initial_img
    while (isRewardScreen(img) and reward_count < 3):
        lprint('Capturing rewards')
        write_img(img, 'REWARD')
        click_on('RIGHT_EDGE')
        time.sleep(5)
        reward_count += 1
        img = get_full_screen()


def handle_start_game(img):
    # TO-DO Verify clicking the right button here
    if (not isSelectDecks(img)):
        lprint('Not on select decks screen')
        click_on('PLAY_GAME')
        time.sleep(3)
    else:
        lprint('On select decks screen')
        click_on('FIND_MATCH')
        time.sleep(3)
        click_on('RANKED_MATCH')
        time.sleep(2)
        click_on('HISTORIC_RANKED')
        time.sleep(2)

        img = get_full_screen()
        if (isDeckCollapsed(img) and (not isDeckExpanded(img))):
            click_on('EXPAND_DECK')
            time.sleep(2)
        img = get_full_screen()
        if (isDeckCollapsed(img) and (not isDeckExpanded(img))):
            exit_and_report('DECK SHOULD BE EXPANDED', img)
        elif (isDeckExpanded(img) and (not isDeckCollapsed(img))):
            click_on('SELECT_FIRST_DECK')
            time.sleep(1.5)
            click_on('PLAY_GAME')
            time.sleep(4)
        else:
            isDeckExpandedV = isDeckExpanded(img)
            isDeckCollapsedV = isDeckCollapsed(img)
            lprint('isDeckExpanded: ' + str(isDeckExpandedV))
            lprint('isDeckCollapsed: ' + str(isDeckCollapsedV))
            exit_and_report(
                'WEIRD COMBINATION OF RESULTS - DECK SHOULD BE EXPANDED', img)
