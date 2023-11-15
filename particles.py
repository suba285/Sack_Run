import pygame._sdl2
from random import randrange

pygame.init()


# add fps adjust


class Particles():
    def __init__(self, particle_num):
        # images -------------------------------------------------------------------------------------------------------
        self.front_particle_raw = pygame.image.load('data/images/light_purple_flake.PNG').convert()
        self.bg_particle_raw = pygame.image.load('data/images/dark_purple_flake.PNG').convert()
        self.front_particle = pygame.transform.scale(self.front_particle_raw, (3, 3))
        self.bg_particle = pygame.transform.scale(self.bg_particle_raw, (5, 5))

        # variables ----------------------------------------------------------------------------------------------------
        self.swidth = 900
        self.sheight = 660
        self.front_x_speed = -0.3
        self.front_y_speed = 0.2
        self.bg_x_speed = -0.3
        self.bg_y_speed = 0.1
        self.front_particle_list = []
        self.bg_particle_list = []

        # setting up particles -----------------------------------------------------------------------------------------
        for part in range(particle_num):
            x = randrange(0, 360)
            y = randrange(0, 264)
            position = [x, y]
            self.front_particle_list.append(position)
        for part in range(particle_num):
            x = randrange(0, 360)
            y = randrange(0, 264)
            position = [x, y]
            self.bg_particle_list.append(position)

# FRONT PARTICLES ======================================================================================================
    def front_particles(self, screen, camera_move_x, camera_move_y, fps_adjust):
        for particle in self.front_particle_list:
            particle[0] += self.front_x_speed * fps_adjust + camera_move_x
            particle[1] += self.front_y_speed * fps_adjust + camera_move_y
            if particle[0] < -100 or particle[1] > 480:
                direction = randrange(0, 2)
                if direction == 1:
                    particle[0] = 480
                    particle[1] = randrange(0, 270)
                elif direction == 0:
                    particle[0] = randrange(0, 480)
                    particle[1] = 0

            screen.blit(self.front_particle, particle)

# BACKGROUND PARTICLES =================================================================================================
    def bg_particles(self, screen, camera_move_x, camera_move_y, fps_adjust):
        for particle in self.bg_particle_list:
            particle[0] += self.bg_x_speed * fps_adjust + camera_move_x
            particle[1] += self.bg_y_speed * fps_adjust + camera_move_y
            if particle[0] < -100 or particle[1] > 480:
                direction = randrange(0, 2)
                if direction == 1:
                    particle[0] = 480
                    particle[1] = randrange(0, 270)
                elif direction == 0:
                    particle[0] = randrange(0, 480)
                    particle[1] = 0

            screen.blit(self.bg_particle, (particle[0], particle[1]))