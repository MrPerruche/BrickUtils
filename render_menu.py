import os
from brci import FM, deepcopy
from data import version, br_version, get_len_unit, clen_str, str_connector, str_int_dir, match_color, render_lightbar
from data import get_r_lightbar_colors
import re


# Everything regarding print() here. This part is... alright, I guess.
# I really don't see much to say here. It's not in order, but it's not too bad.
# I ate cereals today.


cwd = os.path.dirname(os.path.realpath(__file__))


def clear_terminal():
    # os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[H\033[J", end='')


def bool_to_yes_no(value: bool) -> str:
    return 'yes' if value else 'no'


def render_text(pre_text: str, text: str, is_menu: bool, color: str | None = None) -> str:
    # Get color chars to use
    color_ = FM.remove_color if color is None else color
    menu_highlight = FM.reverse if is_menu else FM.remove_reverse

    # Add spacing to the margin
    pre_text = ' ' * (5 - len(pre_text)) + pre_text

    # Return text
    return f'{color_}{FM.reverse} {pre_text} {menu_highlight} {text} {FM.remove_color}{FM.remove_reverse}'


def render_menu(menu: str, memory: dict[str, any], safe_mode: bool, arbitrary_code: bool) -> str:

    clear_terminal()

    unit = memory['main']['system']


    if not safe_mode:
        print(render_text('WARN', 'Safe mode is disabled!', False, FM.yellow))
    if arbitrary_code:
        print(render_text('WARN', 'Arbitrary code was run from force_settings.txt', False, FM.yellow))


    match menu:

        case 'invalid':

            print(render_text('ANY', 'Invalid input', True, FM.light_red))
            additional_text: list[str] = ['No additional information'] if memory['invalid']['text'] == '' else memory['invalid']['text'].split('\n')
            for text in additional_text:
                print(render_text('', text, False, FM.light_red))

        case 'fatal_error':

            print(render_text('n', 'AN ERROR OCCURED!', True, FM.red))
            print(render_text('y', 'Attempt to reset memory', False, FM.red))
            additional_text: list[str] = ['No additional information'] if memory['fatal_error']['text'] == '' else memory['fatal_error']['text'].split('\n')
            for text in additional_text:
                print(render_text('', text, False, FM.red))

        case 'success':

            print(render_text('ANY', 'Success', True, FM.light_cyan))
            additional_text: list[str] = ['No additional information'] if memory['success']['text'] == '' else memory['success']['text'].split('\n')
            for text in additional_text:
                print(render_text('', text, False, FM.light_cyan))

        case 'main':

            with open(os.path.join(cwd, 'resources', 'brick_utils_icon.txt'), 'r') as f:
                brick_utils = f.read()

            print(f'{FM.light_blue}{brick_utils}\nVersion {version} by @perru_ for Brick Rigs {br_version} {FM.remove_color}\n')

            print(render_text('0', 'Main menu', True))
            print(render_text('1', 'Brick generator', False))
            print(render_text('2', 'Hollow arc generator (under consideration)', False, FM.light_red))
            print(render_text('3', 'Pixel art importer', False))
            print(render_text('4', 'Lightbar generator', False))
            print(render_text('5', 'Creation editor', False))
            print(render_text('6', 'Rotation rounder (planned)', False, FM.light_red))
            # here menu where you can encrypt / decrypt files
            print(render_text('7', 'Encrypt / Decrypt project', False))
            print(render_text('8', 'Settings', False))
            print(render_text('9', 'Important information', False))

        case 'main/arc':

            pass  # TODO

        case 'main/pixelart':

            key: int = 0

            # Go back to the main menu
            print(render_text(str(key), 'Main menu > Pixel art importer', True)); key += 1

            # Set project
            print(render_text(str(key), f'Selected project: {memory["main/pixelart"]["project"]}', False)); key += 1

            # Set image
            print(render_text(str(key), f'Selected image: {memory["main/pixelart"]["image"]}', False)); key += 1

            # Set import mode
            r_import_mode: str = f'Unknown ({memory["main/pixelart"]["import_mode"]})'
            if memory['main/pixelart']['import_mode'] == 'scalable_rle':
                r_import_mode = 'scalable bricks (using run-length encoding)'
            print(render_text(str(key), f'Import mode (coming soon): {r_import_mode}', False)); key += 1
            # If import mode is scalable_rle
            if memory['main/pixelart']['import_mode'] == 'scalable_rle':

                # Set in-game resolution calculation
                r_ig_calc: str = f'Unknown ({memory["main/pixelart"]["ig_calc"]})'
                if memory['main/pixelart']['ig_calc'] == 'auto_x':
                    r_ig_calc = 'automatically calculate x resolution'
                elif memory['main/pixelart']['ig_calc'] == 'auto_y':
                    r_ig_calc = 'automatically calculate y resolution'
                elif memory['main/pixelart']['ig_calc'] == 'no_auto':
                    r_ig_calc = 'manually set x and y resolution'
                print(render_text(str(key), f'In-game resolution calculation: {r_ig_calc}', False)); key += 1

                # Set resolution x
                print(render_text(str(key), f'In-game resolution X: {memory["main/pixelart"]["ig_res_x"]:,}', False,
                                  FM.light_black if memory['main/pixelart']['ig_calc'] == 'auto_x' else None)); key += 1

                # Set resolution y
                print(render_text(str(key), f'In-game resolution Y: {memory["main/pixelart"]["ig_res_y"]:,}', False,
                                  FM.light_black if memory['main/pixelart']['ig_calc'] == 'auto_y' else None)); key += 1

                # Set number of colors
                print(render_text(str(key), f'Maximum number of colors: {memory["main/pixelart"]["colors"]:,}', False)); key += 1

                # Color picking method
                r_color_method: str = f'Unknown ({memory["main/pixelart"]["color_method"]})'
                if memory['main/pixelart']['color_method'] == 'common':
                    r_color_method = 'pick most common colors'
                elif memory['main/pixelart']['color_method'] == 'random_list':
                    r_color_method = 'pick random pixel\'s color'
                elif memory['main/pixelart']['color_method'] == 'random_set':
                    r_color_method = 'pick random set of color (equal probability for each)'
                print(render_text(str(key), f'Palette colors picking method: {r_color_method}', False)); key += 1

                # Set connections
                r_connections = 'do not connect ' + ', '.join([key for key, item in memory['main/pixelart']['connections'].items() if not item])
                if all(memory['main/pixelart']['connections'].values()):
                    r_connections = 'keep all connections'
                print(render_text(str(key), f'Connections: {r_connections}', False)); key += 1

                # Set scale mode
                r_scale_mode: str = f'Unknown ({memory["main/pixelart"]["scale_mode"]})'
                if memory['main/pixelart']['scale_mode'] == 'pixel':
                    r_scale_mode = 'set pixel size'
                elif memory['main/pixelart']['scale_mode'] == 'image':
                    r_scale_mode = 'set image size'
                elif memory['main/pixelart']['scale_mode'] == 'reference':
                    r_scale_mode = 'calculate size'
                print(render_text(str(key), f'Scale mode: {r_scale_mode}', False)); key += 1
                # If scale mode is depending on pixels
                if memory['main/pixelart']['scale_mode'] == 'pixel':

                    # Set pixel size
                    print(render_text(str(key), f'Pixel scale (x axis): {clen_str(memory["main/pixelart"]["px_scale_x"], unit)}', False)); key += 1

                    # Set pixel size
                    print(render_text(str(key), f'Pixel scale (y axis): {clen_str(memory["main/pixelart"]["px_scale_y"], unit)}', False)); key += 1

                # If scale mode is depending on image size
                elif memory['main/pixelart']['scale_mode'] == 'image':

                    # Set auto calc
                    r_img_scale_calc: str = f'Unknown ({memory["main/pixelart"]["img_scale_calc"]})'
                    if memory['main/pixelart']['img_scale_calc'] == 'auto_x':
                        r_img_scale_calc = 'automatically calculate size on x axis'
                    elif memory['main/pixelart']['img_scale_calc'] == 'auto_y':
                        r_img_scale_calc = 'automatically calculate size on y axis'
                    elif memory['main/pixelart']['img_scale_calc'] == 'no_auto':
                        r_img_scale_calc = 'manually set length and width'
                    print(render_text(str(key), f'Image scale calculation: {r_img_scale_calc}', False)); key += 1

                    # Set image size x
                    print(render_text(str(key), f'Image scale (x axis): {clen_str(memory["main/pixelart"]["img_scale_x"], unit)}', False,
                                      FM.light_black if memory['main/pixelart']['img_scale_calc'] == 'auto_x' else None)); key += 1

                    # Set image size y
                    print(render_text(str(key), f'Image scale (y axis): {clen_str(memory["main/pixelart"]["img_scale_y"], unit)}', False,
                                      FM.light_black if memory['main/pixelart']['img_scale_calc'] == 'auto_y' else None)); key += 1

                # If scale mode is depending on reference
                elif memory['main/pixelart']['scale_mode'] == 'reference':

                    # Set reference px
                    print(render_text(str(key), f'Reference size (on image): {memory["main/pixelart"]["ref_scale_px"]} px', False)); key += 1

                    # Set reference len
                    print(render_text(str(key), f'Reference (true) size: {clen_str(memory["main/pixelart"]["ref_scale_img"], unit)}', False)); key += 1

                # Set pixel thickness
                print(render_text(str(key), f'Pixel thickness: {clen_str(memory["main/pixelart"]["thickness"], unit)}', False)); key += 1

                # Set red color correction
                print(render_text(str(key), f'Red color correction: r = {memory["main/pixelart"]["red_cor"]}', False)); key += 1

                # Set green color correction
                print(render_text(str(key), f'Green color correction: g = {memory["main/pixelart"]["green_cor"]}', False)); key += 1

                # Set blue color correction
                print(render_text(str(key), f'Blue color correction: b = {memory["main/pixelart"]["blue_cor"]}', False)); key += 1

                # Set alpha color correction
                print(render_text(str(key), f'Alpha color correction: a = {memory["main/pixelart"]["alpha_cor"]}', False)); key += 1

                # Set alpha handling
                r_alpha_handling: str = f'Unknown ({memory["main/pixelart"]["alpha_handling"]})'
                if memory["main/pixelart"]["alpha_handling"] == 'ignore':
                    r_alpha_handling = 'ignore alpha'
                elif memory["main/pixelart"]["alpha_handling"] == 'do_not_duplicate_delete':
                    r_alpha_handling = 'add transparency (do not duplicate nor delete)'
                elif memory["main/pixelart"]["alpha_handling"] == 'do_not_duplicate':
                    r_alpha_handling = 'add transparency (do not duplicate bricks)'
                elif memory["main/pixelart"]["alpha_handling"] == 'yes':
                    r_alpha_handling = 'add transparency (duplicating bricks allowed)'
                print(render_text(str(key), f'Alpha handling: {r_alpha_handling}', False)); key += 1

                # Thumbnail setting
                r_thumbnail: str = f'Unknown ({memory["main/pixelart"]["thumbnail"]})'
                if memory["main/pixelart"]["thumbnail"] == 'image':
                    r_thumbnail = 'image'
                elif memory["main/pixelart"]["thumbnail"] == 'brci':
                    r_thumbnail = 'BRCI logo'
                print(render_text(str(key), f'Thumbnail: {r_thumbnail}', False)); key += 1

                # Generate
                print(render_text(str(key), 'Generate pixel art', False)); key += 1

                # Reset menu
                print(render_text(str(key), 'Reset settings', False)); key += 1

        case 'main/pixelart/project':

            print(render_text('', 'Main menu > Pixel art importer > Edit selected project', True))
            print(render_text('ANY', 'Input new project...', False))

        case 'main/pixelart/image':

            print(render_text('', 'Main menu > Pixel art importer > Edit selected image', True))
            print(render_text('', 'Formats known to be supported: .png, .jpeg, .jpg, .webp', False))
            print(render_text('', 'BrickUtils use Pillow; which supports many niche formats such as .im, .xbm, SPIDER, .eps, etc.', False))
            print(render_text('', 'However support for these formats may be limited- insufficient for BrickUtils.', False))
            print(render_text('ANY', 'Input new image (file extension included)...', False))

        case 'main/pixelart/ig_res_x':

            print(render_text('', 'Main menu > Pixel art importer > Edit in-game resolution X', True))
            print(render_text('ANY', 'Input new resolution (x axis)...', False))

        case 'main/pixelart/ig_res_y':

            print(render_text('', 'Main menu > Pixel art importer > Edit in-game resolution Y', True))
            print(render_text('ANY', 'Input new resolution (y axis)...', False))

        case 'main/pixelart/colors':

            print(render_text('', 'Main menu > Pixel art importer > Edit number of colors', True))
            print(render_text('ANY', 'Input new number of colors...', False))

        case 'main/pixelart/connections':

            state_table = [
                f'current: {bool_to_yes_no(memory["main/pixelart"]["connections"]["sides"])}' if memory['main/pixelart/connections']['edited'] == 'sides'
                else f'new: {bool_to_yes_no(memory["main/pixelart/connections"]["new"]["sides"])} / {memory["main/pixelart/connections"]["scores"]["sides"][0]} vs {memory["main/pixelart/connections"]["scores"]["sides"][1]}',

                f'current: {bool_to_yes_no(memory["main/pixelart"]["connections"]["front"])}' if memory['main/pixelart/connections']['edited'] in ['sides', 'front']
                else f'new: {bool_to_yes_no(memory["main/pixelart/connections"]["new"]["front"])} / {memory["main/pixelart/connections"]["scores"]["front"][0]} vs {memory["main/pixelart/connections"]["scores"]["front"][1]}',

                f'current: {bool_to_yes_no(bool_to_yes_no(memory["main/pixelart"]["connections"]["back"]))}' if memory['main/pixelart/connections']['edited'] in ['sides', 'front', 'back']
                else f'new: {bool_to_yes_no(memory["main/pixelart/connections"]["new"]["back"])} / {memory["main/pixelart/connections"]["scores"]["back"][0]} vs {memory["main/pixelart/connections"]["scores"]["back"][1]}'
            ]

            print(render_text('0', 'Main menu > Pixel art importer > Edit connections', True))

            print(render_text('OTHER' if memory['main/pixelart/connections']['edited'] == 'sides' else '',
                              f'Connect sides (input yes / no) ?... ({state_table[0]})',
                              False, None if memory['main/pixelart/connections']['edited'] == 'sides' else FM.light_black))

            print(render_text('OTHER' if memory['main/pixelart/connections']['edited'] == 'front' else '',
                              f'Connect front (input yes / no) ?... ({state_table[1]})',
                              False, None if memory['main/pixelart/connections']['edited'] == 'front' else FM.light_black))

            print(render_text('OTHER' if memory['main/pixelart/connections']['edited'] == 'back' else '',
                              f'Connect back. (input yes / no) ?... ({state_table[2]})',
                              False, None if memory['main/pixelart/connections']['edited'] == 'back' else FM.light_black))

            print(render_text('OTHER' if memory['main/pixelart/connections']['edited'] == 'confirm' else '',
                              f'Confirm connections (input yes / no) ?...',
                              False, None if memory['main/pixelart/connections']['edited'] == 'confirm' else FM.light_black))

        case 'main/pixelart/px_scale_x':

            print(render_text('', 'Main menu > Pixel art importer > Edit pixel scale (x axis)', True))
            print(render_text('ANY', f'Input new pixel scale for the x axis in {get_len_unit(unit, False)}...', False))

        case 'main/pixelart/px_scale_y':

            print(render_text('', 'Main menu > Pixel art importer > Edit pixel scale (y axis)', True))
            print(render_text('ANY', f'Input new pixel scale for the y axis in {get_len_unit(unit, False)}...', False))

        case 'main/pixelart/img_scale_x':

            print(render_text('', 'Main menu > Pixel art importer > Edit image scale (x axis)', True))
            print(render_text('ANY', f'Input new image scale for the x axis in {get_len_unit(unit, False)}...', False))

        case 'main/pixelart/img_scale_y':

            print(render_text('', 'Main menu > Pixel art importer > Edit image scale (y axis)', True))
            print(render_text('ANY', f'Input new image scale for the y axis in {get_len_unit(unit, False)}...', False))

        case 'main/pixelart/ref_scale_px':

            print(render_text('', 'Main menu > Pixel art importer > Edit reference scale', True))
            print(render_text('ANY', f'Input new reference scale in pixels...', False))

        case 'main/pixelart/ref_scale_img':

            print(render_text('', 'Main menu > Pixel art importer > Edit reference scale', True))
            print(render_text('ANY', f'Input new reference scale in {get_len_unit(unit, False)}...', False))

        case 'main/pixelart/thickness':

            print(render_text('', 'Main menu > Pixel art importer > Edit pixel thickness', True))
            print(render_text('ANY', f'Input new thickness in {get_len_unit(unit, False)}...', False))

        case 'main/pixelart/red_cor':

            print(render_text('', 'Main menu > Pixel art importer > Edit red correction', True))
            print(render_text('', 'You may use r, g, b, a variables ranging between 1 and 0', False))
            print(render_text('', 'Math module is imported. You may use functions like math.log(a, 2)', False))
            print(render_text('', 'Documentation: https://docs.python.org/3.12/library/math.html', False))
            print(render_text('', 'Warning: this setting use eval(), which is capable of running arbitrary code.', False))
            print(render_text('ANY', f'Input new red correction formula (recommended: r ** 2.2)...', False))

        case 'main/pixelart/green_cor':

            print(render_text('', 'Main menu > Pixel art importer > Edit green correction', True))
            print(render_text('', 'You may use r, g, b, a variables ranging between 1 and 0', False))
            print(render_text('', 'Math module is imported. You may use functions like math.log(a, 2)', False))
            print(render_text('', 'Documentation: https://docs.python.org/3.12/library/math.html', False))
            print(render_text('', 'Warning: this setting use eval(), which is capable of running arbitrary code.', False))
            print(render_text('ANY', f'Input new green correction formula (recommended: g ** 2.2)...', False))

        case 'main/pixelart/blue_cor':

            print(render_text('', 'Main menu > Pixel art importer > Edit blue correction', True))
            print(render_text('', 'You may use r, g, b, a variables ranging between 1 and 0', False))
            print(render_text('', 'Math module is imported. You may use functions like math.log(a, 2)', False))
            print(render_text('', 'Documentation: https://docs.python.org/3.12/library/math.html', False))
            print(render_text('', 'Warning: this setting use eval(), which is capable of running arbitrary code.', False))
            print(render_text('ANY', f'Input new blue correction formula (recommended: b ** 2.2)...', False))

        case 'main/pixelart/alpha_cor':

            print(render_text('', 'Main menu > Pixel art importer > Edit alpha correction', True))
            print(render_text('', 'You may use r, g, b, a variables ranging between 1 and 0', False))
            print(render_text('', 'Math module is imported. You may use functions like math.log(a, 2)', False))
            print(render_text('', 'Documentation: https://docs.python.org/3.12/library/math.html', False))
            print(render_text('', 'Warning: this setting use eval(), which is capable of running arbitrary code.', False))
            print(render_text('ANY', f'Input new alpha correction formula (recommended: a)...', False))

        case 'main/settings':

            print(render_text('0', 'Main menu > Settings', True))

            if memory['main/settings']['new_main']['port'] == [True, True]:
                r_porting_mode: str = 'update new and edited creations'
            elif memory['main/settings']['new_main']['port'] == [True, False]:
                r_porting_mode: str = 'update new creations only'
            elif memory['main/settings']['new_main']['port'] == [False, True]:
                r_porting_mode: str = 'update edited creations only'
            else:  # if memory['main/settings']['new_main']['port'] == [False, True]
                r_porting_mode: str = 'do not update any creation'

            r_backup = f'Unknown ({memory["main"]["backup"]})'
            if memory['main/settings']['new_main']['backup'] == [True, True]:
                r_backup = 'backup creations stored in projects and Brick Rigs'
            elif memory['main/settings']['new_main']['backup'] == [True, False]:
                r_backup = 'backup creations stored in projects only (not recommended!)'
            elif memory['main/settings']['new_main']['backup'] == [False, True]:
                r_backup = 'backup creations stored in Brick Rigs only'
            elif memory['main/settings']['new_main']['backup'] == [False, True]:
                r_backup = 'do not backup any creation (not recommended!)'

            if memory['main/settings']['new_main']['system'] == 'cgs':
                r_system = 'cgs (centimeter-gram-second) system'
            elif memory['main/settings']['new_main']['system'] == 'si':
                r_system = 'si system (système international)'
            elif memory['main/settings']['new_main']['system'] == 'imperial':
                r_system = 'imperial system'
            elif memory['main/settings']['new_main']['system'] == 'scal':
                r_system = 'scalable bricks / si system'
            else: # if memory['main/settings']['new_main']['system'] == 'stud' # secret system for peculiar applications
                r_system = f'"{memory["main/settings"]["new_main"]["system"]}" system'

            print(render_text('1', f'Porting mode: {r_porting_mode}', False))
            print(render_text('2', f'Backup mode: {r_backup}', False))
            print(render_text('3', f'Backup limit: {memory['main/settings']['new_main']["backup_limit"]}', False,
                  FM.light_black if memory['main/settings']['new_main']["backup"] == [False, False] else None))
            print(render_text('4', 'Open backup & brick rigs folders', False))
            print(render_text('5', f'Unit system: {r_system}', False))
            print(render_text('6', 'Cancel', False))
            print(render_text('7', 'Apply without saving', False))
            print(render_text('8', 'Apply and save', False))

        case 'main/settings/backup_limit':

            print(render_text('0', 'Main menu > Settings > Backup limit', True))
            print(render_text('OTHER', f'Input new backup limit...', False))

        case 'main/edit':

            key = 0

            print(render_text(str(key), 'Main menu > Creation editor', True)); key += 1  # Exit

            print(render_text(str(key), f'Project: {memory["main/edit"]["project"]}', False)); key += 1

            print(render_text(str(key), f'Move: {bool_to_yes_no(memory["main/edit"]["move"])}', False)); key += 1
            if memory["main/edit"]["move"]:

                print(render_text(str(key), f'Offset on the x axis: {clen_str(memory["main/edit"]["off_x"], unit)}', False)); key += 1

                print(render_text(str(key), f'Offset on the y axis: {clen_str(memory["main/edit"]["off_y"], unit)}', False)); key += 1

                print(render_text(str(key), f'Offset on the z axis: {clen_str(memory["main/edit"]["off_z"], unit)}', False)); key += 1

            print(render_text(str(key), f'Scale: {bool_to_yes_no(memory["main/edit"]["scale"])}', False)); key += 1
            if memory["main/edit"]["scale"]:

                print(render_text(str(key), f'Scale on the x axis: {str(memory["main/edit"]["scale_x"])}', False)); key += 1

                print(render_text(str(key), f'Scale on the y axis: {str(memory["main/edit"]["scale_y"])}', False)); key += 1

                print(render_text(str(key), f'Scale on the z axis: {str(memory["main/edit"]["scale_z"])}', False)); key += 1

                r_adapt_connections = f'Unknown ({memory["main/edit"]["adapt_connections"]})'
                if memory["main/edit"]["adapt_connections"] == 'no':
                    r_adapt_connections = 'do not modify'
                elif memory["main/edit"]["adapt_connections"] == 'delete':
                    r_adapt_connections = 'delete all connections'
                elif memory["main/edit"]["adapt_connections"] == 'yes':
                    r_adapt_connections = 'try to scale connections'
                print(render_text(str(key), f'Adapt connections: {r_adapt_connections}', False)); key += 1

                print(render_text(str(key), f'Scale relevant non-size related properties: {bool_to_yes_no(memory["main/edit"]["scale_extras"])}', False)); key += 1

            print(render_text('WARN', 'Rotation is not working correctly. That\'s why it\'s in red.', False, FM.yellow))

            print(render_text(str(key), f'Rotate: {bool_to_yes_no(memory["main/edit"]["rotate"])}', False, FM.light_red)); key += 1
            if memory["main/edit"]["rotate"]:

                print(render_text(str(key), f'Rotation on the x axis: {memory["main/edit"]["rot_x"]}°', False, FM.light_red)); key += 1

                print(render_text(str(key), f'Rotation on the y axis: {memory["main/edit"]["rot_y"]}°', False, FM.light_red)); key += 1

                print(render_text(str(key), f'Rotation on the z axis: {memory["main/edit"]["rot_z"]}°', False, FM.light_red)); key += 1

            print(render_text(str(key), f'Delete duplicated bricks: {bool_to_yes_no(memory["main/edit"]["clear_duplicates"])}', False)); key += 1

            print(render_text(str(key), 'Generate modified creation', False)); key += 1

        case 'main/edit/off_x':

            print(render_text('', 'Main menu > Creation editor > Offset on the x axis', True))
            print(render_text('ANY', f'Input new offset on the x axis in {get_len_unit(unit, False, True)}...', False))

        case 'main/edit/off_y':

            print(render_text('', 'Main menu > Creation editor > Offset on the y axis', True))
            print(render_text('ANY', f'Input new offset on the y axis in {get_len_unit(unit, False, True)}...', False))

        case 'main/edit/off_z':

            print(render_text('', 'Main menu > Creation editor > Offset on the z axis', True))
            print(render_text('ANY', f'Input new offset on the z axis in {get_len_unit(unit, False, True)}...', False))

        case 'main/edit/scale_x':

            print(render_text('', 'Main menu > Creation editor > Scale on the x axis', True))
            print(render_text('ANY', f'Input new scale on the x axis...', False))

        case 'main/edit/scale_y':

            print(render_text('', 'Main menu > Creation editor > Scale on the y axis', True))
            print(render_text('ANY', f'Input new scale on the y axis...', False))

        case 'main/edit/scale_z':

            print(render_text('', 'Main menu > Creation editor > Scale on the z axis', True))
            print(render_text('ANY', f'Input new scale on the z axis...', False))

        case 'main/edit/rot_x':

            print(render_text('', 'Main menu > Creation editor > Rotation on the x axis', True))
            print(render_text('ANY', f'Input new rotation on the x axis in degree(s)...', False))

        case 'main/edit/rot_y':

            print(render_text('', 'Main menu > Creation editor > Rotation on the y axis', True))
            print(render_text('ANY', f'Input new rotation on the y axis in degree(s)...', False))

        case 'main/edit/rot_z':

            print(render_text('', 'Main menu > Creation editor > Rotation on the z axis', True))
            print(render_text('ANY', f'Input new rotation on the z axis in degree(s)...', False))

        case 'main/edit/project':

            print(render_text('', 'Main menu > Creation editor > Project name', True))
            print(render_text('ANY', f'Input new project name...', False))

        case 'main/brick':

            print(render_text('0', 'Main menu > Brick generator', True))
            print(render_text('1', f'Selected project: {memory["main/brick"]["project"]}', False))
            print(render_text('2', f'Selected brick: {memory["main/brick"]["brick"]}', False))
            print(render_text('3', 'Edit properties...', False))
            print(render_text('4', 'Generate brick', False))

        case 'main/brick/project':

            print(render_text('', 'Main menu > Brick generator > Project name', True))
            print(render_text('ANY', f'Input new project name...', False))

        case 'main/brick/select_brick':

            print(render_text('0', 'Main menu > Brick generator > Select brick', True))
            print(render_text('1', f'Search: {memory["main/brick/select_brick"]["search"]}', False))
            if len(memory['main/brick/select_brick']['matches']) == 0:
                print(render_text('', 'No matches.', False))
            for i, match in enumerate(memory['main/brick/select_brick']['matches']):
                print(render_text(f'{i + 2}', match, False))

        case 'main/brick/select_brick/search':

            print(render_text('0', 'Main menu > Brick generator > Select brick > Search', True))
            print(render_text('', 'Will search for every brick with all given keywords (separated with space).', False))
            print(render_text('', 'Ignores case. Example: "scal cone" returns all scalable cones.', False))
            print(render_text("all", 'Return all bricks', False))
            print(render_text('OTHER', f'Input new search...', False))

        case 'main/brick/properties':

            key = 0

            print(render_text(str(key), 'Main menu > Brick generator > Edit properties', True)); key += 1

            print(render_text(str(key), f'Advanced mode: {bool_to_yes_no(memory["main/brick/properties"]["advanced"])}', False)); key += 1

            if len(memory['main/brick']['properties']) == 0:
                print(render_text('', 'Select a brick.', False)); key += 1

            properties = deepcopy(memory['main/brick']['properties'])

            if memory['main/brick/properties']['advanced']:

                print(render_text('', f'Warning: advanced mode use eval(); which is capable of running arbitrary code.', False))

            else:
                properties.pop('gbn')
                properties.pop('Position')
                properties.pop('Rotation')

            for prop, val in properties.items():
                print(render_text(str(key), f'{prop}: {repr(val)}', False)); key += 1


        case 'main/brick/properties/advanced_required':

            print(render_text('ANY', f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/advanced_required"]["property"]}', True))
            print(render_text('', 'Advanced mode is required to edit this property.', False))


        case 'main/brick/properties/color':

            alpha_text = ' '
            alpha_initial = ''
            if memory['main/brick/properties/color']['alpha']:
                alpha_text = ', alpha (%) '
                alpha_initial = 'A'

            if memory['main/brick/properties/color']['mode'] == 'select_color_space':

                print(render_text('0', f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/color"]["property"]} > Select color', True))
                print(render_text('1', f'Use HSV{alpha_initial} color space', False))
                print(render_text('2', f'Use HSL{alpha_initial} color space', False))
                print(render_text('3', f'Use RGB{alpha_initial} color space / hex', False))
                print(render_text('4', f'Use CMYK{alpha_initial} color space', False))

                return ''

            elif memory['main/brick/properties/color']['mode'] == 'hsva':

                print(render_text('0', f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/color"]["property"]} > Set HSV{alpha_initial} color', True))
                print(render_text('OTHER', f'Input hue (degrees), saturation (%), value (%){alpha_text}separated by a comma...', False))

            elif memory['main/brick/properties/color']['mode'] == 'hsla':

                print(render_text('0', f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/color"]["property"]} > Set HSL{alpha_initial} color', True))
                print(render_text('OTHER', f'Input hue (degrees), saturation (%), lightness (%){alpha_text}separated by a comma...', False))

            elif memory['main/brick/properties/color']['mode'] == 'rgba':

                print(render_text('0', f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/color"]["property"]} > Set RGB{alpha_initial} color', True))
                print(render_text('OTHER', f'Input red (0-255), green (0-255), blue (0-255){alpha_text}separated by a comma or # followed by a hex code...', False))

            elif memory['main/brick/properties/color']['mode'] == 'cmyka':

                print(render_text('0', f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/color"]["property"]} > Set CMYK{alpha_initial} color', True))
                print(render_text('OTHER', f'Input cyan (%), magenta (%), yellow (%), key (aka black) (%){alpha_text}separated by a comma...', False))

        case 'main/brick/properties/choice':

            key = 0

            print(render_text(str(key), f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/choice"]["property"]}', True)); key += 1

            for choice in memory['main/brick/properties/choice']['options']:

                print(render_text(str(key), repr(choice), False)); key += 1


        case 'main/brick/properties/connector':

            print(render_text('0', f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/connector"]["property"]}', True))

            print(render_text('', 'You may be here trying to get smaller connections. You cannot: smaller connections could not be saved in the BRV.', False))

            for i in range(6):

                print(render_text(str(i+1), f'{str_int_dir(i)} axis connector: {str_connector(memory["main/brick"]['properties'][memory['main/brick/properties/connector']['property']][i])}', False))



        case 'main/brick/properties/float':

            print(render_text('', f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/float"]["property"]}', True))

            dist_text = ''
            if memory['main/brick/properties/float']['distance'] is not None:
                dist_text = f'(in {get_len_unit(memory['main']['system'], False, True)}) '

            print(render_text('ANY', f'Input a number {dist_text}or, -inf, inf, nan...', False))


        case 'main/brick/properties/int':

            print(render_text('', f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/int"]["property"]}', True))

            print(render_text('ANY', 'Input an integer...', False))


        case 'main/brick/properties/list':

            print(render_text('', f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/list"]["property"]}', True))

            str_unit = f'(in {get_len_unit(memory['main']['system'], False, True)}) '

            lim: list[str] = [str(x) for x in memory['main/brick/properties/list']['len']]
            print(render_text('ANY', f'Input {'either ' if len(lim) >= 2 else ''}{','.join(lim)} values {str_unit}separated by commas{' or None' if memory['main/brick/properties/list']['accepts_none'] else ''}...', False))


        case 'main/brick/properties/strany':

            print(render_text('', f'Main menu > Brick generator > Edit properties > Edit {memory['main/brick/properties/list']['property']}', True))

            print(render_text('', 'You may use \\r\\n to create a new line. Limit: 32767 characters.', False))

            print(render_text('ANY', 'Input text...', False))


        case 'main/brick/properties/eval':

            print(render_text('', f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/eval"]["property"]} (Advanced mode)', True))
            print(render_text('', 'WARNING: You\'re using advanced mode; which is capable of running arbitrary code.', False))
            print(render_text('', 'Available: prev (previous value), math module, BrickInput.', False))
            print(render_text('', 'Only the first two arguments of BrickInput are required. The third one won\'t do anything.', False))
            print(render_text('', 'Brick name (May be useful for brick inputs): \'brick\'', False))
            print(render_text('ANY', 'Input new value...', False))

        case 'main/help':

            print(render_text('0', 'Main menu > Important information', True))
            print(render_text('1', f'Language: {memory["main/help"]["lang"]}', False))
            if memory["main/help"]["lang"] == 'english (english)':
                print(render_text('', 'Python and Pillow is required to fully use BrickUtils.', False))
                print(render_text('', 'BrickUtils do not support os other than Windows.', False))
                print(render_text('', 'Using another operating system may result in errors or data loss.', False))
                print(render_text('', 'Backups are available to revert any data loss. You can access the backup folder in the settings.', False))
                print(render_text('', 'Generation / Edition may be slow if BrickUtils is attempting to backup too many files.', False))
                print(render_text('', 'If backups are disabled, consider disabling porting to prevent data loss.', False))
                print(render_text('', 'We recommend you adjusting backup limit accordingly in settings to avoid wasting disk space.', False))
                print(render_text('', 'BrickUtils is on GitHub only to distribute it\'s code. We will not accept contributions.', False))
                print(render_text('', 'REMINDER: As expressed in the GPL-3.0 license, BrickUtils is provided "as is".', False))
                print(render_text('', 'We are therefore not liable for any damage caused by the use of BrickUtils.', False))
                print(render_text('', 'If you\'re having issues:', False))
                print(render_text('', '1. Make sure you comply with all requirements then restart BrickUtils', False))
                print(render_text('', '2. Reinstall BrickUtils; making sure you\'re using the latest version', False))
                print(render_text('', '3. Contact @perru_ on discord and describe your issue. We will try to resolve it as soon as possible.', False))
            elif memory["main/help"]["lang"] == 'français (french)':
                print(render_text('', 'NOTE: L\'intégralité de BrickUtils à l\'exception de ce menu est en anglais.', False))
                print(render_text('', 'Python et Pillow sont nécéssaires pour utiliser pleinement BrickUtils.', False))
                print(render_text('', 'BrickUtils ne prend pas en charge les systèmes d\'exploitation autres que Windows.', False))
                print(render_text('', 'L\'utilisation d\'un autre système d\'exploitation peut entraîner des erreurs ou une perte de données.', False))

                print(render_text('', 'Des sauvegardes sont disponibles pour rétablir toute perte de données.', False))
                print(render_text('', 'Vous pouvez accéder au dossier de sauvegarde dans les paramètres.', False))

                print(render_text('', 'La génération/l\'édition peut être lente si BrickUtils tente de sauvegarder trop de fichiers.', False))
                print(render_text('', 'Si les sauvegardes sont désactivées, envisagez de désactiver le portage pour éviter la perte de données.', False))
                print(render_text('', 'Veuillez ajuster la limite de sauvegarde dans les paramètres pour ne pas gaspiller de l\'espace disque.', False))
                print(render_text('', 'BrickUtils est sur GitHub uniquement pour distribuer son code. Nous n\'accepterons pas les contributions.', False))
                print(render_text('', 'RAPPEL : Conformément à la licence GPL-3.0, BrickUtils est fourni "as is" ("tel quel").', False))
                print(render_text('', 'Nous ne sommes donc pas responsables des dommages causés par l\'utilisation de BrickUtils.', False))
                print(render_text('', 'Si vous rencontrez des problèmes :', False))
                print(render_text('', '1. Assurez-vous de respecter toutes les exigences, puis redémarrez BrickUtils.', False))
                print(render_text('', '2. Réinstallez BrickUtils en vous assurant d\'utiliser la dernière version.', False))
                print(render_text('', '3. Contactez @perru_ sur Discord et décrivez votre problème. Nous essaierons de le résoudre rapidement.', False))
            elif memory['main/help']['lang'] == 'русский (russian)':
                print(render_text('', 'NOTE: Этот текст был переведен с помощью искусственного интеллекта.', False))
                print(render_text('', 'NOTE: Весь Brickutils, за исключением этого меню, на английском языке.', False))
                print(render_text('', 'Для полноценного использования BrickUtils требуется Python и Pillow.', False))
                print(render_text('', 'BrickUtils не поддерживает операционные системы, отличные от Windows.', False))
                print(render_text('', 'Использование другой операционной системы может привести к ошибкам или потере данных.', False))
                print(render_text('', 'Для восстановления потерянных данных доступны резервные копии.', False))
                print(render_text('', 'Вы можете получить доступ к папке с резервными копиями в настройках.', False))
                print(render_text('', 'Генерация/редактирование может быть медленным, если BrickUtils пытается сохранить слишком много файлов.', False))
                print(render_text('', 'Если отключены резервные копии, рассмотрите отключение портирования, чтобы избежать потери данных.', False))
                print(render_text('', 'Пожалуйста, настройте лимит резервного копирования в настройках, чтобы не занимать место на диске.', False))
                print(render_text('', 'BrickUtils находится на GitHub только для распространения своего кода. Мы не принимаем вклады.', False))
                print(render_text('', 'НАПОМИНАНИЕ: Согласно лицензии GPL-3.0, BrickUtils предоставляется "как есть".', False))
                print(render_text('', 'Следовательно, мы не несем ответственности за ущерб, причиненный использованием BrickUtils.', False))
                print(render_text('', 'Если у вас возникли проблемы:', False))
                print(render_text('', '1. Убедитесь, что вы выполнили все требования, затем перезапустите BrickUtils.', False))
                print(render_text('', '2. Переустановите BrickUtils, убедившись, что вы используете последнюю версию.', False))
                print(render_text('', '3. Свяжитесь с @perru_ на Discord и опишите свою проблему. Мы постараемся решить ее быстро.', False))
            elif memory['main/help']['lang'] == 'deutsch (german)':
                print(render_text('', 'HINWEIS: Dieser Text wurde mithilfe künstlicher Intelligenz übersetzt.', False))
                print(render_text('', 'HINWEIS: Der gesamte Inhalt von Brickutils, mit Ausnahme dieses Menüs, ist in Englisch.', False))
                print(render_text('', 'Python und Pillow sind erforderlich, um BrickUtils vollständig nutzen zu können.', False))
                print(render_text('', 'BrickUtils unterstützt keine Betriebssysteme außer Windows.', False))
                print(render_text('', 'Die Verwendung eines anderen Betriebssystems kann zu Fehlern oder Datenverlust führen.', False))
                print(render_text('', 'Backups sind verfügbar, um Datenverluste wiederherzustellen.', False))
                print(render_text('', 'Sie können auf den Backup-Ordner in den Einstellungen zugreifen.', False))
                print(render_text('', 'Die Generierung/Bearbeitung kann langsam sein, wenn BrickUtils versucht, zu viele Dateien zu sichern.', False))
                print(render_text('', 'Wenn Backups deaktiviert sind, sollten Sie das Portieren deaktivieren, um Datenverluste zu vermeiden.', False))
                print(render_text('', 'Bitte passen Sie die Backup-Grenze in den Einstellungen an, um Speicherplatz zu sparen.', False))
                print(render_text('', 'BrickUtils ist auf GitHub nur zur Verbreitung des Codes verfügbar. Wir akzeptieren keine Beiträge.', False))
                print(render_text('', 'ERINNERUNG: Gemäß der GPL-3.0-Lizenz wird BrickUtils "wie es ist" bereitgestellt.', False))
                print(render_text('', 'Wir übernehmen keine Verantwortung für Schäden durch die Verwendung von BrickUtils.', False))
                print(render_text('', 'Wenn Sie Probleme haben:', False))
                print(render_text('', '1. Stellen Sie sicher, dass Sie alle Anforderungen erfüllen, und starten Sie dann BrickUtils neu.', False))
                print(render_text('', '2. Installieren Sie BrickUtils neu und verwenden Sie die neueste Version.', False))
                print(render_text('', 'Kontaktieren Sie @perru_ auf Discord und beschreiben Ihr Problem. Wir werden es schnell lösen.', False))
            elif memory['main/help']['lang'] == 'español (spanish)':
                print(render_text('', 'NOTA: Este texto ha sido traducido con inteligencia artificial', False))
                print(render_text('', 'NOTA: Todo BrickUtils, excepto este menú, está en inglés.', False))
                print(render_text('', 'Python y Pillow son necesarios para utilizar completamente BrickUtils.', False))
                print(render_text('', 'BrickUtils no es compatible con sistemas operativos que no sean Windows.', False))
                print(render_text('', 'El uso de otro sistema operativo puede provocar errores o pérdida de datos.', False))
                print(render_text('', 'Puede acceder a la carpeta de respaldo en la configuración.', False))
                print(render_text('', 'Hay copias de seguridad disponibles para restaurar cualquier pérdida de datos.', False))
                print(render_text('', 'La generación/edición puede ser lenta si BrickUtils respalda demasiados archivos.', False))
                print(render_text('', 'Si las copias de seguridad están desactivadas, desactive el portado para evitar pérdida de datos.', False))
                print(render_text('', 'Ajuste el límite de respaldo en la configuración para no desperdiciar espacio en disco.', False))
                print(render_text('', 'BrickUtils está en GitHub solo para distribuir su código. No aceptaremos contribuciones.', False))
                print(render_text('', 'RECORDATORIO: Según la licencia GPL-3.0, BrickUtils se proporciona "as is" ("tal cual").', False))
                print(render_text('', 'Por lo tanto, no somos responsables de los daños causados por el uso de BrickUtils.', False))
                print(render_text('', 'Si tiene problemas:', False))
                print(render_text('', '1. Asegúrese de cumplir con todos los requisitos y luego reinicie BrickUtils.', False))
                print(render_text('', '2. Vuelva a instalar BrickUtils asegurándose de usar la última versión.', False))
                print(render_text('', '3. Contacte a @perru_ en Discord y describa su problema. Intentaremos resolverlo rápido.', False))


        case 'main/lightbar':

            key: int = 0

            print(render_text(str(key), 'Main menu > Lightbar generator', True)); key += 1

            print(render_text('WARN', 'Generation is not available yet. You may export it, to import and generate it in a later version.', False, FM.yellow))

            print(render_text(str(key), f'Project: {memory['main/lightbar']['project']}', False)); key += 1

            # Debug render test
            """
            new_layout = []
            import random
            for _ in range(50):
                # new_layout.append({'col': [random.randint(0, 255) for _ in range(4)], 'brightness': 0.5, 'material': 'Glass'})
                new_layout.append({'col': [random.randint(0, 255), 255 - int(random.uniform(0, 1) ** 2.2 * 255), random.randint(0, 255), random.randint(0, 255)], 'brightness': 0.5, 'material': 'Glass'})
            memory['main/lightbar']['layout'] = new_layout
            """
            print(render_text(str(key), f'Lightbar layout: {render_lightbar(memory['main/lightbar']['layout'])}', False)); key += 1

            print(render_text(str(key), 'Add a new stage', False)); key += 1
            if len(memory['main/lightbar']['lightbar']) > 0:
                last_stage = memory['main/lightbar']['lightbar'][-1]
                print(render_text(str(key), f'Remove last stage (Stage {str(len(memory['main/lightbar']['lightbar'])).zfill(2)} "{last_stage["name"]}" ({round(last_stage['loops']*last_stage['layer_duration']*len(last_stage['layers'])*1000):,}ms))', False)); key += 1
            else:
                print(render_text(str(key), f'Remove last stage (No stage found)', False, FM.light_black)); key += 1

            for i, stage in enumerate(memory['main/lightbar']['lightbar']):
                stage = memory['main/lightbar']['lightbar'][i]
                print(render_text(str(key), f'Stage {str(i+1).zfill(2)} "{stage['name']}" ({round(stage['loops']*stage['layer_duration']*len(stage['layers'])*1000):,}ms)', False)); key += 1

            print(render_text(str(key), 'Export lightbar', False)); key += 1
            print(render_text(str(key), 'Import lightbar (from lightbar.json)', False)); key += 1
            print(render_text(str(key), 'Import lightbar from..', False)); key += 1
            print(render_text(str(key), 'Preview', False)); key += 1
            print(render_text(str(key), 'Generate lightbar', False, FM.light_black)); key += 1


        case 'main/lightbar/project':

            print(render_text('', 'Main menu > Lightbar generator > Edit selected project', True))
            print(render_text('ANY', 'Input new project name...', False))


        case 'main/lightbar/layout':

            print(render_text('0', 'Main menu > Lightbar generator > Edit layout', True))
            print(render_text('SELEC', render_lightbar(memory['main/lightbar']['layout'], zfill_override=True, sel=memory['main/lightbar/layout']['selected'], space=True), False))

            key = len(memory['main/lightbar']['layout']) + 1
            sel = memory['main/lightbar/layout']['selected']
            sel_b = memory['main/lightbar']['layout'][sel]
            ccode = f'H{sel_b['col'][0]/255*360:.1f}°, S{sel_b['col'][1]/255*100:.1f}%, V{sel_b['col'][2]/255*100:.1f}%, A{sel_b['col'][3]/255*100:.1f}%'

            print(render_text(str(key), f'Selected light color: {ccode}', False)); key += 1
            print(render_text(str(key), f'Selected light brightness: {sel_b['brightness']*100}%', False)); key += 1
            print(render_text(str(key), f'Selected light material: {sel_b['material']}', False)); key += 1

            del_col = None if len(memory['main/lightbar']['layout']) > 1 else FM.light_black
            print(render_text(str(key), f'Delete selected light brick', False, del_col)); key += 1

            add_col = None if len(memory['main/lightbar']['layout']) < 99 else FM.light_black
            print(render_text(str(key), f'Insert new light to the right', False, add_col)); key += 1
            print(render_text(str(key), f'Duplicate selected light', False, add_col)); key += 1


        case 'main/lightbar/layout/color':

            alpha_text = ' '
            alpha_initial = ''
            if memory['main/lightbar/layout/color']['alpha']:
                alpha_text = ', alpha (%) '
                alpha_initial = 'A'

            if memory['main/lightbar/layout/color']['mode'] == 'select_color_space':

                print(render_text('0', f'Main menu > Lightbar generator > Edit layout > Edit color > Select color', True))
                print(render_text('1', f'Use HSV{alpha_initial} color space', False))
                print(render_text('2', f'Use HSL{alpha_initial} color space', False))
                print(render_text('3', f'Use RGB{alpha_initial} color space / hex', False))
                print(render_text('4', f'Use CMYK{alpha_initial} color space', False))

                return ''

            elif memory['main/lightbar/layout/color']['mode'] == 'hsva':

                print(render_text('0', f'Main menu > Lightbar generator > Edit layout > Edit color > Set HSV{alpha_initial} color', True))
                print(render_text('OTHER', f'Input hue (degrees), saturation (%), value (%){alpha_text}separated by a comma...', False))

            elif memory['main/lightbar/layout/color']['mode'] == 'hsla':

                print(render_text('0', f'Main menu > Lightbar generator > Edit layout > Edit color > Set HSL{alpha_initial} color', True))
                print(render_text('OTHER', f'Input hue (degrees), saturation (%), lightness (%){alpha_text}separated by a comma...', False))

            elif memory['main/lightbar/layout/color']['mode'] == 'rgba':

                print(render_text('0', f'Main menu > Lightbar generator > Edit layout > Edit color > Set RGB{alpha_initial} color', True))
                print(render_text('OTHER', f'Input red (0-255), green (0-255), blue (0-255){alpha_text}separated by a comma or # followed by a hex code...', False))

            elif memory['main/lightbar/layout/color']['mode'] == 'cmyka':

                print(render_text('0', f'Main menu > Lightbar generator > Edit layout > Edit color > Set CMYK{alpha_initial} color', True))
                print(render_text('OTHER', f'Input cyan (%), magenta (%), yellow (%), key (aka black) (%){alpha_text}separated by a comma...', False))

        case 'main/lightbar/layout/brightness':

            print(render_text('', f'Main menu > Lightbar generator > Edit layout > Edit brightness', True))
            print(render_text('ANY', f'Input new brightness (include percentage sign to input a value in percents)...', False))

        case 'main/lightbar/layout/material':

            print(render_text('0', f'Main menu > Lightbar generator > Edit layout > Edit material', True))

            print(render_text('1', f'Glass', False))
            print(render_text('2', f'CloudyGlass', False))
            print(render_text('3', f'Glow', False))
            print(render_text('4', f'LEDMatrix', False))

        case 'main/lightbar/stage':

            stage_id = memory['main/lightbar/stage']['selected']
            stage = memory['main/lightbar']['lightbar'][stage_id]
            stage_id_str = str(stage_id + 1).zfill(2)

            key = 0

            print(render_text(str(key), f'Main menu > Lightbar generator > Edit stage {stage_id_str} "{stage['name']}"', True)); key += 1

            print(render_text(str(key), f'Name: {stage["name"]}', False)); key += 1
            print(render_text('', f'Total duration: {round(stage['layer_duration']*stage['loops']*len(stage['layers'])*1000)}ms', False))
            print(render_text(str(key), f'Layer duration: {round(stage['layer_duration']*1000)}ms', False)); key += 1
            print(render_text(str(key), f'Loops: {stage["loops"]}', False)); key += 1

            new_layer_info, new_layer_col = '', None
            if len(stage['layers']) >= 99:
                new_layer_info, new_layer_col = ' (layer limit reached)', FM.light_black
            print(render_text(str(key), f'Add new layer{new_layer_info}', False, new_layer_col)); key += 1

            print(render_text(str(key), f'Remove last layer' if len(stage['layers']) > 1 else 'Disable all bricks', False)); key += 1

            print(render_text('', f'How to edit stages: Input layer\'s id followed by a slash then the brick\'s id. e.g. 2/5', False))

            super_key = 1
            color_char_table = get_r_lightbar_colors(memory['main/lightbar']['layout'])

            for layer in stage['layers']:

                print(render_text(f'{super_key}/', ' '.join([f'{FM.reverse if layer[i] else ''}{col}{str(i+1).zfill(2)}{FM.reset}' for i, col in enumerate(color_char_table)]), False)); super_key += 1

        case 'main/lightbar/stage/name':

            stage_id = memory['main/lightbar/stage']['selected']
            stage = memory['main/lightbar']['lightbar'][stage_id]
            stage_id_str = str(stage_id + 1).zfill(2)

            print(render_text('', f'Main menu > Lightbar generator > Edit stage {stage_id_str} "{stage["name"]}" > Edit name', True))
            print(render_text('ANY', f'Input new name...', False))

        case 'main/lightbar/stage/layer_duration':

            stage_id = memory['main/lightbar/stage']['selected']
            stage = memory['main/lightbar']['lightbar'][stage_id]
            stage_id_str = str(stage_id + 1).zfill(2)

            print(render_text('0', f'Main menu > Lightbar generator > Edit stage {stage_id_str} "{stage["name"]}" > Edit layer duration', True))
            print(render_text('OTHER', f'Input new layer duration (in milliseconds)...', False))

        case 'main/lightbar/stage/loops':

            stage_id = memory['main/lightbar/stage']['selected']
            stage = memory['main/lightbar']['lightbar'][stage_id]
            stage_id_str = str(stage_id + 1).zfill(2)

            print(render_text('0', f'Main menu > Lightbar generator > Edit stage {stage_id_str} "{stage["name"]}" > Edit loops', True))
            print(render_text('OTHER', f'Input new number of loops...', False))

        case 'main/lightbar/import_from':

            print(render_text('', 'Main menu > Lightbar generator > Import from', True))
            print(render_text('OTHER', 'Input file name (with extension)...', False))

        case 'main/encrypt':

            print(render_text('0', 'Main menu > Encrypt / Decrypt project', True))
            print(render_text('1', f'Project: {memory['main/encrypt']['project']}', False))



            pw = memory['main/encrypt']['password']
            password = pw

            pass_key, pass_msg = 'ANY', 'Hide password'
            if not memory['main/encrypt']['see_password']:
                password = '*' * len(password)
                pass_key, pass_msg = '3', 'See password'

            excess_password = max(0, (len(password) - 80))
            if excess_password > 0:
                excess = excess_password + 3
                password_end = password[-10:]
                password = password[:- (10 + excess)]
                password += f'{FM.light_black}...{FM.remove_color}{password_end} {FM.light_black}({len(pw)})'

            print(render_text('2', f'Password: {password}', False))

            password_strength: int = 0
            if len(pw) > 11: password_strength += 1  # If long
            if len(pw) > 31: password_strength += 1  # If very long
            if len(pw) > 127: password_strength += 1  # If extremely long
            if pw.lower() != pw: password_strength += 1  # If caps in password
            if re.search(r'\d', pw): password_strength += 1  # If numbers in password
            if re.search(r'\W', pw): password_strength += 1  # If special chars in password
            info = ''
            if password_strength == 0: info = 'Insufficient'
            elif password_strength == 1: info = 'Very weak'
            elif password_strength == 2: info = 'Weak'
            elif password_strength == 3: info = 'Mild'
            elif password_strength == 4: info = 'Fairly strong'
            elif password_strength == 5: info = 'Extremely strong'
            else: info = 'Practically invulnerable'

            print(render_text('', f'Password strength: {password_strength}/6 ({info})', False))
            print(render_text(pass_key, pass_msg, False))
            memory['main/encrypt']['see_password'] = False


            print(render_text('4', 'Generate a safe password', False))
            print(render_text('5', 'BrickUtils\' encryption method is not flawless. Learn more...', False))
            print(render_text('6', 'Encrypt vehicle', False))
            print(render_text('7', 'Decrypt vehicle', False))

        case 'main/encrypt/project':

            print(render_text('', 'Main menu > Encrypt / Decrypt project > Edit selected project', True))
            print(render_text('ANY', 'Input new project name...', False))

        case 'main/encrypt/password':

            if not memory['main/encrypt/password']['repeat']:
                print(render_text('', 'Main menu > Encrypt / Decrypt project > Edit password', True))
                print(render_text('ANY', 'Input new password...', False))
            else:
                print(render_text('NPREV', 'Main menu > Encrypt / Decrypt project > Edit password', True))
                print(render_text('OTHER', 'Input new password again...', False))

        case 'main/encrypt/generate':

            pw = memory['main/encrypt/generate']['password']
            password = pw

            excess_password = max(0, (len(password) - 80))
            if excess_password > 0:
                excess = excess_password + 3
                password_end = password[-10:]
                password = password[:- (10 + excess)]
                password += f'{FM.light_black}...{FM.remove_color}{password_end} {FM.light_black}({len(pw)})'


            print(render_text('0', 'Main menu > Encrypt / Decrypt project > Generate password', True))
            print(render_text('', f'Suggested: {password}', False))
            print(render_text('1', 'Use and copy to clipboard', False))
            print(render_text('2', 'Copy to clipboard', False))

        case 'main/encrypt/info':

            print(render_text('0', 'Main menu > Encrypt / Decrypt project > Learn more', True))
            print(render_text('', 'Do not use it to encrypt high risk files.. or nuclear codes.', False))
            print(render_text('', 'How to make your password safer:', False))
            print(render_text('', 'Make your password extremely long, use caps, numbers and special characters', False))
            print(render_text('', 'The password must be unique. Do not reuse it for another file.', False))

