import pygame
class Button:
    def __init__(self):
        self.price = 3
        self.level = 1   
    sprite = pygame.image.load('./media/img/button.png')
    typeIndicatorSprite = pygame.image.load('./media/img/null_indicator.png')
