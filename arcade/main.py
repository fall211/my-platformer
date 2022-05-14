# Module imports
import arcade
import arcade.gui
import json

# File imports
from settings import *
from scripts import *
from leveldata import *
from player import Player
from userinterface import *
from weapons import *

with open('arcade/playerdata.json', 'r') as import_data:
    player_data = json.load(import_data)
import_data.close()

class PlatformerRPG(arcade.Window):
    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(WIDTH, HEIGHT, WINDOW_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.ui_manager = arcade.gui.UIManager()

        self.player = None
        self.left_clicked = False
        self.tile_map = None
        self.current_level = 1
        self.enemy = None
        self.just_setup = True


    def setup(self):

        self.just_setup = True
        map_file = f'maps/map_{self.current_level}.tmj'
        layer_options = {
            'Ground': {
                'use_spatial_hash': True,
            },
            'Items': {
                'use_spatial_hash': True,
            },
            'Doors': {
                'use_spatial_hash': True,
            }
        }

        self.tile_map = arcade.load_tilemap(map_file,1,layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list('Player')
        self.scene.add_sprite_list('Attack')
        self.scene.add_sprite_list('Enemies')

        if self.current_level == 1: self.level_data = level_1
        elif self.current_level == 2: self.level_data = level_2


        # Death scene
        self.death_scene = arcade.Scene()
        self.respawn_button = RespawnButton(self)

        self.ui_manager.add(self.respawn_button)


        # Player
        self.player = Player('player', 'player', False)    
        self.player.position = (self.level_data['player_spawn_pos'])
        self.scene.add_sprite('Player', self.player)

        # Player stats    
        self.player_exp = player_data['player_exp']
        self.player_level = player_data['player_level']
        self.player.health = player_data['player_health']

        # Player physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant=GRAVITY, walls=self.scene['Ground']
        )
        self.physics_engine.enable_multi_jump(5)

        # Enemy 
        self.enemy_list = self.scene.get_sprite_list('Enemies')
        self.enemy_respawn_timer = 0



        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

    def on_draw(self):
        self.clear()
        
        if self.player.is_alive:
            self.camera.use()
            # Anything after here will be on the screen and moved with self.camera
            self.scene.draw()


            self.gui_camera.use()
            # Anything after here will be on the GUI
            self.player_exp_text = f'Exp: {self.player_exp}'
            self.player_health_text = f'Health: {self.player.health}'
            arcade.draw_text(self.player_exp_text, 20, 615, arcade.color.ROMAN_SILVER, 25)
            arcade.draw_text(self.player_health_text, 20, 660, arcade.color.RASPBERRY_GLACE, 40)

        else:
            self.ui_manager.enable()
            self.death_scene.draw()
            arcade.draw_text('you died', WIDTH/3, HEIGHT/2, arcade.color.RASPBERRY_GLACE, 70)
            self.ui_manager.draw()

    def on_key_press(self,key,modifiers):
        if self.player.is_alive:
            self.just_setup = False
            if key == arcade.key.W or key == arcade.key.SPACE:
                if self.physics_engine.can_jump():
                    self.player.change_y = PLAYER_JUMP
                    self.physics_engine.increment_jump_counter()
            if key == arcade.key.D:
                self.player.change_x += PLAYER_SPEED
            if key == arcade.key.A:
                self.player.change_x -= PLAYER_SPEED
            if key == arcade.key.P:
                save_game()

    def on_key_release(self,key,modifiers):
        if self.player.is_alive:
            if key == arcade.key.D and not self.just_setup:
                self.player.change_x -= PLAYER_SPEED
            if key == arcade.key.A and not self.just_setup:
                self.player.change_x += PLAYER_SPEED
            
            if key == arcade.key.S and self.player.collides_with_list(self.scene['Doors']):
                if self.current_level == 1: self.current_level = 2
                else: self.current_level = 1
                save_game()
                self.setup()
            
            elif key == arcade.key.L:
                print(self.player.position)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.player.is_alive:
            self.mouse_x = x + self.camera.position[0]
            self.mouse_y = y + self.camera.position[1]
            if button == arcade.MOUSE_BUTTON_LEFT: 
                self.left_clicked = True


    def on_update(self, delta_time):

        if self.player.is_alive:
            # Player update stuff
            self.physics_engine.update()
            center_camera_to_target(self,self.player)
            self.scene.update_animation(delta_time,['Player'])
            self.player.on_update(delta_time)
            
            # If you fall off the map then kill the player
            if self.player.center_y < -1000: self.player.is_alive = False

            # Player contact with enemies
            self.enemy_list = self.scene.get_sprite_list('Enemies')
            if self.player.collides_with_list(self.enemy_list):
                self.player_enemy_collision_list = self.player.collides_with_list(self.enemy_list)
                for enemy in self.player_enemy_collision_list:
                    if not enemy.on_attack_cd and not self.player.is_immune:
                        self.player.health -= ENEMY_CONTACT_DAMAGE
                        enemy.on_attack_cd = True
            if self.player.health <= 0:
                self.player.health = 0

            # Enemy update stuff
            if len(self.enemy_list) >= 1:
                self.scene.update_animation(delta_time,['Enemies'])
                for enemy in self.enemy_list:
                    self.enemy_physics_engine = arcade.PhysicsEnginePlatformer(
                        enemy, gravity_constant=GRAVITY, walls=self.scene['Ground']
                    )
                    enemy.pursue_target(self.player, self.enemy_physics_engine)
                    self.enemy_physics_engine.update()
                    enemy.on_update(delta_time)
                    if enemy.collides_with_list(self.scene['Attack']):
                        if not enemy.is_immune:
                            enemy.health -= RANGED_ATTACK_DAMAGE
                            enemy.iframes = ENEMY_IMMUNITY_TIME
                            enemy.is_provoked = True
                    if enemy.health <= 0:
                        enemy.kill()
                        self.player_exp += 1
                        enemy.is_dead = True

            if len(self.enemy_list) < ENEMY_SPAWN_CAP:
                if self.enemy_respawn_timer <= 0:
                    spawn_enemy(self, self.level_data['enemy_spawner_pos'])
                    self.enemy_respawn_timer = choice(range(60,300))
                else: self.enemy_respawn_timer -= 1


            # Attack update stuff
            laser = LaserAttack()
            melee = MeleeAttack()

            self.attack_list = self.scene.get_sprite_list('Attack')
            self.ground_list = self.scene.get_sprite_list('Ground')

            if self.player.equipped_weapon == 'laser':
                if self.left_clicked: 
                    laser.ranged_attack(self)
                laser.on_update(self.attack_list, self.ground_list)
            elif self.player.equipped_weapon == 'melee':
                if self.left_clicked:
                    self.attack_list.clear()
                    melee.melee_attack(self)
                melee.on_update(self, self.attack_list)



        else:
            pass
        



game = PlatformerRPG()

def main():
    """Main function"""
    game.setup()
    arcade.run()

def save_game():
    player_data['player_exp'] = game.player_exp
    player_data['player_level'] = game.player_level
    player_data['player_health'] = game.player.health
    with open('arcade/playerdata.json', 'w') as write_data:
        json.dump(player_data, write_data, indent=4)
        write_data.close()

if __name__ == '__main__':
    main()



# TODO:
# 
# ----now----
# 
# enemy: 
# - some death/spawn effect (particles?)
# 
# player:
# - level up system
# 
# 
# ----later on----
# 
# - esc menu with save game option (reassign key.P to the menu)
# - GUI improvements
# - inventory system
# - items, enemy drops, etc
# - different attacks... rework the laser
# - rewrite the i-frames for attacking an enemy to the weapon instead of the enemy
# - level up perks
# - better system for moving from one map to the next (and back)
# - more maps
# - more enemies
# 
# 
# ----long term----
# 
# - crafting
# - armor
# - quests/storyline
# - player customization
# - custom map that the player can edit and place stuff in
# 
# 
# ----polishment/art----
# 
# - custom art