import pygame
from entity import Entity

class Player(Entity):
    def __init__(self,pos,group,obstacle_sprites):
        super().__init__(group)
        self.image = pygame.image.load('placeholders/playerPH.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = 10
        self.obstacle_sprites = obstacle_sprites


    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]: self.direction.x = -1
        elif keys[pygame.K_d]: self.direction.x = 1
        else: self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.direction.y = -self.jump_speed

    def player_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        self.player_input()
        self.rect.x += self.direction.x * self.speed
        self.horiz_collision()
        self.player_gravity()
        self.vert_collision()

        #simple collision
        #if self.rect.y > HEIGHT: self.rect.y = HEIGHT
