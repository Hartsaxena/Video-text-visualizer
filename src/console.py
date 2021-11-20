from copy import deepcopy
from tools import *
import clipboard
import colors
import constants
import os
import pickle
import preprocessor
import pygame
pygame.init()


clipboard.paste() # For some reason, the first command using clipboard is slow, so we'll just put it here.


def main_menu(screen):
    screen_dimensions = screen.get_size()
    screen_center     = (screen_dimensions[0] // 2, screen_dimensions[1] // 2)

    selected = False
    selected_option = "PLAY ANIMATION"
    spaces_inbetween = 13

    # Calculate how many pixels are used in spaces_inbetween spaces, then divide by 2.
    first_option_circle_offset = constants.console_font.render(" " * spaces_inbetween, True, colors.BLACK, colors.WHITE).get_rect().width // 2

    limit = pygame.time.Clock()
    while not selected:
        screen.fill(colors.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_d or event.key == pygame.K_a:
                    if selected_option == "PLAY ANIMATION":
                        selected_option = "PROCESS VIDEO"
                    elif selected_option == "PROCESS VIDEO":
                        selected_option = "PLAY ANIMATION"
                elif event.key == pygame.K_RETURN:
                    selected = True
            
        render_text("Select an option (Select by pressing \"Enter\"):", constants.console_font, None, screen, colors.NEON, center=(screen_center[0], 50))

        options_rect = render_text(f'''PLAY ANIMATION{" " * spaces_inbetween}PROCESS VIDEO''', constants.console_font, None, screen, colors.NEON, center=screen_center)

        if selected_option == "PLAY ANIMATION":
            pygame.draw.circle(screen, colors.NEON, (options_rect.topleft[0] - first_option_circle_offset, options_rect.centery), 20, width=3)
        elif selected_option == "PROCESS VIDEO":
            pygame.draw.circle(screen, colors.NEON, options_rect.center, 20, width=3)
        
        pygame.display.update()
        limit.tick(60)

        

    if selected_option == "PLAY ANIMATION":
        while True:
            data_file_name, fps, bg_color, binary_color = get_render_values(screen)
            screen.fill(colors.BLACK)
            render_text("Loading Frame Data...", constants.console_font, None, screen, colors.NEON, center=screen_center)
            pygame.display.update()
            try:
                with open(data_file_name, 'rb') as frame_data:
                    frames = pickle.load(frame_data)
                binary_render = data_file_name.endswith(".bdata")
                break
            except pickle.UnpicklingError:
                continue
        return fps, bg_color, binary_color, frames, binary_render
    
    elif selected_option == "PROCESS VIDEO":
        while True:
            workspace, video, text_file_path, data_file_path, frame_interval, scale, coloring_type = get_process_values(screen)
            screen.fill(colors.BLACK)
            rect1 = render_text("Processing Video...", constants.console_font, None, screen, colors.NEON, center=screen_center)
            render_text("(This can take a while.)", constants.console_font, None, screen, colors.NEON, center=(rect1.centerx, rect1.centery + rect1.height))
            pygame.display.update()
            # video_fps = preprocessor.gen_frames(workspace, video, frame_interval, text_file_path, data_file_path, scale, verbose=False)
            # break
            try:
                video_fps = preprocessor.gen_frames(workspace, video, frame_interval, text_file_path, data_file_path, scale, coloring_type, verbose=False)
                break
            except Exception:
                continue

        memorize_values = [f"Data file path: {data_file_path}", f"FPS: {video_fps}", f"Frame Intervals: {frame_interval}"]
        
        # Since the program is basically dead by this point, we don't need to constantly draw the exact same thing over and over again.
        screen.fill(colors.BLACK)

        rect1 = render_text("Finished Processing Video! Please restart this program and select \"PLAY ANIMATION\" Next time!", constants.console_font, None, screen, colors.NEON, center=screen_center)
        rect2 = render_text("Remember these values if you want to run the video you just processed: ", constants.console_font, None, screen, colors.NEON, center=(screen_center[0], screen_center[1] + rect1.height))
        next_pos = (rect2.centerx, rect2.centery + rect2.height) # NOTE: This is the center of the rects, not the topleft value.
        for message in memorize_values:
            message_rect = render_text(message, constants.console_font, None, screen, colors.NEON, center=next_pos)
            next_pos = (next_pos[0], next_pos[1] + message_rect.height)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_program()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    exit_program()


def check_data_file_name(data_file_name, return_bool=True):
    # Checks if data_file_name is valid. Only used twice.
    # TODO: Fix a couple bugs regarding this thing.
    result = data_file_name
    if not os.path.isfile(result):
        if result.endswith(".data"):
            result = data_file_name[:-5]
        os.makedirs("public_data", exist_ok=True)
        if f"{data_file_name}.data" in os.listdir("public_data"):
            result = os.path.join("public_data", f"{result}.data")
        
        if result.endswith(".bdata"):
            result = result[:-6]
        os.makedirs("public_data", exist_ok=True)
        if f"{result}.bdata" in os.listdir("public_data"):
            result = os.path.join("public_data", f"{result}.bdata")

    return (isvalidpath(result) and result.endswith(".bdata")) if return_bool else result


def is_valid_path(file_path):
    # checks if a file path is valid
    if os.path.isfile(file_path):
        return True
    elif os.path.isdir(file_path):
        return False
    try:
        open(file_path, 'a')
    except FileNotFoundError:
        return False
    return True


def get_render_values(surface):
    # The cool console window to get values from the user (values for playing animation).
    current_prompt        = 0
    messages_to_render    = []

    data_file_name_prompt = "Please input the name of the datafile to load: "
    fps_prompt            = "Please input the fps (frames per second) of the video: "
    interval_prompt       = "Please input the interval between frames of the files: "
    bg_color_prompt       = f"Please input the background color {tuple([color for color in colors.bg_colors.keys()])}: "
    binary_color_prompt   = "Please input the color of the letters (NEON, BLACK, or WHITE): " # This only appears if data_file_name_prompt is a .bdata file.

    all_prompts       = [data_file_name_prompt, fps_prompt, interval_prompt, bg_color_prompt]
    default_prompts   = deepcopy(all_prompts)
    prompt_messages   = {prompt: "" for prompt in all_prompts}

    limit = pygame.time.Clock()
    exit = False
    while not exit:
        surface.fill(colors.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program()
            elif event.type == pygame.KEYDOWN:
                answering_prompt = all_prompts[current_prompt]
                current_pressed = pygame.key.get_pressed()

                if event.key == pygame.K_BACKSPACE:
                    if len(prompt_messages[answering_prompt]) != 0:
                        prompt_messages[answering_prompt] = prompt_messages[answering_prompt][:-1]
                elif event.key == pygame.K_RETURN:
                    if (answering_prompt == bg_color_prompt) and (binary_color_prompt not in all_prompts):
                        if check_data_file_name(prompt_messages[data_file_name_prompt]):
                            prompt_messages[binary_color_prompt] = ""
                            all_prompts.append(binary_color_prompt)

                    if current_prompt < len(all_prompts) - 1:
                        current_prompt += 1
                    else:
                        data_file_name    = prompt_messages[data_file_name_prompt]
                        fps               = prompt_messages[fps_prompt]
                        interval          = prompt_messages[interval_prompt]
                        bg_color          = prompt_messages[bg_color_prompt]

                        if binary_color_prompt in all_prompts:
                            binary_color = prompt_messages[binary_color_prompt].upper()

                        data_file_name = check_data_file_name(data_file_name, return_bool=False)
                        
                        if not interval:
                            interval = 1

                        conditions = [
                            os.path.isfile(data_file_name),
                            can_be(fps, float),
                            can_be(interval, int),
                            bg_color.upper() in colors.bg_colors,
                        ]

                        if binary_color_prompt in all_prompts:
                            conditions.append(binary_color in colors.all_colors)

                        conditions_met = all(conditions)
                        if not conditions_met:
                            all_prompts       = default_prompts
                            prompt_messages   = {prompt: "" for prompt in all_prompts}
                            current_prompt    = 0
                        else:
                            bg_color = colors.bg_colors[bg_color.upper()]
                            if binary_color_prompt not in all_prompts:
                                binary_color = None
                            else:
                                binary_color = colors.all_colors[binary_color]
                            exit = True

                elif event.key == pygame.K_v and any(current_pressed[key] for key in constants.cmd_keys):
                    prompt_messages[answering_prompt] += clipboard.paste()
                    

                elif answering_prompt == fps_prompt or answering_prompt == interval_prompt:
                    if event.key in constants.number_keys or event.key == pygame.K_PERIOD:
                        prompt_messages[answering_prompt] += event.unicode
                else:
                    prompt_messages[answering_prompt] += event.unicode

        messages_to_render = [prompt + answer for prompt, answer in prompt_messages.items()]
        next_position = (20, 20)
        for msg_index in range(current_prompt + 1):
            text_rect = render_text(messages_to_render[msg_index], constants.console_font, next_position, surface, colors.NEON)
            next_position = (next_position[0], next_position[1] + 35)
        
        pygame.draw.rect(surface, colors.NEON, (text_rect.topright[0], text_rect.topright[1] + 5, 12, 30)) # Draw the cursor.

        pygame.display.update()
        limit.tick(60)

    result = (data_file_name, float(fps) / int(interval), bg_color, binary_color)
    return result



def get_process_values(surface):
    # The cool console window to get values from the user (values for processing video).
    current_prompt        = 0
    messages_to_render    = []

    video_prompt            = "Please input the path to the video: "
    text_file_prompt        = "Please input the path to the text file: "
    data_file_prompt        = "Please input the file to store the animation data: "
    frame_interval_prompt   = "Please input the frame intervals: "
    scale_prompt            = "Please input the scale of the frames (in percent): "
    color_type_prompt       = "[EXP] Please input the coloring you would like to use (COLORED, GRAYSCALE, or BINARY): "

    all_prompts         = [video_prompt, text_file_prompt, data_file_prompt, frame_interval_prompt, scale_prompt, color_type_prompt]
    numbered_prompts    = [frame_interval_prompt, scale_prompt]
    prompt_messages     = {prompt: "" for prompt in all_prompts}
    limit               = pygame.time.Clock()
    exit_loop                = False
    while not exit_loop:
        surface.fill(colors.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program()
            if event.type == pygame.KEYDOWN:
                answering_prompt = all_prompts[current_prompt]
                current_pressed = pygame.key.get_pressed()

                if event.key == pygame.K_BACKSPACE:
                    if len(prompt_messages[answering_prompt]) != 0:
                        if any(current_pressed[key] for key in constants.cmd_keys):
                            prompt_messages[answering_prompt] = ""
                        else:
                            prompt_messages[answering_prompt] = prompt_messages[answering_prompt][:-1]
                elif event.key == pygame.K_RETURN:
                    if current_prompt < len(all_prompts) - 1:
                        current_prompt += 1
                    else:
                        video_path             = prompt_messages[video_prompt]
                        text_file_path    = prompt_messages[text_file_prompt]
                        data_file_path    = prompt_messages[data_file_prompt]
                        frame_interval    = prompt_messages[frame_interval_prompt]
                        scale             = prompt_messages[scale_prompt]
                        color_type        = prompt_messages[color_type_prompt].upper()
                        workspace         = "frames"

                        # Now we do some "smart" detection of files
                        os.makedirs(workspace, exist_ok=True)

                        if not os.path.isabs(video_path):
                            if "public_videos" not in video_path.split(os.sep):
                                video_path = os.path.join("public_videos", video_path)
                            if "." not in video_path:
                                video_path += ".mp4"

                        if not os.path.isabs(text_file_path):
                            if "public_text" not in text_file_path.split(os.sep):
                                text_file_path = os.path.join("public_text", text_file_path)
                        
                        if color_type != "COLORED" and color_type != "GRAYSCALE":
                            color_type = "BINARY"
                        if color_type != "BINARY":
                            if not data_file_path.endswith(".data"):
                                data_file_path += ".data"
                        else:
                            if not data_file_path.endswith(".bdata"):
                                data_file_path += ".bdata"

                        if not os.path.isabs(data_file_path):
                            data_file_path = os.path.join("public_data", data_file_path)
                        
                        if frame_interval == "0":
                            frame_interval = 1

                        # Check if all the values are valid.
                        conditions = [
                            os.path.isfile(video_path),
                            os.path.isfile(text_file_path),
                            isvalidpath(data_file_path),
                            can_be(frame_interval, int),
                            can_be(scale, int),
                        ]
                        conditions_met = all(conditions)
                        if not conditions_met:
                            all_prompts       = [video_prompt, text_file_prompt, data_file_prompt, frame_interval_prompt, scale_prompt, color_type_prompt]
                            prompt_messages   = {prompt: "" for prompt in all_prompts}
                            current_prompt    = 0
                            print(conditions)
                        else:
                            frame_interval    = int(frame_interval)
                            scale             = int(scale)
                            exit_loop = True
                elif event.key == pygame.K_v and any(current_pressed[key] for key in constants.cmd_keys):
                    prompt_messages[answering_prompt] += clipboard.paste()
                    

                elif any([answering_prompt == answer for answer in numbered_prompts]):
                    if event.key in constants.number_keys or event.key == pygame.K_PERIOD:
                        prompt_messages[answering_prompt] += event.unicode
                else:
                    prompt_messages[answering_prompt] += event.unicode

        messages_to_render = [prompt + answer for prompt, answer in prompt_messages.items()]
        next_position = (20, 20)
        for msg_index in range(current_prompt + 1):
            text_rect = render_text(messages_to_render[msg_index], constants.console_font, next_position, surface, colors.NEON)
            next_position = (next_position[0], next_position[1] + 35)
        
        pygame.draw.rect(surface, colors.NEON, (text_rect.topright[0], text_rect.topright[1] + 5, 12, 30)) # Draw the cursor.

        pygame.display.update()
        limit.tick(60)

    result = (workspace, video_path, text_file_path, data_file_path, frame_interval, scale, color_type)
    return result