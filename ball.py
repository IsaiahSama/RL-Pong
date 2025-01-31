import math
import pygame

from pygame.sprite import Sprite
from pygame import Surface, Vector2

from paddle import PlayerType, Paddle

from random import choice, randint

LEFT_DIR = (180, 1)
RIGHT_DIR = (0, -1)

class Ball(Sprite):
    def __init__(self, x:int, y: int):
        super().__init__()
        
        self.image = Surface([20, 20])
        # self.image.fill("white")

        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.centery = y

        self.radius = 10

        self.direction = 0
        self.speed = 0

        self.canCollide = 0

    def start(self):
        self.direction = choice([0, 180])
        self.direction += self.get_angle_variance()
        self.speed = 300

    def get_angle_variance(self) -> int:
        return choice([1, -1]) * randint(0, 15)

    def collide(self, paddle: Paddle):
        if (self.canCollide > 0): return

        w, _ = pygame.display.get_surface().get_size()
        
        next_dir = LEFT_DIR if self.rect.centerx > w // 2 else RIGHT_DIR

        base_angle = next_dir[0]

        if self.rect.centery in range(paddle.rect.centery - 5, paddle.rect.centery +5):
            midpoint = 270 if self.direction > 180 else 90
            diff = abs(midpoint - self.direction)
            
            if midpoint == 270 and self.direction < 270 or midpoint == 90 and self.direction < 90:
                multiplier = 1
            else:
                multiplier = -1

            self.direction = midpoint + (diff * multiplier)

        elif self.rect.centery < paddle.rect.centery:
            # Make the ball go down
            _, h = paddle.rect.size
            
            self.direction = base_angle - 30 * next_dir[1]

        else:
            # Make the ball go up
            _, h = paddle.rect.size 

            self.direction = base_angle + 30 * next_dir[1]

        self.direction += self.get_angle_variance()
        self.canCollide = 2

    def draw(self, screen: Surface):
        pygame.draw.circle(
                screen,
                "white",
                (self.rect.centerx, self.rect.centery),
                self.radius,
                0
            )

    def get_new_pos(self, dt):
        move_vec = Vector2()
        move_vec.from_polar((self.speed * dt, self.direction))
        return self.rect.center + move_vec

    def boundary(self):
        w, h = pygame.display.get_surface().get_size()
        current_dir = self.direction
        if self.rect.bottom > h:
            if current_dir > 90: # It was moving south west
                self.direction = (180 - current_dir) + 180
            else:
                self.direction = - current_dir

        if self.rect.top < 0:
            if current_dir < 270: # It was moving north west
                self.direction = 180 - (current_dir - 180) 
            else:
                self.direction = 360 - current_dir

        if self.direction != current_dir:
            self.direction += self.get_angle_variance()
        
    def update(self, dt):
        if self.canCollide > 0:
            self.canCollide -= dt
        elif self.canCollide < 0:
            self.canCollide = 0

        self.boundary()
        self.speed += dt
        self.speed = round(self.speed, 2)
        new_pos = self.get_new_pos(dt)
        self.rect.center = round(new_pos[0]), round(new_pos[1])

