import arcade
from settings import *

def make_map(self,map):
    self.levelmap = map
    for row_index,row in enumerate(self.levelmap):
        for col_index,col in enumerate(row):
            x = col_index * TILE_SIZE + 64
            y = row_index * TILE_SIZE + 64
            if col == 'X':
                floor = arcade.Sprite(':resources:images/tiles/stoneCenter.png')
                floor.top = y
                floor.left = x
                self.scene.add_sprite('Platforms',floor)
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

def center_camera_to_target(self,target):
    self.target = target
    screen_center_x = self.target.center_x - (self.camera.viewport_width/2)
    screen_center_y = self.target.center_y - (self.camera.viewport_height/2)
    # restrict camera movements past certain coords
    if screen_center_y < -200: screen_center_y = -200
    
    target_centered = screen_center_x, screen_center_y
    self.camera.move_to(target_centered,0.1)