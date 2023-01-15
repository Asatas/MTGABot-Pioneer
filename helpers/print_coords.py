from pynput import mouse

import time

mouse = mouse.Controller()


def print_coord():
    print(mouse.position)


if __name__ == "__main__":
    while True:
        time.sleep(3)
        print_coord()
