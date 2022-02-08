import pygame
from settings import *
from sys import exit
from global_ import Global

class Map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('placeholders/bgPH.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(0,0))

class StartLogo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('placeholders/logoPH.png').convert_alpha()
        self.rect = self.image.get_rect(center =(100,100))
