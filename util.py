import re

import pyautogui as pag

g_loop: bool = False


def add_delimiter(stored_val: str, add_data: str, delimiter: str):
    delimiter = delimiter if stored_val else ''
    return delimiter + add_data


def exit_loop() -> None:  # Function to exit the loop
    global g_loop
    g_loop = False


def debug(label, *var: any, sleep: float = 0, prompt: bool = False) -> None:
    output: str = f'{label} --> {var}'
    print(output)
    pag.sleep(sleep)
    if prompt:
        pag.prompt(output, label)


def pause():
    seconds: int = 10
    print(f'Pause button pressed. Pausing for {seconds} seconds...')
    pag.sleep(seconds)
    print('Resuming...')


def regex(input_str: str, separator: str, grab: str = '<') -> str:
    which_exp = fr'^[^{separator};]*' if grab == '<' else fr'(?<=\{separator}).*$'
    return re.search(which_exp, input_str).group()


def replace_text(text: str, seconds: float = 0.5):
    pag.hotkey('ctrl', 'a')
    pag.typewrite(text)  # paste text
    pag.sleep(seconds)
    pag.press('enter')
