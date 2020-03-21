import pygame as py
from pygame.locals import *
from event_class import EventKeep
import json
from player_class import Player
from block_filling_test import splice_rects, i_hate_coding, generate_images
import random as r

clock = py.time.Clock()  # maintains fps & junk

event = EventKeep()  # handles events from keyboard and mouse

"""
The screen is 720 x 720, but all blits are done onto a 240 x 240 screen
which is scaled up by x3 and blited at 0,0
"""
WIDTH = 720  # 240
HEIGHT = 720
SCALE = 3

screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Do the Double Jump")  # sets window caption
display = py.Surface((int(WIDTH / SCALE), int(WIDTH / SCALE)))  # suface all bliting is done onto


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


def load_animations():
    """
    Uses data dir to load animations into a dict
    (i commented this function a will ago, I don't remember what I put lol)
    :return: dictionary of animations and timings
    """
    animations = {}
    for dir in ["player"]:  # cycles through each directory in the animations folder
        with open(f"data/animations/{dir}/{dir}_timings", "r") as f:
            data = json.load(f)
        # the json file in each dir is used to load each needed animation
        
        for cycle in data:
            """
            for each animation in the json file, each duration under the cycle is put with a image surface with each
            given json entry in a list, and that list is going to be added to the frames of the animation

            """
            animations[cycle] = []  # the list used to represent the animation
            frames = []  # list of image, duration pairs
            for i in range(0, len(data[cycle][0])):  # cycles from 0 to the number of duration's in the file
                image = py.image.load(f"data/animations/{dir}/{dir}_{cycle}/player_{cycle}{i}.png").convert_alpha()
                # the upper line loads the image in the action's image dir that corresponds with the duration
                duration = data[cycle][0][i]  # the entry in the json file
                frames.append([image, duration])  # adds a list of the image and duration to the frames
            animations[cycle].append(frames)  # adds the list of image, dur pairs
            animations[cycle].append(data[cycle][1])
            """
            the line prior adds the second half of the json entry onto the animation
            currently, this is unused but is being included to allow for a future animation tag system

            """
    return animations


animations = load_animations()

player = Player((WIDTH / SCALE) / 2, (HEIGHT / SCALE) / 2, 1, 0, 5, 12)
scroll = [0, 0]

with open("data/levels/export_level", "r") as f:
    data = json.load(f)

export_rects = []
for rect in data["collision_rects"]:
    export_rects.append(py.Rect(rect))

# splits the rects into points [x, y] based on each point being a square with scale (12) sides
spliced = splice_rects(export_rects, 12)

# the fist color is inside the shape, the second is outside the shape
base_colors = [(127, 127, 127), (0, 0, 0)]
color_scheme = [[(255, 128, 164), (255, 38, 116)],  # pink
                [(191, 255, 60), (16, 210, 117)],  # green
                [(148, 33, 106), (67, 0, 103)],  # purple
                [(104, 174, 212), (35, 73, 117)]]  # blue

num = -1  # temporary counter


# generates new images to put over the rects
def generates_new_images(rect_points, scale):
    step_1 = i_hate_coding(rect_points, scale)
    step_2 = generate_images(step_1)
    for part in step_2:
        color_set = r.choice(color_scheme)
        part[1] = swap_color(part[1], base_colors[0], color_set[0])
        part[1] = swap_color(part[1], base_colors[1], color_set[1])
    return step_2


while True:
    num += 1
    
    display.fill((255, 255, 255))
    
    player.handle_veloctiy(event, export_rects)
    player.handle_animations(animations)
    
    player.draw_player(display, scroll)
    
    # temporarily prevents out of bounds falling by giving the player an upward boost in velocity
    if player.hitbox.y > 240:
        player.velocity[1] = -6
    
    # takes a all given events from mouse & keyboard and puts them in class object
    event.take_events()
    
    # adds the difference between the players coordinate and the scrolls displacement
    # tbh this isn't really my idea; credit goes to DaFluffyPotato; he is a god w/ pygame
    scroll[0] += int((player.x - scroll[0] - 120) / 2)
    scroll[1] += int((player.y - scroll[1] - 120) / 2)
    
    if num % 60 == 0:  # every second
        images = generates_new_images(spliced, 12)  # generates the masks to put on the collision rects
    for part in images:
        display.blit(part[1], (part[0][0] - scroll[0], part[0][1] - scroll[1]))

    screen.blit(py.transform.scale(display, (WIDTH, HEIGHT)), (0, 0))  # scales display up to screen
    py.display.update()
    clock.tick(60)  # FPS 60
