
from button import *
from image_loader import img_loader
from font_manager import Text
from screen_info import swidth, sheight
import random
import math
import json

local_tile_size = 32
tile_size = local_tile_size


class mainMenu:
    def __init__(self):
        self.text = Text()

        # images -------------------------------------------------------------------------------------------------------
        self.play_button = img_loader('data/images/button_play2.PNG', tile_size, tile_size * 0.75)
        self.play_button_press = img_loader('data/images/button_play2_press.PNG', tile_size, tile_size * 0.75)
        self.play_button_down = img_loader('data/images/button_play_down.PNG', tile_size, tile_size * 0.75)
        self.settings_button = img_loader('data/images/button_settings2.PNG', tile_size * 1.5, tile_size * 0.75)
        self.settings_button_press = img_loader('data/images/button_settings2_press.PNG', tile_size * 1.5,
                                                tile_size * 0.75)
        self.settings_button_down = img_loader('data/images/button_settings2_down.PNG', tile_size * 1.5,
                                               tile_size * 0.75)

        self.menu_background_raw = pygame.image.load('data/images/menu_background.PNG').convert()
        self.menu_background = pygame.transform.scale(self.menu_background_raw, (swidth, sheight))

        self.logo = img_loader('data/images/sack_run_logo.PNG', tile_size * 4, tile_size)
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.x = swidth / 2 - self.logo.get_width() / 2
        self.logo_rect.y = round(sheight * 0.26)

        self.quit_txt = self.text.make_text([' Quit (ctrl + Q)'])
        self.quit_txt_y = round(sheight * 0.85)
        self.quit_txt.set_alpha(180)
        self.quit_txt_alpha = 0

        self.author_txt = self.text.make_text(['Made by Suba'])
        self.author_txt_alpha = 255

        self.screen_alpha = 0

        # variables ----------------------------------------------------------------------------------------------------
        self.play_x = swidth / 2 - self.play_button.get_width() / 2
        self.play_y = round(sheight * 0.57)

        self.settings_x = swidth / 2 - self.settings_button.get_width() / 2
        self.settings_y = round(sheight * 0.7)

        self.settings = False
        self.settings_cooldown = 0

        self.sack_run_logo_y = sheight / 2 - self.logo.get_height() / 2
        self.final_sack_run_logo_y = round(70 / 270 * sheight)

        self.logo_pos_counter = 0

        self.particles = []

        self.joystick_counter = 0
        self.joystick_moved = False
        self.hat_y_pressed = False

        self.logo_surface = pygame.Surface((swidth, self.logo_rect.y + self.logo.get_height()))
        self.logo_surface.set_colorkey((0, 0, 0))
        self.logo_surface.set_alpha(0)
        self.logo_surface_y = round(30 / 270 * sheight)

        self.button_surface = pygame.Surface((swidth, sheight))
        self.surface_alpha = 0
        self.button_surface.set_colorkey((0, 0, 0))
        self.button_surface.set_alpha(0)

        self.opening_animation_counter = 50

        self.quit_txt_bright = False

        for i in range(20):
            self.particles.append([random.randrange(0, swidth),
                                   random.randrange(1, self.logo_surface.get_height() - 2)])

        # loading speed run times
        try:
            with open('data/times.json', 'r') as json_file:
                times_data = json.load(json_file)
                self.time = times_data['time']
        except FileNotFoundError:
            self.time = 'no data'

        if self.time == 'no data':
            self.best_time_txt = self.text.make_text(['Speedrun'])
        else:
            self.best_time_txt = self.text.make_text([f'Best time: ' + self.time])
        self.best_time_txt_alpha = 0
        self.best_time_txt.set_alpha(0)
        self.best_time_width = self.best_time_txt.get_width()

        # initiating button classes ------------------------------------------------------------------------------------
        self.p_button = Button(self.play_x, self.play_y, self.play_button, self.play_button_press,
                               self.play_button_down)
        self.s_button = Button(self.settings_x, self.settings_y, self.settings_button, self.settings_button_press,
                               self.settings_button_down)

    def update_time(self):
        try:
            with open('data/times.json', 'r') as json_file:
                times_data = json.load(json_file)
                self.time = times_data['time']
        except FileNotFoundError:
            self.time = 'no data'
        if self.time == 'no data':
            self.best_time_txt = self.text.make_text(['Speedrun'])
        else:
            self.best_time_txt = self.text.make_text([f'Best time: ' + self.time])
        self.best_time_width = self.best_time_txt.get_width()

# UPDATING AND DRAWING MENU ============================================================================================
    def menu(self, menu_screen, mouse_adjustement, events, fps_adjust, joysticks, speedrun_mode):

        menu_screen.blit(self.menu_background, (0, 0))

        key = pygame.key.get_pressed()

        joystick_sound = False
        joystick_over1 = False
        joystick_over0 = False

        self.screen_alpha += 6 * fps_adjust
        if self.screen_alpha <= 255:
            menu_screen.set_alpha(self.screen_alpha)
        if self.screen_alpha > 255 > menu_screen.get_alpha():
            menu_screen.set_alpha(255)

        if self.screen_alpha > 255:
            self.opening_animation_counter += 1 * fps_adjust
            self.logo_pos_counter += 1 * fps_adjust

        # vertical axis input
        if events['joyaxismotion_y']:
            event = events['joyaxismotion_y']
            # down
            if event.value > 0.1 and not self.joystick_moved:
                self.joystick_counter += 1
                self.joystick_moved = True
                joystick_sound = True
                if self.joystick_counter > 1:
                    self.joystick_counter = 0
            # up
            elif event.value < -0.1 and not self.joystick_moved:
                self.joystick_counter -= 1
                joystick_sound = True
                self.joystick_moved = True
                if self.joystick_counter < 0:
                    self.joystick_counter = 1
            elif event.value == 0:
                self.joystick_moved = False
        # D-pad input
        if joysticks:
            hat_value = joysticks[0].get_hat(0)
            if hat_value[1] == -1 and not self.hat_y_pressed:
                self.hat_y_pressed = True
                self.joystick_counter += 1
                if self.joystick_counter > 1:
                    self.joystick_counter = 0
            if hat_value[1] == 1 and not self.hat_y_pressed:
                self.hat_y_pressed = True
                self.joystick_counter -= 1
                if self.joystick_counter < 0:
                    self.joystick_counter = 1
            if hat_value[1] == 0:
                self.hat_y_pressed = False

        if joysticks:
            if self.joystick_counter == 1:
                joystick_over1 = True
            if self.joystick_counter == 0:
                joystick_over0 = True

        self.logo_surface.fill((0, 0, 0))
        self.button_surface.fill((0, 0, 0))

        for particle in self.particles:
            if speedrun_mode:
                part_speed = 6
                particle[0] += part_speed * fps_adjust
                pygame.draw.line(self.logo_surface, (136, 104, 134), particle, (particle[0] + 50, particle[1]), 1)
            else:
                part_speed = 1
                particle[0] += part_speed * fps_adjust
                pygame.draw.circle(self.logo_surface, (136, 104, 134), particle, 1, 1)
            if particle[0] > swidth:
                particle[0] = 0
                if speedrun_mode:
                    particle[0] = -50
                particle[1] = random.randrange(1, self.logo_surface.get_height() - 2)
        menu_screen.blit(self.logo_surface, (0, self.logo_surface_y))

        menu_screen.blit(self.logo, (self.logo_rect.x, int(self.sack_run_logo_y)))
        if self.author_txt_alpha > 0:
            menu_screen.blit(self.author_txt, (swidth / 2 - self.author_txt.get_width() / 2,
                                               sheight/2 + round(270 / 40 * sheight)))

        if self.opening_animation_counter > 280:
            if self.quit_txt_alpha < 180:
                self.quit_txt_alpha += 15 * fps_adjust
            if self.quit_txt_alpha <= 180:
                self.quit_txt.set_alpha(self.quit_txt_alpha)

            if key[pygame.K_q] or key[pygame.K_LCTRL]:
                self.quit_txt.set_alpha(255)
                self.quit_txt_bright = True
            else:
                if self.quit_txt_bright:
                    self.quit_txt_bright = False
                    self.quit_txt.set_alpha(180)

            menu_screen.blit(self.quit_txt, (swidth / 2 - self.quit_txt.get_width() / 2, self.quit_txt_y))

        if self.opening_animation_counter > 230:
            self.surface_alpha += 8 * fps_adjust
            if self.surface_alpha <= 255:
                self.button_surface.set_alpha(self.surface_alpha)
                self.logo_surface.set_alpha(self.surface_alpha)

        if self.opening_animation_counter > 200:
            if self.sack_run_logo_y > self.final_sack_run_logo_y:
                self.sack_run_logo_y -= 1 / 270 * sheight * fps_adjust

        if self.opening_animation_counter > 180:
            if self.author_txt_alpha > 0:
                self.author_txt_alpha -= 10 * fps_adjust
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
            self.sack_run_logo_y = self.final_sack_run_logo_y - math.sin(self.logo_pos_counter / 16) * 3
            if self.best_time_txt_alpha < 255:
                self.best_time_txt_alpha += 5 * fps_adjust
                self.best_time_txt.set_alpha(self.best_time_txt_alpha)

        if self.opening_animation_counter > 230:
            # play button
            play, over1 = self.p_button.draw_button(self.button_surface, False,
                                                    mouse_adjustement, events, joystick_over0)

            # settings button
            settings, over2 = self.s_button.draw_button(self.button_surface, False,
                                                        mouse_adjustement, events, joystick_over1)
        else:
            settings = False
            play = False

        menu_screen.blit(self.button_surface, (0, 0))

        if self.best_time_txt_alpha > 0 and speedrun_mode:
            menu_screen.blit(self.best_time_txt, (swidth / 2 - self.best_time_width / 2,
                                                  sheight / 2 - 10 - math.sin(self.logo_pos_counter / 16 - 0.9) * 2))

        if (over1 or over2 or over4) and self.opening_animation_counter > 250:
            end_over1 = True

        if joystick_sound:
            end_over1 = True

        return play, end_over1, end_over2, settings
