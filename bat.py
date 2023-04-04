import math
import pygame._sdl2
from screen_info import swidth
from image_loader import img_loader


class Bat:
    def __init__(self, spawn_pos):
        self.bat_frames = {}
        for frame in range(1, 6):
            self.bat_frames[frame] = img_loader(f'data/images/bat/bat_{frame}.PNG', 36, 22)
        self.bat_dash_img_right = img_loader('data/images/bat/bat_dash.PNG', 36, 22)
        self.bat_dash_img_left = pygame.transform.flip(self.bat_dash_img_right, True, False)
        self.outline_surf_right = pygame.Surface((36, 22))
        self.outline_surf_right.set_colorkey((0, 0, 0))
        bat_dash_mask = pygame.mask.from_surface(self.bat_dash_img_right)
        outline = bat_dash_mask.outline()
        for point in outline:
            self.outline_surf_right.set_at(point, (255, 0, 0))
        self.outline_surf_left = pygame.transform.flip(self.outline_surf_right, True, False)
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
        self.dash = 0
        self.dash_direction = 1
        self.flash_duration = 2

    def update_bat_laser(self, sack_rect, fps_adjust, screen, camera_move_x, camera_move_y, moved, dead):
        harm = False

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
            if self.laser_counter > 130:
                flash = True
        if self.laser_counter >= 150 and not dead:
            shoot = True
            colour = (255, 255, 255)
            girth = 2
        if self.laser_counter >= 156:
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

        if (aim or shoot) and not dead:
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
        if (y - 14 < sack_rect.y + 9 < y + 14 or x - 14 < sack_rect.x + 8 < x + 14) and shoot and not dead:
            harm = True

        return harm, shoot

    def update_bat_charge(self, sack_rect, fps_adjust, screen, camera_move_x, camera_move_y, moved, dead):
        harm = False

        dx = 0
        dy = 0
        outline = self.outline_surf_left

        self.dash -= 1 * fps_adjust

        # checking if the bat is far away enough from the sack
        current_radius = math.sqrt((sack_rect.x - self.x) ** 2 + (sack_rect.y - self.y) ** 2)

        # sack follow
        angle = 0
        angle = math.atan2(sack_rect.y - self.y, sack_rect.x - self.x)
        dx = math.cos(angle) * ((current_radius - self.halt_radius) / 20) * fps_adjust
        dy = math.sin(angle) * ((current_radius - self.halt_radius) / 20) * fps_adjust

        if not (sack_rect.y - 3 < self.y < sack_rect.y + 3) and self.dash < 0 and moved:
            if self.y > sack_rect.y:
                dy -= 1 * fps_adjust
            if self.y < sack_rect.y:
                dy += 1 * fps_adjust
        if sack_rect.y - 4 < self.y < sack_rect.y + 4 and moved and self.dash < - 40 and not dead:
            self.dash = 40
            if sack_rect.x > self.x:
                self.dash_direction = 1
            else:
                self.dash_direction = -1

        # updating bat position
        if self.dash > 0:
            if self.dash < 35:
                self.x += 6 * self.dash_direction * fps_adjust + camera_move_x
        else:
            self.x += dx + camera_move_x
            self.y += dy + camera_move_y

        # animation frames
        self.frame_duration -= 1 * fps_adjust
        if self.frame_duration < 0:
            self.frame_counter += 1
            self.frame_duration = 6
        if self.frame_counter > 5:
            self.frame_counter = 1
        bat_img = self.bat_frames[self.frame_counter]
        if self.dash > 0:
            if self.dash_direction == -1:
                bat_img = self.bat_dash_img_left
                outline = self.outline_surf_left
            else:
                bat_img = self.bat_dash_img_right
                outline = self.outline_surf_right

        # harm
        if sack_rect.colliderect(self.x - 5, self.y - 4, 10, 8):
            harm = True

        # drawing the bat onto the screen
        screen.blit(bat_img, (self.x - 18, self.y - 11))

        if self.dash > 20:
            screen_shake = True
        else:
            screen_shake = False

        return harm, screen_shake

