import pygame

class Cupid:
    position = pygame.Vector2()
    position.xy = 295, 100
    velocity = pygame.Vector2()
    velocity.xy = 3, 0
    acceleration = 0.1
    power=1
    rightDirection = pygame.image.load('./media/img/cupid.png')
    leftDirection = pygame.transform.flip(rightDirection, True, False)
    currentDirection = rightDirection