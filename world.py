import pygame._sdl2
from bee import Bee
from bear_trap_class import BearTrap
from plant_spit import PlantSpit
from image_loader import img_loader
from font_manager import Text
from shockwave import Shockwave
from bat import Bat
from screen_info import swidth, sheight
from popup_bg_generator import popup_bg_generator
from popup import draw_popup
from random import choice, randrange, randint
import math
from json import load, dump

pygame.mixer.init()
pygame.init()

tile_size = 32

# this class is responsible for assigning tile images to their places on the screen
# it's functions draw the tiles and manage the interactive tiles of the game


def img_rect_pos(img, col_count, row_count, offset):
    rect = img.get_rect()
    rect.x = col_count * tile_size - offset
    rect.y = row_count * tile_size
    tile = [img, rect]
    return tile


def bg_img_rect_pos(img, col_count, row_count, offset):
    rect = img.get_rect()
    rect.x = col_count * tile_size / 2 - offset
    rect.y = row_count * tile_size / 2
    tile = [img, rect]
    return tile


def key_animation(img1, img2, counter, fps_adjust):
    counter += 1*fps_adjust
    if counter >= 30:
        img = img2
        if counter >= 40:
            counter = 0
    else:
        img = img1
    return counter, img


class CircleAnimation:
    def __init__(self):
        self.counter = -10
        self.radius1 = 0
        self.radius2 = 0
        self.max_radius = 25
        self.radius_speed = 2
        self.surface = pygame.Surface((tile_size * 2, tile_size * 2))
        self.surface.fill((0, 0, 0))
        self.surface.set_colorkey((0, 0, 0))
        self.surface.set_alpha(150)

    def draw_circle_animation(self, position, screen, fps_adjust):
        self.counter += 0.8 * fps_adjust
        self.radius_speed -= 0.1 * fps_adjust
        if self.radius_speed < 0:
            self.radius_speed = 0
        self.radius1 += self.radius_speed * fps_adjust
        if self.counter > 0:
            self.radius2 += 1.5 * fps_adjust

        width = self.radius1 - self.radius2

        if width > 0:
            self.surface.fill((0, 0, 0))
            pygame.draw.circle(self.surface, (255, 255, 255), (tile_size, tile_size), int(self.radius1), int(width))
            finished = False
        else:
            finished = True

        screen.blit(self.surface, (position[0] - tile_size / 2, position[1] - tile_size / 2))

        return finished


class World:
    def __init__(self, data, screen, slow_computer, bg_data, settings_counters, world_count):
        self.settings_counters = settings_counters

        self.data = data
        self.bg_data = bg_data

        self.screen = screen

        self.slow_computer = slow_computer

        self.world_count = world_count
        self.level_count = 1

        # lists (a lot of lists) ---------------------------------------------------------------------------------------
        self.main_tile_list = []
        self.main_fg_tile_list = []
        self.tile_list = []
        self.tile_pos_list = []
        self.updating_tile_list = []
        self.bg_tile_list = []
        self.bg_tile_pos_list = []
        self.next_level_list = []
        self.portal_list = []
        self.bear_trap_rect_list = []
        self.grn_mushroom_list = []
        self.bee_hive_list = []
        self.shut_trap_list = []
        self.slope_list = []
        self.decoration_list = []
        self.spitting_plant_list_left = []
        self.spitting_plant_list_right = []
        self.spitting_plant_list_up = []
        self.log_list = []
        self.bg_decoration_list = []
        self.wheat_list = []
        self.gem_list = []
        self.shockwave_mushroom_list = []
        self.shockwave_center_list = []
        self.set_lava_list = []
        self.hot_lava_list = []
        self.bridge_list = []
        self.bat_list = []
        self.copper_wheel_list = []
        self.pipe_list = []
        self.pipe_pos_list = []
        self.crate_pos_list = []
        self.freeze_tiles = []
        self.beans_list = []
        self.lamp_list = []
        self.chute_list = []
        self.hostile_rect_list = []
        self.spit_rect_list = []
        self.wheel_circle_hit_pos_list = []

        # variables ----------------------------------------------------------------------------------------------------
        self.bg_border = 0
        self.portal_counter = 0
        self.portal_part_counter = 0
        self.bee_release_counter = 400
        self.bee_counter = 0
        self.bee_harm = False
        self.spitting_counter = 0
        self.spit_list = []
        self.spit_particle_list = []
        self.log_counter = 0
        self.wood_num = 0
        self.playing_wheat_sound = False
        self.collectible_bob_counter = 0
        self.gem_flicker_counter = 0
        self.gem_equipped = False
        self.bridge_collapse_counter = 0
        self.bridge_collapsing = False
        self.bridge_collapsed = False
        self.bridge_collapse_cooldown = 10
        self.bridge_debris_list = []
        self.wood_particles = []
        self.gem_particles = []
        self.mush_particles = []
        self.shock_mush_part_anim_count = 0
        self.shock_mush_part_frame_len_count = 0
        self.copper_wheel_radius = 60
        self.copper_wheel_count = 0
        self.copper_wheel_frame = 0
        self.arrow_bob_counter = 0

        self.key_press_counter = 0

        self.sack_height = 32
        self.sack_width = 20

        self.background_x = 0
        self.background_y = 0

        self.bear_trap = BearTrap()

        self.level_length = 0
        self.level_height = 0

        self.portal_position = (0, 0)

        # load bean data
        try:
            with open('data/collected_beans.json', 'r') as json_file:
                self.collected_beans = load(json_file)
        except FileNotFoundError:
            self.collected_beans = [0]

        # tile images --------------------------------------------------------------------------------------------------
        self.dirt_tile = img_loader(f'data/images/tile_dirt.PNG', tile_size, tile_size)
        tile_dirt_edge = img_loader(f'data/images/tile_dirt_edge.PNG', tile_size, tile_size)
        tile_dirt_corner = img_loader(f'data/images/tile_dirt_corner.PNG', tile_size, tile_size)
        self.dirt_tile_rocks = img_loader(f'data/images/tile_dirt_rocks.PNG', tile_size, tile_size)
        dirt_tile_two_edges = img_loader(f'data/images/tile_dirt_two_edges.PNG', tile_size, tile_size)
        dirt_tile_top_edge = tile_dirt_edge
        dirt_tile_btm_edge = pygame.transform.flip(tile_dirt_edge, False, True)
        dirt_tile_right_edge = pygame.transform.rotate(tile_dirt_edge, 270)
        dirt_tile_left_edge = pygame.transform.rotate(tile_dirt_edge, 90)
        dirt_tile_left = tile_dirt_corner
        dirt_tile_right = pygame.transform.flip(tile_dirt_corner, True, False)
        dirt_tile_two_corners = img_loader(f'data/images/tile_dirt_two_corners.PNG', tile_size, tile_size)
        dirt_tile_btm_left = pygame.transform.flip(tile_dirt_corner, False, True)
        dirt_tile_btm_right = pygame.transform.flip(tile_dirt_corner, True, True)

        self.dirt_tiles = {
            (True, True, True, True): self.dirt_tile,
            (False, True, True, True): dirt_tile_top_edge,
            (True, False, True, True): dirt_tile_right_edge,
            (True, True, False, True): dirt_tile_btm_edge,
            (True, True, True, False): dirt_tile_left_edge,
            (False, True, True, False): dirt_tile_left,
            (False, False, True, True): dirt_tile_right,
            (True, False, False, True): dirt_tile_btm_right,
            (True, True, False, False): dirt_tile_btm_left,
            (True, False, True, False): dirt_tile_two_edges,
            (False, False, True, False): dirt_tile_two_corners,
        }

        self.stone_tile = img_loader(f'data/images/tile_stone.PNG', tile_size, tile_size)
        tile_stone_edge = img_loader(f'data/images/tile_stone_edge.PNG', tile_size, tile_size)
        tile_stone_corner = img_loader(f'data/images/tile_stone_corner.PNG', tile_size, tile_size)
        self.stone_tile_rocks = img_loader(f'data/images/tile_stone_rocks.PNG', tile_size, tile_size)
        stone_tile_two_edges = img_loader(f'data/images/tile_stone_two_edges.PNG', tile_size, tile_size)
        stone_tile_top_edge = tile_stone_edge
        stone_tile_btm_edge = pygame.transform.flip(tile_stone_edge, False, True)
        stone_tile_right_edge = pygame.transform.rotate(tile_stone_edge, 270)
        stone_tile_left_edge = pygame.transform.rotate(tile_stone_edge, 90)
        stone_tile_left = tile_stone_corner
        stone_tile_right = pygame.transform.flip(tile_stone_corner, True, False)
        stone_tile_two_corners = img_loader(f'data/images/tile_stone_two_corners.PNG', tile_size, tile_size)
        stone_tile_btm_left = pygame.transform.flip(tile_stone_corner, False, True)
        stone_tile_btm_right = pygame.transform.flip(tile_stone_corner, True, True)

        self.stone_tiles = {
            (True, True, True, True): self.stone_tile,
            (False, True, True, True): stone_tile_top_edge,
            (True, False, True, True): stone_tile_right_edge,
            (True, True, False, True): stone_tile_btm_edge,
            (True, True, True, False): stone_tile_left_edge,
            (False, True, True, False): stone_tile_left,
            (False, False, True, True): stone_tile_right,
            (True, False, False, True): stone_tile_btm_right,
            (True, True, False, False): stone_tile_btm_left,
            (True, False, True, False): stone_tile_two_edges,
            (False, False, True, False): stone_tile_two_corners,
        }

        self.brick_tile = img_loader('data/images/tile_brick.PNG', tile_size, tile_size)
        self.brick_tile_right_ext_edge = img_loader('data/images/tile_brick_ext_edge.PNG', tile_size, tile_size)
        self.brick_tile_left_ext_edge = pygame.transform.flip(self.brick_tile_right_ext_edge, True, False)
        brick_tile_floor_left = img_loader('data/images/tile_brick_floor_corner.PNG', tile_size, tile_size)
        brick_tile_floor_right = pygame.transform.flip(brick_tile_floor_left, True, False)
        brick_tile_corner = img_loader('data/images/tile_brick_corner.PNG', tile_size, tile_size)
        brick_tile_btm_right = pygame.transform.flip(brick_tile_corner, False, True)
        brick_tile_btm_left = pygame.transform.flip(brick_tile_btm_right, True, False)
        brick_tile_right_edge = img_loader('data/images/tile_brick_edge.PNG', tile_size, tile_size)
        brick_tile_left_edge = pygame.transform.flip(brick_tile_right_edge, True, False)
        brick_tile_top_edge = img_loader('data/images/tile_brick_top_edge.PNG', tile_size, tile_size)
        brick_tile_btm_edge = pygame.transform.rotate(brick_tile_right_edge, 270)
        brick_tile_two_edges = img_loader('data/images/tile_brick_two_edges.PNG', tile_size, tile_size)
        brick_tile_two_bottom_corners = pygame.transform.flip(img_loader('data/images/tile_brick_two_corners.PNG',
                                                                         tile_size, tile_size), False, True)

        brick_pass_right = img_loader('data/images/brick_passage_right_fg.PNG', tile_size, tile_size)
        brick_pass_right_bg = img_loader('data/images/brick_passage_right_bg.PNG', tile_size, tile_size)
        brick_pass_left = img_loader('data/images/brick_passage_left_fg.PNG', tile_size, tile_size)
        brick_pass_left_bg = img_loader('data/images/brick_passage_left_bg.PNG', tile_size, tile_size)
        self.brick_pass = brick_pass_right

        self.foundations_floor = img_loader('data/images/tile_foundations_floor.PNG', tile_size, tile_size)
        self.foundations = img_loader('data/images/tile_foundations.PNG', tile_size, tile_size)

        self.brick_tiles = {
            (True, True, True, True): self.brick_tile,
            (False, True, True, True): brick_tile_top_edge,
            (True, False, True, True): brick_tile_right_edge,
            (True, True, False, True): brick_tile_btm_edge,
            (True, True, True, False): brick_tile_left_edge,
            (False, True, True, False): brick_tile_floor_left,
            (False, False, True, True): brick_tile_floor_right,
            (True, False, False, True): brick_tile_btm_right,
            (True, True, False, False): brick_tile_btm_left,
            (True, False, True, False): brick_tile_two_edges,
            (True, False, False, False): brick_tile_two_bottom_corners,
            (True, False, False, False): brick_tile_two_edges,
        }

        self.passage_brick_tiles_bg = {
            'left': brick_pass_left_bg,
            'right': brick_pass_right_bg
        }

        self.passage_brick_tiles_fg = {
            'left': brick_pass_left,
            'right': brick_pass_right,
        }

        self.roof_tiles = img_loader('data/images/tile_roof.PNG', tile_size, tile_size)
        self.roof_tiles_left = img_loader('data/images/tile_roof_corner_left.PNG', tile_size, tile_size)
        self.roof_tiles_right = img_loader('data/images/tile_roof_corner_right.PNG', tile_size, tile_size)

        #    0
        # 3 [] 1
        #   2

        # bear trap tile images ----------------------------------------------------------------------------------------
        self.bear_trap_shut_img = img_loader('data/images/bear_trap_shut.PNG', tile_size, tile_size / 2)

        # portal tile images -------------------------------------------------------------------------------------------
        self.portal = img_loader('data/images/portal.PNG', tile_size, tile_size)
        self.portal_part_list = []
        self.portal.set_colorkey((0, 0, 0))

        # platform img -------------------------------------------------------------------------------------------------
        self.platform = img_loader('data/images/platform.PNG', tile_size, tile_size)

        # shockwave mushroom tile images -------------------------------------------------------------------------------
        self.shockwave_mushroom = img_loader('data/images/shockwave_mushroom.PNG', tile_size, tile_size / 2)
        self.shockwave_mushroom_dark = img_loader('data/images/shockwave_mushroom_dark.PNG', tile_size, tile_size / 2)
        # shockwave mushroom particle animation
        self.mush_part_anim_left = []
        self.mush_part_anim_right = []
        for frame in range(1, 9):
            img = img_loader(f'data/images/mush_part_animation/mushroom_particles{frame}.PNG', 16, 8)
            self.mush_part_anim_left.append(img)
            self.mush_part_anim_right.append(pygame.transform.flip(img, True, False))

        # green mushroom -----------------------------------------------------------------------------------------------
        self.green_mushroom = img_loader('data/images/green_mushroom.PNG', tile_size / 2, tile_size / 2)

        # gem ----------------------------------------------------------------------------------------------------------
        self.gem = img_loader('data/images/gem.PNG', tile_size / 2, tile_size / 2)
        self.gem.set_colorkey((0, 0, 0))
        self.gem_surface = pygame.Surface((tile_size / 2, tile_size / 2)).convert()
        gem_mask = pygame.mask.from_surface(self.gem)
        self.gem_mask_surf = pygame.mask.Mask.to_surface(gem_mask, setcolor=(255, 0, 0)).convert_alpha()
        self.gem_outline = gem_mask.outline()
        self.gem_dotted_outline = gem_mask.outline(3)
        self.gem_outline_surface = pygame.Surface((tile_size / 2, tile_size / 2)).convert()
        self.gem_outline_surface.set_colorkey((0, 0, 0))
        for pixel in self.gem_outline:
            self.gem_outline_surface.set_at(pixel, (255, 255, 255))
        self.gem_mask_surf.set_colorkey((255, 0, 0))

        # background dirt tiles ----------------------------------------------------------------------------------------
        self.bg_tile = img_loader('data/images/bg_tile.PNG', tile_size / 2, tile_size / 2)
        bg_tile_edge = img_loader('data/images/bg_tile_edge.PNG', tile_size / 2, tile_size / 2)
        bg_tile_corner = img_loader('data/images/bg_tile_corner.PNG', tile_size / 2, tile_size / 2)

        #    0
        # 3 [] 1
        #   2

        self.bg_dirt_tiles = {
            (True, True, True, True): self.bg_tile,
            (False, True, True, True): bg_tile_edge,
            (True, False, True, True): pygame.transform.rotate(bg_tile_edge, 270),
            (True, True, False, True): pygame.transform.rotate(bg_tile_edge, 180),
            (True, True, True, False): pygame.transform.rotate(bg_tile_edge, 90),
            (False, False, True, True): pygame.transform.flip(bg_tile_corner, True, False),
            (True, False, False, True): pygame.transform.rotate(bg_tile_corner, 180),
            (True, True, False, False): pygame.transform.flip(bg_tile_corner, False, True),
            (False, True, True, False): bg_tile_corner,
        }

        self.bg_dark_tile = img_loader('data/images/bg_dark_tile.PNG', tile_size / 2, tile_size / 2)
        bg_dark_tile_edge = img_loader('data/images/bg_dark_tile_edge.PNG', tile_size / 2, tile_size / 2)
        bg_dark_tile_corner = img_loader('data/images/bg_dark_tile_corner.PNG', tile_size / 2, tile_size / 2)

        self.bg_dark_tiles = {
            (True, True, True, True): self.bg_dark_tile,
            (False, True, True, True): bg_dark_tile_edge,
            (True, False, True, True): pygame.transform.rotate(bg_dark_tile_edge, 270),
            (True, True, False, True): pygame.transform.rotate(bg_dark_tile_edge, 180),
            (True, True, True, False): pygame.transform.rotate(bg_dark_tile_edge, 90),
            (False, False, True, True): pygame.transform.flip(bg_dark_tile_corner, True, False),
            (True, False, False, True): pygame.transform.rotate(bg_dark_tile_corner, 180),
            (True, True, False, False): pygame.transform.flip(bg_dark_tile_corner, False, True),
            (False, True, True, False): bg_dark_tile_corner,
        }

        self.bg_brick_tile = img_loader('data/images/tile_bg_brick.PNG', tile_size, tile_size)
        self.bg_brick_danger = img_loader('data/images/tile_bg_brick_danger.PNG', tile_size, tile_size)
        self.bg_brick_chute = img_loader('data/images/tile_bg_brick_chute.PNG', tile_size, tile_size)
        self.bg_brick_window = img_loader('data/images/tile_bg_brick_window.PNG', tile_size, tile_size)
        self.bg_brick_support = img_loader('data/images/tile_bg_brick_support1.PNG', tile_size, tile_size)
        self.bg_brick_support_top = img_loader('data/images/tile_bg_brick_support2.PNG', tile_size, tile_size)

        # bee hive tile images -----------------------------------------------------------------------------------------
        self.bee_hive = img_loader('data/images/bee_hive.PNG', tile_size, 1.5 * tile_size)
        self.bee_hive.set_colorkey((0, 0, 0))
        self.bee_bar = pygame.Surface((20, 3))
        self.bee_bar.fill((10, 10, 10))
        self.honey_colour = (192, 163, 10)

        # crate --------------------------------------------------------------------------------------------------------
        self.crate = img_loader('data/images/crate.PNG', 22, 22)

        # bush tiles ---------------------------------------------------------------------------------------------------
        self.bush = img_loader('data/images/bush1.PNG', 2 * tile_size, 2 * tile_size)
        self.bush_img = self.bush

        # rock tiles ---------------------------------------------------------------------------------------------------
        self.rock1 = img_loader('data/images/rock1.PNG', tile_size, tile_size)
        self.rock2 = img_loader('data/images/rock2.PNG', tile_size, tile_size)

        # tree tiles ---------------------------------------------------------------------------------------------------
        self.tree = img_loader('data/images/tree.PNG', 2 * tile_size, 2 * tile_size)
        self.birch_tree = img_loader('data/images/tree_birch.PNG', tile_size, tile_size * 3)

        # bridge tiles -------------------------------------------------------------------------------------------------
        self.bridge_section = img_loader('data/images/platform.PNG', tile_size, tile_size)
        self.bridge_support_left = img_loader('data/images/bridge_support.PNG', tile_size, tile_size)
        self.bridge_support_right = pygame.transform.flip(self.bridge_support_left, True, False)

        # debris = [image, position, velocity, rotation, rotation_speed, alpha, fadeout_counter]
        self.default_debris_list = []
        deb1 = [self.bridge_section.copy(), [0, 0], 3, 0, -8, 255, 5]
        deb2 = [self.bridge_section.copy(), [0, 0], 4, 0, 3, 255, 4]
        deb3 = [self.bridge_section.copy(), [0, 0], 2, 0, 7, 255, 5]
        self.default_debris_list = [deb1, deb2, deb3]

        # foliage tile images ------------------------------------------------------------------------------------------
        self.short_grass = img_loader('data/images/short_grass.PNG', tile_size, tile_size)
        self.short_grass_left = img_loader('data/images/short_grass_left.PNG', tile_size, tile_size)
        self.short_grass_right = img_loader('data/images/short_grass_right.PNG', tile_size, tile_size)
        self.short_flowers_together = img_loader('data/images/short_flowers_together.PNG', tile_size, tile_size)

        # spitting plant tile images -----------------------------------------------------------------------------------
        self.spitting_plant0_raw = pygame.image.load('data/images/spitting_plant0.PNG').convert()
        self.spitting_plant0l = img_loader('data/images/spitting_plant0.PNG', tile_size, tile_size)
        self.spitting_plant1l = img_loader('data/images/spitting_plant1.PNG', tile_size, tile_size)
        self.spitting_plant2l = img_loader('data/images/spitting_plant2.PNG', tile_size, tile_size)
        self.spitting_plant0r = pygame.transform.flip(self.spitting_plant0l, True, False)
        self.spitting_plant1r = pygame.transform.flip(self.spitting_plant1l, True, False)
        self.spitting_plant2r = pygame.transform.flip(self.spitting_plant2l, True, False)
        self.spitting_plant_up0_raw = pygame.image.load('data/images/spitting_plant_up0.PNG').convert()
        self.spitting_plant_up0 = img_loader('data/images/spitting_plant_up0.PNG', tile_size, tile_size)
        self.spitting_plant_up1 = img_loader('data/images/spitting_plant_up1.PNG', tile_size, tile_size)
        self.spitting_plant_up2 = img_loader('data/images/spitting_plant_up2.PNG', tile_size, tile_size)
        self.spitting_plant_img_up = self.spitting_plant_up0
        self.spitting_plant_img_right = self.spitting_plant0r
        self.spitting_plant_img_left = self.spitting_plant0l

        # log frames ---------------------------------------------------------------------------------------------------
        self.log0 = img_loader('data/images/log0.PNG', 2 * tile_size, tile_size)
        self.log1 = img_loader('data/images/log1.PNG', 2 * tile_size, tile_size)
        self.log1.set_colorkey((0, 0, 0))

        # copper wheel frames ------------------------------------------------------------------------------------------
        self.copper_wheel_frames = {}
        index_count = 0
        for frame in range(7):
            img = img_loader(f'data/images/copper_wheel{index_count + 1}.PNG', tile_size * 4, tile_size * 4)
            self.copper_wheel_frames[index_count] = img
            index_count += 1

        # copper pipe images -------------------------------------------------------------------------------------------
        pipe_vertical = img_loader('data/images/pipe1.PNG', tile_size, tile_size)  # |
        self.pipe = pipe_vertical.copy()
        pipe_bend = img_loader('data/images/pipe2.PNG', tile_size, tile_size)  # ¬
        pipe_cross = img_loader('data/images/pipe3.PNG', tile_size, tile_size)  # -|
        pipe_end = img_loader('data/images/pipe4.PNG', tile_size, tile_size)  # i
        self.copper_pipe_imgs = {
            (True, False, True, False): pipe_vertical,
            (False, True, False, True): pygame.transform.rotate(pipe_vertical, 90),
            (False, False, True, True): pipe_bend,
            (False, True, True, False): pygame.transform.flip(pipe_vertical, True, False),
            (True, False, False, True): pygame.transform.rotate(pipe_bend, -90),
            (True, True, False, False): pygame.transform.rotate(pipe_bend, 180),
            (False, True, True, False): pygame.transform.flip(pipe_bend, True, False),
            (True, False, False, False): pygame.transform.flip(pipe_end, False, True),
            (False, True, False, False): pygame.transform.rotate(pipe_end, 90),
            (False, False, True, False): pipe_end,
            (False, False, False, True): pygame.transform.rotate(pipe_end, -90),
            (True, False, True, True): pipe_cross,
            (False, True, True, True): pygame.transform.rotate(pipe_cross, 90),
            (True, True, True, False): pygame.transform.rotate(pipe_cross, 180),
            (True, True, False, True): pygame.transform.rotate(pipe_cross, 270),
        }

        # wheat --------------------------------------------------------------------------------------------------------
        self.wheat = img_loader('data/images/wheat.PNG', 3, 40)

        # grain chute --------------------------------------------------------------------------------------------------
        self.grain_chute = img_loader('data/images/grain_chute.PNG', tile_size * 2, tile_size * 5)

        # lamp ---------------------------------------------------------------------------------------------------------
        self.lamp = img_loader('data/images/lamp.PNG', 13, 9)
        self.lamp_direction = 1

        # lava ---------------------------------------------------------------------------------------------------------
        self.set_lava = img_loader('data/images/lava.PNG', tile_size, 5)
        self.set_lava2 = img_loader('data/images/lava2.PNG', tile_size, 5)
        self.set_lava_left = img_loader('data/images/lava_edge.PNG', tile_size, 5)
        self.set_lava_right = pygame.transform.flip(self.set_lava_left, True, False)
        self.molten_lava = pygame.Surface((tile_size, tile_size - 7)).convert()
        self.molten_lava.fill((66, 3, 3))
        self.set_lava_img_list = []
        self.set_lava_rect = self.set_lava.get_rect()

        # buildings ---------------------------------------------------------------------------------------------------
        self.greenhouse = img_loader('data/images/greenhouse.PNG', tile_size * 3, tile_size * 2)
        self.greenhouse_glazing = img_loader('data/images/greenhouse_glazing.PNG', tile_size * 3, tile_size * 2)
        self.cottage = img_loader('data/images/cottage.PNG', tile_size * 6, tile_size * 4)
        self.mill = img_loader('data/images/mill.PNG', tile_size * 8, tile_size * 6)
        self.garage = img_loader('data/images/garage.PNG', tile_size * 4, tile_size * 3)

        # beans --------------------------------------------------------------------------------------------------------
        self.beans = img_loader('data/images/beans.PNG', 13, 20)
        self.beans_popup = popup_bg_generator((60, 15))
        self.beans_popup_counter = 0

        # guidance arrows and keys -------------------------------------------------------------------------------------
        self.white_arrow_up = img_loader('data/images/white_arrow.PNG', tile_size / 2, tile_size / 2)
        self.white_arrow_down = pygame.transform.flip(self.white_arrow_up, False, True)

        # compass card -------------------------------------------------------------------------------------------------
        self.compass_card = img_loader('data/images/health_bar_card.PNG', tile_size * 2, tile_size * 2)

        # text ---------------------------------------------------------------------------------------------------------
        eq_full_text = Text()
        self.eq_full_txt = eq_full_text.make_text(['eq is full, bin cards to free up space'])

    def create_world(self, start_x, start_y, data, bg_data, level_count, world_count):

        # lists (a lot of lists) ---------------------------------------------------------------------------------------
        self.main_tile_list = []
        self.main_fg_tile_list = []
        self.tile_list = []
        self.tile_pos_list = []
        self.updating_tile_list = []
        self.bg_tile_list = []
        self.bg_tile_pos_list = []
        self.next_level_list = []
        self.portal_list = []
        self.spitting_plant_list_left = []
        self.spitting_plant_list_right = []
        self.spitting_plant_list_up = []
        self.bear_trap_rect_list = []
        self.grn_mushroom_list = []
        self.bee_hive_list = []
        self.shut_trap_list = []
        self.decoration_list = []
        self.log_list = []
        self.bg_decoration_list = []
        self.wheat_list = []
        self.gem_list = []
        self.shockwave_mushroom_list = []
        self.set_lava_list = []
        self.hot_lava_list = []
        self.bridge_list = []
        self.bat_list = []
        self.copper_wheel_list = []
        self.pipe_list = []
        self.pipe_pos_list = []
        self.crate_pos_list = []
        self.freeze_tiles = []
        self.beans_list = []
        self.lamp_list = []
        self.chute_list = []
        self.hostile_rect_list = []
        self.spit_rect_list = []
        self.wheel_circle_hit_pos_list = []

        # variables ----------------------------------------------------------------------------------------------------
        self.portal_counter = 0
        self.portal_part_counter = 0
        self.bee_release_counter = 400
        self.bee_counter = 0
        self.bee_harm = False
        self.spitting_counter = 0
        self.spit_list = []
        self.spit_particle_list = []
        self.log_counter = 0
        self.wood_num = 0
        self.playing_wheat_sound = False
        self.bridge_collapse_counter = 0
        self.bridge_collapsing = False
        self.bridge_collapsed = False
        self.bridge_collapse_cooldown = 10
        self.bridge_debris_list = []
        self.wood_particles = []
        self.mush_particles = []
        self.gem_particles = []
        self.copper_wheel_radius = 60

        # assigning tiles to corresponding coordinates by the level map ------------------------------------------------
        self.level_height = 0

        self.data = data
        self.bg_data = bg_data

        # load bean data
        try:
            with open('data/collected_beans.json', 'r') as json_file:
                self.collected_beans = load(json_file)
        except FileNotFoundError:
            self.collected_beans = [0]

        self.level_count = level_count
        self.world_count = world_count

        # bean popup
        self.beans_popup = popup_bg_generator((60, 15))
        bean_text = Text().make_text([f'{self.collected_beans[0] + 1} of 9'])
        self.beans_popup.blit(bean_text, (30, 7))
        self.beans_popup_counter = 400

        # TILE DATA ENCODING SYSTEM ====================================================================================

        # 6 - garage
        # 7 - greenhouse
        # 8 - cottage
        # 9 - mill
        # 10 - gem
        # 11 - dirt
        # 12 - stone
        # 13 - bricks
        # 14 - rocks 1
        # 15 - rocks 2
        # 16 - charge bat spawn
        # 17 - laser bat spawn
        # 18 - wheat
        # 19 - bridge
        # 20 - portal
        # 21 - copper wheel
        # 22 - pipe
        # 23 - bear trap
        # 24 - platform
        # 25 - wobbly mushrooms
        # 26 - hot lava start
        # 27 - hot lava stop
        # 28 - bee hive
        # 29 - shockwave mushroom
        # 30 - set lava
        # 31 - set lava left
        # 32 - set lava right
        # 33 - short grass
        # 34 - short grass left
        # 35 - short grass right
        # 36 - bush
        # 37 - spitting plant left
        # 38 - spitting plant right
        # 39 - spitting plant up
        # 40 - log
        # 41 - birch tree
        # 42 - tree
        # 43 - flowers
        # 44 - crate
        # 45 - beans
        # 46 - lamp

        lava_start = []

        # static lists:
        # • tile_list
        # • decoration_list
        # • set_lava_list
        # • bg_tile_list
        # • bg_decoration_list

        pov_offset = (480 - swidth) / 2

        self.tile_surface_pos = [start_x * tile_size - pov_offset, start_y * tile_size]

        row_count = start_y
        tile_row = 0
        for row in self.data:
            column_count = start_x
            tile_column = 0
            self.level_length = 0
            for tile in row:
                if tile == 99:
                    # background transition border
                    self.bg_border = row_count * tile_size
                if tile == 98:
                    # first speed dash freeze (jump)
                    pos = [column_count * tile_size - pov_offset, row_count * tile_size]
                    tile = [pos, 'sd1']
                    self.freeze_tiles.append(tile)
                if tile == 97:
                    # second speed dash freeze (dash)
                    pos = [column_count * tile_size - pov_offset, row_count * tile_size]
                    tile = [pos, 'sd2']
                    self.freeze_tiles.append(tile)
                if tile == 96:
                    # speed dash lock
                    pos = [column_count * tile_size - pov_offset, row_count * tile_size]
                    tile = [pos, 'sd0']
                    self.freeze_tiles.append(tile)
                if tile == 95:
                    # grian chute
                    rect = pygame.rect.Rect(column_count * tile_size - pov_offset,
                                            row_count * tile_size + tile_size,
                                            tile_size * 2, tile_size * 2)
                    tile = ['chute', rect]
                    self.chute_list.append(tile)
                    self.next_level_list.append(tile)
                if tile == 6:
                    # garage
                    tile = img_rect_pos(self.garage, column_count, row_count, pov_offset)
                    self.bg_decoration_list.append(tile)
                if tile == 7:
                    # greenhouse
                    tile = img_rect_pos(self.greenhouse, column_count, row_count, pov_offset)
                    self.bg_decoration_list.append(tile)
                if tile == 8:
                    # cottage
                    tile = img_rect_pos(self.cottage, column_count, row_count, pov_offset)
                    self.bg_decoration_list.append(tile)
                if tile == 9:
                    # mill
                    tile = img_rect_pos(self.mill, column_count, row_count, pov_offset)
                    self.bg_decoration_list.append(tile)
                if tile == 10:
                    # gem
                    tile_type = 'gem'
                    if [self.world_count, level_count] in [[3, 4], [3, 5], [3, 6], [4, 7], [5, 3]]:
                        offset = tile_size / 2
                    else:
                        offset = 0
                    if [self.world_count, level_count] in [[3, 4], [3, 5], [3, 6], [4, 7], [5, 3]]:
                        rect = pygame.Rect(0, 0, tile_size, tile_size)
                        rect.x = column_count * tile_size - pov_offset
                        rect.y = row_count * tile_size + offset
                    else:
                        rect = self.gem.get_rect()
                        rect.x = column_count * tile_size + 8 - pov_offset
                        rect.y = row_count * tile_size + 8 + offset
                    shake_counter = 7
                    surface = pygame.surface.Surface((tile_size / 2, tile_size / 2))
                    surface.set_colorkey((0, 0, 0))
                    animation = CircleAnimation()
                    gem_collected = False
                    gem_counter = 0
                    tile = [tile_type, rect, shake_counter, gem_collected, surface, animation, gem_counter]
                    self.gem_list.append(tile)
                if tile == 11:
                    # dirt
                    tile = img_rect_pos(self.dirt_tile, column_count, row_count, pov_offset)
                    tile.append('grass')
                    tile.append([(column_count - start_x) * tile_size, (row_count - start_y) * tile_size])
                    self.tile_pos_list.append([tile[1].x, tile[1].y])
                    self.bg_tile_pos_list.append([tile[1].x, tile[1].y])
                    self.bg_tile_pos_list.append([tile[1].x + 16, tile[1].y])
                    self.bg_tile_pos_list.append([tile[1].x, tile[1].y + 16])
                    self.bg_tile_pos_list.append([tile[1].x + 16, tile[1].y + 16])
                    self.tile_list.append(tile)
                if tile == 12:
                    # stone
                    tile = img_rect_pos(self.stone_tile, column_count, row_count, pov_offset)
                    tile.append('rock')
                    tile.append([tile_column * tile_size, tile_row * tile_size])
                    self.tile_pos_list.append([tile[1].x, tile[1].y])
                    self.bg_tile_pos_list.append([tile[1].x, tile[1].y])
                    self.bg_tile_pos_list.append([tile[1].x + 16, tile[1].y])
                    self.bg_tile_pos_list.append([tile[1].x, tile[1].y + 16])
                    self.bg_tile_pos_list.append([tile[1].x + 16, tile[1].y + 16])
                    self.tile_list.append(tile)
                if tile == 13:
                    # bricks
                    tile = img_rect_pos(self.brick_tile, column_count, row_count, pov_offset)
                    tile.append('wood')
                    tile.append([tile_column * tile_size, tile_row * tile_size])
                    self.tile_pos_list.append([tile[1].x, tile[1].y])
                    self.bg_tile_pos_list.append([tile[1].x, tile[1].y])
                    self.bg_tile_pos_list.append([tile[1].x + 16, tile[1].y])
                    self.bg_tile_pos_list.append([tile[1].x, tile[1].y + 16])
                    self.bg_tile_pos_list.append([tile[1].x + 16, tile[1].y + 16])
                    self.tile_list.append(tile)
                if tile == 14:
                    # rock 1
                    tile = img_rect_pos(self.rock1, column_count, row_count, pov_offset)
                    self.bg_decoration_list.append(tile)
                if tile == 15:
                    # rock 2
                    tile = img_rect_pos(self.rock2, column_count, row_count, pov_offset)
                    self.bg_decoration_list.append(tile)
                if tile in [16, 17]:
                    # bat spawn
                    bat = Bat((column_count * tile_size + 18, row_count * tile_size + 11))
                    bat_pack = [bat, tile]
                    self.bat_list.append(bat_pack)

                if tile == 18:
                    # wheat
                    wheat_spacer = 4
                    local_list = []
                    for num in range(8):
                        rect = self.wheat.get_rect()
                        rect.y = (row_count * tile_size) + randrange(0, 6)
                        rect.x = (column_count * tile_size) + wheat_spacer * num - pov_offset
                        counter = randrange(0, 200)
                        package = [rect, counter]
                        local_list.append(package)
                    self.wheat_list.append(local_list)
                if tile == 19:
                    # bridge
                    tile = img_rect_pos(self.bridge_section, column_count, row_count, pov_offset)
                    tile.append('wood')
                    self.tile_list.append(tile)
                if tile == 20:
                    # portal
                    tile_type = 'portal'
                    img1 = self.portal
                    img1.set_colorkey((0, 0, 0))
                    img1_rectangle = img1.get_rect()
                    img1_rectangle.x = column_count * tile_size - pov_offset
                    img1_rectangle.y = row_count * tile_size
                    star_surface = pygame.Surface((tile_size, tile_size * 1.5)).convert()
                    star_surface.fill((1, 1, 1))
                    star_surface.set_colorkey((0, 0, 0))
                    stars = []  # position, speed, colour
                    for star in range(30):
                        stars.append([[randrange(0, tile_size - 1),
                                       randrange(0, int(tile_size * 1.5 - 1))],
                                      choice([1/8, 2/8]),
                                      choice([(255, 0, 255), (143, 0, 255)])])
                    portal_surface = pygame.Surface((tile_size, tile_size * 1.5)).convert()
                    portal_surface.set_colorkey((0, 0, 255))
                    tile = (tile_type, img1_rectangle, portal_surface, star_surface, stars)
                    self.next_level_list.append(tile)
                    self.portal_list.append(tile)
                    self.portal_position = (img1_rectangle[0], img1_rectangle[1])
                if tile == 21:
                    # copper wheel
                    tile_type = 'copper_wheel'
                    x = column_count * tile_size - pov_offset
                    y = row_count * tile_size
                    rect = pygame.Rect(x, y, tile_size * 4, tile_size * 4)
                    if level_count > 3 or world_count == 5:
                        boxes = [0, 90, 180, 270]
                    else:
                        boxes = [0, 180]
                    # tile[-1] -> stop the wheel after dying from it
                    tile = [tile_type, rect, boxes, False]
                    self.copper_wheel_list.append(tile)
                if tile == 22:
                    # copper pipe
                    tile = img_rect_pos(self.pipe, column_count, row_count, pov_offset)
                    self.pipe_list.append(tile)
                    self.pipe_pos_list.append([tile[1].x, tile[1].y])
                if tile == 23:
                    # bear trap
                    img = self.bear_trap_shut_img
                    img2 = pygame.transform.scale(img, (8, tile_size / 4))
                    img_rectangle = img2.get_rect()
                    img_rectangle.x = (column_count * tile_size) + 12 - pov_offset
                    img_rectangle.y = (row_count * tile_size) + 24
                    tile = (img, img_rectangle)
                    shut = False
                    self.hostile_rect_list.append(img_rectangle)
                    self.shut_trap_list.append(shut)
                    self.bear_trap_rect_list.append(tile)
                if tile == 24:
                    # platform
                    img = self.platform
                    dimension_img = pygame.transform.scale(img, (tile_size, tile_size/4))
                    img_rectangle = dimension_img.get_rect()
                    img_rectangle.x = column_count * tile_size - pov_offset
                    img_rectangle.y = row_count * tile_size
                    tile = [img, img_rectangle, 'wood', [tile_column * tile_size, tile_row * tile_size], 'platform']
                    self.tile_list.append(tile)
                if tile == 25:
                    # wobbly mushrooms
                    tall_rect = self.green_mushroom.get_rect()
                    short_rect = self.green_mushroom.get_rect()
                    medium_rect = self.green_mushroom.get_rect()
                    base_rect = self.short_grass.get_rect()
                    tall_rect.x = column_count * tile_size - pov_offset
                    tall_rect.y = row_count * tile_size + 14
                    short_rect.x = column_count * tile_size + 8 - pov_offset
                    short_rect.y = row_count * tile_size + 20
                    medium_rect.x = column_count * tile_size + 16 - pov_offset
                    medium_rect.y = row_count * tile_size + 17
                    base_rect.x = column_count * tile_size - pov_offset
                    base_rect.y = row_count * tile_size
                    tile = [base_rect, tall_rect, short_rect, medium_rect]
                    self.grn_mushroom_list.append(tile)
                if tile == 26:
                    # hot lava start
                    lava_start = [column_count * tile_size - pov_offset, row_count * tile_size]
                if tile == 27:
                    # hot lava stop
                    lava_stop = [column_count * tile_size + tile_size - pov_offset, row_count * tile_size]
                    len = lava_stop[0] - lava_start[0]
                    lava_surface = pygame.Surface((len, tile_size)).convert()
                    lava_surface.set_colorkey((0, 0, 0))
                    img = pygame.transform.scale(self.molten_lava, (len, tile_size - 7))
                    lava_surface.blit(img, (0, 7))
                    wave_counter = 0
                    wave_center = 0
                    collided = False
                    rect = pygame.Rect(lava_start[0], lava_start[1] + 10, len, tile_size - 10)
                    package = [lava_surface, lava_start, lava_stop, len, wave_counter, wave_center, collided, img, rect]
                    self.hot_lava_list.append(package)
                    self.hostile_rect_list.append(rect)
                if tile == 28:
                    # bee hive
                    tile_type = 'bee_hive'
                    img = self.bee_hive
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size - pov_offset
                    img_rectangle.y = row_count * tile_size + tile_size / 2
                    bee_list = []
                    for i in range(4):
                        bee = Bee(img_rectangle.x, img_rectangle.y)
                        bee_list.append(bee)
                    tile = (tile_type, img_rectangle, bee_list)
                    self.bee_hive_list.append(tile)
                if tile == 29:
                    # shockwave mushroom
                    tile_type = 'shockwave_mushroom'
                    img = self.shockwave_mushroom
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size - pov_offset
                    img_rectangle.y = row_count * tile_size + tile_size / 2
                    squash_counter = 0
                    cooldown = 0
                    shockwave_init = Shockwave(self.screen)
                    tile = [tile_type, img_rectangle, squash_counter, cooldown, shockwave_init]
                    self.shockwave_mushroom_list.append(tile)
                if tile == 30:
                    # set lava
                    tile_type = 'set_lava'
                    lava_img = choice([self.set_lava, self.set_lava2])
                    img = choice([lava_img, pygame.transform.flip(lava_img, True, False)])
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size - pov_offset
                    img_rect.y = row_count * tile_size + tile_size - 5
                    offset = 0
                    tile = (img, img_rect, offset, tile_type)
                    self.set_lava_list.append(tile)
                    self.hostile_rect_list.append(img_rect)
                if tile == 31:
                    # set lava left
                    tile_type = 'set_lava'
                    img = self.set_lava_left
                    img_rect = img.get_rect()
                    img_rect.width = tile_size - 10
                    img_rect.x = column_count * tile_size + 10 - pov_offset
                    img_rect.y = row_count * tile_size + tile_size - 5
                    offset = -10
                    tile = (img, img_rect, offset, tile_type)
                    self.set_lava_list.append(tile)
                    self.hostile_rect_list.append(img_rect)
                if tile == 32:
                    # set lava right
                    tile_type = 'set_lava'
                    img = self.set_lava_right
                    img_rect = img.get_rect()
                    img_rect.width = tile_size - 10
                    img_rect.x = column_count * tile_size - pov_offset
                    img_rect.y = row_count * tile_size + tile_size - 5
                    offset = 0
                    tile = (img, img_rect, offset, tile_type)
                    self.set_lava_list.append(tile)
                    self.hostile_rect_list.append(img_rect)
                if tile == 33:
                    # short grass
                    img = pygame.transform.scale(self.short_grass, (tile_size, tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size - pov_offset
                    img_rectangle.y = row_count * tile_size
                    tile = (img, img_rectangle)
                    self.decoration_list.append(tile)
                if tile == 34:
                    # short grass left
                    img = pygame.transform.scale(self.short_grass_left, (tile_size, tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size - pov_offset
                    img_rectangle.y = row_count * tile_size
                    tile = (img, img_rectangle)
                    self.decoration_list.append(tile)
                if tile == 35:
                    # short grass right
                    img = pygame.transform.scale(self.short_grass_right, (tile_size, tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size - pov_offset
                    img_rectangle.y = row_count * tile_size
                    tile = (img, img_rectangle)
                    self.decoration_list.append(tile)
                if tile == 36:
                    # bush
                    img_rectangle = self.bush.get_rect()
                    img_rectangle.x = column_count * tile_size - pov_offset
                    img_rectangle.y = row_count * tile_size
                    tile = (self.bush, img_rectangle)
                    self.bg_decoration_list.append(tile)
                if tile == 37:
                    # spitting plant left
                    tile_type = 'spitting_plant_left'
                    img = self.spitting_plant0l
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size - pov_offset
                    img_rectangle.y = row_count * tile_size
                    direction = 'left'
                    spit_list = []
                    for i in range(6):
                        plant_spit = PlantSpit(direction, img_rectangle.x, img_rectangle.y)
                        spit_list.append(plant_spit)
                    tile = (tile_type, img_rectangle, direction, spit_list)
                    self.spitting_plant_img_left = img
                    self.spitting_plant_list_left.append(tile)
                if tile == 38:
                    # spitting plant right
                    tile_type = 'spitting_plant_right'
                    img = self.spitting_plant0r
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size - pov_offset
                    img_rectangle.y = row_count * tile_size
                    direction = 'right'
                    spit_list = []
                    for i in range(6):
                        plant_spit = PlantSpit(direction, img_rectangle.x, img_rectangle.y)
                        spit_list.append(plant_spit)
                    tile = (tile_type, img_rectangle, direction, spit_list)
                    self.spitting_plant_img_right = img
                    self.spitting_plant_list_right.append(tile)
                if tile == 39:
                    # spitting plant up
                    tile_type = 'spitting_plant_up'
                    img = self.spitting_plant_up0
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size - pov_offset
                    img_rectangle.y = row_count * tile_size
                    direction = 'up'
                    spit_list = []
                    for i in range(6):
                        plant_spit = PlantSpit(direction, img_rectangle.x, img_rectangle.y)
                        spit_list.append(plant_spit)
                    tile = (tile_type, img_rectangle, direction, spit_list)
                    self.spitting_plant_img_up = img
                    self.spitting_plant_list_up.append(tile)
                if tile == 40:
                    # log
                    tile_type = 'log'
                    img = self.log0
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size - pov_offset
                    img_rectangle.y = row_count * tile_size + tile_size
                    tile = (tile_type, img_rectangle)
                    self.log_list.append(tile)
                if tile == 41:
                    # birch tree
                    img = self.birch_tree
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size - pov_offset
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.bg_decoration_list.append(tile)
                if tile == 42:
                    # tree
                    img = self.tree
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size - pov_offset
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.bg_decoration_list.append(tile)
                if tile == 43:
                    # short flowers together
                    img = self.short_flowers_together
                    img_rect = self.short_flowers_together.get_rect()
                    img_rect.x = column_count * tile_size - pov_offset
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.decoration_list.append(tile)
                if tile == 44:
                    # crate
                    tile = img_rect_pos(self.crate, column_count, row_count, pov_offset)
                    tile[1].x += 5
                    tile[1].y += 10
                    tile.append('wood')
                    self.tile_list.append(tile)
                    self.crate_pos_list.append([tile[1].x, tile[1].y])
                if tile == 45 and [world_count, level_count] not in self.collected_beans:
                    # beans
                    tile_type = 'beans'
                    rect = self.beans.get_rect()
                    rect.x = column_count * tile_size + 9
                    rect.y = row_count * tile_size + 6
                    beans_collected = False
                    collection_counter = 0
                    size_adder = 0
                    rotation = 0
                    speed = 0
                    tile = [tile_type, rect, beans_collected, collection_counter, size_adder, speed]
                    self.beans_list.append(tile)
                if tile == 46:
                    # lamp
                    tile_type = 'lamp'
                    x = column_count * tile_size - pov_offset
                    y = row_count * tile_size
                    rect = pygame.Rect(x, y, tile_size, tile_size * 1.5)
                    vel_x = 0
                    r = 25
                    s = [rect.x + (tile_size / 2 - 1), rect.y]
                    sine_counter = 0
                    tile = [tile_type, rect, vel_x, r, s, sine_counter]
                    self.lamp_list.append(tile)

                column_count += 1
                tile_column += 1
                self.level_length += 1
            row_count += 1
            tile_row += 1
            self.level_height += 1

        self.tile_surface_fg = pygame.Surface((self.level_length * tile_size, self.level_height * tile_size))
        self.tile_surface_fg.set_colorkey((0, 0, 0))
        self.tile_surface_bg = pygame.Surface((self.level_length * tile_size, self.level_height * tile_size))
        self.tile_surface_bg.set_colorkey((0, 0, 0))

        self.set_lava_img_list = [self.set_lava, self.set_lava2, pygame.transform.flip(self.set_lava, True, False),
                                  pygame.transform.flip(self.set_lava2, True, False), self.set_lava_left,
                                  self.set_lava_right]

        temp_tile_list = []
        removal_list = []

        for tile in self.tile_list:
            #    0
            # 3 [ ] 1
            #    2
            tile_edge_data = [True, True, True, True]
            # checking if there is a tile behind
            if [tile[1].x - tile_size, tile[1].y] not in self.tile_pos_list:
                tile_edge_data[3] = False
            # checking if there is a tile in front
            if [tile[1].x + tile_size, tile[1].y] not in self.tile_pos_list:
                tile_edge_data[1] = False
            # checking if there is a tile above
            if [tile[1].x, tile[1].y - tile_size] not in self.tile_pos_list:
                tile_edge_data[0] = False
            # checking if there is a tile beneath
            if [tile[1].x, tile[1].y + tile_size] not in self.tile_pos_list:
                tile_edge_data[2] = False

            if tile[0] == self.crate:
                if [tile[1].x, tile[1].y + tile_size] in self.crate_pos_list:
                    tile[1].y += 10

            if tile[0] == self.brick_tile:
                left_x = self.tile_list[0][1].x
                top_y = self.tile_list[0][1].y
                right_x = self.tile_list[-1][1].x
                btm_y = self.tile_list[-1][1].y

                if tile[1].x == left_x:
                    tile_edge_data[3] = True
                if tile[1].x == right_x:
                    tile_edge_data[1] = True
                if tile[1].y == top_y:
                    tile_edge_data[0] = True
                if tile[1].y == btm_y:
                    tile_edge_data[2] = True

            index = tuple(tile_edge_data)

            if tile[0] == self.dirt_tile:
                try:
                    tile[0] = self.dirt_tiles[index]
                except KeyError:
                    tile[0] = self.dirt_tile
            if tile[0] == self.stone_tile:
                try:
                    tile[0] = self.stone_tiles[index]
                except KeyError:
                    tile[0] = self.stone_tile
            if tile[0] == self.brick_tile:
                try:
                    tile[0] = self.brick_tiles[index]
                except KeyError:
                    tile[0] = self.brick_tile

            if tile[0] == self.bridge_section:
                self.bridge_list.append(tile)
            else:
                self.tile_surface_fg.blit(tile[0], (tile[1][0] - start_x * tile_size + pov_offset,
                                                    tile[1][1] - start_y * tile_size))

            if tile[0] != self.dirt_tile and tile[0] != self.stone_tile:
                temp_tile_list.append(tile)

        for tile in self.pipe_list:
            #    0
            # 3 [ ] 1
            #    2
            tile_edge_data = [True, True, True, True]

            pipe_pos_list = self.pipe_pos_list + self.tile_pos_list

            # checking if there is a tile behind
            if [tile[1].x - tile_size, tile[1].y] not in pipe_pos_list:
                tile_edge_data[3] = False
            # checking if there is a tile in front
            if [tile[1].x + tile_size, tile[1].y] not in pipe_pos_list:
                tile_edge_data[1] = False
            # checking if there is a tile above
            if [tile[1].x, tile[1].y - tile_size] not in pipe_pos_list:
                tile_edge_data[0] = False
            # checking if there is a tile beneath
            if [tile[1].x, tile[1].y + tile_size] not in pipe_pos_list:
                tile_edge_data[2] = False

            index = tuple(tile_edge_data)

            try:
                tile[0] = self.copper_pipe_imgs[index]
            except KeyError:
                tile[0] = self.pipe
            self.bg_decoration_list.append(tile)

        for tile in self.decoration_list:
            self.tile_surface_fg.blit(tile[0], (tile[1][0] - start_x * tile_size + pov_offset,
                                                tile[1][1] - start_y * tile_size))
        for tile in self.set_lava_list:
            self.tile_surface_fg.blit(tile[0], (tile[1][0] - start_x * tile_size + pov_offset + tile[-2],
                                                tile[1][1] - start_y * tile_size))

        self.tile_list = temp_tile_list
        # removing brick passage tiles from the tile list
        for tile in removal_list:
            self.tile_list.remove(tile)

        # background tiles ---------------------------------------------------------------------------------------------

        # 47 - background dirt tile
        # 48 - background stone tile
        # 49 - background brick tile
        # 50 - background brick way out tile
        # 51 - background brick window tile
        # 52 - background brick support

        bg_row_count = start_y * 2
        self.background_y = start_y * tile_size
        self.background_x = start_x * tile_size
        for row in self.bg_data:
            bg_col_count = start_x * 2
            for bg_tile in row:
                if bg_tile == 47:
                    # bg dirt tile
                    tile = bg_img_rect_pos(self.bg_tile, bg_col_count, bg_row_count, pov_offset)
                    self.bg_tile_list.append(tile)
                    self.bg_tile_pos_list.append([tile[1].x, tile[1].y])
                if bg_tile == 48:
                    # bg dark tile
                    tile = bg_img_rect_pos(self.bg_dark_tile, bg_col_count, bg_row_count, pov_offset)
                    self.bg_tile_list.append(tile)
                    self.bg_tile_pos_list.append([tile[1].x, tile[1].y])
                if bg_tile == 49:
                    # bg brick tile
                    tile = bg_img_rect_pos(self.bg_brick_tile, bg_col_count, bg_row_count, pov_offset)
                    self.bg_tile_list.append(tile)
                if bg_tile == 50:
                    # bg brick way out tile
                    if [world_count, level_count] == [4, 8]:
                        img = self.bg_brick_chute
                    else:
                        img = self.bg_brick_danger
                    tile = bg_img_rect_pos(img, bg_col_count, bg_row_count, pov_offset)
                    self.bg_tile_list.append(tile)
                if bg_tile == 51:
                    # bg brick window tile
                    tile = bg_img_rect_pos(self.bg_brick_window, bg_col_count, bg_row_count, pov_offset)
                    self.bg_tile_list.append(tile)
                if bg_tile == 52:
                    # bg brick support
                    tile = bg_img_rect_pos(self.bg_brick_support, bg_col_count, bg_row_count, pov_offset)
                    self.bg_tile_list.append(tile)

                bg_col_count += 1
            bg_row_count += 1

        for tile in self.bg_tile_list:
            #    0
            # 3 [ ] 1
            #    2
            tile_edge_data = [True, True, True, True]
            # checking if there is a tile behind
            if [tile[1].x - tile_size / 2, tile[1].y] not in self.bg_tile_pos_list:
                tile_edge_data[3] = False
            # checking if there is a tile in front
            if [tile[1].x + tile_size / 2, tile[1].y] not in self.bg_tile_pos_list:
                tile_edge_data[1] = False
            # checking if there is a tile above
            if [tile[1].x, tile[1].y - tile_size / 2] not in self.bg_tile_pos_list:
                tile_edge_data[0] = False
            # checking if there is a tile beneath
            if [tile[1].x, tile[1].y + tile_size / 2] not in self.bg_tile_pos_list:
                tile_edge_data[2] = False
            if tile[0] == self.bg_tile:
                try:
                    tile[0] = self.bg_dirt_tiles[tuple(tile_edge_data)]
                except KeyError:
                    tile[0] = self.bg_tile
            if tile[0] == self.bg_dark_tile:
                try:
                    tile[0] = self.bg_dark_tiles[tuple(tile_edge_data)]
                except KeyError:
                    tile[0] = self.bg_dark_tile
            if tile[0] == self.bg_brick_support:
                if [tile[1].x, tile[1].y - tile_size] in self.tile_pos_list:
                    tile[0] = self.bg_brick_support_top

            self.tile_surface_bg.blit(tile[0], (tile[1][0] - start_x * tile_size + pov_offset,
                                                tile[1][1] - start_y * tile_size))

        for tile in self.bg_decoration_list:
            self.tile_surface_bg.blit(tile[0], (tile[1][0] - start_x * tile_size + pov_offset,
                                                tile[1][1] - start_y * tile_size))

        bg_tiles = [self.spitting_plant_list_up, self.spitting_plant_list_left, self.spitting_plant_list_right,
                    self.set_lava_list, self.portal_list, self.gem_list, self.beans_list, self.log_list,
                    self.copper_wheel_list, self.lamp_list]

        for el in bg_tiles:
            self.main_tile_list += el

        fg_tiles = [self.shockwave_mushroom_list, self.bee_hive_list, self.chute_list]

        for el in fg_tiles:
            self.main_fg_tile_list += el

        self.updating_tile_list = self.tile_list + self.main_tile_list + self.main_fg_tile_list

        return self.level_length, self.level_height

    def return_tile_list(self):
        return self.tile_list, self.level_length

    # functions drawing and updating tile surfaces =====================================================================

    # updating the position of all tiles -------------------------------------------------------------------------------
    def update_tile_list(self, camera_move_x, camera_move_y):
        for tile in self.updating_tile_list:
            tile[1][0] += camera_move_x
            tile[1][1] += camera_move_y
            if tile[0] == 'lamp':
                tile[4][0] += camera_move_x
                tile[4][1] += camera_move_y

        for tile in self.freeze_tiles:
            tile[0][0] += camera_move_x
            tile[0][1] += camera_move_y

        self.tile_surface_pos[0] += camera_move_x
        self.tile_surface_pos[1] += camera_move_y

        self.bear_trap.bear_trap_update(camera_move_x, camera_move_y, self.bear_trap_rect_list)

        for mush in self.grn_mushroom_list:
            for num in range(4):
                mush[num][0] += camera_move_x
                mush[num][1] += camera_move_y

        for lava in self.hot_lava_list:
            lava[1][0] += camera_move_x
            lava[1][1] += camera_move_y
            lava[2][0] += camera_move_x
            lava[2][1] += camera_move_y
            lava[8][0] += camera_move_x
            lava[8][1] += camera_move_y

        for wheat_tile in self.wheat_list:
            for wheat in wheat_tile:
                wheat[0][0] += camera_move_x
                wheat[0][1] += camera_move_y

        self.bg_border += camera_move_y

        return self.tile_list

    # ------------------------------------------------------------------------------------------------------------------
    def draw_static_tiles_foreground(self, screen):
        screen.blit(self.tile_surface_fg, self.tile_surface_pos)

    # ------------------------------------------------------------------------------------------------------------------
    def draw_static_tiles_background(self, screen):
        screen.blit(self.tile_surface_bg, self.tile_surface_pos)

    # functions for drawing animated or interactive tiles and enemies ==================================================

    def update_bg_tiles(self, screen, fps_adjust, tutorial, camera_move_x, camera_move_y, sack_rect,
                        gem_equipped, health):
        harm = False
        update_wheel_angles = False
        # portal variables
        self.portal_counter += 1 * fps_adjust
        self.portal_part_counter += 1 * fps_adjust
        # gem variables
        self.collectible_bob_counter += 1 * fps_adjust
        self.gem_flicker_counter += 1 * fps_adjust
        if self.gem_flicker_counter >= 90:
            self.gem_flicker_counter = 0
        gem_sound = False
        # spitting plant variables
        spit_harm = False
        self.spitting_counter += 1 * fps_adjust
        self.spit_rect_list = []
        # log variables
        self.log_counter += 1 * fps_adjust
        # copper wheel variables
        self.wheel_circle_hit_pos_list = []
        self.copper_wheel_count += 1 * fps_adjust
        if self.copper_wheel_count > 3.5:
            self.copper_wheel_count = 0
            self.copper_wheel_frame += 1
            update_wheel_angles = True
        if self.copper_wheel_frame > 6:
            self.copper_wheel_frame = 0
        speed = -1.6

        # spit counters
        append_spit = False
        if self.spitting_counter >= 60:
            self.spitting_plant_img_up = self.spitting_plant_up2
            self.spitting_plant_img_left = self.spitting_plant2l
            self.spitting_plant_img_right = self.spitting_plant2r
            self.spitting_counter = 0
            append_spit = True
        elif self.spitting_counter >= 45:
            self.spitting_plant_img_up = self.spitting_plant_up1
            self.spitting_plant_img_left = self.spitting_plant1l
            self.spitting_plant_img_right = self.spitting_plant1r
        elif self.spitting_counter >= 30:
            self.spitting_plant_img_up = self.spitting_plant_up0
            self.spitting_plant_img_left = self.spitting_plant0l
            self.spitting_plant_img_right = self.spitting_plant0r
        elif self.spitting_counter >= 15:
            self.spitting_plant_img_up = self.spitting_plant_up1
            self.spitting_plant_img_left = self.spitting_plant1l
            self.spitting_plant_img_right = self.spitting_plant1r

        draw_circle = pygame.draw.circle
        draw_rect = pygame.draw.rect
        draw_line = pygame.draw.line
        blit = screen.blit
        collision_sack = sack_rect.colliderect

        for tile in self.main_tile_list:
            # portal ---------------------------------------------------------------------------------------------------
            if tile[0] == 'portal':
                if -tile_size < tile[1][0] < swidth and -tile_size < tile[1][1] < sheight:
                    portal_y_offset = math.sin((1 / 15) * self.portal_counter) * 2

                    tile[3].fill((1, 1, 1))
                    for star in tile[4]:
                        star[0][0] -= (camera_move_x * star[1])
                        star[0][1] -= (camera_move_y * star[1])
                        if star[0][0] > tile_size:
                            star[0][0] = 0
                            star[0][1] = randrange(0, int(tile_size * 1.5 - 1))
                        if star[0][0] < 0:
                            star[0][0] = tile_size
                            star[0][1] = randrange(0, int(tile_size * 1.5 - 1))
                        if star[0][1] > tile_size * 1.5:
                            star[0][1] = 0
                            star[0][0] = randrange(0, tile_size - 1)
                        if star[0][1] < 0:
                            star[0][1] = tile_size
                            star[0][0] = randrange(0, tile_size - 1)
                        tile[3].set_at((int(star[0][0]), int(star[0][1])), star[2])

                    tile[2].fill((0, 0, 0))
                    tile[2].blit(self.portal, (0, 8 + portal_y_offset))
                    if self.portal_part_counter > 5:
                        self.portal_part_counter = 0
                        # max radius, radius, radius achieved, pos
                        part_vars = [6, 0, False, (int(randrange(8, tile_size - 8)),
                                                   int(randrange(13, tile_size + 4)))]
                        self.portal_part_list.append(part_vars)
                    for part in self.portal_part_list:
                        if part[2]:
                            part[1] -= 0.15 * fps_adjust
                        else:
                            part[1] += 0.15 * fps_adjust
                        if part[1] >= part[0]:
                            part[2] = True
                        if part[1] < 0:
                            self.portal_part_list.remove(part)
                        pygame.draw.circle(tile[2], (0, 0, 255), part[3], part[1], 0)

                    tile[3].blit(tile[2], (0, 0))

                    portal_mask = pygame.mask.from_surface(tile[3])
                    portal_outline = pygame.mask.Mask.outline(portal_mask)
                    for pixel in portal_outline:
                        tile[3].set_at(pixel, (255, 255, 255))

                    blit(tile[3], (tile[1][0], tile[1][1] - 16))

                    if tutorial == 1:
                        blit(self.white_arrow_down, (tile[1][0] + 8, tile[1][1] - tile_size))
            # set lava -------------------------------------------------------------------------------------------------
            if (tile[1].width == self.set_lava_rect.width and tile[1].height == self.set_lava_rect.height) or \
                    tile[-1] == 'set_lava':
                if -tile_size < tile[1][0] < swidth:
                    if collision_sack(tile[1]):
                        harm = True

            # gem ------------------------------------------------------------------------------------------------------
            if tile[0] == 'gem':
                tile[4].fill((0, 0, 0))

                tile[6] -= 1 * fps_adjust

                tile[4].blit(self.gem, (0, 0))
                pygame.draw.line(tile[4], (255, 255, 255),
                                 (16, -10 + self.gem_flicker_counter), (0, self.gem_flicker_counter), 3)
                tile[4].blit(self.gem_mask_surf, (0, 0))
                img = tile[4]

                if collision_sack(tile[1]) and not tile[3] and tile[6] < 0:
                    tile[3] = True
                    gem_equipped = True
                    gem_sound = True

                scale = 1
                circle_animation_finished = False
                if tile[3]:
                    scale = (15 - abs(tile[2])) / 8
                    tile[2] -= 1.5 * fps_adjust
                    if scale > 0:
                        img = pygame.transform.scale(self.gem, (16 * scale, 16 * scale))
                    circle_animation_finished = tile[5].draw_circle_animation((tile[1][0] - (tile_size / 2 - tile[1].width / 2),
                                                                               tile[1][1] - (tile_size / 2 - tile[1].height / 2)),
                                                                              screen, fps_adjust)

                if circle_animation_finished:
                    tile[6] = 60 * 3
                    tile[2] = 7
                    tile[3] = False
                    tile[5] = CircleAnimation()

                gem_y_offset = math.sin((1 / 17) * self.collectible_bob_counter) * 3
                if scale > 0 > tile[6]:
                    if tile[6] > -10:
                        shake_offset_x = choice([-2, 0, 2])
                        shake_offset_y = choice([-2, 0, 2])
                    else:
                        shake_offset_x = 0
                        shake_offset_y = 0

                    blit(img,
                         (tile[1][0] + (tile[1].width / 2 - img.get_width() / 2) + shake_offset_x,
                          tile[1][1] + gem_y_offset + (tile[1].height / 2 - img.get_height() / 2) + shake_offset_y))
                elif tile[6] >= 0:
                    blit(self.gem_outline_surface,
                         (tile[1][0] + (tile[1].width / 2 - img.get_width() / 2),
                          tile[1][1] + gem_y_offset + (tile[1].height / 2 - img.get_height() / 2)))

            # beans ----------------------------------------------------------------------------------------------------
            if tile[0] == 'beans':
                self.beans_popup_counter += 1 * fps_adjust
                if collision_sack(tile[1]):
                    if not tile[2]:
                        try:
                            with open('data/collected_beans.json', 'w') as json_file:
                                bean_data = [self.world_count, self.level_count]
                                self.collected_beans.append(bean_data)
                                self.collected_beans[0] += 1
                                dump(self.collected_beans, json_file)
                        except FileNotFoundError:
                            pass
                        self.beans_popup_counter = -80
                    tile[2] = True
                beans_y_offset = math.sin((1 / 17) * (self.collectible_bob_counter + 4)) * 3
                if not tile[2]:
                    blit(self.beans, (tile[1][0], tile[1][1] + beans_y_offset))
                elif tile[1].y > -20:
                    tile[3] += 1 * fps_adjust
                    img = self.beans
                    if tile[3] < 10:
                        tile[4] += 0.8 * fps_adjust
                    if 30 > tile[3] > 10:
                        tile[4] -= 0.8 * fps_adjust
                    if 30 < tile[3] < 40:
                        tile[4] += 0.8 * fps_adjust
                        if tile[4] > 0:
                            tile[4] = 0
                    if tile[3] > 50:
                        tile[4] = 0
                        tile[5] += 0.1 * fps_adjust
                        tile[1].y -= tile[5]
                    if tile[3] < 20:
                        img = pygame.transform.scale(self.beans, (tile[1].width + tile[4], tile[1].height + tile[4]))
                    blit(img, (tile[1][0] + tile[1].width / 2 - img.get_width() / 2,
                               tile[1][1] + tile[1].height / 2 - img.get_height() / 2))

            # spitting plant left --------------------------------------------------------------------------------------
            if tile[0] == 'spitting_plant_left':
                if append_spit:
                    x = tile[1].left - camera_move_x
                    y = tile[1].center[1] - 2 - camera_move_y
                    rect = pygame.Rect(0, 0, 4, 4)
                    rect.center = (x, y)
                    direction = [-3, 0]
                    counter = 300
                    package = [rect, direction, counter]
                    self.spit_list.append(package)
                    self.spit_rect_list.append(rect)

                if -tile_size < tile[1][0] < swidth and -tile_size < tile[1][1] < sheight:
                    blit(self.spitting_plant_img_left, tile[1])

            # spitting plant right -------------------------------------------------------------------------------------
            if tile[0] == 'spitting_plant_right':
                if append_spit:
                    x = tile[1].right - camera_move_x
                    y = tile[1].center[1] - 2 - camera_move_y
                    rect = pygame.Rect(0, 0, 4, 4)
                    rect.center = (x, y)
                    direction = [3, 0]
                    counter = 300
                    package = [rect, direction, counter]
                    self.spit_list.append(package)
                    self.spit_rect_list.append(rect)

                if -tile_size < tile[1][0] < swidth and -tile_size < tile[1][1] < sheight:
                    blit(self.spitting_plant_img_right, tile[1])

            # spitting plant up ----------------------------------------------------------------------------------------
            if tile[0] == 'spitting_plant_up':
                if append_spit:
                    x = tile[1].center[0] - camera_move_x
                    y = tile[1].top - camera_move_y
                    rect = pygame.Rect(0, 0, 4, 4)
                    rect.center = (x, y)
                    direction = [0, -3]
                    counter = 300
                    package = [rect, direction, counter]
                    self.spit_list.append(package)
                    self.spit_rect_list.append(rect)

                if -tile_size < tile[1][0] < swidth and -tile_size < tile[1][1] < sheight:
                    blit(self.spitting_plant_img_up, tile[1])

            # log ------------------------------------------------------------------------------------------------------
            if tile[0] == 'log':
                if -tile_size * 2 < tile[1][0] < swidth and -tile_size < tile[1][1] < sheight:
                    img = self.log0
                    if self.log_counter >= 15:
                        if self.wood_num != 1:
                            self.wood_num = randrange(1, 4)
                        if self.wood_num != 1:
                            self.log_counter = 0
                        if self.wood_num == 1:
                            img = self.log1
                            if self.log_counter >= 20:
                                self.wood_num = 0
                                self.log_counter = 0
                                # loading wood particles
                                append = self.wood_particles.append
                                for i in range(5):
                                    append([[tile[1][0] + tile_size + tile_size / 3,
                                             tile[1][1] + tile_size / 3],
                                            [(randint(0, 40) / 10) - 2,
                                             (randint(0, 20) / 10) - 1],
                                            randint(2, 3)])
                    blit(img, tile[1])
                # updating wood particles
                if self.wood_particles:
                    remove = self.wood_particles.remove
                    for part in self.wood_particles:
                        part[0][0] += part[1][0] * fps_adjust + camera_move_x
                        part[0][1] += part[1][1] * fps_adjust + camera_move_y
                        part[2] -= 0.4
                        draw_rect(screen, (192, 161, 133), [int(part[0][0]), int(part[0][1]), 1, 1])
                        if part[2] <= 0:
                            remove(part)

            # copper wheel ---------------------------------------------------------------------------------------------
            if tile[0] == 'copper_wheel':
                if not tile[-1]:
                    img = self.copper_wheel_frames[self.copper_wheel_frame]
                else:
                    img = tile[-1]
                blit(img, tile[1])

                append = self.wheel_circle_hit_pos_list.append
                for angle in tile[2]:
                    # drawing obstacle circles
                    if not tile[-1]:
                        index = tile[2].index(angle)
                        tile[2][index] += speed * fps_adjust
                        angle = tile[2][index]
                    radian_angle = math.radians(angle)
                    x = math.sin(radian_angle) * self.copper_wheel_radius
                    y = math.cos(radian_angle) * self.copper_wheel_radius
                    x += 64 + tile[1].x
                    y += 64 + tile[1].y
                    draw_circle(screen, (0, 0, 0), (x, y), 16, 16)
                    draw_circle(screen, (255, 255, 255), (x, y), 16, 1)
                    pos = [x, y]
                    append(pos)
                    # collision
                    radius = 9
                    circ_rect = pygame.Rect(x - radius, y - radius, 18, 18)
                    if collision_sack(circ_rect):
                        if sack_rect.left < x < sack_rect.right:
                            harm = True
                            tile[-1] = img
                        elif sack_rect.top < y < sack_rect.bottom:
                            harm = True
                            tile[-1] = img
                        else:
                            condition1 = abs(sack_rect.right - x) < radius and abs(sack_rect.bottom - y) < radius
                            condition2 = abs(sack_rect.right - x) < radius and abs(sack_rect.top - y) < radius
                            condition3 = abs(sack_rect.left - x) < radius and abs(sack_rect.bottom - y) < radius
                            condition4 = abs(sack_rect.left - x) < radius and abs(sack_rect.top - y) < radius
                            if condition1 or condition2 or condition3 or condition4:
                                harm = True
                                tile[-1] = img

            # lamp -----------------------------------------------------------------------------------------------------
            if tile[0] == 'lamp':
                # tile[2] -> velocity
                gravity = 0.2
                given_vel = 2
                r = tile[3]
                s = tile[4]

                tile[5] -= 0.1 * fps_adjust

                default_swing = 14

                if collision_sack(tile[1]) and tile[5] < 6:
                    tile[5] = default_swing
                    if camera_move_x > 0:
                        self.lamp_direction = -1
                    elif camera_move_x < 0:
                        self.lamp_direction = 1
                    else:
                        self.lamp_direction = 0

                if tile[5] > 0:
                    offset = math.sin((default_swing - tile[5])) * tile[5] * self.lamp_direction
                else:
                    offset = 0

                x = tile[1].x + (tile_size / 2 - 1) + offset

                # circle math
                M = (r*r - s[0]*s[0] - s[1]*s[1] - x*x + 2*x*s[0])
                y1 = (2*s[1] - math.sqrt(abs(4*s[1]*s[1] + 4*M))) / 2
                y2 = (2*s[1] + math.sqrt(abs(4*s[1]*s[1] + 4*M))) / 2
                y = max([y1, y2])

                # lamp rotation
                if offset != 0:
                    b = y - s[1]
                    a = offset
                    angle = math.atan2(b, a) * 57.3
                    img = pygame.transform.rotate(self.lamp, 90 - angle)
                else:
                    img = self.lamp

                draw_line(screen, (173, 173, 173), s, (x, y), 1)
                blit(img, (x - img.get_width() / 2 + 1, y - img.get_height() / 2))

        # plant spit collisions, harm and particles --------------------------------------------------------------------
        removal_list = []
        append = removal_list.append
        for spit in self.spit_list:
            spit[0].x += spit[1][0] * fps_adjust + camera_move_x
            spit[0].y += spit[1][1] * fps_adjust + camera_move_y
            spit[2] -= 1 * fps_adjust
            if spit[2] <= 0:
                append(spit)
            if collision_sack(spit[0]):
                harm = True
                append(spit)
            for tile in self.tile_list:
                if tile[1].colliderect(spit[0]):
                    append(spit)
            draw_circle(screen, (255, 255, 255), spit[0].center, 3, 3)
            draw_circle(screen, (255, 0, 0), spit[0].center, 3, 1)
        remove = self.spit_list.remove
        append = self.spit_particle_list.append
        for spit in removal_list:
            if spit in self.spit_list:
                remove(spit)
                for i in range(20):
                    dx = randrange(-10, 10) / 10
                    dy = math.sqrt((1 - dx**2)) * choice([-1, 1])
                    part = [[spit[0].centerx, spit[0].centery], [dx, dy], choice([2, 3, 4])]
                    append(part)

        part_removal_list = []
        append = part_removal_list.append
        for part in self.spit_particle_list:
            part[0][0] += part[1][0] * fps_adjust + camera_move_x
            part[0][1] += part[1][1] * fps_adjust + camera_move_y
            draw_circle(screen, (255, 0, 0), part[0], part[2])
            part[2] -= 0.2 * fps_adjust
            if part[2] <= 0:
                append(part)
        remove = self.spit_particle_list.remove
        for part in part_removal_list:
            if part in self.spit_particle_list:
                remove(part)

        return harm, gem_equipped, gem_sound

    # ------------------------------------------------------------------------------------------------------------------

    def update_fg_tiles(self, screen, sack_rect, fps_adjust, camera_move_x, camera_move_y, health, player_moved,
                        shock_mush_tutorial):
        # shockwave mushroom variables
        self.shockwave_center_list = []
        # bee tile variables
        self.bee_harm = False
        if player_moved:
            self.bee_release_counter += 1 * fps_adjust
        bee_release_time = 120
        bee_num = 3
        max_bee_timeout = 210
        if shock_mush_tutorial:
            bee_release_time = 180
            bee_num = 2
        if self.bee_release_counter >= bee_release_time and health > 0 and player_moved:
            self.bee_counter += 1
            if self.bee_counter >= bee_num:
                self.bee_counter = bee_num
            self.bee_release_counter = 0
        distance_list = []

        self.arrow_bob_counter += 1 * fps_adjust

        blit = screen.blit
        draw_line = pygame.draw.line
        scale = pygame.transform.scale
        append = self.shockwave_center_list.append

        for tile in self.main_fg_tile_list:
            # shockwave mushroom ---------------------------------------------------------------------------------------
            if tile[0] == 'shockwave_mushroom':
                if -tile_size < tile[1][0] < swidth and -tile_size < tile[1][1] < sheight:
                    squash = 0
                    trigger = False
                    tile[3] -= 1 * fps_adjust
                    tile[2] -= 1 * fps_adjust
                    if tile[3] < 0:
                        tile[3] = 0

                    if tile[2] > 12:
                        squash = 2
                    elif tile[2] > 9:
                        squash = 4
                    elif tile[2] > 6:
                        squash = 6
                    elif tile[2] > 3:
                        squash = 4
                    elif tile[2] > 0:
                        squash = 2
                        trigger = True

                    # particle animation
                    particle_animation = True
                    if tile[2] > 12:
                        frame = 1
                    elif tile[2] > 10:
                        frame = 2
                    elif tile[2] > 8:
                        frame = 3
                    elif tile[2] > 6:
                        frame = 4
                    elif tile[2] > 4:
                        frame = 5
                    elif tile[2] > 2:
                        frame = 6
                    elif tile[2] > 0:
                        frame = 7
                    elif tile[2] > -2:
                        frame = 8
                    else:
                        particle_animation = False
                        frame = 1

                    if squash > 0:
                        img = scale(self.shockwave_mushroom,
                                                     (tile_size + squash, tile_size / 2 - squash))
                    else:
                        img = self.shockwave_mushroom

                    if tile[3] != 0 and tile[2] < 0:
                        img = self.shockwave_mushroom_dark

                    shockwave_center = (tile[1][0] + tile_size / 2, tile[1][1] + 10)
                    radius = tile[4].update_shockwave((shockwave_center[0], shockwave_center[1]),
                                                      fps_adjust, trigger)

                    if particle_animation:
                        blit(self.mush_part_anim_left[frame - 1],
                                    (shockwave_center[0] - tile_size, shockwave_center[1] - 4))
                        blit(self.mush_part_anim_right[frame - 1],
                                    (shockwave_center[0] + tile_size/2, shockwave_center[1] - 4))

                    append((shockwave_center[0], shockwave_center[1], radius))

                    blit(img, (tile[1][0] - squash / 2, tile[1][1] + squash))
                    if shock_mush_tutorial:
                        offset = math.sin(self.arrow_bob_counter / 15) * 3
                        blit(self.white_arrow_down, (tile[1][0] + 8, tile[1][1] - tile_size + offset))

            # bee hive -------------------------------------------------------------------------------------------------
            if tile[0] == 'bee_hive':
                timeout = max_bee_timeout
                if self.bee_counter > 0:
                    append = distance_list.append
                    for i in range(self.bee_counter):
                        if i <= 4:
                            bee_harm, distance, bee_timeout = tile[2][i].update_bee(screen, sack_rect, fps_adjust,
                                                                       camera_move_x,
                                                                       camera_move_y, tile[1][0], tile[1][1],
                                                                       health,
                                                                       self.shockwave_center_list,
                                                                       player_moved)
                            if timeout > bee_timeout:
                                timeout = bee_timeout
                            if bee_harm:
                                self.bee_harm = True
                            append(distance)
                # honey bar calculation
                black_bar_scale = timeout / max_bee_timeout
                if (bee_release_time - self.bee_release_counter) / bee_release_time < black_bar_scale and \
                        self.bee_counter < bee_num:
                    black_bar_scale = (bee_release_time - self.bee_release_counter) / bee_release_time
                yellow_bar_scale = 1 - black_bar_scale
                yellow_bar_length = 20 * yellow_bar_scale
                if yellow_bar_length > 20:
                    yellow_bar_length = 20
                # drawing the bee hive
                if -tile_size < tile[1][0] < swidth and -tile_size < tile[1][1] < sheight:
                    if yellow_bar_length > 16 and player_moved:
                        offset = [choice([-1, 0, 1]), choice([-1, 0, 1])]
                    else:
                        offset = [0, 0]
                    blit(self.bee_hive, (tile[1][0] + offset[0], tile[1][1] + offset[1]))
                # drawing the honey bar
                draw_line(screen, (10, 10, 10),
                          (tile[1][0] + 6, tile[1][1] + 20), (tile[1][0] + 26, tile[1][1] + 20), 3)
                draw_line(screen, (212, 156, 0),
                          (tile[1][0] + 6, tile[1][1] + 20),
                          (tile[1][0] + 6 + yellow_bar_length, tile[1][1] + 20), 3)

            # grain chute ----------------------------------------------------------------------------------------------
            if tile[0] == 'chute':
                blit(self.grain_chute, (tile[1][0], tile[1][1] - tile_size - 7))

        return self.bee_harm, distance_list

    # ------------------------------------------------------------------------------------------------------------------

    def draw_bat(self, sack_rect, screen, fps_adjust, camera_move_x, camera_move_y, moved, health, draw_hitbox):
        bat_harm = False
        screen_shake = False
        dead = False
        change_music = False
        if health == 0:
            dead = True
        for bat in self.bat_list:
            if bat[1] == 17:
                harm, screen_shake = bat[0].update_bat_laser(sack_rect, fps_adjust, screen, camera_move_x,
                                                             camera_move_y, moved, dead)
                if screen_shake:
                    change_music = True

            else:
                harm, screen_shake = bat[0].update_bat_charge(sack_rect, fps_adjust, screen, camera_move_x,
                                                              camera_move_y, moved, dead, draw_hitbox)
            if harm:
                bat_harm = True

        return bat_harm, screen_shake, change_music

    # ------------------------------------------------------------------------------------------------------------------

    def draw_hot_lava(self, screen, sack_rect, fps_adjust):
        hot_lava_harm = False
        blit = screen.blit
        draw_line = pygame.draw.line
        collision_sack = sack_rect.colliderect
        for package in self.hot_lava_list:
            package[4] -= 1 * fps_adjust
            package[0].fill((0, 0, 0))
            package[0].blit(package[7], (0, 7))
            if collision_sack(package[8]):
                hot_lava_harm = True
                if not package[6]:
                    package[4] = 120
                    package[5] = sack_rect.x + 10 - package[1][0]
                package[6] = True
            else:
                package[6] = False

            if package[4] > 0:
                for pixel in range(47 * 2):
                    if 30 < pixel < 60:
                        y_mult = 5
                    else:
                        y_mult = 3

                    y_wave = math.sin(60 - package[4] * 1/10) * package[4] / 120
                    y_lava_offset = int(math.cos((pixel - 47) / 10) * y_mult * y_wave)

                    x = (package[5] - (pixel - 47))
                    if y_lava_offset > 0:
                        draw_line(package[0], (66, 3, 3), (x, 7 - y_lava_offset), (x, 7))
                    elif y_lava_offset < 0:
                        draw_line(package[0], (0, 0, 0), (x, 7 - y_lava_offset), (x, 7))

                    package[0].set_at((round(package[5] - (pixel - 47)), round(7 - y_lava_offset)), (255, 0, 0))
                if package[5] - 47 > 0:
                    draw_line(package[0], (255, 0, 0), (0, 7), (package[5] - 47, 7))
                if package[3] > package[5] + 47:
                    draw_line(package[0], (255, 0, 0), (package[5] + 47, 7), (package[3], 7))
            else:
                draw_line(package[0], (255, 0, 0), (0, 7),
                                 (package[3], 7))
            blit(package[0], package[1])

        return hot_lava_harm

    # ------------------------------------------------------------------------------------------------------------------

    def draw_bridge(self, screen, camera_move_x, camera_move_y, fps_adjust, sack_rect):
        offset_x = 0
        offset_y = 0
        offset_x_bg = 0
        offset_y_bg = 0

        screen_shake = False

        if self.bridge_collapsing:
            self.bridge_collapse_counter -= 1 * fps_adjust

        debris_tile_counter = 0

        change_music = False

        blit = screen.blit
        append = self.bridge_debris_list.append
        remove = self.tile_list.remove

        for tile in self.bridge_list:
            if sack_rect.x > tile[1][0] and not self.bridge_collapsing:
                self.bridge_collapse_cooldown -= 1*fps_adjust
                if self.bridge_collapse_cooldown < 0:
                    self.bridge_collapsing = True
                    self.bridge_collapse_counter = 100
            if self.bridge_collapsing:
                offset_x = randint(-2, 3)
                offset_y = randint(-2, 3)
                offset_x_bg = randint(-2, 3)
                offset_y_bg = randint(-2, 3)
            if self.bridge_collapse_counter >= 0:
                if tile[-1] == 'right':
                    blit(self.bridge_support_right, (tile[1][0] + offset_x_bg, tile[1][1] + offset_y_bg))
                elif tile[-1] == 'left':
                    blit(self.bridge_support_left, (tile[1][0] + offset_x_bg, tile[1][1] + offset_y_bg))
                blit(tile[0], (tile[1][0] + offset_x, tile[1][1] + offset_y))
            if self.bridge_collapse_counter < 0 and tile in self.tile_list:
                remove(tile)
                # debris = [image, position, velocity, rotation, rotation_speed, alpha, fadeout_counter]
                debris = self.default_debris_list[debris_tile_counter].copy()
                debris[1] = [tile[1][0], tile[1][1]]
                append(debris)
                self.bridge_collapsed = True
                change_music = True
            debris_tile_counter += 1

        # debris management
        remove = self.bridge_debris_list.remove
        rotate = pygame.transform.rotate
        for debris in self.bridge_debris_list:
            # y velocity
            debris[1][1] += debris[2] * fps_adjust + camera_move_y
            debris[1][0] += camera_move_x
            # rotation
            debris[3] += debris[4] * fps_adjust
            # alpha value
            debris[-2] -= debris[-1] * fps_adjust
            debris[0].set_alpha(debris[-2])

            img = debris[0]
            if debris[-2] < 0:
                remove(debris)
            else:
                img = rotate(debris[0], debris[3])
            blit(img, (debris[1][0] - img.get_width() / 2 + tile_size / 2,
                              debris[1][1] - img.get_height() / 2 + tile_size / 2))

        if self.bridge_collapsing and self.bridge_collapse_counter > -40:
            screen_shake = True

        return screen_shake, change_music

    # ------------------------------------------------------------------------------------------------------------------

    def draw_bear_trap_list(self, screen, sack_rect):
        harm, play_bear_trap_cling = self.bear_trap.bear_trap_blit(screen, sack_rect, self.shut_trap_list,
                                                                   self.bear_trap_rect_list)
        return harm, play_bear_trap_cling

    # ------------------------------------------------------------------------------------------------------------------

    def draw_green_mushrooms(self, screen, sack_rect):
        blit = screen.blit
        collision_sack = sack_rect.colliderect
        for tile in self.grn_mushroom_list:
            if -tile_size < tile[1][0] < swidth and -tile_size < tile[1][1] < sheight:
                for num in range(1, 4):
                    y = tile[num][1]
                    if collision_sack(tile[num]):
                        y += 3
                    blit(self.green_mushroom, (tile[num][0], y))
                blit(self.short_grass, tile[0])

    # ------------------------------------------------------------------------------------------------------------------

    def draw_wheat(self, screen, sack_rect, moving, fps_adjust):
        sound = 0
        colliding = False
        blit = screen.blit
        for list_of_wheat in self.wheat_list:
            if -tile_size < list_of_wheat[0][0].x < swidth and -tile_size < list_of_wheat[0][0].y < sheight:
                for wheat_pos_pack in list_of_wheat:
                    wheat_pos = wheat_pos_pack[0]
                    wheat_pos_pack[1] += 1 * fps_adjust
                    counter = wheat_pos_pack[1]
                    offset = math.sin(1/50 * counter) * 2
                    y = wheat_pos[1]
                    if wheat_pos.colliderect(sack_rect.x - 4, sack_rect.y, sack_rect.width + 8, sack_rect.height):
                        y += 6
                        offset = 0
                        colliding = True
                        if not self.playing_wheat_sound and moving:
                            sound = 1
                            self.playing_wheat_sound = True
                    blit(self.wheat, (wheat_pos[0], y + offset))
        if not colliding or not moving:
            if self.playing_wheat_sound:
                sound = -1
            self.playing_wheat_sound = False

        return sound

    # ------------------------------------------------------------------------------------------------------------------

    def draw_hitboxes(self, screen):
        draw_rect = pygame.draw.rect
        draw_circle = pygame.draw.circle
        make_rect = pygame.Rect
        for rect in self.hostile_rect_list:
            draw_rect(screen, (255, 240, 0), rect, 1)
        for pos in self.spit_rect_list:
            rect = make_rect(pos[0], pos[1], 6, 6)
            draw_rect(screen, (255, 240, 0), rect, 1)
        for pos in self.wheel_circle_hit_pos_list:
            draw_circle(screen, (255, 240, 0), pos, 9, 1)

    # ------------------------------------------------------------------------------------------------------------------

    def draw_bean_popup(self, screen):
        if 400 > self.beans_popup_counter > 0:
            draw_popup(screen, self.beans_popup, (self.beans, (7, 2)), self.beans_popup_counter)

    # ------------------------------------------------------------------------------------------------------------------

    def draw_portal_compass(self, sack_rect, screen):
        screen.blit(self.compass_card, (0, -20))
        if self.portal_list:
            center_x = tile_size
            center_y = tile_size - 10
            radius = 12
            dot_radius = 2
            portal_loc = self.portal_list[0][1]
            if sack_rect.colliderect(portal_loc):
                radius = 0
            angle = math.atan2(sack_rect.y - portal_loc.y, sack_rect.x - portal_loc.x)
            dot_x = math.cos(angle) * radius
            dot_y = math.sin(angle) * radius
            x = center_x - dot_x
            y = center_y - dot_y - dot_radius
            pygame.draw.circle(screen, (150, 0, 0), (x, y), dot_radius)
