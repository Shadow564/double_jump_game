import pygame as py
import json
import random as r
from event_class import EventKeep
from player_class import Player
from break_up_functions import splice_rects, form_blocks, generate_images
from enemy_classes import ShooterBlock, Glob
from functions import load_image, swap_color
from entity_class import load_animations

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

animations = load_animations()

player = Player((WIDTH / SCALE) / 2, (HEIGHT / SCALE) / 2, 1, 0, 5, 12)
scroll = [0, 0]
health_img = load_image("health.png")

with open("data/levels/export_level", "r") as f:
    data = json.load(f)

export_rects = []
export_shooters = []
export_globs = []
for rect in data["collision_rects"]:
    export_rects.append(py.Rect(rect))
for shoot in data["objects"]["shooter"]:
    export_shooters.append(ShooterBlock(shoot[0], shoot[1], 0, 0, 12, 12, shoot[2]))
for glob in data["objects"]["glob"]:
    export_globs.append(Glob(glob[0], glob[1], 1, 3, 8, 6))

# splits the rects into points [x, y] based on each point being a square with scale (12) sides
spliced = splice_rects(export_rects, 12)

# the fist color is inside the shape, the second is outside the shape
base_colors = [(127, 127, 127), (0, 0, 0)]
color_scheme = [[(255, 128, 164), (255, 38, 116)],  # pink
                [(191, 255, 60), (16, 210, 117)],  # green
                [(148, 33, 106), (67, 0, 103)],  # purple
                [(0, 120, 153), (0, 40, 89)]]  # blue

num = -1  # temporary counter


# generates new images to put over the rects
def generates_new_images(rect_points, scale, surface):
    step_1 = form_blocks(rect_points, scale)
    step_2 = generate_images(step_1, surface)
    for part in step_2:
        color_set = r.choice(color_scheme)
        part[1] = swap_color(part[1], base_colors[0], color_set[0])
        part[1] = swap_color(part[1], base_colors[1], color_set[1])
    return step_2


while True:
    num += 1
    
    display.fill((255, 255, 255))

    collision_rects = []
    collision_rects.extend(export_rects)
    collision_rects.extend([shoot.hitbox for shoot in export_shooters])
    
    damage_rects = []
    for shooter in export_shooters:
        for proj in shooter.projectiles:
            damage_rects.append(proj.hitbox)
    for glob in export_globs:
        if glob.action == "roaming":
            damage_rects.append(glob.hitbox)
    
    for glob in export_globs:
        if glob.action == "rest":
            collision_rects.append(glob.hitbox)
        
    if player.action != "dead":
        player.handle_veloctiy(event, collision_rects)
        player.handle_animations(animations)
        player.handle_health()
        player.draw_player(display, scroll)
    
    if player.action == "dead":
        player.die(display, scroll)
    
    # temporarily prevents out of bounds falling by giving the player an upward boost in velocity
    if player.hitbox.y > 240:
        player.velocity[1] = -6

    for shooter in export_shooters:
        shooter.turn(player, collision_rects)

    for glob in export_globs:
        glob.turn(player, collision_rects)
    
    # takes a all given events from mouse & keyboard and puts them in class object
    event.take_events()
    
    # adds the difference between the players coordinate and the scrolls displacement
    # tbh this isn't really my idea; credit goes to DaFluffyPotato; he is a god w/ pygame
    scroll[0] += int((player.x - scroll[0] - 120) / 4)
    scroll[1] += int((player.y - scroll[1] - 120) / 4)
    
    if num % 60 == 0:  # every second
        images = generates_new_images(spliced, 12, display)  # generates the masks to put on the collision rects
    for part in images:
        display.blit(part[1], (part[0][0] - scroll[0], part[0][1] - scroll[1]))
    for shooter in export_shooters:
        shooter.draw_projectiles(display, scroll, animations)
        shooter.draw_shooter(display, scroll)
    for glob in export_globs:
        glob.cycle_animation(animations)
        glob.draw_glob(display, scroll)
    
    for i in range(player.health):
        py.draw.rect(display, (255, 128, 164), (6 + i * 12, 6, 12, 6))
        display.blit(health_img, (6 + i * 12, 6))
    
    screen.blit(py.transform.scale(display, (WIDTH, HEIGHT)), (0, 0))  # scales display up to screen
    py.display.update()
    clock.tick(60)  # FPS 60
