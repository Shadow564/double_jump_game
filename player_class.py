from pygame.locals import *
from entity_class import Entity, Particle
import pygame as py
from functions import flip, rotate, load_image
from math import pi


class Player(Entity):  # inherited from Entity class, check entity class.py file
    
    def __init__(self, x, y, offset_x, offset_y, width, height):
        super().__init__(x, y, offset_x, offset_y, width, height)
        self.action = "idle"  # current action being taken
        self.jumps = 0
        """
        JUMPS:
        0: Not jumped or in air from jumps
        1: 1 frame into the jump in order to show squish frame
        2: during 1st jump
        3: another buffer frame
        4: during 2nd jump
        """
        self.is_jumping = False  # bool
        self.velocity = [0, 0]  # [0]: x; [1]: y
        self.direction = "right"  # direction facing, left or right
        self.health = 4
        self.damage_timer = 0
        self.particles = []
        self.dir = "player"

    def handle_veloctiy(self, event, rects):
        # kinda self explained
        if K_RIGHT in event.keys:
            self.velocity[0] = 1.5
            self.direction = "right"
        elif K_LEFT in event.keys:
            self.velocity[0] = -1.5
            self.direction = "left"
        else:
            self.velocity[0] = 0
        
        # resets jump variables, the != 1 is to prevent the 1st frame from reseting the jump
        if self.collisions["bottom"] and self.jumps != 1:
            if self.jumps == 2:
                self.health = 0
            self.jumps = 0
            self.velocity[1] = 0
            self.is_jumping = False
        
        # if bonk head, set y velocity to 0
        if self.collisions["top"]:
            self.velocity[1] = 0
        
        if K_UP in event.downs and self.jumps in [0, 2]:
            """
            check the comment on the constructor for self.jumps details
            Basically, if we hit up and either we haven't jumped yet since landing or are mid-first-jump
            we set jumps to 1 or 3 respectively. This creates a one frame latency btwn hitting jump and
            starting the jump
            """
            self.is_jumping = True
            self.jumps += 1
        elif self.jumps in [1, 3]:
            # the actual jump. if you will
            self.velocity[1] = -4
            self.jumps += 1
        
        # GRAVITY
        self.velocity[1] += 0.25
        
        if self.velocity[1] > 5:  # terminal velocity
            self.velocity[1] = 5
        
        # takes the velocity determined and the collision rects, and moves the player
        self.move(self.velocity, rects)

    def sight_dangers(self, danger_rects):
        if self.damage_timer > 0:
            self.damage_timer -= 1
        for rect in danger_rects:
            if self.hitbox.colliderect(rect):
                if self.damage_timer == 0:
                    self.health -= 1
                    self.damage_timer = 60
        if self.health == 0:
            self.action = "dead"
            self.animation_timer = 0
    
    def die(self, surface, scroll):
        dead_img = load_image("dead_head.png")
        if self.animation_timer == 0:
            small_img = load_image("particles/small_death.png")
            large_img = load_image("particles/large_death.png")
            part1 = Particle(self.x + 2, self.y + 4, small_img, 3 * pi / 4, 2, 0.25, 20)
            part2 = Particle(self.x + 5, self.y + 4, small_img, pi / 4, 2, 0.25, 20)
            part3 = Particle(self.x + 2, self.y + 7, large_img, 3 * pi / 4, 2, 0.5, 40)
            part4 = Particle(self.x + 4, self.y + 6, large_img, pi / 4, 2, 0.5, 40)
            self.particles = [part1, part2, part3, part4]
        elif self.animation_timer == 300:
            self.action = "idle"
            self.animation_timer = 0
            self.changed_action = True
            self.set_pos((100, 100))
            self.health = 4
        else:
            for part in self.particles:
                part.turn()
                part.draw_particle(surface, scroll)
        self.animation_timer += 1
        surface.blit(rotate(dead_img, self.animation_timer * 8), (self.x - scroll[0], self.y - (self.animation_timer * 4) - scroll[1]))

    def handle_animations(self, animations):
        # this if to else switch determines the action based on player variables
        if self.jumps in [1, 2]:
            new_action = "jump"
        elif self.jumps in [3, 4]:
            new_action = "double_jump"
        elif self.velocity[0] != 0:
            new_action = "walk"
        else:
            new_action = "idle"
        
        if new_action != self.action:  # if the action changes, the animation changes and resets
            self.action = new_action
            self.changed_action = True
        else:
            # if it didn't change, just continue the animations
            self.changed_action = False
        if self.action == "double_jump":  # "double_jump" isn't an action in the animation dict, so this is a workaround
            self.action = "jump"
            self.cycle_animation(animations)  # Actual cycling of animation
            self.action = "double_jump"
        else:
            self.cycle_animation(animations)  # Actual cycling of animation

    def draw_player(self, surface, scroll):
        if self.direction == "right":
            surface.blit(self.image, (int(self.x - scroll[0]), int(self.y - scroll[1])))
        elif self.direction == "left":
            surface.blit(flip(self.image), (int(self.x - scroll[0]), int(self.y - scroll[1])))
