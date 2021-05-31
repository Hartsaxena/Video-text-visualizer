from PIL import Image
from pathlib import Path
from tools import *
from tqdm import tqdm
import cv2
import os
import pickle
import translate


def gen_frames(workspace, video_path, frame_interval, text_file, data_file, scale_amount=0, colors="BINARY", verbose=True):
    os.makedirs(workspace, exist_ok=True)
    vidcap = cv2.VideoCapture(video_path)
    major_ver = (cv2.__version__).split('.')[0]
    if int(major_ver) < 3:
        fps = vidcap.get(cv2.cv.CV_CAP_PROP_FPS)
        video_frames = int(vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    else:
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        video_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(fps)

    translate_to_binary       = colors.upper() == "BINARY"
    translate_to_grayscale    = colors.upper() == "GRAYSCALE"

    generator = range(video_frames)
    if verbose:
        print(f"Processing {fps} frames every {frame_interval} frames... (This can take a while)")
        generator = tqdm(generator)
    count = 0
    frames = []
    for _ in generator:
        _, image = vidcap.read()
        if count % frame_interval == 0:
            print(f"Processing frame {len(frames)}/{video_frames}...")
            fullpath        = os.path.join(workspace, f"frame{count}.jpg")
            width           = int(image.shape[1] * scale_amount / 100)
            height          = int(image.shape[0] * scale_amount / 100)
            dsize           = (width, height)
            output          = cv2.resize(image, dsize)
            if translate_to_grayscale:
                output      = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(fullpath, output)
            image           = Image.open(fullpath)
            pix             = image.load()
            if translate_to_binary:
                pix         = binary_pixels(pix, image.size)
            input_string    = translate.parse_file(text_file)
            image_list      = translate.translate_image(image, input_string, translate_to_binary)
            frames.append(image_list)
            os.remove(fullpath)
        count += 1
    if verbose:
        print("Dumping data into file...")
    with open(data_file, "wb") as data_file: # Save the video's frame data to pickle file. I don't really like pickles. Too salty.
        pickle.dump(frames, data_file)
    cv2.destroyAllWindows()
    return fps


def gen_image(image_path, data_file, scale_amount=0, colors="BINARY"):
    # Generate one image. # TODO: Implement this. I got exams right now.
    os.makedirs(workspace, exist_ok=True)


def binary_pixels(pixels, image_dimensions):
    changed_pixels = pixels
    for x in range(image_dimensions[0]):
        for y in range(image_dimensions[1]):
            changed_pixels[x,y] = translate.color_to_binary(pixels[x,y])
    return changed_pixels


if __name__ == "__main__":
    os.chdir(Path(__file__).parent.absolute())
    video             = input("Please input the path to the video: ")
    text_file_path    = input("Please input the path to the text file with the text you would like to display: ")
    data_file_path    = input("Please input the file to store the animation data: ")
    frame_interval    = int(input("Please input the frame intervals: "))
    scale             = int(input("Please input the scale of the frames: "))
    workspace         = input("Please input the path of the folder you would like the program to work in\n(input \"default\" or nothing to work in default folder): ").lower()
    if workspace == "default" or workspace == "":
        workspace = "frames"
    if not data_file_path.endswith(".data"):
        data_file_path += ".data"
    if len(data_file_path.split(os.sep)) == 1:
        data_file_path = os.path.join("public_data", data_file_path)
    if not os.path.isabs(text_file_path):
        text_file_path = os.path.join("inputs", text_file_path)
    if not os.path.isabs(video):
        video = os.path.join("public_videos", video)
    if not video.endswith(".mp4"):
        print("Warning! The video you want to process isn't in .mp4 format. This can cause problems.")
        print("It's suggested to convert your video to .mp4 format before continuing. There are tons of easy-to-use converters online.")
        input("Press \"ENTER\" to continue.")
    if frame_interval == 0:
        frame_interval = 1
    prev_files = os.listdir(workspace)
    if len(prev_files) != 0:
        print("WARNING: The workspace folder is not empty.")
        print("In order to function correctly, the frames folder must be empty.")
        print("The program will automatically delete all files in the folder before running.")
        input("Press \"ENTER\" to continue, or press CTRL + C to exit.")
        for file_name in prev_files:
            os.remove(os.path.join(workspace, file_name))
    gen_frames(workspace, video, frame_interval, text_file_path, data_file_path, scale_amount=scale, colors="NONE")
