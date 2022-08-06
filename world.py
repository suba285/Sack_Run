import pygame
from bee import Bee
from bear_trap_class import BearTrap
from plant_spit import PlantSpit
from new_card_animation import CardAnimation
from image_loader import img_loader
from font_manager import Text
import random
import math

pygame.mixer.init()
pygame.init()

tile_size = 32
swidth = 360
sheight = 264

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


class World:
    def __init__(self, data, screen, slow_computer, start_x, start_y, bg_data, controls):

        if slow_computer:
            self.fps_adjust = 0.5
        else:
            self.fps_adjust = 1

        self.controls = controls

        # lists (a lot of lists) ---------------------------------------------------------------------------------------
        self.tile_list = []
        self.bg_tile_list = []
        self.next_level_list = []
        self.portal1_list = []
        self.grass1_list = []
        self.mushroom_list = []
        self.mushroom_pick_list = []
        self.bear_trap_rect_list = []
        self.grn_mushroom_list = []
        self.bee_hive_list = []
        self.chest_list = []
        self.shut_trap_list = []
        self.bush_list = []
        self.slope_list = []
        self.decoration_list = []
        self.toxic_flower_list = []
        self.bee_list = []
        self.spitting_plant_list_left = []
        self.spitting_plant_list_right = []
        self.spitting_plant_list_up = []
        self.spit_list_left = []
        self.spit_list_right = []
        self.spit_list_up = []
        self.log_list = []
        self.anchor_eye_list = []
        self.tree_list = []
        self.wheat_list = []

        # variables ----------------------------------------------------------------------------------------------------
        self.portal_counter = 0
        self.grass_counter = 0
        self.obtain_mushroom = 0
        self.mushroom_picked = False
        self.in_grn_mush_count = 0
        self.out_grn_mush_count = 60
        self.grn_mush_in = False
        self.bee_release_counter = 400
        self.bee_counter = 0
        self.chest_opened = False
        self.chest_opened_independent = False
        self.chest_counter = 0
        self.chest_press = False
        self.eq_full = False
        self.eq_full_counter = 0
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

        self.key_press_counter = 0

        self.sack_height = 32
        self.sack_width = 20

        self.background_x = 0
        self.background_y = 0

        self.eye_animation = False
        self.eye_counter = 0

        self.bear_trap = BearTrap()

        self.level_length = 0

        # dirt with rocks tile images ----------------------------------------------------------------------------------
        self.stone1 = img_loader('data/images/stone_dirt.PNG', tile_size, tile_size)
        self.stone2 = img_loader('data/images/stone2_dirt.PNG', tile_size, tile_size)

        # dirt tile images ---------------------------------------------------------------------------------------------
        self.dirt = img_loader('data/images/plain_dirt.PNG', tile_size, tile_size)
        self.dirt_grass = img_loader('data/images/dirt_grass.PNG', tile_size, tile_size)
        self.dirt_grass_left = img_loader('data/images/dirt_grass_left.PNG', tile_size, tile_size)
        self.dirt_grass_right = img_loader('data/images/dirt_grass_right.PNG', tile_size, tile_size)
        self.dirt_grass_both_sides = img_loader('data/images/dirt_grass_2sides.PNG', tile_size, tile_size)
        self.dirt_left = img_loader('data/images/dirt_bottom_left.PNG', tile_size, tile_size)
        self.dirt_right = img_loader('data/images/dirt_bottom_right.PNG', tile_size, tile_size)
        self.dirt_patch = img_loader('data/images/dirt_patch.PNG', tile_size, tile_size)
        self.dirt_patch_right = img_loader('data/images/dirt_patch_grass_left.PNG', tile_size, tile_size)
        self.dirt_patch_left = img_loader('data/images/dirt_patch_grass_right.PNG', tile_size, tile_size)

        # bear trap tile images ----------------------------------------------------------------------------------------
        self.bear_trap_shut_img = img_loader('data/images/bear_trap_shut.PNG', tile_size, tile_size / 2)

        # portal tile images -------------------------------------------------------------------------------------------
        portal1 = pygame.image.load('data/images/portal1.PNG').convert()
        self.portal1 = img_loader('data/images/portal1.PNG', tile_size, tile_size)
        self.portal2 = img_loader('data/images/portal2.PNG', tile_size, tile_size)
        self.portal3 = img_loader('data/images/portal3.PNG', tile_size, tile_size)
        self.portal4 = img_loader('data/images/portal4.PNG', tile_size, tile_size)

        # moving grass tile images -------------------------------------------------------------------------------------
        grass1 = pygame.image.load('data/images/grass0.PNG').convert()
        self.grass2 = img_loader('data/images/grass1.PNG', tile_size, tile_size)
        self.grass3 = img_loader('data/images/grass2.PNG', tile_size, tile_size)

        # platform img -------------------------------------------------------------------------------------------------
        self.platform = img_loader('data/images/platform.PNG', tile_size, tile_size)

        # healing mushroom tile images ---------------------------------------------------------------------------------
        self.mushroom = img_loader('data/images/mushroom.PNG', tile_size, tile_size)
        self.mushroom_pick = img_loader('data/images/mushroom_pick.PNG', tile_size, tile_size)
        self.mushroom_dirt = img_loader('data/images/mushroom_dirt_pile.PNG', tile_size, tile_size)

        # green mushroom -----------------------------------------------------------------------------------------------
        self.green_mushroom = img_loader('data/images/green_mushroom.PNG', tile_size / 2, tile_size / 2)

        # dark background dirt tiles -----------------------------------------------------------------------------------
        self.bg_tile = img_loader('data/images/background_tile.PNG', tile_size, tile_size)
        self.bg_tile_left_corner = img_loader('data/images/background_tile_corner.PNG', tile_size, tile_size)
        self.bg_tile_right_corner = pygame.transform.flip(self.bg_tile_left_corner, True, False)
        self.bg_tile_left_btm_corner = pygame.transform.flip(self.bg_tile_left_corner, False, True)
        self.bg_tile_right_btm_corner = pygame.transform.flip(self.bg_tile_right_corner, False, True)
        self.bg_tile_two_corners = img_loader('data/images/background_tile_edges.PNG', tile_size, tile_size)

        # bee hive tile images -----------------------------------------------------------------------------------------
        bee_hive_raw = pygame.image.load('data/images/bee_hive.PNG').convert()
        bee_hive = pygame.transform.scale(bee_hive_raw, (tile_size, tile_size))
        bee_hive.set_colorkey((0, 0, 0))
        self.bee_hive = img_loader('data/images/bee_hive.PNG', tile_size, 2 * tile_size)

        # chest tile images and card animation class init --------------------------------------------------------------
        chest0_raw = pygame.image.load('data/images/chest0.PNG').convert()
        chest1_raw = pygame.image.load('data/images/chest1.PNG').convert()
        chest2_raw = pygame.image.load('data/images/chest2.PNG').convert()
        chest_open_raw = pygame.image.load('data/images/chest_open.PNG').convert()
        self.chest1 = pygame.transform.scale(chest1_raw, (tile_size, tile_size))
        self.chest2 = pygame.transform.scale(chest2_raw, (tile_size, tile_size))
        self.chest_open = pygame.transform.scale(chest_open_raw, (tile_size, tile_size))
        self.chest1.set_colorkey((0, 0, 0))
        self.chest2.set_colorkey((0, 0, 0))
        self.chest_open.set_colorkey((0, 0, 0))

        # bush tiles ---------------------------------------------------------------------------------------------------
        self.bush = img_loader('data/images/bush1.PNG', 2 * tile_size, 2 * tile_size)
        self.bush_img = self.bush

        # tree tiles ---------------------------------------------------------------------------------------------------
        self.tree = img_loader('data/images/tree.PNG', 2 * tile_size, 2 * tile_size)

        # foliage tile images ------------------------------------------------------------------------------------------
        short_grass_raw = pygame.image.load('data/images/short_grass.PNG').convert()
        short_grass_left_raw = pygame.image.load('data/images/short_grass_left.PNG').convert()
        short_grass_right_raw = pygame.image.load('data/images/short_grass_right.PNG').convert()
        self.short_grass = img_loader('data/images/short_grass.PNG', tile_size, tile_size)
        self.short_grass_left = img_loader('data/images/short_grass_left.PNG', tile_size, tile_size)
        self.short_grass_right = img_loader('data/images/short_grass_right.PNG', tile_size, tile_size)
        self.short_flowers_apart = img_loader('data/images/short_flowers_apart.PNG', tile_size, tile_size)
        self.short_flowers_together = img_loader('data/images/short_flowers_together.PNG', tile_size, tile_size)

        # toxic flower tile images -------------------------------------------------------------------------------------
        toxic_flower_raw = pygame.image.load('data/images/toxic_flowers.PNG').convert()
        self.toxic_flower = img_loader('data/images/toxic_flowers.PNG', tile_size, tile_size)

        # spitting plant tile images -----------------------------------------------------------------------------------
        spitting_plant0_raw = pygame.image.load('data/images/spitting_plant0.PNG').convert()
        self.spitting_plant0l = img_loader('data/images/spitting_plant0.PNG', tile_size, tile_size)
        self.spitting_plant1l = img_loader('data/images/spitting_plant1.PNG', tile_size, tile_size)
        self.spitting_plant2l = img_loader('data/images/spitting_plant2.PNG', tile_size, tile_size)
        self.spitting_plant0r = pygame.transform.flip(self.spitting_plant0l, True, False)
        self.spitting_plant1r = pygame.transform.flip(self.spitting_plant1l, True, False)
        self.spitting_plant2r = pygame.transform.flip(self.spitting_plant2l, True, False)
        spitting_plant_up0_raw = pygame.image.load('data/images/spitting_plant_up0.PNG').convert()
        self.spitting_plant_up0 = img_loader('data/images/spitting_plant_up0.PNG', tile_size, tile_size)
        self.spitting_plant_up1 = img_loader('data/images/spitting_plant_up1.PNG', tile_size, tile_size)
        self.spitting_plant_up2 = img_loader('data/images/spitting_plant_up2.PNG', tile_size, tile_size)

        # log frames ---------------------------------------------------------------------------------------------------
        log0 = pygame.image.load('data/images/log0.PNG').convert()
        self.log0 = img_loader('data/images/log0.PNG', 2 * tile_size, tile_size)
        self.log1 = img_loader('data/images/log1.PNG', 2 * tile_size, tile_size)
        self.log1.set_colorkey((0, 0, 0))

        # crops --------------------------------------------------------------------------------------------------------
        self.carrot_patch = img_loader('data/images/carrot_patch.PNG', tile_size, tile_size)
        self.lettuce_patch = img_loader('data/images/lettuce_patch.PNG', tile_size, tile_size)
        self.leek_patch = img_loader('data/images/leek_patch.PNG', tile_size, tile_size)
        self.wheat = img_loader('data/images/light_wheat_plant.PNG', 3, tile_size)

        # guidance arrows and keys -------------------------------------------------------------------------------------
        self.white_arrow_up = img_loader('data/images/white_arrow.PNG', tile_size / 2, tile_size / 2)
        self.white_arrow_down = pygame.transform.flip(self.white_arrow_up, False, True)

        self.key_x = img_loader('data/images/key_x.PNG', tile_size / 2, tile_size / 2)
        self.key_x_press = img_loader('data/images/key_x_press.PNG', tile_size / 2, tile_size / 2)

        # text ---------------------------------------------------------------------------------------------------------
        eq_full_text = Text()
        self.eq_full_txt = eq_full_text.make_text(['eq is full, bin cards to free up space'])
        self.blit_eq_full = False

        # assigning tiles to corresponding coordinates by the level map ------------------------------------------------
        row_count = start_y
        self.level_height = 0
        for row in data:
            column_count = start_x
            self.level_length = 0
            for tile in row:
                if tile == 10:
                    # dirt patch
                    tile = img_rect_pos(self.dirt_patch, column_count, row_count)
                    self.tile_list.append(tile)
                if tile == 11:
                    # dirt
                    tile = img_rect_pos(self.dirt, column_count, row_count)
                    self.tile_list.append(tile)
                if tile == 12:
                    # dirt_grass
                    tile = img_rect_pos(self.dirt_grass, column_count, row_count)
                    self.tile_list.append(tile)
                if tile == 13:
                    # dirt_grass_right
                    tile = img_rect_pos(self.dirt_grass_right, column_count, row_count)
                    self.tile_list.append(tile)
                if tile == 14:
                    # dirt_grass_left
                    tile = img_rect_pos(self.dirt_grass_left, column_count, row_count)
                    self.tile_list.append(tile)
                if tile == 15:
                    # dirt_grass_both_sides
                    tile = img_rect_pos(self.dirt_grass_both_sides, column_count, row_count)
                    self.tile_list.append(tile)
                if tile == 16:
                    # dirt_right
                    tile = img_rect_pos(self.dirt_right, column_count, row_count)
                    self.tile_list.append(tile)
                if tile == 17:
                    # dirt_left
                    tile = img_rect_pos(self.dirt_left, column_count, row_count)
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
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.decoration_list.append(tile)
                if tile == 20:
                    # portal
                    img1 = pygame.transform.scale(portal1, (tile_size, tile_size))
                    img1.set_colorkey((0, 0, 0))
                    img1_rectangle = img1.get_rect()
                    img1_rectangle.x = column_count * tile_size
                    img1_rectangle.y = row_count * tile_size
                    tile = (img1, img1_rectangle)
                    self.next_level_list.append(tile)
                    self.portal1_list.append(tile)
                if tile == 21:
                    # stone dirt1
                    img = self.stone1
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    tile = (img, img_rectangle)
                    self.tile_list.append(tile)
                if tile == 22:
                    # stone dirt2
                    img = self.stone2
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    tile = (img, img_rectangle)
                    self.tile_list.append(tile)
                if tile == 23:
                    # bear trap
                    img = self.bear_trap_shut_img
                    img2 = pygame.transform.scale(img, (8, tile_size / 2))
                    img_rectangle = img2.get_rect()
                    img_rectangle.x = (column_count * tile_size) + 12
                    img_rectangle.y = (row_count * tile_size) + 16
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
                    # mushroom
                    tile = img_rect_pos(self.mushroom, column_count, row_count)
                    self.mushroom_list.append(tile)
                    tile = img_rect_pos(self.mushroom_pick, column_count, row_count)
                    self.mushroom_pick_list.append(tile)
                if tile == 27:
                    # weed
                    pass
                if tile == 28:
                    # bee hive
                    img = pygame.transform.scale(bee_hive, (tile_size, 2 * tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    bee_list = []
                    for i in range(4):
                        bee = Bee(screen, img_rectangle.x, img_rectangle.y, slow_computer)
                        bee_list.append(bee)
                    tile = (img, img_rectangle, bee_list)
                    self.bee_hive_list.append(tile)
                if tile == 29:
                    # chest
                    img = pygame.transform.scale(chest0_raw, (tile_size, tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    chest_open = False
                    animation = CardAnimation()
                    chest_clicked = False
                    tile = [img, img_rectangle, chest_open, animation, chest_clicked]
                    self.chest_list.append(tile)
                if tile == 30:
                    # bush
                    img_rectangle = self.bush.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    tile = (self.bush, img_rectangle)
                    self.bush_list.append(tile)
                if tile == 31:
                    # dirt patch transition left
                    img = self.dirt_patch_left
                    rect = img.get_rect()
                    rect.x = column_count * tile_size
                    rect.y = row_count * tile_size
                    tile = (img, rect)
                    self.tile_list.append(tile)
                if tile == 32:
                    # dirt patch transition right
                    img = self.dirt_patch_right
                    rect = img.get_rect()
                    rect.x = column_count * tile_size
                    rect.y = row_count * tile_size
                    tile = (img, rect)
                    self.tile_list.append(tile)
                if tile == 33:
                    # short grass
                    img = pygame.transform.scale(short_grass_raw, (tile_size, tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    tile = (img, img_rectangle)
                    self.decoration_list.append(tile)
                if tile == 34:
                    # short left
                    img = pygame.transform.scale(short_grass_left_raw, (tile_size, tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    tile = (img, img_rectangle)
                    self.decoration_list.append(tile)
                if tile == 35:
                    # short right
                    img = pygame.transform.scale(short_grass_right_raw, (tile_size, tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    tile = (img, img_rectangle)
                    self.decoration_list.append(tile)
                if tile == 36:
                    # toxic flower
                    img = pygame.transform.scale(toxic_flower_raw, (tile_size, tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    tile = (img, img_rectangle)
                    self.toxic_flower_list.append(tile)
                if tile == 37:
                    # spitting plant left
                    img = pygame.transform.scale(spitting_plant0_raw, (tile_size, tile_size))
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
                    img_raw = pygame.transform.scale(spitting_plant0_raw, (tile_size, tile_size))
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
                    img = pygame.transform.scale(spitting_plant_up0_raw, (tile_size, tile_size))
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
                    img = pygame.transform.scale(log0, (tile_size*2, tile_size))
                    img.set_colorkey((0, 0, 0))
                    img_rectangle = img.get_rect()
                    img_rectangle.x = column_count * tile_size
                    img_rectangle.y = row_count * tile_size + tile_size
                    tile = (img, img_rectangle)
                    self.log_list.append(tile)
                    print(self.log_list)
                if tile == 41:
                    # other tree
                    pass
                if tile == 42 or tile == 41:
                    # tree
                    img = self.tree
                    img_rect = self.tree.get_rect()
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

        # background tiles ---------------------------------------------------------------------------------------------
        self.bg_surface = pygame.Surface((self.level_length * tile_size, self.level_height * tile_size))

        bg_row_count = 0
        self.background_y = start_y * tile_size
        self.background_x = start_x * tile_size
        for row in bg_data:
            bg_col_count = 0
            for bg_tile in row:
                if bg_tile == 47:
                    # bg tile
                    tile = img_rect_pos(self.bg_tile, bg_col_count, bg_row_count)
                    self.bg_surface.blit(tile[0], tile[1])
                if bg_tile == 48:
                    # bg tile both corners
                    tile = img_rect_pos(self.bg_tile_two_corners, bg_col_count, bg_row_count)
                    self.bg_surface.blit(tile[0], tile[1])
                if bg_tile == 49:
                    # bg tile left
                    tile = img_rect_pos(self.bg_tile_left_corner, bg_col_count, bg_row_count)
                    self.bg_surface.blit(tile[0], tile[1])
                if bg_tile == 50:
                    # bg tile right
                    tile = img_rect_pos(self.bg_tile_right_corner, bg_col_count, bg_row_count)
                    self.bg_surface.blit(tile[0], tile[1])
                if bg_tile == 51:
                    # bg tile left bottom
                    tile = img_rect_pos(self.bg_tile_left_btm_corner, bg_col_count, bg_row_count)
                    self.bg_surface.blit(tile[0], tile[1])
                if bg_tile == 52:
                    # bg tile right bottom
                    tile = img_rect_pos(self.bg_tile_right_btm_corner, bg_col_count, bg_row_count)
                    self.bg_surface.blit(tile[0], tile[1])

                bg_col_count += 1
            bg_row_count += 1

        self.bg_surface.set_colorkey((0, 0, 0))

        self.list_of_lists = [self.tile_list, self.decoration_list, self.toxic_flower_list, self.slope_list,
                              self.grass1_list, self.portal1_list, self.mushroom_list,
                              self.bee_hive_list, self.chest_list, self.bush_list,
                              self.spitting_plant_list_up, self.spitting_plant_list_left,
                              self.spitting_plant_list_right, self.tree_list,
                              self.log_list, self.anchor_eye_list]

    def return_tile_list(self):
        return self.tile_list, self.level_length

    def return_slope_list(self):
        return self.slope_list

    # functions drawing tiles ==========================================================================================

    def draw_background(self, screen, camera_move_x, camera_move_y):
        self.background_x += camera_move_x
        self.background_y += camera_move_y
        screen.blit(self.bg_surface, (self.background_x, self.background_y))

    def draw_foliage(self, screen):
        for tile in self.decoration_list:
            if - tile_size * 2 < tile[1][0] < swidth:
                if - tile_size * 2 < tile[1][1] < sheight:
                    screen.blit(tile[0], tile[1])

    def draw_toxic_flowers(self, screen):
        for tile in self.toxic_flower_list:
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

        for wheat_list in self.wheat_list:
            for wheat in wheat_list:
                wheat[0] += camera_move_x
                wheat[1] += camera_move_y

        return self.tile_list

    # ------------------------------------------------------------------------------------------------------------------
    def draw_tile_list(self, screen):
        for tile in self.tile_list:
            if - tile_size < tile[1][0] < swidth:
                if - tile_size * 2 < tile[1][1] < sheight:
                    screen.blit(tile[0], tile[1])

    # functions for drawing animated or interactive tiles and enemies ==================================================

    def draw_grass_list(self, screen, sack_rect, sack_direction, fps_adjust):
        self.grass_counter += 0.78*fps_adjust
        for tile in self.grass1_list:
            if self.grass_counter > 80:
                self.grass_counter = 0
                img = tile[0]
            elif self.grass_counter > 60:
                img = self.grass2
            elif self.grass_counter > 40:
                img = self.grass3
            elif self.grass_counter > 20:
                img = self.grass2
            else:
                img = tile[0]

            if tile[1].colliderect(sack_rect.x, sack_rect.y, self.sack_height, self.sack_width):
                if sack_direction == 1:
                    img = self.grass3
                elif sack_direction == 0:
                    img = tile[0]
                screen.blit(img, tile[1])
            else:
                screen.blit(img, tile[1])

    # ------------------------------------------------------------------------------------------------------------------

    def draw_portal_list(self, screen, fps_adjust, level_count):
        self.portal_counter += 1*fps_adjust
        for tile in self.portal1_list:
            if self.portal_counter > 60:
                self.portal_counter = 0
                img = tile[0]
            elif self.portal_counter > 45:
                img = self.portal4
            elif self.portal_counter > 30:
                img = self.portal3
            elif self.portal_counter > 15:
                img = self.portal2
            else:
                img = tile[0]

            screen.blit(img, tile[1])
            if level_count == 1:
                screen.blit(self.white_arrow_down, (tile[1][0] + 8, tile[1][1] - tile_size / 2))

    # ------------------------------------------------------------------------------------------------------------------

    def draw_mushroom(self, screen, sack_rect, health, camera_move_x, camera_move_y, fps_adjust, tutorial):
        key = pygame.key.get_pressed()
        trigger = False
        for tile in self.mushroom_list:
            output = tile[0]
            if tile[1].colliderect(sack_rect.x, sack_rect.y, self.sack_height, self.sack_width):
                if tile[0] == self.mushroom_dirt:
                    output = self.mushroom_dirt
                for tile2 in self.mushroom_pick_list:
                    if tile[0] != self.mushroom_dirt and health == 1:
                        output = self.mushroom_pick
                if key[self.controls['interact']] and tile[0] != self.mushroom_dirt and health == 1:
                    for i in range(8):
                        self.mush_particles.append([[tile[1][0] + tile_size/2,
                                                    tile[1][1] + tile_size/2],
                                                    [(random.randint(0, 40) / 10) - 2,
                                                    (random.randint(0, 20) / 10) - 1],
                                                    random.randint(1, 2), random.randint(1, 2)])
                    self.mushroom_picked = True
                    trigger = True
                    tile[0] = self.mushroom_dirt
                    output = self.mushroom_dirt
                    self.obtain_mushroom += 1
                    health = 2

            screen.blit(output, tile[1])
            if tutorial and tile[0] != self.mushroom_dirt and health == 1:
                if tile[1].colliderect(sack_rect):
                    self.key_press_counter, img = key_animation(self.key_x, self.key_x_press, self.key_press_counter,
                                                                fps_adjust)
                    screen.blit(img, (swidth / 2 - tile_size / 4, sheight / 3 - tile_size / 4))
                screen.blit(self.white_arrow_down, (tile[1][0] + 8, tile[1][1] - tile_size / 2))

        if self.mush_particles:
            for part in self.mush_particles:
                part[0][0] += part[1][0]*fps_adjust + camera_move_x
                part[0][1] += part[1][1]*fps_adjust + camera_move_y
                part[2] -= 0.3
                if part[3] == 1:
                    colour = (255, 255, 255)
                else:
                    colour = (255, 0, 0)
                pygame.draw.rect(screen, colour, [int(part[0][0]), int(part[0][1]), 1, 1])
                if part[2] <= 0:
                    self.mush_particles.remove(part)

        return trigger, health

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

    def draw_and_manage_beehive(self, screen, sack_rect, fps_adjust, camera_move_x, camera_move_y, health, radius,
                                player_moved):
        self.bee_harm = False
        if player_moved:
            self.bee_release_counter += 1*fps_adjust
        if self.bee_release_counter >= 180 and health > 0:
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
                                                              self.tile_list, camera_move_x,
                                                              camera_move_y, tile[1][0], tile[1][1],
                                                              self.toxic_flower_list, health, radius,
                                                              player_moved)
                    if self.bee_harm:
                        return self.bee_harm
        return self.bee_harm

    # ------------------------------------------------------------------------------------------------------------------

    def draw_chest(self, screen, sack_rect, fps_adjust, power_list, tutorial, eq_list, level_count):
        reinit_eq = False
        play_lock_sound = False
        key = pygame.key.get_pressed()
        chosen_power = "none"
        max_card_num = 3
        eq_len = len(eq_list)
        self.blit_eq_full = False
        for tile in self.chest_list:
            if tile[1].colliderect(sack_rect.x, sack_rect.y, self.sack_height, self.sack_width):
                if eq_len < max_card_num and not tile[4]:
                    output = self.chest_open
                else:
                    output = tile[0]
                if key[self.controls['interact']] and tile[0] != self.chest2 and not tile[4] and\
                        power_list and eq_len < max_card_num:
                    self.chest_press = True
                    tile[4] = True
                    play_lock_sound = True
                if key[self.controls['interact']] and eq_len >= max_card_num:
                    self.eq_full = True
                if eq_len >= max_card_num and not tile[4]:
                    self.blit_eq_full = True
                if self.chest_press:
                    self.chest_counter += 1*fps_adjust
                    if self.chest_counter > 10:
                        tile[2] = True
                        tile[4] = True
                        tile[0] = self.chest2
                        self.chest_counter = 0
                        self.chest_press = False
                        output = self.chest2
                        if power_list:
                            chosen_power = random.choice(power_list)
                            if tutorial and level_count == 1:
                                chosen_power = 'jump boost'
                            if tutorial and level_count == 2:
                                chosen_power = 'no harm'
                            eq_list.append(chosen_power)
                            reinit_eq = True

                    elif self.chest_counter > 5:
                        output = self.chest1

            else:
                output = tile[0]
                self.eq_full = False

            if tile[2]:
                tile[3].animate_card(screen, tile[1][0], tile[1][1], fps_adjust)
            screen.blit(output, tile[1])
            if tutorial and tile[0] != self.chest2 and not tile[4]:
                if tile[1].colliderect(sack_rect):
                    self.key_press_counter, img = key_animation(self.key_x, self.key_x_press, self.key_press_counter,
                                                                fps_adjust)
                    screen.blit(img, (swidth/2 - tile_size/4, sheight/3 - tile_size/4))
                screen.blit(self.white_arrow_down, (tile[1][0] + 8, tile[1][1] - tile_size / 2))

        return chosen_power, reinit_eq, play_lock_sound, power_list, self.chest_press

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
                if wheat_pos.colliderect(sack_rect.x - 1, sack_rect.y, sack_rect.width + 2, sack_rect.height):

                    y += 6
                screen.blit(self.wheat, (wheat_pos[0], y))

    # ------------------------------------------------------------------------------------------------------------------

    def draw_portal_compass(self, sack_rect, screen):
        # this just draws the dot showing the direction to the portal, the background is blitted separately
        if self.portal1_list:
            center_x = tile_size
            center_y = tile_size + 10
            radius = 12
            dot_radius = 2
            portal_loc = self.portal1_list[0][1]
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

