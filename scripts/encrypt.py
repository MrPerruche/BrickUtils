from data import hash_password, password_protected_brv, xor_encrypt, xor_rand_encrypt, cwd, version, generate_backup
import os
import brci
from shutil import copytree


def is_encrypted(brv: bytearray) -> bool:
    return brv.startswith(password_protected_brv)


def encrypt(data: dict[str, any], port: bool, backup_mode: list[bool], limit: int) -> (bool, str):

    projects_folder_path = os.path.join(cwd, 'projects')

    if not os.path.exists(projects_folder_path):
        return False, 'important folders are missing. Please reinstall BrickUtils.'

    project_path = os.path.join(projects_folder_path, data['project'])
    if not os.path.exists(project_path):
        return False, f'project \'{data["project"]}\' was not found.'

    brv_path = os.path.join(project_path, 'Vehicle.brv')
    if not os.path.exists(brv_path):
        return False, f'Vehicle.brv was not found in project \'{data["project"]}\''

    with open(brv_path, 'rb') as f:
        brv = bytearray(f.read())

    if is_encrypted(brv):
        return False, f'project \'{data["project"]}\' is already encrypted'

    password = data['password']

    # Version 2
    password = hash_password(password, 'sha512-r')  # 100,000 iter
    rand_password = hash_password(password, 'sha512')  # 100,001 iter
    encrypted = xor_rand_encrypt(brv, password, rand_password, undo=False)

    try:
        backup_success, backup_message = generate_backup(brci.BRCI(), backup_mode, limit)
        if not backup_success:
            return False, backup_message
    except Exception as e:
        return False, f'backup failed for unknown reasons.\n({type(e).__name__}: {e})'

    try:
        with open(brv_path, 'wb') as f:
            f.write(password_protected_brv)
            f.write(brci.unsigned_int(2, 1))
            f.write(encrypted)
    except Exception as e:
        return False, f'could not write to Vehicle.brv\n({type(e).__name__}: {e})'

    try:
        if port:
            local_appdata_dir = os.getenv('LOCALAPPDATA')
            project_br_dir = os.path.join(local_appdata_dir, 'BrickRigs', 'SavedRemastered', 'Vehicles', data['project'])

            if not os.path.exists(project_br_dir):
                os.makedirs(project_br_dir)
            copytree(project_path, project_br_dir, dirs_exist_ok=True)

    except Exception as e:
        return False, f'porting failed for unknown reasons.\n({type(e).__name__}: {e})'

    return True, f'project was encrypted using password \'{data["password"]}\''


def decrypt(data: dict[str, any], port: bool, backup_mode: list[bool], limit: int) -> (bool, str):

    projects_folder_path = os.path.join(cwd, 'projects')

    if not os.path.exists(projects_folder_path):
        return False, 'important folders are missing. Please reinstall BrickUtils.'

    project_path = os.path.join(projects_folder_path, data['project'])
    if not os.path.exists(project_path):
        return False, f'project \'{data["project"]}\' was not found.'

    brv_path = os.path.join(project_path, 'Vehicle.brv')
    if not os.path.exists(brv_path):
        return False, f'Vehicle.brv was not found in project \'{data["project"]}\''

    with open(brv_path, 'rb') as f:
        brv = bytearray(f.read())

    if is_encrypted(brv):
        brci.b_pop(brv, len(password_protected_brv))
    else:
        return False, f'project \'{data["project"]}\' is already encrypted'

    encrypt_version = brci.r_unsigned_int(brci.b_pop(brv, 1))

    try:
        backup_success, backup_message = generate_backup(brci.BRCI(), backup_mode, limit)
        if not backup_success:
            return False, backup_message
    except Exception as e:
        return False, f'backup failed for unknown reasons.\n({type(e).__name__}: {e})'

    if encrypt_version == 1:

        password = hash_password(data['password'], 'sha512')
        decrypted = xor_encrypt(brv, password)

    elif encrypt_version == 2:

        password = hash_password(data['password'], 'sha512-r')
        rand_password = hash_password(password, 'sha512')
        decrypted = xor_rand_encrypt(brv, password, rand_password, undo=True)

    else:
        return False, 'unknown encryption version. Consider updating BrickUtils.'

    with open(brv_path, 'wb') as f:
        f.write(decrypted)

    try:
        if port:
            local_appdata_dir = os.getenv('LOCALAPPDATA')
            project_br_dir = os.path.join(local_appdata_dir, 'BrickRigs', 'SavedRemastered', 'Vehicles', data['project'])

            if not os.path.exists(project_br_dir):
                os.makedirs(project_br_dir)

            copytree(project_path, project_br_dir, dirs_exist_ok=True)

    except Exception as e:
        return False, f'porting failed for unknown reasons.\n({type(e).__name__}: {e})'

    return True, f'using password \'{data["password"]}\''