import pygame
from settings import *
from random import randint
from player import Player
from map import * #Map, StartLogo, PlayButton, ExitButton
from button import *

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.game_sprites = pygame.sprite.Group()
        self.game_sprites.add(Map(),Player())
        self.hidden_sprites = pygame.sprite.Group()
        self.menu_sprites = pygame.sprite.Group()
        self.menu_sprites.add(StartLogo())

    def run(self):
        #update/draw game


        if Global.state == 'game level':
            self.game_sprites.draw(self.display_surface)
            self.game_sprites.update()
        elif Global.state == 'main menu':
            self.menu_sprites.draw(self.display_surface)
            self.menu_sprites.update()

            #exit button
            exit_button = Button('placeholders/exitbuttonPH.png',(1100,100),Button.exit_game)
            exit_button.when_clicked(Global.mouseclick_event)
            self.display_surface.blit(exit_button.image, exit_button.rect)

            #start button
            start_button = Button('placeholders/startbuttonPH.png',(600,575),Button.start_game)
            start_button.when_clicked(Global.mouseclick_event)
            self.display_surface.blit(start_button.image, start_button.rect)
