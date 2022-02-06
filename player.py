import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('placeholders/playerPH.png').convert_alpha()
        self.rect = self.image.get_rect(center=(600,325))


    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.rect.y -= 5
        if keys[pygame.K_a]: self.rect.x -= 5
        if keys[pygame.K_s]: self.rect.y += 5
        if keys[pygame.K_d]: self.rect.x += 5


    def update(self):
        self.player_input()
