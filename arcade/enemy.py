import arcade
from entity import Entity
from settings import *

class Enemy(Entity):
    def __init__(self, image):
        super().__init__(image)