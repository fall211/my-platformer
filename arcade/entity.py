import arcade

class Entity(arcade.Sprite):
    def __init__(self, image_folder, image_name, jump):
        super().__init__()

        self.current_texture = 0

        image_path = f'images/{image_folder}/{image_name}'

        self.idle_textures = []
        for i in range(1,9):
            texture = arcade.load_texture(f'{image_path}_{i}.png')
            self.idle_textures.append(texture)
        if jump == True:
            self.jump_textures = []
            for i in range(1,9):
                texture = arcade.load_texture(f'{image_path}_jump_{i}.png')
                self.jump_textures.append(texture)


        self.texture = arcade.load_texture(f'{image_path}_1.png')
        self.set_hit_box(self.texture.hit_box_points)

