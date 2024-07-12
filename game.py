from world import World, tile_size
from player import Player
from levels import *
from button import *
from particles import Particles
from eq_management import eqManager
from image_loader import img_loader
from font_manager import Text
from popup_bg_generator import popup_bg_generator
from screen_info import swidth, sheight
from json import load, dump
import random
from math import sin, cos


particle_num = 12

level_dictionary = {
    "level1_1": level1_1,
    "level2_1": level2_1,
    "level1_2": level1_2,
    "level2_2": level2_2,
    "level3_2": level3_2,
    "level4_2": level4_2,
    "level5_2": level5_2,
    "level6_2": level6_2,
    "level7_2": level7_2,
    "level8_2": level8_2,
    "level9_2": level9_2,
    "level10_2": level10_2,
    "level1_3": level1_3,
    "level2_3": level2_3,
    "level3_3": level3_3,
    "level4_3": level4_3,
    "level5_3": level5_3,
    "level6_3": level6_3,
    "level7_3": level7_3,
    "level8_3": level8_3,
    "level9_3": level9_3,
    "level1_4": level1_4,
    "level2_4": level2_4,
    "level3_4": level3_4,
    "level4_4": level4_4,
    "level5_4": level5_4,
    "level6_4": level6_4,
    "level7_4": level7_4,
    "level8_4": level8_4,
    "level1_5": level1_5,
    "level2_5": level2_5,
    "level3_5": level3_5,
}

level_bg_dictionary = {
    "level1_1_bg": level1_1_bg,
    "level2_1_bg": level2_1_bg,
    "level1_2_bg": level1_2_bg,
    "level2_2_bg": level2_2_bg,
    "level3_2_bg": level3_2_bg,
    "level4_2_bg": level4_2_bg,
    "level5_2_bg": level5_2_bg,
    "level6_2_bg": level6_2_bg,
    "level7_2_bg": level7_2_bg,
    "level8_2_bg": level8_2_bg,
    "level9_2_bg": level9_2_bg,
    "level10_2_bg": level10_2_bg,
    "level1_3_bg": level1_3_bg,
    "level2_3_bg": level2_3_bg,
    "level3_3_bg": level3_3_bg,
    "level4_3_bg": level4_3_bg,
    "level5_3_bg": level5_3_bg,
    "level6_3_bg": level6_3_bg,
    "level7_3_bg": level7_3_bg,
    "level8_3_bg": level8_3_bg,
    "level9_3_bg": level9_3_bg,
    "level1_4_bg": level1_4_bg,
    "level2_4_bg": level2_4_bg,
    "level3_4_bg": level3_4_bg,
    "level4_4_bg": level4_4_bg,
    "level5_4_bg": level5_4_bg,
    "level6_4_bg": level6_4_bg,
    "level7_4_bg": level7_4_bg,
    "level8_4_bg": level8_4_bg,
    "level1_5_bg": level1_5_bg,
    "level2_5_bg": level2_5_bg,
    "level3_5_bg": level3_5_bg,
}

level_pos_dictionary = {
    "level1_1": (4, -3),
    "level2_1": (5, -2),
    "level3_1": (5, -2),
    "level1_2": (2, -4),
    "level2_2": (2, 0),
    "level3_2": (5, -5),
    "level4_2": (2, -4),
    "level5_2": (4, 1),
    "level6_2": (5, -6),
    "level7_2": (-2, -7),
    "level8_2": (5, -19),
    "level9_2": (0, 4),
    "level10_2": (5, -5),
    "level1_3": (3, -3),
    "level2_3": (1, -1),
    "level3_3": (4, -4),
    "level4_3": (0, 0),
    "level5_3": (-20, -1),
    "level6_3": (-21, -1),
    "level7_3": (-2, -5),
    "level8_3": (3, -8),
    "level9_3": (2, -8),
    "level1_4": (3, 0),
    "level2_4": (-17, 0),
    "level3_4": (3, -1),
    "level4_4": (1, -8),
    "level5_4": (2, -1),
    "level6_4": (4, -8),
    "level7_4": (2, 1),
    "level8_4": (4, 1),
    "level1_5": (2, -20),
    "level2_5": (-1, -7),
    "level3_5": (-24, 0),
}

level_card_dictionary = {
    "level2_1": "mid-air_jump",
    "level2_3": "speed_dash"
}

world_ending_levels = {
    1: 3,
    2: 11,
    3: 10,
    4: 9,
    5: 4
}

ending_world_level = [4, 9]

music_change_list = [[2, 9], [3, 4], [4, 8]]
music_level_phases = [[2, 1, 1], [2, 9, 2], [3, 1, 1], [3, 2, 2], [3, 4, 3], [3, 9, 4], [4, 1, 1], [4, 2, 2], [4, 4, 3], [4, 8, 4]]

bee_popup = [2, 7]
dash_popup = [3, 5]


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


def time_unpacker(string_time):
    multer = 3600
    digiter = 10
    out_time = 0
    for char in string_time:
        if char != ':':
            out_time += int(char) * multer * digiter
            if digiter == 1:
                multer /= 60
            if digiter == 10:
                digiter = 1
            else:
                digiter = 10
    return out_time


class SpeedRunClock:
    def __init__(self):
        text = Text()
        self.cooldown = 70
        self.char_width = 5
        self.box = popup_bg_generator((56, 15))
        self.box_width = self.box.get_width()
        self.gap = 1
        self.time_string = ''
        self.x = swidth - (self.box.get_width() + 7) + ((self.box.get_width() - (40 + self.gap * 5)) / 2)
        self.y = 15
        self.time_counter = 0
        self.minutes = 0
        self.seconds = 0
        self.miliseconds = 0
        self.number_imgs = []
        for num in range(0, 10):
            img = text.make_text([str(num)])
            self.number_imgs.append(img)
        self.colon = text.make_text([':'])

    def update_clock(self, fps_adjust, screen):
        self.time_counter += 1/60 * fps_adjust
        self.cooldown -= 1 * fps_adjust

        if self.cooldown < 0:
            self.miliseconds += 1 * fps_adjust
            if self.miliseconds >= 60:
                self.miliseconds = 0
                self.seconds += 1
            if self.seconds >= 60:
                self.seconds = 0
                self.minutes += 1

        minutes = self.minutes
        seconds = self.seconds
        miliseconds = round(self.miliseconds)

        if minutes > 9:
            minutes1 = self.number_imgs[int(str(minutes)[0])]
            minutes2 = self.number_imgs[int(str(minutes)[1])]
        else:
            minutes2 = self.number_imgs[int(str(minutes)[0])]
            minutes1 = self.number_imgs[0]
            minutes = '0' + str(minutes)
        if seconds > 9:
            seconds1 = self.number_imgs[int(str(seconds)[0])]
            seconds2 = self.number_imgs[int(str(seconds)[1])]
        else:
            seconds2 = self.number_imgs[int(str(seconds)[0])]
            seconds1 = self.number_imgs[0]
            seconds = '0' + str(seconds)
        if miliseconds > 9:
            miliseconds1 = self.number_imgs[int(str(miliseconds)[0])]
            miliseconds2 = self.number_imgs[int(str(miliseconds)[1])]
        else:
            miliseconds2 = self.number_imgs[int(str(miliseconds)[0])]
            miliseconds1 = self.number_imgs[0]
            miliseconds = '0' + str(miliseconds)

        self.time_string = f'{minutes}:{seconds}:{miliseconds}'

        x = self.x

        blit = screen.blit

        blit(self.box, (swidth - self.box_width - 7, self.y - 7))

        blit(minutes1, (x, self.y))
        x += self.gap + self.char_width
        blit(minutes2, (x, self.y))
        x += self.gap + self.char_width
        blit(self.colon, (x, self.y))
        x += self.char_width
        blit(seconds1, (x, self.y))
        x += self.gap + self.char_width
        blit(seconds2, (x, self.y))
        x += self.gap + self.char_width
        blit(self.colon, (x, self.y))
        x += self.char_width
        blit(miliseconds1, (x, self.y))
        x += self.gap + self.char_width
        blit(miliseconds2, (x, self.y))

        return self.time_string

    def save(self):
        try:
            with open('data/times.json', 'r') as json_file:
                times_data = load(json_file)
            if times_data['time'] != 'no data':
                prev_time = time_unpacker(times_data['time'])
                current_time = time_unpacker(self.time_string)
            else:
                prev_time = 1
                current_time = 0
            if current_time < prev_time:
                with open('data/times.json', 'w') as json_file:
                    times_data['time'] = self.time_string
                    dump(times_data, json_file)
        except FileNotFoundError:
            pass
            # cheeky pass :)


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
            arrow_y = dialogue_surf.get_height() - 5 + sin((1 / 10) * self.arrow_bob_counter) * 2
            dialogue_surf.blit(self.down_arrow, (swidth / 2 - 3, arrow_y))

        if self.done:
            sound = False

        return self.done, sound


leaf_brown_img = img_loader('data/images/leaf_brown.PNG', 6, 6)
leaf_green_img = img_loader('data/images/leaf_green.PNG', 6, 6)


def update_leaves(leaf_list, screen, camera_move_x, camera_move_y, fps_adjust, cave_transition):
    blit = screen.blit
    for leaf in leaf_list:
        leaf[0][0] += (-leaf[2] / 10 + camera_move_x) * fps_adjust
        leaf[0][1] += (leaf[2] / 30 + camera_move_y) * fps_adjust
        leaf[4] += 3 * fps_adjust
        leaf[1] += 1 * fps_adjust
        offset = sin(leaf[1]/(leaf[3] * 10)) * (8 + leaf[3])
        # infinite particles
        if leaf[0][0] < -6 and not cave_transition:
            leaf[0][0] = swidth - 2
            leaf[0][1] = random.randrange(0, sheight)
        if leaf[0][0] > swidth:
            leaf[0][0] = -4
            leaf[0][1] = random.randrange(0, sheight)
        if leaf[0][1] > sheight + 20:
            leaf[0][1] = 0
            leaf[0][0] = random.randrange(0, swidth)
        if leaf[0][1] < -20 and not cave_transition:
            leaf[0][1] = sheight + 2
            leaf[0][0] = random.randrange(0, swidth)
        if leaf[5] == 1:
            img = pygame.transform.rotate(leaf_brown_img, leaf[4])
        else:
            img = pygame.transform.rotate(leaf_green_img, leaf[4])
        blit(img, (leaf[0][0], leaf[0][1] + offset))


class Game:
    def __init__(self, slow_computer, world_data, bg_data, controls, world_count, level_count, settings_counters,
                 joystick_connected):

        self.world_data = world_data
        self.bg_data = bg_data

        text = Text()
        self.text = Text()

        if settings_counters['speedrun'] == 1:
            self.speedrun_mode = False
        else:
            self.speedrun_mode = True
        self.speedrun_clock = SpeedRunClock()
        self.speedrun_time = ''
        self.speedrun_time_surf = text.make_text(['00:00:00'])

        if joystick_connected:
            if controls['configuration'][7] == 1:
                self.controller_type = 'xbox'
            else:
                self.controller_type = 'ps4'
        else:
            self.controller_type = 'xbox'

        self.game_screen = pygame.Surface((swidth, sheight))
        self.game_screen.set_colorkey((0, 0, 255))

        self.cave_background_colour = (46, 27, 47)
        self.sky_background_colour = (110, 73, 112)
        self.bg_transition_colour = [0, 0, 0]
        self.brick_colour = (86, 67, 32)

        self.bg_cloud1_pos = [0, 100]
        self.bg_cloud2_pos = [0, 130]

        self.freeze_tiles = []

        self.bridge_rumbled = False

        # longer level transition (speed run mode when changing worlds)
        self.long_transition = False

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

        self.bg_cloud1 = img_loader('data/images/clouds/cloud_background1.PNG', 500, 190)
        self.bg_cloud2 = img_loader('data/images/clouds/cloud_background2.PNG', 500, 190)

        self.button_surf = pygame.Surface((tile_size, tile_size))
        self.button_surf_alpha = 0
        self.button_surf.set_alpha(0)

        # buttons ------------------------------------------------------------------------------------------------------
        self.home_button = Button(swidth - tile_size + (tile_size - home_button_down.get_width()) / 2, 3,
                                  home_button_img, home_button_press, home_button_down)

        # background particles -----------------------------------------------------------------------------------------
        self.particle_leaves = []
        for num in range(6):
            counter = random.randrange(0, 10)
            pos = [random.randrange(0, swidth), random.randrange(0, sheight)]
            sin_speed = random.randrange(4, 6)
            speed = random.randrange(5, 7)
            rotation = random.randrange(0, 360)
            colour = random.randint(1, 2)
            part = [pos, counter, speed, sin_speed, rotation, colour]
            self.particle_leaves.append(part)

        # border surface -----------------------------------------------------------------------------------------------
        self.border = pygame.Surface((swidth / 2, sheight))
        self.border.fill((255, 0, 0))
        self.border_alpha_max = 60
        self.border_alpha = 0
        self.border.set_alpha(self.border_alpha)
        self.border_x = 0

        # speed run mode world progression texts -----------------------------------------------------------------------
        self.world_prog_txts = {
            1: self.text.make_text(['CLIMBTON FARM']),
            2: self.text.make_text(['SIZZLE CAVES']),
            3: self.text.make_text(['HOME RUN']),
        }
        self.world_prog_txt = self.world_prog_txts[1]

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
                self.eq_power_list = load(json_file)

        except FileNotFoundError:
            self.eq_power_list = []
            if world_count >= 2:
                self.eq_power_list = ["mid-air_jump"]
            if world_count >= 3:
                self.eq_power_list = ["mid-air_jump", "speed_dash"]

        # world completed screen variables -----------------------------------------------------------------------------
        self.world_completed_texts = {
            0: 'mio mao mio mao la la la la la',
            1: 'Seems like you got the hang of it!',
            2: 'The farm is now behind you, further challenges lay ahead',
            3: 'Fresh air, finally... No more damp caves',
            4: "Thanks for playing! Now you can try speedrun mode [settings]",
            5: "Beans on toast, that's the stuff"
        }

        self.world_completed_text = text.make_text([self.world_completed_texts[world_count]])
        speedrun_completed_text = text.make_text(['Nice! You must be so sweaty, better take a shower.'])
        if self.speedrun_mode:
            self.world_completed_text = speedrun_completed_text

        self.congrats_text_animation = {}
        for frame in range(0, 87):
            self.congrats_text_animation[frame] = img_loader(f'data/images/congrats_text_animation/text{frame + 1}.PNG',
                                                             tile_size * 4, tile_size * 2)

        self.world_completed_text.set_alpha(0)

        self.world_completed = False

        self.space_btn_count = 0

        self.world_completed_text_alpha = 0
        self.world_completed_text_anim_count = 0
        self.fade_counter = 255

        self.new_best = False

        # game completed scene variables -------------------------------------------------------------------------------
        self.game_completed_scene_step_counter = 1
        self.toaster_animation_counter = 0
        self.toaster_animation_frame_counter = 0
        self.toaster_frame_duration = 2
        self.toaster_animation = False
        self.toaster_alpha = 0
        self.end_counter = 0

        self.smoke_surf = pygame.Surface((tile_size, tile_size))
        self.smoke_surf.set_alpha(0)
        self.smoke_surf_alpha = 0
        self.smoke_counter = 0

        if world_count == 4:
            self.game_completed_scene_step_controller = {
                1: Dialogue('The kernels get cleaned and crushed', text),
                2: Dialogue('Then they get pushed through a screen,', text),
                3: Dialogue('so the large chunks are separated from the fine powder', text),
                4: Dialogue('That fine powder is the finished product - flour', text),
                5: Dialogue('The flour is used to make bread', text),
                6: Dialogue('The bread is used to make toast', text),
                7: Dialogue('The toast is then consumed...', text),
            }

        self.toaster_animation_frames = []
        for frame in range(0, 5):
            img = img_loader(f'data/images/toaster/toaster{frame + 1}.PNG', 100, 70)
            self.toaster_animation_frames.append(img)
        self.toaster_animation_frames[0].set_alpha(0)

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
        self.bat_harm = False

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
        self.world.create_world(self.start_x, self.start_y, world_data, bg_data, 1, world_count)
        self.player = Player(self.game_screen, self.controls, self.settings_counters, world_count)
        self.particles = Particles(particle_num)
        self.eq_manager = eqManager(self.eq_power_list, self.controls)

        # class variables ----------------------------------------------------------------------------------------------
        self.tile_list = self.world.tile_list
        self.level_length = self.world.level_length

        self.left_border = self.start_x * 32 - (480 - swidth) / 2
        self.right_border = self.left_border + self.level_length * 32 - (480 - swidth) / 2

        portal_position = self.world.portal_position
        self.portal_surface_x = portal_position[0] + tile_size / 2 - swidth / 2
        self.portal_surface_y = portal_position[1] + tile_size / 2 - sheight / 2

    def popup_window(self, popup_window, screen, button, mouse_adjustment, events, joystick_over, use_btn):
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
                                                events, joystick_over, use_btn)
            if events['keydown']:
                if events['keydown'].key == self.controls['jump']:
                    press = True
                    events['keydown'] = False
        else:
            press = False

        return press

    # updates the controller type during gameplay if one calibrates their controller mid-game
    def update_controller_type(self, joystick_controls, settings_counters):
        configuration_counter = joystick_controls[7]
        self.settings_counters = settings_counters
        self.player.settings_counters = joystick_controls[4]
        if configuration_counter == 1:
            self.controller_type = 'xbox'
        elif configuration_counter == 2:
            self.controller_type = 'ps4'

# LEVEL CHECKING =======================================================================================================
    def level_checker(self, level_count, world_count):
        # the level position needs to be offset by a certain amount to set the right spawn for the player (center)
        # calculated by tiles from the center of the mould (tiles fitting in the window)

        change_music = False

        max_level = 11
        max_world = 5
        if level_count >= max_level:
            level_count = max_level
        if world_count >= max_world:
            world_count = max_world

        self.long_transition = False

        # popup windows
        if [world_count, level_count] == bee_popup:
            self.bee_info_popup = True

        if [world_count, level_count] == dash_popup:
            self.dash_info_popup = True

        # loading world data and position info
        if self.speedrun_mode and level_count == world_ending_levels[world_count]:
            if world_count < 4:
                self.world_prog_txt = self.world_prog_txts[world_count]
                world_count += 1
                self.long_transition = self.world_prog_txt
            if world_count == 4 and world_ending_levels[4] == level_count:
                self.world_completed = True
            else:
                level_count = 1

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

        if world_count > 5:
            world_count = 5

        if [world_count, level_count] in music_change_list and self.level_check > 1 and self.level_check != level_count:
            change_music = True

        return world_data_level_checker, bg_data, world_count, level_count, change_music

# WORLD COMPLETED ======================================================================================================
    def world_completed_screen(self, screen, events, fps_adjust, joysticks, joystick_calibration, world_count):
        screen.fill((0, 0, 0))

        menu_press = False
        end_screen = False

        if self.world_completed_text_anim_count == 0:
            try:
                with open('data/times.json', 'r') as json_file:
                    times_data = load(json_file)
                if times_data['time'] != 'no data':
                    prev_time = time_unpacker(times_data['time'])
                    current_time = time_unpacker(self.speedrun_time)
                    if current_time < prev_time:
                        self.new_best = True
                else:
                    self.new_best = True
            except FileNotFoundError:
                pass
            if self.new_best:
                addon = 'New best time!: '
            else:
                addon = ''
            print(self.speedrun_time)
            self.speedrun_time_surf = self.text.make_text([f'{addon} {self.speedrun_time}'])

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
            if events['keydown'].key == pygame.K_SPACE:
                menu_press = True
        if events['joybuttondown']:
            if events['joybuttondown'].button == self.controls['configuration'][5]:
                menu_press = True

        text = self.world_completed_text
        if 0 <= self.world_completed_text_alpha <= 255:
            text.set_alpha(self.world_completed_text_alpha)
            self.speedrun_time_surf.set_alpha(self.world_completed_text_alpha)

        if joysticks:
            if self.controller_type == 'xbox':
                btn_img = self.a_button_img
            else:
                btn_img = self.cross_button_img
        else:
            self.space_btn_count += 1 * fps_adjust
            if self.space_btn_count > 50:
                btn_img = self.space_button_press
                if self.space_btn_count > 60:
                    self.space_btn_count = 0
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
        if self.speedrun_mode:
            screen.blit(self.speedrun_time_surf, (swidth / 2 - self.speedrun_time_surf.get_width() / 2, 50))
        screen.blit(congrats_text, (swidth / 2 - tile_size * 2, sheight / 2 - 60))
        if self.fade_counter == 255:
            screen.blit(btn_img, (swidth / 2 - btn_img.get_width() / 2, sheight / 2 - text.get_height() / 2 + 35))

        if menu_press and self.speedrun_mode:
            self.speedrun_clock.save()

        if self.fade_counter <= 0:
            end_screen = True

        return end_screen, menu_press

    def game_completed_cutscene(self, screen, events, fps_adjust, joysticks, joystick_calibration):
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

        end_screen = False
        press = False

        sounds = {
            'click': False
        }

        if events['keydown']:
            if events['keydown'].key == pygame.K_SPACE:
                press = True
        if events['joybuttondown']:
            if events['joybuttondown'].button == self.controls['configuration'][5]:
                press = True

        if not self.toaster_animation:
            if self.toaster_alpha > 250:
                scene_step_type = self.game_completed_scene_step_controller[self.opening_scene_step_counter]
                dialogue_done, sounds['click'] = scene_step_type.display_dialogue(self.dialogue_surface, fps_adjust)
                if dialogue_done and press:
                    self.opening_scene_step_counter += 1
                    if self.opening_scene_step_counter > len(self.game_completed_scene_step_controller):
                        self.toaster_animation = True
                if not dialogue_done and press:
                    scene_step_type.btn_press = True
            screen.blit(self.dialogue_surface, (0, 10))

            self.toaster_alpha += 10 * fps_adjust
            if self.toaster_alpha <= 255:
                self.toaster_animation_frames[0].set_alpha(self.toaster_alpha)
            elif self.toaster_alpha < 1000:
                self.toaster_animation_frames[0].set_alpha(255)
                self.toaster_alpha = 1000
            screen.blit(self.toaster_animation_frames[0], (swidth / 2 - 50, sheight / 2 - 35))

            self.smoke_surf_alpha += 6 * fps_adjust
            if self.smoke_surf_alpha <= 30:
                self.smoke_surf.set_alpha(self.smoke_surf_alpha)
            self.smoke_counter += 1 * fps_adjust
            self.smoke_surf.fill((0, 0, 0))
            for dot in range(tile_size):
                x1 = 5
                x2 = 27
                offset1 = round(sin(1 / 8 * (self.smoke_counter + dot)) * 2)
                offset2 = round(cos(1 / 8 * (self.smoke_counter + dot)) * 2)
                self.smoke_surf.set_at([x1 + offset1, dot], (255, 255, 255))
                self.smoke_surf.set_at([x2 + offset2, dot], (255, 255, 255))
            screen.blit(self.smoke_surf, (swidth / 2 - 16, sheight / 2 - 55))

        else:
            self.toaster_animation_counter += 1 * fps_adjust
            if self.toaster_animation_frame_counter < 4:
                if self.toaster_animation_counter > self.toaster_frame_duration:
                    self.toaster_animation_counter = 0
                    self.toaster_animation_frame_counter += 1

            if self.toaster_animation_counter > 130 and press:
                self.end_counter += 1
                self.toaster_alpha = 255
            if self.end_counter > 0:
                self.end_counter += 1 * fps_adjust
                self.toaster_alpha -= 8 * fps_adjust
                if self.toaster_alpha >= 0:
                    self.toaster_animation_frames[4].set_alpha(self.toaster_alpha)
                else:
                    self.toaster_animation_frames[4].set_alpha(0)
            if self.end_counter > 30:
                end_screen = True

            img = self.toaster_animation_frames[self.toaster_animation_frame_counter]

            if self.toaster_animation_frame_counter == 3:
                offset_x = random.choice([-1, 0, 1])
                offset_y = random.choice([-1, 0, 1])
            else:
                offset_x = 0
                offset_y = 0

            screen.blit(img, (swidth / 2 - 50 + offset_x, sheight / 2 - 35 + offset_y))

            if joysticks:
                if self.controller_type == 'xbox':
                    btn_img = self.a_button_img
                else:
                    btn_img = self.cross_button_img
            else:
                self.space_btn_count += 1 * fps_adjust
                if self.space_btn_count > 50:
                    btn_img = self.space_button_press
                    if self.space_btn_count > 60:
                        self.space_btn_count = 0
                else:
                    btn_img = self.space_button_img

            if self.toaster_animation_counter > 130 and self.end_counter == 0:
                self.button_surf_alpha += 10 * fps_adjust
                if self.button_surf_alpha <= 255:
                    self.button_surf.set_alpha(self.button_surf_alpha)
                self.button_surf.fill((0, 0, 0))
                self.button_surf.blit(btn_img, (16 - btn_img.get_width() / 2, 16 - btn_img.get_height() / 2))
                screen.blit(self.button_surf, (swidth / 2 - 16, sheight / 2 + 45))

        return end_screen, sounds

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
            if events['joybuttondown'].button == self.controls['configuration'][5]:
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

    def update_cloud_bg(self):
        self.game_screen.fill(self.sky_background_colour)
        self.bg_cloud1_pos[0] += self.camera_move_x / 4
        self.bg_cloud2_pos[0] += self.camera_move_x / 3
        self.bg_cloud1_pos[1] += self.camera_move_y / 4
        self.bg_cloud2_pos[1] += self.camera_move_y / 3
        blit = self.game_screen.blit
        blit(self.bg_cloud1, self.bg_cloud1_pos)
        blit(self.bg_cloud2, self.bg_cloud2_pos)
        if self.bg_cloud1_pos[0] > 0:
            blit(self.bg_cloud1, (self.bg_cloud1_pos[0] - 500, self.bg_cloud1_pos[1]))
        if self.bg_cloud2_pos[0] > 0:
            blit(self.bg_cloud2, (self.bg_cloud2_pos[0] - 500, self.bg_cloud2_pos[1]))
        if self.bg_cloud1_pos[0] < 500 - swidth:
            blit(self.bg_cloud1, (self.bg_cloud1_pos[0] + 500, self.bg_cloud1_pos[1]))
        if self.bg_cloud2_pos[0] < 500 - swidth:
            blit(self.bg_cloud2, (self.bg_cloud2_pos[0] + 500, self.bg_cloud2_pos[1]))

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
            'rumble': False,
            'bubbles': 0,
            'buzz': [],
            'laser-aim': False,
            'laser-shot': False,
            'nuh-uh': False
        }
        fadeout = False
        change_music = False
        music_slowdown = self.player.freeze

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
        if world_count == 1 and not self.speedrun_mode:
            tutorial = True
        else:
            tutorial = False

        # dealing with harm
        if self.tile_harm or self.hot_lava_harm or self.trap_harm or self.bee_harm or self.bat_harm:
            self.harm = True
        else:
            self.harm = False

        self.tile_harm = False
        self.hot_lava_harm = False
        self.trap_harm = False
        self.bee_harm = False
        self.bat_harm = False

        # preventing movement when calibrating joystick
        if joystick_calibration:
            self.move = False

        # no tutorial in speedrun mode
        if self.speedrun_mode:
            self.freeze_tiles = []

        # updating player variables ------------------------------------------------------------------------------------
        level_count,\
            sack_rect,\
            sack_direction,\
            self.health,\
            self.camera_move_x,\
            self.camera_move_y,\
            restart_level,\
            self.player_moved,\
            self.world.shockwave_mushroom_list,\
            self.gem_equipped,\
            screen_shake,\
            player_sounds,\
            border_col,\
            self.freeze_tiles,\
            card_active = self.player.update_pos_animation(screen,
                                                           self.tile_list,
                                                           self.world.next_level_list,
                                                           level_count,
                                                           world_count,
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
                                                           self.freeze_tiles,
                                                           self.speedrun_mode
                                                           )
        # updating player sounds
        sounds.update(player_sounds)
        # sack motion
        if self.camera_move_x != 0:
            moving = True
        else:
            moving = False

        if world_count == 4 and self.player_moved:
            if level_count in [1, 4]:
                change_music = True

        # updating solid tile positions --------------------------------------------------------------------------------
        self.tile_list = self.world.update_tile_list(self.camera_move_x, self.camera_move_y)

        # blitting tiles and images in the background ------------------------------------------------------------------
        if world_count in [1, 2, 5] or (world_count == 4 and level_count == 1):
            Game.update_cloud_bg(self)
        elif world_count == 4:
            self.game_screen.fill(self.brick_colour)
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
                        Game.update_cloud_bg(self)
                        self.bg_transition_colour = list(self.sky_background_colour)
            else:
                self.game_screen.fill(self.cave_background_colour)
        self.world.draw_static_tiles_background(self.game_screen)
        self.tile_harm, self.gem_equipped, sounds['gem'] = self.world.update_bg_tiles(self.game_screen, fps_adjust,
                                                                                      tutorial, self.camera_move_x,
                                                                                      self.camera_move_y, sack_rect,
                                                                                      self.gem_equipped, self.health)
        bridge_screen_shake, bridge_change_music = self.world.draw_bridge(self.game_screen, self.camera_move_x,
                                                                          self.camera_move_y, fps_adjust, sack_rect)
        if bridge_change_music:
            change_music = True
        if bridge_screen_shake:
            screen_shake = True
            if not self.bridge_rumbled:
                self.bridge_rumbled = True
                sounds['rumble'] = True

        # drawing the sack ---------------------------------------------------------------------------------------------
        self.player.blit_player(self.game_screen, draw_hitbox, fps_adjust)

        # drawing sack particles ---------------------------------------------------------------------------------------
        self.player.draw_sack_particles(self.game_screen)

        # updating level border positions ------------------------------------------------------------------------------
        self.right_border += self.camera_move_x
        self.left_border += self.camera_move_x

        # updating the world data if new level -------------------------------------------------------------------------
        if self.level_check < level_count or restart_level:
            self.world_data, self.bg_data, world_count, level_count, change_music = Game.level_checker(self,
                                                                                                       level_count,
                                                                                                       world_count)
            self.world.create_world(self.start_x, self.start_y, self.world_data, self.bg_data, level_count, world_count)
            self.freeze_tiles = self.world.freeze_tiles
            self.tile_list, self.level_length = self.world.return_tile_list()
            self.right_border = self.left_border + self.level_length * 32
            self.particles = Particles(particle_num)
            self.blit_card_instructions = False
            self.gem_equipped = False
            self.bridge_rumbled = False
            self.portal_surface_x = self.world.portal_position[0] + tile_size / 2 - swidth / 2
            self.portal_surface_y = self.world.portal_position[1] + tile_size / 2 - sheight / 2
            if not restart_level:
                self.level_check = level_count
                self.player_moved = False
                self.level_duration_counter = 0
            # resetting leaves
            self.particle_leaves = []
            append = self.particle_leaves.append
            for num in range(6):
                counter = random.randrange(0, 10)
                pos = [random.randrange(0, swidth), random.randrange(0, sheight)]
                sin_speed = random.randrange(4, 6)
                speed = random.randrange(5, 7)
                rotation = random.randrange(0, 360)
                colour = random.randint(1, 2)
                part = [pos, counter, speed, sin_speed, rotation, colour]
                append(part)
            # resetting clouds
            self.bg_cloud1_pos = [0, 100]
            self.bg_cloud2_pos = [0, 130]
            # music fading
            if world_ending_levels[world_count] == level_count and not self.speedrun_mode:
                fadeout = True

        # --------------------------------------------------------------------------------------------------------------
        if world_count in [2, 3, 5]:
            self.hot_lava_harm = self.world.draw_hot_lava(self.game_screen, sack_rect, fps_adjust)

        sounds['wheat'] = self.world.draw_wheat(self.game_screen, sack_rect, moving, fps_adjust)
        self.world.draw_green_mushrooms(self.game_screen, sack_rect)

        self.world.draw_static_tiles_foreground(self.game_screen)

        shock_mush_tutorial = False
        if [world_count, level_count] == [2, 9] and not self.speedrun_mode:
            shock_mush_tutorial = True
        self.bee_harm, sounds['buzz'] = self.world.update_fg_tiles(self.game_screen, sack_rect, fps_adjust,
                                                                   self.camera_move_x, self.camera_move_y, self.health,
                                                                   self.player_moved, shock_mush_tutorial)

        self.trap_harm, sounds['trap'] = self.world.draw_bear_trap_list(self.game_screen, sack_rect)

        # collision hightlight
        if draw_hitbox:
            self.player.highlight_cols(self.game_screen)
            self.world.draw_hitboxes(self.game_screen)

        if (world_count in [1, 2, 5] or (world_count == 4 and level_count == 1)) and \
                [world_count, level_count] != [5, 3]:
            update_leaves(self.particle_leaves, self.game_screen, self.camera_move_x, self.camera_move_y, fps_adjust,
                          False)
        if world_count == 3 and level_count == 1:
            leaves_transition = True
            if not self.player_moved:
                leaves_transition = False
            update_leaves(self.particle_leaves, self.game_screen, self.camera_move_x, self.camera_move_y, fps_adjust,
                          leaves_transition)

        # drawing the bat ----------------------------------------------------------------------------------------------
        if world_count == 3:
            self.bat_harm, bat_screen_shake, bat_change_music, bat_sounds = \
                self.world.draw_bat(sack_rect, self.game_screen, fps_adjust, self.camera_move_x, self.camera_move_y,
                                    self.player_moved, self.health, draw_hitbox)
            if bat_screen_shake:
                screen_shake = True
            if bat_change_music:
                change_music = True
            sounds.update(bat_sounds)

        # drawing bean popup -------------------------------------------------------------------------------------------
        self.world.draw_bean_popup(self.game_screen)

        # drawing the border -------------------------------------------------------------------------------------------
        if border_col != 0:
            self.border_alpha = self.border_alpha_max
        self.border_alpha -= 2 * fps_adjust
        self.border_x += self.camera_move_x
        if border_col == 1:
            self.border_x = self.right_border
        if border_col == -1:
            self.border_x = self.left_border - (swidth / 2)
        if self.border_alpha > 0:
            self.border.set_alpha(self.border_alpha)
            self.game_screen.blit(self.border, (self.border_x, 0))

        # speedrun clock -----------------------------------------------------------------------------------------------
        if self.speedrun_mode:
            self.speedrun_time = self.speedrun_clock.update_clock(fps_adjust, self.game_screen)

        # blitting the game screen onto the main screen ----------------------------------------------------------------
        if screen_shake:
            screen.blit(self.game_screen, (random.choice([-3, 0, 3]), random.choice([-3, 0, 3])))
        else:
            screen.blit(self.game_screen, (0, 0))

        # respawn instructions -----------------------------------------------------------------------------------------
        self.player.blit_button_instructions(screen, fps_adjust, joystick_connected, self.settings_counters)

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
                sounds['card'], sounds['nuh-uh'] = self.eq_manager.draw_eq(screen, self.eq_power_list, mouse_adjustment,
                                                                           events, tutorial, fps_adjust, level_count,
                                                                           self.health, self.move, self.player_moved,
                                                                           self.gem_equipped, self.controls,
                                                                           joysticks, self.controller_type,
                                                                           joystick_calibration, card_active)

        if self.mid_air_jump_trigger or self.speed_dash_trigger:
            self.gem_equipped = False

        # popup window -------------------------------------------------------------------------------------------------
        ok_over = False

        if joystick_connected:
            joystick_over = True
        else:
            joystick_over = False

        # new card popup and card animation
        if self.new_card_animation:
            card_type = level_card_dictionary[f"level{level_count}_{world_count}"]
            if card_type in self.eq_power_list:
                self.new_card_animation = False
            else:
                if self.level_duration_counter > 1.45:
                    popup_new_card_press = Game.popup_window(self, self.new_card_popup, screen, self.ok_new_card_button,
                                                             mouse_adjustment, events, joystick_over,
                                                             self.controls['configuration'][5])

                    self.eq_manager.new_card(card_type, screen, fps_adjust, self.level_duration_counter)

                    if popup_new_card_press:
                        self.new_card_animation = False
                        self.eq_power_list.append(card_type)
                        self.reinit_eq = True
                        try:
                            with open('data/collected_cards.json', 'w') as json_file:
                                dump(self.eq_power_list, json_file)
                        except FileNotFoundError:
                            power_list_not_saved_error = True

        else:
            self.move = True

        if ok_over:
            sounds['button'] = True

        # new level transition -----------------------------------------------------------------------------------------
        if self.player_moved:
            self.long_transition = False
        self.player.draw_transition(fps_adjust, self.long_transition)

        # sounds -------------------------------------------------------------------------------------------------------
        if not self.music_playing:
            self.music_playing = True
            play_music = True

        # returns
        return level_count, world_count, play_music, sounds,\
            fadeout, popup_lvl_completed_press, self.world_completed, change_music, music_slowdown
