from colorsys import rgb_to_hsv
from collections import Counter
import brci
from data import cwd, version, generate_backup
from PIL import Image
import math
import os
from random import randint


def reduce_colors(image: Image, colors: int, method: str):
    if image.mode != "RGBA":
        raise ValueError("Input image must be in RGBA mode")

    if method == 'common':
        # Count the occurrences of each color in the image
        color_counts = Counter()
        for x in range(image.width):
            for y in range(image.height):
                rgba = image.getpixel((x, y))
                color_counts[tuple(rgba)] += 1

        # Select the most common colors
        picked_palette = color_counts.most_common(colors)

    elif method[:6] == 'random':
        # Select random colors
        picked_palette = []
        for i in range(colors):
            random_color = image.getpixel((randint(0, image.width - 1), randint(0, image.height - 1)))
            picked_palette.append((random_color, 0))
        if method[:-3] == 'set':
            picked_palette = list(set(picked_palette))

    else:
        raise ValueError("Invalid color method")

    # Create a new image with the selected colors
    new_image = Image.new("RGBA", image.size)

    # Calculate the number of pixels per color
    # pixels_per_color = image.width * image.height // colors

    # Assign each color to approximately equal sections of the image
    for y in range(image.height):
        for x in range(image.width):
            color = image.getpixel((x, y))
            difference_list = []
            for candidates in picked_palette:
                difference_list.append(abs(color[0] - candidates[0][0]) + abs(color[1] - candidates[0][1]) + abs(color[2] - candidates[0][2]) + abs(color[3] - candidates[0][3]))
            color = picked_palette[difference_list.index(min(difference_list))][0]
            new_image.putpixel((x, y), color)
    """current_pixel = 0
    for i, (color, _) in enumerate(most_common_colors):
        start_pixel = current_pixel
        end_pixel = min(current_pixel + pixels_per_color, image.width * image.height)

        for x in range(start_pixel, end_pixel):
            x_pos = x % image.width
            y_pos = x // image.width
            new_image.putpixel((x_pos, y_pos), color)

        current_pixel = end_pixel"""

    return new_image


def resize_image(image: Image, width: int, height: int):

    image = image.resize((width, height))
    return image


def get_thumbnail(image: Image, width: int, height: int):
    # Create a new image with the desired dimensions and an alpha 0 background
    new_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    # Calculate the resized image to fit within the bounding box
    image.thumbnail((width, height))

    # Calculate the position to paste the resized image at the top left corner
    position = ((width - image.width) // 2, (height - image.height) // 2)

    # Paste the resized image onto the new image
    new_image.paste(image, position)

    return new_image


def run_length_encoding(grid):
    compressed_list = []
    rows = len(grid)
    cols = len(grid[0])

    for i in range(rows):
        for j in range(cols):
            if grid[i][j]:
                value = grid[i][j]
                size_x = 1
                size_y = 1
                while j + size_x < cols and grid[i][j + size_x] == value:
                    size_x += 1
                while i + size_y < rows:
                    valid = all(grid[i + size_y][j + k] == value for k in range(size_x))
                    if valid:
                        size_y += 1
                    else:
                        break
                compressed_list.append((value, j, i, size_x, size_y))

                for x in range(i, i + size_y):
                    for y in range(j, j + size_x):
                        grid[x][y] = False

    return compressed_list


def scalable_rle(data: dict[str, any], port: bool, backup_mode: list[bool], limit: int) -> (bool, str):

    # If you wonder why it's commented it's because I had so much trouble I rewrote that 3 times lmfao

    projects_folder_path = os.path.join(cwd, 'projects')
    if not os.path.exists(projects_folder_path):
        return False, 'important folders are missing. Please reinstall BrickUtils.'
    project_path = os.path.join(projects_folder_path, data['project'])
    if not os.path.exists(project_path):
        return False, f'project \'{data["project"]}\' was not found.'
    image_path = os.path.join(project_path, data['image'])
    if not os.path.exists(image_path):
        return False, f'image \'{data["image"]}\'was not found.'
    br_backup_folder_path = os.path.join(cwd, 'backup', 'brickrigs')
    project_backup_folder_path = os.path.join(cwd, 'backup', 'projects')
    if not os.path.exists(br_backup_folder_path) or not os.path.exists(project_backup_folder_path):
        return False, 'important folders are missing. Please reinstall BrickUtils.'

    # Opening it
    try:
        image = Image.open(image_path)
    except Exception as e:
        return False, f'could not open image; likely due to an incompatible format\n({type(e).__name__}: {e})'

    # Resizing (doing first to reduce memory usage)
    image_size_x, image_size_y = image.size
    ig_size_x = data['ig_res_x']
    ig_size_y = data['ig_res_y']
    if data['ig_calc'] == 'auto_x':
        ig_size_x = int((ig_size_y / image_size_y) * image_size_x)
    elif data['ig_calc'] == 'auto_y':
        ig_size_y = int((ig_size_x / image_size_x) * image_size_y)
    else: # if data['ig_calc'] == 'no_auto':
        pass

    try:
        image = image.resize((int(ig_size_x), int(ig_size_y)))
    except Exception as e:
        return False, f'BrickUtils do not support this format (resizing failed).\n({type(e).__name__}: {e})'

    # Converting to RGBA
    try:
        image = image.convert('RGBA')
    except Exception as e:
        return False, f'BrickUtils do not support this format (RGBA conversion failed).\n({type(e).__name__}: {e})'

    # Reducing the amount of colors -> less bricks (it's meant to be a pixelart eitherway) (1 - 256)
    try:
        image = reduce_colors(image, data['colors'], data['color_method'])
    except Exception as e:
        return False, f'BrickUtils do not support this format (quantization failed).\n({type(e).__name__}: {e})'

    # Put the image in a 2d grid of lists (not installing numpy I'm already having to help way too many players w/ installing pillow...)
    try:
        image_list: list[list[tuple[float, float, float, float]]] = []
        for y in range(ig_size_y):
            image_list.append([])
            for x in range(ig_size_x):
                # print(f'{x=}, {y=}, {image.getpixel((x, y))=}')
                # Get pixel color
                r, g, b, a = image.getpixel((x, y))
                # Switch to 0-1
                r, g, b, a = r/255, g/255, b/255, a/255
                # Don't worry, function was previously verified to be safe and valid
                # 'math': math gives the math module.
                r = eval(data['red_cor'], {'r': r, 'g': g, 'b': b, 'a': a, 'math': math})
                g = eval(data['green_cor'], {'r': r, 'g': g, 'b': b, 'a': a, 'math': math})
                b = eval(data['blue_cor'], {'r': r, 'g': g, 'b': b, 'a': a, 'math': math})
                a = eval(data['alpha_cor'], {'r': r, 'g': g, 'b': b, 'a': a, 'math': math})
                # Add color (corrected) tuple to image
                # Convert to HSVA (still under the name r g b a haha; there's not much so no confusion at least)
                try:
                    r, g, b = rgb_to_hsv(r, g, b)
                except Exception as e:
                    return False, f'BrickUtils do not support this format (RGBA -> HSVA conversion failed).\n({type(e).__name__}: {e})'
                image_list[y].append((r, g, b, a))
    except Exception as e:
        return False, f'BrickUtils do not support this format (image processing failed).\n({type(e).__name__}: {e})'

    # Apply run-length encoding
    try:
        image_list = run_length_encoding(image_list)
    except Exception as e:
        return False, f'optimisation process failed for unknown reasons.\n({type(e).__name__}: {e})'

    # Put it in a Brick Rigs creation
    # Can't use conventional data since it's already taken...
    # Setting up data -> creation
    creation = brci.BRCI()
    creation.project_name = data['project']
    creation.project_display_name = f'{data['project']} ({data['image']})'
    creation.project_folder_directory = projects_folder_path
    creation.custom_description_watermark = f'Generated using BrickUtils {version} by @perru_'
    creation.description = f'Project name: {data["project"]}\r\nImage name: {data["image"]}\r\nInfo: {data['ig_res_x']}x{data["ig_res_y"]} / {data["colors"]} colors'

    # Calculate pixel width, depth:
    if data['scale_mode'] == 'pixel':
        px_w = data['px_scale_x']
        px_h = data['px_scale_y']
    elif data['scale_mode'] == 'image':
        img_size_x, img_size_y = image.size
        px_w = data['img_scale_x'] / img_size_x
        px_h = data['img_scale_y'] / img_size_y
        if data['img_scale_calc'] == 'auto_x':
            px_w = px_h
        elif data['img_scale_calc'] == 'auto_y':
            px_h = px_w
        else: # if data['img_scale_calc'] == 'no_auto':
            pass
    elif data['scale_mode'] == 'reference':
        px_w = px_h = data['ref_scale_img'] / data['ref_scale_px']
    else:
        return False, 'unknown scale_mode' # Fail

    # Building em bricks
    for i, item in enumerate(image_list):

        # Get info
        value = item[0]
        x = item[1] * px_w
        y = item[2] * px_h
        w = item[3] * px_w
        h = item[4] * px_h

        # Calculate alpha -> Get materials
        materials = ['Plastic']
        if data['alpha_handling'] == 'ignore':
            pass
        elif data['alpha_handling'] == 'do_not_duplicate':
            if a < 0.1:
                materials = []
            elif a < 0.3:
                materials = ['Glass']
            elif a < 0.5:
                materials = ['CloudyGlass']
            else:
                materials = ['Plastic']
        elif data['alpha_handling'] == 'do_not_duplicate_delete':
            if a < 0.3:
                materials = ['Glass']
            elif a < 0.5:
                materials = ['CloudyGlass']
            else:
                materials = ['Plastic']
        elif data['alpha_handling'] == 'yes':
            a_ = round(a, 1)
            glass_a = 0.1
            cloudy_glass_a = 0.3
            glass: int = (a_ % cloudy_glass) // glass_a
            cloudy_glass: int = a_ // cloudy_glass_a
            for _ in range(glass):
                materials.append('Glass')
            for _ in range(cloudy_glass):
                materials.append('CloudyGlass')

        connections = [
            3 if data['connections']['sides'] else 0,
            3 if data['connections']['sides'] else 0,
            3 if data['connections']['sides'] else 0,
            3 if data['connections']['sides'] else 0,
            3 if data['connections']['front'] else 0,
            3 if data['connections']['back'] else 0
        ]

        # Building
        for brick_material in materials:
            creation.anb(str(i), 'ScalableBrick', {
                'BrickColor': [value[0]*255, value[1]*255, value[2]*255, 255],
                'BrickSize': [w/10, h/10, data['thickness']/10],
                'BrickMaterial': brick_material,
                'ConnectorSpacing': connections
            }, [-(x+w/2), -(y+h/2), data['thickness']/2], [0, 0, 0])

    # Saving
    # Preview
    if data['thumbnail'] == 'image':
        thumbnail = Image.open(image_path)
        thumbnail = get_thumbnail(thumbnail, 128, 128)
        thumbnail.save(os.path.join(project_path, 'Preview.png'))
    elif data['thumbnail'] == 'brci':
        try:
            creation.write_preview()
        except Exception as e:
            return False, f'preview generation (using brci preview) failed. Try setting thumbnail to image instead.\n({type(e).__name__}: {e})'
    # Metadata
    try:
        creation.write_metadata()
    except Exception as e:
        return False, f'metadata generation failed for unknown reasons.\n({type(e).__name__}: {e})'
    # Vehicle
    try:
        creation.write_brv()
    except Exception as e:
        return False, f'it appears vehicle generation failed. Try updating BrickUtils, or if no update is available, BRCI.\n({type(e).__name__}: {e})'
    # Port

    backup_success, backup_message = generate_backup(creation, backup_mode, limit)
    if not backup_success:
        return False, backup_message
    if port:
        creation.write_to_br()

    brick_count = creation.brick_count

    # Pretty sure we don't need to reset bricks using creation.clear_bricks()
    # since because brci.BRCI() is new at every generation there's no mutability-like issues?

    save_ratio = 1 - (brick_count / (ig_size_x * ig_size_y))

    return True, f'-\nWith {brick_count:,}/50,000 bricks (optimisation efficiency: {round(save_ratio*100, 1)}%).'