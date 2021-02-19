#!/usr/bin/env python3
from glob import glob
from os import getcwd, makedirs
from os.path import dirname, exists
from pickle import dump as pdump
from pickle import load as pload
from prompt_toolkit.shortcuts import button_dialog, checkboxlist_dialog, input_dialog, message_dialog, radiolist_dialog, set_title
from sys import version_info
from universal import *

# constants
APP_STYLE = DEFAULT_STYLE
LESSON_DATA = list()
SAVE_DATA = None

# save the save data to file
def save_game():
    if SAVE_DATA is None:
        raise RuntimeError("Save data is None")
    f = open(SAVE_FILE_PATH,'wb'); pdump(SAVE_DATA,f); f.close()

# check if lesson (subchapter) is completed
def is_lesson_completed(module_ind, lesson_ind):
    return sum(SAVE_DATA['completed'][module_ind][lesson_ind]) == len(SAVE_DATA['completed'][module_ind][lesson_ind])

# check if module (chapter) is completed
def is_module_completed(module_ind):
    return sum(is_lesson_completed(module_ind,l) for l in range(len(SAVE_DATA['completed'][module_ind]))) == len(SAVE_DATA['completed'][module_ind])

# under construction app (returns None)
def under_construction_app(title=UNDER_CONSTRUCTION_TITLE, text=UNDER_CONSTRUCTION_MESSAGE):
    return message_dialog(title=title, text=text, style=APP_STYLE)

# welcome message app (returns None)
def welcome_app(title=WELCOME_MESSAGE_TITLE, text=WELCOME_MESSAGE):
    return message_dialog(title=title, text=text, style=APP_STYLE)

# main menu app (returns which app to go to next)
def main_menu_app(title=MAIN_MENU_TITLE, text=MAIN_MENU_TEXT):
    return button_dialog(title=title, text=text, style=APP_STYLE, buttons=[
        ('Lessons',    'lessons'),
        ('Styles',     'styles'),
        ('About',      'about'),
        ('Quit',       None),
    ])

# lessons app (returns which lesson to run)
def lessons_app(title=LESSONS_MENU_TITLE, text=LESSONS_MENU_TEXT):
    values = list()
    for i,m in enumerate(LESSON_DATA):
        if is_module_completed(i):
            if len(m['lessons']) == 0: # empty module (chapter)
                c = 'magenta'
            else:
                c = 'green'
        else:
            c = 'red'
        values.append((i, HTML('<ansi%s>%s</ansi%s>' % (c,m['module_name'],c))))
    return radiolist_dialog(title=title, text=text, style=APP_STYLE, values=values)

# run a selected lesson module (aka chapter)
def run_lesson_module(module_ind, text=LESSON_TEXT):
    if module_ind is None:
        return
    module = LESSON_DATA[module_ind]
    if len(module['lessons']) == 0:
        return message_dialog(title=HTML(module['module_name']), text=EMPTY_MODULE_TEXT, style=APP_STYLE).run()
    else:
        values = list()
        for i,l in enumerate(module['lessons']):
            if is_lesson_completed(module_ind,i):
                c = 'green'
            else:
                c = 'red'
            values.append((i, HTML('<ansi%s>%s</ansi%s>' % (c,l['lesson_name'],c))))
        return radiolist_dialog(title=HTML(module['module_name']), text=text, style=APP_STYLE, values=values).run()

# run a selected lesson (aka subchapter)
def run_lesson(module_ind, lesson_ind):
    if module_ind is None or lesson_ind is None:
        return
    lesson = LESSON_DATA[module_ind]['lessons'][lesson_ind]
    if len(lesson['steps']) == 0:
        message_dialog(title=lesson['lesson_name'], text=EMPTY_LESSON_TEXT, style=APP_STYLE).run()
    elif len(lesson['steps']) == 1:
        SAVE_DATA['completed'][module_ind][lesson_ind][0] = True; save_game()
        button_dialog(title='%s (1/1)' % lesson['lesson_name'], text=HTML(lesson['steps'][0]['text']), style=APP_STYLE, buttons=[('Back', None)]).run()
    else:
        curr_step = 0
        while True:
            if curr_step is None:
                break
            curr_step_data = lesson['steps'][curr_step]
            curr_title = '%s (%d/%d)' % (lesson['lesson_name'], curr_step+1, len(lesson['steps']))
            if 'challenge' in curr_step_data: # challenge step
                solved = False

                # select all challenge
                if curr_step_data['challenge']['type'] == 'select_all':
                    options = curr_step_data['challenge']['options']
                    correct = {v for b,v in options if b}
                    values = [(v,HTML(v)) for b,v in options]
                    answer = checkboxlist_dialog(title=curr_title, text=HTML(curr_step_data['text']), style=APP_STYLE, values=values).run()
                    if answer is None:
                        if curr_step == 0:
                            curr_step = None
                        else:
                            curr_step = curr_step - 1
                    elif set(answer) == correct:
                        solved = True; message_dialog(title=curr_title, text=HTML(CHALLENGE_CORRECT_MESSAGE), style=APP_STYLE).run()
                    else:
                        message_dialog(title=curr_title, text=HTML(CHALLENGE_INCORRECT_MESSAGE), style=APP_STYLE).run()

                # multiple choice (select 1) challenge
                elif curr_step_data['challenge']['type'] == 'multiple_choice':
                    options = curr_step_data['challenge']['options']
                    correct = curr_step_data['challenge']['answer']
                    values = [(b,HTML(v)) for b,v in options]
                    answer = radiolist_dialog(title=curr_title, text=HTML(curr_step_data['text']), style=APP_STYLE, values=values).run()
                    if answer is None:
                        if curr_step == 0:
                            curr_step = None
                        else:
                            curr_step = curr_step - 1
                    elif answer == correct:
                        solved = True; message_dialog(title=curr_title, text=HTML(CHALLENGE_CORRECT_MESSAGE), style=APP_STYLE).run()
                    else:
                        message_dialog(title=curr_title, text=HTML(CHALLENGE_INCORRECT_MESSAGE), style=APP_STYLE).run()

                # short answer challenge
                elif curr_step_data['challenge']['type'] == 'short_answer':
                    correct = curr_step_data['challenge']['answer'].strip()
                    answer = input_dialog(title=curr_title, text=HTML(curr_step_data['text']), style=APP_STYLE).run()
                    if answer is None:
                        if curr_step == 0:
                            curr_step = None
                        else:
                            curr_step = curr_step - 1
                    elif answer.strip() == correct:
                        solved = True; message_dialog(title=curr_title, text=HTML(CHALLENGE_CORRECT_MESSAGE), style=APP_STYLE).run()
                    else:
                        message_dialog(title=curr_title, text=HTML(CHALLENGE_INCORRECT_MESSAGE), style=APP_STYLE).run()

                # math challenge
                elif curr_step_data['challenge']['type'] == 'math':
                    correct = curr_step_data['challenge']['answer']
                    answer = input_dialog(title=curr_title, text=HTML(curr_step_data['text']), style=APP_STYLE).run()
                    if answer is None:
                        if curr_step == 0:
                            curr_step = None
                        else:
                            curr_step = curr_step - 1
                    else:
                        try:
                            answer = float(answer)
                        except:
                            answer = None; message_dialog(title=curr_title, text=HTML(CHALLENGE_MATH_INVALID_NUM), style=APP_STYLE).run()
                        if answer is not None:
                            if abs(float(answer)-correct) < curr_step_data['challenge']['tolerance']:
                                solved = True; message_dialog(title=curr_title, text=HTML(CHALLENGE_CORRECT_MESSAGE), style=APP_STYLE).run()
                            else:
                                message_dialog(title=curr_title, text=HTML(CHALLENGE_INCORRECT_MESSAGE), style=APP_STYLE).run()

                # challenge type not yet implemented
                else:
                    raise NotImplementedError("Need to implement challenge type: %s" % curr_step_data['challenge']['type'])
                if solved:
                    SAVE_DATA['completed'][module_ind][lesson_ind][curr_step] = True; save_game()
                    if curr_step == len(lesson['steps'])-1:
                        curr_step = None
                    else:
                        curr_step = curr_step + 1
            else: # regular text step
                SAVE_DATA['completed'][module_ind][lesson_ind][curr_step] = True; save_game()
                buttons = list()
                if curr_step != len(lesson['steps'])-1:
                    buttons.append(('Next',curr_step+1))
                if curr_step != 0:
                    buttons.append(('Prev',curr_step-1))
                buttons.append(('Cancel',None))
                curr_step = button_dialog(title=curr_title, text=HTML(curr_step_data['text']), style=APP_STYLE, buttons=buttons).run()

# styles app (returns which style to use)
def styles_app(title=STYLES_TITLE, text=STYLES_TEXT):
    return radiolist_dialog(title=title, text=text, style=APP_STYLE, values=[(s,s) for s in STYLES])

# about message app (returns None)
def about_app(title=ABOUT_TITLE, text=ABOUT_MESSAGE):
    return message_dialog(title=title, text=text, style=APP_STYLE)

# organize apps
APPS = {
    'about':      about_app,
    'lessons':    lessons_app,
    'main_menu':  main_menu_app,
    'styles':     styles_app,
    'welcome':    welcome_app,
}
def run_app(s):
    if s not in APPS:
        raise KeyError("Invalid app: %s" % s)
    return APPS[s]().run()

# main program execution
if __name__ == "__main__":
    # load lesson data
    for module_folder in glob('%s/module*' % LESSONS_PATH):
        curr = load_json('%s/meta.json' % module_folder)
        curr['lessons'] = [load_json(lesson_json) for lesson_json in glob('%s/lesson*.json' % module_folder)]
        LESSON_DATA.append(curr)

    # load save data
    if exists(SAVE_FILE_PATH):
        f = open(SAVE_FILE_PATH,'rb'); SAVE_DATA = pload(f); f.close(); APP_STYLE = SAVE_DATA['style']
    else:
        SAVE_DATA = {'completed':[[[False for s in l['steps']] for l in m['lessons']] for m in LESSON_DATA], 'style':APP_STYLE}
        makedirs(dirname(SAVE_FILE_PATH), exist_ok=True); save_game()

    # maximize terminal if possible (only supports Windows)
    maximize_console()

    # prep
    set_title(TITLE_STR)
    run_app('welcome')
    curr_app = 'main_menu'

    # game loop
    while curr_app is not None:
        # Main Menu (pick next app)
        if curr_app == 'main_menu':
            curr_app = run_app(curr_app)

        # Styles Menu (pick style, set next app to Main Menu)
        elif curr_app == 'styles':
            tmp_style = run_app(curr_app)
            if tmp_style is not None:
                APP_STYLE = STYLES[tmp_style]; SAVE_DATA['style'] = APP_STYLE; save_game()
            curr_app = 'main_menu'

        # Lessons Menu (choose a lesson)
        elif curr_app == 'lessons':
            curr_module = 'dummy'
            while True:
                curr_module = run_app(curr_app)
                if curr_module is None:
                    break
                while True:
                    curr_lesson = run_lesson_module(curr_module)
                    if curr_lesson is None:
                        break
                    while True:
                        curr_lesson = run_lesson(curr_module, curr_lesson)
                        if curr_lesson is None:
                            break
            curr_app = 'main_menu'

        # About Page
        elif curr_app == 'about':
            run_app(curr_app); curr_app = 'main_menu'

        # Invalid current app
        else:
            raise ValueError("Invalid current app: %s" % curr_app)
