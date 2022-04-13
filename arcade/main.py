

import arcade
from settings import *



class PlatformerRPG(arcade.Window):
    def __init__(self):

        # call the parent class and set up the window
        super().__init__(WIDTH, HEIGHT, WINDOW_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.scene = None
        self.player = None
        self.physicsengine = None
        self.camera = None
        self.guicamera = None
        self.playerexp = None
        # self.map = None

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        
        self.scene = arcade.Scene()
        self.scene.add_sprite_list('Player')
        self.scene.add_sprite_list('Platforms',use_spatial_hash=True)
        self.scene.add_sprite_list('Coins',use_spatial_hash=True)

        self.playerexp = 0
        
        # mapname = ':resources:tiled_maps/map2_level_1.json'
        # layeroptions = {'Platforms':{'use_spatial_hash':True,},}
        # self.map = arcade.load_tilemap(mapname,1,layeroptions)
        # self.scene = arcade.Scene.from_tilemap(self.map)


        for row_index,row in enumerate(LEVEL_MAP):
            for col_index,col in enumerate(row):
                x = col_index * TILE_SIZE + 64
                y = row_index * TILE_SIZE + 64
                if col == 'X':
                    stoneground = arcade.Sprite(':resources:images/tiles/stoneCenter.png')
                    stoneground.top = y
                    stoneground.left = x
                    self.scene.add_sprite('Platforms',stoneground)
                if col == 'P':
                    self.player = arcade.Sprite('placeholders/playerPH.png')
                    self.player.top = y
                    self.player.left = x
                    self.scene.add_sprite('Player',self.player)
                if col == 'C':
                    gem = arcade.Sprite(':resources:images/items/gemYellow.png')
                    gem.top = y - 64
                    gem.left = x
                    self.scene.add_sprite('Coins',gem)

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

    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width/2)
        screen_center_y = self.player.center_y - (self.camera.viewport_height/2)

        # restrict camera movements past certain coords
        if screen_center_y < -200: screen_center_y = -200
        
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered,0.1)

    def on_update(self, delta_time):
        self.physicsengine.update()
        self.center_camera_to_player()

        if self.player.center_y < -1000: self.setup()

        self.pickuplist = arcade.check_for_collision_with_list(self.player,self.scene['Coins'])
        for item in self.pickuplist:
            item.remove_from_sprite_lists()
            self.playerexp += 1

def main():
    """Main function"""
    window = PlatformerRPG()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()