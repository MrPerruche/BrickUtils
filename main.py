from data import *
from copy import deepcopy
from brci import FM
import update_menu
import render_menu
import os.path
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleTitleW("BrickUtils")


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
