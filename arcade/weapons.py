from math import degrees, atan2, sqrt
import arcade

from settings import *

class Attack(arcade.Sprite):
    def __init__(self):
        super().__init__()


class LaserAttack(Attack):
    def __init__(self):
        super().__init__()

        self.projectile = arcade.Sprite('images/world tiles/laserBlueHorizontal.png')

    def ranged_attack(self, game):
        
        mouse_to_player_angle = ((game.mouse_y-game.player.center_y), (game.mouse_x-game.player.center_x))
        mouse_to_player_radians = atan2(mouse_to_player_angle[0],mouse_to_player_angle[1])
        
        self.projectile.position = game.player.position
        self.projectile.angle = degrees(mouse_to_player_radians)
        self.projectile.vector_x = (game.mouse_x-game.player.center_x) / sqrt(((game.mouse_y-game.player.center_y)**2 + (game.mouse_x-game.player.center_x)**2))
        self.projectile.vector_y = (game.mouse_y-game.player.center_y) / sqrt(((game.mouse_y-game.player.center_y)**2 + (game.mouse_x-game.player.center_x)**2))
        self.projectile.lifespan = 120

        game.scene.add_sprite('Attack',self.projectile)
        game.left_clicked = False

    def on_update(self, attack_list, barrier_list, delta_time: float = 1 / 60):
        
        self.attack_list = attack_list
        self.barrier_list = barrier_list

        for laser in self.attack_list:
            laser.center_x += laser.vector_x * RANGED_ATTACK_SPEED
            laser.center_y += laser.vector_y * RANGED_ATTACK_SPEED
            laser.lifespan -= 1
            if laser.collides_with_list(self.barrier_list):
                laser.kill()
            elif laser.lifespan <= 0:
                laser.kill()
        return super().on_update(delta_time)

class MeleeAttack(Attack):
    def __init__(self):
        super().__init__()

        self.sword = arcade.Sprite('images/world tiles/laserPurple.png', scale=15)

    def melee_attack(self, game):
        
        self.sword.center_x, self.sword.center_y = game.player.position
        self.sword.center_x += 25
        self.sword.center_y += 25
        self.sword.angle = 90

        game.scene.add_sprite('Attack', self.sword)
        game.left_clicked = False

    def on_update(self, game, attack_list, delta_time: float = 1 / 60):
        self.attack_list = attack_list

        for sword in self.attack_list:
            sword.angle -= 10
            sword.center_x, sword.center_y = game.player.position
            sword.center_x += 25
            sword.center_y += 25
        return super().on_update(delta_time)
