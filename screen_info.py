import pygame
pygame.init()

screen_dimensions = pygame.display.Info()
global_monitor_width = screen_dimensions.current_w
global_monitor_height = screen_dimensions.current_h
global_screen_width = global_monitor_width
global_screen_height = global_monitor_width / 16 * 9


global_sheight = 270
global_swidth = 480
global_tile_size = 32

if global_monitor_width / 16 <= global_monitor_height / 9:
    fullscreen_scale = round(global_monitor_width / global_swidth)
    print(global_monitor_width / global_swidth)
    print(fullscreen_scale)
    swidth = global_monitor_width / fullscreen_scale
    sheight = swidth / 16 * 9

wiheight = global_sheight
wiwidth = global_swidth
