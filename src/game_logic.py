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
    elif onHomeMenu(img):
        return "HOMESCREEN", img
    elif isLoadingScreen(img):
        return "LOADSCREEN", img
    elif onKeepHand(img):
        return "MULLIGAN", img
    elif hasPriority(img):
        return "PRIORITY", img
    elif hasBlockingPriority(img):
        return "BLOCKING", img
    elif isDialog(img):
        return "DIALOG", img
    elif isGameOver(img):
        return "ENDOFGAME", img
    elif isDiscard(img):
        return "DISCARD", img
    else:
        return None, img


def handle_unkown_game_outcome(img):
    lprint("UKNOWN GAME OUTCOME - SAVING SCREENSHOT")
    update_score_db("UNKNOWN", get_deck_to_play())
    write_img(img, "UNKOWN_GAME_OUTCOME")
    click_on("RIGHT_EDGE")
    time.sleep(15)
    img = get_full_screen()
    if isRewardScreen(img):
        handle_rewards(img)


def handle_win():
    lprint("ebot WON game")
    update_score_db("WON", get_deck_to_play())
    click_on("RIGHT_EDGE")
    time.sleep(15)
    img = get_full_screen()
    if isRewardScreen(img):
        handle_rewards(img)


def handle_loss():
    lprint("ebot LOST game")
    update_score_db("LOST", get_deck_to_play())
    click_on("RIGHT_EDGE")
    time.sleep(15)
    img = get_full_screen()
    if isRewardScreen(img):
        handle_rewards(img)


def update_score_db(outcome, deck):
    lprint("Updating score for deck: " + deck + " outcome: " + outcome)
    score_db = read_score_db("DAY")
    if outcome == "WON":
        score_db[deck]["wins"] = score_db[deck]["wins"] + 1
        write_score_db("DAY", score_db)
    elif outcome == "LOST":
        score_db[deck]["losses"] = score_db[deck]["losses"] + 1
        write_score_db("DAY", score_db)
    elif outcome == "UNKNOWN":
        score_db[deck]["unknown"] = score_db[deck]["unknown"] + 1
        write_score_db("DAY", score_db)
    else:
        exit_and_report("Invalid outcome type for update_score_db", None)


def get_deck_to_play():
    score_db = read_score_db("DAY")
    main_wins = score_db["main"]["wins"]
    main_finished_playing = score_db["main"]["finished_playing"]
    color_played = (
        score_db["color"]["wins"]
        + score_db["color"]["losses"]
        + score_db["color"]["unknown"]
    )
    color_finished_playing = score_db["color"]["finished_playing"]
    if main_wins < 15:
        return "main"
    elif main_finished_playing == 0:
        critical_print("FINISHED WINNING 15 GAMES W MAIN DECK")
        score_db["main"]["finished_playing"] = 1
        write_score_db("DAY", score_db)
    if color_played < 20:
        return "color"
    elif color_finished_playing == 0:
        critical_print("FINISHED PLAYING 20 GAMES W COLOR DECK")
        score_db["color"]["finished_playing"] = 1
        write_score_db("DAY", score_db)
        exit()
    elif color_finished_playing == 1:
        critical_print(
            "NOTICE - ALREADY FINSHED PLAYING 20 GAMES W COLOR DECK - STOPPING BOT RIGHT AWAY"
        )
        exit()
    # should not get here
    exit_and_report("GET DECK TO PLAY ERROR")


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


def go_to_find_match():
    img = None
    for x in range(4):
        click_on("FIND_MATCH")
        time.sleep(3)
        img = get_full_screen()
        if isFindMatch(img):
            return
        else:
            lprint("Still not on find match screen, tries: " + str(x))
    exit_and_report("COULD NOT GET TO FIND MATCH SCREEN", img)


def handle_start_game(img):
    deck = get_deck_to_play()
    lprint("Getting current deck to start game: " + deck)
    # TO-DO Verify clicking the right button here
    if not isSelectDecks(img):
        lprint("Not on select decks screen")
        click_on("PLAY_GAME")
        time.sleep(3)
    else:
        lprint("On select decks screen")

        go_to_find_match()

        if deck == "main":
            click_on("RANKED_MATCH")
        elif deck == "color":
            click_on("CASUAL_MATCH")
        else:
            exit_and_report("INVALID DECK PASSED")
        time.sleep(2)
        click_on("HISTORIC_RANKED")
        time.sleep(2)

        img = get_full_screen()
        if isDeckCollapsed(img) and (not isDeckExpanded(img)):
            click_on("EXPAND_DECK")
            time.sleep(2)
            img = get_full_screen()
            if isDeckCollapsed(img) and (not isDeckExpanded(img)):
                exit_and_report("DECK SHOULD BE EXPANDED", img)
        if isDeckExpanded(img) and (not isDeckCollapsed(img)):
            if deck == "main":
                click_on("SELECT_FIRST_DECK")
            elif deck == "color":
                click_on("SELECT_SECOND_DECK")
            time.sleep(1.5)
            click_on("PLAY_GAME")
            time.sleep(4)
        else:
            isDeckExpandedV = isDeckExpanded(img)
            isDeckCollapsedV = isDeckCollapsed(img)
            lprint("isDeckExpanded: " + str(isDeckExpandedV))
            lprint("isDeckCollapsed: " + str(isDeckCollapsedV))
            exit_and_report(
                "WEIRD COMBINATION OF RESULTS - DECK SHOULD BE EXPANDED", img
            )
