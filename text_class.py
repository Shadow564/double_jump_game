import pygame as py
from pygame.locals import *

py.font.init()


class TextBox:
    
    def __init__(self, color, content):
        self.font = py.font.SysFont('arial.ttf', 36)
        self.content = content
        self.color = color
        self.text = self.font.render(content, True, color)
        self.rect = self.text.get_rect()
    
    def change_message(self, new_message):
        self.content = str(new_message)
        self.text = self.font.render(self.content, True, self.color)
        self.rect = self.text.get_rect()
    
    def type_box(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    self.content = self.content[:-1]
                else:
                    self.content += event.unicode
                
                self.text = self.font.render(self.content, True, self.color)
                self.rect = self.text.get_rect()
    
    def draw_box(self, surface, x, y, placements):
        # placements is a tuple with [0] being how the x is to be used and [1] being how y to be used
        
        if placements[0] == "center":
            self.rect.centerx = x
        elif placements[0] == "left":
            self.rect.left = x
        elif placements[0] == "right":
            self.rect.right = x
        
        if placements[1] == "center":
            self.rect.centery = y
        elif placements[1] == "bottom":
            self.rect.bottom = y
        elif placements[1] == "top":
            self.rect.top = y
        
        surface.blit(self.text, self.rect)
