import pygame
from settings import *
from player import Player
from map import StartLogo, Tile
from button import Button
from camera import CameraGroup
from global_ import Global
from enemy import Enemy


class Level:
	def __init__(self):

		self.display_surface = pygame.display.get_surface() #display surface

		self.menu_sprites = pygame.sprite.Group() #sprite group for main menu
		self.menu_sprites.add(StartLogo()) #this could be changed into an instance of class

		self.obstacle_sprites = pygame.sprite.Group() #anything in here can be collided with


		self.camera_group = CameraGroup() #anything in here will be drawn, nothing else!


		self.level_setup(LEVEL_MAP)
		self.spawn_initial_enemies(LEVEL_MAP)

	def level_setup(self,levelmap):
		self.level_map = levelmap
		for row_index,row in enumerate(self.level_map):
			for col_index,col in enumerate(row):
				x = col_index * TILE_SIZE
				y = row_index * TILE_SIZE
				if col == 'X':
					Tile((x,y), "aquamarine", [self.camera_group,self.obstacle_sprites])
				if col == 'P':
					self.player = Player((x,y),self.camera_group,self.obstacle_sprites) #player instance on entity class
				if col == 'T':
					self.teleporter = Tile((x,y), "yellow", self.camera_group)


	def spawn_initial_enemies(self, levelmap):
		self.level_map = levelmap
		for row_index,row in enumerate(self.level_map):
			for col_index,col in enumerate(row):
				x = col_index * TILE_SIZE
				y = row_index * TILE_SIZE
				if col == 'E':
					self.enemy = Enemy((x,y),self.camera_group,self.player) #enemy instance of entity class

	def change_level(self,levelmap):
		self.level_map = levelmap
		self.camera_group.empty()
		self.obstacle_sprites.empty()
		self.level_setup(self.level_map)
		self.spawn_initial_enemies(self.level_map)

	def tp_check(self):
		for sprite in self.camera_group:
			if self.player.rect.colliderect(self.teleporter.rect):
				self.change_level(LEVEL_MAP_2)

	def run(self):
		#update/draw game


		if Global.state == 'game level':


			self.camera_group.update()
			self.camera_group.custom_draw(self.player)
			self.tp_check()


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
