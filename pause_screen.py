import pygame._sdl2
from image_loader import img_loader
from font_manager import Text
from button import Button
from screen_info import swidth, sheight
from settings import colour_inversion
from popup_bg_generator import popup_bg_generator

tile_size = 32


class PauseScreen:
    def __init__(self, pause_screen):
        self.pause_screen = pause_screen

        text = Text()

        self.joystick_counter = 0
        self.joystick_moved = False
        self.hat_y_pressed = False

        self.restart_over_counter = 0

        self.background = img_loader('data/images/menu_background.PNG', swidth, sheight)

        self.resume_button = img_loader('data/images/button_resume.PNG', tile_size * 1.5, tile_size * 0.75)
        self.resume_button_press = img_loader('data/images/button_resume_press.PNG', tile_size * 1.5, tile_size * 0.75)
        self.resume_button_down = img_loader('data/images/button_resume_down.PNG', tile_size * 1.5, tile_size * 0.75)

        self.menu_button = img_loader('data/images/button_menu.PNG', tile_size * 1.5, tile_size * 0.75)
        self.menu_button_press = img_loader('data/images/button_menu_press.PNG', tile_size * 1.5, tile_size * 0.75)
        self.menu_button_down = img_loader('data/images/button_menu_down.PNG', tile_size * 1.5, tile_size * 0.75)

        self.settings_button = img_loader('data/images/button_settings2.PNG', tile_size * 1.5, tile_size * 0.75)
        self.settings_button_press = img_loader('data/images/button_settings2_press.PNG', tile_size * 1.5,
                                                tile_size * 0.75)
        self.settings_button_down = img_loader('data/images/button_settings2_down.PNG', tile_size * 1.5,
                                               tile_size * 0.75)

        self.restart_button_img = img_loader('data/images/button_restart.PNG', tile_size * 1.5, tile_size * 0.75)
        self.restart_button_press = img_loader('data/images/button_restart_press.PNG',
                                               tile_size * 1.5, tile_size * 0.75)
        self.restart_button_down = img_loader('data/images/button_restart_down.PNG', tile_size * 1.5, tile_size * 0.75)

        self.reset_button_img = img_loader('data/images/button_reset.PNG', tile_size * 1.5, tile_size * 0.75)
        self.reset_button_press = img_loader('data/images/button_reset_press.PNG', tile_size * 1.5, tile_size * 0.75)
        self.reset_button_down = img_loader('data/images/button_reset_down.PNG', tile_size * 1.5, tile_size * 0.75)

        self.paused_txt = text.make_text(['paused'])

        self.enter_symbol = img_loader('data/images/enter_symbol.PNG', 7, 9)
        self.esc_txt = text.make_text(['esc'])
        self.tab_txt = text.make_text(['tab'])
        self.btn_key_bg_left = img_loader('data/images/button_key_bg.PNG', 24, 27)
        self.btn_key_bg_right = pygame.transform.flip(self.btn_key_bg_left, True, False)

        self.restart_lvl_txt = text.make_text(['restart level'])
        self.restart_lvl_txt_alpha = 0
        self.restart_lvl_txt.set_alpha(0)

        self.resume_btn_pos = (swidth / 2 - self.resume_button.get_width() / 2, 64 / 270 * sheight)
        self.menu_btn_pos = (swidth / 2 - self.menu_button.get_width() / 2, 98 / 270 * sheight)
        self.restart_btn_pos = (swidth / 2 - self.restart_button_img.get_width() / 2, 166 / 270 * sheight)

        self.resume_btn = Button(swidth / 2 - self.resume_button.get_width() / 2, 64 / 270 * sheight,
                                 self.resume_button, self.resume_button_press, self.resume_button_down)
        self.menu_btn = Button(swidth / 2 - self.menu_button.get_width() / 2, 98 / 270 * sheight,
                               self.menu_button, self.menu_button_press, self.menu_button_down)
        self.s_button = Button(swidth / 2 - self.settings_button.get_width() / 2, 132 / 270 * sheight,
                               self.settings_button, self.settings_button_press,
                               self.settings_button_down)
        self.restart_button = Button(swidth / 2 - self.restart_button_img.get_width() / 2, 166 / 270 * sheight,
                                     self.reset_button_img, self.reset_button_press, self.reset_button_down)
        self.restart_over = False

    def draw_pause_screen(self, mouse_adjustment, events, joysticks, joystick_controls, fps_adjust, no_restart):

        self.pause_screen.blit(self.background, (0, 0))

        self.pause_screen.blit(self.paused_txt, (swidth / 2 - self.paused_txt.get_width() / 2, 40 / 270 * sheight))

        final_over1 = False

        hat_value = [0, 0]

        use_btn = joystick_controls[5]

        key = pygame.key.get_pressed()

        joystick_over0 = False
        joystick_over1 = False
        joystick_over2 = False
        joystick_over3 = False

        if events['joyaxismotion_y']:
            event = events['joyaxismotion_y']
            if event.value > 0.1 and not self.joystick_moved:
                self.joystick_counter += 1
                self.joystick_moved = True
                if self.joystick_counter > 3:
                    self.joystick_counter = 0
            elif event.value < -0.1 and not self.joystick_moved:
                self.joystick_counter -= 1
                self.joystick_moved = True
                if self.joystick_counter < 0:
                    self.joystick_counter = 3
            elif abs(event.value) < 0.02:
                self.joystick_moved = False

        if events['joyhatdown']:
            event = events['joyhatdown']
            # hat input
            if joystick_controls[0]:
                if event.button == joystick_controls[0][0]:  # right
                    hat_value[0] = 1
                if event.button == joystick_controls[0][1]:  # down
                    hat_value[1] = -1
                if event.button == joystick_controls[0][2]:  # left
                    hat_value[0] = -1
                if event.button == joystick_controls[0][3]:  # up
                    hat_value[1] = 1

        # D-pad input
        if joysticks and joysticks[0].get_numhats() > 0:
            hat_value = joysticks[0].get_hat(0)

        if not self.hat_y_pressed:
            if hat_value[1] == 1:
                self.joystick_counter -= 1
                self.hat_y_pressed = True
                if self.joystick_counter < 0:
                    self.joystick_counter = 3
            if hat_value[1] == -1:
                self.joystick_counter += 1
                self.hat_y_pressed = True
                if self.joystick_counter > 3:
                    self.joystick_counter = 0
        if hat_value[1] == 0:
            self.hat_y_pressed = False

        if joysticks:
            if self.joystick_counter == 0:
                joystick_over0 = True
            elif self.joystick_counter == 1:
                joystick_over1 = True
            elif self.joystick_counter == 2:
                joystick_over2 = True
            elif self.joystick_counter == 3:
                joystick_over3 = True

        if joystick_over3 or self.restart_over:
            self.restart_over_counter += 1 * fps_adjust
            if self.restart_over_counter > 25:
                self.restart_lvl_txt_alpha += 25 * fps_adjust
                if self.restart_lvl_txt_alpha > 255:
                    self.restart_lvl_txt_alpha = 255
                if self.restart_lvl_txt_alpha <= 255:
                    self.restart_lvl_txt.set_alpha(self.restart_lvl_txt_alpha)
                self.pause_screen.blit(self.restart_lvl_txt, (swidth / 2 + self.restart_button_img.get_width() / 2 + 10,
                                                              174 / 270 * sheight))
        else:
            self.restart_lvl_txt_alpha = 0
            self.restart_over_counter = 0

        if not joysticks:
            resume_key_bg = self.btn_key_bg_right.copy()
            resume_key_txt = colour_inversion(self.esc_txt.copy(), (43, 31, 47))
            resume_key_txt.set_colorkey((255, 255, 255))
            resume_key_bg.blit(resume_key_txt, (4, 9))
            self.pause_screen.blit(resume_key_bg, (self.resume_btn_pos[0] + 43, self.resume_btn_pos[1]))

            menu_key_bg = self.btn_key_bg_right.copy()
            menu_key_txt = self.tab_txt
            if not key[pygame.K_TAB]:
                menu_key_txt = colour_inversion(self.tab_txt.copy(), (43, 31, 47))
                menu_key_txt.set_colorkey((255, 255, 255))
            menu_key_bg.blit(menu_key_txt, (6, 9))
            self.pause_screen.blit(menu_key_bg, (self.menu_btn_pos[0] + 37, self.menu_btn_pos[1]))

            restart_key_bg = self.btn_key_bg_right.copy()
            restart_key_txt = self.enter_symbol
            if not key[pygame.K_RETURN]:
                restart_key_txt = colour_inversion(self.enter_symbol.copy(), (43, 31, 47))
                restart_key_txt.set_colorkey((255, 255, 255))
            restart_key_bg.blit(restart_key_txt, (12, 9))
            self.pause_screen.blit(restart_key_bg, (self.restart_btn_pos[0] + 33, self.restart_btn_pos[1]))

        resume, over1 = self.resume_btn.draw_button(self.pause_screen, False, mouse_adjustment, events,
                                                    joystick_over0, use_btn)
        menu, over2 = self.menu_btn.draw_button(self.pause_screen, False, mouse_adjustment, events,
                                                joystick_over1, use_btn, shortcut_key=pygame.K_TAB)
        settings, over3 = self.s_button.draw_button(self.pause_screen, False, mouse_adjustment, events,
                                                    joystick_over2, use_btn)
        if not no_restart:
            restart, self.restart_over = self.restart_button.draw_button(self.pause_screen, False, mouse_adjustment,
                                                                         events, joystick_over3, use_btn,
                                                                         shortcut_key=pygame.K_RETURN)
        else:
            restart, self.restart_over = False, False

        if over1 or over2 or over3 or self.restart_over:
            final_over1 = True

        return self.pause_screen, final_over1, resume, menu, settings, restart
