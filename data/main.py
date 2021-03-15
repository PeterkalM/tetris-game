import os
import pygame

# Default variables for paths
main_dir = os.path.split(os.path.abspath(__file__))[0]


def load_image(name):
    """ Load image

        Functions loads image, and converts it to display sizes
        so later it can be blited faster.
    """
    fullname = os.path.join(main_dir, "images", name)

    image = pygame.image.load(fullname)
    image = image.convert_alpha()

    return image


def load_font(name, size):
    """ Load font

        Funtions tries to load font specified by name argument
        but if it fails then loads pygame default font
    """
    fullname = os.path.join(main_dir, "fonts", name)

    try:
        font = pygame.font.Font(fullname, size)
    except OSError:
        print("Cannot load font:", fullname)
        font = pygame.font.Font(None, size)
        print("Replaced it with default font.")

    return font


class NoneSound:
    def play(self):
        pass

    def stop(self):
        pass


def load_music(name):
    """ Load music """

    fullname = os.path.join(main_dir, "music", name)

    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print("Cannot load font:", fullname)
        sound = NoneSound()
        print("Replaced it with default font.")

    return sound


def load_sfx(name):
    """ Load sound """

    fullname = os.path.join(main_dir, "sfx", name)
    try:

        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print("Cannot load sound:", fullname)
        sound = NoneSound()
        print("Replaced it with default sound.")

    return sound
