import os
from brci import FM, deepcopy
from data import version, br_version, get_len_unit, clen_str, str_connector, str_int_dir


cwd = os.path.dirname(os.path.realpath(__file__))


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


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


def render_menu(menu: str, memory: dict[str, any]) -> str:

    clear_terminal()

    unit = memory['main']['system']
    match menu:

        case 'invalid':

            print(render_text('ANY', 'Invalid input', True, FM.light_red))
            additional_text: list[str] = ['No additional information'] if memory['invalid']['text'] == '' else memory['invalid']['text'].split('\n')
            for text in additional_text:
                print(render_text('', text, False, FM.light_red))

        case 'fatal_error':

            print(render_text('n', 'AN ERROR OCCURED!', True, FM.red))
            additional_text: list[str] = ['No additional information'] if memory['fatal_error']['text'] == '' else memory['fatal_error']['text'].split('\n')
            for text in additional_text:
                print(render_text('', text, False, FM.red))

        case 'success':

            print(render_text('ANY', 'Generation successful', True, FM.light_cyan))
            additional_text: list[str] = ['No additional information'] if memory['success']['text'] == '' else memory['success']['text'].split('\n')
            for text in additional_text:
                print(render_text('', text, False, FM.light_cyan))

        case 'main':

            with open(os.path.join(cwd, 'resources', 'brick_utils_icon.txt'), 'r') as f:
                brick_utils = f.read()

            print(f'{FM.light_blue}{brick_utils}\nVersion {version} by @perru_ for Brick Rigs {br_version} {FM.remove_color}\n')

            print(render_text('0', 'Main menu', True))
            print(render_text('1', 'Brick generator', False))
            print(render_text('2', 'Hollow arc generator', False, FM.light_red))
            print(render_text('3', 'Pixel art importer', False))
            print(render_text('4', 'Creation editor', False))
            print(render_text('5', 'Rotation rounder', False, FM.light_red))
            print(render_text('6', 'Settings', False))
            print(render_text('7', 'Important information', False))

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
            else: # if memory['main/settings']['new_main']['system'] == 'scal':
                r_system = 'scalable bricks / si system'

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

            print(render_text(str(key), f'Rotate: {bool_to_yes_no(memory["main/edit"]["rotate"])}', False, FM.light_red)); key += 1
            if memory["main/edit"]["rotate"]:

                print(render_text(str(key), f'Rotation on the x axis: {memory["main/edit"]["rot_x"]}°', False, FM.light_red)); key += 1

                print(render_text(str(key), f'Rotation on the y axis: {memory["main/edit"]["rot_y"]}°', False, FM.light_red)); key += 1

                print(render_text(str(key), f'Rotation on the z axis: {memory["main/edit"]["rot_z"]}°', False, FM.light_red)); key += 1

            print(render_text(str(key), f'Delete duplicated bricks: {bool_to_yes_no(memory["main/edit"]["clear_duplicates"])}', False)); key += 1

            print(render_text(str(key), 'Generate modififed creation', False)); key += 1

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

            print(render_text('0', 'Main menu > Brick generator > Project name', True))
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

            alpha_text = ''
            alpha_initial = ''
            if memory['main/brick/properties/color']['alpha']:
                alpha_text = ', alpha (%) '
                alpha_initial = 'A'

            if memory['main/brick/properties/color']['mode'] == 'select_color_space':

                print(render_text('0', 'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/color"]["property"]} > Select color', True))
                print(render_text('1', f'Use HSV{alpha_initial} color space', False))
                print(render_text('2', f'Use HSL{alpha_initial} color space', False))
                print(render_text('3', f'Use RGB{alpha_initial} color space / hex', False))
                print(render_text('4', f'Use CMYK{alpha_initial} color space', False))

                return

            elif memory['main/brick/properties/color']['mode'] == 'hsva':

                print(render_text('0', f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/color"]["property"]} > Set HSV{alpha_initial} color', True))
                print(render_text('OTHER', f'Input hue (degrees), saturation (%), value (%){alpha_text} separated by a comma...', False))

            elif memory['main/brick/properties/color']['mode'] == 'hsla':

                print(render_text('0', f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/color"]["property"]} > Set HSL{alpha_initial} color', True))
                print(render_text('OTHER', f'Input hue (degrees), saturation (%), lightness (%){alpha_text} separated by a comma...', False))

            elif memory['main/brick/properties/color']['mode'] == 'rgba':

                print(render_text('0', f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/color"]["property"]} > Set RGB{alpha_initial} color', True))
                print(render_text('OTHER', 'fInput red (0-255), green (0-255), blue (0-255){alpha_text} separated by a comma or # followed by a hex code...', False))

            elif memory['main/brick/properties/color']['mode'] == 'cmyka':

                print(render_text('0', f'Main menu > Brick generator > Edit properties > Edit {memory["main/brick/properties/color"]["property"]} > Set CMYK{alpha_initial} color', True))
                print(render_text('OTHER', f'Input cyan (%), magenta (%), yellow (%), key (aka black) (%){alpha_text} separated by a comma...', False))

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
