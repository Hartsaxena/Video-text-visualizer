import sys
import os
from pathlib import Path
if sys.executable.endswith("main"):
    os.chdir(os.path.dirname(sys.executable))
    print(f"Running from {os.getcwd()}")
else:
    os.chdir(Path(__file__).parent.absolute())

import frontend
import constants

if __name__ == "__main__":
    frontend.main(constants.game_surface)
    # import pickle
    # # TODO: Fix Grayscale video saving + loading. Run this and you'll see what I mean.
    # with open("public_data/great.data", 'rb') as pickle_file:
    #     thing = pickle.load(pickle_file)
    #     print(thing)