import pygame as py


def flip(surface):  # flips an image horizontally
    return py.transform.flip(surface, True, False)


def rotate(image, angle):  # degrees, neg is cw
    return py.transform.rotate(image, angle)


def load_image(path):
    return py.image.load(f"data/{path}")


def load_image_convert(path, surface):
    return py.image.load(f"data/{path}").convert(surface)


def point_rect_collision(point, rect):
    return rect[0] <= point[0] <= rect[0] + rect[2] and rect[1] <= point[1] <= rect[1] + rect[3]


def swap_color(img, old_c, new_c):  # credit partially given to DaFluffyPotato
    """

    :param img: the image whose color will be switched
    NOTE: img MUST have been loaded with .convert(), as normal alpha values will heck things up
    :param old_c: the color being replaced
    :param new_c: the color taking the place of the old
    :return: img surface with colors switched
    """
    img.set_colorkey(old_c)
    surf = img.copy()
    surf.fill(new_c)
    surf.blit(img, (0, 0))
    surf.set_colorkey((255, 233, 0))
    return surf
    # return img
