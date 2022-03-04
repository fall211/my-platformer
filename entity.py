import pygame


class Entity(pygame.sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)
		self.direction = pygame.math.Vector2()
		self.gravity = 1
		self.jump_speed = 20


	def horiz_collision(self):
		for sprite in self.obstacle_sprites:
			if self.rect.colliderect(sprite.rect):
				if self.direction.x < 0:
					self.rect.left = sprite.rect.right
				if self.direction.x > 0:
					self.rect.right = sprite.rect.left

	def vert_collision(self):
		for sprite in self.obstacle_sprites:
			if self.rect.colliderect(sprite.rect):
				if self.direction.y > 0:
					self.rect.bottom = sprite.rect.top
					self.direction.y = 0
				if self.direction.y < 0:
					self.rect.top = sprite.rect.bottom
					self.direction.y = 0
