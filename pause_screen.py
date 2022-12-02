
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
    swidth = monitor_width / fullscreen_scale
    sheight = swidth / 16 * 9

tile_size = 32


class PauseScreen:
    def __init__(self, pause_screen):
        self.pause_screen = pause_screen

        self.joystick_counter = 0
        self.joystick_moved = False
        self.hat_y_pressed = False

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

        paused_text = Text()
        self.paused_txt = paused_text.make_text(['paused'])

        self.warning_menu_txt = Text().make_text(["progress will be lost"])

        self.resume_btn = Button(swidth / 2 - self.resume_button.get_width() / 2, 64,
                                 self.resume_button, self.resume_button_press, self.resume_button_down)
        self.menu_btn = Button(swidth / 2 - self.menu_button.get_width() / 2, 98,
                               self.menu_button, self.menu_button_press, self.menu_button_down)
        self.s_button = Button(swidth / 2 - self.settings_button.get_width() / 2, 132,
                               self.settings_button, self.settings_button_press,
                               self.settings_button_down)

    def draw_pause_screen(self, mouse_adjustment, events, joysticks, joystick_configuration):

        self.pause_screen.blit(self.background, (0, 0))

        self.pause_screen.blit(self.paused_txt, (swidth / 2 - self.paused_txt.get_width() / 2, 40))

        final_over1 = False

        joystick_over0 = False
        joystick_over1 = False
        joystick_over2 = False

        for event in events:
            if event.type == pygame.JOYAXISMOTION and event.axis == joystick_configuration[0][1]:
                if event.value > 0.1 and not self.joystick_moved:
                    self.joystick_counter += 1
                    self.joystick_moved = True
                    if self.joystick_counter > 2:
                        self.joystick_counter = 0
                elif event.value < -0.1 and not self.joystick_moved:
                    self.joystick_counter -= 1
                    self.joystick_moved = True
                    if self.joystick_counter < 0:
                        self.joystick_counter = 2
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
                        self.joystick_counter = 2
                if hat_value[1] == -1:
                    self.joystick_counter += 1
                    self.hat_y_pressed = True
                    if self.joystick_counter > 2:
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

        resume, over1 = self.resume_btn.draw_button(self.pause_screen, False, mouse_adjustment, events, joystick_over0)
        menu, over2 = self.menu_btn.draw_button(self.pause_screen, False, mouse_adjustment, events, joystick_over1)
        settings, over3 = self.s_button.draw_button(self.pause_screen, False, mouse_adjustment, events, joystick_over2)

        if over1 or over2 or over3:
            final_over1 = True

        return self.pause_screen, final_over1, resume, menu, settings
