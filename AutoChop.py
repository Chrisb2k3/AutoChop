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
        self.d_img_files: dict = {}
        if obj_type == 'bos':
            obj_index: str = 'bos_img_files'
        elif obj_type == 'rss':
            obj_index: str = 'rss_img_files'
        elif obj_type == 'blg':
            obj_index: str = 'blg_img_files'
        else:
            obj_index: str = 'ui1_img_files'

        util.debug('game_data.d_cookie[obj_index] ', game_data.d_cookie[obj_index])

        if game_data.d_cookie[obj_index]:
            for value in game_data.d_cookie[obj_index].split(','):
                l_file_names: list = value
            for key, value in l_file_names.split(':'):
                self.d_img_files[key] = value
            util.debug('self.d_img_files', self.d_img_files)
        self.init_list(obj_type)

    def init_list(self, obj_type):

        dir_files: str = game_data.d_cookie['dir_files']

        if not game_data.d_cookie['dir_files']:
            for line in os.listdir("./images"):
                if not line == 'unused':
                    dir_files += util.add_delimiter(dir_files, line, ',')
                    game_data.d_cookie['dir_files'] = dir_files

        for file_name in dir_files.split(','):
            obj = re.search(r'^\w{3}', file_name).group(0)
            name = re.search(r'^[\w_{4}]*', file_name).group(0).split('_', 1)[1]

            if obj == obj_type:
                util.debug('name//file_name', name, file_name)
                self.d_img_files[name] = file_name

    @staticmethod
    def scout_selection(selection: str):
        img_file_names: str = game_data.d_cookie['scout_list']

        obj_type = util.regex(selection, ':', '<')
        selection = util.regex(selection, ':', '>')

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
                        # util.debug('i//key', i, key)
                        img_file_names += util.add_delimiter(img_file_names, d_img_files[key], ',')

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

        scout_menu_options = (f'1. Starting X Coordinates: \n'
                              f'2. Starting Y Coordinates: \n'
                              f'4. Horizontal Distance(km) to Scout Left:\n'
                              f'3. Vertical Distance(km) to Scout Down: \n'
                              f'5. Screen Mode (Portrait/Landscape): \n'
                              f'6. Minimum Power Value: \n'
                              f'7. Maximum Power Value: \n\n'
                              f'Example: 200,300,1200,350,Landscape,100,900')

        self.label_scout_options = tk.Label(text=scout_menu_options, anchor='n', justify=LEFT)
        self.label_scout_options.place(x=10, y=400, height=200, width=400)

        self.input_scout_options = tk.Text(self.frame)
        self.input_scout_options.place(x=10, y=600, height=30, width=480)
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
        self.max_tile_left: int = 0
        self.max_tile_down: int = 0
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
            'dir_files': '',
            'ui1_img_files': '',
            'bos_selected': '',
            'rss_selected': '',
            'blg_selected': '',
            'obj_min_powers': '',
            'obj_max_powers': '',
            'scout_list': '',
            'scout_options': '',
            'found_scr_objs': '',
            'found_tile_objs': '',
            'ocr_tile_xy_center': '',
            'ocr_obj_xy': '',
            'ocr_bos_lvl': '',
            'ocr_obj_powers': '',
            'CS_goto_xy': ''
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
                    self.max_tile_left = self.start_x - math.ceil(int(item) * .73)  # .73 dist conversion to tile coord
                elif i == 3:
                    self.max_tile_down = self.start_y + math.ceil(int(item) * .73)  # .73 dist conversion to tile coord
                elif i == 4:
                    self.scr_mode = item
                elif i == 5:
                    self.d_cookie['obj_min_powers'] = item
                elif i == 6:
                    self.d_cookie['obj_max_powers'] = item

        self.d_cookie['ocr_tile_xy_center'] = '867,895,159,24'
        self.d_cookie['ocr_bos_lvl'] = '694,235,53,75'
        self.d_cookie['ocr_obj_powers'] = '784,186,140,198'
        self.d_cookie['ocr_obj_xy'] = '1030,203,156,270'
        self.d_cookie['CS_goto_xy'] = '941,903;660,668;1304,659;957,913'

    def data_file(self, action: str = 'w', update_item: str = 'py_cookie'):
        save_str: str = ''

        with open(self.text_file, action) as text_file:
            if action == 'r':
                for item_line in text_file.read().split('|'):
                    if len(item_line.strip()):
                        key = util.regex(item_line, ':', '<')
                        value = util.regex(item_line, ':', '>')
                        self.d_cookie[key] = value

            if action == 'w':
                for key, value in self.d_cookie.items():
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
    found_scr_coords: str = ''
    found_tile_coords: str = ''

    global l_obj_found
    expired_time: float = 0

    # pag.useImageNotFoundException()
    try:
        for img_file_name in game_data.d_cookie['scout_list'].split(','):
            util.debug('img_file_name', img_file_name)
            l_obj_found.append(list(pag.locateAllOnScreen(game_data.img_path + img_file_name, confidence=0.7)))
            util.debug('l_obj_found -try', l_obj_found, prompt=True)

    except:
        l_obj_found.clear()
    else:
        pass

    if l_obj_found:
        scr_location = g_util.ocr(game_data.d_cookie['ocr_tile_xy_center'])
        scr_location = f'{g_util.scrub_data(scr_location, source='ocr', return_val='a_str')}:'

        for each_list in l_obj_found:
            for box in each_list:
                scr_x, scr_y = pag.center(box)  # extract scr x/y coords of found obj

                if not g_util.coords_logged(scr_x, scr_y, old_value_x, old_value_y):  # group same obj findings
                    found_scr_coords += util.add_delimiter(found_scr_coords, f'{scr_x},{scr_y}', ';')
                    old_value_x, old_value_y = scr_x, scr_y
                    tile_x, tile_y = get_tile_coords(scr_x, scr_y)
                    get_tile_coords(scr_x, scr_y)
                    found_tile_coords += util.add_delimiter(found_tile_coords, f'{tile_x},{tile_y}', ';')

        util.debug('out of loop // found_scr_coords// found_tile_coords', found_scr_coords,
                   found_tile_coords, prompt=True)
        game_data.d_cookie['found_scr_objs'] = scr_location + found_scr_coords
        game_data.d_cookie['found_tile_objs'] = scr_location + found_tile_coords

        l_obj_found.clear()


def get_tile_coords(scr_x: int, scr_y: int) -> list:
    power_value = ''
    pag.click(scr_x, scr_y, 1, 1, 'left')  # click on found obj
    pag.sleep(1)

    if find_img_and_click(game_ui1.d_img_files['attack']):

        # get ocr obj powers
        ocr_powers: str = g_util.ocr(game_data.d_cookie['ocr_obj_powers'])
        regex_result: str = util.regex(ocr_powers, separator='.', grab='<')
        obj_powers: list = g_util.scrub_data(regex_result, source='ocr')

        # power_value: str = [value for value in obj_powers]
        for value in obj_powers:
            power_value = value

        if power_value in range(int(game_data.d_cookie['obj_min_powers']), int(game_data.d_cookie['obj_max_powers'])):
            obj_tile_coords: str = g_util.ocr(game_data.d_cookie['ocr_obj_xy'])
            obj_tile_coords: list = g_util.scrub_data(obj_tile_coords, source='ocr')
            util.debug('get_tile_coords()// obj_tile_coords // power_value', 'obj detail screen',
                       obj_tile_coords, power_value, prompt=True)

            return obj_tile_coords

    else:
        print("Image not found")


def find_img_and_click(img_file: str) -> bool:
    return_value: bool = False
    img_file = game_data.img_path + img_file
    t_result: tuple = pag.locateCenterOnScreen(img_file, confidence=0.7)

    if t_result:
        scr_x, scr_y = t_result
        pag.click(scr_x, scr_y, 1, 1, 'left')  # now in obj detail screen
        return_value = True

    return return_value


def process_found_objs():
    scr_id_xy: str = util.regex(game_data.d_cookie['found_tile_objs'], ':', '<').strip()
    found_coords: str = util.regex(game_data.d_cookie['found_tile_objs'], ':', '>').strip()

    x, y = scr_id_xy.split(',')
    g_util.goto_coords(x, y, game_data)  # goto current screen

    for coord in found_coords.split(';'):
        x, y = coord.split(',')
        # g_util.goto_coords(x, y, game_data)  # goto current screen
        pag.click(x, y, 1, 1, 'left')  # click on found obj

        find_img_and_click(game_ui1.d_img_files['share'])

    game_data.d_cookie['found_scr_objs'] = ''  # Reset


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

                if game_data.d_cookie['found_scr_objs']:
                    found_coords: str = util.regex(game_data.d_cookie['found_scr_objs'], ':', '>')
                    for pair in g_util.scrub_data(found_coords):
                        scr_x, scr_y = pair
                        get_tile_coords(int(scr_x), int(scr_y))

                    process_found_objs()
                    game_data.d_cookie['found_scr_objs'] = ''  # Reset
                nav.x -= nav.next_scr_left_x
                nav.y += nav.next_scr_left_y

    print('Application Exit.')


if __name__ == "__main__":
    game_data = GameData()
    game_bos = GameObj('bos')
    game_rss = GameObj('rss')
    game_blg = GameObj('blg')
    game_ui1 = GameObj('ui1')
    # game_idl = GameObj('idl')
    scout_menu = Menu()
    scout_menu.root.mainloop()
    nav = ScreenNavigation()
    main()
    # city_obj = GameObj.create_img_file_obj('cty')   # In city objects
    # ui_obj = GameObj.create_img_file_obj('uii')     # user interface items
