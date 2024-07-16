from data import *
from copy import deepcopy
from brci import FM
import update_menu
import render_menu


memory = deepcopy(init_memory)
memory['main'] = load_json('config.json')


def main():

    # ignoring inspection since it's imported from data...
    # noinspection PyGlobalUndefined
    global menu

    safe_mode: bool = False

    while True:

        if safe_mode:
            try:
                # Print menu
                render_menu.render_menu(menu, memory)
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
            render_menu.render_menu(menu, memory)
            # Get user input
            prompt = input('> ')
            # Update menu
            menu = update_menu.update_menu(prompt, menu, memory)


if __name__ == '__main__':

    main()
