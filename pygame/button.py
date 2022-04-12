import pygame
from settings import *
from sys import exit
from global_ import Global


class Button():
    def __init__(self, file, pos, callback):
        self.image = pygame.image.load(file).convert_alpha()
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.callback = callback

    def when_clicked(self, event):
        self.mouse_position = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (1,0,0) and self.rect.collidepoint(self.mouse_position):
            self.callback(self)

    def exit_game(Button):
        pygame.quit()
        exit()

    def start_game(Button):
        Global.state = 'game level'
