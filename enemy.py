import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,group,target):
        super().__init__(group)
        self.image = pygame.image.load('placeholders/queenslimePH.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.target = target
        self.speed = 5


    def movement(self):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        target_vec = pygame.math.Vector2(self.target.rect.center)
        self.distance = (target_vec - enemy_vec).magnitude()


        if self.distance <= 400 and self.distance >= 10:
            self.direction = (target_vec - enemy_vec).normalize()
        else: self.direction = pygame.math.Vector2()

    def update(self):
        self.movement()
        self.rect.center += self.direction * self.speed
