import time
import pygame

from world import World
from levels import *
from game import Game
from menu import mainMenu
from display_fps import display_frames_per_second
from font_manager import Text
from pause_screen import PauseScreen
from world_selection import LevelSelection
from game import level_dictionary, level_bg_dictionary

pygame.init()
pygame.mixer.pre_init(40000, -16, 1, 1024)

# basic game variables -------------------------------------------------------------------------------------------------
swidth = 360
sheight = 264
wiwidth = 900
wiheight = 660
wiwidth_big = 1260
wiheight_big = 924
tile_size = 32

x = 180
y = 132

start_x = 0
start_y = -3

clock = pygame.time.Clock()
fps = 60

window = pygame.display.set_mode((wiwidth, wiheight), pygame.SCALED)
screen = pygame.Surface((swidth, sheight), pygame.SCALED)
main_screen = pygame.Surface((swidth, sheight), pygame.SCALED)
menu_screen = pygame.Surface((swidth, sheight), pygame.SCALED)
pause_screen = pygame.Surface((swidth, sheight), pygame.SCALED)
level_selection_screen = pygame.Surface((swidth, sheight), pygame.SCALED)

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])

pygame.display.set_caption('sack run')

world_data = level1_1
bg_data = level1_1_bg
first_level = 1
world_count = 1
level_count = first_level

resolution = "small"

default_game_counter = -3
game_counter = default_game_counter

slow_computer = False
run = True
run_game = False
run_menu = True
play_press = False
play = False
run_level_selection = False
level_selection = False
draw_hitbox = False
last_mouse_pos = pygame.mouse.get_pos()
mouse_still_count = 0
play_music = False
play_music_trigger = False
fadeout_music = False

circle = False

dead = False

paused = False

menu_transition_counter = 0
menu_transition = False

menu_y = 0
game_y = swidth

background_raw = pygame.image.load('data/images/menu_background.png').convert()
background = pygame.transform.scale(background_raw, (360, 296))

# sounds ---------------------------------------------------------------------------------------------------------------
sounds = {
        'card_shuffle': pygame.mixer.Sound('data/sounds/card_shuffle.wav'),
        'card_pull': pygame.mixer.Sound('data/sounds/card_pull_short2.wav'),
        'lock_click': pygame.mixer.Sound('data/sounds/lock_click.wav'),
        'bear_trap_cling': pygame.mixer.Sound('data/sounds/bear_trap_cling.wav'),
        'healing_sound': pygame.mixer.Sound('data/sounds/healing_sound2.wav'),
        'button_click': pygame.mixer.Sound('data/sounds/button_click.wav'),
        'paper_crumbling': pygame.mixer.Sound('data/sounds/paper_crumbling.wav')
    }

sounds['card_pull'].set_volume(0.4)
sounds['lock_click'].set_volume(1.4)
sounds['bear_trap_cling'].set_volume(0.6)
sounds['button_click'].set_volume(0.9)
sounds['paper_crumbling'].set_volume(0.8)

one_time_play_card_pull = True
one_time_play_button1 = True
one_time_play_button2 = True
one_time_play_lock = True
card_swoosh_chest = False
card_swoosh_counter = 0

# custom cursor setup --------------------------------------------------------------------------------------------------
pygame.mouse.set_visible(False)
cursor_raw = pygame.image.load('data/images/cursor_classic2.PNG').convert()
pointer_raw = pygame.image.load('data/images/cursor_classic2_point.PNG').convert()
pointer = pygame.transform.scale(pointer_raw, (tile_size/4, tile_size/4))
pointer.set_colorkey((0, 0, 0))
cursor = pygame.transform.scale(cursor_raw, (tile_size/4, tile_size/4))
cursor.set_colorkey((0, 0, 0))
cursor_list = []

mouse_vis = True

# level file reading (not used currently, a different system is in use) ------------------------------------------------
file = open('level_count', 'r')
str_level_count = file.read()
# level_count = int(str_level_count)

# initiating classes ---------------------------------------------------------------------------------------------------
world = World(world_data, screen, slow_computer, start_x, start_y, bg_data)
main_game = Game(x, y, slow_computer, screen, world_data, bg_data)
main_menu = mainMenu(screen)
pause_menu = PauseScreen(pause_screen)
level_select = LevelSelection(world_count)

paused_text = Text()

# loading number images ------------------------------------------------------------------------------------------------
display_numbers = []

for num in range(10):
    number_raw = pygame.image.load(f"data/images/numbers/number_{num}.PNG").convert()
    number_raw.set_colorkey((255, 255, 255))
    number = pygame.transform.scale(number_raw, (tile_size/4, tile_size/4))
    display_numbers.append(number)

# text -----------------------------------------------------------------------------------------------------------------
paused_txt = paused_text.make_text(['paused'])

# fps variables --------------------------------------------------------------------------------------------------------
last_time = time.time()
last_fps = 1
last_fps_adjust = 1

# MAIN LOOP ============================================================================================================
while run:

    events = pygame.event.get()

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    screen.blit(background, (0, 0))

    play_card_pull_sound = False
    play_lock_sound = False
    play_bear_trap_cling_sound = False
    play_healing_sound = False
    play_button_sound = False
    play_paper_sound = False
    button_sound_trigger1 = False
    button_sound_trigger2 = False
    button_sound_trigger3 = False

    mouse_adjustment = wiwidth / swidth

    cursor_list = []

    # fps adjustment ---------------------------------------------------------------------------------------------------
    real_fps = clock.get_fps()
    fps_adjust = time.time() - last_time
    fps_adjust = fps_adjust * 60
    if fps_adjust > last_fps_adjust + 0.2:
        fps_adjust = last_fps_adjust + 0.2
    if fps_adjust < last_fps_adjust - 0.2:
        fps_adjust = last_fps_adjust - 0.2
    last_time = time.time()
    last_fps_adjust = fps_adjust
    display_fps = round(real_fps)

    clock.tick(fps)

    # running the menu -------------------------------------------------------------------------------------------------
    if run_menu:
        run_game = False
        level_selection, slow_computer, resolution, res, button_sound_trigger1,\
            button_sound_trigger3 = main_menu.menu(menu_screen, slow_computer, mouse_adjustment, events)
        if res:
            if resolution == "small":
                wiwidth = 900
                wiheight = 660
                window = pygame.display.set_mode((wiwidth, wiheight), pygame.SCALED)
            if resolution == "big":
                wiwidth = 1260
                wiheight = 924
                window = pygame.display.set_mode((wiwidth, wiheight), pygame.SCALED)
        if level_selection:
            game_counter = default_game_counter
            run_game = False
            run_menu = False
            run_level_selection = True
            level_count = first_level
            menu_y = 0
            game_y = swidth

    # running the game -------------------------------------------------------------------------------------------------
    if run_game:
        if play:
            if real_fps < 30:
                slow_computer = True
            main_game = Game(x, y, slow_computer, screen, world_data, bg_data)
            play = False

        run_menu = False
        level_count,\
            menu_press,\
            play_card_pull_sound,\
            play_lock_sound,\
            play_bear_trap_cling_sound,\
            play_healing_sound,\
            world_data,\
            dead,\
            bg_data,\
            button_sound_trigger2,\
            play_paper_sound,\
            play_music_trigger,\
            fadeout_music = main_game.game(screen, level_count, slow_computer, fps_adjust,
                                           draw_hitbox, mouse_adjustment, events, world_data, bg_data,
                                           game_counter, world_count)

        if play_music_trigger:
            play_music = True

        if menu_press:
            run_menu = False
            run_game = False
            paused = True
            run_level_selection = False
            fadeout_music = True

    # pause ------------------------------------------------------------------------------------------------------------
    if paused:
        pause_screen,\
            button_sound_trigger1,\
            resume,\
            menu = pause_menu.draw_pause_screen(mouse_adjustment, events)

        if menu:
            run_menu = True
            run_game = False
            paused = False
            run_level_selection = False

        if resume:
            run_menu = False
            run_game = True
            paused = False
            run_level_selection = False
            play_music = True

    # world selection --------------------------------------------------------------------------------------------------
    if run_level_selection:
        play,\
            menu,\
            button_sound_trigger1,\
            world_count = level_select.draw_level_selection(level_selection_screen, mouse_adjustment, events)

        if play:
            run_menu = False
            run_game = True
            paused = False
            level_count = 1
            world_data = level_dictionary[f'level1_{world_count}']
            bg_data = level_bg_dictionary[f'level1_{world_count}_bg']
            world = World(world_data, screen, slow_computer, start_x, start_y, bg_data)
            run_level_selection = False
            menu_transition = True
            menu_transition_counter = 0

        if menu:
            run_menu = True
            run_game = False
            paused = False
            run_level_selection = False

    if slow_computer:
        fps = 30
    else:
        fps = 60

    # playing sounds ---------------------------------------------------------------------------------------------------
    if play_card_pull_sound and one_time_play_card_pull:
        sounds['card_pull'].play()
        one_time_play_card_pull = False
    if not play_card_pull_sound:
        one_time_play_card_pull = True

    if button_sound_trigger1 or button_sound_trigger2:
        play_button_sound = True

    if play_button_sound and one_time_play_button1:
        sounds['button_click'].play()
        one_time_play_button1 = False
    if not play_button_sound:
        one_time_play_button1 = True

    if button_sound_trigger3 and one_time_play_button2:
        sounds['button_click'].play()
        one_time_play_button2 = False
    if not button_sound_trigger3:
        one_time_play_button2 = True

    if play_lock_sound and one_time_play_lock:
        sounds['lock_click'].play()
        one_time_play_lock = False
        card_swoosh_chest = True
    if not play_lock_sound:
        one_time_play_lock = True
    if card_swoosh_chest:
        card_swoosh_counter += 1 * fps_adjust
        if card_swoosh_counter >= 20:
            sounds['card_pull'].play()
            card_swoosh_chest = False
            card_swoosh_counter = 0

    if play_bear_trap_cling_sound:
        sounds['bear_trap_cling'].play()

    if play_healing_sound:
        sounds['healing_sound'].play()

    if play_paper_sound:
        sounds['paper_crumbling'].play()

    if play_music:
        pygame.mixer.music.play(-1, 0.0, 300)
        play_music = False

    if fadeout_music:
        pygame.mixer.music.fadeout(300)
        fadeout_music = False

    # displaying fps ---------------------------------------------------------------------------------------------------
    display_frames_per_second(screen, display_fps, display_numbers)

    # game quit handling and respawn -----------------------------------------------------------------------------------
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and dead:
            pass
            # play = True

    # circle experiment ------------------------------------------------------------------------------------------------
    if circle:
        pygame.draw.circle(screen, (255, 255, 255), (100, 100), 50, width=1, draw_top_right=True, draw_top_left=True,
                           draw_bottom_left=True, draw_bottom_right=True)

    # custom mouse cursor ----------------------------------------------------------------------------------------------
    if pygame.mouse.get_focused():
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos == last_mouse_pos and not run_menu and not run_level_selection and not paused:
            mouse_still_count += 1
        else:
            last_mouse_pos = mouse_pos
            mouse_still_count = 0

        if not mouse_still_count >= 70:
            pygame.mouse.set_visible(True)
            mouse_vis = True
            # screen.blit(cursor, (mouse_pos[0]/mouse_adjustment, mouse_pos[1]/mouse_adjustment))
        else:
            pygame.mouse.set_visible(False)
            mouse_vis = False

    # updating the display ---------------------------------------------------------------------------------------------
    if run_game:
        menu_transition_counter -= (sheight / 25) * fps_adjust
        game_counter += 0.04 * fps_adjust
        scaling = game_counter * game_counter + 1
        if game_counter < -2:
            main_screen.blit(level_selection_screen, (0, menu_transition_counter))
        elif game_counter < 0:
            output = pygame.transform.scale(screen, (swidth * scaling, sheight * scaling))
            main_screen.blit(output, (swidth / 2 - swidth * scaling / 2, 0))
        else:
            output = screen
            main_screen.blit(output, (0, 0))

    elif paused:
        main_screen.blit(pause_screen, (0, 0))

    elif run_level_selection:
        main_screen.blit(level_selection_screen, (0, 0))

    else:
        main_screen.blit(menu_screen, (0, 0))

    window.blit(pygame.transform.scale(main_screen, (wiwidth, wiheight)), (0, 0))
    pygame.display.update()

pygame.quit()
# ======================================================================================================================