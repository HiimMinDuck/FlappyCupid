import pygame
class Monster:  
    def __init__(self):
        self.img = pygame.image.load('./media/img/monster.png')
        self.position = pygame.Vector2()
        self.position.xy=0,0
        self.maxhealth=1
        self.health=self.maxhealth