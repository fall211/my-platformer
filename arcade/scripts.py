import arcade
import json
from settings import *
from player import Player
from enemy import Enemy

from math import atan2,degrees, sqrt
from random import choice

def center_camera_to_target(self,target):
    self.target = target
    screen_center_x = self.target.center_x - (self.camera.viewport_width/2)
    screen_center_y = self.target.center_y - (self.camera.viewport_height/2)
    # restrict camera movements past certain coords
    if screen_center_y < -200: screen_center_y = -200
    
    target_centered = screen_center_x, screen_center_y
    self.camera.move_to(target_centered,0.1)


def spawn_enemy(self, pos_list):

    self.spawn_locations = pos_list
    self.position = choice(self.spawn_locations)

    self.enemy = Enemy()
    self.enemy.position = self.position
    self.scene.add_sprite('Enemies', self.enemy)

def revive_player(self):
    self.setup()
    self.player.health = PLAYER_HEALTH
    self.player.is_alive = True