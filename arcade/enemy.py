import arcade
from entity import Entity
from settings import *
from random import choice

class Enemy(Entity):
    def __init__(self):
        image_folder = 'enemy'
        image_name = 'enemy'
        jump = False
        super().__init__(image_folder,image_name, jump)

        self.jump_anim_enabled = jump
        self._health = ENEMY_HEALTH
        self._is_dead = False
        self._is_provoked = False
        self.idle_distance = ENEMY_IDLE_WALK_DISTANCE
        self.should_move = True
        self.direction = choice(['left', 'right'])

        self._is_immune = False
        self.iframes = 0

        self._on_attack_cd = False
        self.attack_cd = 0

    @property
    def health(self):
        return self._health
    @health.setter
    def health(self, value):
        self._health = value
        self.is_immune = True

    @property
    def is_dead(self):
        return self._is_dead
    @is_dead.setter
    def is_dead(self, bool):
        self._is_dead = bool

    @property
    def is_provoked(self):
        return self._is_provoked
    @is_provoked.setter
    def is_provoked(self, bool):
        self._is_provoked = bool

    @property
    def on_attack_cd(self):
        return self._on_attack_cd
    @on_attack_cd.setter
    def on_attack_cd(self, bool):
        self._on_attack_cd = bool
        if self._on_attack_cd == True:
            self.attack_cd = ENEMY_ATTACK_SPEED

    # Immunity property
    @property
    def is_immune(self):
        return self._is_immune
    @is_immune.setter
    def is_immune(self, bool):
        self._is_immune = bool
        if self._is_immune == True:
            self.alpha = 90
            self.iframes = ENEMY_IMMUNITY_TIME
        else: self.alpha = 255



    def on_update(self, delta_time: float = 1 / 60):

        # I-frames for being attacked
        self.iframes -= delta_time
        if self.iframes <= 0:
            self.is_immune = False
        
        # Attack CD for attacking player
        self.attack_cd -= delta_time
        if self.attack_cd <= 0:
            self.on_attack_cd = False


        return super().on_update(delta_time)


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

    def idle_movement(self):
        if self.idle_distance >= 0 and self.should_move:
            if self.direction == 'right':
                self.change_x = ENEMY_SPEED - ENEMY_IDLE_SPEED_REDUCTION
            elif self.direction == 'left':
                self.change_x = -ENEMY_SPEED + ENEMY_IDLE_SPEED_REDUCTION
            self.idle_distance -= 1
        elif self.idle_distance < 0:
            self.change_x = 0
            if self.direction == 'right':
                self.direction = 'left'
            else: self.direction = 'right'
            self.idle_distance = ENEMY_IDLE_WALK_DISTANCE
            self.should_move = True


    def pursue_target(self, target, physics_engine):
        self.target = target
        self.physics_engine = physics_engine

        distance = arcade.get_distance_between_sprites(self, self.target)
        y_distance = (self.center_y - self.target.center_y)

        if distance < ENEMY_PROVOKE_DIST:
            self.is_provoked = True
        if distance > ENEMY_LOSE_PROVOKE_DIST:
            self.is_provoked = False

        if self.is_provoked and distance > 50:
            if self.center_x > self.target.center_x and self.physics_engine.can_jump():
                self.change_x = -ENEMY_SPEED
            elif self.center_x < self.target.center_x and self.physics_engine.can_jump():
                self.change_x = ENEMY_SPEED
            else:
                pass
        else:
            if not self.is_provoked:
                self.idle_movement()
            else: self.change_x = 0

        if (self.physics_engine.can_jump() and
                self.is_provoked and 
                y_distance < ENEMY_ATTEMPT_JUMP_DIST and 
                distance < ENEMY_ATTEMPT_JUMP_DIST and
                self.target.change_y > 0):

            self.change_y = ENEMY_JUMP
