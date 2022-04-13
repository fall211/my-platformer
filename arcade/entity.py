import arcade

class Entity(arcade.Sprite):
    def __init__(self, imagefolder, imagename, jump):
        super().__init__()

        self.currentexture = 0

        imagepath = f"images/{imagefolder}/{imagename}"

        self.idletextures = []
        for i in range(1,9):
            texture = arcade.load_texture(f"{imagepath}_{i}.png")
            self.idletextures.append(texture)
        if jump == True:
            self.jumptextures = []
            for i in range(1,9):
                texture = arcade.load_texture(f"{imagepath}_jump_{i}.png")
                self.jumptextures.append(texture)


        self.texture = arcade.load_texture(f"{imagepath}_1.png")
        self.set_hit_box(self.texture.hit_box_points)
