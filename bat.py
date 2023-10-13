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
        self.silhouette_right = pygame.mask.Mask.to_surface(pygame.mask.from_surface(self.bat_dash_img_right),
                                                            setcolor=(255, 255, 255), unsetcolor=(0, 0, 0)).convert()
        self.silhouette_right.set_colorkey((0, 0, 0))
        self.bat_dash_img_left = pygame.transform.flip(self.bat_dash_img_right, True, False)
        self.silhouette_left = pygame.transform.flip(self.silhouette_right, True, False)
        self.trace_silh = []

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
        self.dash_speed = 5
        self.flash_duration = 2

        self.silhouette_counter = 0

        self.charge_default_flash_count = 2  # length of bat flash when it's charging the sack
        self.charge_flash_count = self.charge_default_flash_count
        self.charge_flash_on = False

    def update_bat_laser(self, sack_rect, fps_adjust, screen, camera_move_x, camera_move_y, moved, dead):
        harm = False

        dx = 0
        dy = 0

        # checking if the bat is far away enough from the sack
        current_radius = math.sqrt((sack_rect.x - self.x) ** 2 + (sack_rect.y - self.y) ** 2)

        # sack follow
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
        if 180 > self.laser_counter > 100:
            aim = True
            if self.laser_counter > 155:
                flash = True
        if self.laser_counter >= 180 and not dead:
            shoot = True
            colour = (255, 255, 255)
            girth = 2
        if self.laser_counter >= 186:
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

    def update_bat_charge(self, sack_rect, fps_adjust, screen, camera_move_x, camera_move_y, moved, dead,
                          draw_hitbox):
        harm = False

        dx = 0
        dy = 0

        set_silhouette = False

        self.dash -= 1 * fps_adjust
        self.silhouette_counter -= 1 * fps_adjust

        # checking if the bat is far away enough from the sack
        current_radius = math.sqrt((sack_rect.x - self.x) ** 2 + (sack_rect.y - self.y) ** 2)

        # sack follow
        angle = 0
        angle = math.atan2(sack_rect.y - self.y, sack_rect.x - self.x)
        dx = math.cos(angle) * ((current_radius - self.halt_radius) / 20) * fps_adjust
        dy = math.sin(angle) * ((current_radius - self.halt_radius) / 20) * fps_adjust

        sack_y = sack_rect.y + 10

        if not (sack_y - 1 < self.y < sack_y + 1) and self.dash < 0 and moved:
            if self.y > sack_y:
                dy -= 1 * fps_adjust
            if self.y < sack_y:
                dy += 1 * fps_adjust
        if sack_y - 2 < self.y < sack_y + 2 and moved and self.dash < - 40 and not dead:
            self.dash = 55
            if sack_rect.x > self.x:
                self.dash_direction = 1
            else:
                self.dash_direction = -1

        # updating bat position
        if self.dash > 0:
            if self.dash < 50:
                self.x += self.dash_speed * self.dash_direction * fps_adjust + camera_move_x
            else:
                self.x += camera_move_x
            self.y += camera_move_y

        else:
            self.x += dx + camera_move_x
            self.y += dy + camera_move_y

        if self.dash > 0:
            self.charge_flash_count -= 1 * fps_adjust
            if self.charge_flash_count < 0:
                if 30 < self.dash < 50:
                    self.charge_flash_on = not self.charge_flash_on
                self.charge_flash_count = self.charge_default_flash_count
                if self.silhouette_counter < 0:
                    set_silhouette = True
                    self.silhouette_counter = 2
            if self.dash <= 30:
                self.charge_flash_on = True

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
                if self.charge_flash_on:
                    bat_img = self.silhouette_left
                else:
                    bat_img = self.bat_dash_img_left
            else:
                if self.charge_flash_on:
                    bat_img = self.silhouette_right
                else:
                    bat_img = self.bat_dash_img_right

        # trace of bat silhouettes
        if set_silhouette:
            pos = [self.x, self.y]
            alpha = 150
            if self.dash_direction == -1:
                img = self.silhouette_left.copy()
            else:
                img = self.silhouette_right.copy()
            img.set_alpha(alpha)
            package = [img, pos, alpha]
            self.trace_silh.append(package)

        # harm
        if sack_rect.colliderect(self.x - 5, self.y - 4, 10, 8):
            harm = True

        # drawing the bat onto the screen
        removal = []
        for silh in self.trace_silh:
            silh[1][0] += camera_move_x
            silh[1][1] += camera_move_y
            silh[2] -= 17
            if silh[2] <= 0:
                removal.append(silh)
            else:
                screen.blit(silh[0], (silh[1][0] - 18, silh[1][1] - 11))
                silh[0].set_alpha(silh[2])
        for trash in removal:
            self.trace_silh.remove(trash)
        # the actual bit
        screen.blit(bat_img, (self.x - 18, self.y - 11))
        if draw_hitbox:
            pygame.draw.rect(screen, (255, 240, 0), (self.x - 5, self.y - 4, 10, 8), 1)

        if 50 > self.dash > 30:
            screen_shake = True
        else:
            screen_shake = False

        return harm, screen_shake

