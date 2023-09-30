import pygame._sdl2
import math

tile_size = 32


class Bee:
    def __init__(self, x, y,):

        # variables ----------------------------------------------------------------------------------------------------
        self.speed = 2
        self.x = x
        self.y = y
        self.angry_counter = 0
        self.direction = 1
        self.captured = False
        self.animation_counter = 0

        self.sack_width = 32
        self.sack_height = 20

        self.stop_counter = 180
        self.blit_bee = True
        self.one_time_adjustment = False
        self.dead = False

        # bee frames ---------------------------------------------------------------------------------------------------
        self.bee0_raw = pygame.image.load('data/images/bee0.PNG').convert()
        self.bee1_raw = pygame.image.load('data/images/bee1.PNG').convert()
        self.bee_dead_raw = pygame.image.load('data/images/bee_dead.PNG').convert()
        self.bee0f = pygame.transform.scale(self.bee0_raw, (tile_size / 2, tile_size / 2))
        self.bee1f = pygame.transform.scale(self.bee1_raw, (tile_size / 2, tile_size / 2))
        self.bee0b = pygame.transform.flip(self.bee0f, True, False)
        self.bee1b = pygame.transform.flip(self.bee1f, True, False)
        self.bee_dead = pygame.transform.scale(self.bee_dead_raw, (tile_size / 2, tile_size / 2))
        self.bee0f.set_colorkey((0, 0, 0))
        self.bee1f.set_colorkey((0, 0, 0))
        self.bee0b.set_colorkey((0, 0, 0))
        self.bee1b.set_colorkey((0, 0, 0))
        self.bee_dead.set_colorkey((0, 0, 0))
        self.bee_rect = self.bee0f.get_rect()
        self.bee_width = self.bee0f.get_width()
        self.bee_height = self.bee0f.get_height()
        self.image = self.bee0f
        self.bee_radius = 0

    def update_bee(self, screen, sack_rect, fps_adjust, camera_move_x, camera_move_y, x, y,
                   health, shockwave_data_list, player_moved):
        dx = 0
        dy = 0

        self.stop_counter += 1

        if not self.one_time_adjustment:
            self.x = x
            self.y = y
            self.one_time_adjustment = True

        harm = False
        self.angry_counter += 1
        self.animation_counter += 1*fps_adjust

        distance = 0

        for shockwave in shockwave_data_list:
            radius = shockwave[2]
            shockwave_x = shockwave[0]
            shockwave_y = shockwave[1]
            self.bee_radius = math.sqrt((shockwave_x - self.x) ** 2 + (shockwave_y - self.y) ** 2)
            if radius > self.bee_radius > radius - 10:
                self.dead = True

        # bee speed, direction, animation and death update -------------------------------------------------------------
        if not self.dead and player_moved:
            if (self.angry_counter > 10 * fps_adjust) and health > 0:
                angle = math.atan2(sack_rect.y - self.y, sack_rect.x - self.x)
                dx = math.cos(angle) * self.speed * fps_adjust
                dy = math.sin(angle) * self.speed * fps_adjust
                if dx >= 0:
                    self.direction = 0
                else:
                    self.direction = 1
                distance = math.sqrt((sack_rect.y - self.y)**2 + (sack_rect.x - self.x)**2)
                if self.x < sack_rect.x:
                    distance *= -1
            if self.animation_counter > 5:
                if self.direction == 1:
                    self.image = self.bee0f
                else:
                    self.image = self.bee0b
                self.animation_counter = 1
            elif self.animation_counter > 3:
                if self.direction == 1:
                    self.image = self.bee1f
                else:
                    self.image = self.bee1b
            else:
                if self.direction == 1:
                    self.image = self.bee0f
                else:
                    self.image = self.bee0b
            if sack_rect.colliderect(self.x, self.y, self.bee_height, self.bee_width):
                harm = True
                self.dead = True

        # bee death handling -------------------------------------------------------------------------------------------
        elif self.dead:
            self.image = self.bee_dead
            dy += 2 * fps_adjust
            if self.y > 360:
                self.y = 360
                dy = 0
                if health > 0:
                    self.dead = False
                    self.angry_counter = 0
                    self.one_time_adjustment = False
                else:
                    self.blit_bee = False

        # updating bee coordinates -------------------------------------------------------------------------------------
        self.x += dx + camera_move_x
        self.y += dy + camera_move_y

        if self.blit_bee:
            screen.blit(self.image, (self.x, self.y))

        return harm, distance



