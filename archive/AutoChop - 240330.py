import math
import os
import re
import tkinter as tk
from time import time
from tkinter import LEFT, END

import keyboard
import pyautogui as pag

import game_util as g_util
import util

l_obj_found: list = []
g_loop: bool = False


# ------------------> Classes -------------------------------------------------

class GameObj:
    def __init__(self, obj_type):
        self.names = []
        self.img_files = []
        self.init_list(obj_type)

    def init_list(self, obj_type):
        file_names: list = []

        for line in os.listdir("./images"):
            if not line == 'unused':
                file_names.append(line)

        for line in file_names:
            if not line == '':
                # obj: str = util.regex(line, '_', '<')
                # name: str = util.regex(line, '_', '>')
                obj = re.search(r'^\w{3}', line).group(0)
                name = re.search(r'^[\w_{4}]*', line).group(0).split('_', 1)[1]

                if obj == obj_type:
                    self.names.append(name)
                    self.img_files.append(line)
                    util.debug('name // line', name, line)

    @staticmethod
    def scout_selection(selection: str, which_list: list):
        l_obj_name: list = []

        img_file_names: str = game_data.d_cookie['scout_list']

        obj_type = util.regex(selection, ':', '<')
        selection = util.regex(selection, ':', '>')

        if obj_type == 'bos':
            l_img_files: list = game_bos.img_files
        elif obj_type == 'rss':
            l_img_files: list = game_rss.img_files
        elif obj_type == 'blg':
            l_img_files: list = game_blg.img_files
        else:
            l_img_files: list = game_bos.img_files

        if len(selection):
            for idx in selection.split(','):
                l_obj_name.append(which_list[int(idx)])

            for name in l_obj_name:
                for line in l_img_files:
                    pattern = re.search(r'(?i)\w' + name, line)  # (?i) ignore case
                    if pattern:
                        img_file_names += util.add_delimiter(img_file_names, line, ',')

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
        self.label_bos1.place(x=5, y=10, height=300, width=200)
        self.label_bos2 = tk.Label(text=self.content_bos2, anchor='n', justify=LEFT)
        self.label_bos2.place(x=200, y=10, height=300, width=200)
        self.label_rss = tk.Label(text=self.content_rss, anchor='n', justify=LEFT)
        self.label_rss.place(x=400, y=10, height=300, width=100)
        self.label_blg = tk.Label(text=self.content_blg, anchor='n', justify=LEFT)
        self.label_blg.place(x=510, y=10, height=300, width=100)

        self.input_bos = tk.Text(self.frame)
        self.input_bos.place(x=10, y=320, height=30, width=350)
        self.input_bos.insert("1.0", game_data.d_cookie['bos_selected'])

        self.input_rss = tk.Text(self.frame)
        self.input_rss.place(x=380, y=320, height=30, width=110)
        self.input_rss.insert("1.0", game_data.d_cookie['rss_selected'])

        self.input_blg = tk.Text(self.frame)
        self.input_blg.place(x=500, y=320, height=30, width=120)
        self.input_blg.insert("1.0", game_data.d_cookie['blg_selected'])

        self.label_input = tk.Label(text="Selection: (Boss)\t\t\t            (RSS)\t   (Buildings)", anchor='w')
        self.label_input.place(x=0, y=360, height=30, width=600)

        scout_menu_options = (f'1. Input Starting X Coordinates: \n'
                              f'2. Input Starting Y Coordinates: \n'
                              f'4. Input Horizontal Distance(km) to Scout Left:\n'
                              f'3. Input Vertical Distance(km) to Scout Down: \n'
                              f'5. Screen Mode (Portrait/Landscape): \n\n'
                              f'Example: 200,300,1200,350,Landscape')

        self.label_scout_options = tk.Label(text=scout_menu_options, anchor='n', justify=LEFT)
        self.label_scout_options.place(x=10, y=400, height=200, width=400)

        self.input_scout_options = tk.Text(self.frame)
        self.input_scout_options.place(x=10, y=600, height=30, width=360)
        self.input_scout_options.insert("1.0", game_data.d_cookie['scout_options'])

        btn_cancel = tk.Button(self.frame, text="Cancel", command=self.hide_window)
        btn_cancel.place(x=400, y=700, height=30, width=100)
        btn_submit = tk.Button(self.frame, text="OK", command=self.submit_input)
        btn_submit.place(x=520, y=700, height=30, width=100)

    def init_display_content(self):
        game_data.set_variable()

        for i, value in enumerate(game_bos.names):
            if i < 12:
                self.content_bos1 += f'{i:02}. {value}\n'
            else:
                self.content_bos2 += f'{i:02}. {value}\n'

        for i, value in enumerate(game_rss.names):
            self.content_rss += f'{i:02}. {value}\n'

        for i, value in enumerate(game_blg.names):
            self.content_blg += f'{i:02}. {value}\n'

    def hide_window(self):
        self.root.withdraw()

    def submit_input(self):
        save_str = ''
        self.hide_window()

        # Get user selection from text box
        game_data.d_cookie['bos_selected'] = self.input_bos.get("1.0", END)
        game_data.d_cookie['rss_selected'] = self.input_rss.get("1.0", END)
        game_data.d_cookie['blg_selected'] = self.input_blg.get("1.0", END)
        game_data.d_cookie['scout_options'] = self.input_scout_options.get("1.0", END)

        # build image file names (to use with pyautogui for detection) from user selection
        game_data.d_cookie['scout_list'] = ''  # reset list to avoid duplicating
        game_bos.scout_selection('bos:' + game_data.d_cookie['bos_selected'].strip(), game_bos.names)
        game_rss.scout_selection('rss:' + game_data.d_cookie['rss_selected'].strip(), game_rss.names)
        game_blg.scout_selection('blg:' + game_data.d_cookie['blg_selected'].strip(), game_blg.names)

        # update cookie list record to be saved to file later
        game_data.data_file('w')
        game_data.set_variable()  # reset init variables
        self.root.destroy()


class GameData:
    def __init__(self):
        self.max_tile_left: int = 0
        self.max_tile_down: int = 0
        self.start_x: int = 0
        self.start_y: int = 0
        self.scr_mode = ''
        self.img_path = 'images\\'
        self.scout_options: str = 'None'
        self.file_cookiepy: str = 'cookiepy.txt'
        self.file_cookie_ahk: str = 'cookieAC.txt'

        self.cookie_ahk = []
        self.d_cookie: dict = {}

        self.data_file('r')  # Setup d_cookie

        self.d_cookie: dict = {
            'bos_selected': '',
            'rss_selected': '',
            'blg_selected': '',
            'scout_list': '',
            'scout_options': '',
            'found_objs': ''
        }
        self.data_file('r')  # Setup d_cookie
        self.d_cookie['CS_goto_coords'] = '(941,903)-(660,668)-(1304,659)-(957,913)'

        self.set_variable()

    def set_variable(self) -> None:
        for i, item in enumerate(self.d_cookie['scout_options'].split(',')):
            if item:
                item = item.strip()
                if i == 0:
                    self.start_x = int(item)
                elif i == 1:
                    self.start_y = int(item)
                elif i == 2:
                    self.max_tile_left = self.start_x - math.ceil(int(item) * .73)  # .73 dist conversion to tile coord
                elif i == 3:
                    self.max_tile_down = self.start_y + math.ceil(int(item) * .73)  # .73 dist conversion to tile coord
                elif i == 4:
                    self.scr_mode = item

    def data_file(self, action: str = 'w', update_item: str = 'py_cookie'):
        save_str: str = ''
        file_name: str = self.file_cookiepy if update_item == 'py_cookie' else self.file_cookie_ahk

        with open(file_name, action) as text_file:
            if action == 'r':
                for item_line in text_file.read().split('|'):
                    if len(item_line.strip()):
                        key = util.regex(item_line, ':', '<')
                        value = util.regex(item_line, ':', '>')

                        if update_item == 'py_cookie':
                            self.d_cookie[key] = value
                        elif update_item == 'cookie_ahk':
                            self.cookie_ahk.append(item_line)

            if action == 'w':
                for key, value in game_data.d_cookie.items():
                    concat_str = f'{key.strip()}:{value.strip()}'
                    save_str += util.add_delimiter(save_str, concat_str, '|')

                text_file.write(save_str)


class ScreenNavigation:
    def __init__(self):
        self.x: int = game_data.start_x
        self.y: int = game_data.start_y

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


def find_obj() -> None:
    old_value_x: int = 0
    old_value_y: int = 0
    found_list: str = ''

    global l_obj_found
    expired_time: float = 0

    # pyautogui.useImageNotFoundException()
    try:
        for img_file_name in game_data.d_cookie['scout_list'].split(','):
            l_obj_found.append(list(pag.locateAllOnScreen(game_data.img_path + img_file_name, confidence=0.7)))
            util.debug('l_obj_found -try', l_obj_found, prompt=True)

    except:
        l_obj_found.clear()
    else:
        pass

    if l_obj_found:
        for each_list in l_obj_found:
            for box in each_list:
                util.debug('x y box typebox', box, type(box), prompt=True)
                scr_x, scr_y = pag.center(box)

                if not g_util.coords_logged(scr_x, scr_y, old_value_x, old_value_y):  # group findings of same obj
                    found_list += util.add_delimiter(found_list, f'({scr_x},{scr_y})', '-')
                    old_value_x, old_value_y = scr_x, scr_y
                    get_game_coords(scr_x, scr_y)

            # g_util.move_to_click(x, y)

        util.debug('out of loop // found_list', found_list, prompt=True)
        game_data.d_cookie['found_objs'] = found_list
        l_obj_found.clear()


def get_game_coords(scr_x: int, scr_y: int) -> list:
    g_util.move_to_click(scr_x, scr_y)


def screen_to_game_coords() -> None:
    tile_coords = util.regex(game_data.d_cookie['found_objs'], ':', '>')
    scr_coords = util.regex(game_data.d_cookie['found_objs'], ':', '<')

    cords_list: list = g_util.scrub_coords(scr_coords)
    for i, pair in enumerate(cords_list):
        x, y = pair
        g_util.move_to_click(x, y)


def main() -> None:
    global l_obj_found
    global g_loop

    pag.sleep(3)  # seconds
    keyboard.add_hotkey('f2', util.pause)
    keyboard.add_hotkey('q', util.exit_loop)  # Register the 'q' key to call the exit_loop function

    g_loop = True
    while g_loop:
        while nav.y < game_data.max_tile_down:
            while nav.x > game_data.max_tile_left:
                pag.sleep(2)

                loop_time = time()
                pag.screenshot(region=(nav.scan_area_x, nav.scan_area_y, nav.scan_area_w, nav.scan_area_h))
                print("FPS {}".format(1 / (time() - loop_time)))

                g_util.goto_coords(nav.x, nav.y, game_data)  # goto current screen
                find_obj()  # find all instances of the obj(s) on current screen
                screen_to_game_coords()
                nav.x -= nav.next_scr_left_x
                nav.y += nav.next_scr_left_y

    print('Application Exit.')


if __name__ == "__main__":
    game_bos = GameObj('bos')
    game_rss = GameObj('rss')
    game_blg = GameObj('blg')
    game_gu1 = GameObj('gu1')
    game_gu1 = GameObj('idl')
    game_data = GameData()
    scout_menu = Menu()
    scout_menu.root.mainloop()
    nav = ScreenNavigation()
    main()
    # city_obj = GameObj.create_img_file_obj('cty')   # In city objects
    # ui_obj = GameObj.create_img_file_obj('uii')     # user interface items
