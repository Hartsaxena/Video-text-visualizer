from PIL import Image
from tqdm import tqdm
import colors
import os
import time


def translate_video(frame_list, inputs=False, exp=False, frame_interval=1, fps=60):
    if exp:
        fps = fps / frame_interval
    for frame in frame_list:
        frame_time = time.perf_counter()
        # os.system("clear")
        print(string_listlist(frame))
        if inputs:
            input()
        elif exp:
            time.sleep(max(1.0 / fps - (time.perf_counter() - frame_time), 0))
        else:
            time.sleep(0.05)


def parse_file(file_path):
    result = open(file_path).read()
    result = result.replace("\n", " ")
    return result


def frame_order_sort(frame_folder):
    frame_numbers = []
    for file_name in os.listdir(frame_folder):
        frame_numbers.append(int(file_name[5:-4]))
    frame_numbers.sort()
    result = [f"frame{num}.jpg" for num in frame_numbers]
    return result


def translate_image(image, wrap_string, translate_binary=False):
    pixels = image.load()
    if translate_binary: # NOTE: binary translating is wonky now. Should work, but not exactly as intended.
        image_list = [[" " for _ in range(image.size[0])] for _ in range(image.size[1])]
        for x in range(0, image.size[0]):
            for y in range(0, image.size[1]):
                color = color_to_binary(pixels[x,y])
                if color == colors.BLACK:
                    image_list[y][x] = "O"
    else:
        image_list = [[["O", pixels[x,y]] for x in range(image.size[0])] for y in range(image.size[1])]

    cycled_index = 0
    for y in range(0, len(image_list)):
        for x in range(0, len(image_list[0])):
            if translate_binary:
                if image_list[y][x] == "O":
                    image_list[y][x] = wrap_string[cycled_index]
                    cycled_index += 1
                    if cycled_index >= len(wrap_string):
                        cycled_index = 0
            elif image_list[y][x][0] == "O":
                image_list[y][x][0] = wrap_string[cycled_index]
                cycled_index += 1
                if cycled_index >= len(wrap_string):
                    cycled_index = 0
    return image_list


def group_coords(topleft, chunk_dimensions, limits):
    bottomright = [topleft[0] + chunk_dimensions[0], topleft[1] + chunk_dimensions[1]]
    bottomright[0] = clamp(bottomright[0], 0, limits[0] - 1)
    bottomright[1] = clamp(bottomright[1], 0, limits[1] - 1)
    result = []
    for x in range(topleft[0], bottomright[0] + 1):
        for y in range(topleft[1], bottomright[1] + 1):
            result.append([x, y])
    return result


def clamp(value, small, big):
    result = value
    if result < small:
        result = small
    elif result > big:
        result = big
    return result


def color_to_binary(color):
    # Converts a color (in format tuple(r, g, b) representing RGB color value) into either:
    # White: (255, 255, 255) or
    # Black: (0, 0, 0)
    r, g, b = color
    luminace = 0.2126 * r + 0.7152 * g + 0.0722 * b # Some formula I found on StackOverflow. Hopefully this works.
    if luminace < 128:
        result = (0, 0, 0)
    else:
        result = (255, 255, 255)
    return result


def string_listlist(listlist, beginning=""):
    # Prints a list of lists
    full_string = beginning
    for row in listlist:
        for col in row:
            full_string += col
        full_string += "\n"
    return full_string


def string_to_tuple(string):
    if not string:
        return tuple()
    
    changed_string = string
    if string[0] == "(" and string[-1] == ")":
        changed_string = changed_string[1:-1]

    result = tuple(map(int, changed_string.split(', ')))
    return result