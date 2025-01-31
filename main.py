import pygame
from paddle import Paddle, PlayerType
from ball import Ball

from movement_controller import PlayerMovementController

pygame.init()
pygame.font.init()

HEIGHT = 900
WIDTH = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

player = Paddle(PlayerMovementController, 0, HEIGHT // 2, PlayerType.PLAYER)
opponent = Paddle(PlayerMovementController, WIDTH - 20, HEIGHT // 2, PlayerType.OPPONENT)

paddles = pygame.sprite.Group()

paddles.add(player)
paddles.add(opponent)

clock = pygame.time.Clock()

running = True

dt = 0

word_font = pygame.font.SysFont('Comic Sans MS', 30)

def reset_game(ball: Ball | None):
    if ball:
        ball.kill()

    ball = Ball(WIDTH // 2, HEIGHT // 2)
    ball.start()
    return ball

ball = reset_game(None)

def end_game():
    pygame.quit()

def get_score(paddles_group) -> pygame.Surface:
    paddles = paddles_group.sprites()

    score1, score2 = paddles[0].score, paddles[1].score

    score_surface = word_font.render(f"{score1} - {score2}", True, (255, 0, 0))

    return score_surface

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
    ball.update(dt)
    paddles.update(dt)

    if hitlist := pygame.sprite.spritecollide(ball, paddles, False):
        ball.collide(hitlist[0])

    # Check to see if we can award points
    if ball.rect.right > WIDTH:
        paddle: Paddle = paddles.sprites()[0]
        paddle.increment_score()

        if paddle.score >= 5:
            end_game()
        ball = reset_game(ball)

    if ball.rect.left < 0:
        paddle: Paddle = paddles.sprites()[1]
        paddle.increment_score()

        if paddle.score >= 5:
            end_game()
        ball = reset_game(ball)

    screen.fill("black")
    
    paddles.draw(screen) 
    ball.draw(screen)

    score_text = get_score(paddles)
    screen.blit(score_text, (WIDTH // 2, 0))

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
