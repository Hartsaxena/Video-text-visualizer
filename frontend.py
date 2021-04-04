from pathlib import Path
import colors
import os
import pickle
import sys
import translate
import pygame
pygame.init()


screen_dimensions = (2560, 1440)
screen = pygame.display.set_mode(screen_dimensions)
clock = pygame.time.Clock()

default_font    = pygame.font.Font(os.path.join("fonts", "Consolas.ttf"), 12)
prompt_font     = pygame.font.Font(os.path.join("fonts", "Consolas.ttf"), 30)

def render_text(message, font, topleft, foregound=colors.BLACK, background=None, surface=screen, center=None):
    text = font.render(message, True, foregound, background)
    text_rect = text.get_rect()
    if center is not None:
        text_rect.center = center
    else:
        text_rect.topleft = topleft
    surface.blit(text, text_rect)
    return text_rect


def number_update(source_text, keys, holdings):
    # This is for numbered text prompts
    # Keep in mind that giving a function a list as an argument allows the function to change the list.
    result = ""
    text = source_text
    if keys[pygame.K_0] and not holdings[0]:
        result += "0"
        holdings[0] = True
    elif not keys[pygame.K_0]:
        holdings[0] = False
    if keys[pygame.K_1] and not holdings[1]:
        result += "1"
        holdings[1] = True
    elif not keys[pygame.K_1]:
        holdings[1] = False
    if keys[pygame.K_2] and not holdings[2]:
        result += "2"
        holdings[2] = True
    elif not keys[pygame.K_2]:
        holdings[2] = False
    if keys[pygame.K_3] and not holdings[3]:
        result += "3"
        holdings[3] = True
    elif not keys[pygame.K_3]:
        holdings[3] = False
    if keys[pygame.K_4] and not holdings[4]:
        result += "4"
        holdings[4] = True
    elif not keys[pygame.K_4]:
        holdings[4] = False
    if keys[pygame.K_5] and not holdings[5]:
        result += "5"
        holdings[5] = True
    elif not keys[pygame.K_5]:
        holdings[5] = False
    if keys[pygame.K_6] and not holdings[6]:
        result += "6"
        holdings[6] = True
    elif not keys[pygame.K_6]:
        holdings[6] = False
    if keys[pygame.K_7] and not holdings[7]:
        result += "7"
        holdings[7] = True
    elif not keys[pygame.K_7]:
        holdings[7] = False
    if keys[pygame.K_8] and not holdings[8]:
        result += "8"
        holdings[8] = True
    elif not keys[pygame.K_8]:
        holdings[8] = False
    if keys[pygame.K_9] and not holdings[9]:
        result += "9"
        holdings[9] = True
    elif not keys[pygame.K_9]:
        holdings[9] = False
    
    if keys[pygame.K_BACKSPACE] and not holdings[10]:
        if len(text) > 0:
            text = text[:-1]
            holdings[10] = True
    elif not keys[pygame.K_BACKSPACE]:
        holdings[10] = False
    
    return text + result


def exit_program():
    pygame.quit()
    sys.exit()


def main():
    data_file_name = input("Please input the name of the datafile to load: ")
    fps = int(input("Please input the fps (frames per second) of the video: "))
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
        print("Done!")

    currentframe_index        = 0
    first_frame               = True
    text_positions            = []
    fps                       = fps / interval
    pause                     = False
    holding_space             = False
    holding_g                 = False
    holding_nums              = [False for _ in range(11)]
    frame_prompt              = False
    frame_prompt_ans          = ""
    total_frames              = len(frames)
    frame_prompt_dimensions   = ((500, 100))
    frame_prompt_surface      = pygame.Surface(frame_prompt_dimensions)
    frame_prompt_center       = (frame_prompt_dimensions[0] // 2, frame_prompt_dimensions[1] // 2)
    while True:
        screen.fill(colors.WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program()
        
        current_frame   = frames[currentframe_index]
        full_message    = translate.string_listlist(current_frame).split("\n")
        if first_frame:
            first_frame = False
            next_position = (0, 0)
            for message in full_message:
                render_text(message, default_font, next_position)
                text_positions.append(next_position)
                next_position = (next_position[0], next_position[1] + 8)
        else:
            for message_index in range(len(full_message)):
                message = full_message[message_index]
                render_text(message, default_font, text_positions[message_index])
        
        if frame_prompt:
            frame_prompt_surface.fill(colors.GRAY)
            render_text(f"{frame_prompt_ans} / {total_frames}", prompt_font, None, surface=frame_prompt_surface, center=frame_prompt_center)
            screen.blit(frame_prompt_surface, (screen_dimensions[0] // 2 - 250, 0))

        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and holding_space == False and not frame_prompt:
            pause = not pause
            holding_space = True
        elif not keys[pygame.K_SPACE]:
            holding_space = False

        if pause:
            if keys[pygame.K_RIGHT]:
                currentframe_index += 1
            elif keys[pygame.K_LEFT]:
                if currentframe_index > 0:
                    currentframe_index -= 1
            
            if keys[pygame.K_g] and holding_g == False:
                frame_prompt = not frame_prompt
                holding_g = True
            elif not keys[pygame.K_g]:
                holding_g = False
            
            if keys[pygame.K_RETURN] and frame_prompt and frame_prompt_ans != "":
                try:
                    frame_prompt_ans    = int(frame_prompt_ans)
                    frame_prompt_ans    = translate.clamp(frame_prompt_ans, 0, total_frames - 1)
                    currentframe_index  = frame_prompt_ans
                    frame_prompt_ans    = str(frame_prompt_ans)
                    frame_prompt        = False
                except ValueError:
                    frame_prompt_ans = ""
            if frame_prompt:
                frame_prompt_ans = number_update(frame_prompt_ans, keys, holding_nums)

        if not pause:
            currentframe_index += 1
        if currentframe_index >= total_frames:
            exit_program()
        pygame.display.update()
        clock.tick(fps)



if __name__ == "__main__":
    main()