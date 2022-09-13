from world import World, tile_size
from player import Player
from levels import *
from button import *
from particles import Particles
from eq_management import eqManager
from shockwave import Shockwave
from image_loader import img_loader
from font_manager import Text
from popup_bg_generator import popup_bg_generator


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
    "level9_2": level9_2
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
    "level9_2_bg": level9_2_bg
}

level_pos_dictionary = {
    "level1_1": (0, -10),
    "level2_1": (3, -2),
    "level3_1": (3, -2),
    "level1_2": (0, -4),
    "level2_2": (4, -5),
    "level3_2": (0, -4),
    "level4_2": (1, 1),
    "level5_2": (4, -7),
    "level6_2": (2, 2),
    "level7_2": (4, -5),
    "level8_2": (4, -5),
    "level9_2": (3, -2)
}


# not in use
def intro_map(screen, int_map, map_img, map_btn):
    GB = min(0, max(0, round(255 * (1 - 0.3))))
    screen.fill((0, GB, GB), special_flags=pygame.BLEND_MULT)
    screen.blit(map_img, (0, 0))
    press = map_btn.draw_button(screen)
    if press:
        int_map = False
    return int_map


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


class Game:
    def __init__(self, x, y, slow_computer, screen, world_data, bg_data, controls, world_count, settings_counters):

        # loading in images --------------------------------------------------------------------------------------------
        background_raw = pygame.image.load('data/images/menu_background.PNG').convert()
        self.background = pygame.transform.scale(background_raw, (360, 264))

        home_button_img = img_loader('data/images/button_pause.PNG', tile_size * 0.75, tile_size * 0.75)
        home_button_press = img_loader('data/images/button_pause_press.PNG', tile_size * 0.75, tile_size * 0.75)
        home_button_down = img_loader('data/images/button_pause_down.PNG', tile_size * 0.75, tile_size * 0.75)

        ok_button_img = img_loader('data/images/button_ok.PNG', tile_size, tile_size * 0.75)
        ok_button_press = img_loader('data/images/button_ok_press.PNG', tile_size, tile_size * 0.75)
        ok_button_down = img_loader('data/images/button_ok_down.PNG', tile_size, tile_size * 0.75)

        # buttons ------------------------------------------------------------------------------------------------------
        self.home_button = Button(swidth - tile_size + (tile_size - home_button_down.get_width()) / 2, 3,
                                  home_button_img, home_button_press, home_button_down)

        # popup windows ------------------------------------------------------------------------------------------------
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
            'interact1': 'X',
            'interact2': 'E',
            'interact3': 'forward slash',
            'shockwave1': 'Z',
            'shockwave2': 'F',
            'shockwave3': 'right shift',
            'delete_card1': 'Q',
            'delete_card2': 'full stop'
        }

        walk_counter = settings_counters['walking']
        jump_counter = settings_counters['jumping']
        interaction_counter = settings_counters['interaction']
        shockwave_counter = settings_counters['shockwave']

        # controls popup window
        controls_txt = Text().make_text(['CONTROLS'])
        walking_controls_txt = Text().make_text([f"walking: {self.nums_to_text[f'walk{walk_counter}']}"])
        jumping_controls_txt = Text().make_text([f"jumping: {self.nums_to_text[f'jump{jump_counter}']}"])
        interaction_controls_txt = Text().make_text([f"interaction: {self.nums_to_text[f'interact{interaction_counter}']}"])
        shockwave_controls_txt = Text().make_text([f"shockwave: {self.nums_to_text[f'shockwave{shockwave_counter}']}"])
        tip1_txt = Text().make_text(['follow the compass in the top-left corner'])

        tip2_txt = Text().make_text(['use shockwaves against bees'])
        tip3_txt = Text().make_text(['regain health by eating red mushrooms'])

        self.controls_popup = popup_bg_generator((tip1_txt.get_width() + 6, 130))
        cont_bg_center = self.controls_popup.get_width() / 2

        self.ok_controls_btn = Button(swidth / 2 - ok_button_img.get_width() / 2,
                                      sheight / 2 + self.controls_popup.get_height() / 2 - tile_size * 0.75 - 3,
                                      ok_button_img, ok_button_press, ok_button_down)

        self.controls_popup.blit(controls_txt, (cont_bg_center - controls_txt.get_width() / 2, 6))
        self.controls_popup.blit(walking_controls_txt,
                                 (cont_bg_center - walking_controls_txt.get_width() / 2, 25))
        self.controls_popup.blit(jumping_controls_txt,
                                 (cont_bg_center - jumping_controls_txt.get_width() / 2, 40))
        self.controls_popup.blit(interaction_controls_txt,
                                 (cont_bg_center - interaction_controls_txt.get_width() / 2, 55))
        self.controls_popup.blit(shockwave_controls_txt,
                                 (cont_bg_center - shockwave_controls_txt.get_width() / 2, 70))
        self.controls_popup.blit(tip1_txt, (cont_bg_center - tip1_txt.get_width() / 2, 90))
        self.controls_popup.blit(ok_button_down, (cont_bg_center - ok_button_img.get_width() / 2,
                                                  self.controls_popup.get_height() - tile_size * 0.75 - 3))

        # bees popup window
        bees_txt = Text().make_text(['BEEWARE!'])
        bees_intro_txt = Text().make_text(['You are about to encounter bees,'])
        bees_things_to_know_txt = Text().make_text(['here are some things you need to know:'])
        shockwave_key = self.nums_to_text[f'shockwave{settings_counters["shockwave"]}']
        bees_tip1_txt = Text().make_text([f'- use shockwaves to kill bees [{shockwave_key}]'])
        bees_tip2_txt = Text().make_text(['- hide in purple flowers to avoid being stung'])

        self.bees_popup = popup_bg_generator((bees_tip2_txt.get_width() + 6, 115))

        bee_bg_center = self.bees_popup.get_width() / 2

        self.ok_bee_btn = Button(swidth / 2 - ok_button_img.get_width() / 2,
                                 sheight / 2 + self.bees_popup.get_height() / 2 - tile_size * 0.75 - 3,
                                 ok_button_img, ok_button_press, ok_button_down)

        self.bees_popup.blit(bees_txt, (bee_bg_center - bees_txt.get_width() / 2, 6))
        self.bees_popup.blit(bees_intro_txt, (bee_bg_center - bees_intro_txt.get_width() / 2, 25))
        self.bees_popup.blit(bees_things_to_know_txt, (bee_bg_center - bees_things_to_know_txt.get_width() / 2, 40))
        self.bees_popup.blit(bees_tip2_txt, (bee_bg_center - bees_tip2_txt.get_width() / 2, 55))
        self.bees_popup.blit(bees_tip1_txt, (bee_bg_center - bees_tip1_txt.get_width() / 2, 70))
        self.bees_popup.blit(ok_button_down, (bee_bg_center - ok_button_img.get_width() / 2,
                                              self.bees_popup.get_height() - tile_size * 0.75 - 3))

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
        self.default_power_list = ['regeneration', 'regeneration', 'regeneration', 'no harm', 'no harm', 'jump boost',
                                   'jump boost', 'no gravity', 'shockwave+', 'shockwave+']

        self.power_list = self.default_power_list
        self.eq_power_list = []
        self.backup_eq_power_list = []

        # variables ----------------------------------------------------------------------------------------------------
        self.level_check = 1

        self.controls = controls
        self.settings_counters = settings_counters

        self.dead = False

        self.reinit_eq = False

        self.trap_harm = False
        self.bee_harm = False
        self.spit_harm_left = False
        self.spit_harm_right = False
        self.spit_harm_up = False

        self.health = 2
        self.jump_boost_trigger = False
        self.regeneration_trigger = False
        self.mush_regeneration_trigger = False
        self.no_gravity_trigger = False
        self.no_harm_trigger = False
        self.shockwave_trigger = False

        self.play_music = False
        self.fadeout = False
        self.menu_fadeout = False

        self.camera_move_x = 0
        self.camera_move_y = 0

        self.x = x
        self.y = y

        self.move = False

        self.player_moved = False

        self.start_x = 2
        self.start_y = -4

        self.restart_level = False

        self.lvl_completed_popup = False
        self.bee_info_popup = False
        self.bee_info_popup_done = False

        self.blit_card_instructions = False

        self.level_length = 0

        self.shockwave_radius = 0

        self.level_duration_counter = 0

        # initiating classes -------------------------------------------------------------------------------------------
        self.player = Player(x, y, screen, self.controls, self.settings_counters)
        self.world = World(world_data, screen, slow_computer, self.start_x, self.start_y, bg_data, controls,
                           settings_counters)
        self.particles = Particles(particle_num, slow_computer)
        self.eq_manager = eqManager(self.eq_power_list, self.controls, self.settings_counters['walking'])
        self.shockwave = Shockwave(screen, controls)
        self.level_display = LevelDisplay(1)

        # nesting lists ------------------------------------------------------------------------------------------------
        self.tile_list, self.level_length = self.world.return_tile_list()
        self.slope_list = self.world.return_slope_list()

        self.left_border = self.start_x * 32
        self.right_border = self.left_border + self.level_length * 32

# LEVEL CHECKING =======================================================================================================
    def level_checker(self, level_count, world_count):
        world_data_level_checker = level1_2
        # the level position needs to be offset by a certain amount to set the right spawn for the player (center)
        # calculated by tiles from the center of the mould (tiles fitting in the window)

        max_level = 9
        max_world = 2
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
    def game(self, screen, level_count, slow_computer, fps_adjust, draw_hitbox, mouse_adjustment, events, world_data,
             bg_data, game_counter, world_count):

        play_card_pull_sound = False
        play_healing_sound = False
        play_paper_sound = False

        self.level_duration_counter += 0.04 * fps_adjust

        chest_opened = False

        self.restart_level = False

        if world_count == 1:
            tutorial = True
        else:
            tutorial = False

        # updating player variables ------------------------------------------------------------------------------------
        level_count,\
            sack_rect,\
            sack_direction,\
            self.health,\
            self.camera_move_x,\
            self.camera_move_y,\
            self.play_music,\
            self.fadeout,\
            self.restart_level,\
            self.player_moved,\
            new_level_cooldown = self.player.update_pos_animation(screen,
                                                                  self.tile_list,
                                                                  self.world.next_level_list,
                                                                  level_count,
                                                                  self.trap_harm,
                                                                  self.bee_harm,
                                                                  self.spit_harm_left,
                                                                  self.spit_harm_right,
                                                                  self.spit_harm_up,
                                                                  self.health,
                                                                  fps_adjust,
                                                                  self.jump_boost_trigger,
                                                                  self.regeneration_trigger,
                                                                  self.mush_regeneration_trigger,
                                                                  self.no_gravity_trigger,
                                                                  self.no_harm_trigger,
                                                                  self.left_border,
                                                                  self.right_border,
                                                                  game_counter,
                                                                  self.move
                                                                  )

        # updating solid tile positions --------------------------------------------------------------------------------
        self.tile_list = self.world.update_tile_list(self.camera_move_x, self.camera_move_y)

        # blitting tiles and images in the background ------------------------------------------------------------------
        screen.blit(self.background, (0, 0))
        self.particles.bg_particles(screen, self.camera_move_x, self.camera_move_y, sack_direction)
        self.world.draw_background(screen, self.camera_move_x, self.camera_move_y)
        self.world.draw_log(screen, fps_adjust, self.camera_move_x, self.camera_move_y)
        self.world.draw_portal_list(screen, fps_adjust, level_count)
        self.world.draw_bush(screen)
        self.world.draw_tree(screen)

        # blitting player ----------------------------------------------------------------------------------------------
        self.player.blit_player(screen, draw_hitbox, fps_adjust)

        # updating level border positions ------------------------------------------------------------------------------
        self.right_border += self.camera_move_x
        self.left_border += self.camera_move_x

        # drawing and updating other tiles and objects in the game -----------------------------------------------------
        self.spit_harm_left = self.world.draw_spitting_plant_left(screen, fps_adjust, self.camera_move_x,
                                                                  self.camera_move_y, sack_rect, self.health)
        self.spit_harm_right = self.world.draw_spitting_plant_right(screen, fps_adjust, self.camera_move_x,
                                                                    self.camera_move_y, sack_rect, self.health)
        self.spit_harm_up = self.world.draw_spitting_plant_up(screen, fps_adjust, self.camera_move_x,
                                                              self.camera_move_y, sack_rect, self.health)
        chosen_power, self.reinit_eq, play_lock_sound,\
            self.power_list, chest_opened = self.world.draw_chest(screen, sack_rect,
                                                                  fps_adjust,
                                                                  self.power_list,
                                                                  tutorial,
                                                                  self.eq_power_list,
                                                                  level_count)

        if chest_opened:
            self.blit_card_instructions = True

        # updating the world data if new level -------------------------------------------------------------------------
        if self.level_check < level_count or self.restart_level:
            world_data, bg_data = Game.level_checker(self, level_count, world_count)
            self.world = World(world_data, screen, slow_computer, self.start_x, self.start_y, bg_data, self.controls,
                               self.settings_counters)
            self.tile_list, self.level_length = self.world.return_tile_list()
            self.right_border = self.left_border + self.level_length * 32
            self.particles = Particles(particle_num, slow_computer)
            self.reinit_eq = True
            self.blit_card_instructions = False
            self.level_display = LevelDisplay(level_count)
            if not self.restart_level:
                self.level_check = level_count
                self.player_moved = False
                self.level_duration_counter = 0
                self.backup_eq_power_list = self.eq_power_list

        # --------------------------------------------------------------------------------------------------------------

        self.world.draw_wheat(screen, sack_rect)

        self.world.draw_green_mushrooms(screen, sack_rect)
        self.world.draw_tile_list(screen)

        self.trap_harm, play_bear_trap_cling_sound = self.world.draw_bear_trap_list(screen, sack_rect)
        self.world.draw_grass_list(screen, sack_rect, sack_direction, fps_adjust)
        self.mush_regeneration_trigger, self.health = self.world.draw_mushroom(screen, sack_rect, self.health,
                                                                               self.camera_move_x,
                                                                               self.camera_move_y, fps_adjust,
                                                                               tutorial)
        self.world.draw_foliage(screen)
        self.world.draw_toxic_flowers(screen)
        self.bee_harm = self.world.draw_and_manage_beehive(screen, sack_rect, fps_adjust, self.camera_move_x,
                                                           self.camera_move_y, self.health, self.shockwave_radius,
                                                           self.player_moved)
        self.particles.front_particles(screen, self.camera_move_x, self.camera_move_y)

        # shockwave ----------------------------------------------------------------------------------------------------
        self.shockwave_radius = self.shockwave.update_shockwave(sack_rect, fps_adjust,
                                                                self.camera_move_x,
                                                                self.camera_move_y,
                                                                mouse_adjustment, self.health)

        # respawn instructions -----------------------------------------------------------------------------------------
        self.player.blit_respawn_instructions(screen, fps_adjust)

        # control instructions -----------------------------------------------------------------------------------------
        self.player.draw_inst_buttons(screen, fps_adjust, level_count, world_count)

        # eq full message ----------------------------------------------------------------------------------------------
        self.world.draw_eq_full(screen)

        # updating player health and blitting health bar ---------------------------------------------------------------
        play_card_pull_sound3 = self.player.update_health(screen, fps_adjust, mouse_adjustment)
        self.world.draw_portal_compass(sack_rect, screen)
        self.player.player_power_indicator(screen)

        if self.restart_level:
            self.eq_power_list = []
            self.eq_manager = eqManager(self.eq_power_list, self.controls, self.settings_counters['walking'])
            self.level_duration_counter = 0
        if self.reinit_eq:
            self.eq_manager = eqManager(self.eq_power_list, self.controls, self.settings_counters['walking'])
            self.reinit_eq = False

        # updating and blitting the card bar ---------------------------------------------------------------------------
        if self.health != 0:
            self.eq_power_list,\
                self.jump_boost_trigger,\
                self.regeneration_trigger,\
                self.no_gravity_trigger,\
                self.no_harm_trigger,\
                self.shockwave_trigger,\
                play_card_pull_sound,\
                self.power_list,\
                play_paper_sound = self.eq_manager.draw_eq(screen, self.eq_power_list, mouse_adjustment, events,
                                                           self.power_list, tutorial, fps_adjust, level_count,
                                                           self.blit_card_instructions, self.health, self.move)

        # resetting shockwave ------------------------------------------------------------------------------------------
        if self.shockwave_trigger:
            self.shockwave = Shockwave(screen, self.controls)

        # menu button --------------------------------------------------------------------------------------------------
        menu, game_button_over = self.home_button.draw_button(screen, False, mouse_adjustment, events)
        if menu and not self.menu_fadeout:
            self.menu_fadeout = True
            self.fadeout = True

        # level count display ------------------------------------------------------------------------------------------
        if not (tutorial and level_count == 3) and not (world_count == 2 and level_count == 9):
            self.level_display.draw_level_number(screen, game_counter)

        # popup window -------------------------------------------------------------------------------------------------
        ok_over = False

        # controls popup
        if self.popup_window_controls:
            self.move = False
            if 0.25 > game_counter > 0:
                scaling = game_counter
                popup = pygame.transform.scale(self.controls_popup, (self.controls_popup.get_width() * scaling * 4,
                                                                     self.controls_popup.get_height() * scaling * 4))
            else:
                popup = self.controls_popup
            if game_counter > 0:
                screen.blit(popup,
                            (swidth / 2 - popup.get_width() / 2,
                             sheight / 2 - popup.get_height() / 2))

            if game_counter >= 0.25:
                popup_controls_press, ok_over = self.ok_controls_btn.draw_button(screen,
                                                                                 False, mouse_adjustment, events)
            else:
                popup_controls_press = False

            if popup_controls_press:
                self.popup_window_controls = False
        else:
            self.move = True

        # level completed popup
        if self.lvl_completed_popup:
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
                popup_tut_completed_press, ok_over = self.lvl_selection_btn.draw_button(screen,
                                                                                        False,
                                                                                        mouse_adjustment,
                                                                                        events)
            else:
                popup_tut_completed_press = False
        else:
            popup_tut_completed_press = False

        # bee info popup
        if self.bee_info_popup and not self.bee_info_popup_done:
            self.move = False
            if 1.7 > self.level_duration_counter > 1.45:
                scaling = self.level_duration_counter - 1.45
                popup = pygame.transform.scale(self.bees_popup,
                                               (self.bees_popup.get_width() * scaling * 4,
                                                self.bees_popup.get_height() * scaling * 4))
            else:
                popup = self.bees_popup

            if self.level_duration_counter > 1.45:
                screen.blit(popup,
                            (swidth / 2 - popup.get_width() / 2,
                             sheight / 2 - popup.get_height() / 2))

            if self.level_duration_counter > 1.7:
                popup_bees_press, ok_over = self.ok_bee_btn.draw_button(screen,
                                                                        False,
                                                                        mouse_adjustment,
                                                                        events)
            else:
                popup_bees_press = False

            if popup_bees_press:
                self.bee_info_popup = False
                self.bee_info_popup_done = True

        if ok_over:
            game_button_over = True

        # new level transition -----------------------------------------------------------------------------------------
        self.player.draw_transition(fps_adjust)

        # sounds -------------------------------------------------------------------------------------------------------
        if self.regeneration_trigger or self.mush_regeneration_trigger:
            play_healing_sound = True

        if play_card_pull_sound3:
            play_card_pull_sound = True

        # pygame.mouse.set_visible(False)

        return level_count, menu, play_card_pull_sound, play_lock_sound, play_bear_trap_cling_sound,\
            play_healing_sound, world_data, self.dead, bg_data, game_button_over, play_paper_sound, self.play_music,\
            self.fadeout, popup_tut_completed_press
