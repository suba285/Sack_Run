import pygame
from button import Button
from image_loader import img_loader
from font_manager import Text
from popup_bg_generator import popup_bg_generator

tile_size = 32

sheight = 264
swidth = 352

card_tile_size = 2 * tile_size


class eqManager:
    def __init__(self, eq_list, controls, walk_counter):
        self.mid_air_jump_trigger = False
        self.speed_dash_trigger = False

        self.controls = controls
        self.card_delete_counter = walk_counter

        self.card_info = False
        self.card_info_type = 'blank'

        self.close_card_info_press = False
        self.card_info_press = False

        self.card_checked = False

        self.y = 264 - 2*tile_size
        self.x = 0
        self.eq_button_list = []

        self.eq_button_counter = 5

        self.completed_txt = Text().make_text(["congrats, you've completed the tutorial"])

        self.card_info_popup = popup_bg_generator((180, 160))
        self.card_info_popup_text_surface = pygame.Surface((self.card_info_popup.get_width(),
                                                            self.card_info_popup.get_height()))
        self.card_info_popup_text_surface.set_colorkey((0, 0, 0))

        self.card_info_counter = 0

        self.card_return_counter = 10

        self.one_time_type_set = False

        self.level_count = 1

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

        mid_air_jump_title = Text().make_text(['MID-AIR JUMP'])
        mid_air_jump_info1 = Text().make_text(['Jump without touching the ground.'])
        mid_air_jump_info2 = Text().make_text(['You can only jump while falling.'])
        mid_air_jump_info3 = Text().make_text(['Duration: 7.5s'])

        speed_dash_title = Text().make_text(['SPEED DASH'])
        speed_dash_info1 = Text().make_text(['When activated, move to dash.'])
        speed_dash_info2 = Text().make_text(['Press space to stop.'])
        speed_dash_info3 = Text().make_text(['You take twice as much damage.'])

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
        self.target_y = sheight - 4.5 * tile_size
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

        # mouse and keys animation images ------------------------------------------------------------------------------
        self.mouse0 = img_loader('data/images/mouse0.PNG', tile_size / 2, tile_size)
        self.mouse1 = img_loader('data/images/mouse1.PNG', tile_size / 2, tile_size)
        self.mouse2 = img_loader('data/images/mouse2.PNG', tile_size / 2, tile_size)
        self.mouse3 = img_loader('data/images/mouse3.PNG', tile_size / 2, tile_size)
        self.mouse_press = img_loader('data/images/mouse_press.PNG', tile_size / 2, tile_size)
        self.key_q = img_loader('data/images/key_q.PNG', tile_size / 2, tile_size / 2)
        self.key_q_press = img_loader('data/images/key_q_press.PNG', tile_size / 2, tile_size / 2)
        self.key_full_stop = img_loader('data/images/key_full_stop.PNG', tile_size / 2, tile_size / 2)
        self.key_full_stop_press = img_loader('data/images/key_full_stop_press.PNG', tile_size / 2, tile_size / 2)
        self.use_text = Text().make_text(['USE'])
        self.info_text = Text().make_text(['INFO'])

        self.press_counter = 0

        self.white_arrow_up = img_loader('data/images/white_arrow.PNG', tile_size / 2, tile_size / 2)
        self.white_arrow_down = pygame.transform.flip(self.white_arrow_up, False, True)

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

    def new_card(self, card_type, screen, fps_adjust):
        self.new_card_y_counter -= 15 * fps_adjust
        if self.new_card_y_counter < 0:
            self.new_card_y_counter = 0

        self.new_card_y = (self.new_card_final_y + self.new_card_y_counter)

        screen.blit(self.card_info_dict[card_type], (self.new_card_x, self.new_card_y))

# DRAWING AND HANDLING EQ BUTTONS ======================================================================================
    def draw_eq(self, screen, eq_list, mouse_adjustment, events, power_list, tutorial, fps_adjust, level_count,
                health, move, player_moved, gem_equipped):

        self.mid_air_jump_trigger = False
        self.speed_dash_trigger = False

        self.press_counter += 1 * fps_adjust

        self.card_return_counter += 1 * fps_adjust

        mousebuttondown = False
        mousebuttonup = False
        keydown = False
        mousebuttondown_right = False

        over = False
        local_over = False

        over1 = False
        over2 = False
        over3 = False
        over4 = False

        if not gem_equipped:
            self.card_jump_animation_done = False

        if self.level_count != level_count:
            self.card_info = False
            self.card_return_counter = 10
            self.card_info_type = 'blank'
            self.level_count = level_count

        key = pygame.key.get_pressed()

        for event in events:
            if event.type == pygame.KEYDOWN:
                keydown = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousebuttondown = True
                if event.button == 3:
                    mousebuttondown_right = True
            if event.type == pygame.MOUSEBUTTONUP:
                mousebuttonup = True

        if not move or self.card_info:
            mouse_adjustment = 0.001

        if self.card_info and mousebuttondown:
            self.close_card_info_press = True

        for button in self.eq_button_list:
            self.eq_button_counter += 1
            local_over = False
            if button[1] == 'mid-air_jump':
                if self.card_info_type != 'mid-air_jump':
                    press, local_over = button[0].draw_button(screen, True, mouse_adjustment, events)
                else:
                    press = False
                    local_over = False
                if press and not self.card_info_press and gem_equipped:
                    self.mid_air_jump_trigger = True
                if local_over and not self.card_info:
                    if mousebuttondown_right:
                        self.card_info_press = True
                    if mousebuttonup and self.card_info_press:
                        self.card_info_type = 'mid-air_jump'
                        eqManager.prepare_card_animation(self, button[2], 'mid-air_jump')
                        self.card_info_popup_text_surface = \
                            eqManager.blit_text_to_surf(self, self.card_info_popup_text_surface, self.card_info_type)

            if button[1] == 'speed_dash':
                if self.card_info_type != 'speed_dash':
                    press, local_over = button[0].draw_button(screen, True, mouse_adjustment, events)
                else:
                    press = False
                    local_over = False
                if press and not self.card_info_press and gem_equipped:
                    self.speed_dash_trigger = True
                if local_over and not self.card_info:
                    if mousebuttondown_right:
                        self.card_info_press = True
                    if mousebuttonup and self.card_info_press:
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

        if gem_equipped and not self.animate_card_jump and not self.card_jump_animation_done:
            self.animate_card_jump = True
            self.card_jump_animation_done = True
            self.card_vel_y = -7

        if self.animate_card_jump:
            eqManager.card_jump_animation(self, fps_adjust, screen)

        # tutorial on how to use cards
        if tutorial and self.eq_button_list and level_count != 3 and player_moved:
            gap = 3
            img = self.mouse3
            if self.card_delete_counter == 1:
                delete_key_images = (self.key_q, self.key_q_press)
            else:
                delete_key_images = (self.key_full_stop, self.key_full_stop_press)

            if over:
                if self.press_counter >= 30:
                    img = self.mouse_press
                    key_img = delete_key_images[1]
                    if self.press_counter >= 40:
                        self.press_counter = 0
                else:
                    img = self.mouse3
                    key_img = delete_key_images[0]

                center_width = swidth / 2
                center_height = sheight / 3 - tile_size / 2 + tile_size / 4

                total_tutorial_width = img.get_width() * 2 + self.use_text.get_width() +\
                                        self.info_text.get_width() + 2 + gap * 4
                tutorial_x = center_width - total_tutorial_width / 2

                screen.blit(img, (tutorial_x, center_height - tile_size / 3))
                tutorial_x += (img.get_width() + gap)
                screen.blit(self.use_text, (tutorial_x, center_height + 5))
                tutorial_x += (self.use_text.get_width() + gap)
                pygame.draw.line(screen, (255, 255, 255), (tutorial_x, center_height - 2),
                                 (tutorial_x, center_height + tile_size / 2 + 2))
                tutorial_x += (1 + gap)
                screen.blit(pygame.transform.flip(img, True, False), (tutorial_x, center_height - tile_size / 3))
                tutorial_x += (img.get_width() + gap)
                screen.blit(self.info_text, (tutorial_x, center_height + 5))

            elif not self.card_checked:
                if self.press_counter >= 60:
                    img = self.mouse0
                    self.press_counter = 0
                elif self.press_counter >= 40:
                    img = self.mouse0
                elif self.press_counter >= 30:
                    img = self.mouse3
                elif self.press_counter >= 20:
                    img = self.mouse2
                elif self.press_counter >= 10:
                    img = self.mouse1
                else:
                    img = self.mouse0
                if health > 1:
                    screen.blit(img, (swidth / 2 - tile_size / 4, sheight / 3 - tile_size / 2))

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
                screen.blit(self.card_info_dict[self.card_info_type],
                            (self.target_x, self.target_y))

            if (mousebuttonup and self.close_card_info_press) or keydown:
                self.card_info = False
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

        return eq_list, self.mid_air_jump_trigger, self.speed_dash_trigger, over, power_list
