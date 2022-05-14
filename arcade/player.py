import arcade
from entity import Entity
from settings import *

class Player(Entity):
    def __init__(self, image_folder, image_name, jump):
        super().__init__(image_folder,image_name, jump)

        self.jump_anim_enabled = jump

        self.x = 0
        self.y = 0
        self._is_alive = True
        self._health = PLAYER_HEALTH
        self.equipped_weapon = 'laser'
        self._is_immune = False
        self.iframes = PLAYER_IMMUNITY_TIME

    # Health property
    @property
    def health(self):
        return self._health
    @health.setter
    def health(self, value):
        self._health = value
        self.is_immune = True
        if self.health > 0:
            self.is_alive = True
        else:
            self.is_alive = False

    # Immunity property
    @property
    def is_immune(self):
        return self._is_immune
    @is_immune.setter
    def is_immune(self, bool):
        self._is_immune = bool
        if self._is_immune == True:
            self.alpha = 90
            self.iframes = PLAYER_IMMUNITY_TIME
        else: self.alpha = 255

    # Is alive property
    @property
    def is_alive(self):
        return self._is_alive
    @is_alive.setter
    def is_alive(self, bool):
        self._is_alive = bool


    def on_update(self, delta_time: float = 1 / 60):

        self.iframes -= delta_time
        if self.iframes <= 0:
            self.is_immune = False

        return super().on_update(delta_time)

    def update_animation(self, delta_time: float = 1/60):
        
        if self.jump_anim_enabled == True:
            if self.change_y != 0:
                self.texture = self.jump_textures[int(self.current_texture)]
        
        if self.change_y == 0:
            self.texture = self.idle_textures[int(self.current_texture)]

        if self.current_texture < 7:
            self.current_texture +=0.2
        else: self.current_texture = 0
