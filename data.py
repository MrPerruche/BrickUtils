import colorsys
import os
import json
from datetime import datetime
import brci
import shutil
import hashlib
import subprocess
from random import choice, randint
from secrets import choice as choice_safe
import string
import re

# A bunch of hardcoded values here, as well as function used in several scripts.
# There's a bunch of warnings here. I haven't figured them out, but it seems everything works. Maybe a bug with my IDE.
# - Functions have the dumbest names possible: match_color(), get_len_unit(), get_r_lightbar_colors(), clen_str(), ...
# - There's no comments even in the most confusing parts
# - I use list comprehension a bit too much. Maybe I shouldn't have, but it's fun to write.

menu: str = 'main'
version: str = 'D8'
br_version: str = '1.7.4'
cwd = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(cwd, 'resources', 'user_react_list.txt'), 'r') as f:
    react_key_item_list: list[str] = f.read().split('\n')
    react_dict: dict[str, float] = {}
    for item in react_key_item_list:
        split_item: list[str] = item.split(',')
        if len(split_item) >= 2:
            key = split_item[0]
            value = float(split_item[1])
            react_dict[key] = value

with open(os.path.join(cwd, 'resources', 'char_blacklist.txt'), 'r') as f:
    char_blacklist = [*f.read().split('\n'), ' ']

with open(os.path.join(cwd, 'resources', 'password_protected.brv'), 'rb') as f:
    password_protected_brv: bytearray = bytearray(f.read())



# Setup Menu Memory
init_memory: dict[str, any] = {
    'invalid': {
        'return_path': '',
        'text': ''
    },
    'fatal_error': {
        'return_path': '',
        'text': ''
    },
    'success': {
        'return_path': '',
        'text': ''
    },
    'main': {
        'port': [True, True],
        'backup': [True, True],
        'backup_limit': 6,
        'system': 'cgs'
    },
    'main/brick': {
        'project': 'Custom Brick',
        'brick': '',
        'properties': {}
    },
    'main/brick/select_brick': {
        'search': '',
        'matches': []
    },
    'main/brick/properties': {
        'advanced': False
    },
    'main/brick/properties/advanced_required': {
        'property': ''
    },
    'main/brick/properties/eval': {
        'property': '',
    },
    'main/brick/properties/color': {
        'property': '',
        'mode': 'select_color_space',
        'alpha': True
    },
    'main/brick/properties/choice': {
        'property': '',
        'options': []
    },
    'main/brick/properties/float': {
        'property': '',
        'distance': None
    },
    'main/brick/properties/int': {
        'property': '',
        'limit': [0, 255]
    },
    'main/brick/properties/list': {
        'property': '',
        'type': '',
        'len': [2],
        'accepts_none': False,
        'distance': None
    },
    'main/brick/properties/connector': {
        'property': ''
    },
    'main/brick/properties/strany': {
        'property': ''
    },
    'main/arc': {

    },
    'main/pixelart': {
        'project': '',
        'image': '',
        'import_mode': 'scalable_rle',
        'ig_calc': 'auto_x',
        'ig_res_x': 32,
        'ig_res_y': 32,
        'color_method': 'random_list',
        'colors': 25,
        'scale_mode': 'pixel',
        'px_scale_x': 2.0,
        'px_scale_y': 2.0,
        'img_scale_calc': 'auto_x',
        'img_scale_x': 50.0,
        'img_scale_y': 50.0,
        'ref_scale_px': 10.0,
        'ref_scale_img': 50.0,
        'thickness': 1.0,
        'connections': {'sides': True, 'front': True, 'back': True},
        'red_cor': "r ** 2.2",
        'green_cor': "g ** 2.2",
        'blue_cor': "b ** 2.2",
        'alpha_cor': "a",
        'alpha_handling': 'do_not_duplicate',
        'thumbnail': 'image'
    },
    'main/pixelart/connections': {
        'edited': 'sides',
        'new': {'sides': True, 'front': True, 'back': True},
        'scores': {'sides': [0, 0], 'front': [0, 0], 'back': [0, 0]},
    },
    """
    'main/edit': {
        'project': '',
        'move': False,
        'off_x': 0.0,
        'off_y': 0.0,
        'off_z': 0.0,
        'scale': False,
        'scale_x': 1.0,
        'scale_y': 1.0,
        'scale_z': 1.0,
        'adapt_connections': 'no',
        'scale_extras': True,
        'rotate': False,
        'rot_x': 0.0,
        'rot_y': 0.0,
        'rot_z': 0.0,
        'clear_duplicates': False
    },
    """
    'abc': None,  # Comment breaks 'main/lightbar' thing...
    'main/lightbar': {
        'project': '',
        'file_name': 'lightbar.json',
        'layout': [
            {'col': [162, 247, 204, 255], 'brightness': 0.5, 'material': 'LEDMatrix'},
            {'col': [162, 247, 204, 255], 'brightness': 0.5, 'material': 'LEDMatrix'},
            {'col': [162, 247, 204, 255], 'brightness': 0.5, 'material': 'LEDMatrix'},
            {'col': [0, 0, 227, 255], 'brightness': 0.5, 'material': 'LEDMatrix'},
            {'col': [162, 247, 204, 255], 'brightness': 0.5, 'material': 'LEDMatrix'},
            {'col': [1, 252, 117, 255], 'brightness': 0.5, 'material': 'LEDMatrix'},
            {'col': [0, 0, 227, 255], 'brightness': 0.5, 'material': 'LEDMatrix'},
            {'col': [1, 252, 117, 255], 'brightness': 0.5, 'material': 'LEDMatrix'},
            {'col': [1, 252, 117, 255], 'brightness': 0.5, 'material': 'LEDMatrix'},
            {'col': [1, 252, 117, 255], 'brightness': 0.5, 'material': 'LEDMatrix'}
        ],
        'lightbar': []
    },
    'main/lightbar/layout': {
        'selected': 0
    },
    'main/lightbar/layout/color' : {
        'mode': 'select_color_space',
        'alpha': True
    },
    'main/lightbar/stage': {
        'selected': 0
    },
    'main/rot': {

    },
    'main/encrypt': {
        'project': '',
        'password': '',
        'see_password': False
    },
    'main/encrypt/password': {
        'repeat': False,
        'pre_pass': ['', '']
    },
    'main/encrypt/generate': {
        'password': ''
    },
    'main/settings': {
        'new_main': {}
    },
    'main/help': {
        'lang': 'english (english)'
    },
    'main/edit': {
        'project': '',
        'move': None,
        'rotate': None,
        'allow_out_of_range_rotation': None,
        'scale': None,
        'connections': {'sides': True, 'top': True, 'bottom': True},
        'duplicates': 'keep',
    },
    'main/edit/connections': {
        'edited': 'sides',
        'new': {'sides': True, 'top': True, 'bottom': True},
        'scores': {'sides': [0, 0], 'top': [0, 0], 'bottom': [0, 0]}
    }
}


"""
def inspect_class(obj):  # TODO
    for attr in dir(obj):
        if not attr.startswith("__"):
            val = getattr(obj, attr)
            print(f"{attr}: {val}abc_123_!?#{brci.FM.reset}")
inspect_class(brci.FM)
input()
"""


terminal_colors: dict[tuple[int, int, int], str] = {
    # (0, 0, 0): brci.FM.black,  # Excluding black since it would be INVISIBLE
    (0, 0, 255): brci.FM.blue,
    (0, 127, 191): brci.FM.cyan,
    (0, 191, 0): brci.FM.green,
    (63, 63, 63): brci.FM.light_black,
    (63, 63, 255): brci.FM.light_blue,
    (0, 255, 255): brci.FM.light_cyan,
    (0, 255, 0): brci.FM.light_green,
    (191, 0, 127): brci.FM.light_purple,
    (255, 127, 127): brci.FM.light_red,
    (255, 255, 255): brci.FM.light_white,
    (255, 255, 191): brci.FM.light_yellow,
    (127, 0, 95): brci.FM.purple,
    (191, 0, 0): brci.FM.red,
    (191, 191, 191): brci.FM.white,
    (127, 79, 0): brci.FM.yellow
}


def hash_password(password: str | bytes, method: str = 'sha512-r') -> bytearray:

    # yes, my iq can be measured with a pH strip

    bin_password: bytes = password.encode('utf-8') if isinstance(password, str) else password

    hash_pass: bytes = b'\x00'

    if method == 'sha512-r':
        hash_pass = bin_password
        for _ in range(206_183):
            hash_pass: bytes = hashlib.sha512(hash_pass).digest()

    elif method == 'sha512':
        hash_pass: bytes = hashlib.sha512(bin_password).digest()

    return bytearray(hash_pass)


def is_valid_folder_name(folder_name: str) -> bool:
    # Windows folder names cannot contain any of these characters
    invalid_chars = r'[<>:"/\\|?*]'

    # Check if the name is empty or contains invalid characters
    if not folder_name or re.search(invalid_chars, folder_name):
        return False

    # Check if the folder name ends with a space or a period (Windows does not allow this)
    if folder_name[-1] in {' ', '.'}:
        return False

    # If all checks pass, the name is valid
    return True



def xor_encrypt(data: bytearray, pw: bytearray) -> bytes:
    """
    :param data: File
    :param pw: Password
    :return: Xor encrypted file
    """
    # These things are stupid it's the last time I'm making one of these comments

    return bytes([data[i] ^ pw[i % len(pw)] for i in range(len(data))])


def xor_rand_encrypt(data: bytearray, xor_pw: bytearray, rand_pw: bytearray, undo: bool = False) -> bytes:

    rand_pw_l = [bit == '1' for byte in rand_pw for bit in '{:08b}'.format(byte)]
    input(rand_pw_l)
    result = bytearray()

    if not undo:
        rand_xor_current_bits = []

        xor_file = bytearray([data[i] ^ xor_pw[i % len(xor_pw)] for i in range(len(data))])
        cur_bit = 0

        for xf_byte in xor_file:

            xf_bits = [(xf_byte >> i) & 1 for i in range(7, -1, -1)]

            for j in range(8):

                rand_xor_current_bits.append(xf_bits[j])

                if rand_pw_l[cur_bit % len(rand_pw_l)]:
                    pass
                    rand_xor_current_bits.append(choice([0, 1]))

                cur_bit += 1

            while len(rand_xor_current_bits) >= 8:
                bits_as_int = sum(bit << (7 - i) for i, bit in enumerate(rand_xor_current_bits[:8]))
                # input(f'{bits_as_int=}, {rand_xor_current_bits[:8]=}, {dict(enumerate(rand_xor_current_bits[:8]))=}')
                result += bits_as_int.to_bytes(1, 'big')
                del rand_xor_current_bits[:8]


    else:  # if undo

        rand_xor_current_bits = []
        # cur_bit = 0 - 1
        rand_file = bytearray()
        pass_input = False
        rand_pw_l_use = []

        for xf_byte in data:

            xf_bits = [(xf_byte >> i) & 1 for i in range(7, -1, -1)]

            for j in range(8):

                if pass_input:
                    pass_input = False
                    continue

                rand_xor_current_bits.append(xf_bits[j])

                if not rand_pw_l_use:
                    rand_pw_l_use = rand_pw_l.copy()

                if rand_pw_l_use[0]:
                    pass_input = True
                del rand_pw_l_use[0]

            while len(rand_xor_current_bits) >= 8:
                bits_as_int = sum(bit << (7 - i) for i, bit in enumerate(rand_xor_current_bits[:8]))
                rand_file += bits_as_int.to_bytes(1, 'big')
                del rand_xor_current_bits[:8]


        result = bytearray([rand_file[i] ^ xor_pw[i % len(xor_pw)] for i in range(len(rand_file))])

    return result


def return_password(min_length: int, max_length: int) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation.replace('`', '')
    length = randint(min_length, max_length)
    return ''.join(choice_safe(alphabet) for _ in range(length))


def set_clipboard(text: str):
    process = subprocess.Popen('clip', stdin=subprocess.PIPE, text=True)
    process.communicate(text)


def match_color(rgb: list[int]):

    if len(rgb) != 3:
        raise IndexError('rgb must have 3 elements, not ' + str(len(rgb)))

    diff_table: dict[tuple[int, int, int], int] = {}

    for col in terminal_colors.keys():
        diff_table |= {col: sum([abs(col - rgb[i]) for i, col in enumerate(col)])}

    least: tuple[int, int, int] = (0, 0, 0)
    least_diff: int = 1_000  # White VS black is 765. It cannot not be replaced at least once

    for col, diff in diff_table.items():
        if diff < least_diff:
            least = col
            least_diff = diff

    return terminal_colors[least]


def render_lightbar(layout: list, filler: str = '[]', zfill_override: bool = False, sel: int | None = None, space: bool = False):

    lightbar_str: str = ''
    space_ = ' ' if space else ''
    light_text = filler

    for i, brick in enumerate(layout):

        if zfill_override:
            light_text = str(i+1).zfill(2)

        rgb_col = [int(y * 255) for y in colorsys.hsv_to_rgb(*[x / 255 for x in brick['col'][:3]])]
        if sel is None or sel == i:
            lightbar_str += f'{match_color(rgb_col)}{brci.FM.reverse}{light_text}{brci.FM.reset}{space_}'
        else:
            lightbar_str += f'{match_color(rgb_col)}{light_text}{brci.FM.reset}{space_}'

    return lightbar_str


def get_r_lightbar_colors(layout: list) -> list[str]:

    output: list = []

    for i, brick in enumerate(layout):

        rgb_col = [int(y * 255) for y in colorsys.hsv_to_rgb(*[x / 255 for x in brick['col'][:3]])]
        output.append(match_color(rgb_col))

    return output


def clamp(min_: float, val: float, max_: float) -> float:

    return max(min_, min(val, max_))


def get_64_time_ns() -> int:

    return int((datetime.now() - datetime(1, 1, 1)).total_seconds() * 1e7)


def load_json(path: str) -> dict:

    with open(path, 'r') as f_:
        return json.load(f_)


def generate_backup(creation: brci.BRCI, behavior: list[bool], limit: int) -> (bool, str):

    projects_path = os.path.join(cwd, 'projects')
    if not os.path.exists(projects_path):
        return False, 'important folders are missing. Please reinstall BrickUtils.'
    projects_backup_path = os.path.join(cwd, 'backup', 'projects')
    if not os.path.exists(projects_backup_path):
        return False, 'important folders are missing. Please reinstall BrickUtils.'
    br_backup_path = os.path.join(cwd, 'backup', 'brickrigs')
    if not os.path.exists(br_backup_path):
        return False, 'important folders are missing. Please reinstall BrickUtils.'

    time: int = get_64_time_ns()

    if behavior[0]:
        shutil.copytree(projects_path, os.path.join(projects_backup_path, str(time)))
    if behavior[1]:
        creation.backup_directory = br_backup_path
        creation.backup(str(time))

    try:
        projects_backup_dir_names: list[int] = [int(directory) for directory in os.listdir(projects_backup_path) if directory.isnumeric()]
    except ValueError:
        return False, f'backup failed. All directories in backup/projects must be integers.'
    elements_in_projects_backup = len(projects_backup_dir_names)
    if elements_in_projects_backup > limit:
        for i in range(elements_in_projects_backup - limit):
            deleted_file = str(min(projects_backup_dir_names))
            shutil.rmtree(os.path.join(projects_backup_path, deleted_file))

    try:
        br_backup_dir_names: list[int] = [int(directory) for directory in os.listdir(br_backup_path) if directory.isnumeric()]
    except ValueError:
        return False, f'backup failed. All directories in backup/brickrigs must be integers.'
    elements_in_br_backup = len(br_backup_dir_names)
    if elements_in_br_backup > limit:
        for i in range(elements_in_br_backup - limit):
            deleted_file = str(min(br_backup_dir_names))
            shutil.rmtree(os.path.join(br_backup_path, deleted_file))

    return True, ''


def save_json(path: str, data: dict) -> None:

    with open(path, 'w') as f_:
        json.dump(data, f_, indent=4)


def multi_replace(string: str, replacements: list[str], new: str) -> str:

    new_str = string

    for replaced in replacements:

        new_str = new_str.replace(replaced, new)

    return new_str


def convert_length(val: float, old_unit: str, new_unit: str) -> float:

    si_unit = 0.0
    if old_unit == 'cgs': si_unit = val * 0.01
    elif old_unit == 'si': si_unit = val
    elif old_unit == 'imperial': si_unit = val * 0.0254
    elif old_unit == 'scal': si_unit = val / (10 / 3)
    elif old_unit == 'stud': si_unit = val / 10

    if new_unit == 'cgs': return si_unit * 100
    elif new_unit == 'si': return si_unit
    elif new_unit == 'imperial': return si_unit / 0.0254
    elif new_unit == 'scal': return si_unit * 30
    elif new_unit == 'stud': return si_unit * 10
    else: return val


def get_len_unit(unit: str, short: bool, may_be_plural: bool = True) -> str:

    if unit == 'cgs':
        if short: return 'cm'
        else: return 'centimeter' + ('s' if may_be_plural else '')
    elif unit == 'si':
        if short: return 'm'
        else: return 'meter' + ('s' if may_be_plural else '')
    elif unit == 'imperial':
        if short: return 'in'
        else: return 'inch' + ('es' if may_be_plural else '')
    elif unit == 'scal':
        if short: return 'scal'
        else: return 'scalable' + ('s' if may_be_plural else '')
    elif unit == 'stud':
        if short: return 's'
        else: return 'stud'
    else: return unit


def clen(val: str | float, unit: str) -> str:

    if unit == 'scal':
        val_str: str = str(val)
        val_str = val_str.replace('s', 'j').replace(' ', '')
        val_complex: complex = complex(val_str)
        return convert_length(val_complex.real + val_complex.imag / 3, unit, 'cgs')

    # else:
    return convert_length(i_float(val), unit, 'cgs')


def clen_str(val: float, unit: str) -> str:

    if unit == 'scal':

        # input = centimeters. convert to thirds
        val_fix = val / 3
        val_fix_low = val_fix / 30
        tolerance = 0.0001

        if (val_fix_low * 9 + tolerance) % 1 <= tolerance * 2:
            complex_val: complex = complex(*divmod(round(val_fix_low * 9), 3))
            val_table = ['', '⅓', '⅔']
            return f'{int(complex_val.real)}{val_table[int(complex_val.imag)]} scal / {round(convert_length(val_fix, 'cgs', unit), 4):,}s'

        else:
            return f'{round(convert_length(val_fix, 'cgs', unit) / 3, 4)} {get_len_unit(unit, True)} / {round(convert_length(val_fix, 'cgs', unit), 4):,}s'

    # else:

    return f'{round(convert_length(val, 'cgs', unit), 4)} {get_len_unit(unit, True)}'


def str_connector(con: int) -> str:
    if con == 0: return 'none'
    elif con == 1: return 'default'
    elif con == 2: return 'halves'
    elif con == 3: return 'thirds'
    else: return 'Unknown'


def str_int_dir(val: int) -> str:

    if val == 0: return 'Y+'
    elif val == 1: return 'Y-'
    elif val == 2: return 'X+'
    elif val == 3: return 'X-'
    elif val == 4: return 'Z+'
    elif val == 5: return 'Z-'
    else: return 'Unknown'


def i_int(i: str) -> int:
    i_ = i.replace(' ', '')
    i_ = i_.replace(',', '')
    if 'inf' in i_:
        if i_[0] == '-':
            return -1_000_000_000
        # else:
        return 1_000_000_000
    if i_ == 'nan':
        return 0
    if 'e' in i_:
        # not using int(float()) to avoid floating point accuracy issues here
        i_ = i_.split('e')
        i_[0] = i_[0][:int(i_[1])]
        i_ = int(i_[0]) * 10 ** int(i_[1])
        return i_
    return int(i_)


def i_float(i: str) -> float:
    i_ = i.replace(' ', '')
    i_ = i_.replace(',', '')
    i_ = i_.replace('_', '')
    try:
        return float(i_)
    except ValueError:
        oom_indicators = {'da': 1, 'h': 2, 'k': 3, 'M': 6, 'G': 9, 'T': 12, 'P': 15, 'E': 18, 'Z': 21, 'Y': 24, 'R': 27, 'Q': 30, # r q: new prefixes adopted in nov 2022
                          'd': -1, 'c': -2, '%': -2, 'm': -3, 'µ': -6, 'u': -6, 'n': -9, 'p': -12, 'f': -15, 'a': -18, 'z': -21, 'y': -24, 'r': -27, 'q': -30}

        oom: int = 0

        for oom_, val in oom_indicators.items():
            while oom_ in i_:
                i_ = i_.replace(oom_, '', 1)
                oom += val

        exp = 1
        if i_.startswith('/'):
            exp = -1
            i_ = i_.replace('/', '')

        return (float(i_) * (10 ** oom)) ** exp
