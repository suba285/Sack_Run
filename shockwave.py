import pygame
from image_loader import img_loader

tile_size = 32
sheight = 264
swidth = 352

# handles the shockwave expansion across the screen, creates the shockwave


class Shockwave:
    def __init__(self, screen):
        self.radius = 0
        self.speed = 4
        self.x = 0
        self.y = 0
        self.width = 4
        self.surface = screen
        self.expand = False

        self.blit_bar = True

        self.shockwave_bar1 = img_loader('data/images/shockwave_counter1.PNG', 2 * tile_size, tile_size)
        self.shockwave_bar2 = img_loader('data/images/shockwave_counter2.PNG', 2 * tile_size, tile_size)
        self.shockwave_bar0 = img_loader('data/images/shockwave_counter0.PNG', 2 * tile_size, tile_size)
        self.shockwave_bar_pale = img_loader('data/images/shockwave_counter_pale.PNG', 2 * tile_size, tile_size)
        self.shockwave_info = img_loader('data/images/shockwave_info.PNG', 2 * tile_size, tile_size)
        self.shockwave_rect = self.shockwave_bar1.get_rect()
        self.shockwave_rect.x = 0
        self.shockwave_rect.y = tile_size * 2 - 4
        self.shockwave_col_rect = (self.shockwave_rect[0], self.shockwave_rect[1]+6, self.shockwave_rect.width, 22)
        self.info_move = 0

    def update_shockwave(self, position, fps_adjust, trigger):
        if trigger and not self.expand:
            self.expand = True
            self.x = position[0]
            self.y = position[1]
        if self.expand:
            self.x = position[0]
            self.y = position[1]
            self.speed -= 0.075
            self.radius += self.speed * fps_adjust
            self.width -= 0.08
            pygame.draw.circle(self.surface, (255, 255, 255), (self.x, self.y), self.radius, round(self.width))
        if self.radius >= 100:
            self.expand = False
            self.speed = 4
            self.radius = 0
            self.width = 4

        return self.radius
