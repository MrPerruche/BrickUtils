from data import *
from copy import deepcopy
from brci import FM, numpy_features_enabled
import update_menu
import render_menu
import os.path
import ctypes

# Welcome to hell
# Please go to bed before you hate me
# You got something better to do in life that look at this disaster, right ?

icon_path = os.path.join(cwd, 'resources', 'brick_utils.ico')

def set_console_icon(icon_path):
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    IMAGE_ICON = 1
    LR_LOADFROMFILE = 0x00000010
    icon = user32.LoadImageW(None, icon_path, IMAGE_ICON, 0, 0, LR_LOADFROMFILE)
    kernel32.SetConsoleTitleW("BrickUtils")

    WM_SETICON = 0x80
    ICON_SMALL = 0
    user32.SendMessageW(kernel32.GetConsoleWindow(), WM_SETICON, ICON_SMALL, icon)

    # Allow multiline inputs
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


set_console_icon(icon_path)


memory = deepcopy(init_memory)
memory['main'] = load_json('config.json')

safe_mode: bool = True


def main():

    # ignoring inspection since it's imported from data...
    # noinspection PyGlobalUndefined
    global menu, safe_mode

    arbitrary_code_run: bool = False

    try:
        force_settings_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'force_settings.txt')
        if os.path.exists(force_settings_path):
            arbitrary_code_run = True
            with open(force_settings_path, 'r') as fsp_file:
                code = fsp_file.read()
            exec(code, globals())

    except Exception as e:
        input(f'{FM.red}An error occured when trying to load force_settings.txt:\n{type(e).__name__}: {e}{FM.reset}')

    if not numpy_features_enabled:

        render_menu.clear_terminal()

        print(render_menu.render_text('WARN', 'NumPy is not installed. Some features will be disabled!', True, FM.yellow))
        print(render_menu.render_text('', 'How to install numpy:', False, FM.yellow))
        print(render_menu.render_text('', '1. Open Windows powershell', False, FM.yellow))
        print(render_menu.render_text('', '2. Input and run the following command: py -3.12 -m pip install numpy', False, FM.yellow))
        print(render_menu.render_text('', '3. Installation is done. You may restart BrickUtils', False, FM.yellow))
        print(render_menu.render_text('ANY', 'Continue without NumPy', False, FM.yellow))
        input('> ')

    while True:

        if safe_mode:
            try:
                # Print menu
                render_menu.render_menu(menu, memory, safe_mode, arbitrary_code_run)
                # Get user input
                prompt = input('> ')
                # Update menu
                menu = update_menu.update_menu(prompt, menu, memory)
            except Exception as e:
                memory['fatal_error']['text'] = f'You may dismiss this message; or restart BrickUtils.\n{type(e).__name__}: {e}'
                memory['fatal_error']['return_path'] = 'main'
                menu = 'fatal_error'
                continue
        else:
            render_menu.render_menu(menu, memory, safe_mode, arbitrary_code_run)
            # Get user input
            prompt = input('> ')
            # Update menu
            menu = update_menu.update_menu(prompt, menu, memory)


if __name__ == '__main__':

    main()
