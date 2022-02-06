import pygame
from settings import *
from random import randint
from player import Player
from map import * #Map, StartLogo, PlayButton, ExitButton

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.game_sprites = pygame.sprite.Group()
        self.game_sprites.add(Map(),Player())
        self.hidden_sprites = pygame.sprite.Group()
        self.menu_sprites = pygame.sprite.Group()
        self.menu_sprites.add(StartLogo(),PlayButton(),ExitButton())

    def run(self):
        #update/draw game


        if Global.state == 'game level':
            self.game_sprites.draw(self.display_surface)
            self.game_sprites.update()
        elif Global.state == 'main menu':
            self.menu_sprites.draw(self.display_surface)
            self.menu_sprites.update()
