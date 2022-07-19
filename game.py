from world import World, tile_size
from player import Player
from levels import *
from button import *
from particles import Particles
from eq_management import eqManager
from shockwave import Shockwave
from image_loader import img_loader


particle_num = 12

swidth = 360
sheight = 264

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
    "level1_1": (0, -4),
    "level2_1": (3, -2),
    "level3_1": (3, -2),
    "level1_2": (0, -4),
    "level2_2": (4, -5),
    "level3_2": (0, -4),
    "level4_2": (1, 1),
    "level5_2": (4, -6),
    "level6_2": (4, -5),
    "level7_2": (4, -5),
    "level8_2": (2, -19),
    "level9_2": (1, -5)
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


class Game:
    def __init__(self, x, y, slow_computer, screen, world_data, bg_data):

        # loading in images --------------------------------------------------------------------------------------------
        background_raw = pygame.image.load('data/images/menu_background.png').convert()
        self.background = pygame.transform.scale(background_raw, (360, 264))

        home_button_img = img_loader('data/images/button_pause.PNG', tile_size * 0.75, tile_size * 0.75)
        home_button_press = img_loader('data/images/button_pause_press.PNG', tile_size * 0.75, tile_size * 0.75)
        home_button_down = img_loader('data/images/button_pause_down.PNG', tile_size * 0.75, tile_size * 0.75)

        self.menu_button_bg = img_loader('data/images/pause_button_background.PNG', tile_size, tile_size)

        # buttons ------------------------------------------------------------------------------------------------------
        self.home_button = Button(swidth - tile_size + (tile_size - home_button_down.get_width()) / 2, 3,
                                  home_button_img, home_button_press, home_button_down)

        # lists --------------------------------------------------------------------------------------------------------
        self.default_power_list = ['regeneration', 'regeneration', 'regeneration', 'no harm', 'no harm', 'jump boost',
                                   'jump boost', 'no gravity', 'shockwave+', 'shockwave+']

        self.power_list = self.default_power_list
        self.eq_power_list = []
        self.backup_eq_power_list = []

        # loading in sounds --------------------------------------------------------------------------------------------
        pygame.mixer.music.load('data/sounds/gameplay_song.wav')
        pygame.mixer.music.set_volume(0.5)

        # variables ----------------------------------------------------------------------------------------------------
        self.level_check = 1

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

        self.int_map = False

        self.play_music = False
        self.fadeout = False
        self.menu_fadeout = False

        self.camera_move_x = 0
        self.camera_move_y = 0

        self.x = x
        self.y = y

        self.player_moved = False

        self.start_x = 2
        self.start_y = -4

        self.restart_level = False

        self.level_length = 0

        self.shockwave_radius = 0

        # initiating classes -------------------------------------------------------------------------------------------
        self.player = Player(x, y, screen)
        self.world = World(world_data, screen, slow_computer, self.start_x, self.start_y, bg_data)
        self.particles = Particles(particle_num, slow_computer)
        self.eq_manager = eqManager(self.eq_power_list)
        self.shockwave = Shockwave(screen)

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
            self.player_moved = self.player.update_pos_animation(screen,
                                                                 self.tile_list,
                                                                 self.world,
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
                                                                 self.shockwave_trigger,
                                                                 self.left_border,
                                                                 self.right_border,
                                                                 slow_computer,
                                                                 game_counter
                                                                 )

        # updating solid tile positions --------------------------------------------------------------------------------
        self.tile_list = self.world.update_tile_list(self.camera_move_x, self.camera_move_y)

        # blitting tiles and images in the background ------------------------------------------------------------------
        screen.blit(self.background, (0, 0))
        self.particles.bg_particles(screen, self.camera_move_x, self.camera_move_y)
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
        chosen_power, self.reinit_eq, play_lock_sound, self.power_list = self.world.draw_chest(screen, sack_rect,
                                                                                               fps_adjust,
                                                                                               self.power_list,
                                                                                               tutorial,
                                                                                               self.eq_power_list)

        # updating the world data if new level -------------------------------------------------------------------------
        if self.level_check < level_count or self.restart_level:
            world_data, bg_data = Game.level_checker(self, level_count, world_count)
            self.world = World(world_data, screen, slow_computer, self.start_x, self.start_y, bg_data)
            self.tile_list, self.level_length = self.world.return_tile_list()
            self.right_border = self.left_border + self.level_length * 32
            self.particles = Particles(particle_num, slow_computer)
            self.reinit_eq = True
            if not self.restart_level:
                self.level_check = level_count
                self.backup_eq_power_list = self.eq_power_list

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
        self.shockwave_radius, play_card_pull_sound2 = self.shockwave.update_shockwave(sack_rect, fps_adjust,
                                                                                       self.camera_move_x,
                                                                                       self.camera_move_y,
                                                                                       mouse_adjustment, self.health)

        # respawn instructions -----------------------------------------------------------------------------------------
        self.player.blit_respawn_instructions(screen, fps_adjust)

        # control instructions -----------------------------------------------------------------------------------------
        self.player.draw_inst_buttons(screen, fps_adjust, level_count)

        # eq full message ----------------------------------------------------------------------------------------------
        self.world.draw_eq_full(screen)

        # updating player health and blitting health bar ---------------------------------------------------------------
        play_card_pull_sound3 = self.player.update_health(screen, fps_adjust, mouse_adjustment)
        self.world.draw_portal_compass(sack_rect, screen)
        self.player.player_power_indicator(screen)

        if self.restart_level:
            self.eq_power_list = []
            self.eq_manager = eqManager(self.eq_power_list)
        if self.reinit_eq:
            self.eq_manager = eqManager(self.eq_power_list)
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
                                                          self.power_list, tutorial, fps_adjust)

        # resetting shockwave ------------------------------------------------------------------------------------------
        if self.shockwave_trigger:
            self.shockwave = Shockwave(screen)

        # menu button --------------------------------------------------------------------------------------------------
        menu, home_button_over = self.home_button.draw_button(screen, False, mouse_adjustment, events)
        if menu and not self.menu_fadeout:
            self.menu_fadeout = True
            self.fadeout = True

        # new level transition -----------------------------------------------------------------------------------------
        self.player.draw_transition(fps_adjust)

        # sounds -------------------------------------------------------------------------------------------------------
        if self.regeneration_trigger or self.mush_regeneration_trigger:
            play_healing_sound = True

        if play_card_pull_sound2 or play_card_pull_sound3:
            play_card_pull_sound = True

        # pygame.mouse.set_visible(False)

        return level_count, menu, play_card_pull_sound, play_lock_sound, play_bear_trap_cling_sound,\
            play_healing_sound, world_data, self.dead, bg_data, home_button_over, play_paper_sound, self.play_music,\
            self.fadeout
