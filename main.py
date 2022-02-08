import pygame
from sys import exit
from settings import *
from level import Level
from button import *


class Game:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('My Game')
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True: #everything happens in this loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


            self.level.run()

            pygame.display.update() #update the screen when While True is on
            self.clock.tick(fps)




if __name__ == '__main__':
	Game().run()
