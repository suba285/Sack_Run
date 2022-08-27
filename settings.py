import pygame
from image_loader import img_loader
from font_manager import Text
from button import Button
from button import inactive_button

tile_size = 32
button_size = tile_size * 0.75

sheight = 264
swidth = 352

# this file is a total mess, you have been warned


class SettingsMenu:
    def __init__(self, controls, settings_counters, resolutions, recommended_res_counter):
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

        self.keyboard_base = img_loader('data/images/keyboard_base.PNG', tile_size * 3, tile_size)
        keyboard_interact1 = img_loader('data/images/keyboard_highlights/keyboard_interact1.PNG',
                                        tile_size * 3, tile_size)
        keyboard_interact2 = img_loader('data/images/keyboard_highlights/keyboard_interact2.PNG',
                                        tile_size * 3, tile_size)
        keyboard_interact3 = img_loader('data/images/keyboard_highlights/keyboard_interact3.PNG',
                                        tile_size * 3, tile_size)
        keyboard_jump1 = img_loader('data/images/keyboard_highlights/keyboard_jump1.PNG',
                                    tile_size * 3, tile_size)
        keyboard_jump2 = img_loader('data/images/keyboard_highlights/keyboard_jump2.PNG',
                                    tile_size * 3, tile_size)
        keyboard_jump3 = img_loader('data/images/keyboard_highlights/keyboard_jump3.PNG',
                                    tile_size * 3, tile_size)
        keyboard_shockwave1 = img_loader('data/images/keyboard_highlights/keyboard_shockwave1.PNG',
                                         tile_size * 3, tile_size)
        keyboard_shockwave2 = img_loader('data/images/keyboard_highlights/keyboard_shockwave2.PNG',
                                         tile_size * 3, tile_size)
        keyboard_shockwave3 = img_loader('data/images/keyboard_highlights/keyboard_shockwave3.PNG',
                                         tile_size * 3, tile_size)
        keyboard_walk1 = img_loader('data/images/keyboard_highlights/keyboard_walk1.PNG',
                                    tile_size * 3, tile_size)
        keyboard_walk2 = img_loader('data/images/keyboard_highlights/keyboard_walk2.PNG',
                                    tile_size * 3, tile_size)

        self.keyboard_overlays = {
            'interact1': keyboard_interact1,
            'interact2': keyboard_interact2,
            'interact3': keyboard_interact3,
            'shockwave1': keyboard_shockwave1,
            'shockwave2': keyboard_shockwave2,
            'shockwave3': keyboard_shockwave3,
            'jump1': keyboard_jump1,
            'jump2': keyboard_jump2,
            'jump3': keyboard_jump3,
            'walk1': keyboard_walk1,
            'walk2': keyboard_walk2
        }

        # variables ----------------------------------------------------------------------------------------------------
        self.controls = controls
        self.recommended_res_counter = recommended_res_counter
        self.keyboard_highlight_counter = 60
        self.keyboard_highlight_off = False
        self.keyboard_bg_alpha = 100

        # major surfaces -----------------------------------------------------------------------------------------------
        self.control_screen = pygame.Surface((swidth, 220))
        self.visual_screen = pygame.Surface((swidth, 220))
        self.sound_screen = pygame.Surface((swidth, 220))

        # dictionaries -------------------------------------------------------------------------------------------------
        self.nums_to_btns = {
            'left1': pygame.K_a,
            'right1': pygame.K_d,
            'left2': pygame.K_LEFT,
            'right2': pygame.K_RIGHT,
            'jump1': pygame.K_SPACE,
            'jump2': pygame.K_w,
            'jump3': pygame.K_UP,
            'shockwave1': pygame.K_z,
            'shockwave2': pygame.K_f,
            'shockwave3': pygame.K_RSHIFT,
            'interact1': pygame.K_x,
            'interact2': pygame.K_e,
            'interact3': pygame.K_SLASH,
            'delete_card1': pygame.K_q,
            'delete_card2': pygame.K_PERIOD
        }

        self.resolutions = resolutions

        # text generation ----------------------------------------------------------------------------------------------

        self.controls_txt = Text().make_text(['CONTROL'])
        self.visual_txt = Text().make_text(['VISUAL'])
        self.sound_txt = Text().make_text(['SOUND'])

        # control settings
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
        self.interact_conf3 = Text().make_text(["forward slash"])
        self.shockwave_conf1 = Text().make_text(['Z key'])
        self.shockwave_conf2 = Text().make_text(['F key'])
        self.shockwave_conf3 = Text().make_text(["right shift"])
        self.controls_message1 = Text().make_text(['This is the recommended controls configuration'])
        self.controls_message2 = Text().make_text(['but feel free to tune it to your liking'])

        # visual settings
        self.resolution_txt = Text().make_text(['window size:'])
        self.performance_txt = Text().make_text(['performance:'])
        self.res_conf1 = Text().make_text([f'{swidth*2} x {sheight*2}'])
        self.res_conf2 = Text().make_text([f'{swidth*3} x {sheight*3}'])
        self.res_conf3 = Text().make_text([f'{swidth*4} x {sheight*4}'])
        self.perf_conf1 = Text().make_text(['Normal'])
        self.perf_conf2 = Text().make_text(['Fast'])
        self.resolution_message1 = Text().make_text(['This window size is recommended for'])
        self.resolution_message2 = Text().make_text(['your screen resolution.'])
        self.resolution_message3 = Text().make_text(['A bit too big, innit?'])
        self.perf_message1 = Text().make_text(["Use 'fast' mode only if your computer"])
        self.perf_message2 = Text().make_text(["is an utter potato."])

        # sound settings
        self.volume_txt = Text().make_text(['music volume:'])
        self.volume_conf1 = Text().make_text(['off'])
        self.volume_conf2 = Text().make_text(['normal'])
        self.volume_conf3 = Text().make_text(['deafening'])
        self.sound_effects_txt = Text().make_text(['sound effects:'])
        self.sounds_conf1 = Text().make_text(['off'])
        self.sounds_conf2 = Text().make_text(['on'])

        self.keyboard_walk_conf = keyboard_walk1
        self.keyboard_jump_conf = keyboard_jump1
        self.keyboard_shockwave_conf = keyboard_shockwave1
        self.keyboard_interact_conf = keyboard_interact1

        # counters -----------------------------------------------------------------------------------------------------
        self.walk_counter = settings_counters['walking']
        self.jump_counter = settings_counters['jumping']
        self.shockwave_counter = settings_counters['shockwave']
        self.interaction_counter = settings_counters['interaction']

        self.resolution_counter = settings_counters['resolution']
        self.resolution_counter_check = 1
        self.performance_counter = settings_counters['performance']

        self.volume_counter = settings_counters['music_volume']
        self.sounds_counter = settings_counters['sounds']

        self.settings_counters = settings_counters

        # button positional variables and other ------------------------------------------------------------------------
        gap = 30
        self.gap = 30
        control_button_start_y = 13
        self.vis_sound_button_start_y = 33
        self.button_start_y = control_button_start_y
        interbutton_space = 120

        self.center = 150

        self.control_row1_y = control_button_start_y + gap
        self.control_row2_y = control_button_start_y + gap * 2
        self.control_row3_y = control_button_start_y + gap * 3
        self.control_row4_y = control_button_start_y + gap * 4

        self.left_btn_x = self.center + 10
        self.right_btn_x = self.center + interbutton_space

        self.res_adjusted = False

        section_btn_select = pygame.Surface((118, 20))
        section_btn_select.blit(self.menu_background, (0, 0))

        section_btn_dark = pygame.Surface((118, 20))
        section_btn_dark.blit(self.menu_background, (0, 0))

        self.draw_control_screen = False
        self.draw_visual_screen = True
        self.draw_sound_screen = True

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
        self.walking_btn_left = Button(self.center + 10, control_button_start_y + gap,
                                       self.left_button, self.left_button_press, self.left_button_down)
        self.walking_btn_right = Button(self.center + interbutton_space, control_button_start_y + gap,
                                        self.right_button, self.right_button_press, self.right_button_down)
        self.jumping_btn_left = Button(self.center + 10, control_button_start_y + gap * 2,
                                       self.left_button, self.left_button_press, self.left_button_down)
        self.jumping_btn_right = Button(self.center + interbutton_space, control_button_start_y + gap * 2,
                                        self.right_button, self.right_button_press, self.right_button_down)
        self.shockwave_btn_left = Button(self.center + 10, control_button_start_y + gap * 3,
                                         self.left_button, self.left_button_press, self.left_button_down)
        self.shockwave_btn_right = Button(self.center + interbutton_space, control_button_start_y + gap * 3,
                                          self.right_button, self.right_button_press, self.right_button_down)
        self.interaction_btn_left = Button(self.center + 10, control_button_start_y + gap * 4,
                                           self.left_button, self.left_button_press, self.left_button_down)
        self.interaction_btn_right = Button(self.center + interbutton_space, control_button_start_y + gap * 4,
                                            self.right_button, self.right_button_press, self.right_button_down)

        self.menu_btn = Button(swidth / 2 - self.menu_button.get_width() / 2, 220,
                               self.menu_button, self.menu_button_press, self.menu_button_down)

        self.control_btn = Button(0, 0, self.control_button_dark, self.control_button_over,
                                  self.control_button_dark)
        self.sound_btn = Button(117 + 118, 0, self.sound_button_dark, self.sound_button_over, self.sound_button_dark)
        self.visual_btn = Button(117, 0, self.visual_button_dark, self.visual_button_over,
                                 self.visual_button_dark)

        self.resolution_btn_left = Button(self.center + 10, self.vis_sound_button_start_y + gap,
                                          self.left_button, self.left_button_press, self.left_button_down)
        self.resolution_btn_right = Button(self.center + interbutton_space, self.vis_sound_button_start_y + gap,
                                           self.right_button, self.right_button_press, self.right_button_down)
        self.performance_btn_left = Button(self.center + 10, self.vis_sound_button_start_y + gap * 2,
                                           self.left_button, self.left_button_press, self.left_button_down)
        self.performance_btn_right = Button(self.center + interbutton_space, self.vis_sound_button_start_y + gap * 2,
                                            self.right_button, self.right_button_press, self.right_button_down)

        self.volume_btn_left = Button(self.center + 10, self.vis_sound_button_start_y + gap,
                                      self.left_button, self.left_button_press, self.left_button_down)
        self.volume_btn_right = Button(self.center + interbutton_space, self.vis_sound_button_start_y + gap,
                                       self.right_button, self.right_button_press, self.right_button_down)

        self.sounds_btn_left = Button(self.center + 10, self.vis_sound_button_start_y + gap * 2,
                                      self.left_button, self.left_button_press, self.left_button_down)
        self.sounds_btn_right = Button(self.center + interbutton_space, self.vis_sound_button_start_y + gap * 2,
                                       self.right_button, self.right_button_press, self.right_button_down)

        self.keyboard_control_box1 = (self.center + 2, control_button_start_y + gap,
                                      interbutton_space + tile_size * 0.75, tile_size)
        self.keyboard_control_box_mould = pygame.Surface((interbutton_space + tile_size, tile_size))

        self.keyboard_control_box1 = self.keyboard_control_box_mould.get_rect()
        self.keyboard_control_box1.x = self.center + 6
        self.keyboard_control_box1.y = control_button_start_y + gap - 4

        self.keyboard_control_box2 = self.keyboard_control_box_mould.get_rect()
        self.keyboard_control_box2.x = self.center + 6
        self.keyboard_control_box2.y = control_button_start_y + gap * 2 - 4

        self.keyboard_control_box3 = self.keyboard_control_box_mould.get_rect()
        self.keyboard_control_box3.x = self.center + 6
        self.keyboard_control_box3.y = control_button_start_y + gap * 3 - 4

        self.keyboard_control_box4 = self.keyboard_control_box_mould.get_rect()
        self.keyboard_control_box4.x = self.center + 6
        self.keyboard_control_box4.y = control_button_start_y + gap * 4 - 4

        # --------------------------------------------------------------------------------------------------------------
    def draw_settings_menu(self, settings_screen, mouse_adjustment, events, fps_adjust):
        settings_screen.fill((0, 0, 0))
        settings_screen.blit(self.menu_background, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0]/mouse_adjustment, mouse_pos[1]/mouse_adjustment)

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

        res_left_press = False
        res_right_press = False
        perf_left_press = False
        perf_right_press = False

        vol_left_press = False
        vol_right_press = False
        sound_left_press = False
        sound_right_press = False

        final_over1 = False
        final_over2 = False

        over = False
        over1 = False
        over2 = False
        over3 = False
        over4 = False
        over5 = False
        over6 = False
        over7 = False
        over8 = False

        menu_press = False

        control_box1_over = False
        control_box2_over = False
        control_box3_over = False
        control_box4_over = False

        control_btn_trigger = False
        visual_btn_trigger = False
        sound_btn_trigger = False

        self.keyboard_highlight_counter += 1 * fps_adjust

        # drawing and updating the menu/back button --------------------------------------------------------------------
        menu_press, over = self.menu_btn.draw_button(settings_screen, False, mouse_adjustment, events)

        # CONTROL SETTINGS SCREEN ======================================================================================
        self.control_screen.blit(self.walking_txt, (self.center - 10 - self.walking_txt.get_width(),
                                                    self.button_start_y + 7 + self.gap))
        self.control_screen.blit(self.jumping_txt, (self.center - 10 - self.jumping_txt.get_width(),
                                                    self.button_start_y + 7 + self.gap * 2))
        self.control_screen.blit(self.shockwave_txt,
                                 (self.center - 10 - self.shockwave_txt.get_width(),
                                  self.button_start_y + 7 + self.gap * 3))
        self.control_screen.blit(self.interactions_txt,
                                 (self.center - 10 - self.interactions_txt.get_width(),
                                  self.button_start_y + 7 + self.gap * 4))

        self.control_screen.blit(self.keyboard_base, (swidth / 2 - self.keyboard_base.get_width() / 2,
                                                      175))
        self.control_screen.blit(self.keyboard_overlays[f'walk{self.walk_counter}'],
                                 (swidth / 2 - self.keyboard_base.get_width() / 2, 175))
        self.control_screen.blit(self.keyboard_overlays[f'jump{self.jump_counter}'],
                                 (swidth / 2 - self.keyboard_base.get_width() / 2, 175))
        self.control_screen.blit(self.keyboard_overlays[f'shockwave{self.shockwave_counter}'],
                                 (swidth / 2 - self.keyboard_base.get_width() / 2, 175))
        self.control_screen.blit(self.keyboard_overlays[f'interact{self.interaction_counter}'],
                                 (swidth / 2 - self.keyboard_base.get_width() / 2, 175))

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
        elif self.interaction_counter == 2:
            interaction_text = self.interact_conf2
        else:
            interaction_text = self.interact_conf3

        button_text_center = self.center + 65

        self.control_screen.blit(walk_text, (button_text_center - walk_text.get_width() / 2 + button_size / 2,
                                             self.control_row1_y + 7))
        self.control_screen.blit(jump_text, (button_text_center - jump_text.get_width() / 2 + button_size / 2,
                                             self.control_row2_y + 7))
        self.control_screen.blit(shockwave_text,
                                 (button_text_center - shockwave_text.get_width() / 2 + button_size / 2,
                                  self.control_row3_y + 7))
        self.control_screen.blit(interaction_text,
                                 (button_text_center - interaction_text.get_width() / 2 + button_size / 2,
                                  self.control_row4_y + 7))

        # managing the buttons to switch between control options -------------------------------------------------------
        if not self.draw_control_screen:
            if self.walk_counter > 1:
                walking_left_press, over1 = self.walking_btn_left.draw_button(self.control_screen,
                                                                              False, mouse_adjustment, events)
            else:
                self.control_screen.blit(self.left_button_grey, (self.left_btn_x, self.control_row1_y))
                inactive_button(self.left_btn_x, self.control_row1_y, self.left_button_grey,
                                mouse_adjustment)

            if self.walk_counter < 2:
                walking_right_press, over2 = self.walking_btn_right.draw_button(self.control_screen,
                                                                                False, mouse_adjustment, events)
            else:
                self.control_screen.blit(self.right_button_grey, (self.right_btn_x, self.control_row1_y))
                inactive_button(self.right_btn_x, self.control_row1_y, self.right_button_grey,
                                mouse_adjustment)

            if self.jump_counter > 1:
                jumping_left_press, over3 = self.jumping_btn_left.draw_button(self.control_screen,
                                                                              False, mouse_adjustment, events)
            else:
                self.control_screen.blit(self.left_button_grey, (self.left_btn_x, self.control_row2_y))
                inactive_button(self.left_btn_x, self.control_row2_y, self.left_button_grey,
                                mouse_adjustment)

            if self.jump_counter < 3:
                jumping_right_press, over4 = self.jumping_btn_right.draw_button(self.control_screen,
                                                                                False, mouse_adjustment, events)
            else:
                self.control_screen.blit(self.right_button_grey, (self.right_btn_x, self.control_row2_y))
                inactive_button(self.right_btn_x, self.control_row2_y, self.right_button_grey,
                                mouse_adjustment)

            if self.shockwave_counter > 1:
                shockwave_left_press, over5 = self.shockwave_btn_left.draw_button(self.control_screen,
                                                                                  False, mouse_adjustment, events)
            else:
                self.control_screen.blit(self.left_button_grey, (self.left_btn_x, self.control_row3_y))
                inactive_button(self.left_btn_x, self.control_row3_y, self.left_button_grey,
                                mouse_adjustment)

            if self.shockwave_counter < 3:
                shockwave_right_press, over6 = self.shockwave_btn_right.draw_button(self.control_screen,
                                                                                    False, mouse_adjustment, events)
            else:
                self.control_screen.blit(self.right_button_grey, (self.right_btn_x, self.control_row3_y))
                inactive_button(self.right_btn_x, self.control_row3_y, self.right_button_grey,
                                mouse_adjustment)

            if self.interaction_counter > 1:
                interactions_left_press, over7 = self.interaction_btn_left.draw_button(self.control_screen, False,
                                                                                       mouse_adjustment, events)
            else:
                self.control_screen.blit(self.left_button_grey, (self.left_btn_x, self.control_row4_y))
                inactive_button(self.left_btn_x, self.control_row4_y, self.left_button_grey,
                                mouse_adjustment)

            if self.interaction_counter < 3:
                interactions_right_press, over8 = self.interaction_btn_right.draw_button(self.control_screen,
                                                                                         False, mouse_adjustment,
                                                                                         events)
            else:
                self.control_screen.blit(self.right_button_grey, (self.right_btn_x, self.control_row4_y))
                inactive_button(self.right_btn_x, self.control_row4_y, self.right_button_grey,
                                mouse_adjustment)

            if self.keyboard_control_box1.collidepoint(mouse_pos):
                control_box1_over = True

            if self.keyboard_control_box2.collidepoint(mouse_pos):
                control_box2_over = True

            if self.keyboard_control_box3.collidepoint(mouse_pos):
                control_box3_over = True

            if self.keyboard_control_box4.collidepoint(mouse_pos):
                control_box4_over = True

            if control_box1_over:
                self.keyboard_overlays[f'walk{self.walk_counter}'].set_alpha(255)
                self.keyboard_overlays[f'jump{self.jump_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_overlays[f'shockwave{self.shockwave_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_overlays[f'interact{self.interaction_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_highlight_off = False

            elif control_box2_over:
                self.keyboard_overlays[f'walk{self.walk_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_overlays[f'jump{self.jump_counter}'].set_alpha(255)
                self.keyboard_overlays[f'shockwave{self.shockwave_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_overlays[f'interact{self.interaction_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_highlight_off = False

            elif control_box3_over:
                self.keyboard_overlays[f'walk{self.walk_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_overlays[f'jump{self.jump_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_overlays[f'shockwave{self.shockwave_counter}'].set_alpha(255)
                self.keyboard_overlays[f'interact{self.interaction_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_highlight_off = False

            elif control_box4_over:
                self.keyboard_overlays[f'walk{self.walk_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_overlays[f'jump{self.jump_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_overlays[f'shockwave{self.shockwave_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_overlays[f'interact{self.interaction_counter}'].set_alpha(255)
                self.keyboard_highlight_off = False

            elif not self.keyboard_highlight_off:
                self.keyboard_overlays[f'walk{self.walk_counter}'].set_alpha(255)
                self.keyboard_overlays[f'jump{self.jump_counter}'].set_alpha(255)
                self.keyboard_overlays[f'shockwave{self.shockwave_counter}'].set_alpha(255)
                self.keyboard_overlays[f'interact{self.interaction_counter}'].set_alpha(255)
                self.keyboard_highlight_off = True

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
        if interactions_right_press and self.interaction_counter < 3:
            self.interaction_counter += 1

        # updating the controls dictionary -----------------------------------------------------------------------------
        if menu_press:
            self.controls['left'] = self.nums_to_btns[f'left{self.walk_counter}']
            self.controls['right'] = self.nums_to_btns[f'right{self.walk_counter}']
            self.controls['jump'] = self.nums_to_btns[f'jump{self.jump_counter}']
            self.controls['interact'] = self.nums_to_btns[f'interact{self.interaction_counter}']
            self.controls['shockwave'] = self.nums_to_btns[f'shockwave{self.shockwave_counter}']
            self.controls['bin_card'] = self.nums_to_btns[f'delete_card{self.walk_counter}']

        # VISUAL SETTINGS SCREEN =======================================================================================
        self.visual_screen.blit(self.resolution_txt,
                                (self.center - 10 - self.resolution_txt.get_width(), 40 + self.gap))
        self.visual_screen.blit(self.performance_txt,
                                (self.center - 10 - self.performance_txt.get_width(), 40 + self.gap * 2))

        if self.performance_counter == 2:
            self.visual_screen.blit(self.perf_message1, (swidth / 2 - self.perf_message1.get_width() / 2,
                                                         35 + self.gap * 4))
            self.visual_screen.blit(self.perf_message2, (swidth / 2 - self.perf_message2.get_width() / 2,
                                                         20 + self.gap * 5))

        elif self.recommended_res_counter == self.resolution_counter:
            self.visual_screen.blit(self.resolution_message1, (swidth / 2 - self.resolution_message1.get_width() / 2,
                                                               35 + self.gap * 4))
            self.visual_screen.blit(self.resolution_message2, (swidth / 2 - self.resolution_message2.get_width() / 2,
                                                               20 + self.gap * 5))

        if self.recommended_res_counter < self.resolution_counter and self.performance_counter != 2:
            self.visual_screen.blit(self.resolution_message3, (swidth / 2 - self.resolution_message3.get_width() / 2,
                                                               42 + self.gap * 4))

        if self.resolution_counter == 1:
            res_text = self.res_conf1
        elif self.resolution_counter == 2:
            res_text = self.res_conf2
        else:
            res_text = self.res_conf3

        if self.performance_counter == 1:
            perf_text = self.perf_conf1
        else:
            perf_text = self.perf_conf2

        self.visual_screen.blit(res_text, (button_text_center - res_text.get_width() / 2 + button_size / 2,
                                             33 + self.gap + 7))
        self.visual_screen.blit(perf_text, (button_text_center - perf_text.get_width() / 2 + button_size / 2,
                                             33 + self.gap * 2 + 7))

        if not self.draw_visual_screen:
            if self.resolution_counter > 1:
                res_left_press, over1 = self.resolution_btn_left.draw_button(self.visual_screen,
                                                                             False, mouse_adjustment, events)
            else:
                self.visual_screen.blit(self.left_button_grey, (self.left_btn_x, 33 + self.gap))
                inactive_button(self.left_btn_x, 33 + self.gap, self.left_button_grey,
                                mouse_adjustment)

            if self.resolution_counter < 3:
                res_right_press, over2 = self.resolution_btn_right.draw_button(self.visual_screen,
                                                                               False, mouse_adjustment, events)
            else:
                self.visual_screen.blit(self.right_button_grey, (self.right_btn_x, 33 + self.gap))
                inactive_button(self.right_btn_x, 33 + self.gap, self.right_button_grey,
                                mouse_adjustment)

            if self.performance_counter > 1:
                perf_left_press, over3 = self.performance_btn_left.draw_button(self.visual_screen,
                                                                              False, mouse_adjustment, events)
            else:
                self.visual_screen.blit(self.left_button_grey, (self.left_btn_x, 33 + self.gap * 2))
                inactive_button(self.left_btn_x, 33 + self.gap * 2, self.left_button_grey,
                                mouse_adjustment)

            if self.performance_counter < 2:
                perf_right_press, over4 = self.performance_btn_right.draw_button(self.visual_screen,
                                                                                 False, mouse_adjustment, events)
            else:
                self.visual_screen.blit(self.right_button_grey, (self.right_btn_x, 33 + self.gap * 2))
                inactive_button(self.right_btn_x, 33 + self.gap * 2, self.right_button_grey,
                                mouse_adjustment)

        if res_left_press and self.resolution_counter > 1:
            self.resolution_counter -= 1
        if res_right_press and self.resolution_counter < 3:
            self.resolution_counter += 1

        if perf_left_press and self.performance_counter > 1:
            self.performance_counter -= 1
        if perf_right_press and self.performance_counter < 2:
            self.performance_counter += 1

        # SOUND SETTINGS SCREEN ========================================================================================
        self.sound_screen.blit(self.volume_txt,
                               (self.center - 10 - self.volume_txt.get_width(), 40 + self.gap))
        self.sound_screen.blit(self.sound_effects_txt,
                               (self.center - 10 - self.sound_effects_txt.get_width(), 40 + self.gap * 2))

        if self.volume_counter == 1:
            vol_text = self.volume_conf1
        elif self.volume_counter == 2:
            vol_text = self.volume_conf2
        else:
            vol_text = self.volume_conf3

        if self.sounds_counter == 1:
            sound_text = self.sounds_conf1
        else:
            sound_text = self.sounds_conf2

        if not self.draw_sound_screen:
            if self.volume_counter > 1:
                vol_left_press, over1 = self.volume_btn_left.draw_button(self.sound_screen,
                                                                         False, mouse_adjustment, events)
            else:
                self.sound_screen.blit(self.left_button_grey,
                                       (self.left_btn_x, self.vis_sound_button_start_y + self.gap))
                inactive_button(self.left_btn_x, self.vis_sound_button_start_y + self.gap, self.left_button_grey,
                                mouse_adjustment)
            if self.volume_counter < 3:
                vol_right_press, over2 = self.volume_btn_right.draw_button(self.sound_screen,
                                                                           False, mouse_adjustment, events)
            else:
                self.sound_screen.blit(self.right_button_grey,
                                       (self.right_btn_x, self.vis_sound_button_start_y + self.gap))
                inactive_button(self.right_btn_x, self.vis_sound_button_start_y + self.gap, self.right_button_grey,
                                mouse_adjustment)

            self.sound_screen.blit(vol_text, (button_text_center - vol_text.get_width() / 2 + button_size / 2,
                                              self.vis_sound_button_start_y + self.gap + 7))

            if self.sounds_counter > 1:
                sound_left_press, over1 = self.sounds_btn_left.draw_button(self.sound_screen,
                                                                           False, mouse_adjustment, events)
            else:
                self.sound_screen.blit(self.left_button_grey,
                                       (self.left_btn_x, self.vis_sound_button_start_y + self.gap * 2))
                inactive_button(self.left_btn_x, self.vis_sound_button_start_y + self.gap * 2, self.left_button_grey,
                                mouse_adjustment)
            if self.sounds_counter < 2:
                sound_right_press, over2 = self.sounds_btn_right.draw_button(self.sound_screen,
                                                                             False, mouse_adjustment, events)
            else:
                self.sound_screen.blit(self.right_button_grey,
                                       (self.right_btn_x, self.vis_sound_button_start_y + self.gap * 2))
                inactive_button(self.right_btn_x, self.vis_sound_button_start_y + self.gap * 2, self.right_button_grey,
                                mouse_adjustment)

            self.sound_screen.blit(sound_text, (button_text_center - sound_text.get_width() / 2 + button_size / 2,
                                              self.vis_sound_button_start_y + self.gap * 2 + 7))

        if vol_left_press and self.volume_counter > 1:
            self.volume_counter -= 1
        if vol_right_press and self.volume_counter < 3:
            self.volume_counter += 1

        if sound_left_press and self.sounds_counter > 1:
            self.sounds_counter -= 1
        if sound_right_press and self.sounds_counter < 2:
            self.sounds_counter += 1

        # screen managing ==============================================================================================
        if not self.draw_control_screen:
            settings_screen.blit(self.control_screen, (0, 0))
        if not self.draw_visual_screen:
            settings_screen.blit(self.visual_screen, (0, 0))
        if not self.draw_sound_screen:
            settings_screen.blit(self.sound_screen, (0, 0))

        # managing the section buttons ---------------------------------------------------------------------------------
        if self.draw_control_screen:
            control_btn_trigger, not_over = self.control_btn.draw_button(settings_screen,
                                                                         False, mouse_adjustment, events)
        else:
            settings_screen.blit(self.control_button_select, (0, 0))
        if self.draw_visual_screen:
            visual_btn_trigger, not_over = self.visual_btn.draw_button(settings_screen, False, mouse_adjustment,
                                                                       events)
        else:
            settings_screen.blit(self.visual_button_select, (117, 0))
        if self.draw_sound_screen:
            sound_btn_trigger, not_over = self.sound_btn.draw_button(settings_screen, False, mouse_adjustment,
                                                                     events)
        else:
            settings_screen.blit(self.sound_button_select, (117 + 118, 0))

        if control_btn_trigger:
            self.draw_control_screen = False
            self.draw_visual_screen = True
            self.draw_sound_screen = True
        if visual_btn_trigger:
            self.draw_control_screen = True
            self.draw_visual_screen = False
            self.draw_sound_screen = True
        if sound_btn_trigger:
            self.draw_control_screen = True
            self.draw_visual_screen = True
            self.draw_sound_screen = False

        if over or over1 or over3 or over5 or over7:
            final_over1 = True
        if over2 or over4 or over6 or over8:
            final_over2 = True

        if res_right_press or res_left_press:
            adjust_resolution = True
        else:
            adjust_resolution = False

        resolution = self.resolutions[str(self.resolution_counter)]

        counters = [self.walk_counter, self.jump_counter, self.interaction_counter, self.shockwave_counter]

        if menu_press:
            self.settings_counters['walking'] = self.walk_counter
            self.settings_counters['jumping'] = self.jump_counter
            self.settings_counters['shockwave'] = self.shockwave_counter
            self.settings_counters['interaction'] = self.interaction_counter
            self.settings_counters['resolution'] = self.resolution_counter
            self.settings_counters['performance'] = self.performance_counter
            self.settings_counters['music_volume'] = self.volume_counter
            self.settings_counters['sounds'] = self.sounds_counter

        return menu_press, self.controls, final_over1, final_over2, self.performance_counter, resolution,\
               adjust_resolution, counters, self.settings_counters
