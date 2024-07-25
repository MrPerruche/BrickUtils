from data import cwd, version
import brci
import os
import math


def pos(x: float, y: float, z: float):
    return [x*10, y*10, z*10]


# Can lead to crashes
F32_MAX: float = 3.4028234663852886e+38
F32_MIN: float = -3.4028234663852886e+38

# Safe values
SF32_MAX: float = 1_000_000_000.0
SF32_MIN: float = -1_000_000_000.0


def next_after(val: float, rep: int = 2, precision: str = 'float') -> float:
    exp = math.log2(val)
    if precision == 'float':
        return val + (2 ** (exp - 23) * rep)
    elif precision == 'double':
        return val + (2 ** (exp - 52) * rep)
    else:
        raise ValueError("Invalid precision")


def generate(data: dict[str, any], port: bool, backup_mode: list[bool], limit: int) -> (bool, str):

    # Verifying files
    projects_folder_path = os.path.join(cwd, 'projects')
    if not os.path.exists(projects_folder_path):
        return False, 'important folders are missing. Please reinstall BrickUtils.'

    current_project_path = os.path.join(projects_folder_path, data['project'])


    # Setup BRCI
    creation: brci.BRCI = brci.BRCI()
    creation.project_folder_directory = projects_folder_path
    creation.project_name = data['project']
    creation.project_display_name = f'{data['project']} ({data['file_name']})'
    creation.custom_description_watermark = f'Generated with BrickUtils {version}'

    stages_duration: list[float] = []
    for stage in data['lightbar']:
        stages_duration.append(stage['layer_duration']*stage['loops']*len(stage['layers']))
    lightbar_duration = sum(stages_duration)

    creation.file_description = f'''Lightbar duration: {round(lightbar_duration * 1_000)}ms
Stages:
{'- ' + '- '.join([f'{stage["name"]} ({round(stages_duration[i]*1000)}ms, {stage["loops"]}x, {len(stage["layers"])} layer(s))\n' for i, stage in enumerate(data['lightbar'])])}
'''

    creation.anb('total_time', 'Sensor_1sx1sx1s', {
        'SensorType': 'Time',
        'OutputChannel.MinIn': 0,
        'OutputChannel.MaxIn': SF32_MAX,
        'OutputChannel.MinOut': 0,
        'OutputChannel.MaxOut': SF32_MAX
    }, pos(0, 0, 0))

    creation.anb('current_time', 'MathBrick_1sx1sx1s', {
        'Operation': 'Fmod',
        'InputChannelA': brci.BrickInput('Custom', ['total_time']),
        'InputChannelB': brci.BrickInput('AlwaysOn', lightbar_duration)
    }, pos(1, 0, 0))

    creation.anb('enabled_len', 'Switch_1sx1sx1s', {
        'OutputChannel.MinIn': 0,
        'OutputChannel.MaxIn': 1,
        'OutputChannel.MinOut': 0,
        'OutputChannel.MaxOut': lightbar_duration,
        'InputChannel': brci.BrickInput('Beacon', None)
    }, pos(2, 0, 0))

    min_i: int = 0
    max_i: int = len(data['lightbar']) - 1
    stage_start_time: float = 0

    in_stage: list[str | list[str]] = []

    for i, stage in enumerate(data['lightbar']):

        stage_end_time = stage_start_time + stages_duration[i]

        if min_i == i:
            in_stage.append([f'sc_{i}_1', f'sc_{i}_2'])
            creation.anb(f'sc_{i}_2', 'Switch_1sx1sx1s', {
                'OutputChannel.MinIn': lightbar_duration,
                'OutputChannel.MaxIn': next_after(lightbar_duration),
                'OutputChannel.MinOut': 0,
                'OutputChannel.MaxOut': 1,
                'InputChannel': brci.BrickInput('Custom', ['current_time', 'enabled_len'])
            }, pos(i+4, 0, 0))
            creation.anb(f'sc_{i}_2', 'Switch_1sx1sx1s', {
                'OutputChannel.MinIn': lightbar_duration + stage_end_time,
                'OutputChannel.MaxIn': next_after(lightbar_duration + stage_end_time),
                'OutputChannel.MinOut': 0,
                'OutputChannel.MaxOut': -1,
                'InputChannel': brci.BrickInput('Custom', ['current_time', 'enabled_len'])
            }, pos(i+4, 1, 0))

        elif max_i == i:
            in_stage.append([f'sc_{i}_1'])
            creation.anb(f'sc_{i}_1', 'Switch_1sx1sx1s', {
                'OutputChannel.MinIn': lightbar_duration + stage_start_time,
                'OutputChannel.MaxIn': next_after(lightbar_duration + stage_start_time),
                'OutputChannel.MinOut': 0,
                'OutputChannel.MaxOut': 1,
                'InputChannel': brci.BrickInput('Custom', ['current_time', 'enabled_len'])
            }, pos(i+4, 0, 0))

        else:
            in_stage.append([f'sc_{i}_1', f'sc_{i}_2'])
            creation.anb(f'sc_{i}_1', 'Switch_1sx1sx1s', {
                'OutputChannel.MinIn': lightbar_duration + stage_start_time,
                'OutputChannel.MaxIn': next_after(lightbar_duration + stage_start_time),
                'OutputChannel.MinOut': 0,
                'OutputChannel.MaxOut': 1,
                'InputChannel': brci.BrickInput('Custom', ['current_time', 'enabled_len'])
            }, pos(i+4, 0, 0))
            creation.anb(f'sc_{i}_2', 'Switch_1sx1sx1s', {
                'OutputChannel.MinIn': lightbar_duration + stage_end_time,
                'OutputChannel.MaxIn': next_after(lightbar_duration + stage_end_time),
                'OutputChannel.MinOut': 0,
                'OutputChannel.MaxOut': -1,
                'InputChannel': brci.BrickInput('Custom', ['current_time', 'enabled_len'])
            }, pos(i+4, 1, 0))

        stage_start_time = stage_end_time


        # layers
        creation.anb(f's{i}_time', 'Sensor_1sx1sx1s', {
            'OutputChannel.MinIn': 0,
            'OutputChannel.MaxIn': SF32_MAX,
            'OutputChannel.MinOut': 0,
            'OutputChannel.MaxOut': SF32_MAX,
            'EnabledInputChannel': brci.BrickInput('Custom', in_stage[i]),
            'SensorType': 'Time',
            'bReturnToZero': True
        }, pos(i, 3, 0))

        creation.anb(f'l{i}_time', 'MathBrick_1sx1sx1s', {
            'Operation': 'Fmod',
            'InputChannelA': brci.BrickInput('Custom', [f's{i}_time']),
            'InputChannelB': brci.BrickInput('AlwaysOn', stages_duration[i] / stage['loops'])
        }, pos(i, 4, 0))

        creation.anb(f'lay{i}_time', 'Switch_1sx1sx1s', {
            'OutputChannel.MinIn': 0,
            'OutputChannel.MaxIn': SF32_MAX,
            'OutputChannel.MinOut': 0,
            'OutputChannel.MaxOut': SF32_MAX / len(stage['layers']),
            'InputChannel': brci.BrickInput('Custom', [f'l{i}_time']),
            'bReturnToZero': True
        }, pos(i, 5, 0))


    # END






    return True, ''