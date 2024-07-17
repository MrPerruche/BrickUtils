import msvcrt
from math import floor


def main():

    from math import floor
    import msvcrt
    import os
    import sys
    import time
    # Change cwd to the same as main.py
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    # Since we changed cwd this is no longer considered as a parent package and therefore can be imported
    from brci import FM
    from data import load_json, get_r_lightbar_colors, clamp
    from render_menu import render_text



    def get_full_watermark(watermark: str, project_name: str):

        return f'{FM.light_blue}{watermark}\nLightbar preview (\'{project_name}\') {FM.reset}\n'


    def clear_terminal():
        # os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[H\033[J", end='')


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

    if len(memory['main/lightbar']['lightbar']) < 1:
        print(render_text('ANY', 'Invalid lightbar', True, FM.light_red))
        print(render_text('', 'No stages are defined.', False, FM.light_red))
        input('> ')
        exit(0)

    color_char_table = get_r_lightbar_colors(memory['main/lightbar']['layout'])

    stages_duration: list[float] = []
    speed = prev_speed = 1
    minimalist_mode: bool = False
    for stage in memory['main/lightbar']['lightbar']:
        stages_duration.append(stage['layer_duration']*stage['loops']*len(stage['layers']))
    lightbar_duration = sum(stages_duration)

    start_time = current_time = time.perf_counter()
    last_update_time = time.perf_counter()

    prev_iter_path: list[int] = [-1, -1, -1]

    if len(stages_duration) < 1:
        print(render_text('ANY', 'Invalid lightbar', True, FM.light_red))
        print(render_text('', 'No stages are defined.', False, FM.light_red))

    while True:

        passed_time = time.perf_counter() - last_update_time
        last_update_time = time.perf_counter()
        current_time += passed_time * speed
        local_time = (current_time - start_time) % lightbar_duration

        # Find in which stage we're in
        current_stage_index: int = 0
        csi_spent_time: float = 0
        for stage in stages_duration:
            if csi_spent_time + stages_duration[current_stage_index] >= local_time:
                break
            current_stage_index += 1
            csi_spent_time += stage

        # Find in which loop we're in
        current_loop_time: float = local_time - csi_spent_time
        loops: int = memory['main/lightbar']['lightbar'][current_stage_index]['loops']
        current_loop_index: int = floor((current_loop_time / stages_duration[current_stage_index]) * loops)

        # Find in which layer we're in
        current_layer_time: float = current_loop_time % (stages_duration[current_stage_index] / loops)
        layers: int = len(memory['main/lightbar']['lightbar'][current_stage_index]['layers'])
        loop_duration: float = stages_duration[current_stage_index] / loops
        layer_duration = loop_duration / layers
        current_layer_index: int = floor(current_layer_time / layer_duration)

        if prev_iter_path != [current_stage_index, current_loop_index, current_layer_index] or prev_speed != speed:

            clear_terminal()

            prev_iter_path = [current_stage_index, current_loop_index, current_layer_index]
            prev_speed = speed

            if not minimalist_mode:

                print(get_full_watermark(brick_utils_watermark, memory['main/lightbar']['project']))

                prev_iter_path = [current_stage_index, current_loop_index, current_layer_index]
                prev_speed = speed

                print(render_text('', f'Main menu > Lightbar generator > Preview of "{memory['main/lightbar']['project']}"', True))
                stage_name: str = memory['main/lightbar']['lightbar'][current_stage_index]['name']
                print(render_text('', f'Stage: {stage_name} ({current_stage_index+1}/{len(memory['main/lightbar']['lightbar'])}) > Loop {current_loop_index+1}/{loops} > Layer {current_layer_index+1}/{layers}', True))

                print(render_text('', '', False))

                lb_layer = memory['main/lightbar']['lightbar'][current_stage_index]['layers'][current_layer_index]
                print(render_text('', ' ' + ' '.join([f'{FM.reverse if lb_layer[i] else ''}{col}{str(i+1).zfill(2)}{FM.reset}' for i, col in enumerate(color_char_table)]), False))

                print(render_text('', '', False))
                print(render_text('', 'You are not required to press enter in this menu.', False))
                print(render_text('', f'Speed: {speed*100:,.1f}%', False))
                if not -10_000_000 < speed < 10_000_000:
                    print(render_text('WARN', 'This high speeds may break preview by making regular speeds run simulation too slow stop.', False, FM.yellow))
                print(render_text('0', 'Toggle reverse', False))
                print(render_text('1', 'Decrease speed by 10%', False))
                print(render_text('2', 'Increase speed by 10%', False))
                print(render_text('SELEC', '3 → 5%, 4 → 30%, 5 → 100%, 6 → 300%, 7 → 2,500%', False))
                print(render_text('9', 'Minimalist mode (renders better higher speeds)', False))
                print(render_text('', '', False))
                print(render_text('', f'Lightbar duration: {lightbar_duration*1000:,.1f}ms RT / {lightbar_duration*1000/speed:,.1f}ms SIM', False))
                print(render_text('', f'Stage duration: {stages_duration[current_stage_index]*1000:,.1f}ms RT / {stages_duration[current_stage_index]*1000/speed:,.1f}ms SIM', False))
                print(render_text('', f'Loop duration: {loop_duration*1000:,.1f}ms RT / {loop_duration*1000/speed:,.1f}ms SIM', False))
                print(render_text('', f'Layer duration: {layer_duration*1000:,.1f}ms RT / {layer_duration*1000/speed:,.1f}ms SIM', False))

            else:

                lb_layer = memory['main/lightbar']['lightbar'][current_stage_index]['layers'][current_layer_index]
                print(''.join([f'{FM.reverse if lb_layer[i] else ''}{col}{str(i+1).zfill(2)}{FM.reset}' for i, col in enumerate(color_char_table)]))
                print('9= +INFO')



        if key_pressed():
            key = get_key()
            if key == b'0':
                speed *= -1
            elif key == b'1':
                speed /= 1.1
            elif key == b'2':
                speed *= 1.1
            elif key == b'3':
                speed = 0.05
            elif key == b'4':
                speed = 0.3
            elif key == b'5':
                speed = 1
            elif key == b'6':
                speed = 3
            elif key == b'7':
                speed = 25
            elif key == b'9':
                minimalist_mode = not minimalist_mode









    """
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

                    print(
KEYBINDS:
┌───────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
│ SPEED │ 10%  │ 25%  │ 50%  │ 75%  │ 100% │ 150% │ 200% │ 300% │ 500% │ 2k % │
├───────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ KEY   │ 1    │ 2    │ 3    │ 4    │ 5    │ 6    │ 7    │ 8    │ 9    │ 0    │
└───────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘)
                    additional_info = ''
                    if speed == 0.1: additional_info = ' (minimum)'
                    elif speed == 1: additional_info = ' (real-time)'
                    elif speed == 20: additional_info = ' (maximum)'
                    print(f'Speed: {speed*100:,.0f}%{additional_info}')

                    if key_pressed():

                        key = get_key()

                        if key in [b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'0']:
                            int_key = int(key.decode('utf-8'))
                            if int_key == 1:
                                speed = 0.1
                            elif int_key == 2:
                                speed = 0.25
                            elif int_key == 3:
                                speed = 0.5
                            elif int_key == 4:
                                speed = 0.75
                            elif int_key == 5:
                                speed = 1
                            elif int_key == 6:
                                speed = 1.5
                            elif int_key == 7:
                                speed = 2
                            elif int_key == 8:
                                speed = 3
                            elif int_key == 9:
                                speed = 5
                            elif int_key == 0:
                                speed = 20

                    time.sleep(layer_duration / speed)
                    clear_terminal()
    """


try:
    main()
except Exception as e:
    red_col = '\x1b[31m'
    input(f'{red_col}PREVIEW FAILED! AN UNEXPECTED ERROR OCCURED:\n{type(e).__name__}: {e}')