import json
import random as r
import pygame as py
from break_up_functions import splice_rects, form_blocks, generate_images
from functions import swap_color
from enemy_classes import ShooterBlock, Glob


class Level:
    
    def __init__(self, file):
        self.file = file
        with open(f"data/levels/{self.file}", "r") as f:
            data = json.load(f)
        self.rects = [py.Rect(rect) for rect in data["collision_rects"]]
        objects = {"shooter": [], "glob": []}
        for s in data["objects"]["shooter"]:
            objects["shooter"].append(ShooterBlock(s[0], s[1], 0, 0, 12, 12, s[2]))
        for g in data["objects"]["glob"]:
            objects["glob"].append(Glob(g[0], g[1], 1, 3, 8, 6))
        self.objects = objects
        self.spliced_rects = splice_rects(self.rects, 12)
        self.images = None
    
    def turn(self, player):
        collision_rects = []
        collision_rects.extend(self.rects)
        collision_rects.extend([shoot.hitbox for shoot in self.objects["shooter"]])
        
        damage_rects = []
        for shooter in self.objects["shooter"]:
            for proj in shooter.projectiles:
                damage_rects.append(proj.hitbox)
        for glob in self.objects["glob"]:
            if glob.action == "roaming":
                damage_rects.append(glob.hitbox)
            elif glob.action == "rest":
                collision_rects.append(glob.hitbox)

        for shooter in self.objects["shooter"]:
            shooter.turn(player, collision_rects)

        for glob in self.objects["glob"]:
            glob.turn(player, collision_rects)
        
        return collision_rects, damage_rects
        
    def update_images(self, surface):
        # the fist color is inside the shape, the second is outside the shape
        base_colors = [(127, 127, 127), (0, 0, 0)]
        color_scheme = [[(255, 128, 164), (255, 38, 116)],  # pink
                        [(191, 255, 60), (16, 210, 117)],  # green
                        [(148, 33, 106), (67, 0, 103)],  # purple
                        [(0, 120, 153), (0, 40, 89)]]  # blue
        blocks = form_blocks(self.spliced_rects, 12)
        self.images = generate_images(blocks, surface)
        for part in self.images:
            color_set = r.choice(color_scheme)
            part[1] = swap_color(part[1], base_colors[0], color_set[0])
            part[1] = swap_color(part[1], base_colors[1], color_set[1])
    
    def draw_level(self, surface, scroll, animations):
        for part in self.images:
            surface.blit(part[1], (part[0][0] - scroll[0], part[0][1] - scroll[1]))
        for shooter in self.objects["shooter"]:
            shooter.draw_projectiles(surface, scroll, animations)
            shooter.draw_shooter(surface, scroll)
        for glob in self.objects["glob"]:
            glob.cycle_animation(animations)
            glob.draw_glob(surface, scroll)
