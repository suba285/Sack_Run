import math
import pygame._sdl2
from screen_info import swidth, sheight
from image_loader import img_loader


class Bat:
    def __init__(self, spawn_pos):
        self.bat_frames = {}
        for frame in range(1, 6):
            self.bat_frames[frame] = img_loader(f'data/images/bat/bat_{frame}.PNG', 36, 22)
        self.frame_counter = 1
        self.frame_duration = 6
        self.max_speed = 2
        self.accel_speed = 1
        self.halt_radius = 100
        self.vel_x = 0
        self.vel_y = 0
        self.x = spawn_pos[0]
        self.y = spawn_pos[1]
        self.laser_counter = 0
        self.set_target_pos = (0, 0, (0, 0))
        self.target_set = False
        self.flash_duration = 2

    def update_bat(self, sack_rect, fps_adjust, screen, camera_move_x, camera_move_y, moved):
        harm = False

        # deceleration
        if self.vel_x > 0:
            self.vel_x -= 0.5 * fps_adjust
            if self.vel_x < 0:
                self.vel_x = 0
        else:
            self.vel_x += 0.5 * fps_adjust
            if self.vel_x > 0:
                self.vel_x = 0
        if self.vel_y > 0:
            self.vel_y -= 1 * fps_adjust
            if self.vel_y < 0:
                self.vel_y = 0
        else:
            self.vel_y += 1 * fps_adjust
            if self.vel_y > 0:
                self.vel_y = 0

        dx = 0
        dy = 0

        # checking if the bat is far away enough from the sack
        current_radius = math.sqrt((sack_rect.x - self.x) ** 2 + (sack_rect.y - self.y) ** 2)

        # sack follow
        angle = 0
        angle = math.atan2(sack_rect.y - self.y, sack_rect.x - self.x)
        dx = math.cos(angle) * ((current_radius - self.halt_radius) / 20) * fps_adjust
        dy = math.sin(angle) * ((current_radius - self.halt_radius) / 20) * fps_adjust

        # laser
        if moved:
            self.laser_counter += 1 * fps_adjust
        aim = False
        shoot = False
        flash = False
        flash_on = True
        colour = (255, 0, 0)
        girth = 1
        if 150 > self.laser_counter > 70:
            aim = True
            if self.laser_counter > 135:
                flash = True
        if self.laser_counter >= 150:
            shoot = True
            colour = (255, 255, 255)
            girth = 2
        if self.laser_counter >= 155:
            self.laser_counter = 0
            self.target_set = False

        if flash or shoot:
            dx = 0
            dy = 0

        # updating bat position
        self.x += dx + camera_move_x
        self.y += dy + camera_move_y

        # drawing laser
        angle = math.atan2(sack_rect.y + 9 - self.y + 2, sack_rect.x + 8 - self.x)
        laser_target = (self.x + math.cos(angle) * swidth, self.y + math.sin(angle) * swidth)

        if flash:
            if not self.target_set:
                line_rect = pygame.Rect(min(self.x, laser_target[0]), min(self.y, laser_target[1]),
                                        abs(laser_target[0] - self.x), abs(laser_target[1] - self.y))
                self.set_target_pos = (laser_target[0] - self.x, laser_target[1] - self.y, laser_target)
                self.target_set = True

        if aim or shoot:
            if flash:
                self.flash_duration -= 1 * fps_adjust
                if self.flash_duration <= 0:
                    flash_on = not flash_on
                    self.flash_duration = 2
            else:
                flash_on = True
            if flash_on and not flash and not shoot:
                pygame.draw.line(screen, colour, (self.x, self.y - 2), laser_target, girth)
            if (shoot or flash) and flash_on:
                pygame.draw.line(screen, colour, (self.x, self.y - 2),
                                 (self.x + self.set_target_pos[0], self.y + self.set_target_pos[1]),
                                 girth)

        # animation frames
        self.frame_duration -= 1 * fps_adjust
        if self.frame_duration < 0:
            self.frame_counter += 1
            self.frame_duration = 6
        if self.frame_counter > 5:
            self.frame_counter = 1
        bat_img = self.bat_frames[self.frame_counter]

        # drawing the bat onto the screen
        screen.blit(bat_img, (self.x - 18, self.y - 11))

        a = (self.set_target_pos[2][1] - self.y + 2) / (self.set_target_pos[2][0] - self.x)
        b = (self.y - 2) - a * self.x
        y = a * (sack_rect.x + 8) + b
        x = (sack_rect.y + 9 - b) / a
        if (y - 12 < sack_rect.y + 9 < y + 12 or x - 12 < sack_rect.x + 8 < x + 12) and shoot:
            harm = True

        return harm


