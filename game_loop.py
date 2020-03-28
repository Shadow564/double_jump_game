import pygame as py
from event_class import EventKeep
from player_class import Player
from level_class import Level
from entity_class import load_animations
from functions import load_image


def game():
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
    
    clock = py.time.Clock()  # maintains fps & junk
    
    event = EventKeep()
    
    player = Player((WIDTH / SCALE) / 2, (HEIGHT / SCALE) / 2, 1, 0, 5, 12)
    scroll = [0, 0]
    
    level = Level("export_level")
    
    animations = load_animations()
    
    num = 0
    
    health_img = load_image("health.png")
    
    while True:
        
        display.fill((255, 255, 255))
        
        # start

        if num % 60 == 0:  # every second
            num = 0
            level.update_images(display)
        num += 1

        collision_rects, damage_rects = level.turn(player)
        
        if player.action != "dead":
            player.handle_veloctiy(event, collision_rects)
            player.handle_animations(animations)
            player.handle_health()
            player.draw_player(display, scroll)

        if player.action == "dead":
            player.die(display, scroll)
        
        scroll[0] += int((player.x - scroll[0] - 120) / 4)
        scroll[1] += int((player.y - scroll[1] - 120) / 4)
        
        level.draw_level(display, scroll, animations)
        
        for i in range(player.health):
            py.draw.rect(display, (255, 128, 164), (6 + i * 12, 6, 12, 6))
            display.blit(health_img, (6 + i * 12, 6))
        
        # end
        
        event.take_events()
        
        screen.blit(py.transform.scale(display, (WIDTH, HEIGHT)), (0, 0))  # scales display up to screen
        py.display.update()
        clock.tick(60)  # FPS 60
