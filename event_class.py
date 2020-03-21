# imports pygame and sys
import pygame as py
from pygame.locals import *
import sys


class EventKeep:
    
    def __init__(self):
        self.keys = []  # a list of current buttons that have been pressed
        self.downs = []
        self.left_click = False
        self.right_click = False
        self.mouse_pos = [0, 0]
        self.init_left_click = False  # 0: never left clicked since unclicked 1: init click 2: left click but not init
    
    def take_events(self):
        self.downs = []
        # the next two variables are the new lists that will replace downs and ups
        for event in py.event.get():
            # this if statements checks if the 'x' in the corner of the screen was hit, if so, the game ends
            if event.type == QUIT:
                py.quit()
                sys.exit()
            
            # for each event, if it is a key press or release, the given key is put into its respective list
            if event.type == KEYDOWN:
                self.keys.append(event.key)
                self.downs.append(event.key)
            if event.type == KEYUP:
                self.keys.remove(event.key)
            
        self.left_click, skipping_the_middle_assign, self.right_click = py.mouse.get_pressed()
        self.mouse_pos = py.mouse.get_pos()
        
        if not self.left_click:
            self.init_left_click = 0
        elif self.left_click and self.init_left_click == 0:
            self.init_left_click = 1
        elif self.init_left_click == 1:
            self.init_left_click = 2
