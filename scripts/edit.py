import os
import brci
import math
from data import cwd, version, generate_backup, clen_str, clamp
from copy import deepcopy


def edit(data: dict[str, any], unit: str, port: bool, backup_mode: list[bool], limit: int) -> (bool, str):

    projects_folder_path = os.path.join(cwd, 'projects')
    if not os.path.exists(projects_folder_path):
        return False, 'important folders are missing. Please reinstall BrickUtils.'
    project_path = os.path.join(projects_folder_path, data['project'])
    if not os.path.exists(project_path):
        return False, f'project \'{data["project"]}\' was not found.'

    if not os.path.exists(os.path.join(project_path, 'Vehicle.brv')):
        return False, 'vehicle.brv file was not found.'


    creation = brci.BRCI()
    creation.project_folder_directory = projects_folder_path
    creation.project_name = data['project']
    creation.project_display_name = f'{data['project']} (modified)'
    creation.custom_description_watermark = f'Modified using BrickUtils {version} by @perru_'
    creation.description = f'Project name: {data['project']}\n'

    move_display: str = 'no'
    if data['move'] is not None:
        move_display = (f'yes (X: {clen_str(data['move'][0], unit)}, '
                        f'Y: {clen_str(data['move'][1], unit)}, '
                        f'Z: {clen_str(data['move'][2], unit)})')
    creation.description += f'Move: {move_display}\n'

    if data['rotate'] is None:
        creation.description += 'Rotate: no\n'
    else:
        creation.description += (f'Rotate around: '
                                 f'X: {clen_str(data['rotate'][1][0], unit)}, '
                                 f'Y: {clen_str(data['rotate'][1][1], unit)}, '
                                 f'Z: {clen_str(data['rotate'][1][2], unit)}\n')
        creation.description += (f'Rotate by: '
                                 f'X: {data['rotate'][0][0]:.2f}°, '
                                 f'Y: {data['rotate'][0][1]:.2f}°, '
                                 f'Z: {data['rotate'][0][2]:.2f}°\n')
        creation.description += (f'Allow rotation to go out of -180° to 180° range: '
                                 f'{'yes' if data['allow_out_of_range_rotation'] else 'no'}\n')

    if data['scale'] is None:
        creation.description += 'Scale: no\n'
    else:
        creation.description += f'Scale: x{data['scale']}'

    try:
        creation.load_brv(True, False, False)
    except Exception as e:
        return False, f'An unexpected error occured whilst trying to load the vehicle.\n({type(e).__name__}: {e})'

    bricks = creation.get_all_bricks()
    new_bricks = []

    # I know I could just make creation.bricks a set then a list again but whatever.
    known_bricks: set = set()

    for i, brick in enumerate(bricks):

        if data['duplicates'] == 'delete identical':

            if brick[1] in known_bricks:
                continue
            # else:
            known_bricks.add(brick[1])

        if data['rotate'] is not None:

            brick[1]['Position'] = brci.rotate_point_3d(brick[1]['Position'], data['rotate'][1], data['rotate'][0])
            brick[1]['Rotation'] = list(map(lambda x, y: x+y, brick[1]["Rotation"], data['rotate'][0]))

        if not data['allow_out_of_range_rotation']:

            brick[1]['Rotation'] = [(axis_rot + 180) %360 - 180 for axis_rot in brick[1]['Rotation']]

        if not data["connections"]["sides"] and 'ConnectorSpacing' in brick[1]:
            brick[1]['ConnectorSpacing'][0] = 0
            brick[1]['ConnectorSpacing'][1] = 0
            brick[1]['ConnectorSpacing'][2] = 0
            brick[1]['ConnectorSpacing'][3] = 0

        if not data["connections"]['top'] and 'ConnectorSpacing' in brick[1]:
            brick[1]['ConnectorSpacing'][4] = 0

        if not data["connections"]['bottom'] and 'ConnectorSpacing' in brick[1]:
            brick[1]['ConnectorSpacing'][5] = 0

        if data['scale'] is not None:

            for prop, val in brick[1].items():

                if prop == 'Position':
                    val = [axis_pos * data['scale'] for axis_pos in val]

                elif prop == 'BrickSize':
                    val = [axis_size * data['scale'] for axis_size in val]

                elif prop == 'ExitLocation' and val is not None:
                    val = [axis_pos * data['scale'] for axis_pos in val]

                elif prop in ['Brightness', 'FontSize', 'InputScale', 'SuspensionLength',
                              'TireThickness', 'WheelDiameter', 'WheelWidth', 'WinchSpeed']:
                    val *= data['scale']

                elif prop == 'GearRatioScale':
                    val /= data['scale']

                brick[1][prop] = val

            if data['move'] is not None:

                brick[1]['Position'] = [axis_pos + axis_move for axis_pos, axis_move in zip(brick[1]['Position'], data['move'])]

        to_mod: dict = {}

        for prop, val in brick[1].items():

            if isinstance(val, brci.BrickInput) and val.brick_input_type == 'Custom' and val.brick_input is not None:
                to_mod |= {prop: brci.BrickInput('Custom', [str(ab) for ab in val.brick_input])}

            elif prop in brci.br_property_types.keys():

                if brci.br_property_types[prop] == 'brick_id':
                    to_mod |= {prop: str(val)}

                elif brci.br_property_types[prop] == 'list[brick_id]':
                    to_mod |= {prop: [str(ab) for ab in val]}

        brick[1] |= deepcopy(to_mod)


        brick[0] = str(brick[0] + 1) # If + 1: KeyError("9") else KeyError("'739'") (brick count). WHY IS IT A STR AND AN INT WHEN I DID EVERYTHING TO PREVENT THAT?
        new_bricks.append(deepcopy(brick))

    creation.bricks = new_bricks

    generate_backup(creation, backup_mode, limit)

    creation.write_brv()
    creation.write_metadata()
    if not os.path.exists(os.path.join(project_path, 'Preview.png')):
        creation.write_preview()

    if port:
        creation.write_to_br()

    return True, ''