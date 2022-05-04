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


    def setup(self):

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

        # Enemy temp
        self.enemy = Enemy()
        self.enemy.position = (2250,630)
        self.scene.add_sprite('Enemies', self.enemy)

        self.enemy_physics_engine = arcade.PhysicsEnginePlatformer(
            self.enemy, gravity_constant=GRAVITY, walls=self.scene['Ground']
        )

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
        if key == arcade.key.D:
            self.player.change_x -= PLAYER_SPEED
        elif key == arcade.key.A:
            self.player.change_x += PLAYER_SPEED
        
        elif key == arcade.key.S and self.player.collides_with_list(self.scene['Doors']):
            if self.current_level == 1: self.current_level = 2
            else: self.current_level = 1
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
        self.enemy.pursue_target(self.player, self.enemy_physics_engine)
        self.scene.update_animation(delta_time,['Enemies'])
        self.enemy_physics_engine.update()


        # Attack update stuff
        if self.left_clicked == True:
            ranged_attack(self)

        for laser in self.scene.get_sprite_list('RangedAttack'):
            laser.center_x += laser.vector_x * RANGED_ATTACK_SPEED
            laser.center_y += laser.vector_y * RANGED_ATTACK_SPEED
            laser.lifespan -= 1
            if laser.lifespan == 0 or laser.collides_with_list(self.scene['Ground']):
                laser.remove_from_sprite_lists()

        



window = PlatformerRPG()

def main():
    """Main function"""
    window.setup()
    arcade.run()

def save_game():
    player_data['player_exp'] = window.player_exp
    player_data['player_level'] = window.player_level
    with open('arcade/playerdata.json', 'w') as write_data:
        json.dump(player_data, write_data, indent=4)
        write_data.close()

if __name__ == '__main__':
    main()



