import json
import logging
import pywintypes
import win32api
import win32con
import cv2
import os

import subprocess

import win32gui
import time
from datetime import datetime

from util.lprint import *
from pynput import mouse

WINDOW_STRING = "MTGA"
DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
mouse = mouse.Controller()


def set_mtga_window_foreground():
    # First find the 'MTGA' window, if the name in the upper left corner of the game window
    # when in windowed mode every changes you will need to update this screen
    # We only need to set this once.
    window_handle = win32gui.FindWindow(None, WINDOW_STRING)
    # Get the windows coordinates
    window_coordinates = win32gui.GetWindowRect(window_handle)
    # Verify the window is in the upper left corner of the screen
    # and that it is the correct size, if not set it properly.
    if (0, 0, 1920, 1080) != window_coordinates:
        # Move the window to a known offset (0,0) for the upper left corner,
        # and force a resize so this works on every system every time
        win32gui.SetWindowPos(window_handle, None, 0, 0, 1920, 1080, 0)
    win32gui.SetForegroundWindow(window_handle)
    # Verify the coordinates are at (0,0,1920,1080)


def is_mtga_open():
    """Checks if Window is open"""
    window_handle = win32gui.FindWindow(None, WINDOW_STRING)
    if window_handle:
        return True
    return False


def is_mtga_window_foreground():
    if WINDOW_STRING == win32gui.GetWindowText(win32gui.GetForegroundWindow()):
        return True
    else:
        return False


def start_mtga_process():
    if not is_mtga_open():
        subprocess.Popen(
            ["C:\Program Files\Wizards of the Coast\MTGA\MTGALauncher\MTGALauncher.exe"]
        )


def set_primary_screen_resolution(x, y):
    devmode = pywintypes.DEVMODEType()
    devmode.PelsWidth = x
    devmode.PelsHeight = y

    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

    win32api.ChangeDisplaySettings(devmode, 0)

    print("set resolution to: ", x, " ", y)


def exit_and_report(error_text, img=None):
    critical_print("FATAL ERROR " + error_text)
    if not img is None:
        write_img(img, "ERROR")
    exit()


def set_up_critical_logger(critical_logs_file_name):
    log = logging.getLogger("critical")
    log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler_info = logging.FileHandler(critical_logs_file_name, mode="a")
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)
    log.setLevel(logging.INFO)


def set_up_dir_and_logger():
    now = datetime.now()
    date_str = now.strftime("%m-%d-%Y")
    logs_directory_path = DIR + "/logs/" + date_str
    if not os.path.exists(logs_directory_path):
        os.mkdir(logs_directory_path)
        print("MADE DIRECTORY: ", logs_directory_path)
    logs_file_name = logs_directory_path + "/app.log"
    logging.basicConfig(
        level=logging.INFO,
        filename=logs_file_name,
        filemode="a",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    critical_logs_file_name = logs_directory_path + "/app.critical.log"
    set_up_critical_logger(critical_logs_file_name)


def write_img(img, type):
    now = datetime.now()
    date_str = now.strftime("%m-%d-%Y")
    time_str = now.strftime("%H-%M-%S")
    logs_directory_path = DIR + "/logs/" + date_str
    if type == "REWARD":
        rewards_png_file_name = logs_directory_path + "/rewards_" + time_str + ".png"
        cv2.imwrite(rewards_png_file_name, img)
    elif type == "ERROR":
        error_png_file_name = logs_directory_path + "/fatal_error_" + time_str + ".png"
        cv2.imwrite(error_png_file_name, img)
    elif type == "UNKOWN_GAME_OUTCOME":
        png_file_name = (
            logs_directory_path + "/unknown_game_outcome_" + time_str + ".png"
        )
        cv2.imwrite(png_file_name, img)
    else:
        exit_and_report("Invalid write_img type", img)


def failsafe():
    if mouse.position == (0, 0):
        lprint("FAILSAFE TRIGGERED, EXITING")
        exit()


def startup():
    set_up_dir_and_logger()
    critical_print("Starting Ebot")
    set_primary_screen_resolution(1920, 1080)
    time.sleep(1)
    start_mtga_process()
    time.sleep(5)
    if not is_mtga_open():
        # TO-DO Implement Handle Update Logic
        exit_and_report("MTGA Not Open", None)
    set_mtga_window_foreground()
    time.sleep(1)
