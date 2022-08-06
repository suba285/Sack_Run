import pygame
from image_loader import img_loader

tile_size = 32

# handles the shockwave expansion across the screen, creates the shockwave


class Shockwave:
    def __init__(self, screen, controls):
        self.radius = 0
        self.speed = 4
        self.x = 0
        self.y = 0
        self.surface = screen
        self.expand = False
        self.shock_num = 2

        self.controls = controls

        self.blit_bar = True

        self.attention_counter = 60
        self.flash_counter = 0

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

        self.shock_img = self.shockwave_bar2
        self.blit_shock = True
        self.info = False

    def update_shockwave(self, sack_rect, fps_adjust, camera_move_x, camera_move_y, mouse_adjustement, health):
        key = pygame.key.get_pressed()
        sound_trigger = False
        self.attention_counter -= 1*fps_adjust
        self.flash_counter += 1*fps_adjust
        self.info = False
        if key[self.controls['shockwave']] and not self.expand and self.shock_num > 0 and health > 0:
            self.expand = True
            self.blit_shock = False
            self.x = sack_rect.x + 10
            self.y = sack_rect.y + 15
        if self.expand:
            self.x += camera_move_x
            self.y += camera_move_y
            self.speed -= 0.075
            self.radius += self.speed * fps_adjust
            pygame.draw.circle(self.surface, (255, 255, 255), (self.x, self.y), self.radius, 1)
        if self.radius >= 100:
            self.expand = False
            self.speed = 4
            self.radius = 0
            self.shock_num -= 1
            self.blit_shock = True

        ms_pos = pygame.mouse.get_pos()
        if (self.shockwave_rect.collidepoint((ms_pos[0]/mouse_adjustement, ms_pos[1]/mouse_adjustement)) and
                pygame.mouse.get_focused()):
            self.info = True
            sound_trigger = True

        if self.info:
            self.info_move = 6
        else:
            self.info_move = 0

        if self.shock_num == 2:
            self.shock_img = self.shockwave_bar2
        elif self.shock_num == 1:
            self.shock_img = self.shockwave_bar1
        else:
            self.shock_img = self.shockwave_bar0
        if not self.blit_shock:
            self.shock_img = self.shockwave_bar_pale

        if self.attention_counter > 0:
            if self.flash_counter > 7:
                self.flash_counter = 0
                self.blit_bar = not self.blit_bar

        if self.attention_counter <= 0:
            self.blit_bar = True

        # blitting shockwave bar
        if self.blit_bar:
            self.surface.blit(self.shock_img, (self.shockwave_rect[0] + self.info_move, self.shockwave_rect[1]))

        if self.info:
            self.surface.blit(self.shockwave_info, (self.shockwave_rect.width, self.shockwave_rect[1]))

        return self.radius, sound_trigger
