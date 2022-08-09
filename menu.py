from button import *
local_tile_size = 32
tile_size = local_tile_size
from image_loader import img_loader


sheight = 264
swidth = 352


class mainMenu:
    def __init__(self, screen):
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

        # initiating button classes ------------------------------------------------------------------------------------
        self.p_button = Button(self.play_x, self.play_y, self.play_button, self.play_button_press,
                               self.play_button_down)
        self.s_button = Button(self.settings_x, self.settings_y, self.settings_button, self.settings_button_press,
                               self.settings_button_down)
        self.f60_button = Button(self.fps_x, self.fps_y, self.fps60_button, self.fps60_button_press,
                                 self.fps60_button)
        self.f30_button = Button(self.fps_x, self.fps_y, self.fps30_button, self.fps30_button_press,
                                 self.fps30_button)
        self.res_btn = Button(self.resolution_x, self.resolution_y, self.resolution_button,
                                     self.resolution_button_press, self.resolution_button)

# UPDATING AND DRAWING MENU ============================================================================================
    def menu(self, menu_screen, slow_computer, mouse_adjustement, events):

        menu_screen.blit(self.menu_background, (0, 0))
        menu_screen.blit(self.logo, (swidth / 2 - self.logo.get_width() / 2, 70))

        play = False
        fps = False
        end_over1 = False
        end_over2 = False
        over1 = False
        over2 = False
        over3 = False
        over4 = False

        # play button
        play, over1 = self.p_button.draw_button(menu_screen, False, mouse_adjustement, events)

        if self.settings:
            # drawing settings background onto the screen
            menu_screen.blit(self.settings_background, (swidth / 2 - tile_size, sheight/2 + 59))

        # settings button
        settings, over2 = self.s_button.draw_button(menu_screen, False, mouse_adjustement, events)

        if over1 or over2 or over4:
            end_over1 = True

        return play, slow_computer, end_over1, end_over2, settings



