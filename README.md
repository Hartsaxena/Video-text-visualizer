# Video-text-visualizer
I made this little project in about 2 days.

Basically, you give this program a video and some text, and it will play the video in black white, except the black pixels are your text.
Keep in mind that this program was not written with efficiency in mind.
Although playing the video won't be too slow (as long as your video's frames aren't too large), processing the video before playing it will take some time.

prerequisites:
I created this program for python version 3.7.7
Other versions of python might work with this project, but I haven't tested any other versions so run at your own risk!
Before running any files, run `pip install requirements.txt` in your console. Keep in mind that "requirements.txt" in this context is the requirements.txt file in the project.

Keep in mind that although this program was written for cross-platform compatibility (it was made to be used for Linux, macOS, and Windows), it has only been tested on macOS.
This program isn't as simple as running main.py, so you'll probably want to read the instructions first.


Instructions:

1. Get a video file. For safety, this should be in .mp4 format. Don't make it too long, and remember that the video will be played in black and white.
2. For simplicity, place this video file into the project's "public_videos" folder.
3. Put some text into a text file. For simplicity, place this file into the project's "inputs" folder.
4. Run the project's preprocessor.py file using `python preprocessor.py` in your computer's Console (Terminal for macOS and Linux, Command Prompt for Windows)
5. Fill out the prompts given to you:
Please input the path to the video: Just input the name of the .mp4 file you put in the "public_videos" folder previously. Keep in mind that the name is case-sensitive. If your file is called "video.mp4", "Video.mp4" won't work.

Please input the path to the text file with the text you would like to display: Input the name of the text file you put your text into, for example "loremipsum.txt"
WARNING: If you're editing a text file on macOS, don't use Rich text. Just use plain text. Google how to change your Text Edit.app's settings to use plain text.

Please input the file to store the animation data: Input a name for the file you want to store the process data in. Basically, make up a name for a file. Avoid using special characters (!, +, #, /), since these can cause problems. Remember the name of this file.

Please input the frame intervals: Input the amount of frames in the video you would like to skip every frame when you play the video in the end. If you want a super smooth video, just input 1. Remember this number

Please input the scale of the frames: Input a percent of how much you want to shrink the image to. Keep in mind that when you play the video in text format in the end, every pixel is a letter, so it's recommend to shrink the images to dimensions around (240, 180)
Example: inputting "70" will shrink the frames to 70% of the original video's frames.

Please input the path of the folder you would like the program to work in: I'm not sure why this is even a prompt, to be honest. Just input nothing.
NOTE: The program may raise a Warning, saying that the workspace folder isn't empty. As long as you inputted nothing in the previous prompt, you'll be fine. Press enter.

Look! A Progress bar!
Depending on what parameters you inputted, this can either be real fast or real slow. Just be patient.

Here's some fun facts to read while you wait:

The first person to ever get convicted of speeding only went 8 miles per hour.

The heads on Easter Island actually do have bodies.

When you're on a flight, you lose 30% of your taste buds. This could be why you don't like airplane food (although I personally like airplane food). Don't worry though! You get your taste buds back after the flight.

The M's in "M&M's" stand for "Mars" and "Murrie".

That last program took quite a while! Don't worry, it's pretty smooth from here.

6. Run `python main.py` in your computer's console. Keep in mind that the "main.py" is the filepath to the "main.py" file in the project.
7. Fill out the prompts:

Please input the name of the datafile to load: Input the filename you made up in the prompt "Please input the file to store the animation data:"

Please input the fps (frames per second) of the video: Input the fps you want to play the video at. Keep in mind that different videos have different fps's, although from my experience, a lot of them are either 60 fps or 30 fps.

Please input the interval between frames of the file: Input the number you inputted in the prompt "Please input the frame intervals:"

If everything goes well, you should see the text "Loading frame data..." Just wait.

Once the console says "Done!", you should see a big window open up with your animation playing. There are a couple controls I added to the window.

Controls:

Space - Pause and Unpause the animation.

g - If you press g while the animation is paused, a prompt will come up allowing you to go to a specific frame. Keep in mind that if you put a frame number that is smaller than 0, the program will round your answer to 0. Same goes for inputting a higher number than the total amount of frames in the animation. Once you've input a number, press enter.

Right and Left Arrows: If you press the Right and Left arrows while the animation is paused, you can go forward in time and backward in time, respectively.

