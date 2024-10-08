import os
from brci import BrickInput, numpy_features_enabled, FM
from copy import deepcopy
from data import (react_dict, char_blacklist, clen, init_memory, i_int, i_float, cwd, save_json, load_json,
                  multi_replace, convert_length, password_protected_brv, return_password, set_clipboard,
                  is_valid_folder_name)
import colorsys
import scripts
import math
import subprocess


# This is where the full begins. Or your nightmares, should I say. Good luck figuring out what is what, it's a mess, and
# I'd rather die than comment it.
# I wouldn't be surprised if there's more empty lines than "legitimate" ones.
# Haha, rest assured, there's plenty of comments here explaining even the least details, and how it works in depth.
# No, I'm kidding. Good luck.


def count_strings_in_list(input_string: str, string_list: list[str] | list[tuple[str, float]]):

    input_string_ = input_string
    pos_count = 0.0
    neg_count = 0.0

    multiplier = 1

    for i, _ in enumerate(input_string_):
        for string, coefficient in string_list:
            string_ = string
            is_mult = False
            if string_[0] == '*':
                string_ = string_[1:]
                is_mult = True
            if input_string[i:].startswith(string_):
                if is_mult: multiplier *= coefficient
                else:
                    count = coefficient * multiplier
                    if count < 0:
                        neg_count -= count
                    else:
                        pos_count += count
                    multiplier = 1

    return pos_count, neg_count



def update_menu(prompt: str, menu: str, memory: dict[str, any]):

    new_menu = menu

    unit = memory['main']['system']

    if menu == 'invalid':

        new_menu = memory['invalid']['return_path']

    elif menu == 'fatal_error':

        if prompt.lower() in ['y', 'yes']:
            memory.clear()
            memory.update(init_memory)
            new_menu = 'main'
            return new_menu
        elif prompt.lower() in ['n', 'no']:
            new_menu = 'main'
            return new_menu
        else:
            memory['invalid']['return_path'] = 'fatal_error'
            memory['invalid']['text'] = f"Please type 'y' or 'n'. Sentences are not accepted here to avoid any additional errors."
            new_menu = 'invalid'

    if menu == 'success':

        new_menu = memory['success']['return_path']

    elif menu == 'main':

        if prompt == '0':

            exit(0)

        elif prompt == '1':

            new_menu = 'main/brick'

        elif prompt == '2':

            memory['invalid']['return_path'] = 'main'
            memory['invalid']['text'] = 'Hollow arc generator is not implemented yet.'
            new_menu = 'invalid'
            # new_menu = 'main/arc'

        elif prompt == '3':

            new_menu = 'main/pixelart'

        elif prompt == '4':

            # new_menu = 'main/lightbar'

            memory['invalid']['text'] = ('Lightbar generator is cancelled.\n'
                                         'If you wish to continue (and waste your time):\n'
                                         '1. Run debug_tools.py\n'
                                         '2. Input 4, press enter and quit.\n'
                                         '3. Restart BrickUtils\n'
                                         '4. Input the following code in the new window:\n'
                                         f'   {FM.reset}menu = {FM.light_green}\'main/lightbar\'{FM.light_red}\n'
                                         '5. Click Inject Code then go back to BrickUtils\n'
                                         '6. Input gibberish and you will open in the lightbar generator.')
            memory['invalid']['return_path'] = 'main'
            new_menu = 'invalid'

        elif prompt == '5':

            new_menu = 'main/edit'
            # memory['invalid']['return_path'] = 'main'
            # memory['invalid']['text'] = 'Creation editor is not functional yet.'
            # new_menu = 'invalid'

        elif prompt == '6':

            # new_menu = 'main/rotate'

            memory['invalid']['text'] = 'Rotation rounder is not implemented yet.'
            memory['invalid']['return_path'] = 'main'
            new_menu = 'invalid'

        elif prompt == '7':

            new_menu = 'main/encrypt'

        elif prompt == '8':

            memory['main/settings']['new_main'] = deepcopy(memory['main'])
            new_menu = 'main/settings'

        elif prompt == '9':

            new_menu = 'main/help'

        """
        elif prompt == '6':

            if memory['main']['port'] == [True, True]:
                memory['main']['port'] = [True, False]
            elif memory['main']['port'] == [True, False]:
                memory['main']['port'] = [False, True]
            elif memory['main']['port'] == [False, True]:
                memory['main']['port'] = [False, False]
            else: # if memory['main']['port'] == [False, False]:
                memory['main']['port'] = [True, True]

        elif prompt == '7':

            if memory['main']['system'] == 'cgs':
                memory['main']['system'] = 'si'
            elif memory['main']['system'] == 'si':
                memory['main']['system'] = 'imperial'
            elif memory['main']['system'] == 'imperial':
                memory['main']['system'] = 'scal'
            else: # if memory['main']['system'] == 'scal':
                memory['main']['system'] = 'cgs'
        """

    elif menu == 'main/arc':

        if prompt == '0':

            new_menu = 'main'


    elif menu == 'main/pixelart':

        try:
            int_prompt = i_int(prompt)
        except ValueError:
            return menu

        # Go back to the main menu
        if int_prompt == 0:
            new_menu = 'main'
            return new_menu
        int_prompt -= 1

        # Set project
        if int_prompt == 0:
            new_menu = 'main/pixelart/project'
            return new_menu
        int_prompt -= 1

        # Set image
        if int_prompt == 0:
            new_menu = 'main/pixelart/image'
            return new_menu
        int_prompt -= 1

        # Set import mode
        if int_prompt == 0:
            memory['invalid']['return_path'] = 'main/pixelart'
            memory['invalid']['text'] = 'No other import mode has been added yet.'
            new_menu = 'invalid'
        int_prompt -= 1

        # If import mode is scalable_rle
        if memory['main/pixelart']['import_mode'] == 'scalable_rle':

            # Change ig resolution calculation mode
            if int_prompt == 0:
                if memory['main/pixelart']['ig_calc'] == 'auto_x':
                    memory['main/pixelart']['ig_calc'] = 'auto_y'
                elif memory['main/pixelart']['ig_calc'] == 'auto_y':
                    memory['main/pixelart']['ig_calc'] = 'no_auto'
                else: # if memory['main/pixelart']['ig_calc'] == 'no_auto':
                    memory['main/pixelart']['ig_calc'] = 'auto_x'
                new_menu = 'main/pixelart'
            int_prompt -= 1

            # Set resolution x
            if int_prompt == 0:
                if not memory['main/pixelart']['ig_calc'] == 'auto_x':
                    new_menu = 'main/pixelart/ig_res_x'
                    return new_menu
                else:
                    memory['invalid']['return_path'] = 'main/pixelart'
                    memory['invalid']['text'] = 'It is configured to automatically calculate the in-game resolution x.'
                    new_menu = 'invalid'
            int_prompt -= 1

            # Set resolution y
            if int_prompt == 0:
                if not memory['main/pixelart']['ig_calc'] == 'auto_y':
                    new_menu = 'main/pixelart/ig_res_y'
                    return new_menu
                else:
                    memory['invalid']['return_path'] = 'main/pixelart'
                    memory['invalid']['text'] = 'It is configured to automatically calculate the in-game resolution y.'
                    new_menu = 'invalid'
            int_prompt -= 1

            # Set number of colors
            if int_prompt == 0:
                new_menu = 'main/pixelart/colors'
                return new_menu
            int_prompt -= 1

            # Select color
            if int_prompt == 0:
                if memory['main/pixelart']['color_method'] == 'common':
                    memory['main/pixelart']['color_method'] = 'random_list'
                elif memory['main/pixelart']['color_method'] == 'random_list':
                    memory['main/pixelart']['color_method'] = 'random_set'
                else: # if memory['main/pixelart']['color_method'] == 'random_set':
                    memory['main/pixelart']['color_method'] = 'common'
            int_prompt -= 1

            # Set connections
            if int_prompt == 0:
                new_menu = 'main/pixelart/connections'
                memory['main/pixelart/connections']['edited'] = 'sides'
                memory['main/pixelart/connections']['new'] = {'sides': True, 'front': True, 'back': True}.copy()
                return new_menu
            int_prompt -= 1

            # Set scale mode
            if int_prompt == 0:
                if memory['main/pixelart']['scale_mode'] == 'pixel':
                    memory['main/pixelart']['scale_mode'] = 'image'
                elif memory['main/pixelart']['scale_mode'] == 'image':
                    memory['main/pixelart']['scale_mode'] = 'reference'
                else: # if memory['main/pixelart']['scale_mode'] == 'reference':
                    memory['main/pixelart']['scale_mode'] = 'pixel'
            int_prompt -= 1

            # If scaling mode is pixel
            if memory['main/pixelart']['scale_mode'] == 'pixel':
                # Set scale x
                if int_prompt == 0:
                    new_menu = 'main/pixelart/px_scale_x'
                    return new_menu
                int_prompt -= 1

                # Set scale y
                if int_prompt == 0:
                    new_menu = 'main/pixelart/px_scale_y'
                    return new_menu
                int_prompt -= 1

            elif memory['main/pixelart']['scale_mode'] == 'image':
                # Set auto calc mode
                if int_prompt == 0:
                    if memory['main/pixelart']['img_scale_calc'] == 'auto_x':
                        memory['main/pixelart']['img_scale_calc'] = 'auto_y'
                    elif memory['main/pixelart']['img_scale_calc'] == 'auto_y':
                        memory['main/pixelart']['img_scale_calc'] = 'no_auto'
                    else: # if memory['main/pixelart']['img_scale_calc'] == 'no_auto':
                        memory['main/pixelart']['img_scale_calc'] = 'auto_x'
                    new_menu = 'main/pixelart'
                int_prompt -= 1

                # Set scale x
                if int_prompt == 0:
                    if not memory['main/pixelart']['img_scale_calc'] == 'auto_x':
                        new_menu = 'main/pixelart/img_scale_x'
                        return new_menu
                    else:
                        memory['invalid']['return_path'] = 'main/pixelart'
                        memory['invalid']['text'] = 'It is configured to automatically calculate the image scale x.'
                        new_menu = 'invalid'
                int_prompt -= 1

                # Set scale y
                if int_prompt == 0:
                    if not memory['main/pixelart']['img_scale_calc'] == 'auto_y':
                        new_menu = 'main/pixelart/img_scale_y'
                        return new_menu
                    else:
                        memory['invalid']['return_path'] = 'main/pixelart'
                        memory['invalid']['text'] = 'It is configured to automatically calculate the image scale y.'
                        new_menu = 'invalid'
                int_prompt -= 1

            elif memory['main/pixelart']['scale_mode'] == 'reference':
                # Set scale pixels
                if int_prompt == 0:
                    new_menu = 'main/pixelart/ref_scale_px'
                    return new_menu
                int_prompt -= 1

                # Set scale image
                if int_prompt == 0:
                    new_menu = 'main/pixelart/ref_scale_img'
                    return new_menu
                int_prompt -= 1

            # Set pixel thickness
            if int_prompt == 0:
                new_menu = 'main/pixelart/thickness'
                return new_menu
            int_prompt -= 1

            if int_prompt == 0:
                new_menu = 'main/pixelart/red_cor'
                return new_menu
            int_prompt -= 1

            if int_prompt == 0:
                new_menu = 'main/pixelart/green_cor'
                return new_menu
            int_prompt -= 1

            if int_prompt == 0:
                new_menu = 'main/pixelart/blue_cor'
                return new_menu
            int_prompt -= 1

            if int_prompt == 0:
                new_menu = 'main/pixelart/alpha_cor'
                return new_menu
            int_prompt -= 1

            if int_prompt == 0:
                if memory['main/pixelart']['alpha_handling'] == 'ignore':
                    memory['main/pixelart']['alpha_handling'] = 'do_not_duplicate'
                elif memory['main/pixelart']['alpha_handling'] == 'do_not_duplicate':
                    memory['main/pixelart']['alpha_handling'] = 'do_not_duplicate_delete'
                elif memory['main/pixelart']['alpha_handling'] == 'do_not_duplicate_delete':
                    memory['main/pixelart']['alpha_handling'] = 'yes'
                else: # if memory['main/pixelart']['alpha_handling'] == 'yes':
                    memory['main/pixelart']['alpha_handling'] = 'ignore'
                new_menu = 'main/pixelart'
            int_prompt -= 1

            if int_prompt == 0:
                if memory['main/pixelart']['thumbnail'] == 'image':
                    memory['main/pixelart']['thumbnail'] = 'brci'
                else: # if memory['main/pixelart']['thumbnail'] == 'brci':
                    memory['main/pixelart']['thumbnail'] = 'image'
            int_prompt -= 1

            if int_prompt == 0:

                if not is_valid_folder_name(memory['main/pixelart']['project']):
                    memory['invalid']['text'] = 'This project name is invalid (likely unfilled).'
                    memory['invalid']['return_path'] = 'main/pixelart'
                    new_menu = 'invalid'
                    return new_menu
                if memory['main/pixelart']['image'] in {'', ' '}:
                    memory['invalid']['text'] = 'Please fill image field.'
                    memory['invalid']['return_path'] = 'main/pixelart'
                    new_menu = 'invalid'
                    return new_menu

                # noinspection PyUnusedLocal
                success, return_data = False, 0
                """
                success, return_data = scripts.pixelart.scalable_rle(memory['main/pixelart'], memory['main']['port'][0], memory['main']['backup'], memory['main']['backup_limit'])
                memory['success']['return_path'] = 'main/pixelart'
                memory['success']['text'] = f'Successfully generated \'{memory['main/pixelart']['image']}\' {return_data}'
                new_menu = 'success'
                """
                try:
                    success, return_data = scripts.pixelart.scalable_rle(memory['main/pixelart'], memory['main']['port'][0], memory['main']['backup'], memory['main']['backup_limit'])
                except Exception as e:
                    memory['invalid']['return_path'] = 'main/pixelart'
                    memory['invalid']['text'] = f'Failed to generate image (An unexpected error occured!).\n{type(e).__name__}: {e}'
                    new_menu = 'invalid'
                    return new_menu
                if success:
                    memory['success']['return_path'] = 'main/pixelart'
                    memory['success']['text'] = f'Successfully generated \'{memory['main/pixelart']['image']}\' {return_data}'
                    new_menu = 'success'
                else:
                    memory['invalid']['return_path'] = 'main/pixelart'
                    memory['invalid']['text'] = f'Failed to generate image: {return_data}.'
                    new_menu = 'invalid'
            int_prompt -= 1

            if int_prompt == 0:
                memory['main/pixelart'] = deepcopy(init_memory['main/pixelart'])
            int_prompt -= 1


    elif menu == 'main/pixelart/project':

        memory['main/pixelart']['project'] = prompt
        new_menu = 'main/pixelart'

    elif menu == 'main/pixelart/image':

        memory['main/pixelart']['image'] = prompt
        new_menu = 'main/pixelart'

    elif menu == 'main/pixelart/ig_res_x':

        try:
            prompt_int = i_int(prompt)
            if prompt_int < 1:
                raise ValueError
            memory['main/pixelart']['ig_res_x'] = prompt_int
            new_menu = 'main/pixelart'
        except ValueError:
            memory['invalid']['return_path'] = 'main/pixelart'
            memory['invalid']['text'] = 'The resolution x must be an integer greater than 0.'
            new_menu = 'invalid'

    elif menu == 'main/pixelart/ig_res_y':

        try:
            prompt_int = i_int(prompt)
            if prompt_int < 1:
                raise ValueError
            memory['main/pixelart']['ig_res_y'] = prompt_int
            new_menu = 'main/pixelart'
        except ValueError:
            memory['invalid']['return_path'] = 'main/pixelart'
            memory['invalid']['text'] = 'The resolution y must be an integer greater than 0.'
            new_menu = 'invalid'

    elif menu == 'main/pixelart/colors':

        try:
            prompt_int = i_int(prompt)
            if prompt_int < 1:
                raise ValueError
            if prompt_int > 256:
                raise ValueError
            memory['main/pixelart']['colors'] = prompt_int
            new_menu = 'main/pixelart'
        except ValueError:
            memory['invalid']['return_path'] = 'main/pixelart'
            memory['invalid']['text'] = 'The number of colors must be an integer greater than 0 and less than or equal to 256.'
            new_menu = 'invalid'

    elif menu == 'main/pixelart/connections':

        if prompt == '0':
            new_menu = 'main/pixelart'
            return new_menu

        # else:
        edited = memory['main/pixelart/connections']['edited']
        if not memory['main/pixelart/connections']['edited'] == 'confirm':
            # get input
            modified_input = multi_replace(prompt.lower(), char_blacklist, '')
            user_pos, user_neg = count_strings_in_list(modified_input, [(key, item) for key, item in react_dict.items() if key != 'y'][::-1])
            # interpret output
            if prompt == 'y': user_pos = 10.0
            elif prompt == 'n': user_neg = 10.0
            if user_pos - user_neg != 0:
                memory['main/pixelart/connections']['new'][edited] = user_pos - user_neg > 0
                memory['main/pixelart/connections']['scores'][edited] = [round(user_pos, 4), round(user_neg, 4)]
            elif user_pos == user_neg and user_pos != 0:
                memory['invalid']['return_path'] = 'main/pixelart/connections'
                memory['invalid']['text'] = 'Brickutils is unsure if you meant yes or no.'
                new_menu = 'invalid'
                return new_menu
            else:  # if user_pos == user_neg == 0
                memory['invalid']['return_path'] = 'main/pixelart/connections'
                memory['invalid']['text'] = 'Input misunderstood. Try yes / no.'
                new_menu = 'invalid'
                return new_menu

        if edited == 'sides':
            memory['main/pixelart/connections']['edited'] = 'front'
        elif edited == 'front':
            memory['main/pixelart/connections']['edited'] = 'back'
        elif edited == 'back':
            memory['main/pixelart/connections']['edited'] = 'confirm'
        elif edited == 'confirm':
            # get input
            modified_input = multi_replace(prompt.lower(), char_blacklist, '')
            user_pos, user_neg = count_strings_in_list(modified_input, [(key, item) for key, item in react_dict.items() if key != 'y'][::-1])
            # interpret output
            if prompt == 'y': user_pos = 10.0
            elif prompt == 'n': user_neg = 10.0
            # If favorable
            if user_pos > user_neg:
                memory['main/pixelart']['connections'] = deepcopy(memory['main/pixelart/connections']['new'])
                new_menu = 'main/pixelart'
            elif user_pos < user_neg:
                memory['main/pixelart/connections']['edited'] = 'sides'
                memory['main/pixelart/connections']['new'] = {'sides': True, 'front': True, 'back': True}.copy()
            elif user_pos == user_neg and user_pos != 0:
                memory['invalid']['return_path'] = 'main/pixelart/connections'
                memory['invalid']['text'] = 'Brickutils is unsure if you meant yes or no.'
                new_menu = 'invalid'
                return new_menu
            else: # if user_pos == user_neg == 0
                memory['invalid']['return_path'] = 'main/pixelart/connections'
                memory['invalid']['text'] = 'Input misunderstood. Try yes / no.'
                new_menu = 'invalid'
                return new_menu

    elif menu == 'main/pixelart/px_scale_x':

        try:
            memory['main/pixelart']['px_scale_x'] = clen(prompt, unit)
            new_menu = 'main/pixelart'
        except ValueError:
            memory['invalid']['return_path'] = 'main/pixelart'
            memory['invalid']['text'] = "Pixel scale must be a number."
            new_menu = 'invalid'

    elif menu == 'main/pixelart/px_scale_y':

        try:
            memory['main/pixelart']['px_scale_y'] = clen(prompt, unit)
            new_menu = 'main/pixelart'
        except ValueError:
            memory['invalid']['return_path'] = 'main/pixelart'
            memory['invalid']['text'] = "Pixel scale must be a number."
            new_menu = 'invalid'

    elif menu == 'main/pixelart/img_scale_x':

        try:
            memory['main/pixelart']['img_scale_x'] = clen(prompt, unit)
            new_menu = 'main/pixelart'
        except ValueError:
            memory['invalid']['return_path'] = 'main/pixelart'
            memory['invalid']['text'] = "Image scale must be a number."
            new_menu = 'invalid'

    elif menu == 'main/pixelart/img_scale_y':

        try:
            memory['main/pixelart']['img_scale_y'] = clen(prompt, unit)
            new_menu = 'main/pixelart'
        except ValueError:
            memory['invalid']['return_path'] = 'main/pixelart'
            memory['invalid']['text'] = "Image scale must be a number."
            new_menu = 'invalid'

    elif menu == 'main/pixelart/ref_scale_px':

        try:
            memory['main/pixelart']['ref_scale_px'] = i_float(prompt)
            new_menu = 'main/pixelart'
        except ValueError:
            memory['invalid']['return_path'] = 'main/pixelart'
            memory['invalid']['text'] = "Reference scale must be a number."
            new_menu = 'invalid'

    elif menu == 'main/pixelart/ref_scale_img':

        try:
            memory['main/pixelart']['ref_scale_img'] = clen(prompt, unit)
            new_menu = 'main/pixelart'
        except ValueError:
            memory['invalid']['return_path'] = 'main/pixelart'
            memory['invalid']['text'] = "Reference scale must be a number."
            new_menu = 'invalid'

    elif menu == 'main/pixelart/thickness':

        try:
            memory['main/pixelart']['thickness'] = clen(prompt, unit)
            new_menu = 'main/pixelart'
        except ValueError:
            memory['invalid']['return_path'] = 'main/pixelart'
            memory['invalid']['text'] = "Thickness must be a number."
            new_menu = 'invalid'

    elif menu == 'main/pixelart/red_cor':

        try:
            for i in range(101): # 0, 1, ..., 99, 100
                i_ = i / 100
                r = eval(prompt, globals(), {'r': i_, 'g': i_, 'b': i_, 'a': i_, 'math': math})
                if (not isinstance(r, float)) or r < 0 or r > 1:
                    memory['invalid']['return_path'] = 'main/pixelart'
                    memory['invalid']['text'] = f"Output must be a number ranging between 0.0 and 1.0. r was {r} for r = g = b = a = {i_}\nFunction: {prompt}"
                    new_menu = 'invalid'
                    return new_menu

            memory['main/pixelart']['red_cor'] = prompt
            new_menu = 'main/pixelart'
        except Exception as e:
            memory['invalid']['return_path'] = 'main/pixelart'
            memory['invalid']['text'] = f"Provided function causes an error.\nFunction: {prompt}\n{type(e).__name__}: {e}"
            new_menu = 'invalid'

    elif menu == 'main/pixelart/green_cor':

        try:
            for i in range(101): # 0, 1, ..., 99, 100
                i_ = i / 100
                g = eval(prompt, globals(), {'r': i_, 'g': i_, 'b': i_, 'a': i_, 'math': math})
                if (not isinstance(g, float)) or g < 0 or g > 1:
                    memory['invalid']['return_path'] = 'main/pixelart'
                    memory['invalid']['text'] = f"Output must be a number ranging between 0.0 and 1.0. g was {g} for r = g = b = a = {i_}\nFunction: {prompt}"
                    new_menu = 'invalid'
                    return new_menu

            memory['main/pixelart']['green_cor'] = prompt
            new_menu = 'main/pixelart'
        except Exception as e:
            memory['invalid']['return_path'] = 'main/pixelart'
            memory['invalid']['text'] = f"Provided function causes an error.\nFunction: {prompt}\n{type(e).__name__}: {e}"
            new_menu = 'invalid'

    elif menu == 'main/pixelart/blue_cor':

        try:
            for i in range(101): # 0, 1, ..., 99, 100
                i_ = i / 100
                b = eval(prompt, globals(), {'r': i_, 'g': i_, 'b': i_, 'a': i_, 'math': math})
                if (not isinstance(b, float)) or b < 0 or b > 1:
                    memory['invalid']['return_path'] = 'main/pixelart'
                    memory['invalid']['text'] = f"Output must be a number ranging between 0.0 and 1.0. b was {b} for r = g = b = a = {i_}\nFunction: {prompt}"
                    new_menu = 'invalid'
                    return new_menu

            memory['main/pixelart']['blue_cor'] = prompt
            new_menu = 'main/pixelart'
        except Exception as e:
            memory['invalid']['return_path'] = 'main/pixelart'
            memory['invalid']['text'] = f"Provided function causes an error.\nFunction: {prompt}\n{type(e).__name__}: {e}"
            new_menu = 'invalid'

    elif menu == 'main/pixelart/alpha_cor':

        try:
            for i in range(101): # 0, 1, ..., 99, 100
                i_ = i / 100
                a = eval(prompt, globals(), {'r': i_, 'g': i_, 'b': i_, 'a': i_, 'math': math})
                if (not isinstance(a, float)) or a < 0 or a > 1:
                    memory['invalid']['return_path'] = 'main/pixelart'
                    memory['invalid']['text'] = f"Output must be a number ranging between 0.0 and 1.0. a was {a} for r = g = b = a = {i_}\nFunction: {prompt}"
                    new_menu = 'invalid'
                    return new_menu

            memory['main/pixelart']['alpha_cor'] = prompt
            new_menu = 'main/pixelart'
        except Exception as e:
            memory['invalid']['return_path'] = 'main/pixelart'
            memory['invalid']['text'] = f"Provided function causes an error.\nFunction: {prompt}\n{type(e).__name__}: {e}"
            new_menu = 'invalid'

    elif menu == 'main/settings':

        if prompt == '0':
            new_menu = 'main'

        elif prompt == '1':

            if memory['main/settings']['new_main']['port'] == [True, True]:
                memory['main/settings']['new_main']['port'] = [True, False]
            elif memory['main/settings']['new_main']['port'] == [True, False]:
                memory['main/settings']['new_main']['port'] = [False, True]
            elif memory['main/settings']['new_main']['port'] == [False, True]:
                memory['main/settings']['new_main']['port'] = [False, False]
            else:  # if memory['main/settings']['new_main']['port'] == [False, False]:
                memory['main/settings']['new_main']['port'] = [True, True]

        elif prompt == '2':

            if memory['main/settings']['new_main']['backup'] == [True, True]:
                memory['main/settings']['new_main']['backup'] = [True, False]
            elif memory['main/settings']['new_main']['backup'] == [True, False]:
                memory['main/settings']['new_main']['backup'] = [False, True]
            elif memory['main/settings']['new_main']['backup'] == [False, True]:
                memory['main/settings']['new_main']['backup'] = [False, False]
            else:  # if memory['main/settings']['new_main']['backup'] == [False, False]:
                memory['main/settings']['new_main']['backup'] = [True, True]

        elif prompt == '3' and memory['main/settings']['new_main']['backup'] != [False, False]:

            new_menu = 'main/settings/backup_limit'

        elif prompt == '4':

            # Open backup/projects in explorer
            backup_path = os.path.join(cwd, 'backup')
            appdata_local_path = os.getenv('LOCALAPPDATA')
            brickrigs_path = os.path.join(appdata_local_path, 'BrickRigs', 'SavedRemastered', 'Vehicles')

            os.startfile(backup_path)
            os.startfile(brickrigs_path)

        elif prompt == '5':

            if memory['main/settings']['new_main']['system'] == 'cgs':
                memory['main/settings']['new_main']['system'] = 'si'
            elif memory['main/settings']['new_main']['system'] == 'si':
                memory['main/settings']['new_main']['system'] = 'imperial'
            elif memory['main/settings']['new_main']['system'] == 'imperial':
                memory['main/settings']['new_main']['system'] = 'scal'
            else:  # if memory['main']['system'] == 'scal':
                memory['main/settings']['new_main']['system'] = 'cgs'

        elif prompt == '6':

            new_menu = 'main'

        elif prompt == '7':

            memory['main'] = deepcopy(memory['main/settings']['new_main'])
            new_menu = 'main'

        elif prompt == '8':

            memory['main'] = deepcopy(memory['main/settings']['new_main'])
            save_json('config.json', memory['main'])
            new_menu = 'main'


        elif prompt == '9':

            # Taken from debug_tools.py

            sr_source = os.path.join(cwd, 'resources', 'default_config')  # has no extension
            # sr_new_path = os.path.join(cwd, 'config.json')

            memory['main/settings']['new_main'] = load_json(sr_source)


    elif menu == 'main/settings/backup_limit':

        if prompt == '0':
            new_menu = 'main/settings'
            return new_menu

        # else:

        try:
            backup_limit = i_int(prompt)
            if backup_limit <= 0:
                memory['invalid']['return_path'] = 'main/settings'
                memory['invalid']['text'] = f"Backup limit must be a number greater than 0."
                new_menu = 'invalid'
            else:
                memory['main/settings']['new_main']['backup_limit'] = backup_limit
                new_menu = 'main/settings'
        except ValueError:
            memory['invalid']['return_path'] = 'main/settings'
            memory['invalid']['text'] = f"Backup limit must be a number greater than or equal to 0."
            new_menu = 'invalid'

    elif menu == 'main/brick':

        if prompt == '0':

            new_menu = 'main'

        elif prompt == '1':

            new_menu = 'main/brick/project'

        elif prompt == '2':

            new_menu = 'main/brick/select_brick'

        elif prompt == '3':

            new_menu = 'main/brick/properties'

        elif prompt == '4':

            if not is_valid_folder_name(memory['main/brick']['project']):
                memory['invalid']['text'] = 'This project name is invalid (likely unfilled).'
                memory['invalid']['return_path'] = 'main/brick'
                new_menu = 'invalid'
                return new_menu

            success, output_message = scripts.brick.generate(memory['main/brick'], memory['main']['port'][0], memory['main']['backup'], memory['main']['backup_limit'])

            if success:

                memory['success']['text'] = 'Successfully generated 1 brick.'
                memory['success']['return_path'] = 'main/brick'
                new_menu = 'success'

            else:

                memory['invalid']['text'] = f'An error occured: {output_message}'
                memory['success']['return_path'] = 'main/brick'
                new_menu = 'invalid'

    elif menu == 'main/brick/project':

        try:
            memory['main/brick']['project'] = prompt
            new_menu = 'main/brick'

        except ValueError:
            memory['invalid']['return_path'] = 'main/brick'
            memory['invalid']['text'] = f"Congrats! You somehow made project name invalid."

    elif menu == 'main/brick/select_brick':

        try:
            int_prompt = int(prompt)
        except ValueError:
            return new_menu

        if int_prompt == 0:
            new_menu = 'main/brick'
            return new_menu
        int_prompt -= 1

        if int_prompt == 0:
            new_menu = 'main/brick/select_brick/search'
            return new_menu
        int_prompt -= 1

        try:
            memory['main/brick']['brick'] = memory['main/brick/select_brick']['matches'][int_prompt]
            memory['main/brick']['properties'] = scripts.brick.get_brick_properties(memory['main/brick']['brick'])
            new_menu = 'main/brick'
        except IndexError:
            pass

        return new_menu

    elif menu == 'main/brick/select_brick/search':

        memory['main/brick/select_brick']['search'] = prompt

        if prompt == '0':
            new_menu = 'main/brick/select_brick'
            return new_menu

        elif prompt == 'all':
            matches = scripts.brick.return_matches([])

        else:
            matches = scripts.brick.return_matches(prompt.split(' '))

        if matches is not None:
            memory['main/brick/select_brick']['matches'] = matches

        new_menu = 'main/brick/select_brick'

    elif menu == 'main/brick/properties':

        try:
            int_prompt = int(prompt)
        except ValueError:
            return new_menu

        if int_prompt == 0:
            new_menu = 'main/brick'
            return new_menu
        int_prompt -= 1

        if int_prompt == 0:
            memory['main/brick/properties']['advanced'] = not memory['main/brick/properties']['advanced']
            return new_menu
        int_prompt -= 1

        try:
            properties = deepcopy(memory['main/brick']['properties'])

            if not memory['main/brick/properties']['advanced']:

                properties.pop('gbn')
                properties.pop('Position')
                properties.pop('Rotation')

            sel_prop = list(properties.keys())[int_prompt]


            if memory['main/brick/properties']['advanced']:  # Yes it's separate idk why

                memory['main/brick/properties/eval']['property'] = sel_prop
                new_menu = 'main/brick/properties/eval'
                return new_menu


            # advanced mode
            if sel_prop in ['IdlerWheels', 'OwningSeat']:
                memory['main/brick/properties/advanced_required']['property'] = sel_prop
                new_menu = 'main/brick/properties/advanced_required'
                return new_menu


            # bool
            if sel_prop in ['bAccumulated', 'bAccumulateInput', 'bCanDisableSteering', 'bCanInvertSteering', 'bDriven', 'bGenerateLift', 'bHasBrake', 'bHasHandBrake',
                            'bInvertDrive', 'bInvertTankSteering', 'bReturnToZero', 'bTankDrive']:
                memory['main/brick']['properties'][sel_prop] = not memory['main/brick']['properties'][sel_prop]


            # choice
            if sel_prop in ['ActuatorMode', 'AmmoType', 'BrickMaterial', 'BrickPattern', 'CouplingMode', 'FlashSequence', 'Font', 'FuelType', 'Image', 'LightDirection',
                            'Operation', 'SensorType', 'SirenType', 'TraceMask']:

                memory['main/brick/properties/choice']['property'] = sel_prop
                options = []
                if sel_prop in ['ActuatorMode']: options = ['Accumulated', 'Seeking', 'Cycle', 'PhysicsDriven', 'Spring', 'Static']
                elif sel_prop in ['AmmoType']: options = ['Standard', 'Incendiary', 'HighExplosive', 'TargetSeeking', 'Guided']
                elif sel_prop in ['BrickMaterial']: options = ['Aluminium', 'BrushedAlu', 'Carbon', 'ChannelledAlu', 'Chrome', 'CloudyGlass', 'Copper', 'Foam', 'Glass', 'Glow',
                                                               'Gold', 'LEDMatrix', 'Oak', 'Pine', 'Plastic', 'RoughWood', 'Rubber', 'RustedSteel', 'Steel', 'Tungsten']
                elif sel_prop in ['BrickPattern']: options = ['Default', 'C_Army', 'C_Army_Digital', 'C_Autumn', 'C_Berlin_2', 'C_Berlin', 'C_Berlin_Digital', 'C_Cristal_Contrast',
                                                              'C_Cristal_Red', 'C_Dark', 'C_Desert_2', 'C_Desert', 'C_Desert_Digital', 'C_Flecktarn', 'C_Heat', 'C_Navy', 'C_Sharp',
                                                              'C_Sky', 'C_Sweden', 'C_Swirl', 'C_Tiger', 'C_Urban', 'C_Yellow', 'P_Burnt', 'P_Fire', 'P_Hexagon', 'P_Swirl_Arabica',
                                                              'P_Warning', 'P_Warning_Red', 'P_YellowCircles']
                elif sel_prop in ['CouplingMode']: options = ['Default', 'Static']
                elif sel_prop in ['FlashSequence']: options = ['None', 'Blinker_Sequence', 'Blinker_Sequence_Inverted', 'DoubleFlash_Inverted_Sequence', 'DoubleFlash_Sequence',
                                                               'RunningLight_01_Inverted_Sequence', 'RunningLight_01_Sequence', 'RunningLight_02_Inverted_Sequence',
                                                               'RunningLight_02_Sequence', 'RunningLight_03_Inverted_Sequence', 'RunningLight_03_Sequence',
                                                               'RunningLight_04_Inverted_Sequence', 'RunningLight_04_Sequence', 'Strobe_Sequence']
                elif sel_prop in ['Font']: options = ['BigShouldersStencil', 'NotoEmoji', 'Orbitron', 'PermanentMarker', 'Roboto', 'RobotoSerif', 'Silkscreen']
                elif sel_prop in ['FuelType']: options = ['C4', 'Nitro', 'Petrol', 'RocketFuel']
                elif sel_prop in ['Image']: options = ['Arrow', 'Biohazard', 'BRAF', 'BrickRigs', 'BrickRigsArms', 'Caution', 'Criminals', 'Crosshair', 'DesertWorms', 'Dummy',
                                                       'ElectricHazard', 'ExplosiveHazard', 'FireDept', 'FireHazard', 'Gauge', 'Limit80', 'NoEntrance', 'OneWay', 'Phone', 'Police',
                                                       'Radioactive', 'Star', 'Stop', 'Tank', 'Virus']
                elif sel_prop in ['LightDirection']: options = ['Off', 'Omnidirectional', 'X', 'XNeg', 'Y', 'YNeg', 'Z', 'ZNeg']
                elif sel_prop in ['Operation']: options = ['Add', 'Subtract', 'Multiply', 'Divide', 'Fmod', 'Power', 'Greater', 'Less', 'Min', 'Max', 'Abs', 'Sign', 'Round',
                                                           'Ceil', 'Floor', 'Sqrt', 'SinDeg', 'Sin', 'AsinDeg', 'Asin', 'CosDeg', 'Cos', 'AcosDeg', 'Acos', 'TanDeg', 'Tan',
                                                           'AtanDeg', 'Atan']
                elif sel_prop in ['SensorType']: options = ['Speed', 'NormalSpeed', 'Acceleration', 'NormalAcceleration', 'AngularSpeed', 'NormalAngularSpeed', 'Distance', 'Time',
                                                            'Proximity', 'DistanceToGround', 'Altitude', 'Pitch', 'Yaw', 'Roll', 'NumSeekingProjectiles',
                                                            'SeekingProjectilesDistance']
                elif sel_prop in ['SirenType']: options = ['Car', 'EmsUS', 'FireDeptGerman', 'PoliceGerman', 'TruckHorn']
                elif sel_prop in ['TraceMask']: options = ['All', 'Static', 'Vehicles', 'OtherVehicles', 'Pawn', 'Water']
                memory['main/brick/properties/choice']['options'] = options
                new_menu = 'main/brick/properties/choice'


            # connector spacing
            if sel_prop in ['ConnectorSpacing']:

                memory['main/brick/properties/connector']['property'] = sel_prop
                new_menu = 'main/brick/properties/connector'


            # float
            if sel_prop in ['BrakeStrength', 'Brightness', 'FontSize', 'GearRatioScale', 'HornPitch', 'InputScale', 'LightConeAngle', 'MaxAngle', 'MaxLimit', 'MinAngle',
                            'MinLimit', 'OutlineThickness', 'OutputChannel.MinIn', 'OutputChannel.MinOut', 'OutputChannel.MaxIn', 'OutputChannel.MaxOut', 'SpawnScale',
                            'SpeedFactor', 'SteeringAngle', 'SteeringSpeed', 'SuspensionDamping', 'SuspensionStiffness', 'TirePressureRatio', 'WinchSpeed']:

                memory['main/brick/properties/float']['property'] = sel_prop
                memory['main/brick/properties/float']['distance'] = None
                new_menu = 'main/brick/properties/float'

            if sel_prop in ['SuspensionLength']:

                memory['main/brick/properties/float']['property'] = sel_prop
                memory['main/brick/properties/float']['distance'] = 'cgs'
                new_menu = 'main/brick/properties/float'

            if sel_prop in ['TireThickness', 'WheelDiameter', 'WheelWidth']:

                memory['main/brick/properties/float']['property'] = sel_prop
                memory['main/brick/properties/float']['distance'] = 'stud'
                new_menu = 'main/brick/properties/float'

            # list[3*float], not_color
            if sel_prop in ['BrickSize']:

                memory['main/brick/properties/list']['property'] = sel_prop
                memory['main/brick/properties/list']['type'] = 'float'
                memory['main/brick/properties/list']['len'] = [3]
                memory['main/brick/properties/list']['accepts_none'] = False
                memory['main/brick/properties/list']['distance'] = 'stud'
                new_menu = 'main/brick/properties/list'

            if sel_prop in ['ExitLocation']:

                memory['main/brick/properties/list']['property'] = sel_prop
                memory['main/brick/properties/list']['type'] = 'float'
                memory['main/brick/properties/list']['len'] = [3]
                memory['main/brick/properties/list']['accepts_none'] = True
                memory['main/brick/properties/list']['distance'] = 'cgs'
                new_menu = 'main/brick/properties/list'


            # list[4*uint8], is_color
            elif sel_prop in ['BrickColor', 'DisplayColor', 'ImageColor', 'SmokeColor', 'TextColor', 'TrackColor']:

                memory['main/brick/properties/color']['property'] = sel_prop
                memory['main/brick/properties/color']['mode'] = 'select_color_space'
                memory['main/brick/properties/color']['alpha'] = True
                if sel_prop in ['DisplayColor', 'ImageColor', 'SmokeColor', 'TextColor']:
                    memory['main/brick/properties/color']['alpha'] = False

                new_menu = 'main/brick/properties/color'
                return new_menu


            # strany
            elif sel_prop in ['SwitchName', 'Text']:

                memory['main/brick/properties/strany']['property'] = sel_prop
                new_menu = 'main/brick/properties/strany'


            # uint8
            elif sel_prop in ['NumFractionalDigits']:

                memory['main/brick/properties/int']['property'] = sel_prop
                memory['main/brick/properties/color']['limit'] = [0, 255]
                new_menu = 'main/brick/properties/int'

        except IndexError:
            pass

    elif menu == 'main/brick/properties/advanced_required':

        new_menu = 'main/brick/properties'

    elif menu == 'main/brick/properties/eval':

        try:
            val = eval(prompt, globals(), {'prev': memory['main/brick']['properties'][memory['main/brick/properties/eval']['property']], 'math': math, 'BrickInput': BrickInput})
            memory['main/brick']['properties'][memory['main/brick/properties/eval']['property']] = val
            new_menu = 'main/brick/properties'
        except Exception as e:
            memory['invalid']['return_path'] = 'main/brick/properties/eval'
            memory['invalid']['text'] = f'Input: {prompt}\nError: {type(e).__name__}: {e}'
            new_menu = 'invalid'

    elif menu == 'main/brick/properties/color':

        if prompt == '0':
            new_menu = 'main/brick/properties'
            return new_menu
        new_menu = 'main/brick/properties/color'

        color_space = memory['main/brick/properties/color']['mode']

        if color_space == 'select_color_space':

            if prompt == '1':
                memory['main/brick/properties/color']['mode'] = 'hsva'
            elif prompt == '2':
                memory['main/brick/properties/color']['mode'] = 'hsla'
            elif prompt == '3':
                memory['main/brick/properties/color']['mode'] = 'rgba'
            elif prompt == '4':
                memory['main/brick/properties/color']['mode'] = 'cmyka'

            return new_menu

        try:
            values = [i_float(i) for i in multi_replace(prompt, ['[', ']', '(', ')', '{', '}', ' '], '').split(',')]
            min_len = 4
            if color_space == 'cymka':
                min_len = 5
            if len(values) < min_len:
                values += [1.0]

        except ValueError:
            if prompt[0] == '#':
                pass
            else:
                return new_menu

        if color_space == 'hsva':

            if len(values) != 4:
                memory['invalid']['return_path'], memory['invalid']['text'] = 'main/brick/properties/color', 'Please specify 4 elements'
                return 'invalid'

            hsv_h = values[0] / 360
            hsv_s = values[1] / 100
            hsv_v = values[2] / 100
            hsv_a = values[3] / 100

            hsv_h, hsv_s, hsv_v, hsv_a = int(hsv_h * 255), int(hsv_s * 255), int(hsv_v * 255), int(hsv_a * 255)
            memory['main/brick']['properties'][memory['main/brick/properties/color']['property']] = [hsv_h, hsv_s, hsv_v]
            if memory['main/brick/properties/color']['alpha']:
                memory['main/brick']['properties'][memory['main/brick/properties/color']['property']] += [hsv_a]

        elif color_space == 'hsla':

            if len(values) != 4:
                memory['invalid']['return_path'], memory['invalid']['text'] = 'main/brick/properties/color', 'Please specify 4 elements'
                return 'invalid'

            # Convert to hsva; we WILL NOT create a function for that in scripts
            hsl_h = values[0] / 360
            hsl_s = values[1] / 100
            hsl_l = values[2] / 100
            hsv_a = values[3] / 100

            rgb_r, rgb_g, rgb_b = colorsys.hls_to_rgb(hsl_h, hsl_l, hsl_s)
            hsv_h, hsv_s, hsv_v = colorsys.rgb_to_hsv(rgb_r, rgb_g, rgb_b)

            hsv_h, hsv_s, hsv_v, hsv_a = int(hsv_h * 255), int(hsv_s * 255), int(hsv_v * 255), int(hsv_a * 255)

            memory['main/brick']['properties'][memory['main/brick/properties/color']['property']] = [hsv_h, hsv_s, hsv_v]
            if memory['main/brick/properties/color']['alpha']:
                memory['main/brick']['properties'][memory['main/brick/properties/color']['property']] += [hsv_a]

        elif color_space == 'rgba':

            if prompt[0] == '#':

                rgb_r = int(prompt[1:3], 16) / 255
                rgb_g = int(prompt[3:5], 16) / 255
                rgb_b = int(prompt[5:7], 16) / 255
                try:
                    rgb_a = int(prompt[7:9], 16) / 255
                except ValueError:
                    rgb_a = 1.0

            else:

                if len(values) != 4:
                    memory['invalid']['return_path'], memory['invalid'][
                        'text'] = 'main/brick/properties/color', 'Please specify 4 elements'
                    return 'invalid'

                rgb_r = values[0] / 255
                rgb_g = values[1] / 255
                rgb_b = values[2] / 255
                rgb_a = values[3] / 255

            hsv_h, hsv_s, hsv_v = colorsys.rgb_to_hsv(rgb_r, rgb_g, rgb_b)

            hsv_h, hsv_s, hsv_v, hsv_a = int(hsv_h * 255), int(hsv_s * 255), int(hsv_v * 255), int(rgb_a * 255)

            memory['main/brick']['properties'][memory['main/brick/properties/color']['property']] = [hsv_h, hsv_s, hsv_v]
            if memory['main/brick/properties/color']['alpha']:
                memory['main/brick']['properties'][memory['main/brick/properties/color']['property']] += [hsv_a]

        elif color_space == 'cmyka':

            # Convert CYMKA to RGBA

            if len(values) != 5:
                memory['invalid']['return_path'], memory['invalid']['text'] = 'main/brick/properties/color', 'Please specify 4 elements'
                return 'invalid'

            cmyka_c = values[0] / 100
            cmyka_m = values[1] / 100
            cmyka_y = values[2] / 100
            cmyka_k = values[3] / 100
            cmyka_a = values[4] / 100

            rgb_r = (1 - cmyka_c) * (1 - cmyka_k)
            rgb_g = (1 - cmyka_m) * (1 - cmyka_k)
            rgb_b = (1 - cmyka_y) * (1 - cmyka_k)
            rgb_a = cmyka_a

            # Convert RGBA to HSVA
            hsv_h, hsv_s, hsv_v = colorsys.rgb_to_hsv(rgb_r, rgb_g, rgb_b)

            hsv_h, hsv_s, hsv_v, hsv_a = int(hsv_h * 255), int(hsv_s * 255), int(hsv_v * 255), int(rgb_a * 255)

            memory['main/brick']['properties'][memory['main/brick/properties/color']['property']] = [hsv_h, hsv_s, hsv_v]
            if memory['main/brick/properties/color']['alpha']:
                memory['main/brick']['properties'][memory['main/brick/properties/color']['property']] += [hsv_a]

        new_menu = 'main/brick/properties'

    elif menu == 'main/brick/properties/choice':

        try:
            int_prompt = int(prompt)
        except ValueError:
            new_menu = 'main/brick/properties'
            return new_menu

        if int_prompt == 0:

            new_menu = 'main/brick/properties'
            return new_menu
        int_prompt -= 1

        try:
            memory['main/brick']['properties'][memory['main/brick/properties/choice']['property']] = memory['main/brick/properties/choice']['options'][int_prompt]
            new_menu = 'main/brick/properties'
        except IndexError:
            return new_menu

    elif menu == 'main/brick/properties/float':

        try:
            memory['main/brick']['properties'][memory['main/brick/properties/float']['property']] = i_float(prompt)
            new_menu = 'main/brick/properties'
        except ValueError:
            return new_menu

    elif menu == 'main/brick/properties/int':

        try:
            int_prompt = int(prompt)
            if int_prompt < memory['main/brick/properties/int']['limit'][0] or int_prompt > memory['main/brick/properties/int']['limit'][1]:
                memory['invalid']['text'] = f'The integer must be between {memory["main/brick/properties/int"]["limit"][0]} and {memory["main/brick/properties/int"]["limit"][1]}.'
                memory['invalid']['return_path'] = 'main/brick/properties/int'
                new_menu = 'invalid'
                return new_menu
            memory['main/brick']['properties'][memory['main/brick/properties/int']['property']] = int_prompt
            new_menu = 'main/brick/properties'
        except ValueError:
            memory['invalid']['text'] = f'It must be an integer.'
            memory['invalid']['return_path'] = 'main/brick/properties/int'
            new_menu = 'invalid'
            return new_menu

    elif menu == 'main/brick/properties/list':

        none_error_risk = False

        try:

            if prompt == 'None':
                if memory['main/brick/properties/list']['accepts_none']:
                    memory['main/brick']['properties'][memory['main/brick/properties/list']['property']] = None
                    new_menu = 'main/brick/properties'
                    return new_menu
                else:
                    none_error_risk = True

            p_type = memory['main/brick/properties/list']['type']
            list_prompt = prompt.replace(' ', '').split(',')

            if len(list_prompt) in memory['main/brick/properties/list']['len']:
                pass
            else:
                memory['invalid']['text'] = f'The list must have {memory["main/brick/properties/list"]["len"]} elements'
                memory['invalid']['return_path'] = 'main/brick/properties/list'
                new_menu = 'invalid'
                return new_menu

            if p_type == 'float':
                if memory['main/brick/properties/list']['distance'] is not None:
                    list_prompt = [convert_length(clen(x, unit), 'cgs', memory['main/brick/properties/list']['distance']) for x in list_prompt]
                else:
                    list_prompt = [i_float(x) for x in list_prompt]

            memory['main/brick']['properties'][memory['main/brick/properties/list']['property']] = deepcopy(list_prompt)
            new_menu = 'main/brick/properties'

        except Exception as e:

            if none_error_risk:
                memory['invalid']['text'] = f'None is not supported here.'
                memory['invalid']['return_path'] = 'main/brick/properties/list'
                new_menu = 'invalid'
            else:
                memory['invalid']['text'] = f'It appears you gave an invalid list.\n{type(e).__name__}: {e}'
                memory['invalid']['return_path'] = 'main/brick/properties/list'
                new_menu = 'invalid'

    elif menu == 'main/brick/properties/connector':

        try:
            int_prompt = int(prompt)
        except ValueError:
            new_menu = 'main/brick/properties/connector'
            return new_menu

        if int_prompt == 0:
            new_menu = 'main/brick/properties'
            return new_menu
        int_prompt -= 1

        try:
            val = memory['main/brick']['properties'][memory['main/brick/properties/connector']['property']][int_prompt]
            memory['main/brick']['properties'][memory['main/brick/properties/connector']['property']][int_prompt] = int(val+1) % 4
            # new_menu = 'main/brick/properties/connector' # equiv: nothing
        except IndexError:
            pass

    elif menu == 'main/brick/properties/strany':

        if len(prompt) > 32767:
            memory['invalid']['text'] = f'The text is too long ({len(prompt):,}/32,767 characters).'
            memory['invalid']['return_path'] = 'main/brick/properties/strany'
            new_menu = 'invalid'
            return new_menu
        # else:
        new_prompt = prompt.replace('\\r\\n', '\r\n')
        memory['main/brick']['properties'][memory['main/brick/properties/strany']['property']] = new_prompt
        new_menu = 'main/brick/properties'

    elif menu == 'main/help':

        if prompt == '0':
            new_menu = 'main'
        elif prompt == '1':
            if memory['main/help']['lang'] == 'english (english)':
                memory['main/help']['lang'] = 'français (french)'
            elif memory['main/help']['lang'] == 'français (french)':
                memory['main/help']['lang'] = 'русский (russian)'
            elif memory['main/help']['lang'] == 'русский (russian)':
                memory['main/help']['lang'] = 'deutsch (german)'
            elif memory['main/help']['lang'] == 'deutsch (german)':
                memory['main/help']['lang'] = 'español (spanish)'
            else: # memory['main/help']['lang'] == 'español (spanish)':
                memory['main/help']['lang'] = 'english (english)'

            new_menu = 'main/help'


    elif menu == 'main/lightbar':

        try:
            int_prompt = int(prompt)
        except ValueError:
            return new_menu

        if int_prompt == 0:
            new_menu = 'main'
            return new_menu
        int_prompt -= 1

        if int_prompt == 0:
            new_menu = 'main/lightbar/project'
            return new_menu
        int_prompt -= 1

        if int_prompt == 0:
            new_menu = 'main/lightbar/layout'
            return new_menu
        int_prompt -= 1

        if int_prompt == 0:

            new_stage: dict[str, any] = {  # TODO
                'name': "New stage",
                'layer_duration': 0.2,
                'loops': 6,
                'layers': [
                    [False]*10
                ]
            }
            memory['main/lightbar']['lightbar'].append(new_stage)
        int_prompt -= 1

        if int_prompt == 0:

            if len(memory['main/lightbar']['lightbar']) > 0:
                del memory['main/lightbar']['lightbar'][-1]
        int_prompt -= 1

        for i in range(len(memory['main/lightbar']['lightbar'])):
            if int_prompt == 0:
                memory['main/lightbar/stage']['selected'] = i
                new_menu = 'main/lightbar/stage'
                return new_menu
            int_prompt -= 1

        # Export
        if int_prompt == 0:

            projects_dir = os.path.join(cwd, 'projects')
            in_project_dir = os.path.join(projects_dir, memory['main/lightbar']['project'])

            if not os.path.exists(projects_dir):
                memory['invalid']['text'] = 'important folders are missing. Please reinstall BrickUtils.'
                memory['invalid']['return_path'] = 'main/lightbar'
                new_menu = 'invalid'
                return new_menu

            if not os.path.exists(in_project_dir):
                os.makedirs(in_project_dir)

            given_dict = {'important_info': 'warning: modifying this file may cause errors and data loss.',
                          'main/lightbar': memory['main/lightbar']}
            save_json(os.path.join(in_project_dir, 'lightbar.json'), given_dict)

            file_size = os.path.getsize(os.path.join(in_project_dir, 'lightbar.json'))

            memory['success']['text'] = f'Project exported as \'lightbar.json\' ({file_size/1024:,.1f} KiB). Please do not edit this file.'
            memory['success']['return_path'] = 'main/lightbar'
            new_menu = 'success'

            return new_menu

        int_prompt -= 1

        # Import lightbar.json
        if int_prompt == 0:

            projects_dir = os.path.join(cwd, 'projects')
            in_project_dir = os.path.join(projects_dir, memory['main/lightbar']['project'])
            lightbar_dir = os.path.join(in_project_dir, 'lightbar.json')

            if not os.path.exists(projects_dir):
                memory['invalid']['text'] = 'important folders are missing. Please reinstall BrickUtils.'
                memory['invalid']['return_path'] = 'main/lightbar'
                new_menu = 'invalid'
                return new_menu

            if not os.path.exists(in_project_dir):
                memory['invalid']['text'] = 'project not found.'
                memory['invalid']['return_path'] = 'main/lightbar'
                new_menu = 'invalid'
                return new_menu

            if not os.path.exists(lightbar_dir):
                memory['invalid']['text'] = 'lightbar.json is missing.'
                memory['invalid']['return_path'] = 'main/lightbar'
                new_menu = 'invalid'
                return new_menu

            lightbar = load_json(lightbar_dir)

            lightbar.pop('important_info')
            memory.update(lightbar)

            file_size = os.path.getsize(lightbar_dir)

            memory['success']['text'] = f'Imported \'lightbar.json\' ({file_size/1024:,.1f} KiB) from {memory['main/lightbar']['project']}.'
            memory['success']['return_path'] = 'main/lightbar'
            new_menu = 'success'

            memory['main/lightbar']['file_name'] = 'lightbar.json'

            return new_menu

        int_prompt -= 1

        if int_prompt == 0:

            new_menu = 'main/lightbar/import_from'
            return new_menu
        int_prompt -= 1

        # preview
        if int_prompt == 0:

            previews_dir = os.path.join(cwd, 'previews')

            if os.path.exists(previews_dir):
                given_dict = {'main/lightbar': memory['main/lightbar']}
                save_json(os.path.join(previews_dir, 'lightbar.json'), given_dict)

            subprocess.Popen('python previews/lightbar_preview.py', creationflags=subprocess.CREATE_NEW_CONSOLE)

            return new_menu

        int_prompt -= 1

        if int_prompt == 0:

            if not is_valid_folder_name(memory['main/lightbar']['project']):
                memory['invalid']['text'] = 'This project name is invalid (likely unfilled).'
                memory['invalid']['return_path'] = 'main/lightbar'
                new_menu = 'invalid'
                return new_menu

            scripts.lightbar.generate(memory['main/lightbar'], memory['main']['port'][0], memory['main']['backup'], memory['main']['backup_limit'])




    elif menu == 'main/lightbar/project':

        memory['main/lightbar']['project'] = prompt
        new_menu = 'main/lightbar'


    elif menu == 'main/lightbar/layout':

        try:
            int_prompt = int(prompt)
        except ValueError:
            return new_menu

        if int_prompt == 0:
            new_menu = 'main/lightbar'
            return new_menu
        # A bit of wizardry here; look carefully!

        if int_prompt <= len(memory['main/lightbar']['layout']):
            memory['main/lightbar/layout']['selected'] = int_prompt - 1  # Index offset
            return new_menu
        # else:
        int_prompt -= len(memory['main/lightbar']['layout']) + 1

        if int_prompt == 0:
            memory['main/lightbar/layout/color']['mode'] = 'select_color_space'
            memory['main/lightbar/layout/color']['alpha'] = True
            new_menu = 'main/lightbar/layout/color'
            return new_menu
        int_prompt -= 1

        if int_prompt == 0:
            new_menu = 'main/lightbar/layout/brightness'
            return new_menu
        int_prompt -= 1

        if int_prompt == 0:
            new_menu = 'main/lightbar/layout/material'
            return new_menu
        int_prompt -= 1

        if int_prompt == 0:

            if len(memory['main/lightbar']['layout']) > 1:
                sel_brick = memory['main/lightbar/layout']['selected']
                del memory['main/lightbar']['layout'][sel_brick]

                for stage in memory['main/lightbar']['lightbar']:
                    for layer in stage['layers']:
                        del layer[sel_brick]

            return new_menu
        int_prompt -= 1

        if int_prompt == 0:

            if len(memory['main/lightbar']['layout']) < 99:
                sel_brick = memory['main/lightbar/layout']['selected']
                memory['main/lightbar']['layout'].insert(sel_brick + 1, {
                    'col': [0, 0, 127, 255],
                    'brightness': 0.5,
                    'material': 'Glass'
                })

                for stage in memory['main/lightbar']['lightbar']:
                    for layer in stage['layers']:
                        layer.insert(sel_brick + 1, False)

            return new_menu
        int_prompt -= 1

        if int_prompt == 0:

            if len(memory['main/lightbar']['layout']) < 99:
                sel_brick = memory['main/lightbar/layout']['selected']
                memory['main/lightbar']['layout'].insert(sel_brick + 1, deepcopy(memory['main/lightbar']['layout'][sel_brick]))

                for stage in memory['main/lightbar']['lightbar']:
                    for layer in stage['layers']:
                        layer.insert(sel_brick + 1, layer[sel_brick])

            return new_menu

    elif menu == 'main/lightbar/layout/color':

        brick = memory['main/lightbar']['layout'][memory['main/lightbar/layout']['selected']]

        if prompt == '0':
            new_menu = 'main/lightbar/layout'
            return new_menu
        new_menu = 'main/lightbar/layout/color'

        color_space = memory['main/lightbar/layout/color']['mode']

        if color_space == 'select_color_space':

            if prompt == '1':
                memory['main/lightbar/layout/color']['mode'] = 'hsva'
            elif prompt == '2':
                memory['main/lightbar/layout/color']['mode'] = 'hsla'
            elif prompt == '3':
                memory['main/lightbar/layout/color']['mode'] = 'rgba'
            elif prompt == '4':
                memory['main/lightbar/layout/color']['mode'] = 'cmyka'

            return new_menu

        try:
            values = [i_float(i) for i in multi_replace(prompt, ['[', ']', '(', ')', '{', '}', ' '], '').split(',')]
            min_len = 4
            if color_space == 'cymka':
                min_len = 5
            if len(values) < min_len:
                values += [1.0]

        except ValueError:
            if prompt[0] == '#':
                pass
            else:
                return new_menu

        if color_space == 'hsva':

            if len(values) != 4:
                memory['invalid']['return_path'], memory['invalid']['text'] = 'main/lightbar/layout/color', 'Please specify 4 elements'
                return 'invalid'

            hsv_h = values[0] / 360
            hsv_s = values[1] / 100
            hsv_v = values[2] / 100
            hsv_a = values[3] / 100

            hsv_h, hsv_s, hsv_v, hsv_a = int(hsv_h * 255), int(hsv_s * 255), int(hsv_v * 255), int(hsv_a * 255)
            brick['col'] = [hsv_h, hsv_s, hsv_v]
            if memory['main/lightbar/layout/color']['alpha']:
                brick['col'] += [hsv_a]

        elif color_space == 'hsla':

            if len(values) != 4:
                memory['invalid']['return_path'], memory['invalid']['text'] = 'main/lightbar/layout/color', 'Please specify 4 elements'
                return 'invalid'

            # Convert to hsva; we WILL NOT create a function for that in scripts
            hsl_h = values[0] / 360
            hsl_s = values[1] / 100
            hsl_l = values[2] / 100
            hsv_a = values[3] / 100

            rgb_r, rgb_g, rgb_b = colorsys.hls_to_rgb(hsl_h, hsl_l, hsl_s)
            hsv_h, hsv_s, hsv_v = colorsys.rgb_to_hsv(rgb_r, rgb_g, rgb_b)

            hsv_h, hsv_s, hsv_v, hsv_a = int(hsv_h * 255), int(hsv_s * 255), int(hsv_v * 255), int(hsv_a * 255)

            brick['col'] = [hsv_h, hsv_s, hsv_v]
            if memory['main/lightbar/layout/color']['alpha']:
                brick['col'] += [hsv_a]

        elif color_space == 'rgba':

            if prompt[0] == '#':

                rgb_r = int(prompt[1:3], 16) / 255
                rgb_g = int(prompt[3:5], 16) / 255
                rgb_b = int(prompt[5:7], 16) / 255
                try:
                    rgb_a = int(prompt[7:9], 16) / 255
                except ValueError:
                    rgb_a = 1.0

            else:

                if len(values) != 4:
                    memory['invalid']['return_path'], memory['invalid'][
                        'text'] = 'main/lightbar/layout/color', 'Please specify 4 elements'
                    return 'invalid'

                rgb_r = values[0] / 255
                rgb_g = values[1] / 255
                rgb_b = values[2] / 255
                rgb_a = values[3] / 255

            hsv_h, hsv_s, hsv_v = colorsys.rgb_to_hsv(rgb_r, rgb_g, rgb_b)

            hsv_h, hsv_s, hsv_v, hsv_a = int(hsv_h * 255), int(hsv_s * 255), int(hsv_v * 255), int(rgb_a * 255)

            brick['col'] = [hsv_h, hsv_s, hsv_v]
            if memory['main/lightbar/layout/color']['alpha']:
                brick['col'] += [hsv_a]

        elif color_space == 'cmyka':

            # Convert CYMKA to RGBA
            if len(values) != 5:
                memory['invalid']['return_path'], memory['invalid']['text'] = 'main/lightbar/layout/color', 'Please specify 4 elements'
                return 'invalid'

            cmyka_c = values[0] / 100
            cmyka_m = values[1] / 100
            cmyka_y = values[2] / 100
            cmyka_k = values[3] / 100
            cmyka_a = values[4] / 100

            rgb_r = (1 - cmyka_c) * (1 - cmyka_k)
            rgb_g = (1 - cmyka_m) * (1 - cmyka_k)
            rgb_b = (1 - cmyka_y) * (1 - cmyka_k)
            rgb_a = cmyka_a

            # Convert RGBA to HSVA
            hsv_h, hsv_s, hsv_v = colorsys.rgb_to_hsv(rgb_r, rgb_g, rgb_b)

            hsv_h, hsv_s, hsv_v, hsv_a = int(hsv_h * 255), int(hsv_s * 255), int(hsv_v * 255), int(rgb_a * 255)

            brick['col'] = [hsv_h, hsv_s, hsv_v]
            if memory['main/lightbar/layout/color']['alpha']:
                brick['col'] += [hsv_a]

        new_menu = 'main/lightbar/layout'

    elif menu == 'main/lightbar/layout/brightness':

        try:
            memory['main/lightbar']['layout'][memory['main/lightbar/layout']['selected']]['brightness'] = i_float(prompt)
        except ValueError:
            memory['invalid']['text'] = 'Brightness must be a value.'
            memory['invalid']['return_path'] = 'main/lightbar/layout'
            new_menu = 'invalid'
            return new_menu

        new_menu = 'main/lightbar/layout'

    elif menu == 'main/lightbar/layout/material':

        if prompt not in ['0', '1', '2', '3', '4']:
            return new_menu

        # if prompt == '0':
            # new_menu = 'main/lightbar/layout'
        # elif prompt == '1':
        if prompt == '1':
            memory['main/lightbar']['layout'][memory['main/lightbar/layout']['selected']]['material'] = 'Glass'
        elif prompt == '2':
            memory['main/lightbar']['layout'][memory['main/lightbar/layout']['selected']]['material'] = 'CloudyGlass'
        elif prompt == '3':
            memory['main/lightbar']['layout'][memory['main/lightbar/layout']['selected']]['material'] = 'Glow'
        elif prompt == '4':
            memory['main/lightbar']['layout'][memory['main/lightbar/layout']['selected']]['material'] = 'LEDMatrix'

        new_menu = 'main/lightbar/layout'

    elif menu == 'main/lightbar/stage':

        stage = memory['main/lightbar']['lightbar'][memory['main/lightbar/stage']['selected']]

        try:
            separators = ['/', '.', ',', ' ']
            if not any([separator in prompt for separator in separators]):
                if prompt == '0':
                    new_menu = 'main/lightbar'
                elif prompt == '1':
                    new_menu = 'main/lightbar/stage/name'
                elif prompt == '2':
                    new_menu = 'main/lightbar/stage/layer_duration'
                elif prompt == '3':
                    new_menu = 'main/lightbar/stage/loops'
                elif prompt == '4':
                    if len(stage['layers']) < 99:
                        stage['layers'].append([False] * len(memory['main/lightbar']['layout']))
                elif prompt == '5':
                    if len(stage['layers']) > 1:
                        del stage['layers'][-1]
                    else:
                        stage['layers'] = [[False] * len(memory['main/lightbar']['layout'])]

            else:
                if '/' in prompt:
                    path: list[str] = prompt.split('/')
                elif '.' in prompt:
                    path: list[str] = prompt.split('.')
                elif ',' in prompt:
                    path: list[str] = prompt.split(',')
                else: # if ' ' in prompt:
                    path: list[str] = prompt.split(' ')

                path: tuple[int, int] = (int(path[0]), int(path[1]))

                if not (0 < path[0] <= len(stage['layers']) and 0 < path[1] <= len(memory['main/lightbar']['layout'])):
                    memory['invalid']['text'] = f'Invalid light (layer {path[0]} / brick {path[1]})'
                    memory['invalid']['return_path'] = 'main/lightbar/stage'
                    new_menu = 'invalid'
                    return new_menu

                stage['layers'][path[0]-1][path[1]-1] = not stage['layers'][path[0]-1][path[1]-1]

        except ValueError:
            pass

    elif menu == 'main/lightbar/stage/name':

        stage = memory['main/lightbar']['lightbar'][memory['main/lightbar/stage']['selected']]
        stage['name'] = prompt
        new_menu = 'main/lightbar/stage'

    elif menu == 'main/lightbar/stage/layer_duration':

        new_menu = 'main/lightbar/stage'
        if prompt == '0':
            return new_menu

        stage = memory['main/lightbar']['lightbar'][memory['main/lightbar/stage']['selected']]
        try:
            float_prompt = i_float(prompt)
            if float_prompt <= 0:
                raise ValueError
            stage['layer_duration'] = float_prompt / 1_000
        except ValueError:
            memory['invalid']['text'] = 'Layer duration must be a value greater than 0.'
            memory['invalid']['return_path'] = 'main/lightbar/stage'
            new_menu = 'invalid'

    elif menu == 'main/lightbar/stage/loops':

        new_menu = 'main/lightbar/stage'
        if prompt == '0':
            return new_menu

        stage = memory['main/lightbar']['lightbar'][memory['main/lightbar/stage']['selected']]
        try:
            int_prompt = i_int(prompt)
            if int_prompt <= 0:
                raise ValueError
            stage['loops'] = int_prompt
        except ValueError:
            memory['invalid']['text'] = 'Loops must be an integer greater than 0.'
            memory['invalid']['return_path'] = 'main/lightbar/stage'
            new_menu = 'invalid'


    elif menu == 'main/lightbar/import_from':

        projects_dir = os.path.join(cwd, 'projects')
        in_project_dir = os.path.join(projects_dir, memory['main/lightbar']['project'])
        lightbar_dir = os.path.join(in_project_dir, prompt)

        if not os.path.exists(projects_dir):
            memory['invalid']['text'] = 'important folders are missing. Please reinstall BrickUtils.'
            memory['invalid']['return_path'] = 'main/lightbar'
            new_menu = 'invalid'
            return new_menu

        if not os.path.exists(in_project_dir):
            memory['invalid']['text'] = 'project not found.'
            memory['invalid']['return_path'] = 'main/lightbar'
            new_menu = 'invalid'
            return new_menu

        if not os.path.exists(lightbar_dir) or prompt == '':
            memory['invalid']['text'] = f'{prompt} is missing.'
            if prompt == '':
                memory['invalid']['text'] = f'Specify a file to import.'
            memory['invalid']['return_path'] = 'main/lightbar'
            new_menu = 'invalid'
            return new_menu

        lightbar = load_json(lightbar_dir)

        lightbar.pop('important_info')
        memory.update(lightbar)

        file_size = os.path.getsize(lightbar_dir)

        memory['success']['text'] = f'Imported \'{prompt}\' ({file_size/1024:,.1f} KiB) from {memory['main/lightbar']['project']}.'
        memory['success']['return_path'] = 'main/lightbar'
        new_menu = 'success'

        memory['main/lightbar']['file_name'] = prompt

        return new_menu

    elif menu == 'main/encrypt':

        if prompt == '0':

            new_menu = 'main'

        elif prompt == '1':

            new_menu = 'main/encrypt/project'

        elif prompt == '2':

            new_menu = 'main/encrypt/password'

        elif prompt == '3':

            memory['main/encrypt']['see_password'] = True

        elif prompt == '4':

            new_menu = 'main/encrypt/generate'
            memory['main/encrypt/generate']['password'] = return_password(128, 256)

        elif prompt == '5':

            new_menu = 'main/encrypt/info'

        elif prompt == '6':

            if not is_valid_folder_name(memory['main/encrypt']['project']):
                memory['invalid']['text'] = 'This project name is invalid (likely unfilled).'
                memory['invalid']['return_path'] = 'main/encrypt'
                new_menu = 'invalid'
                return new_menu

            success, message = False, ''

            try:
                success, message = scripts.encrypt.encrypt(memory['main/encrypt'], memory['main']['port'][1], memory['main']['backup'], memory['main']['backup_limit'])
                if success:
                    memory['success']['text'] = f'Successfully encrypted \'{memory['main/encrypt']['project']}\' {message}'
                    memory['success']['return_path'] = 'main/encrypt'
                    new_menu = 'success'
                else:
                    memory['invalid']['text'] = f'Failed to encrypt \'{memory['main/encrypt']['project']}\': {message}'
                    memory['invalid']['return_path'] = 'main/encrypt'
                    new_menu = 'invalid'

            except Exception as e:
                memory['invalid']['text'] = f'Encryption failed: an unexpected error occured\n({type(e).__name__}: {e})'
                memory['invalid']['return_path'] = 'main/encrypt'
                new_menu = 'invalid'

        elif prompt == '7':

            if not is_valid_folder_name(memory['main/encrypt']['project']):
                memory['invalid']['text'] = 'This project name is invalid (likely unfilled).'
                memory['invalid']['return_path'] = 'main/encrypt'
                new_menu = 'invalid'
                return new_menu

            success, message = False, ''

            try:
                success, message = scripts.encrypt.decrypt(memory['main/encrypt'], memory['main']['port'][1], memory['main']['backup'], memory['main']['backup_limit'])
                if success:
                    memory['success']['text'] = f'Successfully decrypted \'{memory['main/encrypt']['project']}\' {message}'
                    memory['success']['return_path'] = 'main/encrypt'
                    new_menu = 'success'
                else:
                    memory['invalid']['text'] = f'Failed to decrypt \'{memory['main/encrypt']['project']}\': {message}'
                    memory['invalid']['return_path'] = 'main/encrypt'
                    new_menu = 'invalid'

            except Exception as e:
                memory['invalid']['text'] = f'Decryption failed: an unexpected error occured\n({type(e).__name__}: {e})'
                memory['invalid']['return_path'] = 'main/encrypt'
                new_menu = 'invalid'

    elif menu == 'main/encrypt/project':

        memory['main/encrypt']['project'] = prompt
        new_menu = 'main/encrypt'

    elif menu == 'main/encrypt/password':

        pw = memory['main/encrypt/password']
        pw['pre_pass'][int(pw['repeat'])] = prompt

        if pw['repeat']:
            if pw['pre_pass'][0] == pw['pre_pass'][1]:
                memory['main/encrypt']['password'] = pw['pre_pass'][0]
                new_menu = 'main/encrypt'
            else:
                memory['invalid']['text'] = f'Passwords don\'t match ({pw["pre_pass"][0]} / {pw["pre_pass"][1]})'
                memory['invalid']['return_path'] = 'main/encrypt'
                new_menu = 'invalid'

        pw['repeat'] = not pw['repeat']

    elif menu == 'main/encrypt/generate':

        if prompt == '0':

            new_menu = 'main/encrypt'

        elif prompt == '1':

            memory['main/encrypt']['password'] = memory['main/encrypt/generate']['password']
            set_clipboard(memory['main/encrypt/generate']['password'])

        elif prompt == '2':

            set_clipboard(memory['main/encrypt/generate']['password'])

    elif menu == 'main/encrypt/info':

        if prompt == '0':

            new_menu = 'main/encrypt'

    elif menu == 'main/edit':

        try:
            int_prompt = int(prompt)
        except ValueError:
            return new_menu

        if int_prompt == 0:
            new_menu = 'main'
            return new_menu
        int_prompt -= 1

        if int_prompt == 0:
            new_menu = 'main/edit/project'
            return new_menu
        int_prompt -= 1

        if int_prompt == 0:
            if memory['main/edit']['move'] is None:
                memory['main/edit']['move'] = [0.0, 0.0, 0.0]
            else:
                new_menu = 'main/edit/move'
                return new_menu
        int_prompt -= 1

        if int_prompt == 0:
            if memory['main/edit']['rotate'] is None:
                memory['main/edit']['rotate'] = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
                memory['main/edit']['allow_out_of_range_rotation'] = False
            else:
                memory['main/edit']['rotate'] = None
        int_prompt -= 1

        if memory['main/edit']['rotate'] is not None and numpy_features_enabled:

            if int_prompt == 0:
                new_menu = 'main/edit/rotate_around'
                return new_menu
            int_prompt -= 1

            if int_prompt == 0:
                new_menu = 'main/edit/rotate_by'
                return new_menu
            int_prompt -= 1

            if int_prompt == 0:
                memory['main/edit']['allow_out_of_range_rotation'] = not memory['main/edit']['allow_out_of_range_rotation']
            int_prompt -= 1

        if int_prompt == 0:
            if memory['main/edit']['scale'] is None:
                memory['main/edit']['scale'] = 1.0
            else:
                new_menu = 'main/edit/scale'
                return new_menu
        int_prompt -= 1

        if int_prompt == 0:
            memory['main/edit/connections'] = deepcopy({
                'edited': 'sides',
                'new': {'sides': True, 'top': True, 'bottom': True},
                'scores': {'sides': [0, 0], 'top': [0, 0], 'bottom': [0, 0]},
            })

            new_menu = 'main/edit/connections'
            return new_menu
        int_prompt -= 1

        if int_prompt == 0:
            if memory['main/edit']['duplicates'] == 'keep':
                memory['main/edit']['duplicates'] = 'delete identical'
            else: #if memory['main/edit']['duplicates'] == 'delete identical':
                memory['main/edit']['duplicates'] = 'keep'
            new_menu = 'main/edit'
            return new_menu
        int_prompt -= 1

        if int_prompt == 0:
            # noinspection PyUnusedLocal
            success, return_data = False, ''
            try:
                success, return_data = scripts.edit.edit(memory['main/edit'], unit, memory['main']['port'][1],
                                                         memory['main']['backup'], memory['main']['backup_limit'])
            except Exception as e:
                memory['invalid']['return_path'] = 'main/edit'
                memory['invalid'][
                    'text'] = f'Failed to modify creation (An unexpected error occured!).\n{type(e).__name__}: {e}'
                new_menu = 'invalid'
                return new_menu
            if success:
                memory['success']['return_path'] = 'main/edit'
                memory['success']['text'] = f'Successfully modified \'{memory['main/edit']['project']}\' {return_data}'
                new_menu = 'success'
            else:
                memory['invalid']['return_path'] = 'main/edit'
                memory['invalid']['text'] = f'Failed to modify creation: {return_data}.'
                new_menu = 'invalid'

        int_prompt -= 1


    elif menu == 'main/edit/project':

        try:
            memory['main/edit']['project'] = prompt
            new_menu = 'main/edit'

        except ValueError:
            memory['invalid']['return_path'] = 'main/edit'
            memory['invalid']['text'] = f"Congrats! You somehow made project name invalid."

    elif menu == 'main/edit/move':

        if prompt == '0':

            new_menu = 'main/edit'

        elif prompt == '1':

            new_menu = 'main/edit/move/x'

        elif prompt == '2':

            new_menu = 'main/edit/move/y'

        elif prompt == '3':

            new_menu = 'main/edit/move/z'

        elif prompt == '4':

            memory['main/edit']['move'] = None
            new_menu = 'main/edit'

    elif menu == 'main/edit/move/x':

        try:
            memory['main/edit']['move'][0] = clen(prompt, unit)
            new_menu = 'main/edit/move'
        except ValueError:
            memory['invalid']['return_path'] = 'main/edit/move'
            memory['invalid']['text'] = "Offset on X axis must be a number."
            new_menu = 'invalid'

    elif menu == 'main/edit/move/y':

        try:
            memory['main/edit']['move'][1] = clen(prompt, unit)
            new_menu = 'main/edit/move'
        except ValueError:
            memory['invalid']['return_path'] = 'main/edit/move'
            memory['invalid']['text'] = "Offset on Y axis must be a number."
            new_menu = 'invalid'

    elif menu == 'main/edit/move/z':

        try:
            memory['main/edit']['move'][2] = clen(prompt, unit)
            new_menu = 'main/edit/move'
        except ValueError:
            memory['invalid']['return_path'] = 'main/edit/move'
            memory['invalid']['text'] = "Offset on Z axis must be a number."
            new_menu = 'invalid'

    elif menu == 'main/edit/rotate_around':

        if prompt == '0':
            new_menu = 'main/edit'
        elif prompt == '1':
            new_menu = 'main/edit/rotate_around/x'
        elif prompt == '2':
            new_menu = 'main/edit/rotate_around/y'
        elif prompt == '3':
            new_menu = 'main/edit/rotate_around/z'
        elif prompt == '4':
            memory['main/edit']['rotate'][1] = [0.0, 0.0, 0.0]

    elif menu == 'main/edit/rotate_around/x':

        try:
            memory['main/edit']['rotate'][1][0] = clen(prompt, unit)
            new_menu = 'main/edit/rotate_around'
        except ValueError:
            memory['invalid']['return_path'] = 'main/edit/rotate_around'
            memory['invalid']['text'] = "Center of rotation position on X axis must be a number."
            new_menu = 'invalid'

    elif menu == 'main/edit/rotate_around/y':

        try:
            memory['main/edit']['rotate'][1][1] = clen(prompt, unit)
            new_menu = 'main/edit/rotate_around'
        except ValueError:
            memory['invalid']['return_path'] = 'main/edit/rotate_around'
            memory['invalid']['text'] = "Center of rotation position on Y axis must be a number."
            new_menu = 'invalid'

    elif menu == 'main/edit/rotate_around/z':

        try:
            memory['main/edit']['rotate'][1][2] = clen(prompt, unit)
            new_menu = 'main/edit/rotate_around'
        except ValueError:
            memory['invalid']['return_path'] = 'main/edit/rotate_around'
            memory['invalid']['text'] = "Center of rotation position on Z axis must be a number."
            new_menu = 'invalid'

    elif menu == 'main/edit/rotate_by':

        if prompt == '0':
            new_menu = 'main/edit'
        elif prompt == '1':
            new_menu = 'main/edit/rotate_by/x'
        elif prompt == '2':
            new_menu = 'main/edit/rotate_by/y'
        elif prompt == '3':
            new_menu = 'main/edit/rotate_by/z'
        elif prompt == '4':
            memory['main/edit']['rotate'][0] = [0.0, 0.0, 0.0]

    elif menu == 'main/edit/rotate_by/x':

        try:
            memory['main/edit']['rotate'][0][0] = i_float(prompt)
            new_menu = 'main/edit/rotate_by'
        except ValueError:
            memory['invalid']['return_path'] = 'main/edit/rotate_by'
            memory['invalid']['text'] = "Rotation angle on X axis must be a number."
            new_menu = 'invalid'

    elif menu == 'main/edit/rotate_by/y':

        try:
            memory['main/edit']['rotate'][0][1] = i_float(prompt)
            new_menu = 'main/edit/rotate_by'
        except ValueError:
            memory['invalid']['return_path'] = 'main/edit/rotate_by'
            memory['invalid']['text'] = "Rotation angle on Y axis must be a number."
            new_menu = 'invalid'

    elif menu == 'main/edit/rotate_by/z':

        try:
            memory['main/edit']['rotate'][0][2] = i_float(prompt)
            new_menu = 'main/edit/rotate_by'
        except ValueError:
            memory['invalid']['return_path'] = 'main/edit/rotate_by'
            memory['invalid']['text'] = "Rotation angle on Z axis must be a number."
            new_menu = 'invalid'

    elif menu == 'main/edit/scale':

        if prompt == '0':
            new_menu = 'main/edit'
        elif prompt == '1':
            new_menu = 'main/edit/scale/set_scale'
        elif prompt == '2':
            memory['main/edit']['scale'] = None

    elif menu == 'main/edit/scale/set_scale':

        try:
            memory['main/edit']['scale'] = i_float(prompt)
            new_menu = 'main/edit/scale'
        except ValueError:
            memory['invalid']['return_path'] = 'main/edit/scale'
            memory['invalid']['text'] = "Scale must be a number."
            new_menu = 'invalid'

    elif menu == 'main/edit/connections':

        if prompt == '0':
            new_menu = 'main/edit'
            return new_menu

        # else:
        edited = memory['main/edit/connections']['edited']
        if not memory['main/edit/connections']['edited'] == 'confirm':
            # get input
            modified_input = multi_replace(prompt.lower(), char_blacklist, '')
            user_pos, user_neg = count_strings_in_list(modified_input, [(key, item) for key, item in react_dict.items() if key != 'y'][::-1])
            # interpret output
            if prompt == 'y': user_pos = 10.0
            elif prompt == 'n': user_neg = 10.0
            if user_pos - user_neg != 0:
                memory['main/edit/connections']['new'][edited] = user_pos - user_neg > 0
                memory['main/edit/connections']['scores'][edited] = [round(user_pos, 4), round(user_neg, 4)]
            elif user_pos == user_neg and user_pos != 0:
                memory['invalid']['return_path'] = 'main/edit/connections'
                memory['invalid']['text'] = 'Brickutils is unsure if you meant yes or no.'
                new_menu = 'invalid'
                return new_menu
            else:  # if user_pos == user_neg == 0
                memory['invalid']['return_path'] = 'main/edit/connections'
                memory['invalid']['text'] = 'Input misunderstood. Try yes / no.'
                new_menu = 'invalid'
                return new_menu

        if edited == 'sides':
            memory['main/edit/connections']['edited'] = 'top'
        elif edited == 'top':
            memory['main/edit/connections']['edited'] = 'bottom'
        elif edited == 'bottom':
            memory['main/edit/connections']['edited'] = 'confirm'
        elif edited == 'confirm':
            # get input
            modified_input = multi_replace(prompt.lower(), char_blacklist, '')
            user_pos, user_neg = count_strings_in_list(modified_input, [(key, item) for key, item in react_dict.items() if key != 'y'][::-1])
            # interpret output
            if prompt == 'y': user_pos = 10.0
            elif prompt == 'n': user_neg = 10.0
            # If favorable
            if user_pos > user_neg:
                memory['main/edit']['connections'] = deepcopy(memory['main/edit/connections']['new'])
                new_menu = 'main/edit'
            elif user_pos < user_neg:
                memory['main/edit/connections']['edited'] = 'sides'
                memory['main/edit/connections']['new'] = {'sides': True, 'top': True, 'bottom': True}.copy()
            elif user_pos == user_neg and user_pos != 0:
                memory['invalid']['return_path'] = 'main/edit/connections'
                memory['invalid']['text'] = 'BrickUtils is unsure if you meant yes or no.'
                new_menu = 'invalid'
                return new_menu
            else: # if user_pos == user_neg == 0
                memory['invalid']['return_path'] = 'main/edit/connections'
                memory['invalid']['text'] = 'Input misunderstood. Try yes / no.'
                new_menu = 'invalid'
                return new_menu

    return new_menu
