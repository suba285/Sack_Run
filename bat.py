import math
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

    def update_bat(self, sack_pos, fps_adjust, screen, camera_move_x, camera_move_y):
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
        current_radius = math.sqrt((sack_pos.x - self.x) ** 2 + (sack_pos.y - self.y) ** 2)

        # sack follow
        angle = 0
        angle = math.atan2(sack_pos.y - self.y, sack_pos.x - self.x)
        dx = math.cos(angle) * ((current_radius - self.halt_radius) / 20) * fps_adjust
        dy = math.sin(angle) * ((current_radius - self.halt_radius) / 20) * fps_adjust

        # updating bat position
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

        # drawing the bat onto the screen
        screen.blit(bat_img, (self.x - 18, self.y - 11))


