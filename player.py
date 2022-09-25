import pygame
from level_transition import CircleTransition
from shockwave import Shockwave
from image_loader import img_loader
import random

sheight = 264
swidth = 352

pygame.init()
tile_size = 32
player_size_y = 32
player_size_x = 20

jump_offset_amount = 5


# hey particles coming off the player ----------------------------------------------------------------------------------
class HeyParticle:
    def __init__(self, img1, img2, img3, sack_rect):
        self.img1 = img1
        self.img2 = img2
        self.img3 = img3
        self.sack_rect = sack_rect
        self.x1 = sack_rect.x
        self.y1 = sack_rect.y
        self.x2 = sack_rect.x
        self.y2 = sack_rect.y
        self.x3 = sack_rect.x
        self.y3 = sack_rect.y
        self.part_counter1 = 0
        self.part_counter2 = 140
        self.part_counter3 = 250
        pass

    def update_particle(self, sack_rect, fps_adjust, new_level, camera_move_x, camera_move_y):
        # three particles being recycled to create an illusion of infinite particles

        # updating particles' positions
        self.part_counter1 += 1*fps_adjust
        self.part_counter2 += 1*fps_adjust
        self.part_counter3 += 1*fps_adjust
        self.x1 -= 1*fps_adjust - camera_move_x
        self.y1 += 0.2*fps_adjust + camera_move_y
        self.x2 -= 0.8 * fps_adjust - camera_move_x
        self.y2 += 0.3 * fps_adjust + camera_move_y
        self.x3 -= 1.1 * fps_adjust - camera_move_x
        self.y3 += 0.1 * fps_adjust + camera_move_y

        # updating individual particles
        if self.part_counter1 >= 360:
            self.x1 = sack_rect.x
            self.y1 = sack_rect.y
            self.part_counter1 = 0
        if self.part_counter2 >= 360:
            self.x2 = sack_rect.x
            self.y2 = sack_rect.y
            self.part_counter2 = 0
        if self.part_counter3 >= 360:
            self.x3 = sack_rect.x
            self.y3 = sack_rect.y
            self.part_counter3 = 0

        # new level reset
        if new_level:
            self.x1 = 0
            self.y1 = 0
            self.x2 = 0
            self.y2 = 0
            self.x3 = 0
            self.y3 = 0
            self.part_counter1 = 0
            self.part_counter2 = 140
            self.part_counter3 = 250

    def blit_particle(self, screen):
        screen.blit(self.img1, (self.x1, self.y1))
        screen.blit(self.img2, (self.x2, self.y2))
        screen.blit(self.img3, (self.x3, self.y3))


# player death animation (to be redone) --------------------------------------------------------------------------------
def death_animation1(self, fps_adjust):
    self.dead_counter += 1 * fps_adjust
    if self.dead_counter > 36:
        self.sack_img = self.dead6
    elif self.dead_counter > 30:
        self.sack_img = self.dead5
    elif self.dead_counter > 24:
        self.sack_img = self.dead4
    elif self.dead_counter > 18:
        self.sack_img = self.dead3
    elif self.dead_counter > 12:
        self.sack_img = self.dead2
    elif self.dead_counter > 6:
        self.sack_img = self.dead1

    return self.sack_img


# player healing animation - not used at the moment --------------------------------------------------------------------
def heal_animation(screen, fps_adjust, anim_list, dy, sack_rect):
    top_border = random.randrange(sack_rect.y - 10, sack_rect.y)
    for part in anim_list:
        part[2] -= part[0] * fps_adjust
        part[2] += dy/2
        if part[2] < top_border:
            part[2] = sack_rect.y + 40
        pygame.draw.circle(screen, (255, 0, 0), (part[1], part[2]), 1)


# player animation used for teleportation and healing ------------------------------------------------------------------
def magic_animation(self, screen, counter, particle_x):
    blit = True
    img = self.particles1

    if counter > 90:
        img = self.particles2
    elif counter > 80:
        img = self.particles1
    elif counter > 70:
        img = self.particles2
    elif counter > 60:
        img = self.particles3
    elif counter > 50:
        img = self.particles4
    elif counter > 40:
        img = self.particles3
    elif counter > 30:
        img = self.particles1
    elif counter > 20:
        img = self.particles2
    elif counter > 10:
        img = self.particles3
    elif counter > 0:
        img = self.particles1
    else:
        blit = False

    if blit:
        screen.blit(img, (particle_x + 2, self.sack_rect.y))


# particles appearing around the health bar when the player takes damage -----------------------------------------------
def health_bar_particles(screen, fps_adjust, health_bar_part_list,
                         health_position_x, health_position_y, new_particles):
    if new_particles:
        for i in range(15):
            health_bar_part_list.append([[health_position_x, health_position_y],
                                         [(random.randint(0, 20) / 10) - 2, (random.randint(0, 10) / 10)],
                                         random.randint(3, 4)])

    if health_bar_part_list:
        for particle in health_bar_part_list:
            particle[0][0] += particle[1][0] * fps_adjust
            particle[0][1] += particle[1][1] * fps_adjust
            particle[2] -= 0.1
            pygame.draw.circle(screen, (150, 0, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                health_bar_part_list.remove(particle)


# ======================================================================================================================

class Player:
    def __init__(self, x, y, screen, controls, settings_counters):
        # player sprite assets -----------------------------------------------------------------------------------------
        self.sack0f = img_loader('data/images/sack0.PNG', player_size_x, player_size_y)
        self.sack1f = img_loader('data/images/sack1.PNG', player_size_x, player_size_y)
        self.sack2f = img_loader('data/images/sack2.PNG', player_size_x, player_size_y)
        self.sack0b = pygame.transform.flip(self.sack0f, True, False)
        self.sack1b = pygame.transform.flip(self.sack1f, True, False)
        self.sack2b = pygame.transform.flip(self.sack2f, True, False)
        self.sack_blinkf = img_loader('data/images/sack_eyes_closed.PNG', player_size_x, player_size_y)
        self.sack_lookf = img_loader('data/images/sack_side_look.PNG', player_size_x, player_size_y)
        self.sack_jumpf = img_loader('data/images/sack_jumping.PNG', player_size_x, player_size_y)
        self.sack_jumpb = pygame.transform.flip(self.sack_jumpf, True, False)
        self.sack_jump1f = img_loader('data/images/sack_jumping1.PNG', tile_size, tile_size)
        self.sack_jump2f = img_loader('data/images/sack_jumping2.PNG', tile_size, tile_size)
        self.sack_jump3f = img_loader('data/images/sack_jumping3.PNG', tile_size, tile_size)
        self.sack_jump1b = pygame.transform.flip(self.sack_jump1f, True, False)
        self.sack_jump2b = pygame.transform.flip(self.sack_jump2f, True, False)
        self.sack_jump3b = pygame.transform.flip(self.sack_jump3f, True, False)
        self.sack_blinkb = pygame.transform.flip(self.sack_blinkf, True, False)
        self.sack_lookb = pygame.transform.flip(self.sack_lookf, True, False)
        self.sack_img = self.sack0f
        self.sack_rect = self.sack0f.get_rect()
        self.dead_rect = img_loader('data/images/sack0.PNG', 4, player_size_y).get_rect()
        self.sack_rect.x = x
        self.sack_rect.y = y
        self.speed = 4
        self.slide = 0.4
        self.default_on_ground_counter = 6
        self.on_ground_counter = self.default_on_ground_counter
        self.sack_width = self.sack0f.get_width()
        self.sack_height = self.sack0f.get_height()
        self.vel_y = 0
        self.vel_x_l = 0
        self.vel_x_r = 0
        self.vel_x = 0
        self.jumped = False
        self.sack_offset = 0

        self.controls = controls
        self.settings_counters = settings_counters

        # player sprite death animation frames -------------------------------------------------------------------------
        self.dead1 = img_loader('data/images/dead_sack1.PNG', tile_size, tile_size)
        self.dead2 = img_loader('data/images/dead_sack2.PNG', tile_size, tile_size)
        self.dead3 = img_loader('data/images/dead_sack3.PNG', tile_size, tile_size)
        self.dead4 = img_loader('data/images/dead_sack4.PNG', tile_size, tile_size)
        self.dead5 = img_loader('data/images/dead_sack5.PNG', tile_size, tile_size)
        self.dead6 = img_loader('data/images/dead_sack6.PNG', tile_size, tile_size)

        # teleportation particles frames -------------------------------------------------------------------------------
        self.particles1 = img_loader('data/images/particles1.PNG', tile_size, tile_size)
        self.particles2 = img_loader('data/images/particles2.PNG', tile_size, tile_size)
        self.particles3 = img_loader('data/images/particles3.PNG', tile_size, tile_size)
        self.particles4 = img_loader('data/images/particles4.PNG', tile_size, tile_size)

        # health bar images and related --------------------------------------------------------------------------------
        self.bar_full_health = img_loader('data/images/bar_full_health.PNG', tile_size * 2, tile_size / 2)
        self.bar_half_health = img_loader('data/images/bar_half_health.PNG', tile_size * 2, tile_size / 2)
        self.bar_no_health = img_loader('data/images/bar_no_health.PNG', tile_size * 2, tile_size / 2)
        self.health_bar_info = img_loader('data/images/health_bar_info.PNG', tile_size * 2, tile_size)
        self.health_bar = self.bar_full_health
        self.health_bar_rect = self.bar_full_health.get_rect()
        self.health_bar_card = img_loader('data/images/health_bar_card.PNG', tile_size * 2, tile_size * 2)

        self.health_bar_rect.x = 0
        self.health_bar_rect.y = 0
        self.health_info = False
        self.health_info_move = 0

        # card powers indicator images ---------------------------------------------------------------------------------
        self.jump_boost_indicator = img_loader('data/images/icon_jump_boost.PNG', tile_size, tile_size)
        self.no_gravity_indicator = img_loader('data/images/icon_no_gravity.PNG', tile_size, tile_size)
        self.no_harm_indicator = img_loader('data/images/icon_no_harm.PNG', tile_size, tile_size)

        self.jump_boost_surf = pygame.Surface((tile_size, tile_size))
        self.no_harm_surf = pygame.Surface((tile_size, tile_size))
        self.no_gravity_surf = pygame.Surface((tile_size, tile_size))

        self.progress_bar = pygame.Surface((tile_size, 18))
        self.progress_bar.set_alpha(128)
        self.progress_bar.fill((0, 0, 0))

        # respawn instruction images -----------------------------------------------------------------------------------
        self.respawn_instr1 = img_loader('data/images/respawn_instructions1.PNG', tile_size * 2, tile_size)
        self.respawn_instr2 = img_loader('data/images/respawn_instructions2.PNG', tile_size * 2, tile_size)
        self.respawn_instructions_blit_counter = 0
        self.respawn_instructions_blit_counter = 0

        # extra card powers and their counters -------------------------------------------------------------------------
        self.jump_boost = False
        self.jump_boost_counter = 0
        self.jump_boost_duration = 450
        self.regeneration = False
        self.regeneration_counter = 0
        self.no_gravity = False
        self.no_gravity_counter = 0
        self.no_gravity_duration = 180
        self.no_harm = False
        self.no_harm_counter = 0
        self.no_harm_duration = 300

        # other player variables ---------------------------------------------------------------------------------------
        self.walk_counter = 0
        self.blink_counter = 0
        self.direction = 1
        self.animate_walk = True
        self.new_level = False
        self.new_level_cooldown = 70
        self.teleport_count = 0
        self.health = 2
        self.harmed = False
        self.dead = False
        self.transition = False
        self.dead_counter = 0
        self.airborn = False
        self.break_transition = False
        self.transition_get_smaller = True
        self.lowest_tile = 0
        self.highest_tile = 264
        self.speed = 0
        self.speed_adder = 0
        self.player_moved = False
        self.blit_plr = True
        self.harm_counter = 40
        self.harm_flash_counter = 0
        self.init_flash = False
        self.first_power_jump = False

        # music and sounds ---------------------------------------------------------------------------------------------
        self.first_level_play_music = True
        self.play_music = False
        self.single_play = True
        self.fadeout = False
        self.single_fadeout = True

        # collisions ---------------------------------------------------------------------------------------------------
        self.top_col = False
        self.btm_col = False
        self.right_col = False
        self.left_col = False
        self.col_types = {'left': False, 'right': False, 'top': False, 'bottom': False}

        # --------------------------------------------------------------------------------------------------------------
        self.camera_movement_x = 0
        self.camera_movement_y = 0

        # --------------------------------------------------------------------------------------------------------------
        self.health_bar_part_list = []
        self.new_health_particles = False
        self.health_part_x = 0
        self.health_part_y = 14
        self.power_indicator_list = []

        self.hands_on_keyboard_counter = 0
        self.hands_on_keyboard_surf = pygame.Surface((tile_size * 2, tile_size * 1.5))
        self.hands_on_keyboard_surf.set_colorkey((0, 0, 0))

        self.draw_hands_on_keyboard = False

        # power particle variables -------------------------------------------------------------------------------------
        self.power_particle_surface = pygame.Surface((swidth, sheight))
        self.power_particle_surface.set_alpha(170)
        self.power_particle_list = []
        self.power_particle_counter = 0
        self.particle_colour = (255, 255, 255)

        # map borders --------------------------------------------------------------------------------------------------
        self.right_border = 0
        self.left_border = 0

        # player movement per frame ------------------------------------------------------------------------------------
        self.dx = 0
        self.dy = 0

        # level restart variables --------------------------------------------------------------------------------------
        self.restart_level = False
        self.restart_trigger = False
        self.restart_counter = 0
        self.single_restart = True

        # control instructions images ----------------------------------------------------------------------------------
        self.key_left = img_loader('data/images/key_left.PNG', tile_size / 2, tile_size / 2)
        self.key_left_press = img_loader('data/images/key_left_press.PNG', tile_size / 2, tile_size / 2)
        self.key_right = img_loader('data/images/key_right.PNG', tile_size / 2, tile_size / 2)
        self.key_right_press = img_loader('data/images/key_right_press.PNG', tile_size / 2, tile_size / 2)
        self.key_x = img_loader('data/images/key_x.PNG', tile_size / 2, tile_size / 2)
        self.key_x_press = img_loader('data/images/key_x_press.PNG', tile_size / 2, tile_size / 2)
        self.key_z = img_loader('data/images/key_z.PNG', tile_size / 2, tile_size / 2)
        self.key_z_press = img_loader('data/images/key_z_press.PNG', tile_size / 2, tile_size / 2)
        self.key_space = img_loader('data/images/key_space.PNG', tile_size, tile_size / 2)
        self.key_space_press = img_loader('data/images/key_space_press.PNG', tile_size, tile_size / 2)
        self.key_a = img_loader('data/images/key_a.PNG', tile_size / 2, tile_size / 2)
        self.key_a_press = img_loader('data/images/key_a_press.PNG', tile_size / 2, tile_size / 2)
        self.key_d = img_loader('data/images/key_d.PNG', tile_size / 2, tile_size / 2)
        self.key_d_press = img_loader('data/images/key_d_press.PNG', tile_size / 2, tile_size / 2)
        self.key_e = img_loader('data/images/key_e.PNG', tile_size / 2, tile_size / 2)
        self.key_e_press = img_loader('data/images/key_e_press.PNG', tile_size / 2, tile_size / 2)
        self.key_slash = img_loader('data/images/key_slash.PNG', tile_size / 2, tile_size / 2)
        self.key_slash_press = img_loader('data/images/key_slash_press.PNG', tile_size / 2, tile_size / 2)
        self.key_w = img_loader('data/images/key_w.PNG', tile_size / 2, tile_size / 2)
        self.key_w_press = img_loader('data/images/key_w_press.PNG', tile_size / 2, tile_size / 2)
        self.key_up = img_loader('data/images/key_up.PNG', tile_size / 2, tile_size / 2)
        self.key_up_press = img_loader('data/images/key_up_press.PNG', tile_size / 2, tile_size / 2)
        self.key_f = img_loader('data/images/key_f.PNG', tile_size / 2, tile_size / 2)
        self.key_f_press = img_loader('data/images/key_f_press.PNG', tile_size / 2, tile_size / 2)
        self.key_shift = img_loader('data/images/key_shift.PNG', tile_size, tile_size / 2)
        self.key_shift_press = img_loader('data/images/key_shift_press.PNG', tile_size, tile_size / 2)

        self.key_images = {
            'left1': self.key_a,
            'left2': self.key_left,
            'right1': self.key_d,
            'right2': self.key_right,
            'left1_press': self.key_a_press,
            'left2_press': self.key_left_press,
            'right1_press': self.key_d_press,
            'right2_press': self.key_right_press,
            'interact1': self.key_x,
            'interact2': self.key_e,
            'interact3': self.key_slash,
            'interact1_press': self.key_x_press,
            'interact2_press': self.key_e_press,
            'interact3_press': self.key_slash_press,
            'jump1': self.key_space,
            'jump2': self.key_w,
            'jump3': self.key_up,
            'jump1_press': self.key_space_press,
            'jump2_press': self.key_w_press,
            'jump3_press': self.key_up_press,
            'shockwave1': self.key_z,
            'shockwave2': self.key_f,
            'shockwave3': self.key_shift,
            'shockwave1_press': self.key_z_press,
            'shockwave2_press': self.key_f_press,
            'shockwave3_press': self.key_shift_press,
        }

        self.left_key_image = self.key_images[f'left{settings_counters["walking"]}']
        self.right_key_image = self.key_images[f'right{settings_counters["walking"]}']
        self.left_key_press_image = self.key_images[f'left{settings_counters["walking"]}_press']
        self.right_key_press_image = self.key_images[f'right{settings_counters["walking"]}_press']

        self.interact_image = self.key_images[f'interact{settings_counters["interaction"]}']
        self.interact_image_press = self.key_images[f'interact{settings_counters["interaction"]}_press']

        self.jump_image = self.key_images[f'jump{settings_counters["jumping"]}']
        self.jump_image_press = self.key_images[f'jump{settings_counters["jumping"]}_press']

        self.shockwave_image = self.key_images[f'shockwave{settings_counters["shockwave"]}']
        self.shockwave_image_press = self.key_images[f'shockwave{settings_counters["shockwave"]}_press']

        self.mouse0 = img_loader('data/images/mouse0.PNG', tile_size / 2, tile_size)
        self.mouse1 = img_loader('data/images/mouse1.PNG', tile_size / 2, tile_size)
        self.mouse2 = img_loader('data/images/mouse2.PNG', tile_size / 2, tile_size)
        self.mouse3 = img_loader('data/images/mouse3.PNG', tile_size / 2, tile_size)

        self.inst_button_counter = 0
        self.inst_mouse_counter = 0

        # hey particle images ------------------------------------------------------------------------------------------
        self.hey_part1 = img_loader('data/images/hey_particle1.PNG', tile_size / 2.5, tile_size / 2.5)
        self.hey_part2 = img_loader('data/images/hey_particle2.PNG', tile_size / 2.5, tile_size / 2.5)
        self.hey_part3 = img_loader('data/images/hey_particle3.PNG', tile_size / 2.5, tile_size / 2.5)

        # healing animation list ---------------------------------------------------------------------------------------
        self.anim_list = []
        # 1 - speed
        # 2 - x position
        # 3 - y position

        # class initiations --------------------------------------------------------------------------------------------
        self.hey_particle1 = HeyParticle(self.hey_part1, self.hey_part2, self.hey_part3, self.sack_rect)
        self.circle_transition = CircleTransition(screen)
        self.shockwave = Shockwave(screen, controls)

    def update_pos_animation(self, screen, tile_list, next_level_list, level_count, trap_harm, bee_harm,
                             spit_harm_left, spit_harm_right, spit_harm_up, health, fps_adjust,
                             jump_boost_trigger, regeneration_trigger, mush_regeneration_trigger, no_gravity_trigger,
                             no_harm_trigger, left_border, right_border, game_counter,
                             move):

        dx = 0
        dy = 0

        if self.airborn:
            self.slide = 0.2
        else:
            self.slide = 0.4

        if self.vel_x_l < 0:
            self.vel_x_l += self.slide * fps_adjust
        else:
            self.vel_x_l = 0

        if self.vel_x_r > 0:
            self.vel_x_r -= self.slide * fps_adjust
        else:
            self.vel_x_r = 0

        self.restart_level = False

        key = pygame.key.get_pressed()

        # borders
        self.left_border = left_border
        self.right_border = right_border
        if level_count == 8:
            top_border = 80
        else:
            top_border = 50

        harm = False

        self.new_health_particles = False

        # music
        self.play_music = False
        self.fadeout = False

        if self.first_level_play_music:
            self.play_music = True
            self.first_level_play_music = False

        # setting all collisions to false
        self.top_col = False
        self.btm_col = False
        self.right_col = False
        self.left_col = False

        # new level cooldown, so the player can't move immediately after progressing to a new level
        self.new_level_cooldown += 1*fps_adjust

        self.health = health

        # turning the 'harm' boolean into a single variable
        if trap_harm or bee_harm or spit_harm_left or spit_harm_right or spit_harm_up:
            if self.teleport_count <= 100:
                harm = True
                self.new_health_particles = True

        # special power cards effects ----------------------------------------------------------------------------------
        if jump_boost_trigger and not self.jump_boost:
            self.jump_boost = True
            self.power_indicator_list.append('jump_boost')
        if (regeneration_trigger or mush_regeneration_trigger) and not self.regeneration:
            self.regeneration = True
        if no_gravity_trigger and not self.no_gravity:
            self.no_gravity = True
            self.power_indicator_list.append('no_gravity')
        if no_harm_trigger and not self.no_harm:
            self.no_harm = True
            self.power_indicator_list.append('no_harm')

        if self.regeneration:
            self.health = 2

        # updating special power cards counters ------------------------------------------------------------------------
        if self.jump_boost:
            self.jump_boost_counter += 1*fps_adjust
            self.particle_colour = (67, 124, 94)
            x_value = int(self.sack_rect.x)
            y_value = int(self.sack_rect.y)
            self.power_particle_list.append([random.randrange(x_value, x_value + self.sack_width),
                                             random.randrange(y_value, y_value + self.sack_height),
                                             random.randrange(6, 14),
                                             self.particle_colour])
        if self.regeneration:
            self.regeneration_counter += 1*fps_adjust
            self.particle_colour = (215, 24, 70)
            x_value = int(self.sack_rect.x)
            y_value = int(self.sack_rect.y)
            self.power_particle_list.append([random.randrange(x_value, x_value + self.sack_width),
                                             random.randrange(y_value, y_value + self.sack_height),
                                             random.randrange(6, 14),
                                             self.particle_colour])
        if self.no_gravity:
            self.no_gravity_counter += 1*fps_adjust
            self.particle_colour = (70, 161, 193)
            x_value = int(self.sack_rect.x)
            y_value = int(self.sack_rect.y)
            self.power_particle_list.append([random.randrange(x_value, x_value + self.sack_width),
                                             random.randrange(y_value, y_value + self.sack_height),
                                             random.randrange(6, 14),
                                             self.particle_colour])
        if self.no_harm:
            self.no_harm_counter += 1*fps_adjust
            self.particle_colour = (191, 117, 213)
            x_value = int(self.sack_rect.x)
            y_value = int(self.sack_rect.y)
            self.power_particle_list.append([random.randrange(x_value, x_value + self.sack_width),
                                             random.randrange(y_value, y_value + self.sack_height),
                                             random.randrange(6, 14),
                                             self.particle_colour])

        if self.jump_boost or self.regeneration or self.no_gravity or self.no_harm:
            self.power_particle_counter += 1 * fps_adjust

        # special power cards duration counters ------------------------------------------------------------------------
        if self.jump_boost_counter >= self.jump_boost_duration:
            self.jump_boost_counter = 0
            self.power_indicator_list.remove('jump_boost')
            self.jump_boost = False
        if self.no_gravity_counter >= self.no_gravity_duration:
            self.no_gravity_counter = 0
            self.power_indicator_list.remove('no_gravity')
            self.no_gravity = False
        if self.no_harm_counter >= self.no_harm_duration:
            self.no_harm_counter = 0
            self.power_indicator_list.remove('no_harm')
            self.no_harm = False

        # dealing with harm --------------------------------------------------------------------------------------------
        if self.no_harm:
            harm = False

        # subtracting health if player is being harmed
        if not self.harmed and harm:
            if self.health != 0:
                self.health -= 1
                # this variable is to prevent loosing more than one health point at once
                self.harmed = True
                self.init_flash = True

        if not harm:
            self.harmed = False

        if self.dead:
            self.sack_img = death_animation1(self, fps_adjust)

        # next level portal collisions ---------------------------------------------------------------------------------
        for tile in next_level_list:
            if tile[1].colliderect(self.sack_rect.x, self.sack_rect.y,
                                   self.sack_width, self.sack_height) and not self.dead:
                self.teleport_count += 1*fps_adjust
                if self.teleport_count >= 100:
                    if not self.transition:
                        self.circle_transition = CircleTransition(screen)
                        # music fadeout
                        self.fadeout = True
                    self.transition = True
                if self.teleport_count >= 130:
                    if self.jump_boost:
                        self.jump_boost_counter = 1000
                    if self.no_gravity:
                        self.no_gravity_counter = 1000
                    if self.no_harm:
                        self.no_harm_counter = 1000
                    level_count += 1
                    self.play_music = True
                    self.new_level = True
                    self.new_level_cooldown = 0
                    self.teleport_count = 0
                    self.player_moved = False
                    # player direction
                    self.direction = 1

        # movement and animation ---------------------------------------------------------------------------------------
        if self.new_level_cooldown >= 30 and not self.dead and self.teleport_count < 100\
                and not (self.col_types['right'] or self.col_types['left']) and game_counter >= 0 and move:
            # player control
            self.transition = False
            if key[self.controls['jump']] and not self.jumped:
                if self.jump_boost:
                    self.first_power_jump = True
                self.teleport_count = 0
                self.player_moved = True
                if not self.jumped and self.on_ground_counter > 0 and not self.airborn:
                    if self.jump_boost:
                        self.vel_y = -15
                    else:
                        self.vel_y = -11
                    self.jumped = True
                    self.animate_walk = False
                    self.airborn = True

            if not key[self.controls['jump']]:
                self.jumped = False
                if not self.airborn:
                    # standing animation
                    self.sack_offset = 0
                    if self.direction == 1:
                        self.blink_counter += 1*fps_adjust
                        if self.blink_counter > 150:
                            self.blink_counter = 0
                        if self.blink_counter > 75:
                            self.sack_img = self.sack0f
                        elif self.blink_counter > 60:
                            self.sack_img = self.sack_blinkf
                        elif self.blink_counter > 30:
                            self.sack_img = self.sack_lookf
                        elif self.blink_counter > 15:
                            self.sack_img = self.sack_blinkf
                        else:
                            self.sack_img = self.sack0f
                    elif self.direction == 0:
                        self.blink_counter += 1*fps_adjust
                        if self.blink_counter > 150:
                            self.blink_counter = 0
                        if self.blink_counter > 75:
                            self.sack_img = self.sack0b
                        elif self.blink_counter > 60:
                            self.sack_img = self.sack_blinkb
                        elif self.blink_counter > 30:
                            self.sack_img = self.sack_lookb
                        elif self.blink_counter > 15:
                            self.sack_img = self.sack_blinkb
                        else:
                            self.sack_img = self.sack0b

            if self.airborn and not self.col_types['bottom']:
                if self.direction == 1:
                    self.sack_offset = jump_offset_amount - 3
                    if self.vel_y < -5:
                        self.sack_img = self.sack_jump1f
                    elif -5 < self.vel_y < 3:
                        self.sack_img = self.sack_jump2f
                    else:
                        self.sack_img = self.sack_jump3f
                else:
                    self.sack_offset = jump_offset_amount + 4
                    if self.vel_y < -5:
                        self.sack_img = self.sack_jump1b
                    elif -5 < self.vel_y < 3:
                        self.sack_img = self.sack_jump2b
                    else:
                        self.sack_img = self.sack_jump3b

            walking_left = False
            walking_right = False

            # walking left
            if key[self.controls['left']]:
                self.player_moved = True
                walking_left = True
                self.speed_adder += 0.1 * fps_adjust
                self.speed += self.speed_adder
                if self.speed > 2.43:
                    self.speed = 2.43 * fps_adjust
                dx -= self.speed
                self.vel_x_l = dx
                self.vel_x_r = 0
                self.direction = 0
                self.teleport_count = 0
                if self.animate_walk:
                    self.walk_counter += 0.9 * fps_adjust
                    if self.walk_counter > 20:
                        self.walk_counter = 0
                    elif self.walk_counter > 15:
                        self.sack_img = self.sack2b
                    elif self.walk_counter > 10:
                        self.sack_img = self.sack0b
                    elif self.walk_counter > 5:
                        self.sack_img = self.sack1b
                    else:
                        self.sack_img = self.sack0b
            # walking right
            if key[self.controls['right']]:
                self.player_moved = True
                walking_right = True
                self.speed_adder += 0.1 * fps_adjust
                self.speed += self.speed_adder
                if self.speed > 2.43:
                    self.speed = 2.43 * fps_adjust
                dx += self.speed
                self.vel_x_r = dx
                self.vel_x_l = 0
                self.teleport_count = 0
                self.direction = 1
                if self.animate_walk:
                    self.walk_counter += 0.9 * fps_adjust
                    if self.walk_counter > 20:
                        self.walk_counter = 0
                    elif self.walk_counter > 15:
                        self.sack_img = self.sack2f
                    elif self.walk_counter > 10:
                        self.sack_img = self.sack0f
                    elif self.walk_counter > 5:
                        self.sack_img = self.sack1f
                    else:
                        self.sack_img = self.sack0f

            if not walking_right and not walking_left:
                self.speed = 0
                self.speed_adder = 0

            if walking_right and walking_left:
                self.speed = 0
                self.speed_adder = 0
                self.walk_counter = 0

        # respawn at the beginning of the level and transition
        if pygame.mouse.get_pressed()[0] and self.dead and self.dead_counter >= 36 and not self.restart_trigger:
            self.restart_trigger = True
            self.single_fadeout = True
            self.teleport_count = 0
            self.circle_transition = CircleTransition(screen)
            self.init_flash = False

        if self.restart_trigger:
            self.restart_counter += 1 * fps_adjust

        if self.restart_counter > 20:
            self.transition = True
            if self.single_fadeout:
                self.fadeout = True
                self.single_fadeout = False

        if self.restart_counter > 50 and self.single_restart:
            self.restart_level = True
            self.player_moved = False
            self.play_music = True
            self.single_restart = False

        if self.restart_counter > 80:
            self.restart_trigger = False
            self.restart_counter = 0
            self.single_restart = True

        self.col_types = {'left': False, 'right': False, 'top': False, 'bottom': False}

        # gravity ------------------------------------------------------------------------------------------------------
        if self.no_gravity:
            self.vel_y = dy
        else:
            self.vel_y += 0.6 * fps_adjust
            if self.vel_y > 8:
                self.vel_y = 8
        dy = self.vel_y*fps_adjust

        # collision detection and position -----------------------------------------------------------------------------
        hit_list_x = []
        self.vel_x = self.vel_x_l + self.vel_x_r
        temp_rect = self.sack_rect
        temp_rect.x += (self.vel_x + 0.5)

        if self.dead:
            x_adjust = 15
            sack_width = 2
        else:
            x_adjust = 0
            sack_width = self.sack_width

        for tile in tile_list:
            if tile[1].colliderect(temp_rect.x + x_adjust + dx, temp_rect.y, sack_width, self.sack_height):
                hit_list_x.append(tile)

        if self.sack_rect.x + 20 > self.right_border:
            if self.vel_x > 0:
                dx = 0
                self.vel_x_r = 0
                self.vel_x = 0
                self.sack_rect.x = self.right_border - 20
        if self.sack_rect.x < self.left_border:
            if self.vel_x < 0:
                dx = 0
                self.vel_x_l = 0
                self.vel_x = 0
                self.sack_rect.x = self.left_border

        for tile in hit_list_x:
            if self.vel_x > 0:
                self.sack_rect.right = tile[1].left
                dx = 0
                self.vel_x = 0
                self.vel_x_r = 0
                self.col_types['right'] = True
            if self.vel_x < 0:
                self.sack_rect.left = tile[1].right
                dx = 0
                self.vel_x = 0
                self.vel_x_l = 0
                self.col_types['left'] = True

        hit_list_y = []
        for tile in tile_list:
            if tile[1].colliderect(self.sack_rect.x + x_adjust, self.sack_rect.y + dy, sack_width, self.sack_height):
                hit_list_y.append(tile)

        self.on_ground_counter -= 1

        for tile in hit_list_y:
            if dy > 0:
                self.sack_rect.bottom = tile[1].top
                dy = 0
                self.vel_y = 0
                self.col_types['bottom'] = True
                self.airborn = False
                self.on_ground_counter = self.default_on_ground_counter
                self.animate_walk = True
            if dy < 0:
                self.sack_rect.top = tile[1].bottom
                dy = 0
                self.vel_y = 0
                self.col_types['top'] = True

        # next level position
        if self.new_level:
            self.sack_rect.y = 264/2 - 16
            self.direction = 1
            self.new_level = False

        # ensuring the player sprite is always in the middle level of the screen
        self.sack_rect.x = 164

        # preventing the player from falling out of the world
        if self.sack_rect.bottom > sheight:
            self.sack_rect.bottom = sheight
            dy = 0
        if self.sack_rect.top + dy < 0:
            self.sack_rect.top = 0
            dy = 0

        # updating hey particles ---------------------------------------------------------------------------------------
        self.hey_particle1.update_particle(self.sack_rect, fps_adjust, self.new_level,
                                           self.camera_movement_x, self.camera_movement_y)

        # updating player coordinates ----------------------------------------------------------------------------------
        self.camera_movement_x = round(-self.vel_x)
        dx = 0
        if self.sack_rect.y > 180 and dy*fps_adjust > 0:
            self.camera_movement_y = round(-dy)
        elif self.sack_rect.y < top_border and dy*fps_adjust < 0:
            self.camera_movement_y = round(-dy)
        else:
            self.camera_movement_y = round(-dy/2)
            self.sack_rect.y += round(dy/2)

        self.dx = dx
        self.dy = dy

        # resetting player health --------------------------------------------------------------------------------------
        if self.restart_level:
            self.dead = False
            self.health = 2
            self.dead_counter = 0

        # returns ------------------------------------------------------------------------------------------------------
        return level_count, self.sack_rect, self.direction, self.health,\
               self.camera_movement_x, self.camera_movement_y, self.play_music,\
               self.fadeout, self.restart_level, self.player_moved, self.new_level_cooldown

# UPDATING PLAYER SPRITE HEALTH ========================================================================================
    def update_health(self, screen, fps_adjust, mouse_adjustment):
        sound_trigger = False

        if self.dead:
            self.health = 0
        if self.health == 2:
            self.health_bar = self.bar_full_health
        elif self.health == 1:
            self.health_bar = self.bar_half_health
            self.health_part_x = tile_size * 2 - 20
        elif self.health == 0:
            self.health_bar = self.bar_no_health
            self.dead = True
            if self.jump_boost:
                self.jump_boost_counter = 1000
            if self.no_gravity:
                self.no_gravity_counter = 1000
            if self.no_harm:
                self.no_harm_counter = 1000
            self.health_part_x = tile_size - 5

        screen.blit(self.health_bar_card, (0, 0))

        screen.blit(self.health_bar, (0, 8))

        if self.health >= 0:
            health_bar_particles(screen, fps_adjust, self.health_bar_part_list, self.health_part_x,
                                 self.health_part_y, self.new_health_particles)

        return sound_trigger

# displaying the currently used power icon -----------------------------------------------------------------------------
    def player_power_indicator(self, screen):
        spacer = 0
        for icon in self.power_indicator_list:
            if icon == 'jump_boost':
                percentage = self.jump_boost_duration / self.jump_boost_counter
                bar_y = int(18 / percentage)
                self.jump_boost_surf.blit(self.jump_boost_indicator, (0, 0))
                self.jump_boost_surf.blit(self.progress_bar, (0, bar_y + 8))
                self.jump_boost_surf.set_colorkey((0, 0, 0))
                screen.blit(self.jump_boost_surf, (2*tile_size + spacer, 0))
            elif icon == 'no_gravity':
                percentage = self.no_gravity_duration / self.no_gravity_counter
                bar_y = int(18 / percentage)
                self.no_gravity_surf.blit(self.no_gravity_indicator, (0, 0))
                self.no_gravity_surf.blit(self.progress_bar, (0, bar_y + 8))
                self.no_gravity_surf.set_colorkey((0, 0, 0))
                screen.blit(self.no_gravity_surf, (2*tile_size + spacer, 0))
            elif icon == 'no_harm':
                percentage = self.no_harm_duration / self.no_harm_counter
                bar_y = int(18 / percentage)
                self.no_harm_surf.blit(self.no_harm_indicator, (0, 0))
                self.no_harm_surf.blit(self.progress_bar, (0, bar_y + 8))
                self.no_harm_surf.set_colorkey((0, 0, 0))
                screen.blit(self.no_harm_surf, (2*tile_size + spacer, 0))
            spacer += 32

# BLITTING PLAYER SPRITE ONTO THE SCREEN ===============================================================================
    def blit_player(self, screen, draw_hitbox, fps_adjust):
        particle_x = self.sack_rect.x - 8
        self.init_flash = False

        # player flickering when taking damage (not in use because it doesn't look that good)
        if self.init_flash and self.health > 0:
            self.harm_counter -= 1
            self.harm_flash_counter += 1
            if self.harm_flash_counter >= 6:
                self.blit_plr = not self.blit_plr
                self.harm_flash_counter = 0
            if self.harm_counter <= 0:
                self.init_flash = False
                self.harm_counter = 60
                self.harm_flash_counter = 0
        else:
            self.blit_plr = True

        # power particles
        self.power_particle_surface.fill((0, 0, 0))

        for particle in self.power_particle_list:
            particle[2] -= 0.3
            particle[0] += self.camera_movement_x
            particle[1] += self.camera_movement_y
            pygame.draw.circle(self.power_particle_surface, particle[3], (particle[0], particle[1]), particle[2])

        self.power_particle_surface.set_colorkey((0, 0, 0))
        screen.blit(self.power_particle_surface, (0, 0))

        # drawing player onto the screen
        if self.blit_plr:
            screen.blit(self.sack_img, (self.sack_rect.x - self.sack_offset, self.sack_rect.y))

        # refilling health if regeneration card used
        if self.regeneration:
            self.health = 2
            self.regeneration_counter += (1 * fps_adjust)/4
            if self.regeneration_counter > 60:
                self.regeneration = False
                self.regeneration_counter = 0
                self.anim_list = []

        if draw_hitbox:
            pygame.draw.rect(screen, (255, 255, 255), self.sack_rect, 1)

        # hey particles
        self.hey_particle1.blit_particle(screen)

        # drawing teleportation particles onto the screen
        if not self.dead and self.teleport_count > 20:
            magic_animation(self, screen, self.teleport_count, particle_x)

# inter-level transition -----------------------------------------------------------------------------------------------
    def draw_transition(self, fps_adjust):
        if self.transition:
            self.circle_transition.draw_circle_transition(self.sack_rect, fps_adjust)

# respawn instructions -------------------------------------------------------------------------------------------------
    def blit_respawn_instructions(self, screen, fps_adjust):
        if self.health == 0 and self.dead_counter >= 36 and self.restart_counter == 0:
            self.respawn_instructions_blit_counter += 1 * fps_adjust

            if self.respawn_instructions_blit_counter > 54:
                self.respawn_instructions_blit_counter = 0
                img = self.respawn_instr1
            elif self.respawn_instructions_blit_counter > 44:
                img = self.respawn_instr2
            else:
                img = self.respawn_instr1

            screen.blit(img, (swidth / 2 - tile_size, sheight / 3 - (tile_size / 2)))

# draws control instruction buttons ------------------------------------------------------------------------------------
    def draw_inst_buttons(self, screen, fps_adjust, level_count, world_count):
        self.inst_mouse_counter += 1 * fps_adjust
        self.inst_button_counter += 1 * fps_adjust

        if not self.player_moved:
            first_key_x = self.sack_rect.x - 55
            y = self.sack_rect.y - 40
            key_size = 16
            gap = 3
            key_press_len = 15
            # controls: mouse
            if self.inst_mouse_counter > 60:
                self.inst_mouse_counter = 0
                mouse_img = self.mouse0
            elif self.inst_mouse_counter > 40:
                mouse_img = self.mouse0
            elif self.inst_mouse_counter > 30:
                mouse_img = self.mouse3
            elif self.inst_mouse_counter > 20:
                mouse_img = self.mouse2
            elif self.inst_mouse_counter > 10:
                mouse_img = self.mouse1
            else:
                mouse_img = self.mouse0
            # controls: buttons
            key_left = self.left_key_image
            key_right = self.right_key_image
            key_x = self.interact_image
            key_z = self.shockwave_image
            key_space = self.jump_image
            if self.inst_button_counter > 250:
                self.inst_button_counter = 0
            elif 220 + key_press_len > self.inst_button_counter > 220:
                key_x = self.interact_image_press
            elif 170 + key_press_len > self.inst_button_counter > 170:
                key_z = self.shockwave_image_press
            elif 120 + key_press_len > self.inst_button_counter > 120:
                key_space = self.jump_image_press
            elif 70 + key_press_len > self.inst_button_counter > 70:
                key_right = self.right_key_press_image
            elif 20 + key_press_len > self.inst_button_counter > 20:
                key_left = self.left_key_press_image

            if self.settings_counters['jumping'] == 1:
                space_size = key_size
            else:
                space_size = 0

            if self.settings_counters['shockwave'] == 3:
                shock_size = key_size
            else:
                shock_size = 0

            # blitting the controls onto the screen (I could've done it a better way)
            screen.blit(key_z, (first_key_x, y))
            screen.blit(key_x, (first_key_x + key_size + shock_size + gap, y))
            screen.blit(key_space, (first_key_x + (2 * key_size + shock_size) + (2 * gap), y))
            screen.blit(key_left, (first_key_x + (3 * key_size + space_size + shock_size) + (3 * gap), y))
            screen.blit(key_right, (first_key_x + (4 * key_size + space_size + shock_size) + (4 * gap), y))
            screen.blit(mouse_img, (first_key_x + (5 * key_size + space_size + shock_size) + (6 * gap), y - 5))

        if level_count == 1 and not self.first_power_jump and self.jump_boost:
            if self.inst_button_counter >= 30:
                img = self.key_space_press
                if self.inst_button_counter >= 40:
                    self.inst_button_counter = 0
            else:
                img = self.key_space

            screen.blit(img, (swidth/2 - tile_size/2, sheight/3 - tile_size/4))

