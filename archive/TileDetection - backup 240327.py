import math
import os
import re
import tkinter as tk
from time import time
from tkinter import LEFT, END

import keyboard
import pyautogui

IMG_PATH = "images\\"

l_obj_found: list = []
g_loop: bool = False


# ------------------> Classes -------------------------------------------------

# class ClickSequence:
#     def __init__(self):
class GameObj:
    def __init__(self):
        self.img_files = []
        for line in os.listdir("./images"):
            if not line == 'unused':
                self.img_files.append(line)

        self.bos_names = []
        self.rss_names = []
        self.blg_names = []
        self.init_list('bos', self.bos_names)
        self.init_list('rss', self.rss_names)
        self.init_list('blg', self.blg_names)

        # self.gui_names = []
        # self.selected_list = []
        # self.init_img_filename_list()

    def init_list(self, prefix, which_obj):
        for line in self.img_files:
            if not line == '':
                pattern = re.search(r'^\w{3}', line).group(0)
                name = re.search(r'^[\w_{4}]*', line).group(0).split('_', 1)[1]
                if pattern == prefix:
                    which_obj.append(name)

    @staticmethod
    def scout_selection(input_str: str, which_list: list):
        lst_obj_name: list = []
        img_file_names: str = game_data.d_cookie['scout_list']

        if len(input_str):
            for idx in input_str.split(','):
                lst_obj_name.append(which_list[int(idx)])

            for name in lst_obj_name:
                for line in game_obj.img_files:
                    pattern = re.search(r'(?i)\w' + name, line)  # (?i) ignore case
                    if pattern:
                        img_file_names += add_delimiter(img_file_names, line, ',')

            game_data.d_cookie['scout_list'] = img_file_names


class Menu:
    def __init__(self):
        self.content_bos: str = ''
        self.content_rss: str = ''
        self.content_blg: str = ''
        self.init_display_content()

        self.root = tk.Tk()
        self.root.title("Scout Selection Menu")
        self.frame = tk.Frame(self.root, width=650, height=800)
        self.frame.pack()

        self.label_bos = tk.Label(text=self.content_bos, anchor='n', justify=LEFT)
        self.label_bos.place(x=10, y=10, height=300, width=200)
        self.label_rss = tk.Label(text=self.content_rss, anchor='n', justify=LEFT)
        self.label_rss.place(x=200, y=10, height=300, width=200)
        self.label_blg = tk.Label(text=self.content_blg, anchor='n', justify=LEFT)
        self.label_blg.place(x=400, y=10, height=300, width=200)

        self.input_bos = tk.Text(self.frame)
        self.input_bos.place(x=10, y=320, height=30, width=180)
        self.input_bos.insert("1.0", game_data.d_cookie['bos_selected'])

        self.input_rss = tk.Text(self.frame)
        self.input_rss.place(x=200, y=320, height=30, width=180)
        self.input_rss.insert("1.0", game_data.d_cookie['rss_selected'])

        self.input_blg = tk.Text(self.frame)
        self.input_blg.place(x=400, y=320, height=30, width=180)
        self.input_blg.insert("1.0", game_data.d_cookie['blg_selected'])

        self.label_input = tk.Label(text="Selection: (Boss)\t\t(RSS)\t\t(Buildings)", anchor='w')
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

        for i, value in enumerate(game_obj.bos_names):
            self.content_bos += f'{i:02}. {value}\n'

        for i, value in enumerate(game_obj.rss_names):
            self.content_rss += f'{i:02}. {value}\n'

        for i, value in enumerate(game_obj.blg_names):
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
        game_obj.scout_selection(game_data.d_cookie['bos_selected'].strip(), game_obj.bos_names)
        game_obj.scout_selection(game_data.d_cookie['rss_selected'].strip(), game_obj.rss_names)
        game_obj.scout_selection(game_data.d_cookie['blg_selected'].strip(), game_obj.blg_names)

        # update cookie list record to be saved to file later
        game_data.txt_file('w')
        game_data.set_variable()  # reset init variables
        self.root.destroy()


def add_delimiter(stored_val: str, add_data: str, delimiter: str) -> str:
    delimiter = delimiter if stored_val else ''
    return delimiter + add_data


class Settings:
    def __init__(self):
        self.max_tile_left: int = 0
        self.max_tile_down: int = 0
        self.start_x: int = 0
        self.start_y: int = 0
        self.scr_mode = ''
        self.scout_options: str = 'None'
        self.file_cookiepy: str = 'cookiepy.txt'
        self.file_cookie_ahk: str = 'cookieAC.txt'

        self.cookie_ahk = []
        self.d_cookie: dict = {}

        self.txt_file('r')  # Setup d_cookie

        self.d_cookie: dict = {
            'bos_selected': '',
            'rss_selected': '',
            'blg_selected': '',
            'scout_list': '',
            'scout_options': ''
        }
        self.txt_file('r')  # Setup d_cookie
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

    def txt_file(self, action: str = 'w', update_item: str = 'py_cookie'):
        save_str: str = ''
        file_name: str = self.file_cookiepy if update_item == 'py_cookie' else self.file_cookie_ahk

        with open(file_name, action) as text_file:
            if action == 'r':
                for item_line in text_file.read().split('|'):
                    if len(item_line.strip()) > 0:
                        key = regex(item_line, ':', '<<')
                        value = regex(item_line, ':', '>>')

                        if update_item == 'py_cookie':
                            self.d_cookie[key] = value
                        elif update_item == 'cookie_ahk':
                            self.cookie_ahk.append(item_line)

            if action == 'w':
                for key, value in game_data.d_cookie.items():
                    concat_str = f'{key.strip()}:{value.strip()}'
                    save_str += add_delimiter(save_str, concat_str, '|')

                text_file.write(save_str)


class ScreenNavigation:
    def __init__(self):
        self.x: int = game_data.start_x
        self.y: int = game_data.start_y

        if game_data.scr_mode.strip() == 'Landscape':
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


def add_delimiter(stored_val: str, add_data: str, delimiter: str):
    delimiter = delimiter if stored_val else ''
    return delimiter + add_data


def debug(label, var, sleep: float = 0, prompt: bool = False) -> None:
    print(f'{label} --> {var}')
    pyautogui.sleep(sleep)
    if prompt:
        pyautogui.prompt(var, label)


def exit_loop() -> None:  # Function to exit the loop
    global g_loop
    g_loop = False


def find_obj() -> None:
    global l_obj_found
    expired_time: float = 0

    # pyautogui.useImageNotFoundException()
    try:
        # debug("game_data.d_cookie['scout_list']",game_data.d_cookie['scout_list'],prompt=True)
        expired_time = time() + 1
        global IMG_PATH

        # debug('expired_time', expired_time)
        # debug('time()', time())
        # debug('game_obj.bos_names', game_obj.bos_names, prompt=True)
        # debug('game_data.d_cookie["scout_list"]', game_data.d_cookie['scout_list'], prompt=True)
        # while expired_time > time():

        for item in game_data.d_cookie['scout_list'].split(','):
            # debug('IMG_PATH + item', IMG_PATH + item, prompt=True)
            l_obj_found.append(list(pyautogui.locateAllOnScreen(IMG_PATH + item, confidence=0.9)))
            debug('l_obj_found', l_obj_found, prompt=True)

    except:
        print(repr(l_obj_found))
        l_obj_found = None
    else:
        pass

    if l_obj_found:
        for l_each_obj_coords in l_obj_found:
            print(f'l_obj_found list --> {l_obj_found}')
            # x, y = coord[0][0], coord[0][1]
            x, y = img_center_xy(l_each_obj_coords)
            print(f'x- {x}, y:{y}')
            pyautogui.moveTo(x, y)
            pyautogui.sleep(1)
            pyautogui.click()
            pyautogui.prompt('out of loop')
        l_obj_found.clear()


def img_center_xy(coords: list) -> list:
    x: int = coords[0]
    y: int = coords[1]
    w: int = coords[2]
    h: int = coords[3]

    return [x + w, y + h]


def goto_coords(x_val: int, y_val: int):  # Game Tile XY Coords not Screen
    x, y = 0, 0
    pairs = game_data.d_cookie['CS_goto_coords'].split('-')
    for i, pair in enumerate(pairs):
        x, y = pair.strip('()').split(',')
        x, y = int(x), int(y)
        process_cs(x, y, 0.5)
        pyautogui.sleep(.5)
        if i == 1:
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.typewrite(str(x_val))
            pyautogui.sleep(.5)
            pyautogui.press('enter')

        elif i == 2:
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.typewrite(str(y_val))
            pyautogui.sleep(.5)
            pyautogui.press('enter')

        # elif i == 3:
        #     pyautogui.sleep(3)


def regex(input_str: str, separator: str, grab: str = '<<') -> str:
    which_exp = fr'^[^{separator};]*' if grab == '<<' else fr'(?<=\{separator}).*$'
    return re.search(which_exp, input_str).group()


def pause():
    seconds: int = 10
    print(f'Pause button pressed. Pausing for {seconds} seconds...')
    pyautogui.sleep(seconds)
    print('Resuming...')


def process_cs(x: int, y: int, wait_time: float = 1) -> None:
    pyautogui.moveTo(x, y)
    pyautogui.sleep(wait_time)
    pyautogui.click()


def validate_found_obj() -> None:
    pass


def main() -> None:
    global l_obj_found
    global g_loop

    pyautogui.sleep(3)  # seconds
    keyboard.add_hotkey('f2', pause)
    keyboard.add_hotkey('q', exit_loop)  # Register the 'q' key to call the exit_loop function

    g_loop = True
    while g_loop:
        while nav.y < game_data.max_tile_down:
            while nav.x > game_data.max_tile_left:
                pyautogui.sleep(2)

                loop_time = time()
                pyautogui.screenshot(region=(nav.scan_area_x, nav.scan_area_y, nav.scan_area_w, nav.scan_area_h))
                print("FPS {}".format(1 / (time() - loop_time)))

                goto_coords(nav.x, nav.y)  # goto current screen
                find_obj()  # find all instances of the obj(s) on current screen
                validate_found_obj()  # scrub obj found
                nav.x -= nav.next_scr_left_x
                nav.y += nav.next_scr_left_y

    print('Application Exit.')


if __name__ == "__main__":
    game_obj = GameObj()
    game_data = Settings()
    scout_menu = Menu()
    scout_menu.root.mainloop()
    nav = ScreenNavigation()
    main()
    # city_obj = GameObj.create_img_file_obj('cty')   # In city objects
    # ui_obj = GameObj.create_img_file_obj('uii')     # user interface items
