import pygame
from screen_info import global_monitor_height, global_monitor_width

monitor_width = global_monitor_width
monitor_height = global_monitor_height

sheight = 270
swidth = 480

if monitor_width / 16 <= monitor_height / 9:
    fullscreen_scale = round(monitor_width / swidth)
    swidth = round(monitor_width / fullscreen_scale)
    sheight = round(swidth / 16 * 9)


class FpsDisplay:
    def __init__(self):
        self.number_images = {}
        for num in range(0, 10):
            img = pygame.image.load(f'data/font/fps_digits/digit{num}.PNG')
            img.set_colorkey((255, 255, 255))
            self.number_images[str(num)] = pygame.transform.scale(img, (3, 5))

        self.gap = 1
        self.digit_width = 3
        digit_height = 5
        self.fps_y = sheight - 5 - digit_height
        self.fps_x = swidth - (self.gap + self.digit_width * 2 + 5)

    def draw_fps(self, current_fps: int, screen):
        fps_string = str(current_fps)
        x_offset = 0
        for digit in fps_string:
            img = self.number_images[digit]
            screen.blit(img, (self.fps_x + x_offset, self.fps_y))
            x_offset += self.gap + self.digit_width





