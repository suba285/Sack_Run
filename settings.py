import pygame._sdl2
import json
from image_loader import img_loader
from font_manager import Text
from button import Button
from popup_bg_generator import popup_bg_generator
from screen_info import swidth, sheight

tile_size = 32
button_size = tile_size * 0.75

# this file is a total mess, you have been warned


class SettingsMenu:
    def __init__(self, controls, settings_counters, resolutions, recommended_res_counter):
        text = Text()
        # unlocked world data ------------------------------------------------------------------------------------------
        try:
            with open('data/unlocked_worlds.json', 'r') as json_file:
                unlocked_world_data = json.load(json_file)
        except FileNotFoundError:
            unlocked_world_data = [True, False, False, False, False]
        if unlocked_world_data[-1]:
            self.speedrun_unlocked = True
        else:
            self.speedrun_unlocked = False

        # image loading ------------------------------------------------------------------------------------------------
        self.menu_background = img_loader('data/images/menu_background.PNG', swidth, sheight)

        self.left_button = img_loader('data/images/button_left.PNG', button_size, button_size)
        self.left_button_press = img_loader('data/images/button_left_press.PNG', button_size, button_size)
        self.left_button_down = img_loader('data/images/button_left_down.PNG', button_size, button_size)

        self.right_button = pygame.transform.flip(self.left_button, True, False)
        self.right_button_press = pygame.transform.flip(self.left_button_press, True, False)
        self.right_button_down = pygame.transform.flip(self.left_button_down, True, False)

        self.arrow_button_mask = pygame.mask.from_surface(self.right_button)
        self.arrow_button_outline = pygame.mask.Mask.outline(self.arrow_button_mask)
        self.arrow_button_outline_surf = pygame.Surface((button_size, button_size))
        self.arrow_button_outline_surf.set_colorkey((0, 0, 0))
        self.arrow_button_outline_alpha = 255
        for pixel in self.arrow_button_outline:
            self.arrow_button_outline_surf.set_at((pixel[0], pixel[1]), (255, 255, 255))

        self.right_button_gray = img_loader('data/images/button_right_grey.PNG', button_size, button_size)
        self.left_button_gray = pygame.transform.flip(self.right_button_gray, True, False)
        self.right_button_gray_dim = self.right_button_gray.copy()
        self.left_button_gray_dim = self.right_button_gray.copy()
        self.right_button_gray_dim.set_alpha(100)
        self.left_button_gray_dim.set_alpha(100)

        self.menu_button = img_loader('data/images/button_back.PNG', tile_size * 1.5, tile_size * 0.75)
        self.menu_button_press = img_loader('data/images/button_back_press.PNG', tile_size * 1.5, tile_size * 0.75)
        self.menu_button_down = img_loader('data/images/button_back_down.PNG', tile_size * 1.5, tile_size * 0.75)

        self.calibrate_btn = img_loader('data/images/button_calibrate.PNG', tile_size * 2, tile_size * 0.75)
        self.calibrate_btn_press = img_loader('data/images/button_calibrate_press.PNG', tile_size * 2, tile_size * 0.75)
        self.calibrate_btn_down= img_loader('data/images/button_calibrate_down.PNG', tile_size * 2, tile_size * 0.75)

        self.keyboard_base = img_loader('data/images/keyboard_highlights/keyboard_base.PNG', tile_size * 3, tile_size)
        self.keyboard_press_surf = pygame.Surface((tile_size * 3, tile_size))
        self.keyboard_press_surf.fill((255, 255, 255))
        self.keyboard_press_surf.set_colorkey((255, 255, 255))
        self.mouse_base = img_loader('data/images/keyboard_highlights/mouse_base.PNG', tile_size, tile_size)
        keyboard_jump1 = img_loader('data/images/keyboard_highlights/keyboard_jump1.PNG',
                                    tile_size * 3, tile_size)
        keyboard_jump2 = img_loader('data/images/keyboard_highlights/keyboard_jump2.PNG',
                                    tile_size * 3, tile_size)
        keyboard_jump3 = img_loader('data/images/keyboard_highlights/keyboard_jump3.PNG',
                                    tile_size * 3, tile_size)
        keyboard_walk1 = img_loader('data/images/keyboard_highlights/keyboard_walk1.PNG',
                                    tile_size * 3, tile_size)
        keyboard_walk2 = img_loader('data/images/keyboard_highlights/keyboard_walk2.PNG',
                                    tile_size * 3, tile_size)
        keyboard_cards1 = img_loader('data/images/keyboard_highlights/keyboard_cards1.PNG',
                                     tile_size * 3, tile_size)
        mouse_cards1 = img_loader('data/images/keyboard_highlights/mouse_cards.PNG', tile_size, tile_size)

        self.kbr_bg = img_loader('data/images/keyboard_highlights/keyboard_background.PNG', 130, 50)

        self.keyboard_overlays = {
            'jump1': keyboard_jump1,
            'jump2': keyboard_jump2,
            'jump3': keyboard_jump3,
            'walk1': keyboard_walk1,
            'walk2': keyboard_walk2,
            'keybrd_cards': keyboard_cards1,
            'mouse_cards': mouse_cards1
        }

        rows = [4, 7, 10, 13]
        x_by_row = [6, 7, 6, 0]
        self.pygame_kbr_events = [
            [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o,
             pygame.K_p],
            [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k,
             pygame.K_l],
            [pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n, pygame.K_m, ],
            [pygame.K_SPACE, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]
        ]
        self.keyboard_press_pos = {
            pygame.K_SPACE: [30, 26],
            pygame.K_UP: [80, 26],
            pygame.K_LEFT: [74, 28],
            pygame.K_DOWN: [80, 28],
            pygame.K_RIGHT: [86, 28],
        }
        key_highlight = pygame.Surface((4, 4))
        key_highlight.fill((0, 0, 0))
        space_hightlight = pygame.Surface((28, 4))
        space_hightlight.fill((0, 0, 0))
        arrow_hightlight = pygame.Surface((4, 2))
        arrow_hightlight.fill((0, 0, 0))
        row_count = 0
        for row in self.pygame_kbr_events:
            y = rows[row_count]
            key_count = 0
            for key in row:
                x = x_by_row[row_count]
                if row_count < 3:
                    self.keyboard_press_pos[key] = [(x + key_count * 3) * 2, y * 2]
                key_count += 1
            row_count += 1

        self.keyboard_presses = {}
        for row in self.pygame_kbr_events:
            for key in row:
                if key == pygame.K_SPACE:
                    img = space_hightlight
                elif key in [pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN]:
                    img = arrow_hightlight
                else:
                    img = key_highlight
                self.keyboard_presses[key] = [False, self.keyboard_press_pos[key], img]

        self.mouse_press_overlays = {
            1: img_loader('data/images/keyboard_highlights/mouse_left_c.PNG', tile_size, tile_size),
            3: img_loader('data/images/keyboard_highlights/mouse_right_c.PNG', tile_size, tile_size),
        }
        self.mouse_current_press_overlay = self.mouse_press_overlays[1]
        self.mouse_press = False

        # controller press overlays
        self.controller = img_loader('data/images/keyboard_highlights/controller.PNG', tile_size * 2, tile_size)
        colorkey = (255, 255, 255)
        self.controller_presses = {
            'a': [False, img_loader('data/images/keyboard_highlights/cont_a_overlay.PNG', tile_size * 2, tile_size,
                                    colorkey)],
            'b': [False, img_loader('data/images/keyboard_highlights/cont_b_overlay.PNG', tile_size * 2, tile_size,
                                    colorkey)],
            'x': [False, img_loader('data/images/keyboard_highlights/cont_x_overlay.PNG', tile_size * 2, tile_size,
                                    colorkey)],
            'pause': [False, img_loader('data/images/keyboard_highlights/cont_pause_overlay.PNG', tile_size * 2,
                                        tile_size, colorkey)],
            'rb': [False, img_loader('data/images/keyboard_highlights/cont_rb_overlay.PNG', tile_size * 2, tile_size,
                                     colorkey)],
            'lb': [False, img_loader('data/images/keyboard_highlights/cont_lb_overlay.PNG', tile_size * 2, tile_size,
                                     colorkey)],
            'up': [False, img_loader('data/images/keyboard_highlights/cont_up_overlay.PNG', tile_size * 2, tile_size,
                                     colorkey)],
            'right': [False, img_loader('data/images/keyboard_highlights/cont_right_overlay.PNG', tile_size * 2,
                                        tile_size, colorkey)],
            'left': [False, img_loader('data/images/keyboard_highlights/cont_left_overlay.PNG', tile_size * 2,
                                       tile_size, colorkey)],
            'down': [False, img_loader('data/images/keyboard_highlights/cont_down_overlay.PNG', tile_size * 2,
                                       tile_size, colorkey)],
        }

        self.joystick_movement = [0, 0]

        # variables ----------------------------------------------------------------------------------------------------
        self.controls = controls
        self.cont_overlay_key = {
            controls['configuration'][1]: 'lb',
            controls['configuration'][2]: 'rb',
            controls['configuration'][3]: 'pause',
            0: 'a',
            1: 'b',
            2: 'x',
        }
        self.recommended_res_counter = recommended_res_counter
        self.keyboard_highlight_counter = 60
        self.keyboard_highlight_off = False
        self.keyboard_bg_alpha = 100
        self.screen_alpha_counter = 0

        # major surfaces -----------------------------------------------------------------------------------------------
        self.control_screen = pygame.Surface((swidth, (220 / 270 * sheight)))
        self.visual_screen = pygame.Surface((swidth, (220 / 270 * sheight)))
        self.sound_screen = pygame.Surface((swidth, (220 / 270 * sheight)))

        self.dim_surf = pygame.Surface((swidth, sheight))
        self.dim_surf.fill((0, 0, 0))
        self.dim_surf_target_alpha = 140
        self.dim_surf_alpha = 0
        self.dim_surf.set_alpha(self.dim_surf_alpha)

        # dictionaries -------------------------------------------------------------------------------------------------
        self.nums_to_btns = {
            'left1': pygame.K_a,
            'right1': pygame.K_d,
            'left2': pygame.K_LEFT,
            'right2': pygame.K_RIGHT,
            'jump1': pygame.K_SPACE,
            'jump2': pygame.K_w,
            'jump3': pygame.K_UP,
            'configuration': controls['configuration'],
            'rumble1': pygame.K_x,
            'rumble2': pygame.K_e,
            'rumble3': pygame.K_SLASH,
        }

        self.resolutions = resolutions

        # text generation ----------------------------------------------------------------------------------------------
        self.controls_txt = text.make_text(['CONTROL'])
        self.visual_txt = text.make_text(['MAIN'])
        self.sound_txt = text.make_text(['SOUND'])
        self.controls_txt_vague = self.controls_txt.copy()
        self.controls_txt_vague.set_alpha(180)
        self.visual_txt_vague = self.visual_txt.copy()
        self.visual_txt_vague.set_alpha(180)
        self.sound_txt_vague = self.sound_txt.copy()
        self.sound_txt_vague.set_alpha(180)

        self.on_conf = text.make_text(['on'])
        self.off_conf = text.make_text(['off'])

        # control settings
        self.walking_txt = text.make_text(['keyboard walking:'])
        self.jumping_txt = text.make_text(['keyboard jumping:'])
        self.keyboard_cards = text.make_text(['keyboard cards:'])
        self.configuration_txt = text.make_text(['controller calibration:'])
        self.move_conf1 = text.make_text(['A and D keys'])
        self.move_conf2 = text.make_text(['arrow keys'])
        self.jump_conf1 = text.make_text(['space bar'])
        self.jump_conf2 = text.make_text(['W key'])
        self.jump_conf3 = text.make_text(['up key'])
        self.cards_conf1 = text.make_text(['mouse'])
        self.cards_conf2 = text.make_text(['J K L keys'])

        # visual settings
        self.resolution_txt = text.make_text(['window size:'])
        self.pov_txt = text.make_text(['POV adjust:'])
        self.res_conf1 = text.make_text([f'{int(swidth*2)} x {int(sheight*2)}'])
        self.res_conf2 = text.make_text([f'{int(swidth*3)} x {int(sheight*3)}'])
        self.res_conf3 = text.make_text([f'{int(swidth*4)} x {int(sheight*4)}'])
        self.res_conf4 = text.make_text(['FULLSCREEN'])
        self.pov_conf1 = text.make_text(['off'])
        self.pov_conf2 = text.make_text(['on'])
        self.speedrun_txt = text.make_text(['speedrun mode:'])
        self.speedrun_conf1 = text.make_text(['off'])
        self.speedrun_conf2 = text.make_text(['on'])
        self.speedrun_txt_dim = self.speedrun_txt.copy()
        self.speedrun_txt_dim.set_alpha(90)
        self.speedrun_conf1_dim = self.speedrun_conf1.copy()
        self.speedrun_conf1_dim.set_alpha(90)
        self.speedrun_conf2_dim = self.speedrun_conf2.copy()
        self.speedrun_conf2_dim.set_alpha(90)
        self.hitbox_txt = text.make_text(['show hitbox:'])
        self.hitbox_conf1 = self.off_conf
        self.hitbox_conf2 = self.on_conf
        self.unlock_speedrun_txt = text.make_text(['complete game to unlock'])

        # sound settings
        self.volume_txt = text.make_text(['music volume:'])
        self.volume_conf1 = self.off_conf
        self.volume_conf2 = text.make_text(['normal'])
        self.volume_conf3 = text.make_text(['deafening'])
        self.sound_effects_txt = text.make_text(['sound effects:'])
        self.sounds_conf1 = self.off_conf
        self.sounds_conf2 = self.on_conf

        # counters -----------------------------------------------------------------------------------------------------
        self.walk_counter = settings_counters['walking']
        self.jump_counter = settings_counters['jumping']
        self.cards_counter = settings_counters['cards']
        self.configuration_counter = settings_counters['configuration']

        self.resolution_counter = settings_counters['resolution']
        self.resolution_counter_check = 1
        self.pov_counter = settings_counters['pov']
        self.hitbox_counter = settings_counters['hitbox']
        self.speedrun_counter = settings_counters['speedrun']

        self.volume_counter = settings_counters['music_volume']
        self.sounds_counter = settings_counters['sounds']

        self.settings_counters = settings_counters

        self.section_counter = 0

        # --------------------------------------------------------------------------------------------------------------
        self.joystick_counter = 0
        self.joystick_moved = False
        self.calib_joystick_moved = False
        self.hat_x_pressed = False
        self.hat_y_pressed = False
        self.hat_value = [0, 0]

        # button positional variables and other ------------------------------------------------------------------------
        gap = 30 / 270 * sheight
        self.gap = 30 / 270 * sheight
        control_button_start_y = round(13 / 270 * sheight)
        self.vis_sound_button_start_y = round(33 / 270 * sheight)
        self.button_start_y = control_button_start_y
        interbutton_space = 120

        self.center = swidth / 2 - 20

        self.control_row1_y = control_button_start_y + gap
        self.control_row2_y = control_button_start_y + gap * 2
        self.control_row3_y = control_button_start_y + gap * 3
        self.control_row4_y = control_button_start_y + gap * 4

        self.left_btn_x = self.center + 10
        self.right_btn_x = self.center + interbutton_space

        self.res_adjusted = False

        self.draw_control_screen = False
        self.draw_visual_screen = True
        self.draw_sound_screen = True

        if swidth % 3 == 0:
            section_btn_width1 = swidth / 3
            section_btn_width2 = swidth / 3
            section_btn_width3 = swidth / 3
        elif swidth % 3 == 1:
            section_btn_width1 = (swidth - 1) / 3
            section_btn_width3 = (swidth - 1) / 3
            section_btn_width2 = swidth - 2 * section_btn_width1
        else:
            section_btn_width2 = (swidth - 2) / 3
            section_btn_width1 = (swidth - section_btn_width2) / 2
            section_btn_width3 = (swidth - section_btn_width2) / 2

        section_btn_select = pygame.Surface((200, 20))
        section_btn_select.blit(self.menu_background, (0, 0))

        section_btn_dark = pygame.Surface((200, 20))
        section_btn_dark.fill((56, 41, 59))

        self.control_button_select = pygame.Surface((section_btn_width1, 20))
        self.sound_button_select = pygame.Surface((section_btn_width3, 20))
        self.visual_button_select = pygame.Surface((section_btn_width2, 20))

        self.control_button_dark = pygame.Surface((section_btn_width1, 20))
        self.sound_button_dark = pygame.Surface((section_btn_width3, 20))
        self.visual_button_dark = pygame.Surface((section_btn_width2, 20))

        self.control_button_select.blit(section_btn_select, (0, 0))
        self.control_button_select.blit(self.controls_txt, (swidth / 6 - self.controls_txt.get_width() / 2, 7))

        self.sound_button_select.blit(section_btn_select, (0, 0))
        self.sound_button_select.blit(self.sound_txt, (swidth / 6 - self.sound_txt.get_width() / 2, 7))

        self.visual_button_select.blit(section_btn_select, (0, 0))
        self.visual_button_select.blit(self.visual_txt, (swidth / 6 - self.visual_txt.get_width() / 2, 7))

        self.control_button_dark.blit(section_btn_dark, (0, 0))
        self.control_button_dark.blit(self.controls_txt, (swidth / 6 - self.controls_txt_vague.get_width() / 2, 7))

        self.sound_button_dark.blit(section_btn_dark, (0, 0))
        self.sound_button_dark.blit(self.sound_txt, (swidth / 6 - self.sound_txt_vague.get_width() / 2, 7))

        self.visual_button_dark.blit(section_btn_dark, (0, 0))
        self.visual_button_dark.blit(self.visual_txt, (swidth / 6 - self.visual_txt_vague.get_width() / 2, 7))

        self.control_button_over = pygame.Surface((section_btn_width1, 20))
        self.control_button_over.blit(self.control_button_dark, (0, 0))
        self.control_button_over.blit(self.controls_txt, (swidth / 6 - self.controls_txt.get_width() / 2, 7))

        self.visual_button_over = pygame.Surface((section_btn_width2, 20))
        self.visual_button_over.blit(self.visual_button_dark, (0, 0))
        self.visual_button_over.blit(self.visual_txt, (swidth / 6 - self.visual_txt.get_width() / 2, 7))

        self.sound_button_over = pygame.Surface((section_btn_width3, 20))
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
        self.rumble_btn_left = Button(self.center + 10, control_button_start_y + gap * 3,
                                      self.left_button, self.left_button_press, self.left_button_down)
        self.rumble_btn_right = Button(self.center + interbutton_space, control_button_start_y + gap * 3,
                                       self.right_button, self.right_button_press, self.right_button_down)
        self.config_btn_left = Button(self.center + 10, control_button_start_y + gap * 4,
                                      self.left_button, self.left_button_press, self.left_button_down)
        self.config_btn_right = Button(self.center + interbutton_space, control_button_start_y + gap * 4,
                                       self.right_button, self.right_button_press, self.right_button_down)

        self.calibration_btn = Button(self.center + 8,
                                      control_button_start_y + gap * 4,
                                      self.calibrate_btn, self.calibrate_btn_press, self.calibrate_btn_down)

        self.menu_btn = Button(swidth / 2 - self.menu_button.get_width() / 2, round(220 / 270 * sheight),
                               self.menu_button, self.menu_button_press, self.menu_button_down)

        self.control_btn = Button(0, 0, self.control_button_dark, self.control_button_over,
                                  self.control_button_dark)
        self.sound_btn = Button(section_btn_width1 + section_btn_width2, 0,
                                self.sound_button_dark, self.sound_button_over, self.sound_button_dark)
        self.visual_btn = Button(section_btn_width1, 0, self.visual_button_dark, self.visual_button_over,
                                 self.visual_button_dark)

        self.resolution_btn_left = Button(self.center + 10, self.vis_sound_button_start_y + gap,
                                          self.left_button, self.left_button_press, self.left_button_down)
        self.resolution_btn_right = Button(self.center + interbutton_space, self.vis_sound_button_start_y + gap,
                                           self.right_button, self.right_button_press, self.right_button_down)
        self.performance_btn_left = Button(self.center + 10, self.vis_sound_button_start_y + gap * 2,
                                           self.left_button, self.left_button_press, self.left_button_down)
        self.performance_btn_right = Button(self.center + interbutton_space, self.vis_sound_button_start_y + gap * 2,
                                            self.right_button, self.right_button_press, self.right_button_down)
        self.hitbox_btn_left = Button(self.center + 10, self.vis_sound_button_start_y + gap * 3,
                                           self.left_button, self.left_button_press, self.left_button_down)
        self.hitbox_btn_right = Button(self.center + interbutton_space, self.vis_sound_button_start_y + gap * 3,
                                            self.right_button, self.right_button_press, self.right_button_down)
        self.speedrun_btn_left = Button(self.center + 10, self.vis_sound_button_start_y + gap * 4,
                                        self.left_button, self.left_button_press, self.left_button_down)
        self.speedrun_btn_right = Button(self.center + interbutton_space, self.vis_sound_button_start_y + gap * 4,
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

        self.volume_col_box = pygame.Rect(self.center + 10, self.vis_sound_button_start_y + gap, 150, 30)

        # pov settings popup window
        self.pov_popup_text = text.make_text(['POV settings changes will apply after restarting the game'])
        self.pov_popup = popup_bg_generator((self.pov_popup_text.get_width() + 10, 15))
        self.pov_popup.blit(self.pov_popup_text, (7, 7))

        self.pov_popup_counter = 0

        # no controller detected popup window
        self.no_controller_txt = text.make_text(['no controller connected'])
        self.no_controller_popup = popup_bg_generator((self.no_controller_txt.get_width() + 10, 15))
        self.no_controller_popup.blit(self.no_controller_txt, (7, 7))
        self.no_controller_counter = 0

        # controller configuration popup window
        self.controller_conf_popup0 = popup_bg_generator((200, 100))
        self.controller_conf_popup1 = popup_bg_generator((200, 100))
        self.controller_conf_popup2 = popup_bg_generator((200, 100))
        self.controller_conf_popup3 = popup_bg_generator((200, 100))
        self.controller_conf_popup4 = popup_bg_generator((200, 100))
        self.controller_conf_popup5 = popup_bg_generator((200, 100))
        self.controller_conf_popup6 = popup_bg_generator((200, 100))
        self.controller_conf_popup7 = popup_bg_generator((200, 100))
        self.controller_conf_title = text.make_text(['CONTROLLER CALIBRATION'])
        self.controller_conf_cal0 = text.make_text(['move the left stick as shown below'])
        self.controller_conf_cal1 = text.make_text(['press the LB button (left bumper)'])
        self.controller_conf_cal2 = text.make_text(['press the RB button (right bumper)'])
        self.controller_conf_cal3 = text.make_text(['press the options button (pause)'])
        self.controller_conf_cal4 = text.make_text(['press the left face button'])
        self.controller_conf_cal5 = text.make_text(['press the bottom face button'])
        self.controller_conf_cal6 = text.make_text(['press the right face button'])
        self.controller_conf_cal7 = text.make_text(['choose your button naming'])
        button_rb = img_loader('data/images/buttons/button_rb.PNG', tile_size / 2, tile_size / 2)
        button_lb = img_loader('data/images/buttons/button_lb.PNG', tile_size / 2, tile_size / 2)
        self.button_rb = button_rb
        self.button_lb = button_lb
        button_rb_press = img_loader('data/images/buttons/button_rb_press.PNG', tile_size / 2, tile_size / 2)
        button_lb_press = img_loader('data/images/buttons/button_lb_press.PNG', tile_size / 2, tile_size / 2)
        button_a = img_loader('data/images/buttons/button_a.PNG', tile_size / 2, tile_size / 2)
        button_b = img_loader('data/images/buttons/button_b.PNG', tile_size / 2, tile_size / 2)
        button_x = img_loader('data/images/buttons/button_x.PNG', tile_size / 2, tile_size / 2)
        button_square = img_loader('data/images/buttons/button_square.PNG', tile_size / 2, tile_size / 2)
        button_cross = img_loader('data/images/buttons/button_cross.PNG', tile_size / 2, tile_size / 2)
        button_circle = img_loader('data/images/buttons/button_circle.PNG', tile_size / 2, tile_size / 2)
        self.steps_to_btns = {
            4: [button_b, button_circle],
            5: [button_a, button_cross],
            6: [button_x, button_square]
        }
        self.controller_hat_imgs = {
            0: img_loader('data/images/buttons/hat.PNG', tile_size, tile_size),
            1: img_loader('data/images/buttons/hat_R.PNG', tile_size, tile_size),
            2: img_loader('data/images/buttons/hat_D.PNG', tile_size, tile_size),
            3: img_loader('data/images/buttons/hat_L.PNG', tile_size, tile_size),
            4: img_loader('data/images/buttons/hat_U.PNG', tile_size, tile_size),
        }
        self.controller_hat_animation_surf = pygame.Surface((tile_size, tile_size))
        self.controller_hat_animation_surf.set_colorkey((0, 0, 0))

        btn_gap = 2
        btn_names_surf_width = int(tile_size * 1.5 + btn_gap * 4)
        self.btn_names1 = pygame.Surface((btn_names_surf_width, 20))
        self.btn_names2 = pygame.Surface((btn_names_surf_width, 20))
        self.btn_names1.set_colorkey((0, 0, 0))
        self.btn_names2.set_colorkey((0, 0, 0))
        popup_bg_colour = (60, 55, 60)
        self.btn_names1.fill(popup_bg_colour)
        self.btn_names2.fill(popup_bg_colour)
        self.btn_names1.set_at((0, 0), (0, 0, 0))
        self.btn_names2.set_at((0, 0), (0, 0, 0))
        self.btn_names1.set_at((btn_names_surf_width - 1, 0), (0, 0, 0))
        self.btn_names2.set_at((btn_names_surf_width - 1, 0), (0, 0, 0))
        self.btn_names1.set_at((btn_names_surf_width - 1, 19), (0, 0, 0))
        self.btn_names2.set_at((btn_names_surf_width - 1, 19), (0, 0, 0))
        self.btn_names1.set_at((0, 19), (0, 0, 0))
        self.btn_names2.set_at((0, 19), (0, 0, 0))

        x = btn_gap
        self.btn_names1.blit(button_x, (x, 2))
        self.btn_names2.blit(button_square, (x, 2))
        x += tile_size / 2 + btn_gap
        self.btn_names1.blit(button_a, (x, 2))
        self.btn_names2.blit(button_cross, (x, 2))
        x += tile_size / 2 + btn_gap
        self.btn_names1.blit(button_b, (x, 2))
        self.btn_names2.blit(button_circle, (x, 2))
        btn_width = self.btn_names2.get_width()
        self.btn_names_button1 = Button(100 - btn_width / 2 - 40, 60, self.btn_names1, self.btn_names1, self.btn_names1)
        self.btn_names_button2 = Button(100 - btn_width / 2 + 40, 60, self.btn_names2, self.btn_names2, self.btn_names2)

        self.bumpers = {
            '1_1': button_lb,
            '1_2': button_lb_press,
            '2_1': button_rb,
            '2_2': button_rb_press
        }

        or_text = text.make_text(['or'])
        cancel_text = text.make_text(['cancel'])
        self.cancel_surface = pygame.Surface((tile_size + or_text.get_width() + cancel_text.get_width() + 4, tile_size / 2))
        self.cancel_surface.set_colorkey((0, 0, 0))
        x = 0
        self.cancel_surface.blit(button_a, (x, 0))
        x += button_a.get_width() + 1
        self.cancel_surface.blit(or_text, (x, 4))
        x += or_text.get_width() + 1
        self.cancel_surface.blit(button_cross, (x, 0))
        x += button_cross.get_width() + 2
        self.cancel_surface.blit(cancel_text, (x, 4))

        self.controller_calibration_btn_surf = pygame.Surface((tile_size / 2, tile_size / 2))
        self.controller_calibration_2btn_surf = pygame.Surface((tile_size * 1.5, tile_size / 2))

        popup_width = self.controller_conf_popup1.get_width()
        popup_height = self.controller_conf_popup1.get_height()
        face_center_x = popup_width / 2 - 8
        face_y = popup_height / 2 - 8
        self.controller_conf_popup0.blit(self.controller_conf_title,
                                         (popup_width / 2 - self.controller_conf_title.get_width() / 2, 6))
        self.controller_conf_popup0.blit(self.controller_conf_cal0,
                                         (popup_width / 2 - self.controller_conf_cal0.get_width() / 2, 30))
        self.controller_conf_popup1.blit(self.controller_conf_title,
                                         (popup_width / 2 - self.controller_conf_title.get_width() / 2, 6))
        self.controller_conf_popup1.blit(self.controller_conf_cal1,
                                         (popup_width / 2 - self.controller_conf_cal1.get_width() / 2, 30))
        self.controller_conf_popup2.blit(self.controller_conf_title,
                                         (popup_width / 2 - self.controller_conf_title.get_width() / 2, 6))
        self.controller_conf_popup2.blit(self.controller_conf_cal2,
                                         (popup_width / 2 - self.controller_conf_cal2.get_width() / 2, 30))
        self.controller_conf_popup3.blit(self.controller_conf_title,
                                         (popup_width / 2 - self.controller_conf_title.get_width() / 2, 6))
        self.controller_conf_popup3.blit(self.controller_conf_cal3,
                                         (popup_width / 2 - self.controller_conf_cal3.get_width() / 2, 30))
        self.controller_conf_popup4.blit(self.controller_conf_title,
                                         (popup_width / 2 - self.controller_conf_title.get_width() / 2, 6))
        self.controller_conf_popup4.blit(self.controller_conf_cal4,
                                         (popup_width / 2 - self.controller_conf_cal4.get_width() / 2, 30))
        self.controller_conf_popup4.blit(button_b, (face_center_x - 10, face_y))
        self.controller_conf_popup4.blit(button_circle, (face_center_x + 10, face_y))
        self.controller_conf_popup5.blit(self.controller_conf_title,
                                         (popup_width / 2 - self.controller_conf_title.get_width() / 2, 6))
        self.controller_conf_popup5.blit(self.controller_conf_cal5,
                                         (popup_width / 2 - self.controller_conf_cal5.get_width() / 2, 30))
        self.controller_conf_popup5.blit(button_a, (face_center_x - 10, face_y))
        self.controller_conf_popup5.blit(button_cross, (face_center_x + 10, face_y))
        self.controller_conf_popup6.blit(self.controller_conf_title,
                                         (popup_width / 2 - self.controller_conf_title.get_width() / 2, 6))
        self.controller_conf_popup6.blit(self.controller_conf_cal6,
                                         (popup_width / 2 - self.controller_conf_cal6.get_width() / 2, 30))
        self.controller_conf_popup6.blit(button_x, (face_center_x - 10, face_y))
        self.controller_conf_popup6.blit(button_square, (face_center_x + 10, face_y))
        self.controller_conf_popup7.blit(self.controller_conf_title,
                                         (popup_width / 2 - self.controller_conf_title.get_width() / 2, 6))
        self.controller_conf_popup7.blit(self.controller_conf_cal7,
                                         (popup_width / 2 - self.controller_conf_cal4.get_width() / 2, 30))

        self.controller_calibration = False
        self.controller_calibration_counter = 0
        self.controller_calibration_step_counter = 0
        self.controller_calibration_button_counter = 0
        self.controller_calibration_axis_counter = 0
        self.calibrated_hat_btns = []
        self.controller_configuration = [[], -1, -1, -1, -1, -1, -1, -1]
        self.controller_taken_btns = []
        self.choose_different_btn_counter = 0
        self.btn_names_counter = 1

        self.choose_different_btn_txt = text.make_text(['this button is already assigned'])
        self.choose_different_btn_surf = pygame.Surface((self.choose_different_btn_txt.get_width(), 30))
        self.choose_different_btn_surf.fill((78, 69, 80))
        self.choose_different_btn_surf.blit(self.choose_different_btn_txt,
                                            (0, 10))

    def update_settings_counters(self, settings_counters, controls):
        self.settings_counters = settings_counters
        self.walk_counter = settings_counters['walking']
        self.jump_counter = settings_counters['jumping']
        self.cards_counter = settings_counters['cards']
        self.configuration_counter = settings_counters['configuration']

        self.resolution_counter = settings_counters['resolution']
        self.resolution_counter_check = 1
        self.pov_counter = settings_counters['pov']
        self.hitbox_counter = settings_counters['hitbox']
        self.speedrun_counter = settings_counters['speedrun']

        self.volume_counter = settings_counters['music_volume']
        self.sounds_counter = settings_counters['sounds']

        self.controls['configuration'] = controls['configuration']
        self.cont_overlay_key = {
            controls['configuration'][1]: 'lb',
            controls['configuration'][2]: 'rb',
            controls['configuration'][3]: 'pause',
            0: 'a',
            1: 'b',
            2: 'x',
            13: 'b',
            14: 'a',
            15: 'x',
            (-1, 0): 'left',
            (1, 0): 'right',
            (0, -1): 'down',
            (0, 1): 'up',
        }
        self.nums_to_btns['configuration'] = controls['configuration']

    def controller_calibration_func(self, local_screen, events, fps_adjust, in_settings, joysticks):
        calibration_done = False
        configuration = []
        calibrated = False
        self.controller_calibration_counter += 0.04 * fps_adjust
        self.controller_calibration_button_counter += 1 * fps_adjust
        if self.choose_different_btn_counter > 0:
            self.choose_different_btn_counter -= 1 * fps_adjust

        if self.dim_surf_alpha <= self.dim_surf_target_alpha:
            self.dim_surf_alpha += 20 * fps_adjust
        if self.dim_surf_alpha < self.dim_surf_target_alpha:
            self.dim_surf.set_alpha(self.dim_surf_alpha)
        if self.dim_surf_alpha > self.dim_surf_target_alpha:
            self.dim_surf.set_alpha(self.dim_surf_target_alpha)

        if self.controller_calibration_step_counter == 0 and joysticks:
            hats = joysticks[0].get_numhats()
            if hats > 0:
                self.controller_calibration_step_counter = 1
                self.controller_configuration[self.controller_calibration_step_counter] = []

        # sequence: [(D-pad), rb, lb, pause, b, a, x, button naming]
        # D-pad sequence: [right, down, left, up]

        if events['joybuttondown'] and self.controller_calibration_counter > 0.25:
            event = events['joybuttondown']

            if self.controller_calibration_step_counter == 0 and event.button not in self.controller_taken_btns:
                self.calibrated_hat_btns.append(event.button)
                self.controller_taken_btns.append(event.button)

            if self.controller_calibration_step_counter == 7 and event.button == self.controller_configuration[5]:
                self.controller_configuration[self.controller_calibration_step_counter] = self.btn_names_counter
                self.controller_calibration_step_counter += 1

            elif 1 <= self.controller_calibration_step_counter <= 6:
                if event.button not in self.controller_taken_btns:
                    self.controller_configuration[self.controller_calibration_step_counter] = event.button
                    self.controller_taken_btns.append(event.button)
                    self.controller_calibration_step_counter += 1
                    print(self.controller_calibration_step_counter)
                else:
                    self.choose_different_btn_counter = 60

            if (event.button == self.controller_configuration[5] or event.button == self.controls['configuration'][5])\
                    and in_settings and self.controller_calibration_step_counter == 0:
                self.controller_calibration = False
                self.configuration_counter = 3
                self.controller_calibration_step_counter = 0
                self.controller_calibration_counter = 0
                self.calibrated_hat_btns = []
                self.controller_configuration = [[], -1, -1, -1, -1, -1, -1, -1]
                self.controller_taken_btns = []
                calibrated = False
                self.dim_surf_alpha = 0
                self.dim_surf.set_alpha(self.dim_surf_alpha)

        if events['joydeviceremoved']:
            self.controller_calibration = False
            self.configuration_counter = 3
            self.controller_calibration_step_counter = 0
            self.controller_calibration_counter = 0
            self.calibrated_hat_btns = []
            self.controller_configuration = [[], -1, -1, -1, -1, -1, -1, -1]
            self.controller_taken_btns = []
            calibrated = False
            self.dim_surf_alpha = 0
            self.dim_surf.set_alpha(self.dim_surf_alpha)

        if self.controller_calibration_step_counter == 8:
            self.controller_calibration = False
            self.calibrated_hat_btns = []
            self.controller_calibration_step_counter = 0
            self.controller_calibration_counter = 0
            self.configuration_counter = self.btn_names_counter
            self.nums_to_btns['configuration'] = self.controller_configuration
            self.controls['configuration'] = self.controller_configuration
            configuration = self.controller_configuration
            self.controller_configuration = [[], -1, -1, -1, -1, -1, -1, -1]
            self.controller_taken_btns = []
            calibration_done = True
            self.dim_surf_alpha = 0
            self.dim_surf.set_alpha(self.dim_surf_alpha)
            calibrated = True

        if self.controller_calibration_step_counter == 0:
            raw_popup = self.controller_conf_popup0
        elif self.controller_calibration_step_counter == 1:
            raw_popup = self.controller_conf_popup1
        elif self.controller_calibration_step_counter == 2:
            raw_popup = self.controller_conf_popup2
        elif self.controller_calibration_step_counter == 3:
            raw_popup = self.controller_conf_popup3
        elif self.controller_calibration_step_counter == 4:
            raw_popup = self.controller_conf_popup4
        elif self.controller_calibration_step_counter == 5:
            raw_popup = self.controller_conf_popup5
        elif self.controller_calibration_step_counter == 6:
            raw_popup = self.controller_conf_popup6
        else:
            raw_popup = self.controller_conf_popup7

        # button animation counter cap
        if self.controller_calibration_button_counter > 50:
            self.controller_calibration_button_counter = 0

        if 0 < self.controller_calibration_step_counter <= 2:
            if self.controller_calibration_button_counter > 40:
                btn_img = self.bumpers[f'{self.controller_calibration_step_counter}_2']
            else:
                btn_img = self.bumpers[f'{self.controller_calibration_step_counter}_1']
            self.controller_calibration_btn_surf.fill((79, 70, 81))
            self.controller_calibration_btn_surf.blit(btn_img, (0, 0))
            raw_popup.blit(self.controller_calibration_btn_surf, (raw_popup.get_width() / 2 - btn_img.get_width() / 2,
                                                        raw_popup.get_height() / 2 - btn_img.get_height() / 2 + 10))

        if self.controller_calibration_step_counter == 0:
            if self.controller_calibration_button_counter > 30 and len(self.calibrated_hat_btns) < 4:
                hat_img = self.controller_hat_imgs[len(self.calibrated_hat_btns) + 1]
            else:
                hat_img = self.controller_hat_imgs[0]
            self.controller_hat_animation_surf.fill((79, 70, 81))
            self.controller_hat_animation_surf.blit(hat_img, (0, 0))
            raw_popup.blit(self.controller_hat_animation_surf, (raw_popup.get_width() / 2 - 16,
                                                                raw_popup.get_height() / 2 - 12))

        if self.controller_calibration_step_counter == 7:
            hat_value = [0, 0]
            # D-pad input
            if joysticks and joysticks[0].get_numhats() > 0:
                hat_value = joysticks[0].get_hat(0)
            if events['joyhatdown']:
                event = events['joyhatdown']
                if self.controller_configuration[0]:
                    if event.button == self.controller_configuration[0][0]:  # right
                        hat_value[0] = 1
                    if event.button == self.controller_configuration[0][2]:  # left
                        hat_value[0] = -1

            if hat_value[0] != 0 and not self.hat_x_pressed:
                self.hat_x_pressed = True
                if self.btn_names_counter == 1:
                    self.btn_names_counter = 2
                else:
                    self.btn_names_counter = 1
            if hat_value[0] == 0:
                self.hat_x_pressed = False

            if events['joyaxismotion_x']:
                event = events['joyaxismotion_x']
                if not self.calib_joystick_moved and abs(event.value) > 0.3:
                    if self.btn_names_counter == 1:
                        self.btn_names_counter = 2
                    else:
                        self.btn_names_counter = 1
                    self.calib_joystick_moved = True
                if abs(event.value) < 0.05:
                    self.calib_joystick_moved = False

            joystick_over_btn1 = False
            joystick_over_btn2 = False
            if self.btn_names_counter == 1:
                joystick_over_btn1 = True
            if self.btn_names_counter == 2:
                joystick_over_btn2 = True
            use_btn = [self.controller_configuration[5]]
            self.btn_names_button1.draw_button(raw_popup, False, [1, 0, 0], events, joystick_over_btn1, use_btn)
            self.btn_names_button2.draw_button(raw_popup, False, [1, 0, 0], events, joystick_over_btn2, use_btn)

        if 0.25 > self.controller_calibration_counter > 0:
            scaling = self.controller_calibration_counter
            popup = pygame.transform.scale(raw_popup,
                                           (raw_popup.get_width() * scaling * 4,
                                            raw_popup.get_height() * scaling * 4))
        else:
            popup = raw_popup

        if in_settings and self.controller_calibration_step_counter == 0:
            popup.blit(self.cancel_surface, (popup.get_width() / 2 - self.cancel_surface.get_width() / 2,
                                             popup.get_height() - 25))

        local_screen.blit(self.dim_surf, (0, 0))
        local_screen.blit(popup, (swidth / 2 - popup.get_width() / 2, sheight / 2 - popup.get_height() / 2))

        if self.choose_different_btn_counter > 0 and 0 < self.controller_calibration_step_counter < 7:
            local_screen.blit(self.choose_different_btn_surf,
                              (swidth / 2 - self.choose_different_btn_surf.get_width() / 2,
                               sheight / 2 - 8))

        if len(self.calibrated_hat_btns) == 4 and self.controller_calibration_step_counter == 0:
            self.controller_configuration[self.controller_calibration_step_counter] = self.calibrated_hat_btns
            self.calibrated_hat_btns = []
            self.controller_calibration_step_counter += 1

        return configuration, calibration_done, calibrated

        # --------------------------------------------------------------------------------------------------------------
    def draw_settings_menu(self, settings_screen, mouse_adjustment, events, fps_adjust, joystick_connected, joysticks,
                           game_paused):
        settings_screen.fill((0, 0, 0))
        settings_screen.blit(self.menu_background, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0]/mouse_adjustment[0] - mouse_adjustment[2],
                     mouse_pos[1]/mouse_adjustment[0] - mouse_adjustment[1])

        joystick_counter_cap = 0
        if not self.draw_control_screen:
            joystick_counter_cap = 4
        if not self.draw_visual_screen:
            joystick_counter_cap = 4
        if not self.draw_sound_screen:
            joystick_counter_cap = 2

        joystick_tab_left = False
        joystick_tab_right = False

        prev_joystick_counter = self.joystick_counter

        use_btn = self.controls['configuration'][5]

        joystick_moved = 0

        if not self.controller_calibration:
            # axis input
            if events['joyaxismotion_x'] or events['joyaxismotion_y']:
                # horizontal joystick movement
                if events['joyaxismotion_x']:
                    event = events['joyaxismotion_x']
                    self.joystick_movement[0] = event.value
                    if abs(event.value) > 0.7 and not self.joystick_moved:
                        self.joystick_counter = self.joystick_counter * -1
                        self.joystick_moved = True
                    if abs(event.value) < 0.02:
                        self.joystick_moved = False
                    if joystick_moved:
                        self.pov_popup_counter = 0
                # vertical joystick movement
                if events['joyaxismotion_y']:
                    event = events['joyaxismotion_y']
                    self.joystick_movement[1] = event.value
                    # down
                    if event.value > 0.7 and not self.joystick_moved:
                        if self.joystick_counter >= 0:
                            self.joystick_counter -= 1
                            if self.joystick_counter < 0:
                                self.joystick_counter = 0
                        if self.joystick_counter < 0:
                            self.joystick_counter += 1
                            if self.joystick_counter > 0:
                                self.joystick_counter = 0
                        self.joystick_moved = True
                        joystick_moved = -1
                    # up
                    if event.value < -0.7 and not self.joystick_moved:
                        if self.joystick_counter >= 0:
                            self.joystick_counter += 1
                            if self.joystick_counter > joystick_counter_cap:
                                self.joystick_counter = 0
                        if self.joystick_counter < 0:
                            self.joystick_counter -= 1
                            if self.joystick_counter < -joystick_counter_cap:
                                self.joystick_counter = 0
                        self.joystick_moved = True
                        joystick_moved = 1
                    if abs(event.value) < 0.02:
                        self.joystick_moved = False
                    if joystick_moved:
                        self.pov_popup_counter = 0

            if events['joybuttondown']:
                event = events['joybuttondown']
                self.no_controller_counter = 0
                self.pov_popup_counter = 0
                # bumper input
                if event.button == self.controls['configuration'][1]:
                    joystick_tab_left = True
                if event.button == self.controls['configuration'][2]:
                    joystick_tab_right = True
                # controller press visualization buttons (down)
                try:
                    key = self.cont_overlay_key[event.button]
                    self.controller_presses[key][0] = True
                except KeyError:
                    pass
            if events['joyhatdown']:
                event = events['joyhatdown']
                # hat input
                if event.button == self.controls['configuration'][0][0]:  # right
                    self.hat_value[0] = 1
                if event.button == self.controls['configuration'][0][1]:  # down
                    self.hat_value[1] = -1
                if event.button == self.controls['configuration'][0][2]:  # left
                    self.hat_value[0] = -1
                if event.button == self.controls['configuration'][0][3]:  # up
                    self.hat_value[1] = 1
            if events['joybuttonup']:
                event = events['joybuttonup']
                # controller press visualization buttons (up)
                try:
                    key = self.cont_overlay_key[event.button]
                    self.controller_presses[key][0] = False
                except KeyError:
                    pass
            if events['joyhatup']:
                # hat up input
                event = events['joyhatup']
                if event.button in [self.controls['configuration'][0][0], self.controls['configuration'][0][2]]:
                    self.hat_value[0] = 0
                if event.button in [self.controls['configuration'][0][1], self.controls['configuration'][0][3]]:
                    self.hat_value[1] = 0
            if events['mousebuttondown'] or events['keydown']:
                self.no_controller_counter = 0
                self.pov_popup_counter = 0

            # D-pad input
            if joysticks and joysticks[0].get_numhats() > 0:
                self.hat_value = joysticks[0].get_hat(0)

            # controller press visualization D-pad management
            self.controller_presses['left'][0] = False
            self.controller_presses['right'][0] = False
            self.controller_presses['up'][0] = False
            self.controller_presses['down'][0] = False
            if self.hat_value[0] == -1:
                self.controller_presses['left'][0] = True
            if self.hat_value[0] == 1:
                self.controller_presses['right'][0] = True
            if self.hat_value[1] == -1:
                self.controller_presses['down'][0] = True
            if self.hat_value[1] == 1:
                self.controller_presses['up'][0] = True

            if not self.hat_x_pressed:
                if abs(self.hat_value[0]) == 1:
                    self.joystick_counter = self.joystick_counter * -1
                    self.hat_x_pressed = True
            if not self.hat_y_pressed:
                # down
                if self.hat_value[1] == -1:
                    if self.joystick_counter >= 0:
                        self.joystick_counter -= 1
                        if self.joystick_counter < 0:
                            self.joystick_counter = 0
                        self.joystick_moved = True
                    if self.joystick_counter < 0:
                        self.joystick_counter += 1
                        if self.joystick_counter > 0:
                            self.joystick_counter = 0
                    joystick_moved = -1
                    self.hat_y_pressed = True
                # up
                if self.hat_value[1] == 1:
                    if self.joystick_counter >= 0:
                        self.joystick_counter += 1
                        if self.joystick_counter > joystick_counter_cap:
                            self.joystick_counter = 0
                        self.joystick_moved = True
                    if self.joystick_counter < 0:
                        self.joystick_counter -= 1
                        if self.joystick_counter < -joystick_counter_cap:
                            self.joystick_counter = 0
                    joystick_moved = 1
                    self.hat_y_pressed = True
            # if not pressed
            if self.hat_value[0] == 0:
                self.hat_x_pressed = False
            if self.hat_value[1] == 0:
                self.hat_y_pressed = False
                    
        if self.joystick_counter > joystick_counter_cap:
            self.joystick_counter = joystick_counter_cap
        if self.joystick_counter < -joystick_counter_cap:
            self.joystick_counter = -joystick_counter_cap

        joystick_over0 = False
        joystick_over1 = False
        joystick_over2 = False
        joystick_over3 = False
        joystick_over4 = False
        joystick_over_1 = False
        joystick_over_2 = False
        joystick_over_3 = False
        joystick_over_4 = False

        if joystick_connected and not self.controller_calibration:
            if self.joystick_counter == 0:
                joystick_over0 = True
            if self.joystick_counter == 1:
                joystick_over1 = True
            if self.joystick_counter == 2:
                joystick_over2 = True
            if self.joystick_counter == 3:
                joystick_over3 = True
            if self.joystick_counter == 4:
                joystick_over4 = True
            if self.joystick_counter == -1:
                joystick_over_1 = True
            if self.joystick_counter == -2:
                joystick_over_2 = True
            if self.joystick_counter == -3:
                joystick_over_3 = True
            if self.joystick_counter == -4:
                joystick_over_4 = True

        self.control_screen.blit(self.menu_background, (0, 20))
        self.sound_screen.blit(self.menu_background, (0, 20))
        self.visual_screen.blit(self.menu_background, (0, 20))

        walking_left_press = False
        walking_right_press = False
        jumping_left_press = False
        jumping_right_press = False
        rumble_left_press = False
        rumble_right_press = False
        config_left_press = False
        config_right_press = False

        res_left_press = False
        res_right_press = False
        pov_left_press = False
        pov_right_press = False
        hit_left_press = False
        hit_right_press = False
        speedrun_left_press = False
        speedrun_right_press = False

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

        calibrated = False

        control_box1_over = False
        control_box2_over = False
        control_box3_over = False
        control_box4_over = False

        control_btn_trigger = False
        visual_btn_trigger = False
        sound_btn_trigger = False

        self.keyboard_highlight_counter += 1 * fps_adjust
        self.no_controller_counter -= 1 * fps_adjust
        self.pov_popup_counter -= 1 * fps_adjust

        if prev_joystick_counter != self.joystick_counter:
            self.arrow_button_outline_alpha = 0
            prev_joystick_counter = self.joystick_counter

        if self.arrow_button_outline_alpha * 40 < 255:
            self.arrow_button_outline_alpha += 1
            self.arrow_button_outline_surf.set_alpha(self.arrow_button_outline_alpha * 40)

        # drawing and updating the menu/back button --------------------------------------------------------------------
        menu_press, over = self.menu_btn.draw_button(settings_screen, False, mouse_adjustment, events, joystick_over0,
                                                     use_btn)

        button_text_center = self.center + 65

        # CONTROL SETTINGS SCREEN ======================================================================================

        if not self.draw_control_screen:
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

            if self.cards_counter == 1:
                cards_text = self.cards_conf1
            else:
                cards_text = self.cards_conf2

            # updating the text showing the player's current controls --------------------------------------------------
            self.control_screen.blit(self.walking_txt, (self.center - 10 - self.walking_txt.get_width(),
                                                        self.button_start_y + 7 + self.gap))
            self.control_screen.blit(self.jumping_txt, (self.center - 10 - self.jumping_txt.get_width(),
                                                        self.button_start_y + 7 + self.gap * 2))
            self.control_screen.blit(self.keyboard_cards, (self.center - 10 - self.keyboard_cards.get_width(),
                                                           self.button_start_y + 7 + self.gap * 3))
            self.control_screen.blit(self.configuration_txt, (self.center - 10 - self.configuration_txt.get_width(),
                                                        self.button_start_y + 7 + self.gap * 4))
            # keyboard controls visualisation --------------------------------------------------------------------------
            if self.walk_counter == 2 or self.jump_counter == 3:
                keyboard_x = swidth / 2 - tile_size
                mouse_x = swidth / 2 - tile_size * 2
            else:
                keyboard_x = swidth / 2 - tile_size * 1.8
                mouse_x = keyboard_x + tile_size * 3
            # mouse button presses
            if events['mousebuttondown']:
                if events['mousebuttondown'].button in [1, 3]:
                    self.mouse_current_press_overlay = self.mouse_press_overlays[events['mousebuttondown'].button]
                    self.mouse_press = True
            if events['mousebuttonup']:
                self.mouse_press = False

            try:
                if events['keydown']:
                    self.keyboard_presses[events['keydown'].key][0] = True
                if events['keyup']:
                    self.keyboard_presses[events['keyup'].key][0] = False
            except KeyError:
                pass

            self.control_screen.blit(self.kbr_bg, (swidth / 2 - 65, 165 / 270 * sheight))

            if not joystick_connected:
                self.control_screen.blit(self.keyboard_base, (keyboard_x,
                                                              (175 / 270 * sheight)))
                self.control_screen.blit(self.mouse_base, (mouse_x,(175 / 270 * sheight)))
                self.control_screen.blit(self.keyboard_overlays[f'walk{self.walk_counter}'],
                                         (keyboard_x, (175 / 270 * sheight)))
                self.control_screen.blit(self.keyboard_overlays[f'jump{self.jump_counter}'],
                                         (keyboard_x, (175 / 270 * sheight)))

                if self.cards_counter == 2:
                    self.control_screen.blit(self.keyboard_overlays['keybrd_cards'],
                                             (keyboard_x, (175 / 270 * sheight)))
                else:
                    self.control_screen.blit(self.keyboard_overlays['mouse_cards'],
                                             (mouse_x, (175 / 270 * sheight)))
                    if self.mouse_press:
                        self.control_screen.blit(self.mouse_current_press_overlay, (mouse_x, (175 / 270 * sheight)))

                self.keyboard_press_surf.fill((255, 255, 255))
                for key in self.keyboard_presses:
                    pressed_key = self.keyboard_presses[key]
                    if pressed_key[0]:
                        self.keyboard_press_surf.blit(pressed_key[2], pressed_key[1])
                self.control_screen.blit(self.keyboard_press_surf, (keyboard_x, (175 / 270 * sheight)))

            else:
                self.control_screen.blit(self.controller, (swidth / 2 - tile_size, (175 / 270 * sheight)))
                for key in self.controller_presses:
                    if self.controller_presses[key][0]:
                        self.control_screen.blit(self.controller_presses[key][1],
                                                 (swidth / 2 - tile_size, (175 / 270 * sheight)))
                if self.joystick_movement != [0, 0]:
                    pygame.draw.circle(self.control_screen, (0, 0, 0),
                                       (swidth / 2 - tile_size + 20 + self.joystick_movement[0] * 3
                                        , 175 / 270 * sheight + 10 + self.joystick_movement[1] * 3), 2, 2)

            # displaying the selected option (text) --------------------------------------------------------------------
            self.control_screen.blit(walk_text, (button_text_center - walk_text.get_width() / 2 + button_size / 2,
                                                 self.control_row1_y + 7))
            self.control_screen.blit(jump_text, (button_text_center - jump_text.get_width() / 2 + button_size / 2,
                                                 self.control_row2_y + 7))
            self.control_screen.blit(cards_text, (button_text_center - cards_text.get_width() / 2 + button_size / 2,
                                                   self.control_row3_y + 7))

            if self.walk_counter > 1:
                walking_left_press, over1 = self.walking_btn_left.draw_button(self.control_screen,
                                                                              False, mouse_adjustment, events,
                                                                              joystick_over4, use_btn)
            else:
                self.control_screen.blit(self.left_button_gray, (self.left_btn_x, self.control_row1_y))
                if joystick_over4:
                    self.control_screen.blit(self.arrow_button_outline_surf, (self.left_btn_x, self.control_row1_y))

            if self.walk_counter < 2:
                walking_right_press, over2 = self.walking_btn_right.draw_button(self.control_screen,
                                                                                False, mouse_adjustment, events,
                                                                                joystick_over_4, use_btn)
            else:
                self.control_screen.blit(self.right_button_gray, (self.right_btn_x, self.control_row1_y))
                if joystick_over_4:
                    self.control_screen.blit(self.arrow_button_outline_surf, (self.right_btn_x, self.control_row1_y))

            if self.jump_counter > 1:
                jumping_left_press, over3 = self.jumping_btn_left.draw_button(self.control_screen,
                                                                              False, mouse_adjustment, events,
                                                                              joystick_over3, use_btn)
            else:
                self.control_screen.blit(self.left_button_gray, (self.left_btn_x, self.control_row2_y))
                if joystick_over3:
                    self.control_screen.blit(self.arrow_button_outline_surf, (self.left_btn_x, self.control_row2_y))

            if self.jump_counter < 3:
                jumping_right_press, over4 = self.jumping_btn_right.draw_button(self.control_screen,
                                                                                False, mouse_adjustment, events,
                                                                                joystick_over_3, use_btn)
            else:
                self.control_screen.blit(self.right_button_gray, (self.right_btn_x, self.control_row2_y))
                if joystick_over_3:
                    self.control_screen.blit(self.arrow_button_outline_surf, (self.right_btn_x, self.control_row2_y))

            if self.cards_counter > 1:
                rumble_left_press, over5 = self.rumble_btn_left.draw_button(self.control_screen,
                                                                            False, mouse_adjustment, events,
                                                                            joystick_over2, use_btn)
            else:
                self.control_screen.blit(self.left_button_gray, (self.left_btn_x, self.control_row3_y))
                if joystick_over2:
                    self.control_screen.blit(self.arrow_button_outline_surf, (self.left_btn_x, self.control_row3_y))

            if self.cards_counter < 2:
                rumble_right_press, over6 = self.rumble_btn_right.draw_button(self.control_screen,
                                                                              False, mouse_adjustment, events,
                                                                              joystick_over_2, use_btn)
            else:
                self.control_screen.blit(self.right_button_gray, (self.right_btn_x, self.control_row3_y))
                if joystick_over_2:
                    self.control_screen.blit(self.arrow_button_outline_surf, (self.right_btn_x, self.control_row3_y))

            if joystick_over1 or joystick_over_1:
                config_over = True
            else:
                config_over = False

            if not self.controller_calibration:
                calib_press, over5 = self.calibration_btn.draw_button(self.control_screen, False, mouse_adjustment,
                                                                      events, config_over, use_btn)
            else:
                calib_press = False

            if self.keyboard_control_box1.collidepoint(mouse_pos):
                control_box1_over = True

            if self.keyboard_control_box2.collidepoint(mouse_pos):
                control_box2_over = True

            if self.keyboard_control_box3.collidepoint(mouse_pos):
                control_box3_over = True

            # controller calibration trigger
            if calib_press and joystick_connected:
                self.controller_calibration = True
            if calib_press and not joystick_connected:
                self.no_controller_counter = 75

            if control_box1_over:
                self.keyboard_overlays[f'walk{self.walk_counter}'].set_alpha(255)
                self.keyboard_overlays[f'jump{self.jump_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_overlays['keybrd_cards'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_overlays['mouse_cards'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_highlight_off = False

            elif control_box2_over:
                self.keyboard_overlays[f'walk{self.walk_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_overlays[f'jump{self.jump_counter}'].set_alpha(255)
                self.keyboard_overlays['keybrd_cards'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_overlays['mouse_cards'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_highlight_off = False

            elif control_box3_over:
                self.keyboard_overlays[f'walk{self.walk_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_overlays[f'jump{self.jump_counter}'].set_alpha(self.keyboard_bg_alpha)
                self.keyboard_overlays['keybrd_cards'].set_alpha(255)
                self.keyboard_overlays['mouse_cards'].set_alpha(255)
                self.keyboard_highlight_off = False

            elif not self.keyboard_highlight_off:
                self.keyboard_overlays[f'walk{self.walk_counter}'].set_alpha(255)
                self.keyboard_overlays[f'jump{self.jump_counter}'].set_alpha(255)
                self.keyboard_overlays['keybrd_cards'].set_alpha(255)
                self.keyboard_overlays['mouse_cards'].set_alpha(255)
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

        if rumble_left_press and self.cards_counter > 1:
            self.cards_counter -= 1
        if rumble_right_press and self.cards_counter < 2:
            self.cards_counter += 1

        if config_left_press and self.configuration_counter > 1:
            self.configuration_counter -= 1
        if config_right_press and self.configuration_counter < 3:
            self.configuration_counter += 1

        # updating the controls dictionary -----------------------------------------------------------------------------
        if menu_press:
            self.controls['left'] = self.nums_to_btns[f'left{self.walk_counter}']
            self.controls['right'] = self.nums_to_btns[f'right{self.walk_counter}']
            self.controls['jump'] = self.nums_to_btns[f'jump{self.jump_counter}']
            self.controls['configuration'] = self.nums_to_btns['configuration']
            self.controls['rumble'] = self.nums_to_btns[f'rumble{self.cards_counter}']

        # VISUAL SETTINGS SCREEN =======================================================================================
        text_titles_y = round(40 / 270 * sheight)

        if not game_paused:
            speedrun_txt = self.speedrun_txt
            speedrun_conf1 = self.speedrun_conf1
            speedrun_conf2 = self.speedrun_conf2
        else:
            speedrun_txt = self.speedrun_txt_dim
            speedrun_conf1 = self.speedrun_conf1_dim
            speedrun_conf2 = self.speedrun_conf2_dim

        self.visual_screen.blit(self.resolution_txt,
                                (self.center - 10 - self.resolution_txt.get_width(),
                                 text_titles_y + self.gap))
        self.visual_screen.blit(self.pov_txt,
                                (self.center - 10 - self.pov_txt.get_width(),
                                 text_titles_y + self.gap * 2))
        self.visual_screen.blit(self.hitbox_txt,
                                (self.center - 10 - self.hitbox_txt.get_width(),
                                 text_titles_y + self.gap * 3))
        self.visual_screen.blit(speedrun_txt,
                                (self.center - 10 - self.speedrun_txt.get_width(),
                                 text_titles_y + self.gap * 4))
        if not self.speedrun_unlocked:
            self.visual_screen.blit(self.unlock_speedrun_txt,
                                    (self.center + 15, text_titles_y + self.gap * 4))

        if self.resolution_counter == 1:
            res_text = self.res_conf1
        elif self.resolution_counter == 2:
            res_text = self.res_conf2
        elif self.resolution_counter == 3:
            res_text = self.res_conf3
        else:
            res_text = self.res_conf4

        if self.pov_counter == 1:
            pov_text = self.pov_conf1
        else:
            pov_text = self.pov_conf2

        if self.hitbox_counter == 1:
            hit_text = self.hitbox_conf1
        else:
            hit_text = self.hitbox_conf2

        if self.speedrun_counter == 1:
            speedrun_text = speedrun_conf1
        else:
            speedrun_text = speedrun_conf2

        self.visual_screen.blit(res_text, (button_text_center - res_text.get_width() / 2 + button_size / 2,
                                           self.vis_sound_button_start_y + self.gap + 7))
        self.visual_screen.blit(pov_text, (button_text_center - pov_text.get_width() / 2 + button_size / 2,
                                            self.vis_sound_button_start_y + self.gap * 2 + 7))
        self.visual_screen.blit(hit_text, (button_text_center - hit_text.get_width() / 2 + button_size / 2,
                                           self.vis_sound_button_start_y + self.gap * 3 + 7))
        if self.speedrun_unlocked:
            self.visual_screen.blit(speedrun_text,
                                    (button_text_center - speedrun_text.get_width() / 2 + button_size / 2,
                                     self.vis_sound_button_start_y + self.gap * 4 + 7))

        if not self.draw_visual_screen:
            if self.resolution_counter > 1:
                res_left_press, over1 = self.resolution_btn_left.draw_button(self.visual_screen,
                                                                             False, mouse_adjustment, events,
                                                                             joystick_over4, use_btn)
            else:
                self.visual_screen.blit(self.left_button_gray, (self.left_btn_x, self.vis_sound_button_start_y + self.gap))
                if joystick_over4:
                    self.visual_screen.blit(self.arrow_button_outline_surf, (self.left_btn_x,
                                                                             self.vis_sound_button_start_y + self.gap))

            if self.resolution_counter < 4:
                res_right_press, over2 = self.resolution_btn_right.draw_button(self.visual_screen,
                                                                               False, mouse_adjustment, events,
                                                                               joystick_over_4, use_btn)
            else:
                self.visual_screen.blit(self.right_button_gray, (self.right_btn_x,
                                                                 self.vis_sound_button_start_y + self.gap))
                if joystick_over_4:
                    self.visual_screen.blit(self.arrow_button_outline_surf, (self.right_btn_x,
                                                                             self.vis_sound_button_start_y + self.gap))

            if self.pov_counter > 1:
                pov_left_press, over3 = self.performance_btn_left.draw_button(self.visual_screen,
                                                                              False, mouse_adjustment, events,
                                                                              joystick_over3, use_btn)
            else:
                self.visual_screen.blit(self.left_button_gray, (self.left_btn_x,
                                                                self.vis_sound_button_start_y + self.gap * 2))
                if joystick_over3:
                    self.visual_screen.blit(self.arrow_button_outline_surf,
                                            (self.left_btn_x, self.vis_sound_button_start_y + self.gap * 2))

            if self.pov_counter < 2:
                pov_right_press, over4 = self.performance_btn_right.draw_button(self.visual_screen,
                                                                                False, mouse_adjustment, events,
                                                                                joystick_over_3, use_btn)
            else:
                self.visual_screen.blit(self.right_button_gray, (self.right_btn_x,
                                                                 self.vis_sound_button_start_y + self.gap * 2))

                if joystick_over_3:
                    self.visual_screen.blit(self.arrow_button_outline_surf,
                                            (self.right_btn_x, self.vis_sound_button_start_y + self.gap * 2))

            if self.hitbox_counter > 1:
                hit_left_press, over5 = self.hitbox_btn_left.draw_button(self.visual_screen,
                                                                         False, mouse_adjustment, events,
                                                                         joystick_over2, use_btn)
            else:
                self.visual_screen.blit(self.left_button_gray, (self.left_btn_x,
                                                                self.vis_sound_button_start_y + self.gap * 3))

                if joystick_over2:
                    self.visual_screen.blit(self.arrow_button_outline_surf,
                                            (self.left_btn_x, self.vis_sound_button_start_y + self.gap * 3))

            if self.hitbox_counter < 2:
                hit_right_press, over6 = self.hitbox_btn_right.draw_button(self.visual_screen,
                                                                           False, mouse_adjustment, events,
                                                                           joystick_over_2, use_btn)
            else:
                self.visual_screen.blit(self.right_button_gray, (self.right_btn_x,
                                                                 self.vis_sound_button_start_y + self.gap * 3))

                if joystick_over_2:
                    self.visual_screen.blit(self.arrow_button_outline_surf,
                                            (self.right_btn_x, self.vis_sound_button_start_y + self.gap * 3))

            if game_paused:
                speedrun_gray_btn_img_left = self.left_button_gray_dim
                speedrun_gray_btn_img_right = self.right_button_gray_dim
            else:
                speedrun_gray_btn_img_left = self.left_button_gray
                speedrun_gray_btn_img_right = self.right_button_gray

            if self.speedrun_unlocked:
                if self.speedrun_counter > 1 and not game_paused:
                    speedrun_left_press, over7 = self.speedrun_btn_left.draw_button(self.visual_screen,
                                                                                    False, mouse_adjustment, events,
                                                                                    joystick_over1, use_btn)
                else:
                    self.visual_screen.blit(speedrun_gray_btn_img_left, (self.left_btn_x,
                                                                    self.vis_sound_button_start_y + self.gap * 4))

                    if joystick_over1:
                        if game_paused:
                            if joystick_moved == -1:
                                self.joystick_counter -= 1
                            elif joystick_moved == 1:
                                self.joystick_counter += 1
                        else:
                            self.visual_screen.blit(self.arrow_button_outline_surf,
                                                    (self.left_btn_x, self.vis_sound_button_start_y + self.gap * 4))

                if self.speedrun_counter < 2 and not game_paused:
                    speedrun_right_press, over8 = self.speedrun_btn_right.draw_button(self.visual_screen,
                                                                                      False, mouse_adjustment, events,
                                                                                      joystick_over_1, use_btn)
                else:
                    self.visual_screen.blit(speedrun_gray_btn_img_right, (self.right_btn_x,
                                                                     self.vis_sound_button_start_y + self.gap * 4))

                    if joystick_over_1:
                        if game_paused:
                            if joystick_moved == -1:
                                self.joystick_counter += 1
                            elif joystick_moved == 1:
                                self.joystick_counter -= 1
                        else:
                            self.visual_screen.blit(self.arrow_button_outline_surf,
                                                    (self.right_btn_x, self.vis_sound_button_start_y + self.gap * 4))
            else:
                if self.joystick_counter > 0:
                    if joystick_moved == -1:
                        self.joystick_counter -= 1
                    elif joystick_moved == 1:
                        self.joystick_counter += 1
                elif self.joystick_counter < 0:
                    if joystick_moved == -1:
                        self.joystick_counter += 1
                    elif joystick_moved == 1:
                        self.joystick_counter -= 1

        if res_left_press and self.resolution_counter > 1:
            self.resolution_counter -= 1
        if res_right_press and self.resolution_counter < 4:
            self.resolution_counter += 1

        if pov_left_press and self.pov_counter > 1:
            self.pov_counter -= 1
        if pov_right_press and self.pov_counter < 2:
            self.pov_counter += 1

        if hit_left_press and self.hitbox_counter > 1:
            self.hitbox_counter -= 1
        if hit_right_press and self.hitbox_counter < 2:
            self.hitbox_counter += 1

        if speedrun_left_press and self.speedrun_counter > 1:
            self.speedrun_counter -= 1
        if speedrun_right_press and self.speedrun_counter < 2:
            self.speedrun_counter += 1

        # pov popup trigger
        if pov_left_press or pov_right_press:
            self.pov_popup_counter = 140

        # SOUND SETTINGS SCREEN ========================================================================================
        text_titles_y = round(40 / 270 * sheight)
        self.sound_screen.blit(self.volume_txt,
                               (self.center - 10 - self.volume_txt.get_width(), text_titles_y + self.gap))
        self.sound_screen.blit(self.sound_effects_txt,
                               (self.center - 10 - self.sound_effects_txt.get_width(), text_titles_y + self.gap * 2))

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

        if self.speedrun_counter == 1:
            volume_cap = 3
        else:
            volume_cap = 2

        volume_over = False
        if self.volume_col_box.collidepoint(mouse_pos) and not joysticks:
            volume_over = True

        if not self.draw_sound_screen:
            if self.volume_counter > 1:
                vol_left_press, over1 = self.volume_btn_left.draw_button(self.sound_screen,
                                                                         False, mouse_adjustment, events,
                                                                         joystick_over2, use_btn)
            else:
                self.sound_screen.blit(self.left_button_gray,
                                       (self.left_btn_x, self.vis_sound_button_start_y + self.gap))
                if joystick_over2:
                    self.sound_screen.blit(self.arrow_button_outline_surf, (self.left_btn_x,
                                                                            self.vis_sound_button_start_y + self.gap))
            if self.volume_counter < volume_cap:
                vol_right_press, over2 = self.volume_btn_right.draw_button(self.sound_screen,
                                                                           False, mouse_adjustment, events,
                                                                           joystick_over_2, use_btn)
            else:
                self.sound_screen.blit(self.right_button_gray,
                                       (self.right_btn_x, self.vis_sound_button_start_y + self.gap))
                if joystick_over_2:
                    self.sound_screen.blit(self.arrow_button_outline_surf, (self.right_btn_x,
                                                                            self.vis_sound_button_start_y + self.gap))

            self.sound_screen.blit(vol_text, (button_text_center - vol_text.get_width() / 2 + button_size / 2,
                                              self.vis_sound_button_start_y + self.gap + 7))

            if self.sounds_counter > 1:
                sound_left_press, over3 = self.sounds_btn_left.draw_button(self.sound_screen,
                                                                           False, mouse_adjustment, events,
                                                                           joystick_over1, use_btn)
            else:
                self.sound_screen.blit(self.left_button_gray,
                                       (self.left_btn_x, self.vis_sound_button_start_y + self.gap * 2))
                if joystick_over1:
                    self.sound_screen.blit(self.arrow_button_outline_surf,
                                           (self.left_btn_x, self.vis_sound_button_start_y + self.gap * 2))
            if self.sounds_counter < 2:
                sound_right_press, over4 = self.sounds_btn_right.draw_button(self.sound_screen,
                                                                             False, mouse_adjustment, events,
                                                                             joystick_over_1, use_btn)
            else:
                self.sound_screen.blit(self.right_button_gray,
                                       (self.right_btn_x, self.vis_sound_button_start_y + self.gap * 2))
                if joystick_over_1:
                    self.sound_screen.blit(self.arrow_button_outline_surf,
                                           (self.right_btn_x, self.vis_sound_button_start_y + self.gap * 2))

            self.sound_screen.blit(sound_text, (button_text_center - sound_text.get_width() / 2 + button_size / 2,
                                              self.vis_sound_button_start_y + self.gap * 2 + 7))

        play_music = False
        fadeout_music = False
        change_volume = False
        real_volume = False

        if vol_left_press and self.volume_counter > 1:
            self.volume_counter -= 1
            if self.volume_counter == 2 and self.speedrun_counter == 1:
                change_volume = True
        if vol_right_press and self.volume_counter < volume_cap:
            self.volume_counter += 1
            if self.volume_counter == 3 and self.speedrun_counter == 1:
                change_volume = True
        if vol_right_press or vol_left_press:
            if self.volume_counter == 1:
                fadeout_music = True
            if self.volume_counter == 2 and not change_volume:
                play_music = True

        if (joystick_over2 or joystick_over_2 or volume_over) and not self.draw_sound_screen:
            real_volume = True

        # adjusts background music
        settings_music = {
            'play': play_music,
            'fadeout': fadeout_music,
            'volume': change_volume,
            'real_volume': real_volume
        }

        if sound_left_press and self.sounds_counter > 1:
            self.sounds_counter -= 1
        if sound_right_press and self.sounds_counter < 2:
            self.sounds_counter += 1

        # screen managing ==============================================================================================
        if not self.draw_control_screen:
            if self.screen_alpha_counter <= 255:
                self.control_screen.set_alpha(self.screen_alpha_counter)
            settings_screen.blit(self.control_screen, (0, 0))
        if not self.draw_visual_screen:
            if self.screen_alpha_counter <= 255:
                self.visual_screen.set_alpha(self.screen_alpha_counter)
            settings_screen.blit(self.visual_screen, (0, 0))
        if not self.draw_sound_screen:
            if self.screen_alpha_counter <= 255:
                self.sound_screen.set_alpha(self.screen_alpha_counter)
            settings_screen.blit(self.sound_screen, (0, 0))

        # setting screen transition ------------------------------------------------------------------------------------
        self.screen_alpha_counter += 16 * fps_adjust

        # managing the section buttons ---------------------------------------------------------------------------------
        x = 0
        button_width = 0
        if self.draw_control_screen:
            control_btn_trigger, not_over = self.control_btn.draw_button(settings_screen,
                                                                         False, mouse_adjustment, events, False, use_btn)
        else:
            settings_screen.blit(self.control_button_select,
                                 (0, 0))
            button_width = self.control_button_select.get_width()
            x = 0
        if self.draw_visual_screen:
            visual_btn_trigger, not_over = self.visual_btn.draw_button(settings_screen, False, mouse_adjustment,
                                                                       events, False, use_btn)
        else:
            settings_screen.blit(self.visual_button_select,
                                 (self.control_button_select.get_width(), 0))
            button_width = self.visual_button_select.get_width()
            x = self.visual_button_select.get_width()
        if self.draw_sound_screen:
            sound_btn_trigger, not_over = self.sound_btn.draw_button(settings_screen, False, mouse_adjustment,
                                                                     events, False, use_btn)
        else:
            settings_screen.blit(self.sound_button_select,
                                 (self.control_button_select.get_width() + self.visual_button_select.get_width(), 0))
            button_width = self.sound_button_select.get_width()
            x = self.visual_button_dark.get_width() + self.sound_button_select.get_width()

        if joystick_connected:
            settings_screen.blit(self.button_lb, (x + 10, 3))
            settings_screen.blit(self.button_rb, (x + button_width - 26, 3))

        if control_btn_trigger:
            self.section_counter = 0
            self.screen_alpha_counter = 0
        if visual_btn_trigger:
            self.section_counter = 1
            self.screen_alpha_counter = 0
        if sound_btn_trigger:
            self.section_counter = 2
            self.screen_alpha_counter = 0

        if joystick_tab_left:
            self.screen_alpha_counter = 0
            self.section_counter -= 1
            if self.section_counter < 0:
                self.section_counter = 2
        if joystick_tab_right:
            self.screen_alpha_counter = 0
            self.section_counter += 1
            if self.section_counter > 2:
                self.section_counter = 0

        if self.section_counter == 0:
            self.draw_control_screen = False
            self.draw_visual_screen = True
            self.draw_sound_screen = True
        if self.section_counter == 1:
            self.draw_control_screen = True
            self.draw_visual_screen = False
            self.draw_sound_screen = True
        if self.section_counter == 2:
            self.draw_control_screen = True
            self.draw_visual_screen = True
            self.draw_sound_screen = False

        # calibration window -------------------------------------------------------------------------------------------
        if self.controller_calibration:
            configuration, done, configured = SettingsMenu.controller_calibration_func(self,
                                                                                       settings_screen, events,
                                                                                       fps_adjust, True, joysticks)
            if done and configured:
                calibrated = True
                self.nums_to_btns['configuration'] = configuration

        # no controller detected popup
        if self.no_controller_counter > 0:
            settings_screen.blit(self.no_controller_popup,
                                 (swidth / 2 - self.no_controller_popup.get_width() / 2,
                                  sheight / 2 - self.no_controller_popup.get_height() / 2))
        # pov popup
        if self.pov_popup_counter > 0:
            settings_screen.blit(self.pov_popup,
                                 (swidth / 2 - self.pov_popup.get_width() / 2,
                                  sheight / 2 - self.pov_popup.get_height() / 2))
        # --------------------------------------------------------------------------------------------------------------

        if over or over1 or over3 or over5 or over7:
            final_over1 = True
        if over2 or over4 or over6 or over8:
            final_over2 = True

        if res_right_press or res_left_press:
            adjust_resolution = True
        else:
            adjust_resolution = False

        resolution = self.resolutions[str(self.resolution_counter)]

        self.settings_counters['walking'] = self.walk_counter
        self.settings_counters['jumping'] = self.jump_counter
        self.settings_counters['cards'] = self.cards_counter
        self.settings_counters['configuration'] = self.configuration_counter
        self.settings_counters['resolution'] = self.resolution_counter
        self.settings_counters['pov'] = self.pov_counter
        self.settings_counters['music_volume'] = self.volume_counter
        self.settings_counters['sounds'] = self.sounds_counter
        self.settings_counters['hitbox'] = self.hitbox_counter
        self.settings_counters['speedrun'] = self.speedrun_counter

        return menu_press, self.controls, self.pov_counter, resolution, \
               adjust_resolution, self.settings_counters, calibrated, settings_music
