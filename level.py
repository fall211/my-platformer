import pygame
from settings import *
from random import randint
from player import Player
from map import * #Map, StartLogo, PlayButton, ExitButton

class GameLevel:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.game_sprites = pygame.sprite.Group()
        self.game_sprites.add(Map(),Player())
        self.hidden_sprites = pygame.sprite.Group()

    def run(self):
        #update/draw game

            self.game_sprites.draw(self.display_surface)
            self.game_sprites.update()

class MenuLevel():
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.menu_sprites = pygame.sprite.Group()
        self.menu_sprites.add(StartLogo(),PlayButton(),ExitButton())

    def run(self):

            self.menu_sprites.draw(self.display_surface)
            self.menu_sprites.update()
