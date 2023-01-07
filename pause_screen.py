
from image_loader import img_loader
from font_manager import Text
from button import Button
from screen_info import global_monitor_height, global_monitor_width
import pygame

monitor_width = global_monitor_width
monitor_height = global_monitor_height

sheight = 270
swidth = 480

if monitor_width / 16 <= monitor_height / 9:
    fullscreen_scale = round(monitor_width / swidth)
    swidth = round(monitor_width / fullscreen_scale)
    sheight = round(swidth / 16 * 9)

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

        self.restart_lvl_txt = text.make_text(['restart level'])
        self.restart_lvl_txt_alpha = 0
        self.restart_lvl_txt.set_alpha(0)

        self.resume_btn = Button(swidth / 2 - self.resume_button.get_width() / 2, 64 / 270 * sheight,
                                 self.resume_button, self.resume_button_press, self.resume_button_down)
        self.menu_btn = Button(swidth / 2 - self.menu_button.get_width() / 2, 98 / 270 * sheight,
                               self.menu_button, self.menu_button_press, self.menu_button_down)
        self.s_button = Button(swidth / 2 - self.settings_button.get_width() / 2, 132 / 270 * sheight,
                               self.settings_button, self.settings_button_press,
                               self.settings_button_down)
        self.restart_button = Button(swidth / 2 - self.restart_button_img.get_width() / 2, 166 / 270 * sheight,
                                     self.reset_button_img, self.reset_button_press, self.reset_button_down)

    def draw_pause_screen(self, mouse_adjustment, events, joysticks, joystick_configuration, fps_adjust):

        self.pause_screen.blit(self.background, (0, 0))

        self.pause_screen.blit(self.paused_txt, (swidth / 2 - self.paused_txt.get_width() / 2, 40 / 270 * sheight))

        final_over1 = False

        joystick_over0 = False
        joystick_over1 = False
        joystick_over2 = False
        joystick_over3 = False

        for event in events:
            if event.type == pygame.JOYAXISMOTION and event.axis == joystick_configuration[0][1]:
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
                elif event.value == 0:
                    self.joystick_moved = False

        # D-pad input
        if joysticks:
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
            if self.joystick_counter == 1:
                joystick_over1 = True
            if self.joystick_counter == 2:
                joystick_over2 = True
            if self.joystick_counter == 3:
                joystick_over3 = True

        if joystick_over3:
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

        resume, over1 = self.resume_btn.draw_button(self.pause_screen, False, mouse_adjustment, events, joystick_over0)
        menu, over2 = self.menu_btn.draw_button(self.pause_screen, False, mouse_adjustment, events, joystick_over1)
        settings, over3 = self.s_button.draw_button(self.pause_screen, False, mouse_adjustment, events, joystick_over2)
        restart, over4 = self.restart_button.draw_button(self.pause_screen, False, mouse_adjustment, events,
                                                         joystick_over3)

        if over1 or over2 or over3 or over4:
            final_over1 = True

        return self.pause_screen, final_over1, resume, menu, settings, restart
