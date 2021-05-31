import colors
import pygame
import sys
pygame.init()


def render_text(message, font, topleft, surface, foregound=colors.BLACK, background=None, center=None):
    text = font.render(message, True, foregound, background)
    text_rect = text.get_rect()
    if center is not None:
        text_rect.center = center
    else:
        text_rect.topleft = topleft
    surface.blit(text, text_rect)
    return text_rect


def exit_program():
    pygame.quit()
    sys.exit()


def can_be(value, test_type):
    try:
        _ = test_type(value)
        return True
    except:
        return False


def isvalidpath(path):
    try:
        open(path, 'r')
        return True
    except IOError:
        try:
            open(path, 'w')
            return True
        except:
            return False