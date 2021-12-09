import pygame
class Arrow:  
    def __init__(self):
        self.img = pygame.image.load('./media/img/arrow.png')
        self.position = pygame.Vector2()
        self.position.xy=0,0
        self.power = 1
        self.degree = 0
        self.velocity = pygame.Vector2()
        self.velocity.xy = 0, 0