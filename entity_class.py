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


# function that loads a large dict of animations
def load_animations():
    animations = {}
    for dir in []:  # cycles through each directory in the animations folder
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
                image = py.image.load(f"data/animations/{dir}/{cycle}/{dir}_{cycle}{i}.png").convert_alpha()
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
        current = animations[self.action]
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
