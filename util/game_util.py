import re

import easyocr
import numpy as np
import pyautogui as pag

import util
from AutoChop import GameData

g_loop: bool = False


def coords_logged(x: int, y: int, old_value_x: int, old_value_y: int) -> bool:
    pixel_padding: int = 10
    logged_status: bool = False

    beg_x: int = old_value_x - pixel_padding
    end_x: int = old_value_x + pixel_padding
    beg_y: int = old_value_y - pixel_padding
    end_y: int = old_value_y + pixel_padding

    if x in range(beg_x, end_x) and y in range(beg_y, end_y):
        logged_status = True

    return logged_status


def goto_coords(x_val: int, y_val: int, game_data: GameData = GameData):  # game_data instance of Settings class

    for i, pair in enumerate(game_data.d_cookie['cs_goto_xy'].split(';')):
        x, y = pair.split(',')
        # util.debug('x y ', x, y, prompt=True)
        pag.click(int(x), int(y), 1, 0.3, 'left')
        if i == 1:
            util.replace_text(str(x_val))
        elif i == 2:
            util.replace_text(str(y_val))


def move_to_click(x: int, y: int, wait_time: float = 1) -> None:
    pag.moveTo(x, y)
    pag.sleep(wait_time)
    pag.click()


def ocr(region: str) -> str:

    x, y, w, h = [int(value) for value in region.split(',')]
    screenshot = pag.screenshot(region=(x, y, w, h))  # Take a screenshot and convert it to a NumPy array
    screenshot.save("screenshot.png")
    # util.debug('break after screenshot', 'after SS', prompt=True)
    screenshot_np = np.array(screenshot)  # screenshot.save('screenshot.png')
    reader = easyocr.Reader(['en'])  # Initialize the EasyOCR reader object

    ocr_text:str = ''.join(reader.readtext(screenshot_np, detail=0))
    util.debug('OCR Text', ocr_text)  # The text detected in the image
    return ocr_text


def scrub_data(str_val: str, source: str = 'ocr', return_val: str = 'a_list') -> any:
    l_coords: list = []
    str_value: str = ''

    if source == 'ocr':
        l_coords = re.findall(r'\d+', str_val)

        if return_val == 'a_str':
            for value in l_coords:
                str_value += util.add_delimiter(return_val, value, ',')
            return str_value
    else:
        for pair in str_val.split(';'):
            if len(pair):
                x, y = pair.split(',')
                l_coords.append([int(x), int(y)])

    return l_coords


def validate_found_obj() -> None:
    pass
