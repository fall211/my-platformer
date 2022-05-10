import arcade
from entity import Entity
from settings import *

class Player(Entity):
    def __init__(self, image_folder, image_name, jump):
        super().__init__(image_folder,image_name, jump)

        self.jump_anim_enabled = jump

        self.x = 0
        self.y = 0
        self.health = 100

    def update_animation(self, delta_time: float = 1/60):
        
        if self.jump_anim_enabled == True:
            if self.change_y != 0:
                self.texture = self.jump_textures[int(self.current_texture)]
        
        if self.change_y == 0:
            self.texture = self.idle_textures[int(self.current_texture)]

        if self.current_texture < 7:
            self.current_texture +=0.2
        else: self.current_texture = 0
