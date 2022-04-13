import arcade
from entity import Entity
from settings import *

class Player(Entity):
    def __init__(self, imagefolder, imagename, jump):
        super().__init__(imagefolder,imagename, jump)

        self.jump_anim_enabled = jump

    def update_animation(self, delta_time: float = 1/60):
        
        if self.jump_anim_enabled == True:
            if self.change_y != 0:
                self.texture = self.jumptextures[int(self.currentexture)]
        
        if self.change_y == 0:
            self.texture = self.idletextures[int(self.currentexture)]

        if self.currentexture < 7:
            self.currentexture +=0.2
        else: self.currentexture = 0
