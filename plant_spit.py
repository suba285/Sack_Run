import pygame
import random

tile_size = 32


class PlantSpit:
    def __init__(self, direction, start_x, start_y):

        # images -------------------------------------------------------------------------------------------------------
        img = pygame.image.load('data/images/spitting_plant_spit.PNG')
        self.image = pygame.transform.scale(img, (tile_size/4, tile_size/4))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        # variables ----------------------------------------------------------------------------------------------------
        self.speed = 3
        self.duration = 300
        self.direction = direction
        self.direction_adjust = -1
        self.direction_niller = 1
        if self.direction == 'right':
            self.direction_adjust_x = 1
            self.direction_adjust_y = 0
            self.direction_niller = 0
        if self.direction == 'left':
            self.direction_adjust_x = -1
            self.direction_adjust_y = 0
            self.direction_niller = 1
        if self.direction == 'up':
            self.direction_adjust_x = 0
            self.direction_adjust_y = -1
            self.direction_niller = 1

        self.hit = False
        self.move = True

        self.dx = 0
        self.dy = 0

        self.one_time_adjustment = False
        self.harm = False
        self.explode = False
        self.explode_counter = 0
        self.load_explosion = True

        self.spit_particles = []
        self.spit_particles_hit = []

        self.rect.x = start_x
        self.rect.y = start_y

# UPDATING SPIT ========================================================================================================
    def update_spit(self, screen, camera_move_x, camera_move_y, start_x, start_y,
                    fps_adjust, sack_rect, health, tile_list):

        self.harm = False

        self.duration -= 1*fps_adjust

        # start pos of the spit ----------------------------------------------------------------------------------------
        if not self.one_time_adjustment:
            if self.direction_adjust_x == 1:
                self.rect.x = start_x + 32
                self.rect.y = start_y
            elif self.direction_adjust_x == 0:
                self.rect.x = start_x + 12
                self.rect.y = start_y
            else:
                self.rect.x = start_x
                self.rect.y = start_y
            self.one_time_adjustment = True

        # spit flying particles ----------------------------------------------------------------------------------------
        self.spit_particles.append([[self.rect.x + 6 - (4*self.direction_niller*self.direction_adjust_x*-1 - 2*self.direction_adjust_y),
                                    self.rect.y + 4], [(random.randint(0, 10) / 10)*self.direction_adjust_x,
                                    (random.randint(0, 10) / 10)*self.direction_adjust_y],
                                    random.randint(1, 4)])

        # moving spit --------------------------------------------------------------------------------------------------
        self.dx = 0
        self.dy = 0
        self.dx = self.speed * fps_adjust * self.direction_adjust_x + camera_move_x
        self.dy = self.speed * fps_adjust * self.direction_adjust_y + camera_move_y
        self.rect.x += self.dx
        self.rect.y += self.dy

        # spit collisions ----------------------------------------------------------------------------------------------
        if self.rect.colliderect(sack_rect) and health > 0 and self.move:
            self.hit = True
            self.explode = True
            self.move = False
            if self.load_explosion:
                # loading spit explosion if player hit
                for i in range(25):
                    self.spit_particles_hit.append([[self.rect.x + 4, self.rect.y + 4],
                                                    [(random.randint(0, 40) / 10) - 2,
                                                    (random.randint(0, 20) / 10) - 1],
                                                    random.randint(2, 3)])
                    self.harm = True
                    self.load_explosion = False
        for tile in tile_list:
            if tile[1].colliderect(self.rect):
                self.explode = True
                self.hit = True
                self.move = False
                if self.load_explosion:
                    for i in range(25):
                        self.spit_particles_hit.append([[self.rect.x + 4, self.rect.y + 4],
                                                        [(random.randint(0, 40) / 10) - 2,
                                                         (random.randint(0, 20) / 10) - 1],
                                                        random.randint(2, 4)])
                    self.load_explosion = False

        # updating and drawing spit particles --------------------------------------------------------------------------
        if not self.hit:
            if not self.rect.colliderect(start_x, start_y, tile_size, tile_size):
                screen.blit(self.image, (self.rect.x, self.rect.y))
            # updating flying spit particles
            for part in self.spit_particles:
                part[0][0] += part[1][0] * fps_adjust + camera_move_x
                part[0][1] += part[1][1] * fps_adjust + camera_move_y
                part[2] -= 0.4
                pygame.draw.circle(screen, (255, 0, 0), [int(part[0][0]), int(part[0][1])], int(part[2]))
                if part[2] <= 0:
                    self.spit_particles.remove(part)

        # resetting spit if it lasted it's time ------------------------------------------------------------------------
        if self.duration <= 0:
            self.duration = 300
            self.one_time_adjustment = False
            self.hit = False
            self.spit_particles = []
            self.load_explosion = True
            self.move = True

        # spit explosion if player or tile hit -------------------------------------------------------------------------
        if self.explode:
            for part in self.spit_particles_hit:
                part[0][0] += part[1][0] * fps_adjust + camera_move_x
                part[0][1] += part[1][1] * fps_adjust + camera_move_y
                part[2] -= 0.15
                pygame.draw.circle(screen, (255, 0, 0), [int(part[0][0]), int(part[0][1])], int(part[2]))
                if part[2] <= 0:
                    self.spit_particles_hit.remove(part)
                if not self.spit_particles_hit:
                    self.explode = False

        return self.harm








