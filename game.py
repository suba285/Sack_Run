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
import json
import random
import math


particle_num = 12

sheight = 264
swidth = 352

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
    "level4_3": level4_3
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
    "level4_3_bg": level4_3_bg
}

level_pos_dictionary = {
    "level1_1": (2, -2),
    "level2_1": (3, -2),
    "level3_1": (3, -2),
    "level1_2": (0, -4),
    "level2_2": (4, -5),
    "level3_2": (0, -4),
    "level4_2": (0, -5),
    "level5_2": (4, -7),
    "level6_2": (2, 2),
    "level7_2": (4, -18),
    "level8_2": (4, -5),
    "level9_2": (3, -2),
    "level1_3": (2, -4),
    "level2_3": (-3, -5),
    "level3_3": (2, -3),
    "level4_3": (0, -3)
}

level_card_dictionary = {
    "level2_1": "mid-air_jump",
    "level1_3": "speed_dash"
}


class LevelDisplay:
    def __init__(self, level_count):
        level_text = Text()
        self.text = level_text.make_text([f"Level {level_count}"])

    def draw_level_number(self, screen, game_counter):
        if game_counter < 0:
            local_offset = game_counter * 20
        else:
            local_offset = 0
        screen.blit(self.text, (swidth / 2 - self.text.get_width() / 2, 10 + local_offset))


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


class Game:
    def __init__(self, slow_computer, world_data, bg_data, controls, world_count, settings_counters,
                 joystick_connected):

        self.world_data = world_data
        self.bg_data = bg_data

        self.game_screen = pygame.Surface((swidth, sheight))
        self.game_screen.set_colorkey((0, 0, 255))

        self.cave_background_colour = (35, 29, 39)
        self.sky_background_colour = (100, 63, 102)

        # loading in images --------------------------------------------------------------------------------------------

        home_button_img = img_loader('data/images/button_pause.PNG', tile_size * 0.75, tile_size * 0.75)
        home_button_press = img_loader('data/images/button_pause_press.PNG', tile_size * 0.75, tile_size * 0.75)
        home_button_down = img_loader('data/images/button_pause_down.PNG', tile_size * 0.75, tile_size * 0.75)

        ok_button_img = img_loader('data/images/button_ok.PNG', tile_size, tile_size * 0.75)
        ok_button_press = img_loader('data/images/button_ok_press.PNG', tile_size, tile_size * 0.75)
        ok_button_down = img_loader('data/images/button_ok_down.PNG', tile_size, tile_size * 0.75)

        # buttons ------------------------------------------------------------------------------------------------------
        self.home_button = Button(swidth - tile_size + (tile_size - home_button_down.get_width()) / 2, 3,
                                  home_button_img, home_button_press, home_button_down)

        # POPUP WINDOWS ------------------------------------------------------------------------------------------------
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

        # controls popup window
        controls_txt = Text().make_text(['CONTROLS'])
        if not joystick_connected:
            walking_controls_txt = Text().make_text([f"walking: {self.nums_to_text[f'walk{walk_counter}']}"])
            jumping_controls_txt = Text().make_text([f"jumping: {self.nums_to_text[f'jump{jump_counter}']}"])
            card_controls_txt = Text().make_text(['cards: mouse'])
        else:
            walking_controls_txt = Text().make_text(['walking: Left stick or D-pad'])
            jumping_controls_txt = Text().make_text([f'jumping: {jump_btn} button'])
            card_controls_txt = Text().make_text(['cards: RB and LB'])
        tip1_txt = Text().make_text(['Follow the compass in the top-left corner,'])
        tip1_2_txt = Text().make_text(['it will lead you to portals.'])
        tip2_txt = Text().make_text(['Use cards to gain special abilities.'])
        tip3_txt = Text().make_text(['Collect gems to use cards.'])

        self.controls_popup_text_surface = pygame.Surface((tip1_txt.get_width() + 6, 180)).convert_alpha()
        self.controls_popup_text_space = pygame.Surface((tip1_txt.get_width() + 6, 115)).convert_alpha()
        self.popup_bg_colour = img_loader('data/images/popup_bg.PNG', self.controls_popup_text_space.get_width(),
                                     self.controls_popup_text_space.get_width())
        self.controls_popup_text_space.blit(self.popup_bg_colour, (0, 0))
        self.controls_popup_text_surface.set_colorkey((0, 0, 0))

        self.controls_popup_gradient = Gradient(tip1_txt.get_width() + 10, 15, (1, 101))

        self.controls_popup = popup_bg_generator((tip1_txt.get_width() + 6, 140))
        self.clean_popup = self.controls_popup
        cont_bg_center = self.controls_popup.get_width() / 2

        self.ok_controls_btn = Button(swidth / 2 - ok_button_img.get_width() / 2,
                                      sheight / 2 + self.controls_popup.get_height() / 2 - tile_size * 0.75 - 3,
                                      ok_button_img, ok_button_press, ok_button_down)

        self.controls_popup_text_surface.blit(controls_txt, (cont_bg_center - controls_txt.get_width() / 2, 6))
        self.controls_popup_text_surface.blit(walking_controls_txt,
                                 (cont_bg_center - walking_controls_txt.get_width() / 2, 30))
        self.controls_popup_text_surface.blit(jumping_controls_txt,
                                 (cont_bg_center - jumping_controls_txt.get_width() / 2, 45))
        self.controls_popup_text_surface.blit(card_controls_txt,
                                              (cont_bg_center - card_controls_txt.get_width() / 2, 60))

        self.controls_popup_text_surface.blit(tip1_txt, (cont_bg_center - tip1_txt.get_width() / 2, 90))
        self.controls_popup_text_surface.blit(tip1_2_txt, (cont_bg_center - tip1_2_txt.get_width() / 2, 105))
        self.controls_popup_text_surface.blit(tip2_txt, (cont_bg_center - tip2_txt.get_width() / 2, 120))
        self.controls_popup_text_surface.blit(tip3_txt, (cont_bg_center - tip3_txt.get_width() / 2, 135))

        self.controls_popup_text_space.blit(self.controls_popup_text_surface, (0, 0))
        self.controls_popup.blit(self.controls_popup_text_space, (2, 1))

        self.controls_popup.blit(ok_button_down, (cont_bg_center - ok_button_img.get_width() / 2,
                                                  self.controls_popup.get_height() - tile_size * 0.75 - 3))

        # bees popup window
        bees_txt = Text().make_text(['BEEWARE!'])

        self.bees_popup = popup_bg_generator((220, 150))

        self.bee_banner = img_loader('data/images/banner_shockwave.PNG', 200, 100)

        self.bee_banner_final_y = sheight / 2 - 52
        self.bee_banner_y_counter = sheight - self.bee_banner_final_y
        self.bee_banner_y = sheight
        self.bee_banner_x = swidth / 2 - 100

        bee_bg_center = self.bees_popup.get_width() / 2

        self.ok_bee_btn = Button(swidth / 2 - ok_button_img.get_width() / 2,
                                 sheight / 2 + self.bees_popup.get_height() / 2 - tile_size * 0.75 - 3,
                                 ok_button_img, ok_button_press, ok_button_down)

        self.bees_popup.blit(bees_txt, (bee_bg_center - bees_txt.get_width() / 2, 6))

        # new card popup window
        new_card_txt = Text().make_text(['NEW CARD UNLOCKED'])

        self.new_card_popup = popup_bg_generator((180, 130))
        self.ok_new_card_button = Button(swidth / 2 - ok_button_img.get_width() / 2,
                                         sheight / 2 + self.new_card_popup.get_height() / 2 - tile_size * 0.75 - 3,
                                         ok_button_img, ok_button_press, ok_button_down)

        self.new_card_popup.blit(new_card_txt,
                                 (self.new_card_popup.get_width() / 2 - new_card_txt.get_width() / 2, 6))
        self.new_card_popup.blit(ok_button_down,
                                 (self.new_card_popup.get_width() / 2 - ok_button_img.get_width() / 2,
                                  self.new_card_popup.get_height() - tile_size * 0.75 - 3))

        # level completed popup window
        worlds_nums = {
            1: "the tutorial",
            2: "world 1",
            3: "world 2"
        }
        congrats_txt = Text().make_text(['CONGRATS!'])
        tut_completed_txt = Text().make_text([f"You've completed {worlds_nums[world_count]}."])

        self.level_completed_popup = popup_bg_generator((tut_completed_txt.get_width() + 8, 80))
        tut_comp_center = self.level_completed_popup.get_width() / 2

        self.lvl_selection_btn = Button(swidth / 2 - ok_button_img.get_width() / 2,
                                        sheight / 2 + self.level_completed_popup.get_height() / 2 - tile_size * 0.75 - 3,
                                        ok_button_img, ok_button_press, ok_button_down)

        self.level_completed_popup.blit(congrats_txt, (tut_comp_center - congrats_txt.get_width() / 2, 6))
        self.level_completed_popup.blit(tut_completed_txt, (tut_comp_center - tut_completed_txt.get_width() / 2, 26))
        self.level_completed_popup.blit(ok_button_down,
                                        (self.level_completed_popup.get_width() / 2 - ok_button_img.get_width() / 2 + 1,
                                         self.level_completed_popup.get_height() - tile_size * 0.75 - 3))

        # lists --------------------------------------------------------------------------------------------------------
        self.eq_power_list = []

        try:
            with open('data/collected_cards.json', 'r') as json_file:
                self.eq_power_list = json.load(json_file)

        except FileNotFoundError:
            if world_count == 2:
                self.eq_power_list = ["mid-air_jump"]
            self.eq_power_list = []

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
        self.hot_lava_harm = True

        self.health = 2
        self.harm = False

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
        self.new_card_animation = False

        self.blit_card_instructions = False

        self.level_length = 0

        self.shockwave_radius = 0

        self.level_duration_counter = 0

        self.new_card_animation = False

        self.gem_equipped = False

        self.change_music = True
        self.change_music_counter = 0

        # initiating classes -------------------------------------------------------------------------------------------
        self.world = World(world_data, self.game_screen, slow_computer, bg_data,
                           settings_counters, world_count)
        self.world.create_world(self.start_x, self.start_y, world_data, bg_data)
        self.player = Player(self.game_screen, self.controls, self.settings_counters, world_count)
        self.particles = Particles(particle_num, slow_computer)
        self.eq_manager = eqManager(self.eq_power_list, self.controls, self.settings_counters['walking'])
        self.level_display = LevelDisplay(1)
        cont_width = self.controls_popup.get_width() / 2
        cont_height = self.controls_popup.get_height() / 2
        self.controls_popup_scrollbar = ScrollBar(self.controls_popup.get_height() - 4,
                                                  self.controls_popup_text_space.get_height(),
                                                  self.controls_popup_text_surface.get_height(),
                                                  (swidth / 2 + cont_width + 3, sheight / 2 - cont_height + 2))

        # class variables ----------------------------------------------------------------------------------------------
        self.tile_list = self.world.tile_list
        self.level_length = self.world.level_length

        self.left_border = self.start_x * 32
        self.right_border = self.left_border + self.level_length * 32

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
        else:
            self.controller_type = 'other'
            jump_btn = 'A or cross'

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

        world_data_level_checker = level_dictionary[f'level{level_count}_{world_count}']
        bg_data = level_bg_dictionary[f'level{level_count}_{world_count}_bg']
        pos = level_pos_dictionary[f'level{level_count}_{world_count}']
        self.start_x = pos[0]
        self.start_y = pos[1]

        self.left_border = self.start_x * 32
        self.right_border = self.left_border + self.level_length * 32

        return world_data_level_checker, bg_data

# THE GAME =============================================================================================================
    def game(self, screen, level_count, slow_computer, fps_adjust, draw_hitbox, mouse_adjustment, events,
             game_counter, world_count, controls, joystick_connected, joystick_calibration, joysticks):

        self.controls = controls

        # sounds
        play_card_pull_sound = False
        play_healing_sound = False
        play_paper_sound = False
        play_lock_sound = False

        play_music = False

        popup_lvl_completed_press = False

        # new card animation
        if self.level_duration_counter == 0:
            if (world_count == 1 and level_count == 2) or (world_count == 3 and level_count == 1):
                self.new_card_animation = True
        if self.new_card_animation:
            self.move = False

        if game_counter > 0:
            self.level_duration_counter += 0.04 * fps_adjust

        # setting tutorial on or off
        if world_count == 1:
            tutorial = True
        else:
            tutorial = False

        # dealing with harm
        if self.spit_harm_up or self.spit_harm_left or self.spit_harm_right or self.trap_harm or self.bee_harm or\
                self.set_lava_harm or self.hot_lava_harm:
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
            screen_shake = self.player.update_pos_animation(screen,
                                                            self.tile_list,
                                                            self.world.next_level_list,
                                                            level_count,
                                                            self.harm,
                                                            fps_adjust,
                                                            self.mid_air_jump_trigger,
                                                            self.speed_dash_trigger,
                                                            self.left_border,
                                                            self.right_border,
                                                            game_counter,
                                                            self.move,
                                                            self.world.shockwave_mushroom_list,
                                                            events,
                                                            self.gem_equipped,
                                                            joysticks
                                                            )

        # updating solid tile positions --------------------------------------------------------------------------------
        self.tile_list = self.world.update_tile_list(self.camera_move_x, self.camera_move_y)

        # blitting tiles and images in the background ------------------------------------------------------------------
        if world_count in [1, 2]:
            self.game_screen.fill(self.sky_background_colour)
        else:
            self.game_screen.fill(self.cave_background_colour)
        self.particles.bg_particles(self.game_screen, self.camera_move_x, self.camera_move_y, sack_direction)
        self.world.draw_bg_tile_list(self.game_screen)
        self.world.draw_log(self.game_screen, fps_adjust, self.camera_move_x, self.camera_move_y)
        self.world.draw_portal_list(self.game_screen, fps_adjust, level_count,
                                    self.camera_move_x, self.camera_move_y)
        self.world.draw_bush(self.game_screen)
        self.world.draw_tree(self.game_screen)

        # drawing the  player ------------------------------------------------------------------------------------------
        self.player.blit_player(self.game_screen, draw_hitbox, fps_adjust)

        # drawing gems -------------------------------------------------------------------------------------------------
        self.gem_equipped = self.world.draw_gem(self.game_screen, sack_rect, fps_adjust, self.gem_equipped)

        # updating level border positions ------------------------------------------------------------------------------
        self.right_border += self.camera_move_x
        self.left_border += self.camera_move_x

        # drawing and updating other tiles and objects in the game -----------------------------------------------------
        self.spit_harm_left = self.world.draw_spitting_plant_left(self.game_screen, fps_adjust, self.camera_move_x,
                                                                  self.camera_move_y, sack_rect, self.health)
        self.spit_harm_right = self.world.draw_spitting_plant_right(self.game_screen, fps_adjust, self.camera_move_x,
                                                                    self.camera_move_y, sack_rect, self.health)
        self.spit_harm_up = self.world.draw_spitting_plant_up(self.game_screen, fps_adjust, self.camera_move_x,
                                                              self.camera_move_y, sack_rect, self.health)

        # updating the world data if new level -------------------------------------------------------------------------
        if self.level_check < level_count or restart_level:
            self.world_data, self.bg_data = Game.level_checker(self, level_count, world_count)
            self.world.create_world(self.start_x, self.start_y, self.world_data, self.bg_data)
            self.tile_list, self.level_length = self.world.return_tile_list()
            self.right_border = self.left_border + self.level_length * 32
            self.particles = Particles(particle_num, slow_computer)
            self.blit_card_instructions = False
            self.level_display = LevelDisplay(level_count)
            self.gem_equipped = False
            self.portal_surface_x = self.world.portal_position[0] + tile_size / 2 - swidth / 2
            self.portal_surface_y = self.world.portal_position[1] + tile_size / 2 - sheight / 2
            if not restart_level:
                self.level_check = level_count
                self.player_moved = False
                self.level_duration_counter = 0

        # --------------------------------------------------------------------------------------------------------------

        self.world.draw_wheat(self.game_screen, sack_rect)

        self.set_lava_harm = self.world.draw_set_lava(self.game_screen, sack_rect)
        self.hot_lava_harm = self.world.draw_hot_lava(self.game_screen, sack_rect, fps_adjust)

        self.world.draw_shockwave_mushrooms(self.game_screen, fps_adjust)

        self.world.draw_green_mushrooms(self.game_screen, sack_rect)
        self.world.draw_tile_list(self.game_screen)

        self.trap_harm, play_bear_trap_cling_sound = self.world.draw_bear_trap_list(self.game_screen, sack_rect)

        self.world.draw_foliage(self.game_screen)
        self.bee_harm = self.world.draw_and_manage_beehive(self.game_screen, sack_rect, fps_adjust, self.camera_move_x,
                                                           self.camera_move_y, self.health,
                                                           self.player_moved)
        self.particles.front_particles(self.game_screen, self.camera_move_x, self.camera_move_y)

        # blitting the game screen onto the main screen ----------------------------------------------------------------
        if screen_shake:
            screen.blit(self.game_screen, (random.choice([-3, 0, 3]), random.choice([-3, 0, 3])))
        else:
            screen.blit(self.game_screen, (0, 0))

        # respawn instructions -----------------------------------------------------------------------------------------
        self.player.blit_respawn_instructions(screen, fps_adjust, joystick_connected, self.settings_counters)

        # eq full message ----------------------------------------------------------------------------------------------
        self.world.draw_eq_full(screen)

        # updating player health and blitting health bar ---------------------------------------------------------------
        self.player.update_health()
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
                play_card_pull_sound = self.eq_manager.draw_eq(screen, self.eq_power_list, mouse_adjustment, events,
                                                               tutorial, fps_adjust, level_count,
                                                               self.health, self.move, self.player_moved,
                                                               self.gem_equipped, self.controls['configuration'],
                                                               joysticks, self.controller_type,
                                                               joystick_calibration)

        if self.mid_air_jump_trigger or self.speed_dash_trigger:
            self.gem_equipped = False

        # menu button --------------------------------------------------------------------------------------------------
        menu, game_button_over = self.home_button.draw_button(screen, False, mouse_adjustment, events, False)

        if menu and not self.menu_fadeout:
            self.menu_fadeout = True
            self.music_playing = False
            fadeout = True

        # popup window -------------------------------------------------------------------------------------------------
        ok_over = False

        if joystick_connected:
            joystick_over = True
        else:
            joystick_over = False

        # controls popup
        if self.popup_window_controls:
            self.move = False
            if 0.25 > game_counter > 0:
                scaling = game_counter
                popup = pygame.transform.scale(self.controls_popup, (self.controls_popup.get_width() * scaling * 4,
                                                                     self.controls_popup.get_height() * scaling * 4))
            else:
                popup = self.controls_popup

            if game_counter >= 0.25:
                controls_popup_percentage = self.controls_popup_scrollbar.draw_scroll_bar(screen,
                                                                                          mouse_adjustment, events,
                                                                                          joysticks,
                                                                                          self.controls['configuration'])
                self.controls_popup_text_space.blit(self.popup_bg_colour, (0, 0))
                self.controls_popup_text_space.blit(self.controls_popup_text_surface,
                                                    (0, -controls_popup_percentage * (self.controls_popup_text_surface.get_height() - self.controls_popup_text_space.get_height())))
                popup.blit(self.controls_popup_text_space, (2, 1))
                self.controls_popup_gradient.draw_gradient(popup)

            if game_counter > 0:
                screen.blit(popup,
                            (swidth / 2 - popup.get_width() / 2,
                             sheight / 2 - popup.get_height() / 2))

            if game_counter >= 0.25:
                popup_controls_press, ok_over = self.ok_controls_btn.draw_button(screen,
                                                                                 False, mouse_adjustment,
                                                                                 events, joystick_over)
            else:
                popup_controls_press = False

            if popup_controls_press:
                self.popup_window_controls = False

        # level completed popup
        elif self.lvl_completed_popup:
            self.move = False
            if 1.7 > self.level_duration_counter > 1.45:
                scaling = self.level_duration_counter - 1.45
                popup = pygame.transform.scale(self.level_completed_popup,
                                               (self.level_completed_popup.get_width() * scaling * 4,
                                                self.level_completed_popup.get_height() * scaling * 4))
            else:
                popup = self.level_completed_popup

            if self.level_duration_counter > 1.45:
                screen.blit(popup,
                            (swidth / 2 - popup.get_width() / 2,
                             sheight / 2 - popup.get_height() / 2))

            if self.level_duration_counter > 1.7:
                popup_lvl_completed_press, ok_over = self.lvl_selection_btn.draw_button(screen,
                                                                                        False,
                                                                                        mouse_adjustment,
                                                                                        events, joystick_over)
            else:
                popup_lvl_completed_press = False

        # bee info popup
        elif self.bee_info_popup and not self.bee_info_popup_done:
            popup_bees_press = Game.popup_window(self, self.bees_popup, screen, self.ok_bee_btn,
                                                 mouse_adjustment, events, joystick_over)
            if self.level_duration_counter > 1.45:
                self.bee_banner_y_counter -= 15 * fps_adjust
                if self.bee_banner_y_counter < 0:
                    self.bee_banner_y_counter = 0
                self.bee_banner_y = self.bee_banner_final_y + self.bee_banner_y_counter
                if self.bee_banner_y_counter == 0:
                    y_offset = math.cos(self.level_duration_counter * 2) * 2
                else:
                    y_offset = 0
                screen.blit(self.bee_banner, (self.bee_banner_x, self.bee_banner_y + y_offset))
            if popup_bees_press:
                self.bee_info_popup = False
                self.bee_info_popup_done = True

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
            game_button_over = True

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
        return level_count, menu, play_card_pull_sound, play_lock_sound, play_bear_trap_cling_sound,\
            play_healing_sound, game_button_over, play_paper_sound, play_music,\
            fadeout, popup_lvl_completed_press
