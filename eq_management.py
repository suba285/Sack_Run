import pygame
from button import Button
from image_loader import img_loader
from font_manager import Text

tile_size = 32

sheight = 264
swidth = 352

card_tile_size = 2 * tile_size


class eqManager:
    def __init__(self, eq_list, controls):
        self.jump_boost_trigger = False
        self.regeneration_trigger = False
        self.no_gravity_trigger = False
        self.no_harm_trigger = False
        self.shockwave_trigger = False

        self.controls = controls

        self.y = 264 - 2*tile_size
        num_cards = len(eq_list)
        self.x = 0
        self.eq_button_list = []

        self.eq_button_counter = 0

        self.completed_txt = Text().make_text(["congrats, you've completed the tutorial"])

        # card images --------------------------------------------------------------------------------------------------
        self.card_down_img = img_loader('data/images/card_down.PNG', card_tile_size, card_tile_size)
        self.jump_boost_img1 = img_loader('data/images/card_jump_boost.PNG', card_tile_size, card_tile_size)
        self.regeneration_img1 = img_loader('data/images/card_regeneration.PNG', card_tile_size, card_tile_size)
        self.no_grav_img1 = img_loader('data/images/card_no_gravity.PNG', card_tile_size, card_tile_size)
        self.no_harm_img1 = img_loader('data/images/card_no_harm.PNG', card_tile_size, card_tile_size)
        self.shockwave_img1 = img_loader('data/images/card_shockwave.PNG', card_tile_size, card_tile_size)

        # mouse and keys animation images ------------------------------------------------------------------------------
        self.mouse0 = img_loader('data/images/mouse0.PNG', tile_size / 2, tile_size)
        self.mouse1 = img_loader('data/images/mouse1.PNG', tile_size / 2, tile_size)
        self.mouse2 = img_loader('data/images/mouse2.PNG', tile_size / 2, tile_size)
        self.mouse3 = img_loader('data/images/mouse3.PNG', tile_size / 2, tile_size)
        self.mouse_press = img_loader('data/images/mouse_press.PNG', tile_size / 2, tile_size)
        self.key_q = img_loader('data/images/key_q.PNG', tile_size / 2, tile_size / 2)
        self.key_q_press = img_loader('data/images/key_q_press.PNG', tile_size / 2, tile_size / 2)
        self.use_text = img_loader('data/images/text_use.PNG', tile_size / 2, tile_size / 2)
        self.bin_text = img_loader('data/images/text_bin.PNG', tile_size / 2, tile_size / 2)

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
            btn_info = [button, power]
            self.eq_button_list.append(btn_info)

            self.x += 2.5*tile_size

# DRAWING AND HANDLING EQ BUTTONS ======================================================================================
    def draw_eq(self, screen, eq_list, mouse_adjustement, events, power_list, tutorial, fps_adjust, level_count,
                blit_card_instructions):

        self.jump_boost_trigger = False
        self.regeneration_trigger = False
        self.no_gravity_trigger = False
        self.no_harm_trigger = False
        self.shockwave_trigger = False

        self.press_counter += 1 * fps_adjust

        paper_sound_trigger = False

        over = False
        local_over = False
        over1 = False
        over2 = False
        over3 = False
        over4 = False

        key = pygame.key.get_pressed()

        for button in self.eq_button_list:
            self.eq_button_counter += 1
            local_over = False
            if button[1] == 'jump boost':
                press, local_over = button[0].draw_button(screen, True, mouse_adjustement, events)
                if press:
                    self.jump_boost_trigger = True
                    eq_list.remove('jump boost')
                    self.eq_button_list.remove(button)
                if key[self.controls['bin_card']] and local_over and 'jump boost' in eq_list:
                    eq_list.remove('jump boost')
                    self.eq_button_list.remove(button)
                    paper_sound_trigger = True
            if button[1] == 'regeneration':
                press, local_over = button[0].draw_button(screen, True, mouse_adjustement, events)
                if press:
                    self.regeneration_trigger = True
                    eq_list.remove('regeneration')
                    self.eq_button_list.remove(button)
                if key[self.controls['bin_card']] and local_over and 'regeneration' in eq_list:
                    eq_list.remove('regeneration')
                    self.eq_button_list.remove(button)
                    paper_sound_trigger = True
            if button[1] == 'no gravity':
                press, local_over = button[0].draw_button(screen, True, mouse_adjustement, events)
                if press:
                    self.no_gravity_trigger = True
                    eq_list.remove('no gravity')
                    self.eq_button_list.remove(button)
                if key[self.controls['bin_card']] and local_over and 'no gravity' in eq_list:
                    eq_list.remove('no gravity')
                    self.eq_button_list.remove(button)
                    paper_sound_trigger = True
            if button[1] == 'no harm':
                press, local_over = button[0].draw_button(screen, True, mouse_adjustement, events)
                if press:
                    self.no_harm_trigger = True
                    eq_list.remove('no harm')
                    self.eq_button_list.remove(button)
                if key[self.controls['bin_card']] and local_over and 'no harm' in eq_list:
                    eq_list.remove('no harm')
                    self.eq_button_list.remove(button)
                    paper_sound_trigger = True
            if button[1] == 'shockwave+':
                press, local_over = button[0].draw_button(screen, True, mouse_adjustement, events)
                if press:
                    self.shockwave_trigger = True
                    eq_list.remove('shockwave+')
                    self.eq_button_list.remove(button)
                if key[self.controls['bin_card']] and local_over and 'shockwave+' in eq_list:
                    eq_list.remove('shockwave+')
                    self.eq_button_list.remove(button)
                    paper_sound_trigger = True

            if local_over:
                print(self.eq_button_counter)
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
        if tutorial and self.eq_button_list and level_count != 3 and blit_card_instructions:
            gap = 3
            img = self.mouse3
            if over:
                if self.press_counter >= 30:
                    img = self.mouse_press
                    key_img = self.key_q_press
                    if self.press_counter >= 40:
                        self.press_counter = 0
                else:
                    img = self.mouse3
                    key_img = self.key_q

                center_width = swidth / 2
                center_height = sheight / 3 - tile_size / 2 + tile_size / 4

                screen.blit(img, (center_width - tile_size - gap * 2, center_height - tile_size / 3))
                screen.blit(self.use_text, (center_width - tile_size / 2 - gap, center_height))
                pygame.draw.line(screen, (255, 255, 255), (center_width, center_height - 2),
                                 (center_width, center_height + tile_size / 2 + 2))
                screen.blit(key_img, (center_width + gap + 1, center_height))
                screen.blit(self.bin_text, (center_width + tile_size / 2 + gap * 2 + 3, center_height))

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

                screen.blit(img, (swidth / 2 - tile_size / 4, sheight / 3 - tile_size / 2))

        if tutorial and level_count == 3:
            screen.blit(self.completed_txt, (swidth / 2 - self.completed_txt.get_width() / 2, sheight / 3))

        return eq_list, self.jump_boost_trigger, self.regeneration_trigger, self.no_gravity_trigger,\
               self.no_harm_trigger, self.shockwave_trigger, over, power_list, paper_sound_trigger
