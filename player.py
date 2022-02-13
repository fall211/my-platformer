import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.image = pygame.image.load('placeholders/playerPH.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 10


    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.direction.y = -1
        elif keys[pygame.K_s]: self.direction.y = 1
        else: self.direction.y = 0
        if keys[pygame.K_a]: self.direction.x = -1
        elif keys[pygame.K_d]: self.direction.x = 1
        else: self.direction.x = 0


    def update(self):
        self.player_input()
        self.rect.center += self.direction * self.speed
