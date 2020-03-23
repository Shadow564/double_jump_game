import pygame as py
from entity_class import Entity
from block_filling_test import rotate


class ShooterBlock(Entity):
    shooter_img = py.image.load("data/shooter.png")
    proj_img = py.image.load("data/proj.png")
    
    def __init__(self, x, y, offset_x, offset_y, width, height, direction):
        super().__init__(x, y, offset_x, offset_y, width, height)
        self.timer = 0
        self.direction = direction
        self.projectiles = []
    
    def shoot(self):
        if self.direction == "left":
            self.projectiles.append([self.x + 1, self.y + 4])
        elif self.direction == "right":
            self.projectiles.append([self.x + 8, self.y + 4])
    
    def pass_timer(self, collision_rects):
        self.timer += 1
        if self.timer % 60 == 0:
            self.shoot()
        if self.direction == "left":
            for proj in self.projectiles:
                proj[0] -= 2
        elif self.direction == "right":
            for proj in self.projectiles:
                proj[0] += 2
        for proj in self.projectiles:
            for rect in collision_rects:
                if rect.colliderect(proj[0], proj[1], 4, 4):
                    if rect != self.hitbox:
                        self.projectiles.remove(proj)

    def draw_shooter(self, surface, scroll):
        surface.blit(self.shooter_img if self.direction == "right" else rotate(self.shooter_img, 180), (int(self.x - scroll[0]), int(self.y - scroll[1])))
    
    def draw_projectiles(self, surface, scroll):
        if self.direction == "left":
            for proj in self.projectiles:
                surface.blit(rotate(self.proj_img, 180), (proj[0] - scroll[0], proj[1] - scroll[1]))
        elif self.direction == "right":
            for proj in self.projectiles:
                surface.blit(self.proj_img, (proj[0] - scroll[0], proj[1] - scroll[1]))
