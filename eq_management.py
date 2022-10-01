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
        self.jump_boost_trigger = False
        self.regeneration_trigger = False
        self.no_gravity_trigger = False
        self.no_harm_trigger = False
        self.shockwave_trigger = False

        self.controls = controls
        self.card_delete_counter = walk_counter

        self.card_info = False
        self.card_info_type = 'blank'

        self.close_card_info_press = False
        self.card_info_press = False

        self.y = 264 - 2*tile_size
        num_cards = len(eq_list)
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

        # card images --------------------------------------------------------------------------------------------------
        self.card_down_img = img_loader('data/images/card_down.PNG', card_tile_size, card_tile_size)
        self.jump_boost_img1 = img_loader('data/images/card_jump_boost.PNG', card_tile_size, card_tile_size)
        self.regeneration_img1 = img_loader('data/images/card_regeneration.PNG', card_tile_size, card_tile_size)
        self.no_grav_img1 = img_loader('data/images/card_no_gravity.PNG', card_tile_size, card_tile_size)
        self.no_harm_img1 = img_loader('data/images/card_no_harm.PNG', card_tile_size, card_tile_size)
        self.shockwave_img1 = img_loader('data/images/card_shockwave.PNG', card_tile_size, card_tile_size)

        self.card_info_gap = 6
        self.card_info_y = 90
        self.uni_info_card_x = swidth / 2 - (self.card_down_img.get_width() +
                                             self.card_info_popup.get_width() + self.card_info_gap) / 2

        self.dark_surface = pygame.Surface((swidth, sheight))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(0)

        jump_boost_title = Text().make_text(['JUMP BOOST'])
        jump_boost_class = Text().make_text(['rare'])
        jump_boost_description = Text().make_text(['Reach new heights'])
        jump_boost_duration = Text().make_text(['Duration: 7.5s'])

        no_harm_title = Text().make_text(['NO HARM'])
        no_harm_class = Text().make_text(['common'])
        no_harm_description = Text().make_text(['Pass tricky levels with ease'])
        no_harm_duration = Text().make_text(['Duration: 5s'])

        regeneration_title = Text().make_text(['REGENERATION'])
        regeneration_class = Text().make_text(['common'])
        regeneration_description = Text().make_text(['Fully restore player health'])
        regeneration_duration = Text().make_text(['Duration: -'])

        no_gravity_title = Text().make_text(['NO GRAVITY'])
        no_gravity_class = Text().make_text(['very rare'])
        no_gravity_description = Text().make_text(['Literally walk on air'])
        no_gravity_duration = Text().make_text(['Duration: 3s'])

        shockwave_title = Text().make_text(['SHOCKWAVE +'])
        shockwave_class = Text().make_text(['rare'])
        shockwave_description = Text().make_text(['Fully restore shockwave limit'])
        shockwave_duration = Text().make_text(['Duration: -'])

        self.full_jump_boost_card = pygame.Surface((2 * tile_size, 3 * tile_size))
        self.full_jump_boost_card.set_colorkey((0, 0, 0))
        self.full_jump_boost_card.blit(pygame.transform.flip(self.jump_boost_img1, False, True), (0, 16))
        self.full_jump_boost_card.blit(self.jump_boost_img1, (0, 0))

        self.full_no_harm_card = pygame.Surface((2 * tile_size, 3 * tile_size))
        self.full_no_harm_card.set_colorkey((0, 0, 0))
        self.full_no_harm_card.blit(pygame.transform.flip(self.no_harm_img1, False, True), (0, 16))
        self.full_no_harm_card.blit(self.no_harm_img1, (0, 0))

        self.full_no_gravity_card = pygame.Surface((2 * tile_size, 3 * tile_size))
        self.full_no_gravity_card.set_colorkey((0, 0, 0))
        self.full_no_gravity_card.blit(pygame.transform.flip(self.no_grav_img1, False, True), (0, 16))
        self.full_no_gravity_card.blit(self.no_grav_img1, (0, 0))

        self.full_regeneration_card = pygame.Surface((2 * tile_size, 3 * tile_size))
        self.full_regeneration_card.set_colorkey((0, 0, 0))
        self.full_regeneration_card.blit(pygame.transform.flip(self.regeneration_img1, False, True), (0, 16))
        self.full_regeneration_card.blit(self.regeneration_img1, (0, 0))

        self.full_shockwave_card = pygame.Surface((2 * tile_size, 3 * tile_size))
        self.full_shockwave_card.set_colorkey((0, 0, 0))
        self.full_shockwave_card.blit(pygame.transform.flip(self.jump_boost_img1, False, True), (0, 16))
        self.full_shockwave_card.blit(self.shockwave_img1, (0, 0))

        self.target_x = swidth / 2 - self.full_no_harm_card.get_width() / 2
        self.target_y = sheight - 4.5 * tile_size
        self.card_frame_movement_x = 0
        self.card_frame_movement_y = (self.target_y - (sheight - tile_size * 2)) / -9

        self.card_info_dict = {
            'jump boost': self.full_jump_boost_card,
            'no harm': self.full_no_harm_card,
            'regeneration': self.full_regeneration_card,
            'no gravity': self.full_no_gravity_card,
            'shockwave+': self.full_shockwave_card
        }

        self.card_info_popup_text = {
            'jump boost title': jump_boost_title,
            'jump boost class': jump_boost_class,
            'jump boost description': jump_boost_description,
            'jump boost duration': jump_boost_duration,
            'no harm title': no_harm_title,
            'no harm class': no_harm_class,
            'no harm description': no_harm_description,
            'no harm duration': no_harm_duration,
            'regeneration title': regeneration_title,
            'regeneration class': regeneration_class,
            'regeneration description': regeneration_description,
            'regeneration duration': regeneration_duration,
            'no gravity title': no_gravity_title,
            'no gravity class': no_gravity_class,
            'no gravity description': no_gravity_description,
            'no gravity duration': no_gravity_duration,
            'shockwave+ title': shockwave_title,
            'shockwave+ class': shockwave_class,
            'shockwave+ description': shockwave_description,
            'shockwave+ duration': shockwave_duration,
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
        self.use_text = img_loader('data/images/text_use.PNG', tile_size / 2, tile_size / 2)
        self.bin_text = img_loader('data/images/text_bin.PNG', tile_size / 2, tile_size / 2)
        self.use_text = Text().make_text(['USE'])
        self.bin_text = Text().make_text(['BIN'])
        self.info_text = Text().make_text(['INFO'])

        self.press_counter = 0

        self.white_arrow_up = img_loader('data/images/white_arrow.PNG', tile_size / 2, tile_size / 2)
        self.white_arrow_down = pygame.transform.flip(self.white_arrow_up, False, True)

        # creating buttons of elements in the equipped cards list ------------------------------------------------------
        for power in eq_list:
            if power == 'jump boost':
                img = self.jump_boost_img1

            elif power == 'regeneration':
                img = self.regeneration_img1

            elif power == 'no gravity':
                img = self.no_grav_img1

            elif power == 'no harm':
                img = self.no_harm_img1

            elif power == 'shockwave+':
                img = self.shockwave_img1

            else:
                img = self.card_down_img

            x = self.x
            button = Button(x, self.y, self.card_down_img, img, img)
            btn_info = [button, power, x]
            self.eq_button_list.append(btn_info)

            self.x += 2.5*tile_size

    def create_card_buttons(self, eq_list, reset):
        self.x = 0
        self.eq_button_list = []

        for power in eq_list:
            if power == 'jump boost':
                img = self.jump_boost_img1

            elif power == 'regeneration':
                img = self.regeneration_img1

            elif power == 'no gravity':
                img = self.no_grav_img1

            elif power == 'no harm':
                img = self.no_harm_img1

            elif power == 'shockwave+':
                img = self.shockwave_img1

            else:
                img = self.card_down_img

            x = self.x
            button = Button(x, self.y, self.card_down_img, img, img)
            btn_info = [button, power, x]
            self.eq_button_list.append(btn_info)

            self.x += 2.5*tile_size

    def blit_text_to_surf(self, surface, category):
        surface.fill((0, 0, 0))
        title = self.card_info_popup_text[f'{category} title']
        card_class = self.card_info_popup_text[f'{category} class']
        description = self.card_info_popup_text[f'{category} description']
        duration = self.card_info_popup_text[f'{category} duration']
        surface.blit(title, (surface.get_width() / 2 - title.get_width() / 2, 6))
        surface.blit(description, (surface.get_width() / 2 - description.get_width() / 2, 22))
        surface.blit(card_class, (surface.get_width() / 2 - card_class.get_width() / 2, 38))
        surface.blit(duration, (surface.get_width() / 2 - duration.get_width() / 2, 53))

        return surface

    def prepare_card_animation(self, card_x, card_type):
        self.card_info = True
        self.card_x = card_x
        self.card_y = sheight - tile_size * 2
        self.card_frame_movement_x = (self.target_x - self.card_x) / 9
        self.card_info_press = False
        self.card_info_type = card_type
        self.card_info_counter = 0

# DRAWING AND HANDLING EQ BUTTONS ======================================================================================
    def draw_eq(self, screen, eq_list, mouse_adjustment, events, power_list, tutorial, fps_adjust, level_count,
                blit_card_instructions, health, move):

        self.jump_boost_trigger = False
        self.regeneration_trigger = False
        self.no_gravity_trigger = False
        self.no_harm_trigger = False
        self.shockwave_trigger = False

        self.press_counter += 1 * fps_adjust

        self.card_return_counter += 1 * fps_adjust

        paper_sound_trigger = False

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
            if button[1] == 'jump boost':
                if self.card_info_type != 'jump boost':
                    press, local_over = button[0].draw_button(screen, True, mouse_adjustment, events)
                else:
                    press = False
                    local_over = False
                if press:
                    self.jump_boost_trigger = True
                    eq_list.remove('jump boost')
                    self.eq_button_list.remove(button)
                if local_over and not self.card_info:
                    if mousebuttondown_right:
                        self.card_info_press = True
                    if mousebuttonup and self.card_info_press:
                        self.card_info_type = 'jump boost'
                        eqManager.prepare_card_animation(self, button[2], 'jump boost')
                        self.card_info_popup_text_surface = \
                            eqManager.blit_text_to_surf(self, self.card_info_popup_text_surface, self.card_info_type)
                if key[self.controls['bin_card']] and local_over and 'jump boost' in eq_list:
                    eq_list.remove('jump boost')
                    self.eq_button_list.remove(button)
                    paper_sound_trigger = True
            if button[1] == 'regeneration':
                if self.card_info_type != 'regeneration':
                    press, local_over = button[0].draw_button(screen, True, mouse_adjustment, events)
                else:
                    press = False
                    local_over = False
                if press and not self.card_info_press:
                    self.regeneration_trigger = True
                    eq_list.remove('regeneration')
                    self.eq_button_list.remove(button)
                if local_over and not self.card_info:
                    if mousebuttondown_right:
                        self.card_info_press = True
                    if mousebuttonup and self.card_info_press:
                        self.card_info_type = 'regeneration'
                        eqManager.prepare_card_animation(self, button[2], 'regeneration')
                        self.card_info_popup_text_surface = \
                            eqManager.blit_text_to_surf(self, self.card_info_popup_text_surface, self.card_info_type)
                if key[self.controls['bin_card']] and local_over and 'regeneration' in eq_list:
                    eq_list.remove('regeneration')
                    self.eq_button_list.remove(button)
                    paper_sound_trigger = True
            if button[1] == 'no gravity':
                if self.card_info_type != 'no gravity':
                    press, local_over = button[0].draw_button(screen, True, mouse_adjustment, events)
                else:
                    press = False
                    local_over = False
                if press and not self.card_info_press:
                    self.no_gravity_trigger = True
                    eq_list.remove('no gravity')
                    self.eq_button_list.remove(button)
                if local_over and not self.card_info:
                    if mousebuttondown_right:
                        self.card_info_press = True
                    if mousebuttonup and self.card_info_press:
                        self.card_info_type = 'no gravity'
                        eqManager.prepare_card_animation(self, button[2], 'no gravity')
                        self.card_info_popup_text_surface = \
                            eqManager.blit_text_to_surf(self, self.card_info_popup_text_surface, self.card_info_type)
                if key[self.controls['bin_card']] and local_over and 'no gravity' in eq_list:
                    eq_list.remove('no gravity')
                    self.eq_button_list.remove(button)
                    paper_sound_trigger = True
            if button[1] == 'no harm':
                if self.card_info_type != 'no harm':
                    press, local_over = button[0].draw_button(screen, True, mouse_adjustment, events)
                else:
                    press = False
                    local_over = False
                if press:
                    self.no_harm_trigger = True
                    eq_list.remove('no harm')
                    self.eq_button_list.remove(button)
                if local_over and not self.card_info:
                    if mousebuttondown_right:
                        self.card_info_press = True
                    if mousebuttonup and self.card_info_press:
                        self.card_info_type = 'no harm'
                        eqManager.prepare_card_animation(self, button[2], 'no harm')
                        self.card_info_popup_text_surface = \
                            eqManager.blit_text_to_surf(self, self.card_info_popup_text_surface, self.card_info_type)
                if key[self.controls['bin_card']] and local_over and 'no harm' in eq_list:
                    eq_list.remove('no harm')
                    self.eq_button_list.remove(button)
                    paper_sound_trigger = True
            if button[1] == 'shockwave+':
                if self.card_info_type != 'shockwave+':
                    press, local_over = button[0].draw_button(screen, True, mouse_adjustment, events)
                else:
                    press = False
                    local_over = False
                if press and not self.card_info_press:
                    self.shockwave_trigger = True
                    eq_list.remove('shockwave+')
                    self.eq_button_list.remove(button)
                if local_over and not self.card_info:
                    if mousebuttondown_right:
                        self.card_info_press = True
                    if mousebuttonup and self.card_info_press:
                        self.card_info_type = 'shockwave+'
                        eqManager.prepare_card_animation(self, button[2], 'shockwave+')
                        self.card_info_popup_text_surface = \
                            eqManager.blit_text_to_surf(self, self.card_info_popup_text_surface,
                                                        self.card_info_type)
                if key[self.controls['bin_card']] and local_over and 'shockwave+' in eq_list:
                    eq_list.remove('shockwave+')
                    self.eq_button_list.remove(button)
                    paper_sound_trigger = True

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

        # tutorial on how to use cards
        if tutorial and self.eq_button_list and level_count != 3 and blit_card_instructions and not self.card_info and\
            self.card_return_counter >= 10:
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

                total_tutorial_width = img.get_width() * 2 + self.use_text.get_width() + self.bin_text.get_width() +\
                                       self.info_text.get_width() + 2 + key_img.get_width() + gap * 9
                tutorial_x = center_width - total_tutorial_width / 2

                screen.blit(img, (tutorial_x, center_height - tile_size / 3))
                tutorial_x += (img.get_width() + gap)
                screen.blit(self.use_text, (tutorial_x, center_height + 5))
                tutorial_x += (self.use_text.get_width() + gap)
                pygame.draw.line(screen, (255, 255, 255), (tutorial_x, center_height - 2),
                                 (tutorial_x, center_height + tile_size / 2 + 2))
                tutorial_x += (1 + gap*2)
                screen.blit(key_img, (tutorial_x, center_height))
                tutorial_x += (key_img.get_width() + gap*2)
                screen.blit(self.bin_text, (tutorial_x, center_height + 5))
                tutorial_x += (self.bin_text.get_width() + gap)
                pygame.draw.line(screen, (255, 255, 255), (tutorial_x, center_height - 2),
                                 (tutorial_x, center_height + tile_size / 2 + 2))
                tutorial_x += (1 + gap)
                screen.blit(pygame.transform.flip(img, True, False), (tutorial_x, center_height - tile_size / 3))
                tutorial_x += (img.get_width() + gap)
                screen.blit(self.info_text, (tutorial_x, center_height + 5))

            else:
                if self.press_counter >= 30:
                    screen.blit(self.white_arrow_down, (tile_size - tile_size/4, sheight - tile_size * 1.5))
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

        return eq_list, self.jump_boost_trigger, self.regeneration_trigger, self.no_gravity_trigger,\
               self.no_harm_trigger, self.shockwave_trigger, over, power_list, paper_sound_trigger
