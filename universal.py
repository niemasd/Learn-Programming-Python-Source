#!/usr/bin/env python3
from json import load as jload
from prompt_toolkit import HTML
from prompt_toolkit.styles import Style

# global constants
VERSION = '1.0.9'
LESSONS_PATH = "lesson_data"
SAVE_FILE_PATH = "save/save.pkl"

# game title
TITLE_STR = "Learn Programming: Python"
TITLE_HTML_STR = '<ansired>Learn Programming:</ansired> <ansigreen><b>Python</b></ansigreen>'
TITLE_HTML = HTML(TITLE_HTML_STR)

# under construction app
UNDER_CONSTRUCTION_TITLE = "Under Construction"
UNDER_CONSTRUCTION_MESSAGE = "This section is under construction."

# welcome message app
WELCOME_MESSAGE_TITLE = "Welcome!"
WELCOME_MESSAGE = HTML("Welcome to <b>%s</b>!\n-Created by <b>Niema Moshiri</b>-\n\nPress <b>ENTER</b> to start, and navigate with the <b>ARROW KEYS</b>\n\nPress <b>ALT+ENTER</b> to make fullscreen" % TITLE_HTML_STR)

# about app
ABOUT_TITLE = "About"
ABOUT_MESSAGE = HTML("%s (version %s)\n\nGame developed by <b><ansiblue>Niema Moshiri</ansiblue></b> (www.niema.net)\n\nLesson content written by <b><ansiblue>Sabeel Mansuri</ansiblue></b> (www.sabeelmansuri.com)" % (TITLE_HTML_STR, VERSION))

# main menu app
MAIN_MENU_TITLE = TITLE_HTML
MAIN_MENU_TEXT = "Please select one of the following options:"

# lessons app
LESSONS_MENU_TITLE = "Lessons"
LESSONS_MENU_TEXT = HTML("Please select one of the following chapters:\n\n(press <b>TAB</b> to switch between chapter selection and buttons)")
LESSON_TEXT = HTML("Please select one of the following lessons:\n\n(press <b>TAB</b> to switch between chapter selection and buttons)")
EMPTY_MODULE_TEXT = "This module is empty"
EMPTY_LESSON_TEXT = "This lesson is empty"
CHALLENGE_CORRECT_MESSAGE = "<b><ansigreen>Congratulations! You solved the challenge!</ansigreen></b>"
CHALLENGE_INCORRECT_MESSAGE = "<b><ansired>Sorry, that's incorrect. Try again!</ansired></b>"
CHALLENGE_MATH_INVALID_NUM = "<b><ansired>Please enter a valid number.</ansired></b>"

# challenges app
CHALLENGES_TITLE = "Challenges"

# styles app
STYLES_TITLE = "Styles"
STYLES_TEXT = HTML("Please select one of the following styles:\n\n(press <b>TAB</b> to switch between style selection and buttons)")

# UI styles
STYLES = {
    'Default': None,

    'Hacker Blue': Style.from_dict({
        'dialog':             'bg:ansiblack',
        'dialog frame.label': 'bg:ansiblack ansiblack',
        'dialog.body':        'bg:ansiblack ansiblue',
        'dialog shadow':      'bg:ansiblack',
    }),

    'Hacker Green': Style.from_dict({
        'dialog':             'bg:ansiblack',
        'dialog frame.label': 'bg:ansiblack ansiblack',
        'dialog.body':        'bg:ansiblack ansigreen',
        'dialog shadow':      'bg:ansiblack',
    }),

    'Hacker Purple': Style.from_dict({
        'dialog':             'bg:ansiblack',
        'dialog frame.label': 'bg:ansiblack ansiblack',
        'dialog.body':        'bg:ansiblack ansimagenta',
        'dialog shadow':      'bg:ansiblack',
    }),

    'Hacker Red': Style.from_dict({
        'dialog':             'bg:ansiblack',
        'dialog frame.label': 'bg:ansiblack ansiblack',
        'dialog.body':        'bg:ansiblack ansired',
        'dialog shadow':      'bg:ansiblack',
    }),

    'Hacker Yellow': Style.from_dict({
        'dialog':             'bg:ansiblack',
        'dialog frame.label': 'bg:ansiblack ansiblack',
        'dialog.body':        'bg:ansiblack ansiyellow',
        'dialog shadow':      'bg:ansiblack',
    }),

    'Paper': Style.from_dict({
        'dialog':             'bg:ansiwhite',
        'dialog frame.label': 'bg:ansiwhite ansiblack',
        'dialog.body':        'bg:ansiwhite ansiblack',
        'dialog shadow':      'bg:grey',
        'label':              'ansiblack',
    })
}
DEFAULT_STYLE = None # use prompt_toolkit default

# load a JSON
def load_json(fn):
    f = open(fn); tmp = jload(f); f.close()
    return tmp

# get width of single line of HTML
def html_width(s):
    return sum(len(p.split('>')[1]) if '>' in p else len(p) for p in s.split('<'))

# maximize window (https://stackoverflow.com/a/43959471)
import os
import ctypes
import msvcrt
import subprocess
from ctypes import wintypes
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)
SW_MAXIMIZE = 3
kernel32.GetConsoleWindow.restype = wintypes.HWND
kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)
def maximize_console(lines=None):
    fd = os.open('CONOUT$', os.O_RDWR)
    try:
        hCon = msvcrt.get_osfhandle(fd)
        max_size = kernel32.GetLargestConsoleWindowSize(hCon)
        if max_size.X == 0 and max_size.Y == 0:
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        os.close(fd)
    cols = max_size.X
    hWnd = kernel32.GetConsoleWindow()
    if cols and hWnd:
        if lines is None:
            lines = max_size.Y
        else:
            lines = max(min(lines, 9999), max_size.Y)
        subprocess.check_call('mode.com con cols={} lines={}'.format(
                                cols, lines))
        user32.ShowWindow(hWnd, SW_MAXIMIZE)
