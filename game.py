from world import World, tile_size
from player import Player
from levels import *
from button import *
from particles import Particles
from eq_management import eqManager
from image_loader import img_loader
from font_manager import Text
from popup_bg_generator import popup_bg_generator
from scroll_bar import ScrollBar
from screen_info import swidth, sheight
import json
import random
import math


particle_num = 12

level_dictionary = {
    "level1_1": level1_1,
    "level2_1": level2_1,
    "level3_1": level3_1,
    "level1_2": level1_2,
    "level2_2": level2_2,
    "level3_2": level3_2,
    "level4_2": level4_2,
    "level5_2": level5_2,
    "level6_2": level6_2,
    "level7_2": level7_2,
    "level8_2": level8_2,
    "level9_2": level9_2,
    "level1_3": level1_3,
    "level2_3": level2_3,
    "level3_3": level3_3,
    "level4_3": level4_3,
    "level5_3": level5_3
}

level_bg_dictionary = {
    "level1_1_bg": level1_1_bg,
    "level2_1_bg": level2_1_bg,
    "level3_1_bg": level3_1_bg,
    "level1_2_bg": level1_2_bg,
    "level2_2_bg": level2_2_bg,
    "level3_2_bg": level3_2_bg,
    "level4_2_bg": level4_2_bg,
    "level5_2_bg": level5_2_bg,
    "level6_2_bg": level6_2_bg,
    "level7_2_bg": level7_2_bg,
    "level8_2_bg": level8_2_bg,
    "level9_2_bg": level9_2_bg,
    "level1_3_bg": level1_3_bg,
    "level2_3_bg": level2_3_bg,
    "level3_3_bg": level3_3_bg,
    "level4_3_bg": level4_3_bg,
    "level5_3_bg": level5_3_bg,
}

level_pos_dictionary = {
    "level1_1": (4, -3),
    "level2_1": (5, -2),
    "level3_1": (5, -2),
    "level1_2": (2, -4),
    "level2_2": (5, -5),
    "level3_2": (2, -4),
    "level4_2": (2, -5),
    "level5_2": (5, -7),
    "level6_2": (4, 2),
    "level7_2": (5, -19),
    "level8_2": (5, -5),
    "level9_2": (5, -2),
    "level1_3": (3, 1),
    "level2_3": (3, -4),
    "level3_3": (-2, -5),
    "level4_3": (4, -4),
    "level5_3": (3, -4)
}

level_card_dictionary = {
    "level2_1": "mid-air_jump",
    "level2_3": "speed_dash"
}

world_ending_levels = {
    1: 3,
    2: 9,
    3: 7,
    4: 5
}


class Gradient:
    def __init__(self, width, height, position):
        self.step = 255 / height
        self.colour_image = img_loader('data/images/popup_bg.PNG', width, 1)
        self.stripe = pygame.Surface((width, 1))
        self.alpha = self.step
        self.y = 0
        self.height = height
        self.position = position

    def draw_gradient(self, screen):
        self.alpha = self.step
        self.y = 0
        for i in range(self.height):
            self.alpha += self.step
            self.stripe.set_alpha(self.alpha)
            self.stripe.blit(self.colour_image, (0, self.y))
            self.y += 1
            screen.blit(self.stripe, (self.position[0], self.position[1] + self.y))


class Dialogue:
    def __init__(self, input_text, text):
        self.text_letters = []
        self.text_pixel_len = 0
        for letter in input_text:
            img = text.make_text([letter])
            self.text_pixel_len += img.get_width()
            self.text_letters.append(img)

        self.down_arrow = img_loader('data/images/dialogue_arrow.PNG', 5, 3)

        self.frame_counter = 0
        self.letter_counter = -1
        self.letter_write_duration = 2
        self.done = False

        self.btn_press = False

        self.arrow_bob_counter = 0

    def display_dialogue(self, dialogue_surf, fps_adjust):
        self.frame_counter += 1 * fps_adjust
        self.arrow_bob_counter += 1 * fps_adjust
        sound = False
        if self.frame_counter > self.letter_write_duration:
            self.letter_counter += 1
            self.frame_counter = 0
            sound = True
        if self.btn_press:
            self.btn_press = False
            self.letter_counter = len(self.text_letters) - 1
        if self.letter_counter > len(self.text_letters) - 1:
            self.letter_counter = len(self.text_letters) - 1
            self.done = True
        if self.letter_counter >= 0:
            x = round(swidth / 2) - self.text_pixel_len / 2
            for letter in range(0, self.letter_counter + 1):
                img = self.text_letters[letter]
                dialogue_surf.blit(img, (x, 10))
                x += img.get_width()
        if self.done:
            arrow_y = dialogue_surf.get_height() - 5 + math.sin((1 / 10) * self.arrow_bob_counter) * 2
            dialogue_surf.blit(self.down_arrow, (swidth / 2 - 3, arrow_y))

        if self.done:
            sound = False

        return self.done, sound


class Game:
    def __init__(self, slow_computer, world_data, bg_data, controls, world_count, settings_counters,
                 joystick_connected):

        self.world_data = world_data
        self.bg_data = bg_data

        self.game_screen = pygame.Surface((swidth, sheight))
        self.game_screen.set_colorkey((0, 0, 255))

        self.cave_background_colour = (35, 29, 39)
        self.sky_background_colour = (100, 63, 102)
        self.bg_transition_colour = [0, 0, 0]

        text = Text()

        # loading in images --------------------------------------------------------------------------------------------
        home_button_img = img_loader('data/images/button_pause.PNG', tile_size * 0.75, tile_size * 0.75)
        home_button_press = img_loader('data/images/button_pause_press.PNG', tile_size * 0.75, tile_size * 0.75)
        home_button_down = img_loader('data/images/button_pause_down.PNG', tile_size * 0.75, tile_size * 0.75)

        ok_button_img = img_loader('data/images/button_ok.PNG', tile_size, tile_size * 0.75)
        ok_button_press = img_loader('data/images/button_ok_press.PNG', tile_size, tile_size * 0.75)
        ok_button_down = img_loader('data/images/button_ok_down.PNG', tile_size, tile_size * 0.75)

        self.a_button_img = img_loader('data/images/buttons/button_a.PNG', tile_size / 2, tile_size / 2)
        self.cross_button_img = img_loader('data/images/buttons/button_cross.PNG', tile_size / 2, tile_size / 2)

        self.space_button_img = img_loader('data/images/buttons/key_space.PNG', tile_size, tile_size / 2)
        self.space_button_press = img_loader('data/images/buttons/key_space_press.PNG', tile_size, tile_size / 2)

        # buttons ------------------------------------------------------------------------------------------------------
        self.home_button = Button(swidth - tile_size + (tile_size - home_button_down.get_width()) / 2, 3,
                                  home_button_img, home_button_press, home_button_down)

        # POPUP WINDOWS ================================================================================================

        # controls popup window
        if world_count == 1:
            self.popup_window_controls = True
        else:
            self.popup_window_controls = False

        self.nums_to_text = {
            'walk1': 'A and D',
            'walk2': 'arrow keys',
            'jump1': 'space',
            'jump2': 'W',
            'jump3': 'up key',
        }

        walk_counter = settings_counters['walking']
        jump_counter = settings_counters['jumping']
        configuration_counter = controls['configuration'][4]
        if configuration_counter == 1:
            self.controller_type = 'xbox'
            jump_btn = 'A'
        elif configuration_counter == 2:
            self.controller_type = 'ps4'
            jump_btn = 'Cross'
        else:
            self.controller_type = 'other'
            jump_btn = 'A or cross'

        controls_text = {}

        if world_count == 1:
            controls_text[1] = text.make_text(['CONTROLS'])
            if not joystick_connected:
                controls_text[2] = text.make_text([f"walking: {self.nums_to_text[f'walk{walk_counter}']}"])
                controls_text[3] = text.make_text([f"jumping: {self.nums_to_text[f'jump{jump_counter}']}"])
                controls_text[4] = text.make_text(['cards: mouse'])
            else:
                controls_text[2] = text.make_text(['walking: Left stick or D-pad'])
                controls_text[3] = text.make_text([f'jumping: {jump_btn} button'])
                controls_text[4] = text.make_text(['cards: RB and LB'])

            instructions = {
                1: text.make_text(['Follow the compass in the top-left corner,']),
                2: text.make_text(['it will lead you to portals.']),
                3: text.make_text(['Use cards to gain special abilities.']),
                4: text.make_text(['Collect gems to use cards.'])
            }
            instruction_width = instructions[1].get_width()
        else:
            instructions = {}
            instruction_width = 1

        self.controls_popup_text_surface = pygame.Surface((instruction_width + 6, 180)).convert_alpha()
        self.controls_popup_text_space = pygame.Surface((instruction_width + 6, 115)).convert_alpha()
        self.popup_bg_colour = (79, 70, 81)
        self.controls_popup_text_space.fill(self.popup_bg_colour)
        self.controls_popup_text_surface.set_colorkey((0, 0, 0))

        self.controls_popup_gradient = Gradient(instruction_width + 10, 15, (1, 101))

        self.controls_popup = popup_bg_generator((instruction_width + 6, 140))
        self.clean_popup = self.controls_popup
        cont_bg_center = self.controls_popup.get_width() / 2

        self.ok_controls_btn = Button(swidth / 2 - ok_button_img.get_width() / 2,
                                      sheight / 2 + self.controls_popup.get_height() / 2 - tile_size * 0.75 - 3,
                                      ok_button_img, ok_button_press, ok_button_down)

        if world_count == 1:
            self.controls_popup_text_surface.blit(controls_text[1],
                                                  (cont_bg_center - controls_text[1].get_width() / 2, 6))
            self.controls_popup_text_surface.blit(controls_text[2],
                                                  (cont_bg_center - controls_text[2].get_width() / 2, 30))
            self.controls_popup_text_surface.blit(controls_text[3],
                                                  (cont_bg_center - controls_text[3].get_width() / 2, 45))
            self.controls_popup_text_surface.blit(controls_text[4],
                                                  (cont_bg_center - controls_text[4].get_width() / 2, 60))

            self.controls_popup_text_surface.blit(instructions[1],
                                                  (cont_bg_center - instructions[1].get_width() / 2, 90))
            self.controls_popup_text_surface.blit(instructions[2],
                                                  (cont_bg_center - instructions[2].get_width() / 2, 105))
            self.controls_popup_text_surface.blit(instructions[3],
                                                  (cont_bg_center - instructions[3].get_width() / 2, 120))
            self.controls_popup_text_surface.blit(instructions[4],
                                                  (cont_bg_center - instructions[4].get_width() / 2, 135))

            self.controls_popup_text_space.blit(self.controls_popup_text_surface, (0, 0))
            self.controls_popup.blit(self.controls_popup_text_space, (2, 1))

            self.controls_popup.blit(ok_button_down, (cont_bg_center - ok_button_img.get_width() / 2,
                                                      self.controls_popup.get_height() - tile_size * 0.75 - 3))

        # INSTRUCTION POPUPS -------------------------------------------------------------------------------------------
        popup = popup_bg_generator((220, 150))
        self.banners = {}

        # bees popup window
        self.bees_popup = popup.copy()

        self.banner_final_y = sheight / 2 - 52
        self.bee_banner_y_counter = sheight - self.banner_final_y
        self.bee_banner_y = sheight
        self.bee_banner_x = swidth / 2 - 100

        banner_center = self.bees_popup.get_width() / 2

        self.ok_bee_btn = Button(swidth / 2 - ok_button_img.get_width() / 2,
                                 sheight / 2 + self.bees_popup.get_height() / 2 - tile_size * 0.75 - 3,
                                 ok_button_img, ok_button_press, ok_button_down)
        if world_count == 2:
            self.banners['bee'] = img_loader('data/images/banner_shockwave.PNG', 200, 100)
            bees_txt = text.make_text(['BEEWARE!'])
            self.bees_popup.blit(bees_txt, (banner_center - bees_txt.get_width() / 2, 6))

        # dash popup window
        self.dash_popup = popup.copy()

        self.dash_banner_y_counter = sheight - self.banner_final_y
        self.dash_banner_y = sheight
        self.dash_banner_x = swidth / 2 - 100

        self.ok_dash_btn = Button(swidth / 2 - ok_button_img.get_width() / 2,
                                  sheight / 2 + self.dash_popup.get_height() / 2 - tile_size * 0.75 - 3,
                                  ok_button_img, ok_button_press, ok_button_down)
        if world_count == 3:
            self.banners['dash'] = img_loader('data/images/banner_dash.PNG', 200, 100)
            dash_txt = text.make_text(['DASH CHAIN'])
            self.dash_popup.blit(dash_txt, (banner_center - dash_txt.get_width() / 2, 6))

        # NEW CARD POPUP -----------------------------------------------------------------------------------------------
        new_card_txt = text.make_text(['NEW CARD UNLOCKED'])

        self.new_card_popup = popup_bg_generator((180, 130))
        self.ok_new_card_button = Button(swidth / 2 - ok_button_img.get_width() / 2,
                                         sheight / 2 + self.new_card_popup.get_height() / 2 - tile_size * 0.75 - 3,
                                         ok_button_img, ok_button_press, ok_button_down)

        self.new_card_popup.blit(new_card_txt,
                                 (self.new_card_popup.get_width() / 2 - new_card_txt.get_width() / 2, 6))
        self.new_card_popup.blit(ok_button_down,
                                 (self.new_card_popup.get_width() / 2 - ok_button_img.get_width() / 2,
                                  self.new_card_popup.get_height() - tile_size * 0.75 - 3))

        # lists --------------------------------------------------------------------------------------------------------
        self.eq_power_list = []

        try:
            with open('data/collected_cards.json', 'r') as json_file:
                self.eq_power_list = json.load(json_file)

        except FileNotFoundError:
            self.eq_power_list = []
            if world_count >= 2:
                self.eq_power_list = ["mid-air_jump"]
            if world_count >= 3:
                self.eq_power_list = ["mid-air_jump", "speed_dash"]

        # world completed screen variables -----------------------------------------------------------------------------
        self.world_completed_texts = {
            1: 'Seems like you got the hang of it!',
            2: 'The farm is now behind you, further challenges lay ahead',
            3: 'Fresh air, finally... No more damp caves',
            4: "That is the game, Thanks for playing!"
        }

        self.world_completed_text = text.make_text([self.world_completed_texts[world_count]])

        self.congrats_text_animation = {}
        for frame in range(0, 87):
            self.congrats_text_animation[frame] = img_loader(f'data/images/congrats_text_animation/text{frame + 1}.PNG',
                                                             tile_size * 4, tile_size * 2)

        self.world_completed_text.set_alpha(0)

        self.world_completed = False

        self.world_completed_btn_count = 0

        self.world_completed_text_alpha = 0
        self.world_completed_text_anim_count = 0
        self.fade_counter = 255

        # opening scene variables --------------------------------------------------------------------------------------
        self.opening_scene = False
        self.opening_scene_done = False
        self.opening_scene_end_count = 10
        self.opening_scene_step_counter = 1

        self.sack_position = (swidth / 2 - 18 / 2, sheight / 2 - 28 / 2)

        if world_count == 1:
            self.opening_scene_step_controller = {
                1: 'animation',
                2: Dialogue('Welcome to the world!', text),
                3: Dialogue('Your purpose in life:', text),
                4: Dialogue('become bread.', text),
                5: Dialogue('It may not sound glamorous, I know, but it is what it is.', text),
                6: Dialogue('All you need to do is get to the mill.', text),
                7: Dialogue("You think that's easy? It's a long way full of traps and enemies.", text),
                8: Dialogue('Good luck!', text),
                9: 'end'
            }
        else:
            self.opening_scene_step_controller = {}

        self.sack_birth_animation = {}
        if world_count == 1:
            for frame in range(1, 22):
                img = img_loader(f'data/images/sack_birth_animation/sack{frame}.PNG', 20, 32)
                self.sack_birth_animation[frame - 1] = img

        self.sack_anim_counter = -20
        self.animation_done = False

        self.sack_noise_played = False

        self.dialogue_surface = pygame.Surface((swidth, 32))
        self.dialogue_surface.fill((0, 0, 0))

        # variables ----------------------------------------------------------------------------------------------------
        self.level_check = 1

        self.controls = controls
        self.settings_counters = settings_counters

        self.reinit_eq = False

        self.trap_harm = False
        self.bee_harm = False
        self.spit_harm_left = False
        self.spit_harm_right = False
        self.spit_harm_up = False
        self.set_lava_harm = False
        self.hot_lava_harm = False

        self.health = 2
        self.harm = False
        self.tile_harm = False

        self.mid_air_jump_trigger = False
        self.speed_dash_trigger = False

        self.menu_fadeout = False
        self.music_playing = False

        self.camera_move_x = 0
        self.camera_move_y = 0

        self.move = False

        self.player_moved = False

        self.start_x = level_pos_dictionary[f'level1_{world_count}'][0]
        self.start_y = level_pos_dictionary[f'level1_{world_count}'][1]

        self.lvl_completed_popup = False
        self.bee_info_popup = False
        self.bee_info_popup_done = False
        self.dash_info_popup = False
        self.dash_info_popup_done = False
        self.new_card_animation = False

        self.blit_card_instructions = False

        self.level_length = 0

        self.shockwave_radius = 0

        self.level_duration_counter = 0

        self.new_card_animation = False

        self.gem_equipped = False

        self.change_music = True
        self.change_music_counter = 0

        self.bridge_collapsing = False

        # initiating classes -------------------------------------------------------------------------------------------
        self.world = World(world_data, self.game_screen, slow_computer, bg_data,
                           settings_counters, world_count)
        self.world.create_world(self.start_x, self.start_y, world_data, bg_data, 1)
        self.player = Player(self.game_screen, self.controls, self.settings_counters, world_count)
        self.particles = Particles(particle_num)
        self.eq_manager = eqManager(self.eq_power_list, self.controls, self.settings_counters['walking'])
        cont_width = self.controls_popup.get_width() / 2
        cont_height = self.controls_popup.get_height() / 2
        self.controls_popup_scrollbar = ScrollBar(self.controls_popup.get_height() - 4,
                                                  self.controls_popup_text_space.get_height(),
                                                  self.controls_popup_text_surface.get_height(),
                                                  (swidth / 2 + cont_width + 3, sheight / 2 - cont_height + 2))

        # class variables ----------------------------------------------------------------------------------------------
        self.tile_list = self.world.tile_list
        self.level_length = self.world.level_length

        self.left_border = self.start_x * 32 - (480 - swidth) / 2
        self.right_border = self.left_border + self.level_length * 32 - (480 - swidth) / 2

        portal_position = self.world.portal_position
        self.portal_surface_x = portal_position[0] + tile_size / 2 - swidth / 2
        self.portal_surface_y = portal_position[1] + tile_size / 2 - sheight / 2

    def popup_window(self, popup_window, screen, button, mouse_adjustment, events, joystick_over):
        self.move = False
        if 1.7 > self.level_duration_counter > 1.45:
            scaling = self.level_duration_counter - 1.45
            popup = pygame.transform.scale(popup_window,
                                           (popup_window.get_width() * scaling * 4,
                                            popup_window.get_height() * scaling * 4))
        else:
            popup = popup_window

        if self.level_duration_counter > 1.45:
            screen.blit(popup,
                        (swidth / 2 - popup.get_width() / 2,
                         sheight / 2 - popup.get_height() / 2))

        if self.level_duration_counter > 1.7:
            press, ok_over = button.draw_button(screen,
                                                False,
                                                mouse_adjustment,
                                                events, joystick_over)
        else:
            press = False

        return press

    # updates the controller type during gameplay if one calibrates their controller mid-game
    def update_controller_type(self, joystick_controls, settings_counters):
        configuration_counter = joystick_controls[4]
        self.settings_counters = settings_counters
        self.player.settings_counters = joystick_controls[4]
        if configuration_counter == 1:
            self.controller_type = 'xbox'
            jump_btn = 'A'
        elif configuration_counter == 2:
            self.controller_type = 'ps4'
            jump_btn = 'cross'

# LEVEL CHECKING =======================================================================================================
    def level_checker(self, level_count, world_count):
        # the level position needs to be offset by a certain amount to set the right spawn for the player (center)
        # calculated by tiles from the center of the mould (tiles fitting in the window)

        max_level = 9
        max_world = 3
        if level_count >= max_level:
            level_count = max_level
        if world_count >= max_world:
            world_count = max_world

        if (world_count == 1 and level_count == 3) or (world_count == 2 and level_count == 9):
            self.lvl_completed_popup = True

        if world_count == 2 and level_count == 6:
            self.bee_info_popup = True

        if world_count == 3 and level_count == 5:
            self.dash_info_popup = True

        if level_count != world_ending_levels[world_count]:
            world_data_level_checker = level_dictionary[f'level{level_count}_{world_count}']
            bg_data = level_bg_dictionary[f'level{level_count}_{world_count}_bg']
            pos = level_pos_dictionary[f'level{level_count}_{world_count}']
            self.start_x = pos[0]
            self.start_y = pos[1]

            self.left_border = self.start_x * 32 - (480 - swidth) / 2
            self.right_border = self.left_border + self.level_length * 32 - (480 - swidth) / 2
        else:
            world_data_level_checker = []
            bg_data = []
            self.world_completed = True

        return world_data_level_checker, bg_data

# WORLD COMPLETED ======================================================================================================
    def world_completed_screen(self, screen, events, fps_adjust, joysticks, joystick_calibration):
        screen.fill((0, 0, 0))

        menu_press = False
        end_screen = False

        if joystick_calibration:
            events = {
                'quit': False,
                'keydown': False,
                'keyup': False,
                'mousebuttondown': False,
                'mousebuttonup': False,
                'joyaxismotion': False,
                'joybuttondown': False,
                'joybuttonup': False,
                'joydeviceadded': False,
                'joydeviceremoved': False,
                'mousewheel': False,
                'videoresize': False
            }

        self.world_completed_text_anim_count += 0.5 * fps_adjust

        if self.fade_counter == 255 > self.world_completed_text_alpha:
            self.world_completed_text_alpha += 6 * fps_adjust
            if self.world_completed_text_alpha > 255:
                self.world_completed_text_alpha = 255

        if events['keydown']:
            if events['keydown'].key == self.controls['jump']:
                menu_press = True
        if events['joybuttondown']:
            if events['joybuttondown'].button == 0:
                menu_press = True

        text = self.world_completed_text
        if 0 <= self.world_completed_text_alpha <= 255:
            text.set_alpha(self.world_completed_text_alpha)

        if joysticks:
            if self.controller_type == 'xbox':
                btn_img = self.a_button_img
            else:
                btn_img = self.cross_button_img
        else:
            self.world_completed_btn_count += 1 * fps_adjust
            if self.world_completed_btn_count > 50:
                btn_img = self.space_button_press
                if self.world_completed_btn_count > 60:
                    self.world_completed_btn_count = 0
            else:
                btn_img = self.space_button_img

        if menu_press or 255 > self.fade_counter > 0:
            self.fade_counter -= 20 * fps_adjust
            self.world_completed_text_alpha = self.fade_counter

        if self.world_completed_text_anim_count > len(self.congrats_text_animation) - 1:
            self.world_completed_text_anim_count = len(self.congrats_text_animation) - 1

        congrats_text = self.congrats_text_animation[round(self.world_completed_text_anim_count)]

        if self.fade_counter < 255:
            congrats_text.set_alpha(self.world_completed_text_alpha)

        screen.blit(text, (swidth / 2 - text.get_width() / 2, sheight / 2 - text.get_height() / 2 + 10))
        screen.blit(congrats_text, (swidth / 2 - tile_size * 2, sheight / 2 - 60))
        if self.fade_counter == 255:
            screen.blit(btn_img, (swidth / 2 - btn_img.get_width() / 2, sheight / 2 - text.get_height() / 2 + 35))

        if self.fade_counter <= 0:
            end_screen = True

        return end_screen

    def opening_cutscene(self, screen, fps_adjust, events, joystick_calibration):
        screen.fill((0, 0, 0))
        self.dialogue_surface.fill((0, 0, 0))

        if joystick_calibration:
            events = {
                'quit': False,
                'keydown': False,
                'keyup': False,
                'mousebuttondown': False,
                'mousebuttonup': False,
                'joyaxismotion': False,
                'joybuttondown': False,
                'joybuttonup': False,
                'joydeviceadded': False,
                'joydeviceremoved': False,
                'mousewheel': False,
                'videoresize': False
            }

        final_step = False

        dialogue_done = False
        dialogue = False

        press = False
        sounds = {
            'sack_noise': False,
            'click': False
        }

        scene_step_type = self.opening_scene_step_controller[self.opening_scene_step_counter]
        if type(scene_step_type) == str:
            if scene_step_type == 'animation':
                self.sack_anim_counter += 0.2 * fps_adjust
            elif scene_step_type == 'end':
                final_step = True
        else:
            dialogue_done, sounds['click'] = scene_step_type.display_dialogue(self.dialogue_surface, fps_adjust)
            dialogue = True

        if events['keydown']:
            if events['keydown'].key == pygame.K_SPACE:
                press = True
        if events['joybuttondown']:
            if events['joybuttondown'].button == 0:
                press = True

        if dialogue_done and dialogue and not final_step and press:
            self.opening_scene_step_counter += 1

        if not dialogue_done and press and dialogue:
            scene_step_type.btn_press = True

        if final_step:
            self.opening_scene_end_count -= 1 * fps_adjust
            if self.opening_scene_end_count <= 0:
                self.opening_scene = False
                self.opening_scene_done = True

        if self.opening_scene_step_counter > len(self.opening_scene_step_controller):
            self.opening_scene_step_counter = len(self.opening_scene_step_controller)

        if self.sack_anim_counter > 20:
            self.sack_anim_counter = 20
            if not self.animation_done:
                self.animation_done = True
                self.opening_scene_step_counter += 1

        if self.sack_anim_counter >= 0 and not self.sack_noise_played:
            self.sack_noise_played = True
            sounds['sack_noise'] = True

        anim_counter = round(self.sack_anim_counter)
        if anim_counter < 0:
            anim_counter = 0

        screen.blit(self.sack_birth_animation[anim_counter], self.sack_position)

        screen.blit(self.dialogue_surface, (0, 10))

        return self.opening_scene_done, sounds

# THE GAME =============================================================================================================
    def game(self, screen, level_count, fps_adjust, draw_hitbox, mouse_adjustment, events,
             game_counter, world_count, controls, joystick_calibration, joysticks,
             restart_level_procedure):

        self.controls = controls

        # sounds
        sounds = {
            'card': False,
            'button': False,
            'trap': False,
            'step_grass': False,
            'step_wood': False,
            'step_rock': False,
            'jump': False,
            'mid_air_jump': False,
            'mushroom': False,
            'land': False,
            'death': False,
            'wheat': 0,
            'gem': False,
        }

        if joysticks:
            joystick_connected = True
        else:
            joystick_connected = False

        play_music = False

        popup_lvl_completed_press = False

        # new card animation
        if self.level_duration_counter == 0:
            if (world_count == 1 and level_count == 2) or (world_count == 3 and level_count == 2):
                self.new_card_animation = True
        if self.new_card_animation:
            self.move = False

        if game_counter > 0:
            self.level_duration_counter += 0.04 * fps_adjust

        if game_counter <= 0:
            self.move = False

        # setting tutorial on or off
        if world_count == 1:
            tutorial = True
        else:
            tutorial = False

        # dealing with harm
        if self.tile_harm or self.hot_lava_harm or self.trap_harm or self.bee_harm:
            self.harm = True
        else:
            self.harm = False

        # preventing movement when calibrating joystick
        if joystick_calibration:
            self.move = False

        # updating player variables ------------------------------------------------------------------------------------
        level_count,\
            sack_rect,\
            sack_direction,\
            self.health,\
            self.camera_move_x,\
            self.camera_move_y,\
            fadeout,\
            restart_level,\
            self.player_moved,\
            new_level_cooldown,\
            self.world.shockwave_mushroom_list,\
            self.gem_equipped,\
            screen_shake,\
            player_sounds = self.player.update_pos_animation(screen,
                                                             self.tile_list,
                                                             self.world.next_level_list,
                                                             level_count,
                                                             self.harm,
                                                             fps_adjust,
                                                             self.mid_air_jump_trigger,
                                                             self.speed_dash_trigger,
                                                             self.left_border,
                                                             self.right_border,
                                                             self.move,
                                                             self.world.shockwave_mushroom_list,
                                                             events,
                                                             self.gem_equipped,
                                                             joysticks,
                                                             restart_level_procedure,
                                                             self.controls,
                                                             )
        # updating player sounds
        sounds.update(player_sounds)
        # sack motion
        if self.camera_move_x != 0:
            moving = True
        else:
            moving = False

        # updating solid tile positions --------------------------------------------------------------------------------
        self.tile_list = self.world.update_tile_list(self.camera_move_x, self.camera_move_y)

        # blitting tiles and images in the background ------------------------------------------------------------------
        if world_count in [1, 2, 4]:
            self.game_screen.fill(self.sky_background_colour)
        else:
            if level_count == 1:
                if self.world.bg_border == 0:
                    self.game_screen.fill(self.cave_background_colour)
                else:
                    if self.sack_position[1] > self.world.bg_border:
                        for index in range(3):
                            self.bg_transition_colour[index] -= 6
                            if self.bg_transition_colour[index] < self.cave_background_colour[index]:
                                self.bg_transition_colour[index] = self.cave_background_colour[index]
                        self.game_screen.fill(self.bg_transition_colour)
                    else:
                        self.game_screen.fill(self.sky_background_colour)
                        self.bg_transition_colour = list(self.sky_background_colour)
            else:
                self.game_screen.fill(self.cave_background_colour)
        self.world.draw_static_tiles_background(self.game_screen)
        self.tile_harm, self.gem_equipped, sounds['gem'] = self.world.update_bg_tiles(self.game_screen, fps_adjust,
                                                                                      level_count, self.camera_move_x,
                                                                                      self.camera_move_y, sack_rect,
                                                                                      self.gem_equipped, self.health)
        self.world.draw_bridge(self.game_screen, self.camera_move_x, self.camera_move_y, fps_adjust, sack_rect)

        # drawing the  player ------------------------------------------------------------------------------------------
        self.player.blit_player(self.game_screen, draw_hitbox, fps_adjust)

        # updating level border positions ------------------------------------------------------------------------------
        self.right_border += self.camera_move_x
        self.left_border += self.camera_move_x

        # updating the world data if new level -------------------------------------------------------------------------
        if self.level_check < level_count or restart_level:
            self.world_data, self.bg_data = Game.level_checker(self, level_count, world_count)
            self.world.create_world(self.start_x, self.start_y, self.world_data, self.bg_data, level_count)
            self.tile_list, self.level_length = self.world.return_tile_list()
            self.right_border = self.left_border + self.level_length * 32
            self.particles = Particles(particle_num)
            self.blit_card_instructions = False
            self.gem_equipped = False
            self.portal_surface_x = self.world.portal_position[0] + tile_size / 2 - swidth / 2
            self.portal_surface_y = self.world.portal_position[1] + tile_size / 2 - sheight / 2
            if not restart_level:
                self.level_check = level_count
                self.player_moved = False
                self.level_duration_counter = 0

        # --------------------------------------------------------------------------------------------------------------
        if world_count == 3:
            self.hot_lava_harm = self.world.draw_hot_lava(self.game_screen, sack_rect, fps_adjust)

        if world_count < 3 or level_count == 1:
            sounds['wheat'] = self.world.draw_wheat(self.game_screen, sack_rect, moving)
            self.world.draw_green_mushrooms(self.game_screen, sack_rect)

        self.world.draw_static_tiles_foreground(self.game_screen)

        self.bee_harm = self.world.update_fg_tiles(self.game_screen, sack_rect, fps_adjust, self.camera_move_x,
                                                   self.camera_move_y, self.health, self.player_moved)

        self.trap_harm, sounds['trap'] = self.world.draw_bear_trap_list(self.game_screen, sack_rect)

        # blitting the game screen onto the main screen ----------------------------------------------------------------
        if screen_shake:
            screen.blit(self.game_screen, (random.choice([-3, 0, 3]), random.choice([-3, 0, 3])))
        else:
            screen.blit(self.game_screen, (0, 0))

        # respawn instructions -----------------------------------------------------------------------------------------
        self.player.blit_respawn_instructions(screen, fps_adjust, joystick_connected, self.settings_counters)

        # updating player health and blitting health bar ---------------------------------------------------------------
        self.world.draw_portal_compass(sack_rect, screen)

        if restart_level:
            self.level_duration_counter = 0
        if self.reinit_eq:
            self.eq_manager.create_card_buttons(self.eq_power_list)
            self.reinit_eq = False

        # updating and blitting the card bar ---------------------------------------------------------------------------
        if self.health != 0:
            self.eq_power_list,\
                self.mid_air_jump_trigger,\
                self.speed_dash_trigger,\
                sounds['card'] = self.eq_manager.draw_eq(screen, self.eq_power_list, mouse_adjustment, events,
                                                         tutorial, fps_adjust, level_count,
                                                         self.health, self.move, self.player_moved,
                                                         self.gem_equipped, self.controls,
                                                         joysticks, self.controller_type,
                                                         joystick_calibration)

        if self.mid_air_jump_trigger or self.speed_dash_trigger:
            self.gem_equipped = False

        # popup window -------------------------------------------------------------------------------------------------
        ok_over = False

        if joystick_connected:
            joystick_over = True
        else:
            joystick_over = False

        # controls popup
        if self.popup_window_controls:
            self.move = False
            if 3 > self.level_duration_counter > 2.75:
                scaling = self.level_duration_counter - 2.75
                popup = pygame.transform.scale(self.controls_popup, (self.controls_popup.get_width() * scaling * 4,
                                                                     self.controls_popup.get_height() * scaling * 4))
            else:
                popup = self.controls_popup

            if self.level_duration_counter > 3:
                controls_popup_percentage = self.controls_popup_scrollbar.draw_scroll_bar(screen,
                                                                                          mouse_adjustment, events,
                                                                                          joysticks,
                                                                                          self.controls['configuration'])
                self.controls_popup_text_space.fill(self.popup_bg_colour)
                self.controls_popup_text_space.blit(self.controls_popup_text_surface,
                                                    (0, -controls_popup_percentage * (self.controls_popup_text_surface.get_height() - self.controls_popup_text_space.get_height())))
                popup.blit(self.controls_popup_text_space, (2, 1))
                self.controls_popup_gradient.draw_gradient(popup)

            if self.level_duration_counter > 2.75:
                screen.blit(popup,
                            (swidth / 2 - popup.get_width() / 2,
                             sheight / 2 - popup.get_height() / 2))

            if self.level_duration_counter > 3:
                popup_controls_press, ok_over = self.ok_controls_btn.draw_button(screen,
                                                                                 False, mouse_adjustment,
                                                                                 events, joystick_over)
            else:
                popup_controls_press = False

            if popup_controls_press:
                self.popup_window_controls = False

        # bee info popup
        elif self.bee_info_popup and not self.bee_info_popup_done:
            popup_bees_press = Game.popup_window(self, self.bees_popup, screen, self.ok_bee_btn,
                                                 mouse_adjustment, events, joystick_over)
            if self.level_duration_counter > 1.45:
                self.bee_banner_y_counter -= 15 * fps_adjust
                if self.bee_banner_y_counter < 0:
                    self.bee_banner_y_counter = 0
                self.bee_banner_y = self.banner_final_y + self.bee_banner_y_counter
                if self.bee_banner_y_counter == 0:
                    y_offset = math.cos(self.level_duration_counter * 2) * 2
                else:
                    y_offset = 0
                screen.blit(self.banners['bee'], (self.bee_banner_x, self.bee_banner_y + y_offset))
            if popup_bees_press:
                self.bee_info_popup = False
                self.bee_info_popup_done = True

        # dash info popup
        elif self.dash_info_popup and not self.dash_info_popup_done:
            popup_dash_press = Game.popup_window(self, self.dash_popup, screen, self.ok_dash_btn,
                                                 mouse_adjustment, events, joystick_over)
            if self.level_duration_counter > 1.45:
                self.dash_banner_y_counter -= 15 * fps_adjust
                if self.dash_banner_y_counter < 0:
                    self.dash_banner_y_counter = 0
                self.dash_banner_y = self.banner_final_y + self.dash_banner_y_counter
                if self.dash_banner_y_counter == 0:
                    y_offset = math.cos(self.level_duration_counter * 2) * 2
                else:
                    y_offset = 0
                screen.blit(self.banners['dash'], (self.dash_banner_x, self.dash_banner_y + y_offset))
            if popup_dash_press:
                self.dash_info_popup = False
                self.dash_info_popup_done = True

        # new card popup and card animation
        elif self.new_card_animation:
            card_type = level_card_dictionary[f"level{level_count}_{world_count}"]
            if card_type in self.eq_power_list:
                self.new_card_animation = False
            else:
                if self.level_duration_counter > 1.45:
                    popup_new_card_press = Game.popup_window(self, self.new_card_popup, screen, self.ok_new_card_button,
                                                             mouse_adjustment, events, joystick_over)

                    self.eq_manager.new_card(card_type, screen, fps_adjust, self.level_duration_counter)

                    if popup_new_card_press:
                        self.new_card_animation = False
                        self.eq_power_list.append(card_type)
                        self.reinit_eq = True
                        try:
                            with open('data/collected_cards.json', 'w') as json_file:
                                json.dump(self.eq_power_list, json_file)
                        except FileNotFoundError:
                            power_list_not_saved_error = True

        else:
            self.move = True

        if ok_over:
            sounds['button'] = True

        # new level transition -----------------------------------------------------------------------------------------
        self.player.draw_transition(fps_adjust)

        # sounds -------------------------------------------------------------------------------------------------------
        if world_count == 3 and not self.music_playing:
            self.music_playing = True
            play_music = True

        if world_count == 2 and not self.music_playing:
            self.music_playing = True
            play_music = True

        if world_count == 1 and not self.music_playing:
            self.music_playing = True
            play_music = True

        # returns
        return level_count, play_music, sounds,\
            fadeout, popup_lvl_completed_press, self.world_completed
