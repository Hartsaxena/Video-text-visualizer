import pygame
import os
pygame.init()

game_surface        = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_dimensions   = game_surface.get_size()
screen_center       = (screen_dimensions[0] // 2, screen_dimensions[1] // 2)

number_keys   = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
cmd_keys      = [pygame.K_LSUPER, pygame.K_RSUPER, pygame.K_RCTRL, pygame.K_LCTRL]
frame_prompt_dimensions   = ((500, 100))

# Fonts
font_size       = game_surface.get_height() / 1440

consolas_sizes = {
    "default": 12,
    "prompt": 30,
}

default_font    = pygame.font.Font(os.path.join("fonts", "Consolas.ttf"), int(consolas_sizes["default"] * font_size))
prompt_font     = pygame.font.Font(os.path.join("fonts", "Consolas.ttf"), int(consolas_sizes["prompt"] * font_size))
console_font    = pygame.font.Font(os.path.join("fonts", "FiraCode.ttf"), int(30 * font_size))

consolas_widths = {use: 55/100 * font_size for use, font_size in consolas_sizes.items()} # Consolas font's width if 55% font size. At least, I hope the internet didn't lie.
