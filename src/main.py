import time
from screen.screen import *
from screen.input import *
from windows_api_fxns import *
from game_logic import *

if __name__ == "__main__":

    # setup
    startup()
    lprint('EBot ONLINE')

    # game loop
    while (True):
        time.sleep(.1)
        print('------------------------------------------------------------------')
        state, img = get_game_state()
        if state is not None:
            lprint(state)
        if state == 'REWARDS':
            handle_rewards(img)
        if state == 'PRIORITY':
            isPlayableCard, leftmost_card_pt = locate_leftmost_playable_card()

            if isPlayableCard:
                playCardAt(leftmost_card_pt)
            else:
                click_on('PASS')
                click_on('OPPONENT')

        elif state == 'BLOCKING':
            click_on('PASS')

        elif state == 'ENDOFGAME':
            time.sleep(1)
            img = get_full_screen()
            if (isWinScreenTop(img)):
                handle_win()

            elif (isDefeatScreenTop(img)):
                handle_loss()
            else:
                handle_unkown_game_outcome(img)

        elif state == 'HOMESCREEN':
            handle_start_game(img)

        elif state == 'MULLIGAN':
            click_on('KEEP_HAND')

        elif state == 'DIALOG':
            click_on('DIALOG_DONE')

        elif state == 'LOADSCREEN':
            click_on('RIGHT_EDGE')
