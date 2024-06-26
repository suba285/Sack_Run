import random

import pygame._sdl2
import math
from button import Button
from image_loader import img_loader
from font_manager import Text
from popup_bg_generator import popup_bg_generator
from screen_info import swidth, sheight
from settings import letter_to_key

tile_size = 32

card_tile_size = 2 * tile_size


class eqManager:
    def __init__(self, eq_list, eq_controls):
        text = Text()
        self.text = Text()

        self.mid_air_jump_trigger = False
        self.speed_dash_trigger = False

        self.eq_controls = eq_controls

        self.card_info = False
        self.card_info_type = 'blank'

        self.close_card_info_press = False
        self.card_info_press = False

        self.card_checked = False

        self.y = sheight - 2*tile_size
        self.x = 0
        self.eq_button_list = []

        self.eq_button_counter = 5

        self.card_info_popup = popup_bg_generator((180, 160))
        self.card_info_popup_text_surface = pygame.Surface((self.card_info_popup.get_width(),
                                                            self.card_info_popup.get_height()))
        self.card_info_popup_text_surface.set_colorkey((0, 0, 0))

        self.card_info_counter = 0

        self.card_return_counter = 10

        self.one_time_type_set = False

        self.level_count = 1

        self.joystick_counter = 0
        self.joystick_card_over_time = 5 * 60
        self.joystick_over_counter = 0

        self.card_sin_counter = 0

        self.eq_button_list_length = 0

        self.card_x = 0
        self.card_y = sheight - tile_size * 2

        self.card_vel_y = 0
        self.card_back_default_y = sheight - 18
        self.card_back_y = self.card_back_default_y
        self.card_jump_speed = 0.7
        self.animate_card_jump = False
        self.card_jump_animation_done = False
        self.card_jump_counter = 0

        self.new_card_final_y = sheight / 2 - 3 * tile_size / 2 + 5
        self.new_card_y_counter = sheight - self.new_card_final_y
        self.new_card_y = sheight - (self.new_card_final_y - self.new_card_y_counter)
        self.new_card_x = swidth / 2 - tile_size

        # card images --------------------------------------------------------------------------------------------------
        self.card_down_img = img_loader('data/images/card_down.PNG', card_tile_size, card_tile_size)
        self.card_back_img = img_loader('data/images/card_back.PNG', card_tile_size, card_tile_size)
        self.mid_air_jump_img = img_loader('data/images/card_mid-air_jump.PNG', card_tile_size, card_tile_size)
        self.speed_dash_img = img_loader('data/images/card_speed_dash.PNG', card_tile_size, card_tile_size)

        self.card_info_gap = 6
        self.card_info_y = 90
        self.uni_info_card_x = swidth / 2 - (self.card_down_img.get_width() +
                                             self.card_info_popup.get_width() + self.card_info_gap) / 2

        self.dark_surface = pygame.Surface((swidth, sheight))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(0)

        mid_air_jump_title = text.make_text(['MID-AIR JUMP'])
        mid_air_jump_info1 = text.make_text(['Jump without touching the ground.'])
        mid_air_jump_info2 = text.make_text(['You can only jump while falling.'])
        mid_air_jump_info3 = text.make_text(['Lasts for 3 jumps.'])

        speed_dash_title = text.make_text(['SPEED DASH'])
        speed_dash_info1 = text.make_text(['When activated, move to dash.'])
        speed_dash_info2 = text.make_text(['You can dash left or right.'])
        speed_dash_info3 = text.make_text(['Jump to stop.'])

        self.full_mid_air_jump_card = pygame.Surface((2 * tile_size, 3 * tile_size))
        self.full_mid_air_jump_card.set_colorkey((0, 0, 0))
        self.full_mid_air_jump_card.blit(pygame.transform.flip(self.mid_air_jump_img, False, True), (0, 17))
        self.full_mid_air_jump_card.blit(self.mid_air_jump_img, (0, 0))

        self.full_speed_dash_card = pygame.Surface((2 * tile_size, 3 * tile_size))
        self.full_speed_dash_card.set_colorkey((0, 0, 0))
        self.full_speed_dash_card.blit(pygame.transform.flip(self.speed_dash_img, False, True), (0, 17))
        self.full_speed_dash_card.blit(self.speed_dash_img, (0, 0))

        self.full_back_card = pygame.Surface((2 * tile_size, 3 * tile_size))
        self.full_back_card.set_colorkey((0, 0, 0))
        self.full_back_card.blit(pygame.transform.flip(self.card_back_img, False, True), (0, 17))
        self.full_back_card.blit(self.card_back_img, (0, 0))

        self.target_x = swidth / 2 - self.full_mid_air_jump_card.get_width() / 2
        self.target_y = sheight - (4.5 * tile_size) / 270 * sheight
        self.card_frame_movement_x = 0
        self.card_frame_movement_y = (self.target_y - (sheight - tile_size * 2)) / -9

        self.card_info_dict = {
            'mid-air_jump': self.full_mid_air_jump_card,
            'speed_dash': self.full_speed_dash_card
        }

        self.card_info_popup_text = {
            'mid-air_jump title': mid_air_jump_title,
            'mid-air_jump info1': mid_air_jump_info1,
            'mid-air_jump info2': mid_air_jump_info2,
            'mid-air_jump info3': mid_air_jump_info3,
            'speed_dash title': speed_dash_title,
            'speed_dash info1': speed_dash_info1,
            'speed_dash info2': speed_dash_info2,
            'speed_dash info3': speed_dash_info3,
        }

        # green light
        self.green_light = pygame.Surface((52, 10))
        self.green_light.fill((0, 212, 0))
        self.green_light.set_alpha(18)

        # mouse and keys animation images ------------------------------------------------------------------------------
        self.mouse0 = img_loader('data/images/mouse0.PNG', tile_size / 2, tile_size)
        self.mouse1 = img_loader('data/images/mouse1.PNG', tile_size / 2, tile_size)
        self.mouse2 = img_loader('data/images/mouse2.PNG', tile_size / 2, tile_size)
        self.mouse3 = img_loader('data/images/mouse3.PNG', tile_size / 2, tile_size)
        self.mouse_press = img_loader('data/images/mouse_press.PNG', tile_size / 2, tile_size)
        self.x_btn = img_loader('data/images/buttons/button_x.PNG', tile_size / 2, tile_size / 2)
        self.b_btn = img_loader('data/images/buttons/button_b.PNG', tile_size / 2, tile_size / 2)
        self.square_btn = img_loader('data/images/buttons/button_square.PNG', tile_size / 2, tile_size / 2)
        self.circle_btn = img_loader('data/images/buttons/button_circle.PNG', tile_size / 2, tile_size / 2)
        self.button_rb = img_loader('data/images/buttons/button_rb.PNG', tile_size / 2, tile_size / 2)
        self.button_rb_press = img_loader('data/images/buttons/button_rb_press.PNG', tile_size / 2, tile_size / 2)
        self.button_lb = img_loader('data/images/buttons/button_lb.PNG', tile_size / 2, tile_size / 2)
        self.button_lb_press = img_loader('data/images/buttons/button_lb_press.PNG', tile_size / 2, tile_size / 2)
        self.j_key = img_loader('data/images/buttons/key_j.PNG', tile_size / 2, tile_size / 2)
        self.j_key_press = img_loader('data/images/buttons/key_j_press.PNG', tile_size / 2, tile_size / 2)
        self.k_key = img_loader('data/images/buttons/key_k.PNG', tile_size / 2, tile_size / 2)
        self.k_key_press = img_loader('data/images/buttons/key_k_press.PNG', tile_size / 2, tile_size / 2)
        self.l_key = img_loader('data/images/buttons/key_l.PNG', tile_size / 2, tile_size / 2)
        self.l_key_press = img_loader('data/images/buttons/key_l_press.PNG', tile_size / 2, tile_size / 2)
        self.i_key = img_loader('data/images/buttons/key_i.PNG', tile_size / 2, tile_size / 2)
        self.i_key_press = img_loader('data/images/buttons/key_i_press.PNG', tile_size / 2, tile_size / 2)
        self.key_bg = img_loader('data/images/key_bg.PNG', 11, 14)
        self.key_bg_press = img_loader('data/images/key_bg_press.PNG', 11, 14)
        self.key_space = img_loader('data/images/key_space.PNG', 22, 14)
        self.key_space_press = img_loader('data/images/key_space_press.PNG', 22, 14)
        self.arrows = {
            'up': img_loader('data/images/arrows/arrow_up.PNG', 5, 9),
            'down': img_loader('data/images/arrows/arrow_down.PNG', 5, 9),
            'right': img_loader('data/images/arrows/arrow_right.PNG', 5, 9),
            'left': img_loader('data/images/arrows/arrow_left.PNG', 5, 9),
        }
        self.use_text_caps = text.make_text(['USE'])
        self.use_text = text.make_text(['use'])
        self.info_text_caps = text.make_text(['INFO'])
        self.info_text = text.make_text(['info'])

        controller_btn_width = self.x_btn.get_width()
        controller_btn_height = self.x_btn.get_height()

        or_txt = text.make_text(['or'])
        or_width = or_txt.get_width()

        self.two_btn_surface1 = pygame.Surface((controller_btn_width * 2 + or_width + 1, controller_btn_height))
        self.two_btn_surface2 = pygame.Surface((controller_btn_width * 2 + or_width + 1, controller_btn_height))
        self.two_btn_surface1.set_colorkey((0, 0, 0))
        self.two_btn_surface2.set_colorkey((0, 0, 0))

        self.two_btn_surface1.blit(self.x_btn, (0, 0))
        self.two_btn_surface1.blit(self.square_btn, (controller_btn_width + or_width, 0))
        self.two_btn_surface1.blit(or_txt, (controller_btn_width + 1, 4))
        self.two_btn_surface2.blit(self.b_btn, (0, 0))
        self.two_btn_surface2.blit(self.circle_btn, (controller_btn_width + or_width, 0))
        self.two_btn_surface2.blit(or_txt, (controller_btn_width + 1, 4))

        self.xbox_btns = {
            '1': self.x_btn,
            '2': self.b_btn,
        }

        self.ps4_btns = {
            '1': self.square_btn,
            '2': self.circle_btn,
        }

        self.mixed_controller_btns = {
            '1': self.two_btn_surface1,
            '2': self.two_btn_surface2,
        }

        self.controller_buttons = {
            'xbox': self.xbox_btns,
            'ps4': self.ps4_btns,
            'other': self.mixed_controller_btns
        }

        self.press_counter = 0

        white_arrow_up = img_loader('data/images/white_arrow.PNG', tile_size / 2, tile_size / 2)
        self.white_arrow_down = pygame.transform.flip(white_arrow_up, False, True)

        self.arrow_bob_counter = 0

        self.no_gem_text = text.make_text(['Collect gems to use cards'])
        self.no_gem_card_active_text = text.make_text(['You already have an active card'])
        self.card_message_counter = 0
        self.default_no_gem_counter = 100

        # creating buttons of elements in the equipped cards list ------------------------------------------------------
        for power in eq_list:
            if power == 'mid-air_jump':
                img = self.mid_air_jump_img

            elif power == 'speed_dash':
                img = self.speed_dash_img

            else:
                img = self.card_down_img

            x = self.x
            button = Button(x, self.y, self.card_down_img, img, img)
            btn_info = [button, power, x]
            self.eq_button_list.append(btn_info)

            self.eq_button_list_length = len(self.eq_button_list)

            self.x += 2.5*tile_size

    def create_card_buttons(self, eq_list):
        self.x = 0
        self.eq_button_list = []

        for power in eq_list:
            if power == 'mid-air_jump':
                img = self.mid_air_jump_img

            elif power == 'speed_dash':
                img = self.speed_dash_img

            else:
                img = self.card_down_img

            x = self.x
            button = Button(x, self.y, self.card_down_img, img, img)
            btn_info = [button, power, x]
            self.eq_button_list.append(btn_info)

            self.eq_button_list_length = len(self.eq_button_list)

            self.animate_card_jump = True
            self.card_vel_y = -7

            self.x += 2.5 * tile_size

    def blit_text_to_surf(self, surface, category):
        surface.fill((0, 0, 0))
        title = self.card_info_popup_text[f'{category} title']
        info1 = self.card_info_popup_text[f'{category} info1']
        info2 = self.card_info_popup_text[f'{category} info2']
        info3 = self.card_info_popup_text[f'{category} info3']
        surface.blit(title, (surface.get_width() / 2 - title.get_width() / 2, 6))
        surface.blit(info1, (surface.get_width() / 2 - info1.get_width() / 2, 22))
        surface.blit(info2, (surface.get_width() / 2 - info2.get_width() / 2, 38))
        surface.blit(info3, (surface.get_width() / 2 - info3.get_width() / 2, 53))

        return surface

    def prepare_card_animation(self, card_x, card_type):
        self.card_info = True
        self.card_x = card_x
        self.card_y = sheight - tile_size * 2
        self.card_frame_movement_x = (self.target_x - self.card_x) / 9
        self.card_info_press = False
        self.card_info_type = card_type
        self.card_info_counter = 0

    def card_jump_animation(self, fps_adjust, screen):
        self.card_vel_y += self.card_jump_speed * fps_adjust
        self.card_back_y += self.card_vel_y
        card_back_x = 0
        y_offset = 0
        if self.card_back_y > self.card_back_default_y:
            self.card_back_y = self.card_back_default_y
            self.card_jump_counter += 1
            if self.card_jump_counter == 1:
                self.card_vel_y = -5
            else:
                self.animate_card_jump = False
                self.card_jump_counter = 0
        for card in self.eq_button_list:
            screen.blit(self.card_back_img, (card_back_x, self.card_back_y))
            card_back_x += tile_size * 2.5

    def card_gem_animation(self, fps_adjust, screen):
        self.card_sin_counter += 1 * fps_adjust
        card_back_y = self.card_back_default_y - 5
        card_back_x = 0
        counter_offset = 0
        for card in self.eq_button_list:
            counter = self.card_sin_counter + counter_offset
            card_back_y += math.sin(1/13 * counter) * 3 * fps_adjust
            screen.blit(self.card_back_img, (card_back_x, card_back_y))
            card_back_x += tile_size * 2.5
            counter_offset = 30

    def card_green_light(self, screen):
        x = 6
        for card in self.eq_button_list:
            base_y = sheight - self.green_light.get_height()
            for y in range(self.green_light.get_height() + 1):
                screen.blit(self.green_light, (x, base_y + y))
                base_y += 1
            x += 2.5 * tile_size

    def new_card(self, card_type, screen, fps_adjust, counter):
        self.new_card_y_counter -= 15 * fps_adjust
        if self.new_card_y_counter < 0:
            self.new_card_y_counter = 0

        self.new_card_y = (self.new_card_final_y + self.new_card_y_counter)
        y_card_offset = math.cos(counter * 2) * 2

        screen.blit(self.card_info_dict[card_type], (self.new_card_x, self.new_card_y + y_card_offset))

# DRAWING AND HANDLING EQ BUTTONS ======================================================================================
    def draw_eq(self, screen, eq_list, mouse_adjustment, events, tutorial, fps_adjust, level_count,
                health, move, player_moved, gem_equipped, eq_controls, joysticks, controller_type,
                joystick_calibration, card_active):

        self.mid_air_jump_trigger = False
        self.speed_dash_trigger = False

        self.eq_controls = eq_controls

        self.press_counter += 1 * fps_adjust

        self.card_return_counter += 1 * fps_adjust

        self.joystick_over_counter -= 1 * fps_adjust

        if self.eq_button_list:
            card_num = self.eq_button_list_length - 1
        else:
            card_num = -1

        mousebuttondown = False
        mousebuttonup = False
        keydown = False
        mousebuttondown_right = False

        joystick_over0 = False
        joystick_over1 = False

        self.card_message_counter -= 1 * fps_adjust

        bumper_key_pressed = False
        joystick_info_press = False
        joystick_use_press = False
        joystick_jump_press = False
        joystick_action = False

        over = False
        local_over = False

        over1 = False
        over2 = False
        over3 = False
        over4 = False

        nuh_uh_sound_trigger = False

        if self.eq_controls['insta_card'] == 2:
            use_btn1 = self.eq_controls['configuration'][6]
            use_btn2 = self.eq_controls['configuration'][6]
            use_key1 = letter_to_key[self.eq_controls['binding'][6]]
            use_key2 = letter_to_key[self.eq_controls['binding'][6]]
        else:
            use_btn1 = self.eq_controls['configuration'][1]
            use_btn2 = self.eq_controls['configuration'][2]
            use_key1 = letter_to_key[self.eq_controls['binding'][3]]
            use_key2 = letter_to_key[self.eq_controls['binding'][4]]

        hat_value = [0, 0]

        if not gem_equipped:
            self.card_jump_animation_done = False

        if self.level_count != level_count:
            self.card_info = False
            self.card_return_counter = 10
            self.card_info_type = 'blank'
            self.level_count = level_count

        if not joystick_calibration:
            if self.eq_controls['cards'] == 'mouse':
                if events['mousebuttondown']:
                    event = events['mousebuttondown']
                    mousebuttondown = True
                    if event.button == 3:
                        mousebuttondown_right = True
                if events['mousebuttonup']:
                    mousebuttonup = True
            elif self.eq_controls['cards'] == 'keyboard':
                if events['keydown']:
                    event = events['keydown']
                    if self.card_info:
                        keydown = True
                    if event.key == letter_to_key[self.eq_controls['binding'][3]]:
                        bumper_key_pressed = True
                        if self.joystick_over_counter <= 0:
                            self.joystick_counter = 0
                        else:
                            self.joystick_counter -= 1
                            if self.joystick_counter < 0:
                                self.joystick_counter = card_num
                    elif event.key == letter_to_key[self.eq_controls['binding'][4]]:
                        bumper_key_pressed = True
                        if self.joystick_over_counter <= 0:
                            self.joystick_counter = card_num
                        else:
                            self.joystick_counter += 1
                            if self.joystick_counter > card_num:
                                self.joystick_counter = 0
                    elif event.key == letter_to_key[self.eq_controls['binding'][6]]:
                        joystick_use_press = True
                    elif event.key == letter_to_key[self.eq_controls['binding'][5]]:
                        if not self.card_info:
                            joystick_info_press = True
                    else:
                        keydown = True

            if events['joybuttondown']:
                event = events['joybuttondown']
                # buttons
                if event.button == self.eq_controls['configuration'][1]:
                    bumper_key_pressed = True
                    if self.joystick_over_counter <= 0:
                        self.joystick_counter = 0
                    else:
                        self.joystick_counter -= 1
                        if self.joystick_counter < 0:
                            self.joystick_counter = card_num
                if event.button == self.eq_controls['configuration'][2]:
                    bumper_key_pressed = True
                    if self.joystick_over_counter <= 0:
                        self.joystick_counter = card_num
                    else:
                        self.joystick_counter += 1
                        if self.joystick_counter > card_num:
                            self.joystick_counter = 0

                if event.button == self.eq_controls['configuration'][4]:
                    joystick_info_press = True
                if event.button == self.eq_controls['configuration'][6]:
                    joystick_use_press = True
                if event.button == self.eq_controls['configuration'][5]:
                    joystick_jump_press = True
                if (not joystick_info_press or self.card_info or joystick_jump_press) and not bumper_key_pressed:
                    joystick_action = True

            if events['joyhatdown']:
                # hat
                event = events['joyhatdown']
                if self.eq_controls['configuration'][0]:
                    if event.button == self.eq_controls['configuration'][0][0]:  # right
                        hat_value[0] = 1
                    if event.button == self.eq_controls['configuration'][0][1]:  # down
                        hat_value[1] = -1
                    if event.button == self.eq_controls['configuration'][0][2]:  # left
                        hat_value[0] = -1
                    if event.button == self.eq_controls['configuration'][0][3]:  # up
                        hat_value[1] = 1

            if events['joyaxismotion_x']:
                if abs(events['joyaxismotion_x'].value) > 0.8:
                    joystick_action = True
            if events['joyaxismotion_y']:
                if abs(events['joyaxismotion_y'].value) > 0.8:
                    joystick_action = True

        if joysticks and joysticks[0].get_numhats() > 0:
            hat_value = joysticks[0].get_hat(0)
            if hat_value[0] != 0:
                joystick_action = True

        if bumper_key_pressed:
            self.joystick_over_counter = self.joystick_card_over_time

        if self.joystick_over_counter > 0 and not self.card_info and move and \
                (self.eq_controls['cards'] == 'keyboard' or joysticks):
            if self.joystick_counter == 0:
                joystick_over0 = True
            if self.joystick_counter == 1:
                joystick_over1 = True

        if not move or self.card_info or self.eq_controls['cards'] == 'keyboard' or joysticks:
            mouse_adjustment = [0.0001, 0, 0]

        if self.card_info and mousebuttondown:
            self.close_card_info_press = True

        for button in self.eq_button_list:
            self.eq_button_counter += 1
            if button[1] == 'mid-air_jump':
                if self.card_info_type != 'mid-air_jump':
                    press, mid_air_jump_over = button[0].draw_button(screen, True, mouse_adjustment, events,
                                                                     joystick_over0, use_btn1,
                                                                     use_key1)
                    if mid_air_jump_over:
                        local_over = True
                else:
                    press = False
                if press and not self.card_info_press and gem_equipped and not card_active:
                    self.mid_air_jump_trigger = True
                    self.joystick_over_counter = 0
                if press and (not gem_equipped or card_active):
                    if self.card_message_counter < 70:
                        self.card_message_counter = self.default_no_gem_counter
                        nuh_uh_sound_trigger = True
                if local_over and not self.card_info:
                    if mousebuttondown_right:
                        self.card_info_press = True
                    if (mousebuttonup and self.card_info_press) or joystick_info_press:
                        self.card_info_type = 'mid-air_jump'
                        eqManager.prepare_card_animation(self, button[2], 'mid-air_jump')
                        self.card_info_popup_text_surface = \
                            eqManager.blit_text_to_surf(self, self.card_info_popup_text_surface, self.card_info_type)

            if button[1] == 'speed_dash':
                if self.card_info_type != 'speed_dash':
                    press, speed_dash_over = button[0].draw_button(screen, True, mouse_adjustment, events,
                                                                   joystick_over1, use_btn2,
                                                                   use_key2)
                    if speed_dash_over:
                        local_over = True
                else:
                    press = False
                if press and not self.card_info_press and gem_equipped and not card_active:
                    self.speed_dash_trigger = True
                    self.joystick_over_counter = 0
                if press and (not gem_equipped or card_active):
                    if self.card_message_counter < 70:
                        self.card_message_counter = self.default_no_gem_counter
                        nuh_uh_sound_trigger = True
                if local_over and not self.card_info:
                    if mousebuttondown_right:
                        self.card_info_press = True
                    if (mousebuttonup and self.card_info_press) or joystick_info_press:
                        self.card_info_type = 'speed_dash'
                        eqManager.prepare_card_animation(self, button[2], 'speed_dash')
                        self.card_info_popup_text_surface = \
                            eqManager.blit_text_to_surf(self, self.card_info_popup_text_surface, self.card_info_type)

            if local_over:
                if self.eq_button_counter == 1:
                    over1 = True
                if self.eq_button_counter == 2:
                    over2 = True
                if self.eq_button_counter >= 3:
                    over3 = True
                    self.eq_button_counter = 0

        if over1 or over2 or over3:
            over = True
            self.card_checked = True

        if joystick_action or keydown:
            self.joystick_over_counter = 0

        if gem_equipped and not self.animate_card_jump and not self.card_jump_animation_done:
            self.animate_card_jump = True
            self.card_jump_animation_done = True
            self.card_vel_y = -7
            self.card_checked = False

        if over and joystick_use_press and not gem_equipped:
            if self.card_message_counter < 70:
                self.card_message_counter = self.default_no_gem_counter
                nuh_uh_sound_trigger = True

        if self.card_message_counter > 0:
            if self.card_message_counter > 90:
                offset_x = random.choice([2, 0, -2])
                offset_y = random.choice([2, 0, -2])
            else:
                offset_x = 0
                offset_y = 0
            if card_active:
                txt = self.no_gem_card_active_text
            else:
                txt = self.no_gem_text
            screen.blit(txt, (swidth / 2 - txt.get_width() / 2 + offset_x,
                                           sheight / 2 - txt.get_height() / 2 - 70 + offset_y))

        if self.animate_card_jump:
            eqManager.card_jump_animation(self, fps_adjust, screen)
        elif gem_equipped and self.joystick_over_counter <= 0 and not local_over:
            eqManager.card_gem_animation(self, fps_adjust, screen)

        if gem_equipped and not self.card_info:
            eqManager.card_green_light(self, screen)

        # tutorial on how to use cards ---------------------------------------------------------------------------------
        if self.eq_button_list:
            gap = 3

            if over:
                if self.press_counter >= 40:
                    mouse_img = self.mouse_press
                    if self.eq_controls['binding'][6] != 'space':
                        key1_img = self.key_bg_press.copy()
                    else:
                        key1_img = self.key_space_press.copy()
                    if self.eq_controls['binding'][5] != 'space':
                        key2_img = self.key_bg_press.copy()
                    else:
                        key2_img = self.key_space_press.copy()
                    if self.press_counter >= 50:
                        self.press_counter = 0
                    y = 4
                else:
                    mouse_img = self.mouse3
                    if self.eq_controls['binding'][6] != 'space':
                        key1_img = self.key_bg.copy()
                    else:
                        key1_img = self.key_space.copy()
                    if self.eq_controls['binding'][5] != 'space':
                        key2_img = self.key_bg.copy()
                    else:
                        key2_img = self.key_space.copy()
                    y = 2

                cont_img = self.controller_buttons[controller_type]['1']
                cont_img2 = self.controller_buttons[controller_type]['2']

                mouse_img2 = pygame.transform.flip(mouse_img, True, False)

                center_width = swidth / 2
                center_height = sheight / 3 - tile_size / 2 + tile_size / 4

                if joysticks:
                    img1 = cont_img
                    img2 = cont_img2
                    img_y = center_height
                else:
                    if self.eq_controls['binding'][6] != 'space':
                        if self.eq_controls['binding'][6] in ['up', 'down', 'right', 'left']:
                            letter1 = self.arrows[self.eq_controls['binding'][6]]
                        else:
                            letter1 = self.text.make_text([self.eq_controls['binding'][6]])
                        key1_img.blit(letter1, (3, y))
                    if self.eq_controls['binding'][5] != 'space':
                        if self.eq_controls['binding'][5] in ['up', 'down', 'right', 'left']:
                            letter2 = self.arrows[self.eq_controls['binding'][5]]
                        else:
                            letter2 = self.text.make_text([self.eq_controls['binding'][5]])
                        key2_img.blit(letter2, (3, y))
                    if self.eq_controls['cards'] == 'keyboard':
                        img_y = center_height
                        img1 = key1_img
                        img2 = key2_img
                    else:
                        img_y = center_height - tile_size / 3
                        img1 = mouse_img
                        img2 = mouse_img2

                if gem_equipped:
                    total_tutorial_width = img1.get_width() + img2.get_width() + self.use_text_caps.get_width() + \
                                           self.info_text_caps.get_width() + 2 + gap * 4
                    tutorial_x = center_width - total_tutorial_width / 2

                    screen.blit(img1, (tutorial_x, img_y))
                    tutorial_x += (img1.get_width() + gap)
                    screen.blit(self.use_text_caps, (tutorial_x, center_height + 5))
                    tutorial_x += (self.use_text_caps.get_width() + gap)
                    pygame.draw.line(screen, (255, 255, 255), (tutorial_x, center_height - 2),
                                     (tutorial_x, center_height + tile_size / 2 + 2))
                    tutorial_x += (1 + gap)
                    screen.blit(img2, (tutorial_x, img_y))
                    tutorial_x += (img2.get_width() + gap)
                    screen.blit(self.info_text_caps, (tutorial_x, center_height + 5))
                else:
                    total_tutorial_width = img2.get_width() + self.info_text_caps.get_width() + gap
                    tutorial_x = center_width - total_tutorial_width / 2

                    screen.blit(img2, (tutorial_x, img_y))
                    tutorial_x += (img2.get_width() + gap)
                    screen.blit(self.info_text_caps, (tutorial_x, center_height + 5))

            elif (not self.card_checked or (gem_equipped and not self.card_checked)) and player_moved and tutorial:
                if not joysticks and self.eq_controls['cards'] == 'mouse':
                    if self.press_counter >= 60:
                        mouse_img = self.mouse0
                        self.press_counter = 0
                    elif self.press_counter >= 40:
                        mouse_img = self.mouse0
                    elif self.press_counter >= 30:
                        mouse_img = self.mouse3
                    elif self.press_counter >= 20:
                        mouse_img = self.mouse2
                    elif self.press_counter >= 10:
                        mouse_img = self.mouse1
                    else:
                        mouse_img = self.mouse0
                    if health > 0:
                        screen.blit(mouse_img, (swidth / 2 - tile_size / 4, sheight / 3 - tile_size / 2))
                else:
                    if self.eq_controls['cards'] == 'keyboard' and not joysticks:
                        if self.eq_controls['binding'][3] != 'space':
                            btn1 = self.key_bg.copy()
                            btn_press1 = self.key_bg_press.copy()
                            if self.eq_controls['binding'][3] in ['up', 'down', 'right', 'left']:
                                letter = self.arrows[self.eq_controls['binding'][3]]
                            else:
                                letter = self.text.make_text([self.eq_controls['binding'][3]])
                            btn1.blit(letter, (3, 2))
                            btn_press1.blit(letter, (3, 4))
                        else:
                            btn1 = self.key_space
                            btn_press1 = self.key_space_press
                        if self.eq_controls['binding'][4] != 'space':
                            btn2 = self.key_bg.copy()
                            btn_press2 = self.key_bg_press.copy()
                            if self.eq_controls['binding'][4] in ['up', 'down', 'right', 'left']:
                                letter = self.arrows[self.eq_controls['binding'][4]]
                            else:
                                letter = self.text.make_text([self.eq_controls['binding'][4]])
                            btn2.blit(letter, (3, 2))
                            btn_press2.blit(letter, (3, 4))
                        else:
                            btn2 = self.key_space
                            btn_press2 = self.key_space_press
                    else:
                        btn1 = self.button_rb
                        btn2 = self.button_lb
                        btn_press1 = self.button_rb_press
                        btn_press2 = self.button_lb_press
                    if self.press_counter > 90:
                        btn2 = btn_press2
                        if self.press_counter > 100:
                            self.press_counter = 0
                    elif 50 > self.press_counter > 40:
                        btn1 = btn_press1
                    if health > 0:
                        x = swidth / 2
                        y = sheight / 3 - tile_size / 4
                        gap = 2
                        screen.blit(btn1, (x - gap - btn1.get_width(), y))
                        screen.blit(btn2, (x + gap, y))

                self.arrow_bob_counter += 1 * fps_adjust
                y_arrow_offset = math.sin((1 / 13) * self.arrow_bob_counter) * 3
                for card in self.eq_button_list:
                    arrow_x = card[2] + (tile_size - tile_size / 4)
                    arrow_y = sheight - 42
                    if not self.card_info and not self.card_checked:
                        screen.blit(self.white_arrow_down, (arrow_x, arrow_y + y_arrow_offset))

        # CARD INFO ----------------------------------------------------------------------------------------------------
        if self.card_info:
            self.card_info_counter += 0.04*fps_adjust
            popup = self.card_info_popup
            text = self.card_info_popup_text_surface

            if 0.25 > self.card_info_counter > 0:
                scaling = self.card_info_counter
                popup = pygame.transform.scale(self.card_info_popup, (self.card_info_popup.get_width() * scaling * 4,
                                                                      self.card_info_popup.get_height() * scaling * 4))
                text = pygame.transform.scale(self.card_info_popup_text_surface,
                                              (self.card_info_popup_text_surface.get_width() * scaling * 4,
                                               self.card_info_popup_text_surface.get_height() * scaling * 4))

            if self.card_info_counter > 0.25:
                popup = self.card_info_popup
                text = self.card_info_popup_text_surface

            screen.blit(popup,
                        (swidth / 2 - popup.get_width() / 2, sheight / 2 - popup.get_height() / 2))
            screen.blit(text,
                        (swidth / 2 - text.get_width() / 2, sheight / 2 - text.get_height() / 2))

            if 0.25 > self.card_info_counter > 0:
                self.card_x += self.card_frame_movement_x
                self.card_y -= self.card_frame_movement_y
                screen.blit(self.card_info_dict[self.card_info_type], (self.card_x, self.card_y))
            else:
                y_card_offset = math.cos(self.card_info_counter * 2) * 2
                screen.blit(self.card_info_dict[self.card_info_type],
                            (self.target_x, self.target_y + y_card_offset))

            if (mousebuttonup and self.close_card_info_press) or keydown or joystick_action:
                self.card_info = False
                self.joystick_over_counter = self.joystick_card_over_time
                self.close_card_info_press = False
                self.card_return_counter = 0
                self.press_counter = 0
                self.card_x = self.target_x
                self.card_y = self.target_y

        if not self.card_info and self.card_return_counter < 10:
            screen.blit(self.card_info_dict[self.card_info_type], (self.card_x, self.card_y))
            self.card_x -= self.card_frame_movement_x
            self.card_y += self.card_frame_movement_y
            self.one_time_type_set = True

        if self.card_return_counter >= 10 and self.one_time_type_set:
            self.card_info_type = 'blank'
            self.one_time_type_set = False

        return eq_list, self.mid_air_jump_trigger, self.speed_dash_trigger, over, nuh_uh_sound_trigger
