import pygame
from image_loader import img_loader
from font_manager import Text
from button import Button

tile_size = 32
button_size = tile_size * 0.75

swidth = 360
sheight = 264


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

        # numbers to buttons dictionary --------------------------------------------------------------------------------
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

        # text generation ----------------------------------------------------------------------------------------------
        self.controls_txt = Text().make_text(['CONTROLS'])
        self.visual_txt = Text().make_text(['VISUAL'])
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

        # button positional variables ----------------------------------------------------------------------------------
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

        # --------------------------------------------------------------------------------------------------------------
    def draw_settings_menu(self, settings_screen, mouse_adjustment, events):
        settings_screen.blit(self.menu_background, (0, 20))

        settings_screen.blit(self.controls_txt, (swidth / 2 - self.controls_txt.get_width() / 2, 40))

        settings_screen.blit(self.walking_txt, (self.center - 10 - self.walking_txt.get_width(), 40 + self.gap))
        settings_screen.blit(self.jumping_txt, (self.center - 10 - self.jumping_txt.get_width(), 40 + self.gap * 2))
        settings_screen.blit(self.shockwave_txt, (self.center - 10 - self.shockwave_txt.get_width(), 40 + self.gap * 3))
        settings_screen.blit(self.interactions_txt,
                             (self.center - 10 - self.interactions_txt.get_width(), 40 + self.gap * 4))

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

        # updating the text showing the player's current controls ------------------------------------------------------
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

        settings_screen.blit(walk_text, (button_text_center - walk_text.get_width() / 2 + button_size / 2,
                                         self.walking_y + 7))
        settings_screen.blit(jump_text, (button_text_center - jump_text.get_width() / 2 + button_size / 2,
                                         self.jumping_y + 7))
        settings_screen.blit(shockwave_text, (button_text_center - shockwave_text.get_width() / 2 + button_size / 2,
                                              self.shockwave_y + 7))
        settings_screen.blit(interaction_text, (button_text_center - interaction_text.get_width() / 2 + button_size / 2,
                                              self.interactions_y + 7))

        # managing the buttons to switch between control options -------------------------------------------------------
        if self.walk_counter > 1:
            walking_left_press, over1 = self.walking_btn_left.draw_button(settings_screen,
                                                                          False, mouse_adjustment, events)
        else:
            settings_screen.blit(self.left_button_grey, (self.left_btn_x, self.walking_y))

        if self.walk_counter < 2:
            walking_right_press, over1 = self.walking_btn_right.draw_button(settings_screen,
                                                                            False, mouse_adjustment, events)
        else:
            settings_screen.blit(self.right_button_grey, (self.right_btn_x, self.walking_y))

        if self.jump_counter > 1:
            jumping_left_press, over2 = self.jumping_btn_left.draw_button(settings_screen,
                                                                          False, mouse_adjustment, events)
        else:
            settings_screen.blit(self.left_button_grey, (self.left_btn_x, self.jumping_y))

        if self.jump_counter < 3:
            jumping_right_press, over2 = self.jumping_btn_right.draw_button(settings_screen,
                                                                        False, mouse_adjustment, events)
        else:
            settings_screen.blit(self.right_button_grey, (self.right_btn_x, self.jumping_y))

        if self.shockwave_counter > 1:
            shockwave_left_press, over3 = self.shockwave_btn_left.draw_button(settings_screen,
                                                                              False, mouse_adjustment, events)
        else:
            settings_screen.blit(self.left_button_grey, (self.left_btn_x, self.shockwave_y))

        if self.shockwave_counter < 3:
            shockwave_right_press, over3 = self.shockwave_btn_right.draw_button(settings_screen,
                                                                                False, mouse_adjustment, events)
        else:
            settings_screen.blit(self.right_button_grey, (self.right_btn_x, self.shockwave_y))

        if self.interaction_counter > 1:
            interactions_left_press, over4 = self.interaction_btn_left.draw_button(settings_screen, False,
                                                                                   mouse_adjustment, events)
        else:
            settings_screen.blit(self.left_button_grey, (self.left_btn_x, self.interactions_y))

        if self.interaction_counter < 2:
            interactions_right_press, over4 = self.interaction_btn_right.draw_button(settings_screen,
                                                                                     False, mouse_adjustment, events)
        else:
            settings_screen.blit(self.right_button_grey, (self.right_btn_x, self.interactions_y))

        # adjusting control counters if buttons are pressed ------------------------------------------------------------
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

        # drawing and updating the menu/back button --------------------------------------------------------------------
        menu_press, over = self.menu_btn.draw_button(settings_screen, False, mouse_adjustment, events)

        # updating the controls dictionary -----------------------------------------------------------------------------
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

        return menu_press, self.controls, final_over1, final_over2

