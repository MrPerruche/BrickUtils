import os
import brci
import math
from data import cwd, version, generate_backup, clen_str, clamp


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
    creation.description = f'Project name: {data['project']}\r\nMove: {
        f'x: {clen_str(data['off_x'], unit)}, y: {clen_str(data['off_y'], unit)}, z: {clen_str(data['off_z'], unit)}' if data['move'] else 'no'
    }\r\nScale: {
        f'x: {float(data["scale_x"])}, y: {float(data["scale_y"])}, z: {float(data["scale_z"])}' if data['scale'] else 'no'
    }\r\nRotate: {
        f'x: {float(data["rot_x"])}°, y: {float(data["rot_y"])}°, z: {float(data["rot_z"])}°' if data['rotate'] else 'no'
    }'

    try:
        creation.load_brv(True, False, False)
    except Exception as e:
        return False, f'An unexpected error occured whilst trying to load the vehicle.\n({type(e).__name__}: {e})'

    bricks = creation.get_all_bricks()
    new_bricks = []

    for i, brick in enumerate(bricks):

        if data['rotate']:  # TODO

            rot_x = math.radians(data['rot_x'])  # Convert degrees to radians
            rot_y = math.radians(data['rot_y'])
            rot_z = math.radians(data['rot_z'])

            # Original position vector
            pos = brick[1]['Position']

            # Applying the rotations to the position
            rotated_pos = [
                pos[0] * math.cos(rot_z) - pos[1] * math.sin(rot_z),
                pos[0] * math.sin(rot_z) + pos[1] * math.cos(rot_z),
                pos[2],
            ]
            rotated_pos = [
                rotated_pos[0] * math.cos(rot_y) - rotated_pos[1] * math.sin(rot_y),
                rotated_pos[0] * math.sin(rot_y) + rotated_pos[1] * math.cos(rot_y),
                rotated_pos[2] + pos[0] * math.sin(rot_y) * math.sin(rot_z) - pos[1] * math.cos(rot_y) * math.sin(rot_z),
            ]
            rotated_pos = [
                rotated_pos[0] * math.cos(rot_x) - rotated_pos[1] * math.sin(rot_x),
                rotated_pos[0] * math.sin(rot_x) + rotated_pos[1] * math.cos(rot_x),
                rotated_pos[2],
            ]

            # Update the position in the brick dictionary
            brick[1]['Position'] = rotated_pos

            # Assuming the original rotation is given in degrees and needs to be converted to radians
            brick[1]['Rotation'][0] += data['rot_x']
            brick[1]['Rotation'][1] += data['rot_y']
            brick[1]['Rotation'][2] += data['rot_z']


        if data['move']:

            brick[1]['Position'][0] += data['off_x']
            brick[1]['Position'][1] += data['off_y']
            brick[1]['Position'][2] += data['off_z']

        if data['scale']:

            for prop, val in brick[1].items():

                if prop == 'Position':

                    val[0] *= data['scale_x']
                    val[1] *= data['scale_y']
                    val[2] *= data['scale_z']

                elif prop == 'BrickSize':

                    val[0] *= data['scale_x']
                    val[1] *= data['scale_y']
                    val[2] *= data['scale_z']

                elif prop == 'ConnectorSpacing' and data["adapt_connections"] == 'yes':

                    new_val: list[int] = []

                    for i, connection in enumerate(val):

                        if connection != 0:
                            new_val[i] = int(clamp(1, round(connection / data['scale_x']), 3))

                    val = new_val.copy()

                elif prop == 'ConnectorSpacing' and data["adapt_connections"] == 'delete':

                    val = [0, 0, 0, 0, 0, 0]

                elif prop == 'ExitLocation' and val is not None:

                    val[0] *= data['scale_x']
                    val[1] *= data['scale_y']
                    val[2] *= data['scale_z']

                elif prop == 'FontSize':

                    # Determine if we use scale x, y, or z depending on it's angle
                    # Idk if it works; written by ai.
                    if abs(data['rot_x']) > abs(data['rot_y']) and abs(data['rot_x']) > abs(data['rot_z']):
                        val *= data['scale_x']

                    elif abs(data['rot_y']) > abs(data['rot_x']) and abs(data['rot_y']) > abs(data['rot_z']):
                        val *= data['scale_y']

                    else:
                        val *= data['scale_z']

                elif prop == 'GearRatioScale':

                    val *= (data['scale_x'] + data['scale_y'] + data['scale_z']) / 3

                elif prop == 'ImageScale':

                    val *= min(data['scale_x'], data['scale_y'], data['scale_z'])

                elif prop == 'MinLimit':

                    # Determine if we use scale x, y, z depending on it's angle
                    # Idk if it works; written by ai.
                    if abs(data['rot_x']) > abs(data['rot_y']) and abs(data['rot_x']) > abs(data['rot_z']):
                        val *= data['scale_x']

                    elif abs(data['rot_y']) > abs(data['rot_x']) and abs(data['rot_y']) > abs(data['rot_z']):
                        val *= data['scale_y']

                    else:
                        val *= data['scale_z']

                elif prop == 'MaxLimit':

                    # Determine if we use scale x, y, z depending on it's angle
                    # Idk if it works; written by ai.
                    if abs(data['rot_x']) > abs(data['rot_y']) and abs(data['rot_x']) > abs(data['rot_z']):
                        val *= data['scale_x']

                    elif abs(data['rot_y']) > abs(data['rot_x']) and abs(data['rot_y']) > abs(data['rot_z']):
                        val *= data['scale_y']

                    else:
                        val *= data['scale_z']

                elif prop == 'SpawnScale':

                    # Determine if we use scale x, y, z depending on it's angle
                    # Idk if it works; written by ai.
                    if abs(data['rot_x']) > abs(data['rot_y']) and abs(data['rot_x']) > abs(data['rot_z']):
                        val *= data['scale_x']

                    elif abs(data['rot_y']) > abs(data['rot_x']) and abs(data['rot_y']) > abs(data['rot_z']):
                        val *= data['scale_y']

                    else:
                        val *= data['scale_z']

                elif prop == 'SuspensionLength':

                    # Determine if we use scale x, y, z depending on it's angle
                    # Idk if it works; written by ai.
                    if abs(data['rot_x']) > abs(data['rot_y']) and abs(data['rot_x']) > abs(data['rot_z']):
                        val *= data['scale_z']

                    elif abs(data['rot_y']) > abs(data['rot_x']) and abs(data['rot_y']) > abs(data['rot_z']):
                        val *= data['scale_x']

                    else:
                        val *= data['scale_y']

                elif prop == 'TireThickness':

                    # Determine if we use scale x, y, z depending on it's angle
                    # Idk if it works; written by ai.
                    if abs(data['rot_x']) > abs(data['rot_y']) and abs(data['rot_x']) > abs(data['rot_z']):
                        val *= data['scale_z']  # Up/down

                    elif abs(data['rot_y']) > abs(data['rot_x']) and abs(data['rot_y']) > abs(data['rot_z']):
                        val *= data['scale_x']  # Left/right

                    else:
                        val *= data['scale_y']

                elif prop == 'WheelDiameter':

                    # Determine if we use scale x, y, z depending on it's angle
                    # Idk if it works; written by ai.
                    if abs(data['rot_x']) > abs(data['rot_y']) and abs(data['rot_x']) > abs(data['rot_z']):
                        val *= data['scale_x']

                    elif abs(data['rot_y']) > abs(data['rot_x']) and abs(data['rot_y']) > abs(data['rot_z']):
                        val *= data['scale_y']

                    else:
                        val *= data['scale_z']

                elif prop == 'WheelWidth':

                    # Determine if we use scale x, y, z depending on it's angle
                    # Idk if it works; written by ai.
                    if abs(data['rot_x']) > abs(data['rot_y']) and abs(data['rot_x']) > abs(data['rot_z']):
                        val *= data['scale_x']

                    elif abs(data['rot_y']) > abs(data['rot_x']) and abs(data['rot_y']) > abs(data['rot_z']):
                        val *= data['scale_y']

                    else:
                        val *= data['scale_z']

                elif prop == 'WinchSpeed':

                    # Determine if we use scale x, y, z depending on it's angle
                    # Idk if it works; written by ai.
                    if abs(data['rot_x']) > abs(data['rot_y']) and abs(data['rot_x']) > abs(data['rot_z']):
                        val *= data['scale_x']

                    elif abs(data['rot_y']) > abs(data['rot_x']) and abs(data['rot_y']) > abs(data['rot_z']):
                        val *= data['scale_y']

                    else:
                        val *= data['scale_z']

        new_bricks.append(brick)

    creation.bricks = new_bricks

    generate_backup(creation, backup_mode, limit)

    creation.write_brv()
    creation.write_metadata()
    if not os.path.exists(os.path.join(project_path, 'Preview.png')):
        creation.write_preview()

    if port:
        creation.write_to_br()

    return True, ''