import pygame
class Heart:  
    def __init__(self):
        self.img = pygame.image.load('./media/img/heart.png')
        self.position = pygame.Vector2()
        self.position.xy=0,0