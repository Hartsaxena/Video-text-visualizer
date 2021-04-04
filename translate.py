from PIL import Image
from pathlib import Path
from tqdm import tqdm
import colors
import os
import time
import pickle
import sys

os.chdir(Path(__file__).parent.absolute())


def compile_video(frame_folder, input_string):
    result = []
    for file_name in tqdm(frame_order_sort(frame_folder)):
        img = Image.open(os.path.join(frame_folder, file_name))
        image_list = translate_image(img, input_string)
        result.append(image_list)
    return result


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


def translate_image(image, wrap_string):
    pixels = image.load()
    image_list = [["N" for _ in range(image.size[0])] for _ in range(image.size[1])]
    for x in range(0, image.size[0]):
        for y in range(0, image.size[1]):
            color = color_to_binary(pixels[x,y])
            if color == colors.WHITE:
                image_list[y][x] = " "
            elif color == colors.BLACK:
                image_list[y][x] = "O"
    cycled_index = 0
    for y in range(0, len(image_list)):
        for x in range(0, len(image_list[0])):
            if image_list[y][x] == "O":
                image_list[y][x] = wrap_string[cycled_index]
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


def average_color(colors_list):
    # colors_list is a list of tuples containing RGB values.
    # Returns a single tuple RGB color value as the average value in the list.
    result = [0, 0, 0]
    colors_amount = len(colors_list)
    for rgb in range(3):
        for color in colors_list:
            result[rgb] += color[rgb]
        result[rgb] = rgb // colors_amount
    return tuple(result)


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


if __name__ == "__main__":
    data_file_name = input("Please input the name of the datafile to load: ")
    inputs = input("Would you like to enable manual scrolling?\n(this makes it so that instead of a constant animation, it plays like a slieshow, where pressing enter goes to the next frame.)\n(y / n) ").lower()[0]
    inputs = False
    if inputs == "y":
        inputs = True
    experimental_mode = input("Would you like to use experimental mode? (y / n) ").lower()[0]
    exp = False
    if experimental_mode == "y":
        exp = True
    if exp:
        fps = int(input("Please input the fps (frames per second) of the video: "))
    else:
        fps = 1
    interval = int(input("Please input the interval between frames of the file: "))
    if not interval:
        interval = 1
    data_file = data_file_name
    if not os.path.isfile(data_file_name):
        if data_file_name.endswith(".data"):
            data_file_name = data_file_name[:-5]
        os.makedirs("public_data", exist_ok=True)
        if f"{data_file_name}.data" in os.listdir("public_data"):
            data_file = os.path.join("public_data", f"{data_file_name}.data")
    print("Loading frame data...")
    with open(data_file, 'rb') as frame_data:
        frames = pickle.load(frame_data)
    translate_video(frames, inputs, exp, interval, fps)