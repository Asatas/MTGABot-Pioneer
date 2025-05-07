import time
from screen.screen import *
from screen.input import *
from windows_api_fxns import *
from game_logic import *
from util.lprint import *
import traceback


def main():
    # setup
    startup()
    lprint("EBot ONLINE")
    spells = 0
    # game loop
    while True:
        time.sleep(0.1)
        print("------------------------------------------------------------------")
        state, img = get_game_state()
        if state is not None:
            lprint(state)
        if state == "REWARDS":
            handle_rewards(img)
        if state == "PRIORITY":
            isPlayableCard, leftmost_card_pt = locate_leftmost_playable_card()

            if isPlayableCard:
                if spells < 4:
                    playCardAt(leftmost_card_pt)
                    spells += 1
                else:
                    spells = 0
                    concede_game()
            else:
                if spells >= 4:
                    spells = 0
                    concede_game()
                click_on("PASS")
                click_on("OPPONENT")


        elif state == "BLOCKING":
            click_on("PASS")
            time.sleep(1)

        elif state == "ENDOFGAME":
            time.sleep(1)
            img = get_full_screen()
            if isWinScreenTop(img) or isWin(img):
                handle_win()

            elif isDefeatScreenTop(img) or isDefeat(img):
                handle_loss()
            else:
                handle_unkown_game_outcome(img)

        elif state == "HOMESCREEN":
            handle_start_game(img)

        elif state == "MULLIGAN":
            click_on("KEEP_HAND")
            time.sleep(1)

        elif state == "DIALOG":
            click_on("DIALOG_DONE")
            time.sleep(1)

        elif state == "LOADSCREEN":
            click_on("RIGHT_EDGE")
            time.sleep(1)

        elif state == "DISCARD":
            click_on("DISCARD")
            time.sleep(1)
            click_on("PASS")
            time.sleep(2)

        elif state == "PAY0":
            click_on("PAY0")
            time.sleep(1)
            click_on("CONFIRM0")
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        critical_exception(err)
        traceback.print_exc()
