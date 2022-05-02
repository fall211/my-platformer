import arcade
import json
from settings import *
from player import Player
from math import atan2,degrees, sqrt


def center_camera_to_target(self,target):
    self.target = target
    screen_center_x = self.target.center_x - (self.camera.viewport_width/2)
    screen_center_y = self.target.center_y - (self.camera.viewport_height/2)
    # restrict camera movements past certain coords
    if screen_center_y < -200: screen_center_y = -200
    
    target_centered = screen_center_x, screen_center_y
    self.camera.move_to(target_centered,0.1)

def ranged_attack(self):
    mouse_to_player_angle = ((self.mouse_y-self.player.center_y), (self.mouse_x-self.player.center_x))
    mouse_to_player_radians = atan2(mouse_to_player_angle[0],mouse_to_player_angle[1])
    self.projectile = arcade.Sprite('images/world tiles/laserBlueHorizontal.png')
    self.projectile.position = self.player.position
    self.projectile.angle = degrees(mouse_to_player_radians)
    self.projectile.vector_x = (self.mouse_x-self.player.center_x) / sqrt(((self.mouse_y-self.player.center_y)**2 + (self.mouse_x-self.player.center_x)**2))
    self.projectile.vector_y = (self.mouse_y-self.player.center_y) / sqrt(((self.mouse_y-self.player.center_y)**2 + (self.mouse_x-self.player.center_x)**2))
    self.projectile.lifespan = 120

    self.scene.add_sprite('RangedAttack',self.projectile)
    self.left_clicked = False
    self.player_exp += 1
