import arcade
import json
from settings import *
from scripts import *
from leveldata import *
from player import Player
from enemy import Enemy

with open('arcade/playerdata.json', 'r') as import_data:
    player_data = json.load(import_data)
import_data.close()

class PlatformerRPG(arcade.Window):
    def __init__(self):

        # call the parent class and set up the window
        super().__init__(WIDTH, HEIGHT, WINDOW_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.player = None
        self.left_clicked = False
        self.tile_map = None
        self.current_level = 1
        self.enemy = None
        self.just_setup = False


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
        self.scene.add_sprite_list('RangedAttack')
        self.scene.add_sprite_list('Enemies')

        if self.current_level == 1: self.level_data = level_1
        elif self.current_level == 2: self.level_data = level_2

        # Player
        self.player_exp = player_data['player_exp']
        self.player_level = player_data['player_level']
        self.player = Player('player', 'player', False)
        self.player.position = (self.level_data['player_spawn_pos'])
        self.scene.add_sprite('Player', self.player)

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
        
        self.camera.use()
        # anything after here will be on the screen and moved with self.camera
        self.scene.draw()


        self.gui_camera.use()
        # anything after here will be on the GUI
        self.gui_text = f'Exp: {self.player_exp}'
        arcade.draw_text(self.gui_text, 20, 660, arcade.color.ROMAN_SILVER, 40)


    def on_key_press(self,key,modifiers):
        self.just_setup = False
        if key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP
                self.physics_engine.increment_jump_counter()
        elif key == arcade.key.D:
            self.player.change_x += PLAYER_SPEED
        elif key == arcade.key.A:
            self.player.change_x -= PLAYER_SPEED
        elif key == arcade.key.P:
            save_game()

    def on_key_release(self,key,modifiers):
        if key == arcade.key.D and not self.just_setup:
            self.player.change_x -= PLAYER_SPEED
        elif key == arcade.key.A and not self.just_setup:
            self.player.change_x += PLAYER_SPEED
        
        elif key == arcade.key.S and self.player.collides_with_list(self.scene['Doors']):
            if self.current_level == 1: self.current_level = 2
            else: self.current_level = 1
            save_game()
            self.setup()

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_x = x + self.camera.position[0]
        self.mouse_y = y + self.camera.position[1]
        if button == arcade.MOUSE_BUTTON_LEFT: 
            self.left_clicked = True


    def on_update(self, delta_time):

        # Player update stuff
        self.physics_engine.update()
        center_camera_to_target(self,self.player)
        self.scene.update_animation(delta_time,['Player'])
        if self.player.center_y < -1000: self.setup()


        # Enemy update stuff
        self.enemy_list = self.scene.get_sprite_list('Enemies')

        if len(self.enemy_list) >= 1:
            self.scene.update_animation(delta_time,['Enemies'])
            for enemy in self.enemy_list:
                self.enemy_physics_engine = arcade.PhysicsEnginePlatformer(
                    enemy, gravity_constant=GRAVITY, walls=self.scene['Ground']
                )
                enemy.pursue_target(self.player, self.enemy_physics_engine)
                self.enemy_physics_engine.update()
                enemy.on_update(delta_time)
                if enemy.collides_with_list(self.scene['RangedAttack']):
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
        if self.left_clicked == True:
            ranged_attack(self)

        for laser in self.scene.get_sprite_list('RangedAttack'):
            laser.center_x += laser.vector_x * RANGED_ATTACK_SPEED
            laser.center_y += laser.vector_y * RANGED_ATTACK_SPEED
            laser.lifespan -= 1
            if laser.collides_with_list(self.scene['Ground']):
                laser.kill()
            elif laser.lifespan == 0:
                laser.kill()

        # print(self.player.position)
        



game = PlatformerRPG()

def main():
    """Main function"""
    game.setup()
    arcade.run()

def save_game():
    player_data['player_exp'] = game.player_exp
    player_data['player_level'] = game.player_level
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
# - damage components
# - enemy hit effects
# - some death/spawn effect (particles?)
# 
# player:
# - level up system
# - player health
# - death/revive system
# 
# 
# ----later on----
# 
# - esc menu with save game option (reassign key.P to the menu)
# - GUI improvements
# - inventory system
# - items, enemy drops, etc
# - different attacks... rework the laser
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