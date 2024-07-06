import os
from brci import BrickInput
from copy import deepcopy
from data import react_dict, char_blacklist, clen, init_memory, i_int, i_float, cwd, save_json, multi_replace, convert_length
import colorsys
import scripts
import math


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
            memory = deepcopy(init_memory)
            new_menu = 'main'
        elif prompt.lower() in ['n', 'no']:
            new_menu = 'main'
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
            memory['invalid']['text'] = 'Hollow arc generator was not implemented yet. '
            new_menu = 'invalid'
            # new_menu = 'main/arc'

        elif prompt == '3':

            new_menu = 'main/pixelart'

        elif prompt == '4':

            new_menu = 'main/edit'

        elif prompt == '5':

            new_menu = 'main/rotate'

        elif prompt == '6':

            memory['main/settings']['new_main'] = deepcopy(memory['main'])
            new_menu = 'main/settings'

        elif prompt == '7':

            new_menu = 'main/help'  # TODO

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
            memory['main/edit']['move'] = not memory['main/edit']['move']
        int_prompt -= 1

        if memory['main/edit']['move']:
            if int_prompt == 0:
                new_menu = 'main/edit/off_x'
            int_prompt -= 1

            if int_prompt == 0:
                new_menu = 'main/edit/off_y'
            int_prompt -= 1

            if int_prompt == 0:
                new_menu = 'main/edit/off_z'
            int_prompt -= 1

        if int_prompt == 0:
            memory['main/edit']['scale'] = not memory['main/edit']['scale']
        int_prompt -= 1

        if memory['main/edit']['scale']:
            if int_prompt == 0:
                new_menu = 'main/edit/scale_x'
            int_prompt -= 1

            if int_prompt == 0:
                new_menu = 'main/edit/scale_y'
            int_prompt -= 1

            if int_prompt == 0:
                new_menu = 'main/edit/scale_z'
            int_prompt -= 1

            if int_prompt == 0:
                if memory['main/edit']['adapt_connections'] == 'no':
                    memory['main/edit']['adapt_connections'] = 'delete'
                elif memory['main/edit']['adapt_connections'] == 'delete':
                    memory['main/edit']['adapt_connections'] = 'yes'
                else: # if memory['main/edit']['adjust_connections'] == 'yes':
                    memory['main/edit']['adapt_connections'] = 'no'
            int_prompt -= 1

            if int_prompt == 0:
                memory['main/edit']['scale_extras'] = not memory['main/edit']['scale_extras']
            int_prompt -= 1

        if int_prompt == 0:
            memory['main/edit']['rotate'] = not memory['main/edit']['rotate']
        int_prompt -= 1

        if memory['main/edit']['rotate']:
            if int_prompt == 0:
                new_menu = 'main/edit/rot_x'
            int_prompt -= 1

            if int_prompt == 0:
                new_menu = 'main/edit/rot_y'
            int_prompt -= 1

            if int_prompt == 0:
                new_menu = 'main/edit/rot_z'
            int_prompt -= 1

        if int_prompt == 0:
            memory['main/edit']['clear_duplicates'] = not memory['main/edit']['clear_duplicates']
        int_prompt -= 1

        if int_prompt == 0:
            # noinspection PyUnusedLocal
            success, return_data = False, ''
            try:
                success, return_data = scripts.edit.edit(memory['main/edit'], unit, memory['main']['port'][1], memory['main']['backup'], memory['main']['backup_limit'])
            except Exception as e:
                memory['invalid']['return_path'] = 'main/edit'
                memory['invalid']['text'] = f'Failed to modify creation (An unexpected error occured!).\n{type(e).__name__}: {e}'
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

    elif menu == 'main/edit/off_x':

        try:
            memory['main/edit']['off_x'] = clen(prompt, unit)
            new_menu = 'main/edit'

        except ValueError:
            memory['invalid']['return_path'] = 'main/edit'
            memory['invalid']['text'] = f"Offset on the x axis must be a number."
            new_menu = 'invalid'

    elif menu == 'main/edit/off_y':

        try:
            memory['main/edit']['off_y'] = clen(prompt, unit)
            new_menu = 'main/edit'

        except ValueError:
            memory['invalid']['return_path'] = 'main/edit'
            memory['invalid']['text'] = f"Offset on the y axis must be a number."
            new_menu = 'invalid'

    elif menu == 'main/edit/off_z':

        try:
            memory['main/edit']['off_z'] = clen(prompt, unit)
            new_menu = 'main/edit'

        except ValueError:
            memory['invalid']['return_path'] = 'main/edit'
            memory['invalid']['text'] = f"Offset on the z axis must be a number."
            new_menu = 'invalid'

    elif menu == 'main/edit/scale_x':

        try:
            memory['main/edit']['scale_x'] = i_float(prompt)
            new_menu = 'main/edit'

        except ValueError:
            memory['invalid']['return_path'] = 'main/edit'
            memory['invalid']['text'] = f"Scale on the x axis must be a number."
            new_menu = 'invalid'

    elif menu == 'main/edit/scale_y':

        try:
            memory['main/edit']['scale_y'] = i_float(prompt)
            new_menu = 'main/edit'

        except ValueError:
            memory['invalid']['return_path'] = 'main/edit'
            memory['invalid']['text'] = f"Scale on the y axis must be a number."
            new_menu = 'invalid'

    elif menu == 'main/edit/scale_z':

        try:
            memory['main/edit']['scale_z'] = i_float(prompt)
            new_menu = 'main/edit'

        except ValueError:
            memory['invalid']['return_path'] = 'main/edit'
            memory['invalid']['text'] = f"Scale on the z axis must be a number."

    elif menu == 'main/edit/rot_x':

        try:
            memory['main/edit']['rot_x'] = i_float(prompt)
            new_menu = 'main/edit'

        except ValueError:
            memory['invalid']['return_path'] = 'main/edit'
            memory['invalid']['text'] = f"Rotation on the x axis must be a number."

    elif menu == 'main/edit/rot_y':

        try:
            memory['main/edit']['rot_y'] = i_float(prompt)
            new_menu = 'main/edit'

        except ValueError:
            memory['invalid']['return_path'] = 'main/edit'
            memory['invalid']['text'] = f"Rotation on the y axis must be a number."

    elif menu == 'main/edit/rot_z':

        try:
            memory['main/edit']['rot_z'] = i_float(prompt)
            new_menu = 'main/edit'

        except ValueError:
            memory['invalid']['return_path'] = 'main/edit'
            memory['invalid']['text'] = f"Rotation on the z axis must be a number."

    elif menu == 'main/edit/project':

        try:
            memory['main/edit']['project'] = prompt
            new_menu = 'main/edit'

        except ValueError:
            memory['invalid']['return_path'] = 'main/edit'
            memory['invalid']['text'] = f"Congrats! You somehow made project name invalid."

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

            success, output_message = scripts.brick.generate(memory['main/brick'], memory['main']['port'][0], memory['main']['backup'], memory['main']['backup_limit'])

            if success:

                memory['success']['text'] = 'Successfully generated 1 brick.'
                new_menu = 'success'

            else:

                memory['invalid']['text'] = f'An error occured: {output_message}'
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


            if memory['main/brick/properties']['advanced']:  # Yes it's separate because idk

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
            hsv_h = values[0] / 360
            hsv_s = values[1] / 100
            hsv_v = values[2] / 100
            hsv_a = values[3] / 100

            hsv_h, hsv_s, hsv_v, hsv_a = int(hsv_h * 255), int(hsv_s * 255), int(hsv_v * 255), int(hsv_a * 255)
            memory['main/brick']['properties'][memory['main/brick/properties/color']['property']] = [hsv_h, hsv_s, hsv_v]
            if memory['main/brick/properties/color']['alpha']:
                memory['main/brick']['properties'][memory['main/brick/properties/color']['property']] += [hsv_a]

        elif color_space == 'hsla':

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
            else:
                memory['main/help']['lang'] = 'english (english)'
            new_menu = 'main/help'


    return new_menu
