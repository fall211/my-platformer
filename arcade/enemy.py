import arcade
from entity import Entity
from settings import *

class Enemy(Entity):
    def __init__(self):
        image_folder = 'enemy'
        image_name = 'enemy'
        jump = False
        super().__init__(image_folder,image_name, jump)

        self.jump_anim_enabled = jump
        self.health = ENEMY_HEALTH
        self.provoked = False

    def update_animation(self, delta_time: float = 1/60):
        
        if self.jump_anim_enabled == True:
            if self.change_y != 0:
                self.texture = self.jump_textures[int(self.current_texture)]
            if self.change_y == 0:
                self.texture = self.idle_textures[int(self.current_texture)]
        else: self.texture = self.idle_textures[int(self.current_texture)]

        if self.current_texture < 7:
            self.current_texture +=0.2
        else: self.current_texture = 0


    def pursue_target(self, target, physics_engine):
        self.target = target
        self.physics_engine = physics_engine

        distance = arcade.get_distance_between_sprites(self, self.target)
        y_distance = (self.center_y - self.target.center_y)

        if distance < ENEMY_PROVOKE_DIST:
            self.provoked = True
        if distance > ENEMY_LOSE_PROVOKE_DIST:
            self.provoked = False

        if self.provoked and distance > 50:
            if self.center_x > self.target.center_x and self.physics_engine.can_jump():
                self.change_x = -ENEMY_SPEED
            elif self.center_x < self.target.center_x and self.physics_engine.can_jump():
                self.change_x = ENEMY_SPEED
            else:
                pass
        else: self.change_x = 0

        if (self.physics_engine.can_jump() and
                self.provoked and 
                y_distance < ENEMY_ATTEMPT_JUMP_DIST and 
                distance < ENEMY_ATTEMPT_JUMP_DIST and
                self.target.change_y > 0):

            self.change_y = ENEMY_JUMP
