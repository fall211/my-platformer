import pygame
from settings import *



class StartLogo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('placeholders/logoPH.png').convert_alpha()
        self.rect = self.image.get_rect(center =(100,100))

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, color, groups):
        super().__init__(groups)
        self.color = color

        self.image = pygame.Surface((TILE_SIZE,TILE_SIZE))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=pos)
