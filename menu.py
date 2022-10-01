
from button import *
from image_loader import img_loader
from font_manager import Text
import random

local_tile_size = 32
tile_size = local_tile_size

sheight = 264
swidth = 352


class mainMenu:
    def __init__(self):
        # images -------------------------------------------------------------------------------------------------------
        self.play_button = img_loader('data/images/button_play2.PNG', tile_size, tile_size * 0.75)
        self.play_button_press = img_loader('data/images/button_play2_press.PNG', tile_size, tile_size * 0.75)
        self.play_button_down = img_loader('data/images/button_play_down.PNG', tile_size, tile_size * 0.75)
        self.fps60_button = img_loader('data/images/button_fps602.PNG', tile_size * 2, tile_size / 2)
        self.fps60_button_press = img_loader('data/images/button_fps602_press.PNG', tile_size * 2, tile_size / 2)
        self.fps30_button = img_loader('data/images/button_fps302.PNG', tile_size * 2, tile_size / 2)
        self.fps30_button_press = img_loader('data/images/button_fps302_press.PNG', tile_size * 2, tile_size / 2)
        self.settings_button = img_loader('data/images/button_settings2.PNG', tile_size * 1.5, tile_size * 0.75)
        self.settings_button_press = img_loader('data/images/button_settings2_press.PNG', tile_size * 1.5,
                                                tile_size * 0.75)
        self.settings_button_down = img_loader('data/images/button_settings2_down.PNG', tile_size * 1.5,
                                               tile_size * 0.75)
        self.up_button_press = img_loader('data/images/button_up_press.PNG', tile_size * 2, tile_size / 2)
        self.up_button = img_loader('data/images/button_up.PNG', tile_size * 2, tile_size / 2)

        self.resolution_button = img_loader('data/images/button_res_small2.PNG', tile_size * 2, tile_size / 2)
        self.resolution_button_press = img_loader('data/images/button_res_small2_press.PNG',
                                                  tile_size * 2, tile_size / 2)

        self.resolution_big_button = img_loader('data/images/button_res_big2.PNG', tile_size * 2, tile_size / 2)
        self.resolution_big_button_press = img_loader('data/images/button_res_big2_press.PNG',
                                                      tile_size * 2, tile_size / 2)

        self.menu_background_raw = pygame.image.load('data/images/menu_background.PNG').convert()
        self.menu_background = pygame.transform.scale(self.menu_background_raw, (360, 296))

        self.settings_background = img_loader('data/images/settings_background2.PNG', tile_size * 2, tile_size * 2)
        self.logo = img_loader('data/images/sack_run_logo.PNG', tile_size * 4, tile_size)
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.x = swidth / 2 - self.logo.get_width() / 2
        self.logo_rect.y = 70

        self.quit_txt = Text().make_text([' Quit (ctrl + Q)'])
        self.quit_txt.set_alpha(180)
        self.quit_txt_alpha = 0

        self.author_txt = Text().make_text(['Made by Suba'])
        self.author_txt_alpha = 255

        # variables ----------------------------------------------------------------------------------------------------
        self.play_x = swidth / 2 - self.play_button.get_width() / 2
        self.play_y = 155

        self.fps_x = swidth / 2 - self.fps30_button.get_width() / 2
        self.fps_y = 211

        self.settings_x = swidth / 2 - self.settings_button.get_width() / 2
        self.settings_y = 189

        self.resolution_x = swidth / 2 - self.resolution_button.get_width() / 2
        self.resolution_y = 228

        self.fps_button = True
        self.fps_cooldown = 0

        self.res_button = True
        self.res_cooldown = 0
        self.resolution = "small"

        self.settings = False
        self.settings_cooldown = 0

        self.sack_run_logo_y = sheight / 2 - self.logo.get_height() / 2
        self.final_sack_run_logo_y = 70

        self.logo_pos_counter = 0

        self.particles = []

        self.logo_surface = pygame.Surface((swidth, 70 + self.logo.get_height()))
        self.logo_surface.set_colorkey((0, 0, 0))
        self.logo_surface.set_alpha(0)
        self.logo_surface_y = sheight / 2 - self.logo_surface.get_height() / 2

        self.button_surface = pygame.Surface((swidth, sheight))
        self.surface_alpha = 0
        self.button_surface.set_colorkey((0, 0, 0))
        self.button_surface.set_alpha(0)

        self.opening_animation_counter = 50

        self.quit_txt_bright = False

        for i in range(20):
            self.particles.append([random.randrange(0, swidth),
                                   random.randrange(1, self.logo_surface.get_height() - 2)])

        # initiating button classes ------------------------------------------------------------------------------------
        self.p_button = Button(self.play_x, self.play_y, self.play_button, self.play_button_press,
                               self.play_button_down)
        self.s_button = Button(self.settings_x, self.settings_y, self.settings_button, self.settings_button_press,
                               self.settings_button_down)

# UPDATING AND DRAWING MENU ============================================================================================
    def menu(self, menu_screen, slow_computer, mouse_adjustement, events):

        menu_screen.blit(self.menu_background, (0, 0))

        key = pygame.key.get_pressed()

        self.logo_surface.fill((0, 0, 0))
        self.button_surface.fill((0, 0, 0))

        self.opening_animation_counter += 1
        self.logo_pos_counter += 1

        for particle in self.particles:
            particle[0] += 1
            pygame.draw.circle(self.logo_surface, (136, 104, 134), particle, 1, 1)
            if particle[0] > swidth:
                particle[0] = 0
                particle[1] = random.randrange(1, self.logo_surface.get_height() - 2)
        menu_screen.blit(self.logo_surface, (0, 30))

        menu_screen.blit(self.logo, (self.logo_rect.x, self.sack_run_logo_y))
        if self.author_txt_alpha > 0:
            menu_screen.blit(self.author_txt, (swidth / 2 - self.author_txt.get_width() / 2, sheight/2 + 40))

        if self.opening_animation_counter > 280:
            if self.quit_txt_alpha < 180:
                self.quit_txt_alpha += 15
            if self.quit_txt_alpha <= 180:
                self.quit_txt.set_alpha(self.quit_txt_alpha)

            if key[pygame.K_q] or key[pygame.K_LCTRL]:
                self.quit_txt.set_alpha(255)
                self.quit_txt_bright = True
            else:
                if self.quit_txt_bright:
                    self.quit_txt_bright = False
                    self.quit_txt.set_alpha(180)

            menu_screen.blit(self.quit_txt, (swidth / 2 - self.quit_txt.get_width() / 2, 230))

        if self.opening_animation_counter > 230:
            self.surface_alpha += 8
            if self.surface_alpha <= 255:
                self.button_surface.set_alpha(self.surface_alpha)
                self.logo_surface.set_alpha(self.surface_alpha)

        if self.opening_animation_counter > 200:
            if self.sack_run_logo_y > self.final_sack_run_logo_y:
                self.sack_run_logo_y -= 1

        if self.opening_animation_counter > 180:
            if self.author_txt_alpha > 0:
                self.author_txt_alpha -= 10
                self.author_txt.set_alpha(self.author_txt_alpha)

        play = False
        fps = False
        end_over1 = False
        end_over2 = False
        over1 = False
        over2 = False
        over3 = False
        over4 = False

        if self.opening_animation_counter > 260:
            if self.logo_pos_counter >= 60:
                self.sack_run_logo_y = 70
                self.logo_pos_counter = 0
            elif self.logo_pos_counter >= 50:
                self.sack_run_logo_y = 69

        if self.opening_animation_counter > 230:
            # play button
            play, over1 = self.p_button.draw_button(self.button_surface, False, mouse_adjustement, events)

            # settings button
            settings, over2 = self.s_button.draw_button(self.button_surface, False, mouse_adjustement, events)
        else:
            settings = False
            play = False

        menu_screen.blit(self.button_surface, (0, 0))

        if (over1 or over2 or over4) and self.opening_animation_counter > 250:
            end_over1 = True

        return play, slow_computer, end_over1, end_over2, settings



