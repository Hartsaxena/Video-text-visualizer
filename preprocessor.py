from PIL import Image
from pathlib import Path
from tqdm import tqdm
import cv2
import os
import pickle
import translate


def gen_frames(workspace, video_path, frame_interval, text_file, data_file, scale_amount=0, verbose=True):
    os.makedirs(workspace, exist_ok=True)
    vidcap = cv2.VideoCapture(video_path)
    max_progress = total_frames(vidcap)
    generator = range(max_progress)
    if verbose:
        prev_files = os.listdir(workspace)
        if len(prev_files) != 0:
            print("WARNING: The workspace folder is not empty.")
            print("In order to function correctly, the frames folder must be empty.")
            print("The program will automatically delete all files in the folder before running.")
            input("Press \"ENTER\" to continue, or press CTRL + C to exit.")
            for file_name in prev_files:
                os.remove(os.path.join(workspace, file_name))
        print(f"Processing {max_progress} frames every {frame_interval} frames... (This can take a while)")
        generator = tqdm(generator)
    count = 0
    frames = []
    for _ in generator:
        _, image = vidcap.read()
        if count % frame_interval == 0:
            fullpath        = os.path.join(workspace, f"frame{count}.jpg")
            width           = int(image.shape[1] * scale_amount / 100)
            height          = int(image.shape[0] * scale_amount / 100)
            dsize           = (width, height)
            output          = cv2.resize(image, dsize)
            cv2.imwrite(fullpath, output)
            image           = Image.open(fullpath)
            pix             = image.load()
            pix             = binary_pixels(pix, image.size)
            input_string    = translate.parse_file(text_file)
            image_list      = translate.translate_image(image, input_string)
            frames.append(image_list)
            image.save(fullpath)
        count += 1
    with open(data_file, "wb") as data_file: # Save the video's frame data to pickle file.
        pickle.dump(frames, data_file)
    cv2.destroyAllWindows()


def binary_pixels(pixels, image_dimensions):
    for x in range(image_dimensions[0]):
        for y in range(image_dimensions[1]):
            pixels[x,y] = translate.color_to_binary(pixels[x,y])
    return pixels


def total_frames(video):
    changed_video = video
    result = 0
    result = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    return result


if __name__ == "__main__":
    os.chdir(Path(__file__).parent.absolute())
    frame_interval = int(input("Please input the frame intervals: "))
    scale = int(input("Please input the scale of the frames: "))
    video = input("Please input the path to the video: ")
    text_file_path = input("Please input the path to the text file with the text you would like to display: ")
    data_file_path = input("Please input the file to store the animation data: ")
    workspace = input("Please input the path of the folder you would like the program to work in\n(input \"default\" or nothing to work in default folder): ").lower()
    if workspace == "default" or workspace == "":
        workspace = "frames"
    if not data_file_path.endswith(".data"):
        data_file_path += ".data"
    if len(data_file_path.split(os.sep)) == 1:
        data_file_path = os.path.join("public_data", data_file_path)
    if not (video.startswith("C:") or video.startswith("/")):
        video = os.path.join("public_videos", video)
    gen_frames(workspace, video, frame_interval, text_file_path, data_file_path, scale_amount=scale)