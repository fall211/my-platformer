import pygame
from settings import *
from sys import exit

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

class ExitButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('placeholders/exitbuttonPH.png').convert_alpha()
        self.rect = self.image.get_rect(center =(1100,100))

    def end_game(self):
        mouse_position = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (1,0,0) and self.rect.collidepoint(mouse_position):
            pygame.quit()
            exit()

    def update(self):
        self.end_game()

class PlayButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('placeholders/startbuttonPH.png').convert_alpha()
        self.rect = self.image.get_rect(center =(600,575))

    def start_game(self):
        mouse_position = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (1,0,0) and self.rect.collidepoint(mouse_position):
            print('clicked start game')
            return True
        return False


    def update(self):
        self.start_game()
