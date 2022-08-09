import pygame
from image_loader import img_loader
from font_manager import Text
from button import Button

tile_size = 32
button_size = tile_size * 0.75

sheight = 264
swidth = 352


class SettingsMenu:
    def __init__(self, controls):
        # image loading ------------------------------------------------------------------------------------------------
        self.menu_background = img_loader('data/images/menu_background.PNG', swidth, sheight)

        self.left_button = img_loader('data/images/button_left.PNG', button_size, button_size)
        self.left_button_press = img_loader('data/images/button_left_press.PNG', button_size, button_size)
        self.left_button_down = img_loader('data/images/button_left_down.PNG', button_size, button_size)

        self.right_button = pygame.transform.flip(self.left_button, True, False)
        self.right_button_press = pygame.transform.flip(self.left_button_press, True, False)
        self.right_button_down = pygame.transform.flip(self.left_button_down, True, False)

        self.right_button_grey = img_loader('data/images/button_right_grey.PNG', button_size, button_size)
        self.left_button_grey = pygame.transform.flip(self.right_button_grey, True, False)

        self.menu_button = img_loader('data/images/button_menu.PNG', tile_size * 1.5, tile_size * 0.75)
        self.menu_button_press = img_loader('data/images/button_menu_press.PNG', tile_size * 1.5, tile_size * 0.75)
        self.menu_button_down = img_loader('data/images/button_menu_down.PNG', tile_size * 1.5, tile_size * 0.75)

        # variables ----------------------------------------------------------------------------------------------------
        self.controls = controls

        # major surfaces -----------------------------------------------------------------------------------------------
        self.control_screen = pygame.Surface((swidth, 200))
        self.visual_screen = pygame.Surface((swidth, 200))
        self.sound_screen = pygame.Surface((swidth, 200))

        # dictionaries --------------------------------------------------------------------------------
        self.nums_to_btns = {
            'left1': pygame.K_a,
            'right1': pygame.K_d,
            'left2': pygame.K_LEFT,
            'right2': pygame.K_RIGHT,
            'jump1': pygame.K_SPACE,
            'jump2': pygame.K_w,
            'jump3': pygame.K_UP,
            'shockwave1': pygame.K_z,
            'shockwave2': pygame.K_r,
            'shockwave3': pygame.K_f,
            'interact1': pygame.K_x,
            'interact2': pygame.K_e
        }

        self.resolutions = {
            '1': (900, 660),
            '2': (1260, 924)
        }

        # text generation ----------------------------------------------------------------------------------------------
        self.controls_txt = Text().make_text(['CONTROL'])
        self.visual_txt = Text().make_text(['VISUAL'])
        self.sound_txt = Text().make_text(['SOUND'])
        self.walking_txt = Text().make_text(['walking:'])
        self.jumping_txt = Text().make_text(['jumping:'])
        self.shockwave_txt = Text().make_text(['shockwave:'])
        self.interactions_txt = Text().make_text(['interactions:'])
        self.move_conf1 = Text().make_text(['A and D keys'])
        self.move_conf2 = Text().make_text(['arrow keys'])
        self.jump_conf1 = Text().make_text(['space bar'])
        self.jump_conf2 = Text().make_text(['W key'])
        self.jump_conf3 = Text().make_text(['up key'])
        self.interact_conf1 = Text().make_text(['X key'])
        self.interact_conf2 = Text().make_text(['E key'])
        self.shockwave_conf1 = Text().make_text(['Z key'])
        self.shockwave_conf2 = Text().make_text(['R key'])
        self.shockwave_conf3 = Text().make_text(['F key'])

        # counters -----------------------------------------------------------------------------------------------------
        self.walk_counter = 1
        self.jump_counter = 1
        self.shockwave_counter = 1
        self.interaction_counter = 1

        # button positional variables and other ------------------------------------------------------------------------
        gap = 30
        self.gap = 30
        button_start_y = 33
        interbutton_space = 120

        self.center = 150

        self.walking_y = button_start_y + gap
        self.jumping_y = button_start_y + gap * 2
        self.shockwave_y = button_start_y + gap * 3
        self.interactions_y = button_start_y + gap * 4

        self.left_btn_x = self.center + 10
        self.right_btn_x = self.center + interbutton_space

        section_btn_select = pygame.Surface((118, 20))
        section_btn_select.blit(self.menu_background, (0, 0))

        section_btn_dark = pygame.Surface((118, 20))
        section_btn_dark.blit(self.menu_background, (0, 0))

        self.draw_control_button = False
        self.draw_visual_button = True
        self.draw_sound_button = True

        self.control_button_select = pygame.Surface((117, 20))
        self.sound_button_select = pygame.Surface((117, 20))
        self.visual_button_select = pygame.Surface((118, 20))

        self.control_button_dark = pygame.Surface((117, 20))
        self.control_button_dark.set_alpha(180)
        self.sound_button_dark = pygame.Surface((117, 20))
        self.sound_button_dark.set_alpha(180)
        self.visual_button_dark = pygame.Surface((118, 20))
        self.visual_button_dark.set_alpha(180)

        self.control_button_select.blit(section_btn_select, (0, 0))
        self.control_button_select.blit(self.controls_txt, (swidth / 6 - self.controls_txt.get_width() / 2, 7))

        self.sound_button_select.blit(section_btn_select, (0, 0))
        self.sound_button_select.blit(self.sound_txt, (swidth / 6 - self.sound_txt.get_width() / 2, 7))

        self.visual_button_select.blit(section_btn_select, (0, 0))
        self.visual_button_select.blit(self.visual_txt, (swidth / 6 - self.visual_txt.get_width() / 2, 7))

        self.control_button_dark.blit(section_btn_dark, (0, 0))
        self.control_button_dark.blit(self.controls_txt, (swidth / 6 - self.controls_txt.get_width() / 2, 7))

        self.sound_button_dark.blit(section_btn_dark, (0, 0))
        self.sound_button_dark.blit(self.sound_txt, (swidth / 6 - self.sound_txt.get_width() / 2, 7))

        self.visual_button_dark.blit(section_btn_dark, (0, 0))
        self.visual_button_dark.blit(self.visual_txt, (swidth / 6 - self.visual_txt.get_width() / 2, 7))

        self.control_button_over = pygame.Surface((117, 20))
        self.control_button_over.blit(self.control_button_dark, (0, 0))
        self.control_button_over.blit(self.controls_txt, (swidth / 6 - self.controls_txt.get_width() / 2, 7))

        self.visual_button_over = pygame.Surface((118, 20))
        self.visual_button_over.blit(self.visual_button_dark, (0, 0))
        self.visual_button_over.blit(self.visual_txt, (swidth / 6 - self.visual_txt.get_width() / 2, 7))

        self.sound_button_over = pygame.Surface((117, 20))
        self.sound_button_over.blit(self.sound_button_dark, (0, 0))
        self.sound_button_over.blit(self.sound_txt, (swidth / 6 - self.sound_txt.get_width() / 2, 7))

        # initiating buttons -------------------------------------------------------------------------------------------
        self.walking_btn_left = Button(self.center + 10, button_start_y + gap,
                                       self.left_button, self.left_button_press, self.left_button_down)
        self.walking_btn_right = Button(self.center + interbutton_space, button_start_y + gap,
                                        self.right_button, self.right_button_press, self.right_button_down)
        self.jumping_btn_left = Button(self.center + 10, button_start_y + gap * 2,
                                       self.left_button, self.left_button_press, self.left_button_down)
        self.jumping_btn_right = Button(self.center + interbutton_space, button_start_y + gap * 2,
                                        self.right_button, self.right_button_press, self.right_button_down)
        self.shockwave_btn_left = Button(self.center + 10, button_start_y + gap * 3,
                                         self.left_button, self.left_button_press, self.left_button_down)
        self.shockwave_btn_right = Button(self.center + interbutton_space, button_start_y + gap * 3,
                                          self.right_button, self.right_button_press, self.right_button_down)
        self.interaction_btn_left = Button(self.center + 10, button_start_y + gap * 4,
                                           self.left_button, self.left_button_press, self.left_button_down)
        self.interaction_btn_right = Button(self.center + interbutton_space, button_start_y + gap * 4,
                                            self.right_button, self.right_button_press, self.right_button_down)

        self.menu_btn = Button(swidth / 2 - self.menu_button.get_width() / 2, 220,
                               self.menu_button, self.menu_button_press, self.menu_button_down)

        self.control_btn = Button(0, 0, self.control_button_dark, self.control_button_over,
                                  self.control_button_dark)
        self.sound_btn = Button(117 + 118, 0, self.sound_button_dark, self.sound_button_over, self.sound_button_dark)
        self.visual_btn = Button(117, 0, self.visual_button_dark, self.visual_button_over,
                                 self.visual_button_dark)

        # --------------------------------------------------------------------------------------------------------------
    def draw_settings_menu(self, settings_screen, mouse_adjustment, events):
        settings_screen.fill((0, 0, 0))
        settings_screen.blit(self.menu_background, (0, 0))

        self.control_screen.blit(self.menu_background, (0, 20))
        self.sound_screen.blit(self.menu_background, (0, 20))
        self.visual_screen.blit(self.menu_background, (0, 20))

        walking_left_press = False
        walking_right_press = False
        jumping_left_press = False
        jumping_right_press = False
        shockwave_left_press = False
        shockwave_right_press = False
        interactions_left_press = False
        interactions_right_press = False

        final_over1 = False
        final_over2 = False

        over = False
        over1 = False
        over2 = False
        over3 = False
        over4 = False

        menu_press = False

        control_btn_trigger = False
        visual_btn_trigger = False
        sound_btn_trigger = False

        # drawing and updating the menu/back button ----------------------------------------------------------------
        menu_press, over = self.menu_btn.draw_button(settings_screen, False, mouse_adjustment, events)

        # CONTROL SETTINGS SCREEN ======================================================================================
        self.control_screen.blit(self.walking_txt, (self.center - 10 - self.walking_txt.get_width(), 40 + self.gap))
        self.control_screen.blit(self.jumping_txt, (self.center - 10 - self.jumping_txt.get_width(), 40 + self.gap * 2))
        self.control_screen.blit(self.shockwave_txt,
                             (self.center - 10 - self.shockwave_txt.get_width(), 40 + self.gap * 3))
        self.control_screen.blit(self.interactions_txt,
                             (self.center - 10 - self.interactions_txt.get_width(), 40 + self.gap * 4))

        # updating the text showing the player's current controls --------------------------------------------------
        if self.walk_counter == 1:
            walk_text = self.move_conf1
        else:
            walk_text = self.move_conf2

        if self.jump_counter == 1:
            jump_text = self.jump_conf1
        elif self.jump_counter == 2:
            jump_text = self.jump_conf2
        else:
            jump_text = self.jump_conf3

        if self.shockwave_counter == 1:
            shockwave_text = self.shockwave_conf1
        elif self.shockwave_counter == 2:
            shockwave_text = self.shockwave_conf2
        else:
            shockwave_text = self.shockwave_conf3

        if self.interaction_counter == 1:
            interaction_text = self.interact_conf1
        else:
            interaction_text = self.interact_conf2

        button_text_center = self.center + 65

        self.control_screen.blit(walk_text, (button_text_center - walk_text.get_width() / 2 + button_size / 2,
                                             self.walking_y + 7))
        self.control_screen.blit(jump_text, (button_text_center - jump_text.get_width() / 2 + button_size / 2,
                                             self.jumping_y + 7))
        self.control_screen.blit(shockwave_text,
                                 (button_text_center - shockwave_text.get_width() / 2 + button_size / 2,
                                  self.shockwave_y + 7))
        self.control_screen.blit(interaction_text,
                                 (button_text_center - interaction_text.get_width() / 2 + button_size / 2,
                                  self.interactions_y + 7))

        # managing the buttons to switch between control options ---------------------------------------------------
        if self.walk_counter > 1:
            walking_left_press, over1 = self.walking_btn_left.draw_button(self.control_screen,
                                                                          False, mouse_adjustment, events)
        else:
            self.control_screen.blit(self.left_button_grey, (self.left_btn_x, self.walking_y))

        if self.walk_counter < 2:
            walking_right_press, over1 = self.walking_btn_right.draw_button(self.control_screen,
                                                                            False, mouse_adjustment, events)
        else:
            self.control_screen.blit(self.right_button_grey, (self.right_btn_x, self.walking_y))

        if self.jump_counter > 1:
            jumping_left_press, over2 = self.jumping_btn_left.draw_button(self.control_screen,
                                                                          False, mouse_adjustment, events)
        else:
            self.control_screen.blit(self.left_button_grey, (self.left_btn_x, self.jumping_y))

        if self.jump_counter < 3:
            jumping_right_press, over2 = self.jumping_btn_right.draw_button(self.control_screen,
                                                                        False, mouse_adjustment, events)
        else:
            self.control_screen.blit(self.right_button_grey, (self.right_btn_x, self.jumping_y))

        if self.shockwave_counter > 1:
            shockwave_left_press, over3 = self.shockwave_btn_left.draw_button(self.control_screen,
                                                                              False, mouse_adjustment, events)
        else:
            self.control_screen.blit(self.left_button_grey, (self.left_btn_x, self.shockwave_y))

        if self.shockwave_counter < 3:
            shockwave_right_press, over3 = self.shockwave_btn_right.draw_button(self.control_screen,
                                                                                False, mouse_adjustment, events)
        else:
            self.control_screen.blit(self.right_button_grey, (self.right_btn_x, self.shockwave_y))

        if self.interaction_counter > 1:
            interactions_left_press, over4 = self.interaction_btn_left.draw_button(self.control_screen, False,
                                                                                   mouse_adjustment, events)
        else:
            self.control_screen.blit(self.left_button_grey, (self.left_btn_x, self.interactions_y))

        if self.interaction_counter < 2:
            interactions_right_press, over4 = self.interaction_btn_right.draw_button(self.control_screen,
                                                                                     False, mouse_adjustment,
                                                                                     events)
        else:
            self.control_screen.blit(self.right_button_grey, (self.right_btn_x, self.interactions_y))

        # adjusting control counters if buttons are pressed --------------------------------------------------------
        if walking_left_press and self.walk_counter > 1:
            self.walk_counter -= 1
        if walking_right_press and self.walk_counter < 2:
            self.walk_counter += 1

        if jumping_left_press and self.jump_counter > 1:
            self.jump_counter -= 1
        if jumping_right_press and self.jump_counter < 3:
            self.jump_counter += 1

        if shockwave_left_press and self.shockwave_counter > 1:
            self.shockwave_counter -= 1
        if shockwave_right_press and self.shockwave_counter < 3:
            self.shockwave_counter += 1

        if interactions_left_press and self.interaction_counter > 1:
            self.interaction_counter -= 1
        if interactions_right_press and self.interaction_counter < 2:
            self.interaction_counter += 1

        # updating the controls dictionary -------------------------------------------------------------------------
        if menu_press:
            self.controls['left'] = self.nums_to_btns[f'left{self.walk_counter}']
            self.controls['right'] = self.nums_to_btns[f'right{self.walk_counter}']
            self.controls['jump'] = self.nums_to_btns[f'jump{self.jump_counter}']
            self.controls['interact'] = self.nums_to_btns[f'interact{self.interaction_counter}']
            self.controls['shockwave'] = self.nums_to_btns[f'shockwave{self.shockwave_counter}']

        if over or over1 or over3:
            final_over1 = True
        if over2 or over4:
            final_over2 = True

        if not self.draw_control_button:
            settings_screen.blit(self.control_screen, (0, 0))
        if not self.draw_visual_button:
            settings_screen.blit(self.visual_screen, (0, 0))
        if not self.draw_sound_button:
            settings_screen.blit(self.sound_screen, (0, 0))

        # managing the section buttons ---------------------------------------------------------------------------------
        if self.draw_control_button:
            control_btn_trigger, not_over = self.control_btn.draw_button(settings_screen,
                                                                         False, mouse_adjustment, events)
        else:
            settings_screen.blit(self.control_button_select, (0, 0))
        if self.draw_visual_button:
            visual_btn_trigger, not_over = self.visual_btn.draw_button(settings_screen, False, mouse_adjustment,
                                                                       events)
        else:
            settings_screen.blit(self.visual_button_select, (117, 0))
        if self.draw_sound_button:
            sound_btn_trigger, not_over = self.sound_btn.draw_button(settings_screen, False, mouse_adjustment,
                                                                     events)
        else:
            settings_screen.blit(self.sound_button_select, (117 + 118, 0))

        if control_btn_trigger:
            self.draw_control_button = False
            self.draw_visual_button = True
            self.draw_sound_button = True
        if visual_btn_trigger:
            self.draw_control_button = True
            self.draw_visual_button = False
            self.draw_sound_button = True
        if sound_btn_trigger:
            self.draw_control_button = True
            self.draw_visual_button = True
            self.draw_sound_button = False

        return menu_press, self.controls, final_over1, final_over2

