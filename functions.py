import pygame as py


def flip(surface):  # flips an image horizontally
    return py.transform.flip(surface, True, False)


def rotate(image, angle):  # degrees, neg is cw
    return py.transform.rotate(image, angle)


def load_image(path):
    return py.image.load(f"data/{path}")


def load_image_convert(path, surface):
    comparison_surf = surface
    return py.image.load(f"data/{path}").convert()