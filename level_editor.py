import pygame as py
from event_class import EventKeep
# from text_class import TextBox
from pygame.locals import *
import json
from block_filling_test import rotate

clock = py.time.Clock()

event = EventKeep()

WIDTH = (720 + 24)  # 240
HEIGHT = (720 + 24)
SCALE = 3

screen = py.display.set_mode((WIDTH, HEIGHT))
display = py.Surface((int(WIDTH / SCALE), int(WIDTH / SCALE)))  # surface that all blits are on, used to scale pixels


# click_timer = 0  # unused click_timer


real_c = [0, 0]  # list keeping track of the TRUE mouse value
fake_c = [0, 0]  # list keeping track of mouse value locked onto multiple of 12

blocks = []
objects = {"shooter": []}


def lock_cursors(base_c, mod_c, scale):
    """
    locks a cursor onto a certain scale
    :param base_c: 2 long list for x and y
    :param mod_c:  2 long list for x and y
    :param scale: what number mod_c should be a multiple of (ie. if 4, mod_c will be the largest multiple of 4 smaller
    than the base_c
    :return: no returns, mod_c gets modified
    """
    mod_c[0] = int(base_c[0] - (base_c[0] % scale))
    mod_c[1] = int(base_c[1] - (base_c[1] % scale))
    

def loop_range(start, stop, current):
    """
    runs through a range in a loop like manner
    :param start: first in range
    :param stop:  last in range
    :param current: place in range currently being worked with
    :return: the next number in loop after the current
    """
    advancement = current + 1 if current < stop else start
    return advancement


def import_assets():
    with (open("data/levels/export_level", "r")) as f:
        data = json.load(f)
    
    export_rects = data["collision_rects"]
    export_objects = data["objects"]
    return export_rects, export_objects
 

def export(rects, objects):
    data = {"collision_rects": rects, "objects": objects}
    with (open("data/levels/export_level", "w")) as f:
        json.dump(data, f)


class Bar:
    
    def __init__(self, x, y, rotation):
        self.value = 224
        self.length = 224
        self.growth = [0, 0]
        self.parse = 0
        self.x = x
        self.y = y
        self.rotation = rotation
    
    def grow(self, direction):
        if direction > 0:
            self.value += 12
            self.growth[1] += 1
        if direction < 0:
            self.value += 12
            self.growth[0] += 1
    
    def draw(self, surface):
        if self.rotation == "h":
            bar_rect = (int(round(self.x + ((self.growth[0] + self.parse) * 12) / self.value * self.length)), self.y, int(round(((224 / self.value) * self.length))), 8)
            py.draw.rect(surface, (128, 128, 128), bar_rect)
        elif self.rotation == "v":
            bar_rect = (self.x, int(round(self.y + ((self.growth[0] + self.parse) * 12) / self.value * self.length)), 8, int(round(((224 / self.value) * self.length))))
            py.draw.rect(surface, (128, 128, 128), bar_rect)
            

growing_spot = None  # when building a collision rect, this is the spot where the drag block starts

# the_box = TextBox((0, 0, 0), "")

growing_lock = False  # used to make sure growing spot doesn't update while dragging the mouse

grid_img = py.image.load("data/grid.png")
shooter_img = py.image.load("data/shooter_editor.png")

h_bar = Bar(8, 240, "h")

v_bar = Bar(240, 8, "v")

using = "block"

shooter_direction = "right"


def point_rect_collision(point, rect):
    return rect[0] <= point[0] <= rect[0] + rect[2] and rect[1] <= point[1] <= rect[1] + rect[3]


arrow_img = py.image.load("data/arrow.png")

selected = None

while True:
    display.fill((255, 255, 255))
    for x in range(-h_bar.growth[0], h_bar.growth[1] + 1):
        for y in range(-v_bar.growth[0], v_bar.growth[1] + 1):
            display.blit(grid_img, ((0 - h_bar.parse * 12) + x * 240, (0 - v_bar.parse * 12) + y * 240))
    py.draw.rect(display, (255, 74, 120), (0 - h_bar.parse * 12, 0 - v_bar.parse * 12, 6, 6))
    
    # click_timer -= 1 if click_timer > -1 else 0
    
    real_c = event.mouse_pos  # updates mouse position
    real_c = real_c[0] / 3, real_c[1] / 3  # scales mouse down to display surface

    lock_cursors(real_c, fake_c, 12)
    
    if event.init_left_click == 1:
        if point_rect_collision(real_c, (240, 0, 8, 8)):
            v_bar.grow(-1)
        elif point_rect_collision(real_c, (240, 8, 8, 224)):
            selected = v_bar
        elif point_rect_collision(real_c, (240, 232, 8, 8)):
            v_bar.grow(1)
        elif point_rect_collision(real_c, (0, 240, 8, 8)):
            h_bar.grow(-1)
        elif point_rect_collision(real_c, (8, 240, 224, 8)):
            selected = h_bar
        elif point_rect_collision(real_c, (232, 240, 8, 8)):
            h_bar.grow(1)
        elif not growing_lock and using == "block":
                growing_lock = True  # prevents growing spot from updating
                growing_spot = fake_c.copy()  # creates the spot to grow a block from
        elif using == "shooter":
            print("make_shoot")
            shoot = [fake_c[0] + h_bar.parse * 12, fake_c[1] + v_bar.parse * 12, shooter_direction]
            print(shoot)
            objects["shooter"].append(shoot)
            
    if K_b in event.downs:  # block
        using = "block"
    elif K_n in event.downs:  # shooter
        using = "shooter"
    if not event.left_click and growing_spot is not None and using == "block":  # 2nd cond prevents continual attempts to build a block
        growing_lock = False
        new_block = []
        # TODO there's no way all these conditionals are necessary
        if growing_spot[0] <= fake_c[0]:
            if growing_spot[1] <= fake_c[1]:
                new_block = [growing_spot[0], growing_spot[1], (fake_c[0] - growing_spot[0] + 12), (fake_c[1] - growing_spot[1] + 12)]
            else:
                new_block = [growing_spot[0], fake_c[1], (fake_c[0] - growing_spot[0] + 12), (growing_spot[1] - fake_c[1] + 12)]
        else:
            if growing_spot[1] <= fake_c[1]:
                new_block = [fake_c[0], growing_spot[1], (growing_spot[0] - fake_c[0] + 12), (fake_c[1] - growing_spot[1] + 12)]
            else:
                new_block = [fake_c[0], fake_c[1], (growing_spot[0] - fake_c[0] + 12), (growing_spot[1] - fake_c[1] + 12)]
        new_block = [int(i) for i in new_block]
        new_block[0] += h_bar.parse * 12
        new_block[1] += v_bar.parse * 12
        blocks.append(new_block)
        growing_spot = None
    
    if event.right_click:
        # py.draw.rect(display, (0, 255, 0), (fake_c[0] - h_bar.parse * 12, fake_c[1] - v_bar.parse * 12, 12, 12))
        for rect in blocks:
            print((fake_c[0] - h_bar.parse * 12, fake_c[1] - v_bar.parse * 12), rect)
            if point_rect_collision((fake_c[0] + (h_bar.parse * 12), fake_c[1] + (v_bar.parse * 12)), rect):
                blocks.remove(rect)
    
    if K_LEFT in event.downs:
        shooter_direction = "left"
    elif K_RIGHT in event.downs:
        shooter_direction = "right"
    
    if K_LCTRL in event.keys and K_z in event.downs:
        blocks = blocks[:-1]
        
    if K_i in event.downs:
        blocks, objects = import_assets()
    
    if K_e in event.downs:
        export(blocks, objects)
    
    if K_s in event.downs:
        selected = None
    
    if K_LEFT in event.downs and selected.parse > -h_bar.growth[0]:
        h_bar.parse -= 1
    elif K_RIGHT in event.downs and selected.parse < h_bar.growth[1]:
        h_bar.parse += 1
    elif K_UP in event.downs and selected.parse > -v_bar.growth[0]:
        v_bar.parse -= 1
    elif K_DOWN in event.downs and selected.parse < v_bar.growth[1]:
        v_bar.parse += 1
        
    # print(f"parse {v_bar.parse}")
    # print(f"growth {v_bar.growth}")
    
    for block in blocks:
        py.draw.rect(display, (0, 0, 0), (block[0] - h_bar.parse * 12, block[1] - v_bar.parse * 12, block[2], block[3]))
    for shooter in objects["shooter"]:
        display.blit(shooter_img if shooter[2] == "right" else rotate(shooter_img, 180), (shooter[0] - h_bar.parse * 12, shooter[1] - v_bar.parse * 12))

    if using == "block":
        py.draw.rect(display, (0, 0, 255), (fake_c[0], fake_c[1], 12, 12))
    elif using == "shooter":
        if shooter_direction == "right":
            display.blit(shooter_img, (fake_c[0], fake_c[1]))
        elif shooter_direction == "left":
            display.blit(rotate(shooter_img, 180), (fake_c[0], fake_c[1]))
        
    py.draw.rect(display, (128, 128, 128), (240, 240, 8, 8))
    py.draw.rect(display, (192, 192, 192), (0, 240, 240, 8))
    py.draw.rect(display, (192, 192, 192), (240, 0, 8, 240))

    display.blit(arrow_img, (240, 0))
    display.blit(rotate(arrow_img, 180), (240, 232))
    display.blit(rotate(arrow_img, 90), (0, 240))
    display.blit(rotate(arrow_img, -90), (232, 240))
    
    h_bar.draw(display)
    v_bar.draw(display)
    
    # py.draw.rect(display, (255, 0, 0), [int(real_c[0]), int(real_c[1]), 12, 12])
    # py.draw.rect(display, (0, 255, 0), [int(fake_c[0]), int(fake_c[1]), 12, 12])
    
    # the_box.draw_box(display, 0, 0, ["left", "top"])
    
    event.take_events()
    
    screen.blit(py.transform.scale(display, (WIDTH, HEIGHT)), (0, 0))
    py.display.update()
    clock.tick(60)
