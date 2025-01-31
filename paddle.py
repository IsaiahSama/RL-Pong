from pygame.sprite import Sprite
from pygame import Surface

from enum import Enum

from movement_controller import MovementController

class PlayerType(Enum):
    PLAYER = 1
    OPPONENT = 2

class Paddle(Sprite):
    def __init__(self, controller: MovementController, x:int, y: int, _type: PlayerType):
        super().__init__()

        width = 20
        height = 90

        self.image = Surface([width, height])
        self.image.fill("white")

        self.startx = x
        self.starty = y

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.centery = y

        self.controller = controller(self)
        self._type = _type

        self.score = 0

    def update(self, dt):
        super().update()
        self.controller.update(dt)

    def increment_score(self):
        self.score += 1

    def reset(self):
        self.score = 0
        self.rect.x = self.startx
        self.rect.centery = self.starty

