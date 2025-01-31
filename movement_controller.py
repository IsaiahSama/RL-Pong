import pygame

class MovementController:
    def __init__(self, paddle):
        self.paddle = paddle
        self.speed = 400

    def update(self, dt: float):
        raise NotImplementedError

class PlayerMovementController(MovementController):
    def __init__(self, paddle):
        super().__init__(paddle)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            # Make Pong move up
            self.paddle.rect.y -= self.speed * dt

        if keys[pygame.K_DOWN]:
            # Make pong move down.
            self.paddle.rect.y += self.speed * dt

class OpponentMovementController(MovementController):
    def __init__(self, paddle):
        super().__init__(paddle)

    def update(self, dt):
        pass

    def move_up(self):
        self.paddle.rect.y -= self.speed * dt

    def move_down(self):
        self.paddle.rect.y += self.speed * dt
