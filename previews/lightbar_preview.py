import msvcrt


def main():

    import os
    import sys
    import time
    # Change cwd to the same as main.py
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    # Since we changed cwd this is no longer considered as a parent package and therefore can be imported
    from brci import FM
    from data import load_json, get_r_lightbar_colors



    def get_full_watermark(watermark: str, project_name: str):

        return f'{FM.light_blue}{watermark}\nLightbar preview (\'{project_name}\') {FM.reset}\n'


    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')


    def key_pressed():
        return msvcrt.kbhit()


    def get_key():
        key = msvcrt.getch()
        return key


    preview_dir = os.path.dirname(os.path.realpath(__file__))
    utils_dir = os.path.dirname(preview_dir)
    resources_dir = os.path.join(utils_dir, 'resources')

    with open(os.path.join(resources_dir, 'brick_utils_icon.txt'), 'r') as f:
        brick_utils_watermark = f.read()

    # Loading everything
    memory = load_json(os.path.join(preview_dir, 'lightbar.json'))

    color_char_table = get_r_lightbar_colors(memory['main/lightbar']['layout'])

    lightbar_duration: float = 0
    speed: float = 1
    for stage in memory['main/lightbar']['lightbar']:
        lightbar_duration += stage['layer_duration']*stage['loops']*len(stage['layers'])

    while True:

        for stage in memory['main/lightbar']['lightbar']:

            stage_duration = stage['layer_duration']*stage['loops']*len(stage['layers'])
            loop_duration = stage['layer_duration']*len(stage['layers'])
            layer_duration = stage['layer_duration']

            for loop in range(stage['loops']):

                for layer_index, layer in enumerate(stage['layers']):

                    print(get_full_watermark(brick_utils_watermark, memory['main/lightbar']['project']))
                    print(f'{stage['name']} > Loop {loop + 1}/{stage['loops']} > Layer {layer_index + 1}/{len(stage["layers"])}\n')

                    print(' '.join([f'{FM.reverse if layer[i] else ''}{col}{str(i+1).zfill(2)}{FM.reset}' for i, col in enumerate(color_char_table)]))

                    print('\n\n', end='')

                    print(f'Lightbar duration: RT: {round(lightbar_duration*1000)}ms / SIM: {round(lightbar_duration*1000/speed)}ms')
                    print(f'Stage duration: RT: {round(stage_duration*1000)}ms / SIM: {round(stage_duration*1000/speed)}ms')
                    print(f'Loop duration: RT: {round(loop_duration*1000)}ms / SIM: {round(loop_duration*1000/speed)}ms')
                    print(f'Layer duration: RT: {round(layer_duration*1000)}ms / SIM: {round(layer_duration*1000/speed)}ms')

                    print("""
KEYBINDS:
┌───────┬───────┬───────┬───────┬───────┬───────┬───────┬───────┬───────┬───────┬───────┐
│ SPEED │ -100% │ -30%  │ -10%  │ -3%   │ -1%   │ +1%   │ +3%   │ +10%  │ +30%  │ +100% │
├───────┼───────┼───────┼───────┼───────┼───────┼───────┼───────┼───────┼───────┼───────┤
│ KEY   │ 1     │ 2     │ 3     │ 4     │ 5     │ 6     │ 7     │ 8     │ 9     │ 0     │
└───────┴───────┴───────┴───────┴───────┴───────┴───────┴───────┴───────┴───────┴───────┘""")
                    additional_info = ''
                    if speed == 0.1: additional_info = ' (minimum)'
                    elif speed == 1: additional_info = ' (real-time)'
                    elif speed == 10: additional_info = ' (maximum)'
                    print(f'Speed: {speed*100:,.0f}%{additional_info}')

                    if key_pressed():

                        key = get_key()

                        if key in [b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'0']:
                            int_key = int(key.decode('utf-8'))
                            if int_key == 1:
                                speed -= 1
                            elif int_key == 2:
                                speed -= 0.3
                            elif int_key == 3:
                                speed -= 0.1
                            elif int_key == 4:
                                speed -= 0.03
                            elif int_key == 5:
                                speed -= 0.01
                            elif int_key == 6:
                                speed += 0.01
                            elif int_key == 7:
                                speed += 0.03
                            elif int_key == 8:
                                speed += 0.1
                            elif int_key == 9:
                                speed += 0.3
                            elif int_key == 0:
                                speed += 1

                            if speed < 0.1: speed = 0.1
                            if speed > 10: speed = 10

                    time.sleep(layer_duration / speed)
                    clear_terminal()


try:
    main()
except Exception as e:
    red_col = '\x1b[31m'
    input(f'{red_col}PREVIEW FAILED! AN UNEXPECTED ERROR OCCURED:\n{type(e).__name__}: {e}')