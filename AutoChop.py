import math
import os
import re
import tkinter as tk
from time import time
from tkinter import LEFT, END

import keyboard
import pyautogui as pag

from util import *
from util import *

from util.util import *
from util.game_util import *

g_loop: bool = False


# ------------------> Classes -------------------------------------------------

class GameObj:
    def __init__(self, obj_type):
        self.d_img_files: dict = {}
        self.init_list(obj_type)

    def init_list(self, obj_type):
        dir_files: str = ''

        for line in os.listdir("./images"):
            if not line == 'unused':
                dir_files += add_delimiter(dir_files, line, ',')
                game_data.d_cookie['dir_files'] = dir_files

        for file_name in dir_files.split(','):
            obj = re.search(r'^\w{3}', file_name).group(0)
            name = re.search(r'^[\w_{4}]*', file_name).group(0).split('_', 1)[1]

            if obj == obj_type:
                self.d_img_files[name] = file_name

    @staticmethod
    def scout_selection(selection: str):
        img_file_names: str = game_data.d_cookie['scout_list']

        obj_type, selection = selection.split(':')

        if len(selection):
            if obj_type == 'rss':
                d_img_files: dict = game_rss.d_img_files
            elif obj_type == 'blg':
                d_img_files: dict = game_blg.d_img_files
            elif obj_type == 'ui1':
                d_img_files: dict = game_ui1.d_img_files
            else:
                d_img_files: dict = game_bos.d_img_files

            l_key_names: list = list(d_img_files.keys())

            for choice in selection.split(','):
                for i, key in enumerate(l_key_names):
                    if i == int(choice):
                        # debug('i//key', i, key)
                        img_file_names += add_delimiter(img_file_names, d_img_files[key], ',')

            game_data.d_cookie['scout_list'] = img_file_names


class Menu:
    def __init__(self):
        self.content_bos1: str = ''
        self.content_bos2: str = ''
        self.content_rss: str = ''
        self.content_blg: str = ''
        self.init_display_content()

        self.root = tk.Tk()
        self.root.title("Scout Selection Menu")
        self.frame = tk.Frame(self.root, width=650, height=800)
        self.frame.pack()

        self.label_bos1 = tk.Label(text=self.content_bos1, anchor='n', justify=LEFT)
        self.label_bos1.place(x=5, y=10, height=320, width=200)
        self.label_bos2 = tk.Label(text=self.content_bos2, anchor='n', justify=LEFT)
        self.label_bos2.place(x=200, y=10, height=320, width=200)
        self.label_rss = tk.Label(text=self.content_rss, anchor='n', justify=LEFT)
        self.label_rss.place(x=380, y=10, height=320, width=100)
        self.label_blg = tk.Label(text=self.content_blg, anchor='n', justify=LEFT)
        self.label_blg.place(x=510, y=10, height=320, width=100)

        self.input_bos = tk.Text(self.frame)
        self.input_bos.place(x=10, y=330, height=30, width=350)
        self.input_bos.insert("1.0", game_data.d_cookie['bos_selected'])

        self.input_rss = tk.Text(self.frame)
        self.input_rss.place(x=380, y=330, height=30, width=110)
        self.input_rss.insert("1.0", game_data.d_cookie['rss_selected'])

        self.input_blg = tk.Text(self.frame)
        self.input_blg.place(x=500, y=330, height=30, width=120)
        self.input_blg.insert("1.0", game_data.d_cookie['blg_selected'])

        self.label_input = tk.Label(text="  Selection:  BOSS\t\t\t           RSS\t    BUILDINGS", anchor='w')
        self.label_input.place(x=0, y=360, height=30, width=600)

        scout_menu_options = (f'1. Starting X Coordinate\n'
                              f'2. Starting Y Coordinate\n'
                              f'4. Horizontal Distance(km) to Scout Left\n'
                              f'3. Vertical Distance(km) to Scout Down\n'
                              f'5. Screen Mode (Portrait/Landscape)\n'
                              f'6. Minimum Power Value\n'
                              f'7. Maximum Power Value\n'
                              f'8. Share Link to (Image Filename)\n\n'
                              f'Example: 200,300,1200,350,Landscape,100,900,logo_sav')

        self.label_scout_options = tk.Label(text=scout_menu_options, anchor='n', justify=LEFT)
        self.label_scout_options.place(x=10, y=410, height=200, width=450)

        self.input_scout_options = tk.Text(self.frame)
        self.input_scout_options.place(x=10, y=630, height=30, width=600)
        self.input_scout_options.insert("1.0", game_data.d_cookie['scout_options'])

        btn_cancel = tk.Button(self.frame, text="Cancel", command=self.hide_window)
        btn_cancel.place(x=400, y=700, height=30, width=100)
        btn_submit = tk.Button(self.frame, text="OK", command=self.submit_input)
        btn_submit.place(x=520, y=700, height=30, width=100)

    def init_display_content(self):
        game_data.set_variable()

        for i, value in enumerate(list(game_bos.d_img_files.keys())):
            if i < 12:
                self.content_bos1 += f'{i:02}. {value}\n'
            else:
                self.content_bos2 += f'{i:02}. {value}\n'

        for i, value in enumerate(list(game_rss.d_img_files.keys())):
            self.content_rss += f'{i:02}. {value}\n'

        for i, value in enumerate(list(game_blg.d_img_files.keys())):
            self.content_blg += f'{i:02}. {value}\n'

    def hide_window(self):
        self.root.withdraw()

    def submit_input(self):
        self.hide_window()

        # Get user selection from text box
        game_data.d_cookie['bos_selected'] = self.input_bos.get("1.0", END)
        game_data.d_cookie['rss_selected'] = self.input_rss.get("1.0", END)
        game_data.d_cookie['blg_selected'] = self.input_blg.get("1.0", END)
        game_data.d_cookie['scout_options'] = self.input_scout_options.get("1.0", END)

        # build image file names (to use with pyautogui for detection) from user selection
        game_data.d_cookie['scout_list'] = ''  # reset list to avoid duplicating
        game_bos.scout_selection('bos:' + game_data.d_cookie['bos_selected'].strip())
        game_rss.scout_selection('rss:' + game_data.d_cookie['rss_selected'].strip())
        game_blg.scout_selection('blg:' + game_data.d_cookie['blg_selected'].strip())

        # update cookie dictionary record to be saved to file later
        game_data.data_file('w')
        game_data.set_variable()  # reset init variables
        self.root.destroy()


class GameData:
    def __init__(self):
        self.max_game_left: int = 0
        self.max_game_down: int = 0
        self.start_x: int = 0
        self.start_y: int = 0
        self.scr_mode = ''
        self.img_path = 'images\\'
        self.scout_options: str = 'None'
        self.text_file: str = 'cookiepy.txt'

        self.d_cookie: dict = {
            'bos_img_files': '',
            'rss_img_files': '',
            'blg_img_files': '',
            'ui1_img_files': '',
            'bos_selected': '',
            'rss_selected': '',
            'blg_selected': '',
            'obj_min_power': '',
            'obj_max_power': '',
            'scout_list': '',
            'scout_options': '',
            'found_scr_objs': '',
            'ocr_game_xy': '',
            'ocr_obj_xy': '',
            'ocr_bos_lvl': '',
            'ocr_obj_power': '',
            'share_link_to': '',
            'cs_goto_xy': ''
        }
        self.data_file('r')  # Setup d_cookie
        self.set_variable()
        self.data_file('w')  # Setup d_cookie

    def set_variable(self) -> None:
        for i, item in enumerate(self.d_cookie['scout_options'].split(',')):
            if item:
                item = item.strip()
                if i == 0:
                    self.start_x = int(item)
                elif i == 1:
                    self.start_y = int(item)
                elif i == 2:
                    self.max_game_left = self.start_x - math.ceil(int(item) * .73)  # .73 dist conversion to tile coord
                elif i == 3:
                    self.max_game_down = self.start_y + math.ceil(int(item) * .73)  # .73 dist conversion to tile coord
                elif i == 4:
                    self.scr_mode = item
                elif i == 5:
                    self.d_cookie['obj_min_power'] = item
                elif i == 6:
                    self.d_cookie['obj_max_power'] = item
                elif i == 7:
                    self.d_cookie['share_link_to'] = item

        self.d_cookie['ocr_game_xy'] = '867,895,159,24'
        self.d_cookie['ocr_bos_lvl'] = '694,235,53,75'
        self.d_cookie['ocr_obj_power'] = '784,186,140,198'
        self.d_cookie['ocr_barb_power'] = '1240,679,281,61'
        self.d_cookie['ocr_obj_xy'] = '1030,203,156,270'
        self.d_cookie['cs_goto_xy'] = '941,903;660,668;1304,659;957,913'

    def data_file(self, action: str = 'w', update_item: str = 'py_cookie'):
        save_str: str = ''

        with open(self.text_file, action) as text_file:
            if action == 'r':
                for item_line in text_file.read().split('|'):
                    if len(item_line.strip()):
                        key, value = item_line.split(':')
                        self.d_cookie[key] = value

            if action == 'w':
                for key, value in self.d_cookie.items():
                    concat_str = f'{key.strip()}:{value.strip()}'
                    save_str += add_delimiter(save_str, concat_str, '|')

                text_file.write(save_str)


class ScreenNavigation:
    def __init__(self):
        self.x: int = 0
        self.y: int = 0

        if game_data.scr_mode == 'Landscape':
            val1, val2, val3, val4 = 11, 12, 11, 11
        else:
            val1, val2, val3, val4 = -3, 3, 11, 11

        self.next_scr_left_x = val1
        self.next_scr_left_y = val2
        self.next_scr_down_x = val3
        self.next_scr_down_y = val4

        self.scan_area_x = 174
        self.scan_area_y = 152
        self.scan_area_w = 1690 - self.scan_area_x
        self.scan_area_h = 858 - self.scan_area_y


# ------------------> FUNCTIONS -----------------------------------------------
def find_obj() -> bool:
    saved_x: int = 0
    saved_y: int = 0
    found_scr_coords: str = ''
    found: bool = False

    # pag.useImageNotFoundException()
    try:
        for img_file_name in game_data.d_cookie['scout_list'].split(','):
            all_occurrences = pag.locateAllOnScreen(game_data.img_path + img_file_name, confidence=0.7)

            if all_occurrences:
                for occurrence in all_occurrences:
                    scr_x = int(occurrence.left + (occurrence.width / 2))
                    scr_y = int(occurrence.top + (occurrence.height / 2))

                    if not coords_logged(scr_x, scr_y, saved_x, saved_y):  # group same occurrence to one obj
                        found_scr_coords += add_delimiter(found_scr_coords, f'{scr_x},{scr_y}', ';')
                        saved_x, saved_y = scr_x, scr_y
                        found = True

                game_data.d_cookie['found_scr_objs'] = found_scr_coords

    except:
        print('in except to find obj')

    else:
        print('in else to find obj')
        pass

    debug('l_obj_found??', game_data.d_cookie['found_scr_objs'])

    return found


def check_obj_power(scr_x: int, scr_y: int) -> bool:
    validated: bool = False
    pag.click(scr_x, scr_y, 1, 1, 'left')  # click on found obj
    pag.sleep(1)

    if find_img_and_click(game_ui1.d_img_files['attack']):
        # get ocr obj powers
        ocr_power: str = ocr(game_data.d_cookie['ocr_obj_power'])
        obj_power: list = scrub_data(ocr_power.split('.')[0], source='ocr')

        for value in obj_power:
            min_val = int(game_data.d_cookie['obj_min_power'])
            max_val = int(game_data.d_cookie[
                              'obj_max_power'])

            debug('ocr power scrubbed/stored min/stored max', value,min_val, max_val)

            # if int(value) in range(int(game_data.d_cookie['obj_min_power']), int(game_data.d_cookie['obj_max_power'])):
            if int(value) in range(min_val, max_val):
                validated = True
                pag.hotkey('esc')

    return validated


def find_img_and_click(img_files: str) -> bool:
    occurrence: tuple = ()
    return_value: bool = False

    # pag.useImageNotFoundException()
    try:
        for each_img in img_files.split(','):
            img_file = game_data.img_path + each_img
            # debug('ui image file',img_file, prompt=True)
            occurrence = pag.locateCenterOnScreen(img_file, confidence=0.7)

        if occurrence:
            scr_x: int = int(occurrence.x)
            scr_y: int = int(occurrence.y)

            pag.click(scr_x, scr_y, 1, 1, 'left')  # now in obj detail screen
            return_value = True

    except:
        pass
    else:
        pass

    return return_value


def process_found_obj(scr_x: int, scr_y: int) -> None:
    i: int = 1

    if check_obj_power(scr_x, scr_y):

        for coord in game_data.d_cookie['found_scr_objs'].split(';'):
            debug('found obj count:', i)
            i += 1
            goto_coords(nav.x, nav.y, game_data)  # goto current scr / power check might've moved scr coords

            found_x, found_y = coord.split(',')
            debug('each_coord/found_x/found_y',coord,found_x,found_y)
            pag.click(int(found_x), int(found_y), 1, 1, 'left')  # click on found obj

            find_img_and_click(game_ui1.d_img_files['share'])
            find_img_and_click(game_car.d_img_files[game_data.d_cookie['share_link_to']])
            find_img_and_click(game_ui1.d_img_files['confirm'])

    game_data.d_cookie['found_scr_objs'] = ''  # Reset


def main() -> None:
    global g_loop

    pag.sleep(3)  # seconds
    keyboard.add_hotkey('f2', pause)
    keyboard.add_hotkey('q', exit_loop)  # Register the 'q' key to call the exit_loop function

    g_loop = True
    while g_loop:
        nav.x = game_data.start_x
        nav.y = game_data.start_y

        while nav.y < game_data.max_game_down:
            while nav.x > game_data.max_game_left:
                loop_time = time()
                pag.screenshot(region=(nav.scan_area_x, nav.scan_area_y, nav.scan_area_w, nav.scan_area_h))
                print("FPS {}".format(1 / (time() - loop_time)))

                goto_coords(nav.x, nav.y, game_data)  # goto current screen
                pag.sleep(2)  # wait for screen to refresh

                if find_obj():
                    for pair_xy in game_data.d_cookie['found_scr_objs'].split(';'):
                        scr_x, scr_y = pair_xy.split(',')
                        process_found_obj(int(scr_x), int(scr_y))

                    game_data.d_cookie['found_scr_objs'] = ''  # Reset
                nav.x -= nav.next_scr_left_x
                nav.y += nav.next_scr_left_y

    print('exiting AC')


if __name__ == "__main__":
    game_data = GameData()
    game_bos = GameObj('bos')
    game_rss = GameObj('rss')
    game_blg = GameObj('blg')
    game_ui1 = GameObj('ui1')  # options or prompts
    game_car = GameObj('car')  # non-world click area: menu selection etc
    #  debug('game_car',game_car.d_img_files,prompt=True)
    scout_menu = Menu()
    scout_menu.root.mainloop()
    nav = ScreenNavigation()
    main()
