from pathlib import Path
from time import perf_counter
from tools import *
import colors
import console
import constants
import pygame
import translate
pygame.init()


def main(screen):
    fps, bg_color, binary_color, frames, binary_render = console.main_menu(constants.game_surface)
    screen_dimensions, screen_center = constants.screen_dimensions, constants.screen_center

    currentframe_index        = 0
    pause                     = False
    frame_prompt              = False
    frame_prompt_ans          = ""
    end_timing                = False
    total_frames              = len(frames)
    frame_prompt_surface      = pygame.Surface(constants.frame_prompt_dimensions)
    frame_prompt_center       = (constants.frame_prompt_dimensions[0] // 2, constants.frame_prompt_dimensions[1] // 2)
    clock                     = pygame.time.Clock()
    binary_line_positions     = []
    firstframe                = True


    while True:
        screen.fill(bg_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program()
            if event.type == pygame.KEYDOWN:
                if frame_prompt:
                    if event.key in constants.number_keys:
                        frame_prompt_ans += event.unicode
                    elif event.key == pygame.K_BACKSPACE and len(frame_prompt_ans) != 0:
                        frame_prompt_ans = frame_prompt_ans[:-1]
                elif event.key == pygame.K_SPACE:
                    pause = not pause

                if event.key == pygame.K_g and pause:
                    if frame_prompt:
                        frame_prompt = False
                    else:
                        frame_prompt_ans = str(currentframe_index)
                        frame_prompt = True                
                if event.key == pygame.K_q:
                    end_time = perf_counter() + 3
                    end_timing = True
        
        current_frame = frames[currentframe_index]

        if binary_render:
            full_message = translate.string_listlist(current_frame).split("\n")
        else:
            full_message = []
            for row in current_frame:
                for col in row:
                    full_message.append(col)
                full_message.append("\n")

        next_position = (0, 0)

        if binary_render:
            if firstframe:
                for message in full_message:
                    render_text(message, constants.default_font, next_position, screen, binary_color)
                    binary_line_positions.append(next_position)
                    next_position = (0, next_position[1] + 8)
            else:
                for message_index in range(len(full_message)):
                    message = full_message[message_index]
                    render_text(message, constants.default_font, binary_line_positions[message_index], screen, binary_color)
            

        else:
            for message in full_message:
                if message != "\n":
                    text, color = message
                    render_text(text, constants.default_font, next_position, screen, color)
                    next_position = (next_position[0] + constants.consolas_widths["default"], next_position[1])
                else:
                    next_position = (0, next_position[1] + 8)
        
        if frame_prompt:
            frame_prompt_surface.fill(colors.BLACK)
            pygame.draw.rect(frame_prompt_surface, colors.GRAY, (5, 5, constants.frame_prompt_dimensions[0] - 10, constants.frame_prompt_dimensions[1] - 10))
            render_text(f"{frame_prompt_ans} / {total_frames - 1}", constants.prompt_font, None, surface=frame_prompt_surface, center=frame_prompt_center)
            screen.blit(frame_prompt_surface, (screen_center[0] - 250, 0))

        
        keys = pygame.key.get_pressed()

        if pause:
            if keys[pygame.K_RIGHT]:
                if currentframe_index <= total_frames - 1:
                    currentframe_index += 1
            elif keys[pygame.K_LEFT]:
                if currentframe_index > 0:
                    currentframe_index -= 1
            
            if keys[pygame.K_RETURN] and frame_prompt and frame_prompt_ans != "":
                try:
                    frame_prompt_ans    = int(frame_prompt_ans)
                    frame_prompt_ans    = translate.clamp(frame_prompt_ans, 0, total_frames - 1)
                    currentframe_index  = frame_prompt_ans
                    frame_prompt_ans    = str(frame_prompt_ans)
                    frame_prompt        = False
                except ValueError:
                    frame_prompt_ans    = ""
        
        if keys[pygame.K_q]:
            if perf_counter() >= end_time and end_timing:
                exit_program()
        else:
            end_timing = False


        if not pause:
            currentframe_index += 1
        if currentframe_index >= total_frames:
            currentframe_index = total_frames - 1
        currentframe_index = translate.clamp(currentframe_index, 0, total_frames)

        if firstframe:
            firstframe = False

        pygame.display.update()
        clock.tick(fps)



if __name__ == "__main__":
    main(constants.game_surface)