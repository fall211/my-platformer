import arcade.gui
from settings import *
from scripts import *

class RespawnButton(arcade.gui.UIFlatButton):
    
    def __init__(self, game, x = WIDTH/2 - 100, y = HEIGHT/2 - 200, width = 200, height = 100, text = 'respawn'):
        super().__init__(x, y, width, height, text)

        x = WIDTH/2 - 100, 
        y = HEIGHT/2 - 200,
        width = 200,
        height = 100,
        text = 'respawn'
        
        self.game = game

    def on_click(self, event):
        print('clicked')
        revive_player(self.game)
        return super().on_click(event)