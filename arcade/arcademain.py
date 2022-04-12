

import arcade
from arcadesettings import *

#comment


class PlatformerRPG(arcade.Window):
    def __init__(self):

        # call the parent class and set up the window
        super().__init__(WIDTH, HEIGHT, WINDOW_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.scene = None
        self.player = None
        self.physicsengine = None
        self.camera = None

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        
        self.scene = arcade.Scene()
        self.scene.add_sprite_list('Player')
        self.scene.add_sprite_list('MapSprites',use_spatial_hash=True)


        for row_index,row in enumerate(TEST_MAP):
            for col_index,col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'X':
                    stoneground = arcade.Sprite(':resources:images/tiles/stoneCenter.png')
                    stoneground.top = y
                    stoneground.left = x
                    self.scene.add_sprite('MapSprites',stoneground)
                if col == 'P':
                    self.player = arcade.Sprite('placeholders/playerPH.png')
                    self.player.top = y
                    self.player.left = x
                    self.scene.add_sprite('Player',self.player)

        self.physicsengine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant=GRAVITY, walls=self.scene['MapSprites']
        )
        self.physicsengine.enable_multi_jump(5)
        self.camera = arcade.Camera(self.width, self.height)

    def on_draw(self):
        self.clear()

        self.scene.draw()
        self.camera.use()

        # code to draw the screen goes here

    def on_key_press(self,key,modifiers):
        if key == arcade.key.W:
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

    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width/2)
        screen_center_y = self.player.center_y - (self.camera.viewport_height/2)

        # restrict camera movements past certain coords
        # if screen_center_x < 0:
        #     screen_center_x = 0
        if screen_center_y < -200: screen_center_y = -200
        
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered,0.1)

    def on_update(self, delta_time):
        self.physicsengine.update()
        self.center_camera_to_player()

        if self.player.center_y < -1000: self.setup()


def main():
    """Main function"""
    window = PlatformerRPG()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()