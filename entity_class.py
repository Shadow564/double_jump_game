"""
Structure of data:
data
/animations
//dir for each entity  EX: fox
///dir for each action or cycle EX: fox_walk, fox_jump
///json file with list of cycle with its timings EX: fox_timings
/images
"""
import pygame as py
from math import sin, cos
import json


def load_animations():
    """
    Uses data dir to load animations into a dict
    (i commented this function a will ago, I don't remember what I put lol)
    :return: dictionary of animations and timings
    """
    animations = {}
    for dir in ["player", "shoot_block_proj"]:  # cycles through each directory in the animations folder
        with open(f"data/animations/{dir}/{dir}_timings", "r") as f:
            data = json.load(f)
        # the json file in each dir is used to load each needed animation
        
        for cycle in data:
            """
            for each animation in the json file, each duration under the cycle is put with a image surface with each
            given json entry in a list, and that list is going to be added to the frames of the animation

            """
            animations[f"{dir}_{cycle}"] = []  # the list used to represent the animation
            frames = []  # list of image, duration pairs
            for i in range(0, len(data[cycle][0])):  # cycles from 0 to the number of duration's in the file
                image = py.image.load(f"data/animations/{dir}/{dir}_{cycle}/player_{cycle}{i}.png").convert_alpha()
                # the upper line loads the image in the action's image dir that corresponds with the duration
                duration = data[cycle][0][i]  # the entry in the json file
                frames.append([image, duration])  # adds a list of the image and duration to the frames
            animations[f"{dir}_{cycle}"].append(frames)  # adds the list of image, dur pairs
            animations[f"{dir}_{cycle}"].append(data[cycle][1])
            """
            the line prior adds the second half of the json entry onto the animation
            currently, this is unused but is being included to allow for a future animation tag system

            """
    return animations


def collision_test(main_rect, rect_list):
    collision_list = []
    for rect in rect_list:
        if main_rect.colliderect(rect):
            collision_list.append(rect)
    return collision_list


class Entity:

    def __init__(self, x, y, offset_x, offset_y, width, height):
        self.x = x
        self.y = y
        self.hitbox = py.Rect(x + offset_x, y + offset_y, width, height)
        self.offset = [offset_x, offset_y]
        self.image = None
        self.animation = None
        self.action = None
        self.animation_timer = 0
        self.changed_action = False
        self.frame = 0
        self.flip = False
        self.collisions = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.dir = None
        
    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.hitbox.x = pos[0] + self.offset[0]
        self.hitbox.y = pos[1] + self.offset[1]
    
    def shift(self, velocity):
        self.hitbox.x += int(velocity[0])
        self.hitbox.y += int(velocity[1])
        self.x, self.y = self.hitbox.x - self.offset[0], self.hitbox.y - self.offset[1]
    
    def move(self, velocity, rects):
        self.hitbox.x += int(velocity[0])
        hit_list = collision_test(self.hitbox, rects)
        self.collisions = {'top': False, 'bottom': False, 'right': False, 'left': False}
        for block in hit_list:
            if velocity[0] > 0:
                self.hitbox.right = block.left
                self.collisions['right'] = True
            elif velocity[0] < 0:
                self.hitbox.left = block.right
                self.collisions['left'] = True
        self.hitbox.y += int(velocity[1])
        block_hit_list = collision_test(self.hitbox, rects)
        for block in block_hit_list:
            if velocity[1] > 0:
                self.hitbox.bottom = block.top
                self.collisions['bottom'] = True
            elif velocity[1] < 0:
                self.hitbox.top = block.bottom
                self.collisions['top'] = True
        self.x, self.y = self.hitbox.x - self.offset[0], self.hitbox.y - self.offset[1]

    def cycle_animation(self, animations):
        if self.changed_action:
            self.changed_action = False
            self.frame, self.animation_timer = 0, 0
        current = animations[f"{self.dir}_{self.action}"]
        if self.animation_timer < current[0][self.frame][1]:  # if the timer < frame's duration, timer ++ and move on
            self.animation_timer += 1
        else:  # if not reset timer, and move to next frame in cycle
            self.animation_timer = 0
            if len(current[0]) - 1 > self.frame:  # if the frame isn't the last frame in current
                # the minus one is because frame starts at 0 but len starts at 1
                self.frame += 1
            else:
                self.frame = 0
        self.image = current[0][self.frame][0]
        if self.flip:
            self.image = py.transform.flip(self.image, True, False)


class Particle:
    
    def __init__(self, x, y, image, angle, speed, gravity, life):
        self.x = x
        self.y = y
        self.image = image
        self.angle = angle
        self.speed = speed
        self.vector = [self.speed * cos(self.angle), self.speed * sin(self.angle)]
        self.gravity = gravity
        self.age = 0
        self.life = life
    
    def turn(self):
        self.x += self.vector[0]
        self.y += -self.vector[1]
        self.vector[1] -= self.gravity
        self.age += 1

    def draw_particle(self, surface, scroll):
        if self.age < self.life:
            surface.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))
