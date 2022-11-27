import pygame
from bee import Bee
from bear_trap_class import BearTrap
from plant_spit import PlantSpit
from image_loader import img_loader
from font_manager import Text
from shockwave import Shockwave
import random
import math

pygame.mixer.init()
pygame.init()

tile_size = 32
sheight = 264
swidth = 352

# this class is responsible for assigning tile images to their places on the screen
# it's functions draw the tiles and manage the interactive tiles of the game


def img_rect_pos(img, col_count, row_count):
    rect = img.get_rect()
    rect.x = col_count * tile_size
    rect.y = row_count * tile_size
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
            pygame.draw.circle(screen, (255, 255, 255), position, int(self.radius1), int(width))
            finished = False
        else:
            finished = True

        return finished


class World:
    def __init__(self, data, screen, slow_computer, bg_data, settings_counters, world_count):
        self.settings_counters = settings_counters

        self.data = data
        self.bg_data = bg_data

        self.screen = screen

        self.slow_computer = slow_computer

        self.world_count = world_count

        # lists (a lot of lists) ---------------------------------------------------------------------------------------
        self.tile_list = []
        self.tile_pos_list = []
        self.bg_tile_list = []
        self.bg_tile_pos_list = []
        self.next_level_list = []
        self.portal_list = []
        self.bear_trap_rect_list = []
        self.grn_mushroom_list = []
        self.bee_hive_list = []
        self.shut_trap_list = []
        self.bush_list = []
        self.slope_list = []
        self.decoration_list = []
        self.spitting_plant_list_left = []
        self.spitting_plant_list_right = []
        self.spitting_plant_list_up = []
        self.log_list = []
        self.tree_list = []
        self.wheat_list = []
        self.gem_list = []
        self.shockwave_mushroom_list = []
        self.shockwave_center_list = []
        self.set_lava_list = []
        self.hot_lava_list = []

        self.list_of_lists = []

        # variables ----------------------------------------------------------------------------------------------------
        self.portal_counter = 0
        self.portal_part_counter = 0
        self.bee_release_counter = 400
        self.bee_counter = 0
        self.bee_harm = False
        self.spitting_counter_left = 0
        self.spitting_counter_right = 0
        self.spitting_counter_up = 0
        self.spit_counter_left = 0
        self.spit_counter_right = 0
        self.spit_counter_up = 0
        self.log_counter = 0
        self.wood_num = 0
        self.gem_bob_counter = 0
        self.gem_flicker_counter = 0
        self.gem_equipped = False
        self.wood_particles = []
        self.mush_particles = []
        self.gem_particles = []

        self.key_press_counter = 0

        self.sack_height = 32
        self.sack_width = 20

        self.background_x = 0
        self.background_y = 0

        self.bear_trap = BearTrap()

        self.level_length = 0
        self.level_height = 0

        self.portal_position = (0, 0)

        self.angles = [0, 90, 180, 270]

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

        # bear trap tile images ----------------------------------------------------------------------------------------
        self.bear_trap_shut_img = img_loader('data/images/bear_trap_shut.PNG', tile_size, tile_size / 2)

        # portal tile images -------------------------------------------------------------------------------------------
        self.portal1 = img_loader('data/images/portal1.PNG', tile_size, tile_size)
        self.portal2 = img_loader('data/images/portal2.PNG', tile_size, tile_size)
        self.portal3 = img_loader('data/images/portal3.PNG', tile_size, tile_size)
        self.portal4 = img_loader('data/images/portal4.PNG', tile_size, tile_size)
        self.portal = img_loader('data/images/portal.PNG', tile_size, tile_size)
        self.portal_part_list = []
        self.portal.set_colorkey((0, 0, 0))

        # platform img -------------------------------------------------------------------------------------------------
        self.platform = img_loader('data/images/platform.PNG', tile_size, tile_size)

        # shockwave mushroom tile images -------------------------------------------------------------------------------
        self.shockwave_mushroom = img_loader('data/images/shockwave_mushroom.PNG', tile_size, tile_size / 2)
        self.shockwave_mushroom_dark = img_loader('data/images/shockwave_mushroom_dark.PNG', tile_size, tile_size / 2)

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
        self.bg_dirt_tile = img_loader('data/images/tile_bg.PNG', tile_size, tile_size)
        bg_dirt_tile_left = img_loader('data/images/tile_bg_corner.PNG', tile_size, tile_size)
        bg_dirt_tile_top_edge = img_loader('data/images/tile_bg_edge.PNG', tile_size, tile_size)
        bg_dirt_tile_two_edges = img_loader('data/images/tile_bg_edge.PNG', tile_size, tile_size)
        bg_dirt_tile_btm_edge = pygame.transform.flip(bg_dirt_tile_top_edge, False, True)
        bg_dirt_tile_right_edge = pygame.transform.rotate(bg_dirt_tile_top_edge, 270)
        bg_dirt_tile_left_edge = pygame.transform.rotate(bg_dirt_tile_top_edge, 90)
        bg_dirt_tile_right = pygame.transform.flip(bg_dirt_tile_left, True, False)
        bg_dirt_tile_btm_left = pygame.transform.flip(bg_dirt_tile_left, False, True)
        bg_dirt_tile_btm_right = pygame.transform.flip(bg_dirt_tile_right, False, True)
        bg_dirt_tile_two_corners = img_loader('data/images/tile_bg_two_corners.PNG', tile_size, tile_size)

        self.bg_dirt_tiles = {
            (True, True, True, True): self.bg_dirt_tile,
            (False, False, False, False): self.bg_dirt_tile,
            (False, True, True, True): bg_dirt_tile_top_edge,
            (True, False, True, True): bg_dirt_tile_right_edge,
            (True, True, False, True): bg_dirt_tile_btm_edge,
            (True, True, True, False): bg_dirt_tile_left_edge,
            (False, True, True, False): bg_dirt_tile_left,
            (False, False, True, True): bg_dirt_tile_right,
            (True, False, False, True): bg_dirt_tile_btm_right,
            (True, True, False, False): bg_dirt_tile_btm_left,
            (True, False, True, False): bg_dirt_tile_two_edges,
            (False, False, True, False): bg_dirt_tile_two_corners,
        }

        self.bg_dark_tile = img_loader('data/images/tile_bg_dark.PNG', tile_size, tile_size)
        bg_dark_tile_left = img_loader('data/images/tile_bg_dark_corner.PNG', tile_size, tile_size)
        bg_dark_tile_top_edge = img_loader('data/images/tile_bg_dark_edge.PNG', tile_size, tile_size)
        bg_dark_tile_two_edges = img_loader('data/images/tile_bg_dark_edge.PNG', tile_size, tile_size)
        bg_dark_tile_btm_edge = pygame.transform.flip(bg_dark_tile_top_edge, False, True)
        bg_dark_tile_right_edge = pygame.transform.rotate(bg_dark_tile_top_edge, 270)
        bg_dark_tile_left_edge = pygame.transform.rotate(bg_dark_tile_top_edge, 90)
        bg_dark_tile_right = pygame.transform.flip(bg_dark_tile_left, True, False)
        bg_dark_tile_btm_left = pygame.transform.flip(bg_dark_tile_left, False, True)
        bg_dark_tile_btm_right = pygame.transform.flip(bg_dark_tile_right, False, True)
        bg_dark_tile_two_corners = img_loader('data/images/tile_bg_dark_two_corners.PNG', tile_size, tile_size)

        self.bg_dark_tiles = {
            (True, True, True, True): self.bg_dark_tile,
            (False, False, False, False): self.bg_dark_tile,
            (False, True, True, True): bg_dark_tile_top_edge,
            (True, False, True, True): bg_dark_tile_right_edge,
            (True, True, False, True): bg_dark_tile_btm_edge,
            (True, True, True, False): bg_dark_tile_left_edge,
            (False, True, True, False): bg_dark_tile_left,
            (False, False, True, True): bg_dark_tile_right,
            (True, False, False, True): bg_dark_tile_btm_right,
            (True, True, False, False): bg_dark_tile_btm_left,
            (True, False, True, False): bg_dark_tile_two_edges,
            (False, False, True, False): bg_dark_tile_two_corners,
        }

        # bee hive tile images -----------------------------------------------------------------------------------------
        self.bee_hive = img_loader('data/images/bee_hive.PNG', tile_size, 1.5 * tile_size)
        self.bee_hive.set_colorkey((0, 0, 0))

        # bush tiles ---------------------------------------------------------------------------------------------------
        self.bush = img_loader('data/images/bush1.PNG', 2 * tile_size, 2 * tile_size)
        self.bush_img = self.bush

        # tree tiles ---------------------------------------------------------------------------------------------------
        self.tree = img_loader('data/images/tree.PNG', 2 * tile_size, 2 * tile_size)
        self.birch_tree = img_loader('data/images/tree_birch.PNG', tile_size, tile_size * 3)

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
        self.log0 = pygame.image.load('data/images/log0.PNG').convert()
        self.log0 = img_loader('data/images/log0.PNG', 2 * tile_size, tile_size)
        self.log1 = img_loader('data/images/log1.PNG', 2 * tile_size, tile_size)
        self.log1.set_colorkey((0, 0, 0))

        # crops --------------------------------------------------------------------------------------------------------
        self.carrot_patch = img_loader('data/images/carrot_patch.PNG', tile_size, tile_size)
        self.lettuce_patch = img_loader('data/images/lettuce_patch.PNG', tile_size, tile_size)
        self.leek_patch = img_loader('data/images/leek_patch.PNG', tile_size, tile_size)
        self.wheat = img_loader('data/images/light_wheat_plant.PNG', 3, tile_size)

        # lava ---------------------------------------------------------------------------------------------------------
        self.set_lava = img_loader('data/images/lava.PNG', tile_size, 5)
        self.set_lava2 = img_loader('data/images/lava2.PNG', tile_size, 5)
        self.set_lava_left = img_loader('data/images/lava_edge.PNG', tile_size, 5)
        self.set_lava_right = pygame.transform.flip(self.set_lava_left, True, False)
        self.molten_lava = pygame.Surface((tile_size, tile_size - 7)).convert()
        self.molten_lava.fill((66, 3, 3))

        # guidance arrows and keys -------------------------------------------------------------------------------------
        self.white_arrow_up = img_loader('data/images/white_arrow.PNG', tile_size / 2, tile_size / 2)
        self.white_arrow_down = pygame.transform.flip(self.white_arrow_up, False, True)

        # compass card -------------------------------------------------------------------------------------------------
        self.compass_card = img_loader('data/images/health_bar_card.PNG', tile_size * 2, tile_size * 2)

        # text ---------------------------------------------------------------------------------------------------------
        eq_full_text = Text()
        self.eq_full_txt = eq_full_text.make_text(['eq is full, bin cards to free up space'])
        self.blit_eq_full = False

    def create_world(self, start_x, start_y, data, bg_data):

        # lists (a lot of lists) ---------------------------------------------------------------------------------------
        self.tile_list = []
        self.tile_pos_list = []
        self.bg_tile_list = []
        self.bg_tile_pos_list = []
        self.next_level_list = []
        self.portal_list = []
        self.bear_trap_rect_list = []
        self.grn_mushroom_list = []
        self.bee_hive_list = []
        self.shut_trap_list = []
        self.bush_list = []
        self.slope_list = []
        self.decoration_list = []
        self.spitting_plant_list_left = []
        self.spitting_plant_list_right = []
        self.spitting_plant_list_up = []
        self.log_list = []
        self.tree_list = []
        self.wheat_list = []
        self.gem_list = []
        self.shockwave_mushroom_list = []
        self.set_lava_list = []
        self.hot_lava_list = []

        # variables ----------------------------------------------------------------------------------------------------
        self.portal_counter = 0
        self.portal_part_counter = 0
        self.bee_release_counter = 400
        self.bee_counter = 0
        self.bee_harm = False
        self.spitting_counter_left = 0
        self.spitting_counter_right = 0
        self.spitting_counter_up = 0
        self.spit_counter_left = 0
        self.spit_counter_right = 0
        self.spit_counter_up = 0
        self.log_counter = 0
        self.wood_num = 0
        self.wood_particles = []
        self.mush_particles = []
        self.gem_particles = []

        # assigning tiles to corresponding coordinates by the level map ------------------------------------------------
        row_count = start_y
        self.level_height = 0

        self.data = data
        self.bg_data = bg_data

        # TILE DATA ENCODING SYSTEM ====================================================================================
        # 10 - gem
        # 11 - dirt
        # 12 - stone
        # 13 - free tile
        # 14 - free tile
        # 15 - free tile
        # 16 - free tile
        # 17 - free tile
        # 18 - wheat
        # 19 - fake bee hive
        # 20 - portal
        # 21 - dirt tile rocks
        # 22 - dirt tile two side edge
        # 23 - bear trap
        # 24 - platform
        # 25 - wobbly mushrooms
        # 26 - hot lava start
        # 27 - hot lava stop
        # 28 - real bee hive
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
        # 44 - leek patch
        # 45 - carrot patch
        # 46 - lettuce patch

        lava_start = []

        for row in self.data:
            column_count = start_x
            self.level_length = 0
            for tile in row:
                if tile == 10:
                    # gem
                    rect = self.gem.get_rect()
                    rect.x = column_count * tile_size + 8
                    rect.y = row_count * tile_size + 8
                    shake_counter = 7
                    surface = pygame.surface.Surface((tile_size / 2, tile_size / 2))
                    surface.set_colorkey((0, 0, 0))
                    animation = CircleAnimation()
                    gem_collected = False
                    gem_counter = 0
                    tile = [self.gem, rect, shake_counter, gem_collected, surface, animation, gem_counter]
                    self.gem_list.append(tile)
                if tile == 11:
                    # dirt
                    tile = img_rect_pos(self.dirt_tile, column_count, row_count)
                    self.tile_pos_list.append([tile[1].x, tile[1].y])
                    self.bg_tile_pos_list.append([tile[1].x, tile[1].y])
                    self.tile_list.append(tile)
                if tile == 12:
                    # stone
                    tile = img_rect_pos(self.stone_tile, column_count, row_count)
                    self.tile_pos_list.append([tile[1].x, tile[1].y])
                    self.bg_tile_pos_list.append([tile[1].x, tile[1].y])
                    self.tile_list.append(tile)
                if tile == 18:
                    # wheat
                    wheat_spacer = 4
                    local_list = []
                    for num in range(8):
                        rect = self.wheat.get_rect()
                        rect.y = (row_count * tile_size) + random.randrange(0, 6)
                        rect.x = (column_count * tile_size) + wheat_spacer * num
                        local_list.append(rect)
                    self.wheat_list.append(local_list)
                if tile == 19:
                    # fake bee hive
                    img = self.bee_hive
                    img_rect = self.bee_hive.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size + tile_size / 2
                    tile = (img, img_rect)
                    self.decoration_list.append(tile)
                if tile == 20:
                    # portal
                    img1 = pygame.transform.scale(self.portal, (tile_size, tile_size))
                    img1.set_colorkey((0, 0, 0))
                    img1_rectangle = img1.get_rect()
                    img1_rectangle.x = column_count * tile_size
                    img1_rectangle.y = row_count * tile_size
                    star_surface = pygame.Surface((tile_size, tile_size * 1.5)).convert()
                    star_surface.fill((1, 1, 1))
                    star_surface.set_colorkey((0, 0, 0))
                    stars = []  # position, speed, colour
                    for star in range(30):
                        stars.append([[random.randrange(0, tile_size - 1),
                                       random.randrange(0, int(tile_size * 1.5 - 1))],
                                      random.choice([1/8, 2/8]),
                                      random.choice([(255, 0, 255), (143, 0, 255)])])
                    portal_surface = pygame.Surface((tile_size, tile_size * 1.5)).convert()
                    portal_surface.set_colorkey((0, 0, 255))
                    tile = (img1, img1_rectangle, portal_surface, star_surface, stars)
                    self.next_level_list.append(tile)
                    self.portal_list.append(tile)
                    self.portal_position = (img1_rectangle[0], img1_rectangle[1])
                if tile == 21:
                    # stone dirt
                    img = self.dirt_tile_rocks
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    tile = (img, img_rectangle)
                    self.tile_pos_list.append([img_rectangle.x, img_rectangle.y])
                    self.tile_list.append(tile)
                if tile == 23:
                    # bear trap
                    img = self.bear_trap_shut_img
                    img2 = pygame.transform.scale(img, (8, tile_size / 4))
                    img_rectangle = img2.get_rect()
                    img_rectangle.x = (column_count * tile_size) + 12
                    img_rectangle.y = (row_count * tile_size) + 24
                    tile = (img, img_rectangle)
                    shut = False
                    self.shut_trap_list.append(shut)
                    self.bear_trap_rect_list.append(tile)
                if tile == 24:
                    # platform
                    img = self.platform
                    dimension_img = pygame.transform.scale(img, (tile_size, tile_size/6))
                    img_rectangle = dimension_img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    tile = (img, img_rectangle)
                    self.tile_list.append(tile)
                if tile == 25:
                    # wobbly mushrooms
                    tall_rect = self.green_mushroom.get_rect()
                    short_rect = self.green_mushroom.get_rect()
                    medium_rect = self.green_mushroom.get_rect()
                    base_rect = self.short_grass.get_rect()
                    tall_rect.x = column_count * tile_size
                    tall_rect.y = row_count * tile_size + 14
                    short_rect.x = column_count * tile_size + 8
                    short_rect.y = row_count * tile_size + 20
                    medium_rect.x = column_count * tile_size + 16
                    medium_rect.y = row_count * tile_size + 17
                    base_rect.x = column_count * tile_size
                    base_rect.y = row_count * tile_size
                    tile = [base_rect, tall_rect, short_rect, medium_rect]
                    self.grn_mushroom_list.append(tile)
                if tile == 26:
                    # hot lava start
                    lava_start = [column_count * tile_size, row_count * tile_size]
                if tile == 27:
                    # hot lava stop
                    lava_stop = [column_count * tile_size + tile_size, row_count * tile_size]
                    len = lava_stop[0] - lava_start[0]
                    lava_surface = pygame.Surface((len, tile_size)).convert()
                    lava_surface.set_colorkey((0, 0, 0))
                    img = pygame.transform.scale(self.molten_lava, (len, tile_size - 7))
                    lava_surface.blit(img, (0, 7))
                    wave_counter = 0
                    wave_center = 0
                    collided = False
                    lava_package = [lava_surface, lava_start, lava_stop, len, wave_counter, wave_center, collided, img]
                    self.hot_lava_list.append(lava_package)
                if tile == 28:
                    # bee hive
                    img = self.bee_hive
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size + tile_size / 2
                    bee_list = []
                    for i in range(4):
                        bee = Bee(img_rectangle.x, img_rectangle.y)
                        bee_list.append(bee)
                    tile = (img, img_rectangle, bee_list)
                    self.bee_hive_list.append(tile)
                if tile == 29:
                    # shockwave mushroom
                    img = self.shockwave_mushroom
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size + tile_size / 2
                    squash_counter = 0
                    cooldown = 0
                    shockwave_init = Shockwave(self.screen)
                    tile = [img, img_rectangle, squash_counter, cooldown, shockwave_init]
                    self.shockwave_mushroom_list.append(tile)
                if tile == 30:
                    # set lava
                    lava_img = random.choice([self.set_lava, self.set_lava2])
                    img = random.choice([lava_img, pygame.transform.flip(lava_img, True, False)])
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size + tile_size - 5
                    offset = 0
                    tile = (img, img_rect, offset)
                    self.set_lava_list.append(tile)
                if tile == 31:
                    # set lava left
                    img = self.set_lava_left
                    img_rect = img.get_rect()
                    img_rect.width = tile_size - 10
                    img_rect.x = column_count * tile_size + 10
                    img_rect.y = row_count * tile_size + tile_size - 5
                    offset = -10
                    tile = (img, img_rect, offset)
                    self.set_lava_list.append(tile)
                if tile == 32:
                    # set lava right
                    img = self.set_lava_right
                    img_rect = img.get_rect()
                    img_rect.width = tile_size - 10
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size + tile_size - 5
                    offset = 0
                    tile = (img, img_rect, offset)
                    self.set_lava_list.append(tile)
                if tile == 33:
                    # short grass
                    img = pygame.transform.scale(self.short_grass, (tile_size, tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    tile = (img, img_rectangle)
                    self.decoration_list.append(tile)
                if tile == 34:
                    # short left
                    img = pygame.transform.scale(self.short_grass_left, (tile_size, tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    tile = (img, img_rectangle)
                    self.decoration_list.append(tile)
                if tile == 35:
                    # short right
                    img = pygame.transform.scale(self.short_grass_right, (tile_size, tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    tile = (img, img_rectangle)
                    self.decoration_list.append(tile)
                if tile == 36:
                    # bush
                    img_rectangle = self.bush.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    tile = (self.bush, img_rectangle)
                    self.bush_list.append(tile)
                if tile == 37:
                    # spitting plant left
                    img = pygame.transform.scale(self.spitting_plant0_raw, (tile_size, tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    direction = 'left'
                    spit_list = []
                    for i in range(6):
                        plant_spit = PlantSpit(direction, img_rectangle.x, img_rectangle.y)
                        spit_list.append(plant_spit)
                    tile = (img, img_rectangle, direction, spit_list)
                    self.spitting_plant_img_left = img
                    self.spitting_plant_list_left.append(tile)
                if tile == 38:
                    # spitting plant right
                    img_raw = pygame.transform.scale(self.spitting_plant0_raw, (tile_size, tile_size))
                    img = pygame.transform.flip(img_raw, True, False)
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    direction = 'right'
                    spit_list = []
                    for i in range(6):
                        plant_spit = PlantSpit(direction, img_rectangle.x, img_rectangle.y)
                        spit_list.append(plant_spit)
                    tile = (img, img_rectangle, direction, spit_list)
                    self.spitting_plant_img_right = img
                    self.spitting_plant_list_right.append(tile)
                if tile == 39:
                    # spitting plant up
                    img = pygame.transform.scale(self.spitting_plant_up0_raw, (tile_size, tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    direction = 'up'
                    spit_list = []
                    for i in range(6):
                        plant_spit = PlantSpit(direction, img_rectangle.x, img_rectangle.y)
                        spit_list.append(plant_spit)
                    tile = (img, img_rectangle, direction, spit_list)
                    self.spitting_plant_img_up = img
                    self.spitting_plant_list_up.append(tile)
                if tile == 40:
                    # log
                    img = pygame.transform.scale(self.log0, (tile_size*2, tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size + tile_size
                    tile = (img, img_rectangle)
                    self.log_list.append(tile)
                if tile == 41:
                    # birch tree
                    img = self.birch_tree
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tree_list.append(tile)
                if tile == 42:
                    # tree
                    img = self.tree
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tree_list.append(tile)
                if tile == 43:
                    # short flowers together
                    img = self.short_flowers_together
                    img_rect = self.short_flowers_together.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.decoration_list.append(tile)
                if tile == 44:
                    # leek patch
                    img = self.leek_patch
                    img_rect = self.leek_patch.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.decoration_list.append(tile)
                if tile == 45:
                    # carrot patch
                    img = self.carrot_patch
                    img_rect = self.carrot_patch.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.decoration_list.append(tile)
                if tile == 46:
                    # lettuce patch
                    img = self.lettuce_patch
                    img_rect = self.lettuce_patch.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.decoration_list.append(tile)

                column_count += 1
                self.level_length += 1
            row_count += 1
            self.level_height += 1

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
            if tile[0] == self.dirt_tile:
                try:
                    tile[0] = self.dirt_tiles[tuple(tile_edge_data)]
                except KeyError:
                    tile[0] = self.dirt_tile
            if tile[0] == self.stone_tile:
                try:
                    tile[0] = self.stone_tiles[tuple(tile_edge_data)]
                except KeyError:
                    tile[0] = self.stone_tile

        # background tiles ---------------------------------------------------------------------------------------------
        bg_row_count = start_y
        self.background_y = start_y * 32
        self.background_x = start_x * 32
        for row in self.bg_data:
            bg_col_count = start_x
            for bg_tile in row:
                if bg_tile == 47:
                    # bg dirt tile
                    tile = img_rect_pos(self.bg_dirt_tile, bg_col_count, bg_row_count)
                    self.bg_tile_list.append(tile)
                    self.bg_tile_pos_list.append([bg_col_count * tile_size, bg_row_count * tile_size])
                if bg_tile == 48:
                    # bg dark tile
                    tile = img_rect_pos(self.bg_dark_tile, bg_col_count, bg_row_count)
                    self.bg_tile_list.append(tile)
                    self.bg_tile_pos_list.append([bg_col_count * tile_size, bg_row_count * tile_size])

                bg_col_count += 1
            bg_row_count += 1

        for tile in self.bg_tile_list:
            #    0
            # 3 [ ] 1
            #    2
            tile_edge_data = [True, True, True, True]
            # checking if there is a tile behind
            if [tile[1].x - tile_size, tile[1].y] not in self.bg_tile_pos_list:
                tile_edge_data[3] = False
            # checking if there is a tile in front
            if [tile[1].x + tile_size, tile[1].y] not in self.bg_tile_pos_list:
                tile_edge_data[1] = False
            # checking if there is a tile above
            if [tile[1].x, tile[1].y - tile_size] not in self.bg_tile_pos_list:
                tile_edge_data[0] = False
            # checking if there is a tile beneath
            if [tile[1].x, tile[1].y + tile_size] not in self.bg_tile_pos_list:
                tile_edge_data[2] = False
            if tile[0] == self.bg_dirt_tile:
                try:
                    tile[0] = self.bg_dirt_tiles[tuple(tile_edge_data)]
                except KeyError:
                    tile[0] = self.bg_dirt_tile
            if tile[0] == self.bg_dark_tile:
                try:
                    tile[0] = self.bg_dark_tiles[tuple(tile_edge_data)]
                except KeyError:
                    tile[0] = self.bg_dark_tile

        self.list_of_lists = [self.tile_list, self.decoration_list, self.slope_list, self.set_lava_list,
                              self.portal_list, self.bee_hive_list, self.bush_list, self.bg_tile_list,
                              self.spitting_plant_list_up, self.spitting_plant_list_left,
                              self.spitting_plant_list_right, self.tree_list,
                              self.log_list, self.gem_list, self.shockwave_mushroom_list]

        return self.level_length, self.level_height

    def return_tile_list(self):
        return self.tile_list, self.level_length

    def return_slope_list(self):
        return self.slope_list

    # functions drawing tiles ==========================================================================================

    def draw_foliage(self, screen):
        for tile in self.decoration_list:
            if - tile_size * 2 < tile[1][0] < swidth:
                if - tile_size * 2 < tile[1][1] < sheight:
                    screen.blit(tile[0], tile[1])

    # updating the position of all tiles -------------------------------------------------------------------------------
    def update_tile_list(self, camera_move_x, camera_move_y):
        for tile_list in self.list_of_lists:
            for tile in tile_list:
                tile[1][0] += camera_move_x
                tile[1][1] += camera_move_y

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

        for wheat_list in self.wheat_list:
            for wheat in wheat_list:
                wheat[0] += camera_move_x
                wheat[1] += camera_move_y

        return self.tile_list

    # ------------------------------------------------------------------------------------------------------------------
    def draw_tile_list(self, screen):
        for tile in self.tile_list:
            if - tile_size < tile[1][0] < swidth:
                if - tile_size * 3 < tile[1][1] < sheight:
                    screen.blit(tile[0], tile[1])

    # ------------------------------------------------------------------------------------------------------------------
    def draw_bg_tile_list(self, screen):
        for tile in self.bg_tile_list:
            screen.blit(tile[0], tile[1])
            if - tile_size < tile[1][0] < swidth:
                if - tile_size < tile[1][1] < sheight:
                    screen.blit(tile[0], tile[1])

    # functions for drawing animated or interactive tiles and enemies ==================================================

    def draw_portal_list(self, screen, fps_adjust, level_count, camera_move_x, camera_move_y):
        self.portal_counter += 1*fps_adjust
        self.portal_part_counter += 1*fps_adjust
        for tile in self.portal_list:
            portal_y_offset = math.sin((1 / 15) * self.portal_counter) * 2

            tile[3].fill((1, 1, 1))
            for star in tile[4]:
                star[0][0] -= (camera_move_x * star[1])
                star[0][1] -= (camera_move_y * star[1])
                if star[0][0] > tile_size:
                    star[0][0] = 0
                    star[0][1] = random.randrange(0, int(tile_size * 1.5 - 1))
                if star[0][0] < 0:
                    star[0][0] = tile_size
                    star[0][1] = random.randrange(0, int(tile_size * 1.5 - 1))
                if star[0][1] > tile_size * 1.5:
                    star[0][1] = 0
                    star[0][0] = random.randrange(0, tile_size - 1)
                if star[0][1] < 0:
                    star[0][1] = tile_size
                    star[0][0] = random.randrange(0, tile_size - 1)
                tile[3].set_at((int(star[0][0]), int(star[0][1])), star[2])

            tile[2].fill((0, 0, 0))
            tile[2].blit(self.portal, (0, 8 + portal_y_offset))
            if self.portal_part_counter > 5:
                self.portal_part_counter = 0
                # max radius, radius, radius achieved, pos
                part_vars = [6, 0, False, (int(random.randrange(8, tile_size - 8)),
                                           int(random.randrange(13, tile_size + 4)))]
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

            screen.blit(tile[3], (tile[1][0], tile[1][1] - 16))

            if level_count == 1:
                screen.blit(self.white_arrow_down, (tile[1][0] + 8, tile[1][1] - tile_size))

    # ------------------------------------------------------------------------------------------------------------------

    def draw_set_lava(self, screen, sack_rect):
        set_lava_harm = False
        for tile in self.set_lava_list:
            if tile[1].colliderect(sack_rect):
                set_lava_harm = True
            if - tile_size < tile[1][0] < swidth:
                if - tile_size * 2 < tile[1][1] < sheight:
                    screen.blit(tile[0], (tile[1][0] + tile[2], tile[1][1]))
        return set_lava_harm

    # ------------------------------------------------------------------------------------------------------------------

    def draw_hot_lava(self, screen, sack_rect, fps_adjust):
        hot_lava_harm = False
        for package in self.hot_lava_list:
            package[4] -= 1 * fps_adjust
            package[0].fill((0, 0, 0))
            package[0].blit(package[7], (0, 7))
            if sack_rect.colliderect(package[1][0], package[1][1] + 10, package[3], tile_size - 10):
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
                        pygame.draw.line(package[0], (66, 3, 3), (x, 7 - y_lava_offset), (x, 7))
                    elif y_lava_offset < 0:
                        pygame.draw.line(package[0], (0, 0, 0), (x, 7 - y_lava_offset), (x, 7))

                    package[0].set_at(((package[5] - (pixel - 47)), 7 - y_lava_offset), (255, 0, 0))
                if package[5] - 47 > 0:
                    pygame.draw.line(package[0], (255, 0, 0), (0, 7), (package[5] - 47, 7))
                if package[3] > package[5] + 47:
                    pygame.draw.line(package[0], (255, 0, 0), (package[5] + 47, 7), (package[3], 7))
            else:
                pygame.draw.line(package[0], (255, 0, 0), (0, 7),
                                 (package[3], 7))
            screen.blit(package[0], package[1])

        return hot_lava_harm

    # ------------------------------------------------------------------------------------------------------------------

    def draw_gem(self, screen, sack_rect, fps_adjust, gem_equipped):
        self.gem_bob_counter += 1 * fps_adjust
        self.gem_flicker_counter += 1 * fps_adjust
        if self.gem_flicker_counter >= 90:
            self.gem_flicker_counter = 0

        for tile in self.gem_list:
            tile[4].fill((0, 0, 0))

            tile[6] -= 1 * fps_adjust

            tile[4].blit(tile[0], (0, 0))
            pygame.draw.line(tile[4], (255, 255, 255),
                             (16, -10 + self.gem_flicker_counter), (0, self.gem_flicker_counter), 3)
            tile[4].blit(self.gem_mask_surf, (0, 0))
            img = tile[4]

            if tile[1].colliderect(sack_rect) and not tile[3] and tile[6] < 0:
                tile[3] = True
                gem_equipped = True

            scale = 1
            circle_animation_finished = False
            if tile[3]:
                scale = (15 - abs(tile[2])) / 8
                tile[2] -= 1.5 * fps_adjust
                if scale > 0:
                    img = pygame.transform.scale(tile[0], (16 * scale, 16 * scale))
                circle_animation_finished = tile[5].draw_circle_animation((tile[1][0] + 8, tile[1][1] + 8),
                                                                          screen, fps_adjust)

            if circle_animation_finished:
                tile[6] = 60 * 3
                tile[2] = 7
                tile[3] = False
                tile[5] = CircleAnimation()

            gem_y_offset = math.sin((1 / 17) * self.gem_bob_counter) * 3
            if scale > 0 > tile[6]:
                if tile[6] > -10:
                    shake_offset_x = random.choice([-2, 0, 2])
                    shake_offset_y = random.choice([-2, 0, 2])
                else:
                    shake_offset_x = 0
                    shake_offset_y = 0

                screen.blit(img,
                            (tile[1][0] + (8 - img.get_width() / 2) + shake_offset_x,
                             tile[1][1] + gem_y_offset + (8 - img.get_height() / 2) + shake_offset_y))
            elif tile[6] >= 0:
                screen.blit(self.gem_outline_surface, (tile[1][0] + (8 - img.get_width() / 2),
                            tile[1][1] + gem_y_offset + (8 - img.get_height() / 2)))

        return gem_equipped

    # ------------------------------------------------------------------------------------------------------------------

    def draw_bear_trap_list(self, screen, sack_rect):
        harm, play_bear_trap_cling = self.bear_trap.bear_trap_blit(screen, sack_rect, self.shut_trap_list,
                                                                   self.bear_trap_rect_list)
        return harm, play_bear_trap_cling

    # ------------------------------------------------------------------------------------------------------------------

    def draw_green_mushrooms(self, screen, sack_rect):
        for tile in self.grn_mushroom_list:
            for num in range(1, 4):
                y = tile[num][1]
                if sack_rect.colliderect(tile[num]):
                    y += 3
                screen.blit(self.green_mushroom, (tile[num][0], y))
            screen.blit(self.short_grass, tile[0])

    # ------------------------------------------------------------------------------------------------------------------

    def draw_and_manage_beehive(self, screen, sack_rect, fps_adjust, camera_move_x, camera_move_y, health,
                                player_moved):
        self.bee_harm = False
        if player_moved:
            self.bee_release_counter += 1*fps_adjust
        if self.bee_release_counter >= 120 and health > 0 and player_moved:
            self.bee_counter += 1
            if self.bee_counter >= 4:
                self.bee_counter = 4
            self.bee_release_counter = 0
        for tile in self.bee_hive_list:
            screen.blit(self.bee_hive, tile[1])
            if self.bee_counter > 0:
                for i in range(self.bee_counter - 1):
                    if i <= 4:
                        self.bee_harm = tile[2][i].update_bee(screen, sack_rect, fps_adjust,
                                                              camera_move_x,
                                                              camera_move_y, tile[1][0], tile[1][1],
                                                              health,
                                                              self.shockwave_center_list,
                                                              player_moved)
                    if self.bee_harm:
                        return self.bee_harm
        return self.bee_harm

    # ------------------------------------------------------------------------------------------------------------------

    def draw_shockwave_mushrooms(self, screen, fps_adjust):
        self.shockwave_center_list = []
        for mushroom in self.shockwave_mushroom_list:
            squash = 0
            trigger = False
            mushroom[3] -= 1 * fps_adjust
            mushroom[2] -= 1 * fps_adjust
            if mushroom[3] < 0:
                mushroom[3] = 0

            if mushroom[2] > 12:
                squash = 2
            elif mushroom[2] > 9:
                squash = 4
            elif mushroom[2] > 6:
                squash = 6
            elif mushroom[2] > 3:
                squash = 4
            elif mushroom[2] > 0:
                squash = 2
                trigger = True

            if squash > 0:
                img = pygame.transform.scale(self.shockwave_mushroom, (tile_size + squash, tile_size / 2 - squash))
            else:
                img = self.shockwave_mushroom

            if mushroom[3] != 0 and mushroom[2] < 0:
                img = self.shockwave_mushroom_dark

            shockwave_center = (mushroom[1][0] + tile_size / 2, mushroom[1][1] + 10)
            radius = mushroom[4].update_shockwave((shockwave_center[0], shockwave_center[1]),
                                                  fps_adjust, trigger)

            self.shockwave_center_list.append((shockwave_center[0], shockwave_center[1], radius))

            screen.blit(img, (mushroom[1][0] - squash / 2, mushroom[1][1] + squash))

    # ------------------------------------------------------------------------------------------------------------------

    def draw_bush(self, screen):
        self.bush_img = self.bush
        for tile in self.bush_list:
            if - tile_size * 2 < tile[1][0] < swidth:
                if - tile_size * 2 < tile[1][1] < sheight:
                    screen.blit(self.bush_img, tile[1])

    # ------------------------------------------------------------------------------------------------------------------

    def draw_spitting_plant_left(self, screen, fps_adjust, camera_move_x, camera_move_y, sack_rect, health):
        harm = False
        self.spitting_counter_left += 1 * fps_adjust
        for tile in self.spitting_plant_list_left:
            if self.spitting_counter_left >= 60:
                self.spitting_plant_img_left = self.spitting_plant2l
                if self.spit_counter_left < 5:
                    self.spit_counter_left += 1
                self.spitting_counter_left = 0
            elif self.spitting_counter_left >= 45:
                self.spitting_plant_img_left = self.spitting_plant1l
            elif self.spitting_counter_left >= 30:
                self.spitting_plant_img_left = tile[0]
            elif self.spitting_counter_left >= 15:
                self.spitting_plant_img_left = self.spitting_plant1l

            screen.blit(self.spitting_plant_img_left, tile[1])

            for i in range(self.spit_counter_left):
                harm = tile[3][i].update_spit(screen, camera_move_x, camera_move_y,
                                              tile[1][0], tile[1][1] + tile_size / 3, fps_adjust,
                                              sack_rect, health, self.tile_list)
                if harm:
                    return harm

            screen.blit(self.spitting_plant_img_left, tile[1])
        return harm

    # ------------------------------------------------------------------------------------------------------------------

    def draw_spitting_plant_right(self, screen, fps_adjust, camera_move_x, camera_move_y, sack_rect, health):
        harm = False
        self.spitting_counter_right += 1 * fps_adjust
        for tile in self.spitting_plant_list_right:
            if self.spitting_counter_right >= 60:
                self.spitting_plant_img_right = self.spitting_plant2r
                if self.spit_counter_right < 5:
                    self.spit_counter_right += 1
                self.spitting_counter_right = 0
            elif self.spitting_counter_right >= 45:
                self.spitting_plant_img_right = self.spitting_plant1r
            elif self.spitting_counter_right >= 30:
                self.spitting_plant_img_right = tile[0]
            elif self.spitting_counter_right >= 15:
                self.spitting_plant_img_right = self.spitting_plant1r

            screen.blit(self.spitting_plant_img_right, tile[1])

            for i in range(self.spit_counter_right):
                harm = tile[3][i].update_spit(screen, camera_move_x, camera_move_y,
                                              tile[1][0], tile[1][1] + tile_size / 3, fps_adjust,
                                              sack_rect, health, self.tile_list)
                if harm:
                    return harm

            screen.blit(self.spitting_plant_img_right, tile[1])
        return harm

    # ------------------------------------------------------------------------------------------------------------------

    def draw_spitting_plant_up(self, screen, fps_adjust, camera_move_x, camera_move_y, sack_rect, health):
        harm = False
        self.spitting_counter_up += 1 * fps_adjust
        for tile in self.spitting_plant_list_up:
            if self.spitting_counter_up >= 60:
                self.spitting_plant_img_up = self.spitting_plant_up2
                if self.spit_counter_up < 5:
                    self.spit_counter_up += 1
                self.spitting_counter_up = 0
            elif self.spitting_counter_up >= 45:
                self.spitting_plant_img_up = self.spitting_plant_up1
            elif self.spitting_counter_up >= 30:
                self.spitting_plant_img_up = tile[0]
            elif self.spitting_counter_up >= 15:
                self.spitting_plant_img_up = self.spitting_plant_up1

            screen.blit(self.spitting_plant_img_up, tile[1])

            for i in range(self.spit_counter_up):
                harm = tile[3][i].update_spit(screen, camera_move_x, camera_move_y,
                                              tile[1][0], tile[1][1] + tile_size / 3, fps_adjust,
                                              sack_rect, health, self.tile_list)
                if harm:
                    return harm

            screen.blit(self.spitting_plant_img_up, tile[1])
        return harm

    # ------------------------------------------------------------------------------------------------------------------

    def draw_log(self, screen, fps_adjust, camera_move_x, camera_move_y):
        self.log_counter += 1*fps_adjust
        for tile in self.log_list:
            img = tile[0]
            if self.log_counter >= 15:
                if self.wood_num != 1:
                    self.wood_num = random.randrange(1, 4)
                if self.wood_num != 1:
                    self.log_counter = 0
                if self.wood_num == 1:
                    img = self.log1
                    if self.log_counter >= 20:
                        self.wood_num = 0
                        self.log_counter = 0
                        # loading wood particles
                        for i in range(5):
                            self.wood_particles.append([[tile[1][0] + tile_size + tile_size/3,
                                                        tile[1][1] + tile_size/3],
                                                        [(random.randint(0, 40) / 10) - 2,
                                                        (random.randint(0, 20) / 10) - 1],
                                                        random.randint(2, 3)])
            screen.blit(img, tile[1])
        # updating wood particles
        if self.wood_particles:
            for part in self.wood_particles:
                part[0][0] += part[1][0]*fps_adjust + camera_move_x
                part[0][1] += part[1][1]*fps_adjust + camera_move_y
                part[2] -= 0.4
                pygame.draw.rect(screen, (192, 161, 133), [int(part[0][0]), int(part[0][1]), 1, 1])
                if part[2] <= 0:
                    self.wood_particles.remove(part)

    # ------------------------------------------------------------------------------------------------------------------

    def draw_tree(self, screen):
        for tile in self.tree_list:
            if - tile_size * 2 < tile[1][0] < swidth:
                if - tile_size * 2 < tile[1][1] < sheight:
                    screen.blit(tile[0], tile[1])

    # ------------------------------------------------------------------------------------------------------------------

    def draw_wheat(self, screen, sack_rect):
        for list_of_wheat in self.wheat_list:
            for wheat_pos in list_of_wheat:
                y = wheat_pos[1]
                if wheat_pos.colliderect(sack_rect.x - 4, sack_rect.y, sack_rect.width + 8, sack_rect.height):
                    y += 6
                screen.blit(self.wheat, (wheat_pos[0], y))

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

    def draw_eq_full(self, screen):
        if self.blit_eq_full:
            screen.blit(self.eq_full_txt, (swidth / 2 - self.eq_full_txt.get_width() / 2, sheight / 3))
