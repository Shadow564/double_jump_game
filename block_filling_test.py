import random as r
import pygame as py


def rotate(image, angle):  # degrees, neg is cw
    return py.transform.rotate(image, angle)


def splice_rects(rects, scale):
    """
    takes every rect in list, breaks it up into points [x, y] where each point represents a square of scale size so
    a rect(0, 0, 10, 20) with scale 10 would return
    [[0, 0], [0, 10]]
    :param rects: list of rects to be broken up
    :param scale: size of squares
    :return: list of points
    """
    points = []
    for rect in rects:
        if rect.width == scale and rect.height == scale:
            points.append([rect.x, rect.y])
        else:
            for x in range(rect.x, rect.right, scale):
                for y in range(rect.y, rect.bottom, scale):
                    points.append([x, y])
    return points
        

def i_hate_coding(rects, scale):
    """
    takes the list of points and breaks it up into on of four blocks
    a square block of scale size
    a line that is is scale by 2scale
    a L shape that is 2scale by 2scale with one corner missing
    a 2scale by 2scale square
    this isn't really commented, sorry
    
    In short, it picks a random point, and contiues to build it out into one of the blocks
    with randomness and does this until all the rects are used
    :param rects: rect points given by splice_rects()
    :param scale: scale of square points in rects
    :return: list of broken up blocks
    """
    # print("!!!!!!!!NEW BREAK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    blocks = []
    using_rects = rects.copy()
    while using_rects:
        # print("######NEW BLOCK########")
        block = [[], []]
        target = r.choice(using_rects)
        # print(f"Target: {target}")
        block[0].append(target)
        using_rects.remove(target)
        if r.randint(0, 4) != 4:
            # print("past single")
            possible_neighbors = []
            for n_pair in [[-1, 0, "left"], [1, 0, "right"], [0, -1, "up"], [0, 1, "down"]]:
                if [target[0] + n_pair[0] * scale, target[1] + n_pair[1] * scale] in using_rects:
                    possible_neighbors.append([target[0] + n_pair[0] * scale, target[1] + n_pair[1] * scale, n_pair[2]])
            if not possible_neighbors:
                # print("fail line")
                blocks.append(block)
            else:
                target = r.choice(possible_neighbors)
                using_rects.remove(target[:-1])
                block[0].append(target[:-1])
                block[1].append(target[2])
                if r.randint(0, 2) != 2:
                    # print("past line")
                    possible_neighbors = []
                    if block[1][0] in ["up", "down"]:
                        for n_pair in [[-1, "left"], [1, "right"]]:
                            if [target[0] + n_pair[0] * scale, target[1]] in using_rects:
                                possible_neighbors.append([target[0] + n_pair[0] * scale, target[1], n_pair[1]])
                    elif block[1][0] in ["left", "right"]:
                        for n_pair in [[-1, "up"], [1, "down"]]:
                            if [target[0], target[1] + n_pair[0] * scale] in using_rects:
                                possible_neighbors.append([target[0], target[1] + n_pair[0] * scale, n_pair[1]])
                    if not possible_neighbors:
                        # print("fail L")
                        blocks.append(block)
                    else:
                        target = r.choice(possible_neighbors)
                        using_rects.remove(target[:-1])
                        block[0].append(target[:-1])
                        block[1].append(target[2])
                        if r.randint(0, 3) != 3:  #
                            # print("past L")
                            if [block[0][0][0], block[0][2][1]] in using_rects:
                                block[0].append([block[0][0][0], block[0][2][1]])
                                block[1].append("squared_off")
                                using_rects.remove([block[0][0][0], block[0][2][1]])
                                blocks.append(block)
                            else:
                                # print("fail square")
                                blocks.append(block)
                        else:
                            blocks.append(block)
                else:
                    blocks.append(block)
                    
        else:
            blocks.append(block)
        # print(f"Remaining rects: {using_rects}")
        # print(len(using_rects))
        # print(f"Block created: {block}")
        # print(len(block[0]))
    # print(blocks)
    return blocks


def generate_images(broken):
    # turns the list of blocks into images
    square_img = py.image.load("data/square.png").convert()
    line_img = py.image.load("data/line.png").convert()
    big_square_img = py.image.load("data/big_square.png").convert()
    L_img = py.image.load("data/L.png").convert()
    L_img = py.image.load("data/L.png").convert()

    image_placements = []
    for block in broken:
        if not block[1]:  # single
            image_placements.append([block[0][0], square_img])
        elif len(block[1]) == 1:  # line
            if block[1][0] in ["up", "down"]:
                image_placements.append([[block[0][0][0], min(block[0][0][1], block[0][1][1])], line_img])
            elif block[1][0] in ["right", "left"]:
                image_placements.append([[min(block[0][0][0], block[0][1][0]), block[0][0][1]], rotate(line_img, 90)])
        elif len(block[1]) == 2:  # L
            d = {"upright": "nw", "upleft": "ne", "downright": "sw", "downleft": "se",
                 "leftup": "sw", "leftdown": "nw", "rightup": "se", "rightdown": "ne"}
            direction = d["".join(block[1])]
            pos = (min(block[0][0][0], block[0][1][0], block[0][2][0]),
                   min(block[0][0][1], block[0][1][1], block[0][2][1]))
            d2 = {"nw": 0, "se": 180, "ne": -90, "sw": 90}
            image_placements.append([pos, rotate(L_img, d2[direction])])
        elif len(block[1]) == 3:  # big square:
            pos = (min(block[0][0][0], block[0][1][0], block[0][2][0], block[0][3][0]),
                   min(block[0][0][1], block[0][1][1], block[0][2][1], block[0][3][1]))
            image_placements.append([pos, big_square_img])
        else:
            print(block)
    return image_placements
