import pygame
from screen_info import global_monitor_height, global_monitor_width

tile_size = 32
screen_dimensions = pygame.display.Info()
monitor_width = global_monitor_width
monitor_height = global_monitor_height

sheight = 270
swidth = 480

if monitor_width / 16 <= monitor_height / 9:
    fullscreen_scale = round(monitor_width / swidth)
    swidth = monitor_width / fullscreen_scale
    sheight = swidth / 16 * 9

# handles the shockwave expansion across the screen, creates the shockwave


class Shockwave:
    def __init__(self, screen):
        self.radius = 0
        self.speed = 4
        self.x = 0
        self.y = 0
        self.width = 4
        self.surface = screen
        self.expand = False

        self.blit_bar = True

    def update_shockwave(self, position, fps_adjust, trigger):
        if trigger and not self.expand:
            self.expand = True
            self.x = position[0]
            self.y = position[1]
        if self.expand:
            self.x = position[0]
            self.y = position[1]
            self.speed -= 0.075
            self.radius += self.speed * fps_adjust
            self.width -= 0.08
            width = round(self.width)
            if width > 0:
                pygame.draw.circle(self.surface, (255, 255, 255), (self.x, self.y), self.radius, width)
        if self.radius >= 100:
            self.expand = False
            self.speed = 4
            self.radius = 0
            self.width = 4

        return self.radius
