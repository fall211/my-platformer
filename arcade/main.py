

import arcade
from settings import *
from scripts import *
from player import Player
from entity import Entity
from enemy import Enemy



class PlatformerRPG(arcade.Window):
    def __init__(self):

        # call the parent class and set up the window
        super().__init__(WIDTH, HEIGHT, WINDOW_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.player = None
        self.leftclicked = False

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        
        self.scene = arcade.Scene()
        self.scene.add_sprite_list('Player')
        self.scene.add_sprite_list('Platforms',use_spatial_hash=True)
        self.scene.add_sprite_list('Coins',use_spatial_hash=True)
        self.scene.add_sprite_list('RangedAttack')

        self.playerexp = 0
        
        make_map(self,LEVEL_MAP)

        self.physicsengine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant=GRAVITY, walls=self.scene['Platforms']
        )
        self.physicsengine.enable_multi_jump(5)
        self.camera = arcade.Camera(self.width, self.height)
        self.guicamera = arcade.Camera(self.width, self.height)

    def on_draw(self):
        self.clear()
        
        self.camera.use()
        # anything after here will be on the screen and moved with self.camera
        self.scene.draw()


        self.guicamera.use()
        # anything after here will be on the GUI
        self.guitext = f"Exp: {self.playerexp}"
        arcade.draw_text(self.guitext,20,660,arcade.color.ROMAN_SILVER,40)



    def on_key_press(self,key,modifiers):
        if key == arcade.key.W or key == arcade.key.SPACE:
            if self.physicsengine.can_jump():
                self.player.change_y = PLAYER_JUMP
                self.physicsengine.increment_jump_counter()
        elif key == arcade.key.D:
            self.player.change_x += PLAYER_SPEED
        elif key == arcade.key.A:
            self.player.change_x -= PLAYER_SPEED

    def on_key_release(self,key,modifiers):
        if key == arcade.key.D:
            self.player.change_x -= PLAYER_SPEED
        elif key == arcade.key.A:
            self.player.change_x += PLAYER_SPEED

    def on_mouse_press(self, x, y, button, modifiers):
        self.mousex = x + self.camera.position[0]
        self.mousey = y + self.camera.position[1]
        if button == arcade.MOUSE_BUTTON_LEFT: 
            self.leftclicked = True

    def on_update(self, delta_time):
        self.physicsengine.update()
        center_camera_to_target(self,self.player)
        self.scene.update_animation(delta_time,['Player'])

        if self.player.center_y < -1000: self.setup()

        self.pickuplist = arcade.check_for_collision_with_list(self.player,self.scene['Coins'])
        for item in self.pickuplist:
            item.remove_from_sprite_lists()
            self.playerexp += 1

        if self.leftclicked == True:
            rangedattack(self)

        for laser in self.scene.get_sprite_list('RangedAttack'):
            laser.center_x += laser.vectorx * RANGED_ATTACK_SPEED
            laser.center_y += laser.vectory * RANGED_ATTACK_SPEED
            laser.lifespan -= 1
            if laser.lifespan == 0 or laser.collides_with_list(self.scene['Platforms']):
                laser.remove_from_sprite_lists()





def main():
    """Main function"""
    window = PlatformerRPG()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()