from entity_class import Entity
from functions import flip, load_image, point_rect_collision


class ShooterBlock(Entity):
    shooter_img = load_image("shooter.png")
    proj_img = load_image("proj.png")
    
    def __init__(self, x, y, offset_x, offset_y, width, height, direction):
        super().__init__(x, y, offset_x, offset_y, width, height)
        self.timer = 0
        self.direction = direction
        self.projectiles = []
    
    def shoot(self):
        if self.direction == "left":
            self.projectiles.append(Projectile(self.x + 1, self.y + 4, 0, 0, 4, 4, "left"))
        elif self.direction == "right":
            self.projectiles.append(Projectile(self.x + 8, self.y + 4, 0, 0, 4, 4, "right"))
    
    def turn(self, player, collision_rects):
        self.timer += 1
        if self.timer % 60 == 0:
            self.shoot()
        if self.direction == "left":
            for proj in self.projectiles:
                proj.shift([-2, 0])
        elif self.direction == "right":
            for proj in self.projectiles:
                proj.shift([2, 0])
        for proj in self.projectiles:
            for rect in collision_rects:
                if rect.colliderect(proj.hitbox):
                    if rect != self.hitbox:
                        self.projectiles.remove(proj)
        # for proj in self.projectiles:
        #     if r.randint(0, 21) == 0:
        #         proj.generate_particle()
        # for proj in self.projectiles:
        #     for part in proj.particles:
        #         part.turn()
        for proj in self.projectiles:
            if proj.hitbox.colliderect(player.hitbox) and player.damage_timer == 0:
                player.damage_timer = 60
                if player.health > 0:
                    player.health -= 1

    def draw_shooter(self, surface, scroll):
        surface.blit(self.shooter_img if self.direction == "right" else flip(self.shooter_img), (int(self.x - scroll[0]), int(self.y - scroll[1])))
    
    def draw_projectiles(self, surface, scroll, animations):
        for proj in self.projectiles:
            proj.cycle_animation(animations)
            proj.draw_projectile(surface, scroll)
            # for part in proj.particles:
            #     part.draw_particle(surface, scroll)
            #     if part.age > part.life:
            #         proj.particles.remove(part)


class Projectile(Entity):
    # red_img = load_image("particles/proj_red.png")
    # orange_img = load_image("particles/proj_orange.png")
    
    def __init__(self, x, y, offset_x, offset_y, width, height, direction):
        super().__init__(x, y, offset_x, offset_y, width, height)
        # self.particles = []
        self.dir = "shoot_block_proj"
        self.action = "idle"
        self.direction = direction
    
    # def generate_particle(self):
    #     chosen_image = r.choice([self.red_img, self.red_img, self.orange_img])
    #     # chosen_angle = r.randrange(-11, 13)
    #     chosen_angle = r.choice([0, 1, 2])
    #     self.particles.append(Particle(self.x + 1, self.y + 1, chosen_image, chosen_angle * (pi / 12), 3, 0, 5))
    
    def draw_projectile(self, surface, scroll):
        if self.direction == "right":
            surface.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))
        elif self.direction == "left":
            surface.blit(flip(self.image), (self.x - scroll[0], self.y - scroll[1]))


class Glob(Entity):
    
    def __init__(self, x, y, offset_x, offset_y, width, height):
        super().__init__(x, y, offset_x, offset_y, width, height)
        self.dir = "glob"
        self.action = "rest"  # "roaming"
        self.timer = 0
        self.direction = "right"
    
    def turn(self, player, collision_rects):
        self.timer += 1
        if self.action == "rest":
            self.offset[1] = 3
            self.set_pos_point((self.x, self.y))
            if self.timer == 180:
                self.action = "roaming"
                self.timer = 0
        if self.action == "roaming":
            if self.frame == 0:
                self.offset[1] = 1
                self.set_pos_point((self.x, self.y))
            elif self.frame == 1:
                self.offset[1] = 2
                self.set_pos_point((self.x, self.y))

            safe = 0
            if self.direction == "left":
                view_point_up = (self.x - 0, self.y + 4)
                view_point_down = (self.x - 0, self.y + 9)
                for rect in collision_rects:
                    if point_rect_collision(view_point_up, rect):
                        safe -= 1
                    if point_rect_collision(view_point_down, rect):
                        safe += 1
            elif self.direction == "right":
                view_point_up = (self.x + 9, self.y + 4)
                view_point_down = (self.x + 9, self.y + 9)
                for rect in collision_rects:
                    if rect != self.hitbox:
                        if point_rect_collision(view_point_up, rect):
                            safe -= 1
                        if point_rect_collision(view_point_down, rect):
                            safe += 1

            if safe == 1:  # advance
                self.shift((1, 0)) if self.direction == "right" else self.shift((-1, 0))
            else:
                self.direction = "left" if self.direction == "right" else "right"

            if self.timer == 180:
                self.action = "rest"
                self.changed_action = True
                self.timer = 0
        
        if self.hitbox.colliderect(player.hitbox) and player.damage_timer == 0:
            player.damage_timer = 60
            if player.health > 0:
                player.health -= 1
    
    def draw_glob(self, surface, scroll):
        if self.direction == "right":
            surface.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))
        elif self.direction == "left":
            surface.blit(flip(self.image), (self.x - scroll[0], self.y - scroll[1]))
