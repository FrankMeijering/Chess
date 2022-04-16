import pygame as pg
import os


def get_file(file):
    # Returns the full path, if the file is in the same folder as the main .py program.
    # Useful if a computer uses some random directory (like mine)
    path = os.path.join(os.path.dirname(__file__), file)
    return path


def get_folder_file(folder, file):
    # Returns the full path, if the file is not in the same folder as the main .py program.
    # Useful if a computer uses some random directory (like mine)
    extension = os.path.join(folder, file)
    path = get_file(extension)
    return path


def resize(img, factor):
    # Img should be a surface
    resolution = img.get_size()
    new_reso = (int(resolution[0] * factor), int(resolution[1] * factor))
    return new_reso


def makeimg(name, transparent, factor):
    # all images have to be in the 'Images' folder. Transparent should be a boolean. Scaling factor is equal for
    # every image.
    img = pg.image.load(get_folder_file("Images", name))
    if transparent:
        img = pg.transform.smoothscale(img, resize(img, factor)).convert_alpha()
    else:
        img = pg.transform.smoothscale(img, resize(img, factor)).convert()
    rect = img.get_rect()
    return img, rect
