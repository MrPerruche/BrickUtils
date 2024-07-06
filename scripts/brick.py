import brci
from data import char_blacklist, multi_replace, cwd, version, generate_backup
import os


def return_matches(prompt: list[str]) -> list[str]:

    bricks: list[str] = list(brci.br_brick_list.keys())
    bricks.remove('default_brick_data')

    fixed_bricks: list[str] = []
    for brick in bricks:
        fixed_bricks.append(multi_replace(brick, char_blacklist, '').lower())

    fixed_prompt: list[str] = []
    for word in prompt:
        fixed_prompt.append(multi_replace(word, char_blacklist, '').lower())

    if not prompt: # prompt == []
        return bricks
    # else:

    matches: list[str] = []

    # O(n^2) brother ew brother whats that ik ik but guess what I'm lazy it's only gonna do like 8,000 iterations at worst eitherway
    for i, fixed_brick in enumerate(fixed_bricks):
        is_inside: list[bool] = []
        for word in fixed_prompt:
            is_inside.append(word in fixed_brick)
        if all(is_inside):
            matches.append(bricks[i])

    return matches


def get_brick_properties(brick: str) -> dict[str, any]:

    if brick in brci.br_brick_list:
        return brci.create_brick(brick)

    # else:
    return {}


def generate(data: dict[str, any], port: bool, backup_mode: list[bool], limit: int) -> (bool, str):


    projects_folder_path = os.path.join(cwd, 'projects')
    if not os.path.exists(projects_folder_path):
        return False, 'important folders are missing. Please reinstall BrickUtils.'
    project_path = os.path.join(projects_folder_path, data['project'])


    creation = brci.BRCI()
    creation.project_folder_directory = projects_folder_path
    creation.project_name = data['project']
    creation.project_display_name = f'{data['project']}'
    creation.custom_description_watermark = f'Generated using BrickUtils {version} by @perru_'
    creation.description = f'Project name: {data["project"]}\r\nProperties:'
    for prop, val in data['properties'].items():
        creation.description += f'\r\n{prop}: {val}'

    creation.anb('brick', data['brick'], data['properties'])

    generate_backup(creation, backup_mode, limit)

    creation.write_brv()
    creation.write_metadata()
    if not os.path.exists(os.path.join(project_path, 'Preview.png')):
        creation.write_preview()

    if port:
        creation.write_to_br()

    return True, ''