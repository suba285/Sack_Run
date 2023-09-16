import time
import threading
from screen_info import *
import pygame._sdl2
import os

os.environ['SDL_JOYSTICK_HIDAPI_PS4_RUMBLE'] = '1'

pygame.init()
pygame.joystick.init()
pygame.mixer.pre_init(40000, -16, 1, 1024)
joysticks = {}

# pygame events --------------------------------------------------------------------------------------------------------
allowed_events = [pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.JOYAXISMOTION,
                  pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED,
                  pygame.VIDEORESIZE, pygame.QUIT, pygame.MOUSEWHEEL]
pygame.event.set_allowed(allowed_events)

# basic game variables -------------------------------------------------------------------------------------------------
monitor_width = global_monitor_width
monitor_height = global_monitor_height
screen_width = global_screen_width
screen_height = global_screen_height

wiheight = sheight
wiwidth = swidth
tile_size = global_tile_size


clock = pygame.time.Clock()
fps = 60

# errors
settings_not_saved_error = False
settings_not_loaded_error = False

# loading settings data
try:
    with open('data/controllers.json', 'r') as json_file:
        controllers = json.load(json_file)

except FileNotFoundError:
    settings_not_loaded_error = True
    controllers = {}

try:
    with open('data/settings_configuration.json', 'r') as json_file:
        settings_counters = json.load(json_file)

except FileNotFoundError:
    settings_not_loaded_error = True

    settings_counters = {
        'walking': 1,
        'jumping': 1,
        'cards': 1,
        'configuration': 1,
        'resolution': 1,
        'pov': 1,
        'hitbox': 1,
        'speedrun': 1,
        'music_volume': 2,
        'sounds': 2
    }

if settings_counters['speedrun'] == 1:
    speedrun_mode = False
else:
    speedrun_mode = True

# creating the window and setting the resolution -----------------------------------------------------------------------

resolutions = {
        '1': (swidth * 2, sheight * 2),
        '2': (swidth * 3, sheight * 3),
        '3': (swidth * 4, sheight * 4),
        '4': (screen_width, screen_height)
    }

resolution_1 = resolutions['1']
resolution_2 = resolutions['2']
resolution_3 = resolutions['3']

list_of_resolutions = [resolution_3, resolution_2, resolution_1]

recommended_resolution = resolution_1

resolution_counter = 3

for res in list_of_resolutions:
    if res[0] < monitor_width:
        recommended_resolution = res
        break
    resolution_counter -= 1

if resolution_counter < 1:
    resolution_counter = 1


if settings_counters['resolution'] == 4:
    wiwidth = screen_width
    wiheight = screen_height
    display_geometry = (monitor_width, monitor_height)
    flag = pygame.FULLSCREEN
    resolution_counter = 4
    height_window_space = monitor_height
    width_window_space = monitor_width
else:
    geometry = resolutions[str(settings_counters['resolution'])]
    wiwidth = geometry[0]
    wiheight = geometry[1]
    display_geometry = (wiwidth, wiheight)
    flag = pygame.RESIZABLE
    resolution_counter = settings_counters['resolution']
    height_window_space = wiheight
    width_window_space = wiwidth

scale = wiwidth / swidth

settings_counters['resolution'] = resolution_counter
recommended_res_counter = resolution_counter

# screens (surfaces)
window = pygame.display.set_mode(display_geometry, flag, pygame.DOUBLEBUF)
window.fill((0, 0, 0))
screen = pygame.Surface((swidth, sheight), pygame.SCALED).convert_alpha()
screen.set_alpha(0)
screen_alpha = 0
main_screen = pygame.Surface((swidth, sheight), pygame.SCALED).convert_alpha()
menu_screen = pygame.Surface((swidth, sheight), pygame.SCALED).convert_alpha()
pause_screen = pygame.Surface((swidth, sheight), pygame.SCALED).convert_alpha()
level_selection_screen = pygame.Surface((swidth, sheight), pygame.SCALED).convert_alpha()
settings_screen = pygame.Surface((swidth, sheight), pygame.SCALED).convert_alpha()

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])

pygame.display.set_caption('sack run')

background_sky_colour = (100, 63, 102)

# external file imports ------------------------------------------------------------------------------------------------
from levels import *
from game import Game, world_ending_levels
from menu import mainMenu
from display_fps import FpsDisplay
from font_manager import Text
from popup_bg_generator import popup_bg_generator
from pause_screen import PauseScreen
from world_selection import LevelSelection
from game import level_dictionary, level_bg_dictionary
from settings import SettingsMenu
from image_loader import img_loader
import random

# ----------------------------------------------------------------------------------------------------------------------

world_data = level1_1
bg_data = level1_1_bg
first_level = 1

try:
    with open('data/level_count.json', 'r') as json_file:
        level_counters = json.load(json_file)

except FileNotFoundError:
    level_counters = [1, 1, 1, 1]
try:
    with open('data/unlocked_worlds.json', 'r') as json_file:
        unlocked_worlds_data = json.load(json_file)
        counter = 1
        for value in unlocked_worlds_data:
            if not value:
                world_count = counter - 1
                break

            counter += 1
        if counter > 4:
            world_count = 4
except FileNotFoundError:
    world_count = 1


level_count = level_counters[world_count - 1]

nums_to_unlocked_world_data = {
    1: 1,
    2: 2,
    3: 3,
    4: 4
}

default_game_counter = -3
game_counter = default_game_counter

# variables ------------------------------------------------------------------------------------------------------------
text = Text()

slow_computer = False
run = True
run_game = False
run_menu = True
run_settings = False
paused = False
game_paused = False
play_press = False
play = False
run_level_selection = False
level_selection = False
menu_transition_counter = 0
menu_transition = False
proceed_with_transition = False
reload_world_status = False
menu_y = 0
game_y = swidth

new_world_unlocked = False

opening_scene = True

world_completed = False
world_completed_transition_counter = 0
world_completed_trans_surf = pygame.Surface((swidth, sheight))
world_completed_trans_surf.fill((0, 0, 0))

level_restart_procedure = False

if settings_counters['hitbox'] == 1:
    draw_hitbox = False
else:
    draw_hitbox = True
draw_fps_counter = True

# mouse
last_mouse_pos = pygame.mouse.get_pos()
mouse_still_count = 0
mouse_vis = True
show_cursor = True

# music
play_music = False
play_music_trigger = False
fadeout_music = False
world_completed_sound_played = False
play_background_music = True
play_sounds = True
if settings_counters['sounds'] == 1:
    play_sounds = False
if settings_counters['music_volume'] == 1:
    play_background_music = False

user_quit1 = False
user_quit2 = False

# loading message ------------------------------------------------------------------------------------------------------
loading_text = text.make_text(['Loading'])
loading_bg = popup_bg_generator((loading_text.get_width() + 12, loading_text.get_height() + 30))
loading_text_x = loading_bg.get_width() / 2 - loading_text.get_width() / 2
loading_text_y = loading_bg.get_height() / 2 - loading_text.get_height() / 2 - 5
loading_bg.blit(loading_text, (loading_text_x, loading_text_y))

loading_animation = {}
index_counter = 0
for file in range(-13, 13):
    loading_animation[index_counter] = img_loader(f'data/images/loading_animation/frame{abs(file)}.PNG',
                                                  16, 8)
    index_counter += 1
loading_erase_surf = pygame.Surface((16, 8))
loading_erase_surf.fill((79, 70, 81))
loading_anim_x = loading_bg.get_width() / 2 - 8
loading_anim_y = loading_text_y + 15
loading_counter = 0

screen_dim = pygame.Surface((swidth, sheight))
screen_dim.set_alpha(80)
screen_dim.fill((0, 0, 0))

# sounds ---------------------------------------------------------------------------------------------------------------
sounds = {
        'card_pull': pygame.mixer.Sound('data/sounds/card_pull_short2.wav'),
        'lock': pygame.mixer.Sound('data/sounds/lock_click.wav'),
        'step_grass1': pygame.mixer.Sound('data/sounds/step_grass1.wav'),
        'step_grass2': pygame.mixer.Sound('data/sounds/step_grass2.wav'),
        'step_wood': pygame.mixer.Sound('data/sounds/step_wood.wav'),
        'step_rock1': pygame.mixer.Sound('data/sounds/step_rock1.wav'),
        'step_rock2': pygame.mixer.Sound('data/sounds/step_rock2.wav'),
        'landing': pygame.mixer.Sound('data/sounds/landing.wav'),
        'jump': pygame.mixer.Sound('data/sounds/jump.wav'),
        'mid_air_jump': pygame.mixer.Sound('data/sounds/mid_air_jump.wav'),
        'mushroom': pygame.mixer.Sound('data/sounds/mushroom.wav'),
        'bear_trap_cling': pygame.mixer.Sound('data/sounds/bear_trap_cling.wav'),
        'gem': pygame.mixer.Sound('data/sounds/gem.wav'),
        'death': pygame.mixer.Sound('data/sounds/death2.wav'),
        'wheat': pygame.mixer.Sound('data/sounds/wheat.wav'),
        'button_click': pygame.mixer.Sound('data/sounds/button_click.wav'),
        'world_completed': pygame.mixer.Sound('data/sounds/world_completed_sound.wav'),
        'click': pygame.mixer.Sound('data/sounds/click.wav'),
        'sack_noise': pygame.mixer.Sound('data/sounds/sack_noise.wav'),
    }

# wheat channel
pygame.mixer.Channel(1)
pygame.mixer.Channel(1).set_volume(0.3)

walk_sound_switch = False
step_sound_volume = 0.7

sounds['card_pull'].set_volume(0.4)
sounds['lock'].set_volume(2.5)
sounds['bear_trap_cling'].set_volume(0.6)
sounds['button_click'].set_volume(1.4)
sounds['world_completed'].set_volume(0.6)
sounds['step_grass1'].set_volume(step_sound_volume)
sounds['step_grass2'].set_volume(step_sound_volume)
sounds['step_wood'].set_volume(0.15)
sounds['step_rock1'].set_volume(0.5)
sounds['step_rock2'].set_volume(0.2)
sounds['landing'].set_volume(0.1)
sounds['death'].set_volume(0.7)
sounds['jump'].set_volume(0.3)
sounds['mid_air_jump'].set_volume(0.8)
sounds['gem'].set_volume(0.3)
sounds['click'].set_volume(0.3)
sounds['sack_noise'].set_volume(0.5)
sounds['mushroom'].set_volume(1.2)

music = {
    '1': 'game_song1',
    '2': 'game_song2',
    '3': 'game_song3',
    '4': 'game_song4'
}

music_volumes = {
    '1': 0,
    '2': 0.3,
    '3': 0.6
}

paused_music_volume = 0.1
speedrun_volume = 0.6

pygame.mixer.music.load('data/sounds/game_song1.wav')
pygame.mixer.music.set_volume(music_volumes[str(settings_counters['music_volume'])])

# when True: adjust volume to background level (it was increased for demonstration purposes)
adjust_settings_music_volume = False

# sound locks
one_time_play_card_pull = True
one_time_play_button1 = True
one_time_play_button2 = True
one_time_play_lock = True
card_swoosh_chest = False
card_swoosh_counter = 0

# joystick variables
joystick_moved = False
joystick_idle = True
joystick_connected = False
joystick_configured = False
joystick_name = ''

# controls -------------------------------------------------------------------------------------------------------------
controls_nums = {
    'left1': pygame.K_a,
    'right1': pygame.K_d,
    'left2': pygame.K_LEFT,
    'right2': pygame.K_RIGHT,
    'jump1': pygame.K_SPACE,
    'jump2': pygame.K_w,
    'jump3': pygame.K_UP,
    'configuration': [[0, 1], 4, 5, 10, 1],  # controller button configuration [lb, rb, pause, settings_counter]
    'cards1': 'mouse',
    'cards2': 'keyboard',
}

controls = {
    'left': controls_nums[f"left{settings_counters['walking']}"],
    'right': controls_nums[f"right{settings_counters['walking']}"],
    'jump': controls_nums[f"jump{settings_counters['jumping']}"],
    'configuration': controls_nums["configuration"],
    'cards': controls_nums[f"cards{settings_counters['cards']}"],
}

# custom cursor setup --------------------------------------------------------------------------------------------------
pygame.mouse.set_visible(False)
cursor_raw = pygame.image.load('data/images/cursor_classic2.PNG').convert()
pointer_raw = pygame.image.load('data/images/cursor_classic2_point.PNG').convert()
pointer = pygame.transform.scale(pointer_raw, (tile_size/4, tile_size/4))
pointer.set_colorkey((0, 0, 0))
cursor = pygame.transform.scale(cursor_raw, (tile_size/4, tile_size/4))
cursor.set_colorkey((0, 0, 0))

# initiating classes ---------------------------------------------------------------------------------------------------
main_game = Game(slow_computer, world_data, bg_data, controls, world_count, settings_counters, joystick_connected)
main_menu = mainMenu()
pause_menu = PauseScreen(pause_screen)
level_select = LevelSelection(world_count)
settings_menu = SettingsMenu(controls, settings_counters, resolutions, recommended_res_counter)

fps_display = FpsDisplay()

# function for loading the game as a separate thread
game_loaded = False
loading = False


def load_game(local_world_data, local_bg_data, local_world_count, local_joystick_connected):
    global main_game, game_loaded
    main_game = Game(slow_computer, local_world_data, local_bg_data, controls, local_world_count,
                     settings_counters, local_joystick_connected)
    game_loaded = True


# TEXT -----------------------------------------------------------------------------------------------------------------

# error variables and error messages
settings_not_saved_error_counter = 300
settings_not_saved_error_txt = text.make_text(['error while saving settings configuration'])
settings_not_loaded_error_txt = text.make_text(['error while loading settings configuration'])
# controller connections
controller_not_configured_txt = text.make_text(['Controller not configured [settings]'])
controller_not_configured_popup = popup_bg_generator((controller_not_configured_txt.get_width() + 10, 15))
controller_not_configured_popup.blit(controller_not_configured_txt, (7, 7))
controller_not_configured_counter = 0

controller_connected_txt = text.make_text(['Controller connected'])
controller_disconnected_txt = text.make_text(['Controller disconnected'])
controller_connected_popup = popup_bg_generator((controller_connected_txt.get_width() + 10, 15))
controller_disconnected_popup = popup_bg_generator((controller_disconnected_txt.get_width() + 10, 15))
controller_connected_popup.blit(controller_connected_txt, (7, 7))
controller_disconnected_popup.blit(controller_disconnected_txt, (7, 7))
controller_connected_counter = 0
controller_disconnected_counter = -10
controller_popup = controller_connected_popup

controller_calibration = False
calibration_start_counter = 0

# fps variables --------------------------------------------------------------------------------------------------------
last_time = time.time()
last_fps = 1
last_fps_adjust = 1

game_duration_counter = 0

# MAIN LOOP ============================================================================================================
while run:
    try:
        event_list = pygame.event.get()
    except SystemError:
        event_list = []
    events = {
        'quit': False,
        'keydown': False,
        'keyup': False,
        'mousebuttondown': False,
        'mousebuttonup': False,
        'joyaxismotion_y': False,
        'joyaxismotion_x': False,
        'joybuttondown': False,
        'joybuttonup': False,
        'joydeviceadded': False,
        'joydeviceremoved': False,
        'mousewheel': False,
        'videoresize': False,
    }
    for event in event_list:
        if event.type == pygame.QUIT:
            events['quit'] = event
        if event.type == pygame.KEYDOWN:
            events['keydown'] = event
        if event.type == pygame.KEYUP:
            events['keyup'] = event
        if event.type == pygame.MOUSEBUTTONDOWN:
            events['mousebuttondown'] = event
        if event.type == pygame.MOUSEBUTTONUP:
            events['mousebuttonup'] = event
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == controls['configuration'][0][0]:
                events['joyaxismotion_x'] = event
            if event.axis == controls['configuration'][0][1]:
                events['joyaxismotion_y'] = event
        if event.type == pygame.JOYBUTTONDOWN:
            events['joybuttondown'] = event
        if event.type == pygame.JOYBUTTONUP:
            events['joybuttonup'] = event
        if event.type == pygame.JOYDEVICEADDED:
            events['joydeviceadded'] = event
        if event.type == pygame.JOYDEVICEREMOVED:
            events['joydeviceremoved'] = event
        if event.type == pygame.MOUSEWHEEL:
            events['mousewheel'] = event
        if event.type == pygame.VIDEORESIZE:
            events['videoresize'] = event

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    if joystick_connected:
        events['joyconnected'] = True
    else:
        events['joyconnected'] = False
    key = pygame.key.get_pressed()

    # sound triggers
    button_sound_trigger1 = False
    button_sound_trigger2 = False
    button_sound_trigger3 = False
    sound_triggers = {
        'card': False,
        'lock': False,
        'trap': False,
        'button': False,
        'step_grass': False,
        'step_wood': False,
        'step_rock': False,
        'jump': False,
        'mid_air_jump': False,
        'mushroom': False,
        'land': False,
        'death': False,
        'wheat': False,
        'swoosh': False,
        'gem': False,
        'click': False,
        'sack_noise': False
    }

    load_music = False

    adjust_resolution = False

    if not run_level_selection:
        reload_world_status = True

    mouse_adjustment = [(wiwidth / swidth),
                        (swidth / wiwidth) * ((height_window_space - wiheight) / 2),
                        (swidth / wiwidth) * ((width_window_space - wiwidth) / 2)]

    # fps adjustment ---------------------------------------------------------------------------------------------------
    fps_adjust = time.time() - last_time
    fps_adjust = fps_adjust * 60
    real_fps = clock.get_fps()
    if fps_adjust > 3:
        fps_adjust = 3
    last_time = time.time()
    last_fps_adjust = fps_adjust
    fps_int = int(real_fps)

    clock.tick(60)

    # joystick variables and counters
    joystick_moved = False
    joystick_over_card = False
    game_duration_counter += 1 * fps_adjust
    if game_duration_counter > 20:
        controller_disconnected_counter -= 1 * fps_adjust
        controller_connected_counter -= 1 * fps_adjust
    calibration_start_counter += 1 * fps_adjust

    # running the menu -------------------------------------------------------------------------------------------------
    if run_menu:
        run_game = False
        game_paused = False
        if not controller_calibration:
            menu_events = events
        else:
            menu_events = {
                'quit': False,
                'keydown': False,
                'keyup': False,
                'mousebuttondown': False,
                'mousebuttonup': False,
                'joyaxismotion_y': False,
                'joyaxismotion_x': False,
                'joybuttondown': False,
                'joybuttonup': False,
                'joydeviceadded': False,
                'joydeviceremoved': False,
                'mousewheel': False,
                'videoresize': False
            }
        controller_not_configured_counter -= 1 * fps_adjust
        level_selection, sound_triggers['button'],\
            button_sound_trigger3, settings = main_menu.menu(menu_screen,
                                                             mouse_adjustment, menu_events, fps_adjust,
                                                             joysticks, speedrun_mode)

        # settings not saved error
        if settings_not_saved_error:
            settings_not_saved_error_counter -= 1 * fps_adjust
            if settings_not_saved_error_counter >= 0:
                menu_screen.blit(settings_not_saved_error_txt,
                                 (swidth / 2 - settings_not_loaded_error_txt.get_width() / 2, 3))

        # changing the displayed screens
        if level_selection and (joystick_configured or not joystick_connected):
            if speedrun_mode:
                world_data = level_dictionary[f'level1_1']
                bg_data = level_bg_dictionary[f'level1_1_bg']
                world_count = 1
                level_count = 1
                threading.Thread(target=load_game, args=[world_data, bg_data, world_count, joystick_connected]).start()
                loading = True
                proceed_with_transition = False
            else:
                run_game = False
                run_level_selection = True
                game_counter = default_game_counter
                run_menu = False
                menu_y = 0
                game_y = swidth

        if game_loaded:
            loading = False
            play = True
            load_music = True
            play_music = True
            game_loaded = False
            world_completed = False

        if loading:
            loading_counter += 0.4 * fps_adjust
            if loading_counter > len(loading_animation) - 1:
                loading_counter = 0
            menu_screen.blit(screen_dim, (0, 0))
            loading_bg.blit(loading_erase_surf, (loading_anim_x, loading_anim_y))
            loading_frame = loading_animation[round(loading_counter)]
            loading_bg.blit(loading_frame, (loading_anim_x, loading_anim_y))
            menu_screen.blit(loading_bg,
                                        (swidth / 2 - loading_bg.get_width() / 2,
                                         sheight / 2 - loading_bg.get_height() / 2))

        if play:
            game_counter = default_game_counter
            run_menu = False
            run_game = True
            paused = False
            run_level_selection = False
            menu_transition = True
            menu_transition_counter = 0

        # controller not configured message trigger
        if level_selection and joystick_connected and not joystick_configured:
            controller_not_configured_counter = 80

        # controller not configured message
        if controller_not_configured_counter > 0:
            menu_screen.blit(controller_not_configured_popup,
                             (swidth / 2 - controller_not_configured_popup.get_width() / 2,
                              130))

        # changing the displayed screens
        if settings:
            run_game = False
            run_menu = False
            run_settings = True
            run_level_selection = False
            if joystick_connected and not joystick_configured:
                settings_menu.section_counter = 0
                settings_menu.joystick_counter = 1
            settings_menu.screen_alpha_counter = 0
            pygame.mixer.music.load('data/sounds/game_song1.wav')

    # running the game -------------------------------------------------------------------------------------------------
    if run_game:
        game_paused = False
        if play:
            world_completed_sound_played = False
            play = False

        if not (world_count == 1 and level_count == 1) or settings_counters['speedrun'] == 2:
            opening_scene = False

        run_menu = False
        if pygame.WINDOWMAXIMIZED not in events and not world_completed and not opening_scene:
            level_count,\
                world_count,\
                play_music_trigger,\
                game_sounds,\
                fadeout_music,\
                lvl_selection_press,\
                world_completed = main_game.game(screen, level_count, fps_adjust,
                                                 draw_hitbox, mouse_adjustment, events,
                                                 game_counter, world_count, controls,
                                                 controller_calibration, joysticks, level_restart_procedure)
            level_restart_procedure = False
            sound_triggers.update(game_sounds)
        else:
            menu_press = False
            lvl_selection_press = False

        if world_completed:
            lvl_selection_press = main_game.world_completed_screen(screen, events, fps_adjust, joysticks,
                                                                   controller_calibration, world_count)
            world_completed_transition_counter = 255
            if lvl_selection_press:
                main_menu.update_time()
                events = {
                    'quit': False,
                    'keydown': False,
                    'keyup': False,
                    'mousebuttondown': False,
                    'mousebuttonup': False,
                    'joyaxismotion_y': False,
                    'joyaxismotion_x': False,
                    'joybuttondown': False,
                    'joybuttonup': False,
                    'joydeviceadded': False,
                    'joydeviceremoved': False,
                    'mousewheel': False,
                    'videoresize': False
                }

        if opening_scene:
            opening_scene_done, opening_scene_sounds = main_game.opening_cutscene(screen, fps_adjust, events,
                                                                                  controller_calibration)
            sound_triggers.update(opening_scene_sounds)
            if opening_scene_done:
                opening_scene = False

        if play_music_trigger:
            play_music = True

        # pausing (joystick pausing can be found in 'game event handling')
        if key[pygame.K_ESCAPE]:
            run_menu = False
            run_game = False
            paused = True
            run_level_selection = False
            pygame.mixer.music.set_volume(paused_music_volume)
            pause_menu.joystick_counter = 0

        # changing the displayed screens
        if lvl_selection_press:
            try:
                with open('data/level_count.json', 'w') as json_file:
                    level_count = 1
                    level_counters[world_count - 1] = level_count
                    json.dump(level_counters, json_file)
            except FileNotFoundError:
                pass

            try:
                with open('data/unlocked_worlds.json', 'r') as json_file:
                    unlocked_world_data = json.load(json_file)
            except FileNotFoundError:
                unlocked_world_data = [True, False, False, False, False]
            if world_count < 4 and not unlocked_world_data[world_count]:
                new_world_unlocked = True
            if world_count < 5:
                unlocked_world_data[world_count] = True
            try:
                with open('data/unlocked_worlds.json', 'w') as json_file:
                    json.dump(unlocked_world_data, json_file)
                    if unlocked_world_data[-1]:
                        settings_menu.speedrun_unlocked = True
            except FileNotFoundError:
                progress_not_saved_error = True

            game_counter = default_game_counter
            if speedrun_mode:
                run_menu = True
                run_level_selection = False
            else:
                run_menu = False
                run_level_selection = True
            run_game = False
            run_settings = False
            fadeout_music = True
            menu_y = 0
            game_y = swidth

    # pause ------------------------------------------------------------------------------------------------------------
    if paused:
        game_paused = True
        if joystick_configured or not joystick_connected or controller_calibration:
            paused_events = events
        else:
            paused_events = {
                'quit': False,
                'keydown': False,
                'keyup': False,
                'mousebuttondown': False,
                'mousebuttonup': False,
                'joyaxismotion_y': False,
                'joyaxismotion_x': False,
                'joybuttondown': False,
                'joybuttonup': False,
                'joydeviceadded': False,
                'joydeviceremoved': False,
                'mousewheel': False,
                'videoresize': False
            }
        pause_screen,\
            sound_triggers['button'],\
            resume,\
            lvl_select,\
            settings,\
            restart_level = pause_menu.draw_pause_screen(mouse_adjustment, paused_events,
                                                         joysticks, controls['configuration'],
                                                         fps_adjust, opening_scene)

        if lvl_select:
            if speedrun_mode:
                run_game = False
                run_level_selection = False
                run_settings = False
                run_menu = True
                paused = False
                screen_alpha = 0
                fadeout_music = True
                main_game.update_controller_type(controls['configuration'], settings_counters)
            else:
                run_game = False
                run_level_selection = True
                run_settings = False
                run_menu = False
                paused = False
                screen_alpha = 0
                fadeout_music = True
                main_game.update_controller_type(controls['configuration'], settings_counters)
                try:
                    with open('data/level_count.json', 'w') as json_file:
                        if level_count == world_ending_levels[world_count]:
                            level_count = 1
                        else:
                            pass
                        level_counters[world_count - 1] = level_count
                        json.dump(level_counters, json_file)

                except FileNotFoundError:
                    pass

        if restart_level:
            resume = True

        if resume:
            run_menu = False
            run_game = True
            paused = False
            run_level_selection = False
            if speedrun_mode:
                pygame.mixer.music.set_volume(speedrun_volume)
            else:
                pygame.mixer.music.set_volume(music_volumes[str(settings_counters['music_volume'])])
            main_game.update_controller_type(controls['configuration'], settings_counters)
            if restart_level:
                level_restart_procedure = True

        if settings:
            run_menu = False
            run_game = False
            paused = False
            run_level_selection = False
            run_settings = True
            if joystick_connected and not joystick_configured:
                settings_menu.section_counter = 0
                settings_menu.joystick_counter = 1
            settings_menu.screen_alpha_counter = 0

    # world selection --------------------------------------------------------------------------------------------------
    if run_level_selection:
        world_completed_transition_counter -= 10 * fps_adjust
        if reload_world_status:
            try:
                with open('data/unlocked_worlds.json', 'r') as json_file:
                    level_select.world_status = json.load(json_file)
                    reload_world_status = False
            except FileNotFoundError:
                world_status_loading_error = True
                level_select.world_status = [True, False, False, False, False]
        if joystick_configured or not joystick_connected or controller_calibration:
            lvl_selection_events = events
        else:
            lvl_selection_events = {
                'quit': False,
                'keydown': False,
                'keyup': False,
                'mousebuttondown': False,
                'mousebuttonup': False,
                'joyaxismotion_y': False,
                'joyaxismotion_x': False,
                'joybuttondown': False,
                'joybuttonup': False,
                'joydeviceadded': False,
                'joydeviceremoved': False,
                'mousewheel': False,
                'videoresize': False
            }
        play_press,\
            menu,\
            world_count,\
            new_world_unlocked,\
            level_selection_sounds = level_select.draw_level_selection(level_selection_screen, mouse_adjustment,
                                                                       lvl_selection_events,
                                                                       controls, joysticks, fps_adjust, world_count,
                                                                       new_world_unlocked)
        sound_triggers.update(level_selection_sounds)

        if play_press and (joystick_configured or not joystick_connected):
            if world_count != 1:
                level_count = level_counters[world_count - 1]
            else:
                level_count = 1
            if settings_counters['speedrun'] == 2:
                level_count = 1
            opening_scene = True
            world_data = level_dictionary[f'level{level_count}_{world_count}']
            bg_data = level_bg_dictionary[f'level{level_count}_{world_count}_bg']
            threading.Thread(target=load_game, args=[world_data, bg_data, world_count, joystick_connected]).start()
            loading = True
            proceed_with_transition = False

        if game_loaded:
            loading = False
            play = True
            load_music = True
            game_loaded = False
            world_completed = False

        if loading:
            loading_counter += 0.4 * fps_adjust
            if loading_counter > len(loading_animation) - 1:
                loading_counter = 0
            level_selection_screen.blit(screen_dim, (0, 0))
            loading_bg.blit(loading_erase_surf, (loading_anim_x, loading_anim_y))
            loading_frame = loading_animation[round(loading_counter)]
            loading_bg.blit(loading_frame, (loading_anim_x, loading_anim_y))
            level_selection_screen.blit(loading_bg,
                                        (swidth / 2 - loading_bg.get_width() / 2,
                                         sheight / 2 - loading_bg.get_height() / 2))

        if world_completed_transition_counter > 0:
            world_completed_trans_surf.set_alpha(world_completed_transition_counter)
            level_selection_screen.blit(world_completed_trans_surf, (0, 0))

        if play:
            game_counter = default_game_counter
            run_menu = False
            run_game = True
            paused = False
            run_level_selection = False
            menu_transition = True
            menu_transition_counter = 0

        if menu:
            run_menu = True
            run_game = False
            paused = False
            run_level_selection = False

    # settings ---------------------------------------------------------------------------------------------------------
    if run_settings:
        if controller_calibration:
            settings_events = {
                'quit': False,
                'keydown': False,
                'keyup': False,
                'mousebuttondown': False,
                'mousebuttonup': False,
                'joyaxismotion_y': False,
                'joyaxismotion_x': False,
                'joybuttondown': False,
                'joybuttonup': False,
                'joydeviceadded': False,
                'joydeviceremoved': False,
                'mousewheel': False,
                'videoresize': False
            }
        else:
            settings_events = events

        menu,\
            controls,\
            button_sound_trigger1,\
            button_sound_trigger2,\
            performance_counter,\
            current_resolution,\
            adjust_resolution,\
            settings_counters,\
            calibrated_press,\
            settings_music_control = settings_menu.draw_settings_menu(settings_screen, mouse_adjustment,
                                                                      settings_events, fps_adjust, joystick_connected,
                                                                      joysticks, game_paused)

        if performance_counter == 1:
            slow_computer = False
        else:
            slow_computer = True

        if settings_music_control['play']:
            play_music = True
            play_background_music = True
        if settings_music_control['fadeout']:
            fadeout_music = True
        if settings_music_control['real_volume']:
            if speedrun_mode:
                settings_volume = speedrun_volume
            else:
                settings_volume = music_volumes[str(settings_counters['music_volume'])]
            pygame.mixer.music.set_volume(settings_volume)
            if not game_paused and not adjust_settings_music_volume:
                play_music = True
            adjust_settings_music_volume = True
        elif adjust_settings_music_volume:
            if game_paused:
                pygame.mixer.music.set_volume(paused_music_volume)
            else:
                fadeout_music = True
            adjust_settings_music_volume = False

        if adjust_resolution:
            wiwidth = current_resolution[0]
            wiheight = current_resolution[1]
            height_window_space = wiheight
            width_window_space = wiwidth
            if settings_counters['resolution'] == 4:
                height_window_space = monitor_height
                width_window_space = monitor_width
                flag = pygame.FULLSCREEN
                window = pygame.display.set_mode((monitor_width, monitor_height), flag)
            else:
                flag = pygame.RESIZABLE
                window = pygame.display.set_mode(current_resolution, flag)
            try:
                with open('data/settings_configuration.json', 'w') as json_file:
                    json.dump(settings_counters, json_file)
            except Exception:
                settings_not_saved_error = True
            pygame.event.clear(pygame.VIDEORESIZE, pygame.WINDOWMAXIMIZED)

        if calibrated_press:
            joystick_configured = True
            if joystick_connected and joystick_name != '':
                controllers[joystick_name] = controls['configuration']
                try:
                    with open('data/controllers.json', 'w') as json_file:
                        json.dump(controllers, json_file)
                except FileNotFoundError:
                    settings_not_saved_error = True

        if menu:
            run_game = False
            run_settings = False
            run_level_selection = False
            controller_not_configured_counter = 0
            if game_paused:
                paused = True
                run_menu = False
            else:
                paused = False
                run_menu = True

            if settings_counters['speedrun'] == 1:
                speedrun_mode = False
            else:
                speedrun_mode = True

            if settings_counters['music_volume'] > 1:
                play_background_music = True
                if not game_paused:
                    play_music = False
            if settings_counters['music_volume'] == 1:
                play_background_music = False
                play_music = False

            if settings_counters['sounds'] == 1:
                play_sounds = False
            else:
                play_sounds = True

            if settings_counters['hitbox'] == 1:
                draw_hitbox = False
            else:
                draw_hitbox = True

            try:
                with open('data/settings_configuration.json', 'w') as json_file:
                    json.dump(settings_counters, json_file)
            except FileNotFoundError:
                settings_not_saved_error = True

            controls = {
                'left': controls_nums[f"left{settings_counters['walking']}"],
                'right': controls_nums[f"right{settings_counters['walking']}"],
                'jump': controls_nums[f"jump{settings_counters['jumping']}"],
                'configuration': controls['configuration'],
                'cards': controls_nums[f"cards{settings_counters['cards']}"],
            }

    # displaying fps ---------------------------------------------------------------------------------------------------
    fps_display.draw_fps(fps_int, screen)

    # game event handling ----------------------------------------------------------------------------------------------
    if events['quit']:
        run = False
    if events['keydown']:
        event = events['keydown']
        if event.key == pygame.K_q:
            user_quit1 = True
        if event.key == pygame.K_LCTRL:
            user_quit2 = True
        if event.key == pygame.K_j or event.key == pygame.K_l:
            joystick_over_card = True

    if events['keyup']:
        event = events['keyup']
        if event.key == pygame.K_q:
            user_quit1 = False
        if event.key == pygame.K_LCTRL:
            user_quit2 = False
        # play = True
    if events['videoresize'] and not adjust_resolution:
        window_geometry = (window.get_width(), window.get_height())
        if window_geometry[0] / 16 > window_geometry[1] / 9:
            height_window_space = window_geometry[1]
            width_window_space = window_geometry[0]
            wiheight = window_geometry[1]
            wiwidth = wiheight / 9 * 16
        else:
            height_window_space = window_geometry[1]
            width_window_space = window_geometry[0]
            wiwidth = window_geometry[0]
            wiheight = wiwidth / 16 * 9
        if height_window_space == monitor_height and width_window_space == monitor_width:
            settings_counters['resolution'] = 4
            settings_menu.update_settings_counters(settings_counters, controls)
            try:
                with open('data/settings_configuration.json', 'w') as json_file:
                    json.dump(settings_counters, json_file)
            except FileNotFoundError:
                settings_not_saved_error = True

    if events['joydeviceadded']:
        event = events['joydeviceadded']
        pygame.mouse.set_visible(False)
        joystick = pygame.joystick.Joystick(event.device_index)
        joysticks[0] = joystick
        joystick_connected = True
        joystick_name = str(joystick.get_name())
        if joystick_name in controllers:
            controller_connected_counter = 90
            joystick_configured = True
            controller_popup = controller_connected_popup
        else:
            controller_connected_counter = 90
            settings_counters['configuration'] = 1
            settings_menu.update_settings_counters(settings_counters, controls)
            joystick_configured = False
            controller_popup = controller_connected_popup
            controller_calibration = True

        try:
            if joystick.get_name() not in controllers:
                if run_game:
                    controllers[joystick_name] = [4, 5, 10, 1]
                    joystick_configured = False
                else:
                    controllers[joystick_name] = []

            if joystick_name in controllers:
                settings_counters['configuration'] = controllers[joystick_name][3]
                controls['configuration'] = controllers[joystick_name]
                joystick_configured = True
                settings_menu.update_settings_counters(settings_counters, controls)
        except Exception:
            joystick_connection_error = True

    if events['joydeviceremoved'] and game_duration_counter > 20:
        controller_disconnected_counter = 90
        joysticks = {}
        if not joystick_configured:
            del controllers[joystick_name]
        joystick_connected = False
        joystick_name = ''
        joystick_configured = False
        pygame.mouse.set_visible(True)

    if events['joyaxismotion_x']:
        event = events['joyaxismotion_x']
        if joystick_idle and abs(event.value) > 0.3:
            joystick_moved = True
            joystick_idle = False
        if event.value == 0:
            joystick_idle = True
    if events['joyaxismotion_y']:
        event = events['joyaxismotion_y']
        if joystick_idle and abs(event.value) > 0.3:
            joystick_moved = True
            joystick_idle = False
        if event.value == 0:
            joystick_idle = True

    if events['joybuttondown'] and not controller_calibration:
        event = events['joybuttondown']
        if event.button == controls['configuration'][1] or event.button == controls['configuration'][2]:
            joystick_over_card = True
        # game pause
        if event.button == controls['configuration'][3] and run_game:
            run_menu = False
            run_game = False
            paused = True
            run_level_selection = False
            pygame.mixer.music.set_volume(paused_music_volume)
            pause_menu.joystick_counter = 0

    if user_quit1 and user_quit2:
        run = False

    # PLAYING SOUNDS ---------------------------------------------------------------------------------------------------
    if play_sounds:
        if (sound_triggers['card'] and one_time_play_card_pull)\
                or (joystick_over_card and run_game):
            sounds['card_pull'].play()
            one_time_play_card_pull = False
        if not sound_triggers['card']:
            one_time_play_card_pull = True

        if button_sound_trigger3 and one_time_play_button2:
            sounds['button_click'].play()
            one_time_play_button2 = False
        if not button_sound_trigger3:
            one_time_play_button2 = True

        if not sound_triggers['lock']:
            one_time_play_lock = True
        if card_swoosh_chest:
            card_swoosh_counter += 1 * fps_adjust
            if card_swoosh_counter >= 20:
                sounds['card_pull'].play()
                card_swoosh_chest = False
                card_swoosh_counter = 0

        if sound_triggers['step_grass']:
            sounds[f'step_grass{random.choice([1, 2, 2, 2])}'].play()

        if sound_triggers['step_rock']:
            sounds[f'step_rock{random.choice([1, 2, 2])}'].play()

        if sound_triggers['step_wood']:
            sounds['step_wood'].play()

        if sound_triggers['land']:
            sounds['landing'].play()

        if sound_triggers['death']:
            sounds['death'].play()

        if sound_triggers['trap']:
            sounds['bear_trap_cling'].play()

        if sound_triggers['jump']:
            sounds['jump'].play()
            if joysticks:
                joysticks[0].rumble(0.1, 0.2, 10)

        if sound_triggers['mid_air_jump']:
            sounds['mid_air_jump'].play()

        if sound_triggers['sack_noise']:
            sounds['sack_noise'].play()

        if sound_triggers['mushroom']:
            sounds['mushroom'].play()

        if sound_triggers['gem']:
            sounds['gem'].play()

        if sound_triggers['wheat'] == 1:
            pygame.mixer.Channel(1).set_volume(0.6)
            pygame.mixer.Channel(1).play(sounds['wheat'], -1)
        if sound_triggers['wheat'] == -1:
            pygame.mixer.Channel(1).fadeout(400)

        if sound_triggers['click']:
            sounds['click'].play()

    # lock sound
    if sound_triggers['lock']:
        sounds['lock'].play()
    if sound_triggers['swoosh']:
        sounds['jump'].play()
    # button sounds
    if (sound_triggers['button'] and one_time_play_button1)\
            or (joystick_moved and (run_menu or run_settings or run_level_selection or paused)):
        sounds['button_click'].play()
        one_time_play_button1 = False
    if not sound_triggers['button']:
        one_time_play_button1 = True

    # music
    if load_music:
        if speedrun_mode:
            pygame.mixer.music.load('data/sounds/Speedrun-song.wav')
        else:
            song = music[f'{world_count}']
            pygame.mixer.music.load(f'data/sounds/{song}.wav')

    if play_background_music:
        if not world_completed_sound_played:
            if world_ending_levels[world_count] == level_count and run_game and not speedrun_mode:
                sounds['world_completed'].play()
                world_completed_sound_played = True

        if play_music:
            if speedrun_mode:
                pygame.mixer.music.set_volume(speedrun_volume)
                if paused:
                    pygame.mixer.music.set_volume(paused_music_volume)
            pygame.mixer.music.play(-1, 0.0, 300)
            play_music = False

    if fadeout_music:
        pygame.mixer.music.fadeout(300)
        fadeout_music = False

    # custom mouse cursor ----------------------------------------------------------------------------------------------
    if not run_game:
        show_cursor = True
    else:
        show_cursor = False

    if pygame.mouse.get_focused() and not joystick_configured:
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos == last_mouse_pos and not show_cursor and not run_level_selection and not paused:
            mouse_still_count += 1
        else:
            last_mouse_pos = mouse_pos
            mouse_still_count = 0

        if not mouse_still_count >= 70:
            pygame.mouse.set_visible(True)
            mouse_vis = True
        else:
            pygame.mouse.set_visible(False)
            mouse_vis = False

    # updating the display ---------------------------------------------------------------------------------------------
    if run_game:
        main_screen.fill(background_sky_colour)
    else:
        main_screen.fill((0, 0, 0))
    if run_game:
        menu_transition_counter -= (sheight / 23) * fps_adjust
        game_counter += 0.04 * fps_adjust
        screen_alpha += 4 * fps_adjust
        if screen_alpha <= 255:
            screen.set_alpha(screen_alpha)
        scaling = game_counter * game_counter + 1
        if game_counter < -2:
            run_level_selection = False
            main_screen.blit(level_selection_screen, (0, menu_transition_counter))
        elif game_counter < 0:
            output = pygame.transform.scale(screen, (swidth * scaling, sheight * scaling))
            main_screen.blit(output, (swidth / 2 - swidth * scaling / 2, 0))
        else:
            main_screen = screen.copy()

    elif paused:
        main_screen = pause_screen.copy()

    elif run_level_selection:
        main_screen = level_selection_screen.copy()

    elif run_settings:
        main_screen = settings_screen.copy()

    else:
        main_screen = menu_screen.copy()

    # controller errors and messages -----------------------------------------------------------------------------------

    # controller connected message
    if controller_connected_counter > -10 and game_duration_counter > 20:
        cont_connect_y = 10
        if controller_connected_counter < 5:
            cont_connect_y = controller_connected_counter * 2
        main_screen.blit(controller_popup,
                         (swidth / 2 - controller_popup.get_width() / 2, cont_connect_y))
    # controller disconnected message
    if controller_disconnected_counter > -10 and game_duration_counter > 20:
        cont_connect_y = 10
        if controller_disconnected_counter < 5:
            cont_connect_y = controller_disconnected_counter * 2
        main_screen.blit(controller_disconnected_popup,
                         (swidth / 2 - controller_disconnected_popup.get_width() / 2, cont_connect_y))

    # controller calibration
    if controller_calibration and calibration_start_counter > 60 and joystick_connected:
        configuration, done, calibrated = settings_menu.controller_calibration_func(main_screen, events, fps_adjust,
                                                                                    False, joysticks)
        if done:
            controllers[joystick_name] = configuration
            controls['configuration'] = configuration
            joystick_configured = True
            controller_calibration = False
            try:
                with open('data/controllers.json', 'w') as json_file:
                    json.dump(controllers, json_file)
            except Exception:
                settings_not_saved_error = True

    # DISPLAYING EVERYTHING ON THE MAIN WINDOW
    window.fill((0, 0, 0))
    window.blit(pygame.transform.scale(main_screen, (wiwidth, wiheight)),
                (width_window_space / 2 - wiwidth / 2, height_window_space / 2 - wiheight / 2))
    pygame.display.update()

pygame.quit()
# ======================================================================================================================
